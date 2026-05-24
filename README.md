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
- secret management
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
   ├── Manual SBOM Generation
   ├── Manual Secret Creation
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

### Manual operational jobs
- create-secrets
- deploy
- sbom

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

Purpose:

- build release-ready images
- vulnerability scan
- publish signed images to GHCR
- run DAST (OWASP ZAP) before deployment

---

## Manual workflows

Triggered via `workflow_dispatch`.

### create-secrets
Creates Kubernetes secrets from GitHub Secrets.

### deploy
Deploys services via Helm.

### sbom
Generates SBOM artifacts for all images.

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

Using Anchore SBOM action.

Artifacts generated in SPDX JSON format.

Purpose:

- dependency transparency
- auditability

---

## Secret Management

Secrets are not committed.

Sensitive values are injected from GitHub Secrets into Kubernetes Secrets.

Examples:

- PRODUCTS_DB_HOST
- PRODUCTS_DB_PORT
- PRODUCTS_DB_NAME
- PRODUCTS_DB_USER
- PRODUCTS_DB_PASSWORD

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
- secure deployment practices (Kubernetes + Secrets management)
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

1. Run `create-secrets`
2. Run `deploy`

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
- [x] Kubernetes secret management
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