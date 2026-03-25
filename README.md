# Student Management Application

A full-stack Student Management web application with monitoring, CI/CD, and automated testing.

## Tech Stack

| Layer        | Technology                  |
|--------------|-----------------------------|
| Frontend     | React 18, React Router      |
| Backend      | Python 3.12, FastAPI        |
| Database     | PostgreSQL 16               |
| Auth         | JWT (PyJWT + bcrypt)        |
| Monitoring   | Prometheus + Grafana        |
| Containers   | Docker & Docker Compose     |
| CI/CD        | GitHub Actions              |
| Testing      | pytest, Jest, Selenium      |

## Project Structure

```
StudentApp/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py          # App entry point
│   │   ├── config.py        # Environment config
│   │   ├── database.py      # SQLAlchemy setup
│   │   ├── models.py        # ORM models
│   │   ├── schemas.py       # Pydantic schemas
│   │   ├── auth.py          # JWT auth helpers
│   │   ├── metrics.py       # Prometheus metrics
│   │   ├── middleware.py     # Metrics middleware
│   │   └── routes/
│   │       ├── auth.py      # /api/auth endpoints
│   │       └── students.py  # /api/students endpoints
│   ├── tests/               # pytest unit tests
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                # React frontend
│   ├── src/
│   │   ├── App.js
│   │   ├── pages/           # Login, AddStudent, StudentList
│   │   ├── components/      # Navbar
│   │   └── services/        # Axios API client
│   ├── package.json
│   └── Dockerfile
├── selenium/                # Selenium E2E tests
├── prometheus/              # Prometheus config & alert rules
├── grafana/                 # Dashboard JSON & provisioning
│   ├── dashboards/
│   └── provisioning/
├── db/                      # Database init script
├── docker-compose.yml
└── .github/workflows/ci.yml # CI/CD pipeline
```

## Quick Start

### Prerequisites
- Docker & Docker Compose installed

### Run the full stack

```bash
docker-compose up --build
```

### Access the services

| Service     | URL                          |
|-------------|------------------------------|
| Frontend    | http://localhost:3000         |
| Backend API | http://localhost:8000         |
| API Docs    | http://localhost:8000/docs    |
| Prometheus  | http://localhost:9090         |
| Grafana     | http://localhost:3001         |
| Metrics     | http://localhost:8000/metrics |

### Grafana Login
- **Username:** `admin`
- **Password:** `admin`

The dashboard is auto-provisioned on startup.

## API Endpoints

| Method | Endpoint             | Auth     | Description           |
|--------|----------------------|----------|-----------------------|
| POST   | /api/auth/register   | No       | Register a new user   |
| POST   | /api/auth/login      | No       | Login, returns JWT    |
| POST   | /api/students/       | Required | Add a student         |
| GET    | /api/students/       | Required | List all students     |
| GET    | /api/health          | No       | Health check          |
| GET    | /metrics             | No       | Prometheus metrics    |

## Running Tests

### Backend unit tests
```bash
cd backend
pip install -r requirements.txt
python -m pytest tests/ -v
```

### Frontend unit tests
```bash
cd frontend
npm install --legacy-peer-deps
npm test
```

### Selenium E2E tests
Make sure the app is running first (`docker-compose up`), then:
```bash
cd selenium
pip install -r requirements.txt
pytest test_e2e.py -v
```

## Monitoring & Alerts

### Prometheus Metrics Collected
- `http_requests_total` — total HTTP requests by method, handler, status
- `http_request_duration_seconds` — request latency histogram
- `auth_login_total` — login attempts by status (success/failure)
- `student_created_total` — total students created
- `student_total_count` — current student count gauge

### Grafana Dashboard Rows
1. **System Health** — CPU, Memory, Disk gauges + time-series
2. **API Performance** — RPS, latency p50/p95/p99, error rate, endpoint bar chart, status pie chart
3. **Authentication** — Login success/failure stats, auth success rate gauge, trend chart
4. **Student Operations** — Total count, creation rate, endpoint usage, trends
5. **Database Metrics** — Active connections, query time, connection trend, scan operations

### Alert Rules
| Alert                    | Condition                           |
|--------------------------|-------------------------------------|
| HighApiErrorRate         | Error rate > 5% for 2 minutes       |
| HighApiLatency           | p95 latency > 1s for 2 minutes      |
| HighCpuUsage             | CPU > 80% for 5 minutes             |
| HighMemoryUsage          | Memory > 75% for 5 minutes          |
| LoginFailureSpike        | Failure rate > 0.5/s for 2 minutes  |
| DbConnectionSaturation   | Connections > 85% of max for 3 min  |

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) runs on pushes and PRs to `main`:

1. **Backend Tests** — Installs Python deps, runs pytest
2. **Frontend Tests** — Installs Node deps, runs Jest
3. **Docker Build** — Builds both images (runs after tests pass)
