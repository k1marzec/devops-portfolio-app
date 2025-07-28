# DevOps Portfolio - Todo Application

[![CI/CD Pipeline](https://github.com/k1marzec/devops-portfolio-app/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/k1marzec/devops-portfolio-app/actions/workflows/ci-cd.yml)
[![Docker Tests](https://github.com/k1marzec/devops-portfolio-app/actions/workflows/docker-test.yml/badge.svg)](https://github.com/k1marzec/devops-portfolio-app/actions/workflows/docker-test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)

A comprehensive DevOps portfolio project demonstrating modern software development and deployment practices.

## 🚀 Features

- **Full-Stack Web Application**: Flask-based todo application with PostgreSQL
- **Containerization**: Multi-stage Docker builds with Docker Compose orchestration
- **CI/CD Pipeline**: Automated testing, security scanning, and deployment
- **Infrastructure as Code**: Reproducible environments and deployments
- **Monitoring & Logging**: Health checks, structured logging, and observability
- **Security**: Vulnerability scanning with Trivy, secure container practices
- **Testing**: Unit tests, integration tests, and smoke tests

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API    │    │   Database      │
│   (HTML/CSS/JS) │◄──►│   (Flask)        │◄──►│   (PostgreSQL)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌──────────────────┐
                    │   Docker         │
                    │   Compose        │
                    └──────────────────┘
```

## 🛠️ Technology Stack

### Backend
- **Flask 2.3.3** - Web framework
- **SQLAlchemy** - ORM and database toolkit
- **PostgreSQL 15** - Primary database
- **Gunicorn** - WSGI HTTP Server

### DevOps & Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration  
- **GitHub Actions** - CI/CD pipeline
- **Trivy** - Security scanning
- **pytest** - Testing framework

### Development Tools
- **Python 3.11** - Programming language
- **pip** - Package management
- **Git** - Version control

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)
- Git

### Running with Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/k1marzec/devops-portfolio-app.git
cd devops-portfolio-app

# Start the application
docker-compose up --build

# Access the application
open http://localhost:5000
```

### Local Development

```bash
# Clone and setup
git clone https://github.com/k1marzec/devops-portfolio-app.git
cd devops-portfolio-app

# Install dependencies
pip install -r requirements-dev.txt

# Run the application
python run.py

# Run tests
python manual_test.py
```

## 🧪 Testing

The project includes comprehensive testing at multiple levels:

### Unit Tests
```bash
python run_tests.py
```

### Manual Integration Tests
```bash
python manual_test.py
```

### Docker Tests
```bash
docker-compose -f docker-compose.test.yml up --build
```

## 🏭 CI/CD Pipeline

The project uses GitHub Actions for automated CI/CD with the following stages:

1. **Test Stage**
   - Unit and integration tests
   - Code linting with flake8
   - PostgreSQL integration testing

2. **Security Stage**
   - Vulnerability scanning with Trivy
   - SARIF report generation
   - Security best practices validation

3. **Build Stage**
   - Multi-platform Docker image building
   - Container registry push (GHCR)
   - Image optimization and caching

4. **Deploy Stage**
   - Staging environment deployment
   - Smoke tests execution
   - Deployment verification

## 🐳 Docker

### Multi-Stage Build
The Dockerfile uses multi-stage builds for optimization:
- **Builder stage**: Compiles dependencies and prepares the environment
- **Production stage**: Minimal runtime image with security best practices

### Container Features
- Non-root user execution
- Health checks
- Proper signal handling
- Resource optimization
- Security scanning

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|---------|-------------|
| `/` | GET | Main todo list interface |
| `/add` | GET/POST | Add new task form |
| `/complete/<id>` | POST | Toggle task completion |
| `/delete/<id>` | POST | Delete task |
| `/api/tasks` | GET | JSON API for tasks |
| `/health` | GET | Health check endpoint |

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Application environment | `development` |
| `DATABASE_URL` | Database connection string | `sqlite:///app.db` |
| `SECRET_KEY` | Flask secret key | `dev-secret-key` |

### Docker Compose Services

- **web**: Flask application container
- **db**: PostgreSQL database
- **pgadmin**: Database administration (development)

## 🚀 Deployment

### Production Deployment

The application is production-ready with:
- Gunicorn WSGI server
- PostgreSQL database
- Docker containerization
- Health checks and monitoring
- Structured logging

### Staging Environment

Automated staging deployments happen on every push to `main` branch through GitHub Actions.

## 📈 Monitoring & Observability

- **Health Checks**: `/health` endpoint for service monitoring
- **Structured Logging**: JSON-formatted logs for analysis
- **Metrics**: Application performance tracking
- **Docker Health Checks**: Container-level health monitoring

## 👥 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 DevOps Skills Demonstrated

This project showcases the following DevOps practices and skills:

### ✅ Development Practices
- Clean code architecture
- Test-driven development
- Version control with Git
- Code review process

### ✅ Containerization & Orchestration
- Docker multi-stage builds
- Docker Compose orchestration
- Container security best practices
- Image optimization

### ✅ CI/CD & Automation
- GitHub Actions workflows
- Automated testing
- Security scanning
- Container registry integration

### ✅ Infrastructure & Deployment
- Infrastructure as Code
- Environment management
- Deployment automation
- Service orchestration

### ✅ Monitoring & Operations
- Health checks implementation
- Structured logging
- Performance monitoring
- Troubleshooting capabilities

---

