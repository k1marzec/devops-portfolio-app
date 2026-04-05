# DevOps Portfolio - Todo Application

[![CI/CD Pipeline](https://github.com/k1marzec/devops-portfolio-app/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/k1marzec/devops-portfolio-app/actions/workflows/ci-cd.yml)
[![Docker Tests](https://github.com/k1marzec/devops-portfolio-app/actions/workflows/docker-test.yml/badge.svg)](https://github.com/k1marzec/devops-portfolio-app/actions/workflows/docker-test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)

A comprehensive DevOps portfolio project demonstrating modern software development and deployment practices — including hybrid CI/CD pipelines, Infrastructure as Code, containerization, and cloud deployment on Microsoft Azure.

**Live Demo (provisioned via Terraform):** https://todo-app-karolina-21733.azurewebsites.net

---

## Architecture Overview

The project uses a **dual-pipeline architecture** separating application CI from infrastructure deployment:

```
┌─────────────────────────────────────────────────────────┐
│                     GitHub Repository                   │
└────────────────────┬────────────────────────────────────┘
                     │ git push
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
┌─────────────────┐   ┌──────────────────────┐
│  GitHub Actions │   │       Jenkins        │
│  (App CI/CD)    │   │  (Infrastructure CD) │
│                 │   │                      │
│ - Unit tests    │   │ - Terraform plan     │
│ - Integration   │   │ - Terraform apply    │
│   tests         │   │ - Azure provisioning │
│ - Security scan │   │ - Remote state mgmt  │
│   (Trivy)       │   │   (Azure Storage)    │
│ - Docker build  │   └──────────────────────┘
│ - Push to       │             │
│   Docker Hub    │             ▼
└─────────────────┘   ┌──────────────────────┐
          │           │   Microsoft Azure    │
          └──────────►│   App Service        │
                      │   (containerized)    │
                      └──────────────────────┘
```

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API    │    │   Database      │
│   (HTML/CSS/JS) │◄──►│   (Flask)        │◄──►│   (PostgreSQL)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                 │
                    ┌────────────────────┐
                    │   Docker Compose   │
                    └────────────────────┘
```

---

## Technology Stack

### Backend
- **Flask 2.3.3** — Web framework
- **SQLAlchemy** — ORM and database toolkit
- **PostgreSQL 15** — Primary database
- **Gunicorn** — WSGI HTTP Server

### DevOps & Infrastructure
- **Docker** — Containerization (multi-stage builds)
- **Docker Compose** — Multi-container orchestration
- **Kubernetes** — Local cluster orchestration (Deployments, Services)
- **GitHub Actions** — Application CI/CD pipeline
- **Jenkins (Groovy)** — Infrastructure deployment pipeline
- **Terraform (HCL)** — Infrastructure as Code (Azure provider)
- **Azure Storage Account** — Terraform remote backend for state management
- **Microsoft Azure** — Cloud deployment (App Service, IAM/RBAC, CLI)
- **Docker Hub** — Container registry
- **Trivy** — Security scanning
- **pytest** — Testing framework

---

## CI/CD Pipeline Details

### Pipeline 1 — GitHub Actions (Application CI/CD)

Triggered on every push to `main`. Handles application-level automation:

1. **Test Stage** — Unit and integration tests, code linting (flake8), PostgreSQL integration testing
2. **Security Stage** — Vulnerability scanning with Trivy, SARIF report generation
3. **Build Stage** — Multi-stage Docker image build, push to Docker Hub, image caching
4. **Deploy Stage** — Deployment to Azure App Service, smoke tests, deployment verification

### Pipeline 2 — Jenkins (Infrastructure CD)

Handles all Terraform-based infrastructure operations:

1. **Terraform Init** — Initializes with Azure Storage Account as remote backend
2. **Terraform Plan** — Previews infrastructure changes
3. **Terraform Apply** — Provisions Azure resources (Web Apps, Service Plans, Resource Groups)
4. **Secrets Management** — Azure Service Principals (RBAC) injected via Jenkins Credentials Provider — no credentials exposed in code

---

## Infrastructure as Code (Terraform)

Azure infrastructure is fully managed via Terraform:

- **Remote Backend** — Terraform state stored in Azure Storage Account (secure, team-ready, eliminates local state drift)
- **Resources provisioned** — Azure Web App, App Service Plan, Resource Group
- **Executed via Jenkins** — Every infrastructure change goes through the Jenkins pipeline

---

## Security

- Azure Service Principals with RBAC for least-privilege access
- Jenkins Credentials Provider for secret injection (no hardcoded credentials)
- Trivy vulnerability scanning on every build
- Non-root user execution in Docker containers
- HTTPS enforced on Azure App Service

---

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.11+
- Git

### Running with Docker (Recommended)

```bash
git clone https://github.com/k1marzec/devops-portfolio-app.git
cd devops-portfolio-app
docker-compose up --build
# Access at http://localhost:5000
```

### Local Development

```bash
git clone https://github.com/k1marzec/devops-portfolio-app.git
cd devops-portfolio-app
pip install -r requirements-dev.txt
python run.py
```

---

## Testing

```bash
# Unit tests
python run_tests.py

# Manual integration tests
python manual_test.py

# Docker-based tests
docker-compose -f docker-compose.test.yml up --build
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main todo list interface |
| `/add` | GET/POST | Add new task |
| `/complete/<id>` | POST | Toggle task completion |
| `/delete/<id>` | POST | Delete task |
| `/api/tasks` | GET | JSON API for tasks |
| `/health` | GET | Health check endpoint |

---

## Monitoring & Observability

- `/health` endpoint for service-level health checks
- Docker-level health checks on all containers
- Structured JSON logging for log analysis
- Custom application metrics and performance tracking

---

## Docker

Multi-stage Dockerfile for optimized production images:
- **Builder stage** — Compiles dependencies
- **Production stage** — Minimal runtime image with security hardening (non-root user, health checks, proper signal handling)

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Application environment | `development` |
| `DATABASE_URL` | Database connection string | `sqlite:///app.db` |
| `SECRET_KEY` | Flask secret key | `dev-secret-key` |

---

## License

MIT License — see [LICENSE](LICENSE) for details.
