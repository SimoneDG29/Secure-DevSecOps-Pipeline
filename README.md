# Secure CI/CD Pipeline for Flask Microservices with DevSecOps Controls

![Python](https://img.shields.io/badge/python-3.12-blue)
![Docker](https://img.shields.io/badge/docker-enabled-blue)
![Kubernetes](https://img.shields.io/badge/kubernetes-ready-blue)
![Helm](https://img.shields.io/badge/helm-enabled-blue)
![Security](https://img.shields.io/badge/devsecops-integrated-green)

## Table of Contents
- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Microservices](#microservices)
- [Infrastructure & Orchestration](#infrastructure--orchestration)
- [CI/CD Pipeline](#cicd-pipeline)
- [Pipeline Flow](#pipeline-flow)
- [Security Controls](#security-controls)
- [Local Development](#local-development)
- [Deployment Guide](#deployment-guide)
- [Testing](#testing)
- [Repository Structure](#repository-structure)
- [Roadmap](#roadmap)
- [References](#references)

---

# Project Overview

This project simulates a production-inspired DevSecOps workflow for a Flask-based microservices application.

The main goal is to demonstrate:

- secure CI/CD automation with GitHub Actions
- container supply chain security
- Kubernetes deployment workflows
- container image signing
- SBOM generation
- layered security gates before deployment

This repository is intended as a hands-on DevOps / DevSecOps portfolio project.

**Tech stack:**

- Python / Flask
- Docker
- Kubernetes
- Helm
- GitHub Actions
- Semgrep
- Trivy
- Cosign
- OWASP ZAP
- Dependabot
- SBOM

---

# Architecture

## High-level flow

```text
GitHub Actions
   ↓
Lint/Test
   ↓
Semgrep SAST
   ↓
Dependency Scan (Trivy FS)
   ↓
Helm Lint
   ↓
Build Docker Images
   ↓
Trivy Scan
   ↓
Push to GHCR
   ↓
Cosign Sign
   ↓
OWASP ZAP Full Scan (DAST)
   ↓
Release-ready signed images
   ├── SBOM Generation
   └── Helm Deploy to Kubernetes
```

## Service architecture

```text
services
   ├── auth-service
   ├── api-service
   ├── products-service
   ├── inventory-service
   └── frontend-service
```

---

# Microservices

| Service | Description | Tech Stack | Port |
|---|---|---|---|
| auth-service | Authentication logic | Flask | 5001 |
| api-service | Main API gateway | Flask | 5002 |
| products-service | Product catalog management | Flask + PostgreSQL | 5003 |
| inventory-service | Inventory state management | Flask + Redis | 5004 |
| frontend-service | React/Vite frontend UI | React + Vite + Nginx | 5173 |

Each service contains:

- dedicated Dockerfile
- isolated requirements
- unit/integration tests

---

# Infrastructure & Orchestration

## Containerization
- Docker images built per service.

## Image registry
- GitHub Container Registry (GHCR).

## Orchestration
- Kubernetes.

Supported local clusters:

- kind
- minikube

## Deployment
- Helm charts located in:

```bash
infrastructure/helm/secure-pipeline/
```

## External dependencies
- PostgreSQL
- Redis

---

# CI/CD Pipeline

Implemented with:

```bash
.github/workflows/ci.yml
```

## Pipeline jobs

### Validation jobs
- lint-test
- semgrep
- dependency-scan
- helm-lint

### Build/security jobs
- build-and-scan-images
- sign-images
- zap-dast
- sbom

### Manual operational jobs
- deploy

---

## CI/CD Optimization

This project includes a set of CI/CD optimizations aimed at improving pipeline performance, scalability, and maintainability.

The main focus is reducing execution time and eliminating redundant workload across microservices-based workflows.

## Matrix-based Parallel Execution

The pipeline uses **GitHub Actions matrix strategy** to parallelize repetitive operations across microservices.

### Before optimization

Without matrix strategy:

- Each service was processed sequentially
- Repeated YAML blocks for each microservice
- Longer CI execution time due to serial processing

### After optimization

The pipeline was refactored to use a matrix strategy:

- Parallel execution of tests across all services
- Parallel Docker image builds
- Parallel image security scanning
- Parallel SBOM generation

### Example implementation

```yaml
strategy:
  matrix:
    service:
      - auth-service
      - api-service
      - products-service
      - inventory-service
      - frontend-service
```

### Benefits

- Reduced CI execution time through parallelization
- Improved scalability for additional microservices
- Reduced YAML duplication and improved maintainability
- Better utilization of GitHub Actions runners

## Caching Strategy

The pipeline implements a multi-layer caching strategy to reduce execution time and CI costs.

### Pip cache (Python dependencies)
Using `actions/setup-python@v5` with pip caching enabled:

```yaml
with:
  cache: "pip"
  cache-dependency-path: |
    services/${{ matrix.service }}/requirements.txt
    services/${{ matrix.service }}/requirements-dev.txt
```
- Cache is automatically restored per service
- A new cache key is generated only when requirements files change
- Each matrix service gets an isolated cache (no conflicts)

## Trivy cache

Vulnerability DB caching is enabled via `actions/cache`:

- Speeds up filesystem and image scans
- Stores vulnerability database locally on runner cache directory
- Reused across workflow runs

## Docker Build cache

Enabled via GitHub Actions cache backend:

```yaml
cache-from: type=gha,scope=${{ matrix.service }}
cache-to: type=gha,mode=max,scope=${{ matrix.service }}
```
- Reuses intermediate image layers
- Scoped per service to avoid cross-service contamination
- Significantly reduces build time in matrix builds

### Benefits

- Faster CI execution on repeated runs
- Reduced dependency re-installation
- Optimized Docker rebuilds per service

## Concurrency Control

The pipeline uses GitHub Actions concurrency to prevent redundant workflow executions and reduce CI costs.

```yaml
concurrency:
  group: ci-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```
- Ensures only one running workflow per branch and workflow at a time
- Automatically cancels previous runs when a new commit is pushed
- Prevents duplicated executions of expensive jobs (Docker builds, Trivy scans, OWASP ZAP)

### Benefits

- Reduces CI execution time and resource usage
- Avoids redundant builds and security scans
- Improves feedback loop speed during active development
- Prevents overlapping deployments in fast commit scenarios

## Path Filtering & Dynamic Matrix Generation

This pipeline introduces **path-based filtering combined with dynamic matrix generation** to ensure that only the necessary microservices are processed during CI execution.

This optimization reduces redundant work by avoiding builds, tests, and scans for services that have not changed.

### Before optimization

Without path filtering and dynamic matrix:

- All microservices were always included in CI runs
- Tests, builds, and scans executed even if no relevant code changed
- Wasted compute time on unaffected services
- Fixed static matrix required manual updates when adding services

### After optimization

The pipeline dynamically determines which services changed using `dorny/paths-filter` and builds a runtime matrix:

- Only modified services are included in the CI matrix
- Downstream jobs (tests, builds, scans) run only for affected services
- Helm changes are detected separately for infrastructure validation
- Fully automated service discovery based on Git changes

### Example implementation

```yaml
- name: Filter changed services
  uses: dorny/paths-filter@v3
  with:
    filters: |
      auth-service:
        - 'services/auth-service/**'
      api-service:
        - 'services/api-service/**'
      products-service:
        - 'services/products-service/**'
      inventory-service:
        - 'services/inventory-service/**'
      frontend-service:
        - 'services/frontend-service/**'
      helm:
        - 'infrastructure/helm/**'
```

### Dynamic matrix generation

The filtered results are transformed into a **dynamic JSON matrix** used by GitHub Actions:

```yaml
strategy:
  matrix: ${{ fromJson(needs.detect-changes.outputs.matrix) }}
```

This allows jobs to scale automatically based on actual changes:

- If 1 service changes → 1 parallel job
- If 3 services change → 3 parallel jobs
- If no services change → downstream jobs are skipped

### Optional change flag optimization

A `has_changes` flag is introduced to simplify conditional execution:

```yaml
if: needs.detect-changes.outputs.has_changes == 'true'
```

This improves readability and avoids repeated JSON comparisons across jobs.

### Benefits

- Eliminates unnecessary CI execution for unchanged services
- Reduces pipeline runtime significantly in partial-change scenarios
- Enables fully automatic scaling of CI workloads
- Improves maintainability by removing static service lists from jobs
- Keeps CI aligned with repository structure without manual updates

---

# Pipeline Flow

## Pull Request workflow

Runs automatically on PR:

1. lint-test
2. semgrep
3. dependency-scan
4. helm-lint

Purpose:

- validate code quality
- run tests
- run SAST
- scan project dependencies before container builds
- validate Helm charts

No images are built or deployed.

---

## Push to main workflow

Runs automatically on merge/push to `main`:

1. lint-test
2. semgrep
3. dependency-scan
4. helm-lint
5. build-and-scan-images
6. sign-images
7. zap-dast
8. sbom

Purpose:

- build release-ready images
- vulnerability scan
- publish signed images to GHCR
- run DAST (OWASP ZAP) before deployment
- generates SBOM artifacts for all images.

---

## Manual workflows

Triggered via `workflow_dispatch`.

### deploy
Deploys services via Helm.

This separation avoids automatic deployments during active development.

---

# Security Controls

## Static Analysis (SAST)

Using **Semgrep**.

Rules include:

- blocking `eval()`
- blocking dangerous subprocess patterns

---

## Vulnerability Scanning

Using **Trivy** in two stages.

### Dependency scanning (filesystem scan)

Runs before Docker image builds.

Purpose:

- detect vulnerable dependencies early
- fail fast before container builds
- reduce CI/CD resource waste

Scans include:

- Python requirements
- npm packages
- lockfiles

---

### Container image scanning

Runs after Docker image builds.

Purpose:

- scan final runtime images
- detect OS-level vulnerabilities
- validate container security posture

Pipeline fails on:

- HIGH vulnerabilities
- CRITICAL vulnerabilities

with:

```bash
--exit-code 1
```

---

## Dependency Management

Using **Dependabot** for automated dependency update monitoring.

Purpose:

- detect outdated dependencies
- receive automated update PRs
- reduce exposure to known vulnerable packages

## Image Signing
Using **Cosign** keyless signing.

Purpose:

- supply chain integrity
- provenance verification

---

## Dynamic Application Security Testing (DAST)

Using **OWASP ZAP** in CI pipeline.

The pipeline includes a full-stack DAST scan executed after deployment in Docker Compose.

### Features

- Full application scan of running environment
- Fail pipeline on:
  - High confidence HIGH/CRITICAL findings
  - Excessive medium-confidence vulnerabilities
- Reports generated in:
  - HTML format (`zap-report.html`)
  - JSON format (`zap-report.json`)

---

## SBOM Generation

The SBOM is generated automatically for all services on every push to `main`.
Uses Anchore SBOM action.

Artifacts are generated in SPDX JSON format and published as workflow artifacts.

Purpose:

- dependency transparency
- auditability

---


## Secure Containers

All services:

- run as non-root users
- use slim Python base images

---

These controls implement a layered DevSecOps pipeline covering:

- application security (SAST)
- dependency security (Trivy FS + Dependabot + SBOM)
- container security (Trivy)
- supply chain integrity (Cosign signing)
- secure deployment practices (Kubernetes)
- runtime security testing (OWASP ZAP)

---

# Local Development

## Requirements

- Docker
- Docker Compose
- Python 3.12

---

## Start services locally

```bash
docker-compose up --build
```

---

## Run tests

Example:

```bash
pytest services/products-service/tests
```

---

## Environment variables

Local development uses:

```bash
.env
```

Production uses:

- GitHub Secrets
- Kubernetes Secrets

---

# Deployment Guide

## Local Kubernetes deployment

Supported:

- kind
- minikube

Deploy manually:

1. Run `deploy`

---

## Notes

GitHub-hosted runners cannot access local clusters.

For real deployment, adapt to:

- AWS EKS
- GKE
- AKS

and provide:

- kubeconfig
- reachable cluster

---

# Testing

Each service contains dedicated tests.

Current testing:

- unit tests
- integration-like API tests using Flask test client
- mocked Redis/Postgres dependencies

Security testing:

- Semgrep
- Trivy
- OWASP ZAP

---

# Repository Structure

```bash
services/
  auth-service/
  api-service/
  products-service/
  inventory-service/
  frontend-service/

infrastructure/
  helm/
    secure-pipeline/
  kubernetes/

.github/
  workflows/
    ci.yml
  dependabot.yml

docker-compose.yml
.semgrep.yml
README.md
LICENSE
```

---

# Roadmap

## Completed

- [x] Multi-service Flask architecture
- [x] Dockerized services
- [x] GitHub Actions CI/CD
- [x] Semgrep SAST
- [x] Early dependency vulnerability scanning
- [x] Trivy image scanning
- [x] GHCR image publishing
- [x] Cosign image signing
- [x] Helm deployment
- [x] SBOM generation
- [x] OWASP ZAP DAST

---

## Planned Improvements

### Kubernetes Admission Security

Future integration:

- signature verification before deploy
- admission policies

Possible tooling:

- Cosign verify
- Kyverno / admission controller policies

---

# References

- GitHub Actions: https://docs.github.com/en/actions
- Kubernetes: https://kubernetes.io/docs/
- Helm: https://helm.sh/docs/
- Semgrep: https://semgrep.dev/
- Trivy: https://aquasecurity.github.io/trivy/
- Cosign: https://docs.sigstore.dev/cosign/signing/overview/
- OWASP ZAP: https://www.zaproxy.org/
- Dependabot: https://docs.github.com/en/code-security/dependabot