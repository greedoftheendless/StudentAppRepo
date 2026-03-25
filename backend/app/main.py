from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app

from app.database import Base, engine
from app.middleware import PrometheusMiddleware
from app.models import Student  # noqa: F401 — ensure tables are registered
from app.routes import auth, students


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Student Management API",
    version="1.0.0",
    lifespan=lifespan,
)

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Prometheus middleware ---
app.add_middleware(PrometheusMiddleware)

# --- Routes ---
app.include_router(auth.router)
app.include_router(students.router)

# --- Prometheus /metrics endpoint ---
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


@app.get("/api/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}
