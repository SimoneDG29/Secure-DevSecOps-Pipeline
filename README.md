# Secure CI/CD Pipeline for Microservices

This project is a hands-on demonstration of a secure CI/CD pipeline for a microservices-based application. It is designed to be built incrementally, with each step introducing new security controls and DevSecOps best practices.

## Project Goal

The goal is to build a complete, secure software supply chain using GitHub Actions, Docker, Kubernetes, and various open-source security tools.

## Architecture

- **Microservices**: Two simple services (`auth-service` and `api-service`).
- **Containerization**: Docker.
- **Orchestration**: Kubernetes (local cluster via `kind` or `minikube`).
- **Deployment**: Helm charts.
- **CI/CD**: GitHub Actions.

## Current Status

- **Services**: `auth-service` and `api-service` (Flask) with basic health endpoints.
- **Docker**: Dockerfiles for both services (non-root).
- **Local runtime**: `docker-compose.yml` with Redis.
- **CI**: GitHub Actions pipeline with tests and Docker builds.
- **SAST**: Semgrep scan with a minimal ruleset.
- **Container Scanning**: Trivy (fail on HIGH/CRITICAL).
- **Image signing**: Cosign keyless signing via GitHub OIDC.
- **SBOM**: Manual generation via `workflow_dispatch`.
- **Dependency updates**: Dependabot (weekly) — currently disabled to avoid PRs.

## Repo Structure

```
services/
  auth-service/
  api-service/
infrastructure/
  helm/
  kubernetes/
.github/workflows/
```

*This README is a work in progress and will be updated as the project evolves.*
