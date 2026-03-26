# Student Management Application

A production-ready, full-stack Student Management web application built with **React**, **FastAPI**, and **PostgreSQL**, fully containerized with **Docker Compose**, monitored via **Prometheus + Grafana**, tested with **pytest, Jest, and Selenium**, and deployed through a **GitHub Actions CI/CD pipeline** using a self-hosted runner.

---

## Table of Contents

- [Tech Stack](#tech-stack)
- [Architecture Overview](#architecture-overview)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Service URLs](#service-urls)
- [API Reference](#api-reference)
- [Authentication Flow](#authentication-flow)
- [Frontend Pages](#frontend-pages)
- [Database Schema](#database-schema)
- [Docker Services](#docker-services)
- [Running Tests](#running-tests)
  - [Backend Unit Tests (pytest)](#backend-unit-tests-pytest)
  - [Frontend Unit Tests (Jest)](#frontend-unit-tests-jest)
  - [End-to-End Tests (Selenium)](#end-to-end-tests-selenium)
- [Monitoring & Observability](#monitoring--observability)
  - [Prometheus Metrics](#prometheus-metrics)
  - [Grafana Dashboard](#grafana-dashboard)
  - [Alert Rules](#alert-rules)
- [CI/CD Pipeline](#cicd-pipeline)
  - [Pipeline Stages](#pipeline-stages)
  - [Self-Hosted Runner Setup](#self-hosted-runner-setup)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#troubleshooting)

---

## Tech Stack

| Layer          | Technology                                     | Version     |
|----------------|------------------------------------------------|-------------|
| **Frontend**   | React, React Router, Axios                     | 18.3, 6.28  |
| **Backend**    | Python, FastAPI, Uvicorn                        | 3.12, 0.115 |
| **ORM**        | SQLAlchemy                                      | 2.0         |
| **Database**   | PostgreSQL                                      | 16-alpine   |
| **DB Admin**   | pgAdmin 4                                       | latest      |
| **Auth**       | JWT (PyJWT + bcrypt)                            | 2.10, 4.3   |
| **Monitoring** | Prometheus + Grafana                            | 2.53, 11.1  |
| **Containers** | Docker & Docker Compose                         | —           |
| **CI/CD**      | GitHub Actions (self-hosted runner)             | —           |
| **Testing**    | pytest, Jest, React Testing Library, Selenium   | 8.3, —, 4.x |

---

## Architecture Overview

```
┌──────────────┐     ┌──────────────┐     ┌──────────────────┐
│   Browser    │────▶│   Nginx      │────▶│   FastAPI        │
│   (React)    │     │   :3000      │     │   :8000          │
└──────────────┘     └──────────────┘     └────────┬─────────┘
                                                   │
                          ┌────────────────────────┤
                          │                        │
                   ┌──────▼──────┐          ┌──────▼──────┐
                   │ PostgreSQL  │          │ Prometheus  │
                   │   :5432     │          │   :9090     │
                   └──────┬──────┘          └──────┬──────┘
                          │                        │
                   ┌──────▼──────┐          ┌──────▼──────┐
                   │  pgAdmin    │          │   Grafana   │
                   │   :5051     │          │   :3001     │
                   └─────────────┘          └─────────────┘
```

- **Frontend** → React SPA served by Nginx; proxies `/api/*` requests to the backend
- **Backend** → FastAPI with JWT authentication, Pydantic validation, Prometheus instrumentation
- **Database** → PostgreSQL with health checks and init script
- **Monitoring** → Prometheus scrapes `/metrics`; Grafana auto-provisions dashboards and alerts

---

## Project Structure

```
StudentApp/
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI/CD pipeline
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app entry point, CORS, route registration
│   │   ├── config.py            # Environment variable loader
│   │   ├── database.py          # SQLAlchemy engine, session, Base
│   │   ├── models.py            # ORM models (Student, User)
│   │   ├── schemas.py           # Pydantic request/response schemas
│   │   ├── auth.py              # Password hashing, JWT create/verify
│   │   ├── metrics.py           # Prometheus Counter, Histogram, Gauge definitions
│   │   ├── middleware.py        # Auto-instruments every request (latency + status)
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── auth.py          # POST /api/auth/register, /api/auth/login
│   │       └── students.py      # POST /api/students/, GET /api/students/
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py          # Test fixtures (in-memory SQLite, auth_token)
│   │   ├── test_auth.py         # 4 auth tests
│   │   └── test_students.py     # 5 student tests
│   ├── .dockerignore
│   ├── .env.example
│   ├── Dockerfile               # Python 3.12-slim → Uvicorn
│   └── requirements.txt
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── index.js             # React entry point
│   │   ├── App.js               # Router with PrivateRoute auth guard
│   │   ├── App.css              # Global styles
│   │   ├── App.test.js          # App-level test
│   │   ├── setupTests.js        # jest-dom setup
│   │   ├── components/
│   │   │   └── Navbar.js        # Navigation bar with logout
│   │   ├── pages/
│   │   │   ├── LoginPage.js     # Login/Register form
│   │   │   ├── LoginPage.test.js
│   │   │   ├── AddStudentPage.js    # Add student form
│   │   │   ├── AddStudentPage.test.js
│   │   │   ├── StudentListPage.js   # Student table view
│   │   │   └── StudentListPage.test.js
│   │   └── services/
│   │       └── api.js           # Axios instance with JWT interceptor
│   ├── .dockerignore
│   ├── Dockerfile               # Multi-stage: Node 18 build → Nginx serve
│   ├── nginx.conf               # SPA routing + /api/ reverse proxy
│   └── package.json
├── selenium/
│   ├── conftest.py              # WebDriver fixture (Chrome, configurable headless)
│   ├── test_e2e.py              # 6 E2E tests (register, login, logout, add student, list)
│   └── requirements.txt
├── db/
│   └── init.sql                 # Grants schema permissions
├── prometheus/
│   ├── prometheus.yml           # Scrape config (backend:8000/metrics every 15s)
│   └── alert_rules.yml          # 6 alerting rules
├── grafana/
│   ├── dashboards/
│   │   └── student-app-dashboard.json   # 25+ panel dashboard
│   └── provisioning/
│       ├── dashboards/
│       │   └── dashboards.yml           # Auto-load dashboard directory
│       └── datasources/
│           └── prometheus.yml           # Auto-provision Prometheus datasource
├── docker-compose.yml           # 6 services, 4 volumes
├── .gitignore
└── README.md
```

---

## Prerequisites

| Requirement              | Minimum Version |
|--------------------------|-----------------|
| Docker                   | 20.x+          |
| Docker Compose           | 2.x+           |
| Git                      | 2.x+           |
| Python *(for local dev)* | 3.12+          |
| Node.js *(for local dev)*| 18.x           |
| Chrome *(for Selenium)*  | Latest          |

---

## Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/christopher-pb/StudentAppRepo.git
cd StudentAppRepo
```

### 2. Start all services
```bash
docker-compose up --build
```

### 3. Open the application
Navigate to **http://localhost:3000** in your browser.

### 4. Register & Login
1. Click **Register** to create an account
2. Enter a username and password
3. You'll be redirected to the Student List page

### 5. Stop all services
```bash
docker-compose down
```

To also remove volumes (database data, Grafana config, etc.):
```bash
docker-compose down -v
```

---

## Service URLs

| Service        | URL                          | Credentials              |
|----------------|------------------------------|--------------------------|
| **Frontend**   | http://localhost:3000         | Register your own        |
| **Backend API**| http://localhost:8000         | —                        |
| **Swagger Docs** | http://localhost:8000/docs | —                        |
| **ReDoc**      | http://localhost:8000/redoc   | —                        |
| **Prometheus** | http://localhost:9090         | —                        |
| **Grafana**    | http://localhost:3001         | admin / admin            |
| **pgAdmin**    | http://localhost:5051         | admin@studentapp.com / admin |
| **Metrics**    | http://localhost:8000/metrics | —                        |

### pgAdmin — Connect to PostgreSQL
1. Open http://localhost:5051 and login
2. **Add New Server** →
   - **Name:** StudentDB
   - **Host:** `postgres` (Docker DNS)
   - **Port:** `5432`
   - **Username:** `studentuser`
   - **Password:** `studentpass`
   - **Database:** `studentdb`

---

## API Reference

### Authentication Endpoints

| Method | Endpoint               | Body                                         | Response                        |
|--------|------------------------|----------------------------------------------|---------------------------------|
| POST   | `/api/auth/register`   | `{ "username": "str", "password": "str" }`   | `{ "access_token": "...", "token_type": "bearer" }` |
| POST   | `/api/auth/login`      | `{ "username": "str", "password": "str" }`   | `{ "access_token": "...", "token_type": "bearer" }` |

### Student Endpoints (JWT Required)

| Method | Endpoint           | Headers                          | Body / Response                                  |
|--------|--------------------|----------------------------------|--------------------------------------------------|
| POST   | `/api/students/`   | `Authorization: Bearer <token>`  | Body: `{ "name": "str", "age": int, "email": "str" }` → 201 Created |
| GET    | `/api/students/`   | `Authorization: Bearer <token>`  | `[{ "id": 1, "name": "...", "age": 20, "email": "..." }, ...]` |

### Utility Endpoints

| Method | Endpoint       | Description                          |
|--------|----------------|--------------------------------------|
| GET    | `/api/health`  | Returns `{ "status": "healthy" }`    |
| GET    | `/metrics`     | Prometheus text format metrics        |

### Error Responses
```json
// 400 - Duplicate
{ "detail": "Username already registered" }

// 401 - Invalid credentials
{ "detail": "Invalid credentials" }

// 422 - Validation error
{ "detail": [{ "loc": ["body", "email"], "msg": "value is not a valid email address", "type": "value_error" }] }
```

---

## Authentication Flow

```
┌────────┐    POST /api/auth/login     ┌─────────┐
│ Client │ ──────────────────────────▶ │ FastAPI  │
│        │                             │         │
│        │ ◀────────────────────────── │ verify  │
│        │    { access_token: JWT }    │ bcrypt  │
└───┬────┘                             └─────────┘
    │
    │  Authorization: Bearer <JWT>
    │
    │  GET /api/students/
    ▼
┌─────────┐   decode JWT   ┌──────────┐
│ FastAPI  │ ────────────▶ │ DB Query │
│ auth.py  │               │          │
└──────────┘               └──────────┘
```

- Passwords are hashed with **bcrypt** before storage
- JWT tokens are signed with **HS256** and include the username as subject
- Token is stored in `localStorage` on the frontend
- The Axios interceptor auto-attaches the token to every request

---

## Frontend Pages

| Page              | Route          | Auth Required | Description                              |
|-------------------|----------------|---------------|------------------------------------------|
| **Login/Register**| `/login`       | No            | Toggle between login and registration    |
| **Student List**  | `/students`    | Yes           | Table showing all students               |
| **Add Student**   | `/add-student` | Yes           | Form to create a new student record      |

- Unauthenticated users are redirected to `/login` via `PrivateRoute`
- After login, users are redirected to `/students`
- The **Navbar** shows navigation links and a Logout button

---

## Database Schema

### `users` Table

| Column          | Type         | Constraints              |
|-----------------|--------------|--------------------------|
| id              | Integer      | Primary Key, Auto-increment |
| username        | String(150)  | Unique, Not Null         |
| hashed_password | String(255)  | Not Null                 |

### `students` Table

| Column | Type         | Constraints                 |
|--------|--------------|-----------------------------|
| id     | Integer      | Primary Key, Auto-increment |
| name   | String(150)  | Not Null                    |
| age    | Integer      | Not Null                    |
| email  | String(255)  | Unique, Not Null            |

---

## Docker Services

| Service        | Image                     | Container Name          | Port Mapping   | Depends On           |
|----------------|---------------------------|-------------------------|----------------|----------------------|
| **postgres**   | postgres:16-alpine        | studentapp-db           | 5432:5432      | —                    |
| **backend**    | ./backend (Dockerfile)    | studentapp-api          | 8000:8000      | postgres (healthy)   |
| **frontend**   | ./frontend (Dockerfile)   | studentapp-ui           | 3000:80        | backend              |
| **prometheus** | prom/prometheus:v2.53.0   | studentapp-prometheus   | 9090:9090      | backend              |
| **grafana**    | grafana/grafana:11.1.0    | studentapp-grafana      | 3001:3000      | prometheus           |
| **pgadmin**    | dpage/pgadmin4:latest     | studentapp-pgadmin      | 5051:80        | postgres (healthy)   |

### Volumes

| Volume          | Purpose                          |
|-----------------|----------------------------------|
| `pgdata`        | PostgreSQL data persistence      |
| `promdata`      | Prometheus time-series data      |
| `grafdata`      | Grafana config and dashboards    |
| `pgadmindata`   | pgAdmin configuration            |

### Docker Commands

```bash
# Start all services
docker-compose up --build

# Start in detached mode
docker-compose up -d --build

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Rebuild a single service
docker-compose up --build backend

# Check service status
docker-compose ps

# Clean up dangling images
docker image prune -f
```

---

## Running Tests

### Backend Unit Tests (pytest)

**9 tests** covering authentication and student CRUD operations.

```bash
# Run inside Docker container
docker-compose exec backend python -m pytest tests/ -v

# Run locally
cd backend
pip install -r requirements.txt
python -m pytest tests/ -v
```

| Test File           | Tests | Description                                             |
|---------------------|-------|---------------------------------------------------------|
| `test_auth.py`      | 4     | Register success, duplicate username, login success, invalid credentials |
| `test_students.py`  | 5     | Add success, duplicate email, unauthorized access, list students, list unauthorized |

Tests use an **in-memory SQLite** database (no Docker needed).

---

### Frontend Unit Tests (Jest)

**10 tests** across 4 test suites covering UI rendering, form submission, and error handling.

```bash
# Run via Docker
docker run --rm -w /app -v "${PWD}/frontend:/app" node:18-alpine \
  sh -c "npm install --legacy-peer-deps && npx react-scripts test --watchAll=false --verbose"

# Run locally
cd frontend
npm install --legacy-peer-deps
npm test
```

| Test File                    | Tests | Description                                      |
|------------------------------|-------|--------------------------------------------------|
| `App.test.js`                | 1     | Renders login page when not authenticated        |
| `LoginPage.test.js`          | 3     | Renders form, shows error on failure, toggles login/register |
| `AddStudentPage.test.js`     | 3     | Renders form, submits successfully, shows error on failure |
| `StudentListPage.test.js`    | 3     | Renders heading, shows students in table, empty message |

---

### End-to-End Tests (Selenium)

**6 tests** covering the complete user workflow through a real browser.

> **Prerequisite:** The application must be running (`docker-compose up`)

```bash
# Run with visible browser
cd selenium
pip install selenium pytest
python -m pytest test_e2e.py -v

# Run headless (CI mode) — set in conftest.py
# opts.add_argument("--headless")
```

| Test                                   | Description                                     |
|----------------------------------------|-------------------------------------------------|
| `test_register_new_user`               | Registers a new user, redirects to /students    |
| `test_logout`                          | Clicks Logout, redirects to /login              |
| `test_login_existing_user`             | Logs in with registered user                    |
| `test_login_invalid_credentials`       | Shows error message for bad credentials         |
| `test_add_student`                     | Fills form, submits, sees success message       |
| `test_student_list_shows_added_student`| Verifies the added student appears in the table |

---

## Monitoring & Observability

### Prometheus Metrics

The backend auto-instruments every HTTP request via custom middleware.

| Metric                            | Type      | Labels                          | Description                       |
|-----------------------------------|-----------|---------------------------------|-----------------------------------|
| `http_requests_total`             | Counter   | method, endpoint, http_status   | Total HTTP requests               |
| `http_request_duration_seconds`   | Histogram | method, endpoint                | Request latency distribution      |
| `auth_login_total`                | Counter   | status (success/failure)        | Login attempts                    |
| `student_created_total`           | Counter   | —                               | Students created                  |
| `student_total_count`             | Gauge     | —                               | Current student count             |

**Scrape config:** Prometheus scrapes `backend:8000/metrics` every **15 seconds**.

---

### Grafana Dashboard

Auto-provisioned on startup with **25+ panels** across 5 rows:

| Row                     | Panels                                                               |
|-------------------------|----------------------------------------------------------------------|
| **System Health**       | CPU Usage gauge, Memory Usage gauge, Disk Usage gauge, CPU/Memory time-series |
| **API Performance**     | Request Rate (RPS), Latency p50/p95/p99, Error Rate %, Endpoint bar chart, Status Code pie chart |
| **Authentication**      | Login Success count, Login Failure count, Auth Success Rate gauge, Login Trend time-series |
| **Student Operations**  | Total Students gauge, Creation Rate, Endpoint Usage bar, Student Trend time-series |
| **Database Metrics**    | Active Connections, Query Duration, Connection Trend, Table Scan Operations |

**Access:** http://localhost:3001 → Login with `admin` / `admin`

---

### Alert Rules

Defined in `prometheus/alert_rules.yml`:

| Alert                    | Condition                              | Duration | Severity  |
|--------------------------|----------------------------------------|----------|-----------|
| **HighApiErrorRate**     | 5xx error rate > 5%                    | 2 min    | critical  |
| **HighApiLatency**       | p95 latency > 1 second                | 2 min    | warning   |
| **HighCpuUsage**         | CPU > 80%                              | 5 min    | warning   |
| **HighMemoryUsage**      | Memory > 75%                           | 5 min    | warning   |
| **LoginFailureSpike**    | Login failure rate > 0.5/s             | 2 min    | critical  |
| **DbConnectionSaturation** | DB connections > 85% of max          | 3 min    | critical  |

---

## CI/CD Pipeline

### Pipeline Stages

The GitHub Actions workflow (`.github/workflows/ci.yml`) triggers on **push** and **pull request** to `main`:

```
┌─────────────────┐     ┌──────────────────┐
│  Backend Tests  │     │  Frontend Tests  │
│  (pytest)       │     │  (Jest)          │
│  runs-on:       │     │  runs-on:        │
│  self-hosted    │     │  self-hosted     │
└────────┬────────┘     └────────┬─────────┘
         │                       │
         └───────────┬───────────┘
                     ▼
          ┌─────────────────────┐
          │   Docker Build      │
          │   (backend +        │
          │    frontend images) │
          │   runs-on:          │
          │   self-hosted       │
          └─────────────────────┘
```

| Job              | Runner      | Steps                                                        |
|------------------|-------------|--------------------------------------------------------------|
| **backend-test** | self-hosted | Checkout → Safe directory → Python 3.12 → pip install → pytest |
| **frontend-test**| self-hosted | Checkout → Safe directory → Node 20 → npm install → Jest      |
| **docker-build** | self-hosted | Checkout → Safe directory → Build backend image → Build frontend image → Verify |

### Self-Hosted Runner Setup

1. **Download** the runner from GitHub → Repo **Settings** → **Actions** → **Runners** → **New self-hosted runner**

2. **Configure:**
   ```powershell
   cd D:\KJC\actions-runner
   .\config.cmd --url https://github.com/christopher-pb/StudentAppRepo --token <TOKEN>
   ```

3. **Start:**
   ```powershell
   .\run.cmd
   ```

4. **Fix Git safe directory** (Windows):
   ```powershell
   git config --system --add safe.directory '*'
   ```

> **Note:** For org-level runners that serve multiple repos, register at the organization level instead of the repo level.

---

## Environment Variables

### Backend (`docker-compose.yml`)

| Variable        | Default Value                                        | Description            |
|-----------------|------------------------------------------------------|------------------------|
| `DATABASE_URL`  | `postgresql://studentuser:studentpass@postgres:5432/studentdb` | PostgreSQL connection string |
| `SECRET_KEY`    | `docker-compose-dev-secret-change-in-prod`           | JWT signing secret     |

### PostgreSQL

| Variable            | Value          |
|---------------------|----------------|
| `POSTGRES_USER`     | `studentuser`  |
| `POSTGRES_PASSWORD` | `studentpass`  |
| `POSTGRES_DB`       | `studentdb`    |

### Grafana

| Variable                    | Value    |
|-----------------------------|----------|
| `GF_SECURITY_ADMIN_USER`   | `admin`  |
| `GF_SECURITY_ADMIN_PASSWORD`| `admin` |

### pgAdmin

| Variable                    | Value                    |
|-----------------------------|--------------------------|
| `PGADMIN_DEFAULT_EMAIL`    | `admin@studentapp.com`   |
| `PGADMIN_DEFAULT_PASSWORD` | `admin`                  |

> **⚠ Security Note:** Change all default passwords before deploying to production.

---

## Troubleshooting

### Build & Runtime Issues

| Problem                                | Solution                                                         |
|----------------------------------------|------------------------------------------------------------------|
| Frontend build fails with ajv error    | Ensure `ajv@^8.12.0` is in `package.json` dependencies          |
| Frontend build fails with Node 20      | Use `node:18-alpine` in `frontend/Dockerfile`                    |
| 422 error shows `[object Object]`      | Error handling extracts `.msg` from array-format FastAPI errors   |
| `docker-compose up` version warning    | Remove `version: "3.9"` from `docker-compose.yml` (deprecated)  |
| Port 5050 conflict for pgAdmin         | pgAdmin is mapped to **5051** instead                            |
| Backend tests need database            | Tests use in-memory SQLite — no database required                |
| Selenium tests fail without app        | Start the app first: `docker-compose up -d`                      |
| Jest `Cannot find module @testing-library/dom` | Add `@testing-library/dom@^10.4.0` to `devDependencies`   |
| Jest `Cannot use import statement` (axios) | Add `transformIgnorePatterns: ["node_modules/(?!axios)/"]` to Jest config in `package.json` |

### Self-Hosted Runner Issues

| Problem                                | Solution                                                         |
|----------------------------------------|------------------------------------------------------------------|
| **Git dubious ownership** — `detected dubious ownership in repository` | Run `git config --system --add safe.directory '*'` in an elevated terminal. Also create `C:\ProgramData\Git\config` with `[safe]\n\tdirectory = *` |
| **`$GITHUB_WORKSPACE` empty on Windows** | Use `${{ github.workspace }}` in workflow YAML — it's a GitHub expression resolved before the shell runs |
| **Runner shows offline on GitHub** | Check if the runner service is running: `Get-Service actions.runner.*`. Start with: `Start-Service <service-name>` or manually with `run.cmd` |
| **Runner registered to wrong repo** | Check `.runner` file: `Get-Content <runner-dir>\.runner -Raw`. Re-register with `config.cmd remove` then `config.cmd --url <repo-url> --token <token>` |
| **Multiple repos need a runner** | Option 1: Register runner at org level. Option 2: Create separate runner folders per repo |
| **`No Python 3.12 found` + registry error** | Self-hosted runners can't install Python via `actions/setup-python`. Remove the action and use system-installed Python (`python --version` to verify) |
| **Docker `Access is denied` in runner** | Add the runner's service account to the `docker-users` group (elevated): `net localgroup docker-users "NT AUTHORITY\SERVICE" /add`. Then restart the runner service |
| **Docker build fails in CI** | Ensure Docker Desktop is running, the runner service account is in `docker-users`, and restart the service after group change |
| **`error during connect: ... docker client must be run with elevated privileges`** | Runner service user lacks Docker access. Fix: add `Users` to `docker-users` group → restart runner service |

### Useful Diagnostic Commands

```powershell
# Check runner service status
Get-Service actions.runner.*

# Check which repo a runner is registered to
Get-Content <runner-dir>\.runner -Raw

# Check docker-users group membership
net localgroup docker-users

# Check system Git safe directory config
git config --system --list | Select-String "safe"

# Verify Docker access
docker ps

# Check runner process owner
Get-Process Runner.Listener -ErrorAction SilentlyContinue

# Start runner service (elevated)
Start-Service "actions.runner.christopher-pb-StudentAppRepo.YY282381"

# View runner logs
Get-ChildItem <runner-dir>\_diag\*.log | Sort-Object LastWriteTime -Descending | Select-Object -First 5
```
