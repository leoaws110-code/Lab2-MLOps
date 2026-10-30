# Lab 2: Bring Your Own Model - Container + CI

[![CI Pipeline](https://github.com/leoaws110-code/Lab2-MLOps/actions/workflows/ci.yml/badge.svg)](https://github.com/leoaws110-code/Lab2-MLOps/actions/workflows/ci.yml)

## Overview
This repository implements a production-ready machine learning service using FastAPI, packaged with a multi-stage non-root Docker container, and automatically tested and scanned via a GitHub Actions CI pipeline.

## Features
- **FastAPI Service**: Serves ML model predictions with input validation using Pydantic.
- **Automated Testing**: Unit tests implemented with `pytest` covering model inference, edge cases, and health checks.
- **Containerization**: Multi-stage Docker build optimized for size and security (runs as non-root user).
- **CI/CD Pipeline**: GitHub Actions workflow that automatically runs tests, scans container vulnerabilities with Trivy, and pushes valid images to GitHub Container Registry (GHCR).

## Quick Start (Run Locally)

### 1. Run with Docker
```bash
docker build -t lab2-mlops .
docker run -p 8000:8000 lab2-mlops
```
### 2. Health Check
```bash
curl http://localhost:8000/health
```
### 3. Run Tests
```bash
pytest -v
```