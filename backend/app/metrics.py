from prometheus_client import Counter, Histogram, Gauge

# --- API Metrics ---
HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "handler", "status"],
)

HTTP_REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "handler"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
)

# --- Auth Metrics ---
AUTH_LOGIN_TOTAL = Counter(
    "auth_login_total",
    "Login attempts",
    ["status"],  # success / failure
)

# --- Student Metrics ---
STUDENT_CREATED_TOTAL = Counter(
    "student_created_total",
    "Total students created",
)

STUDENT_TOTAL_COUNT = Gauge(
    "student_total_count",
    "Current total number of students in the database",
)
