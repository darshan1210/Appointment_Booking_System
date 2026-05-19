````md
# 🚀 Running the Project

## Prerequisites

Before running the project, ensure the following tools are installed:

- Python 3.12+
- Poetry
- Redis Server
- PostgreSQL / Supabase
- Node.js (for frontend)

---

# 📦 Backend Setup (FastAPI)

## 1. Install Dependencies

```bash
poetry install
````

---

## 2. Activate Virtual Environment

```bash
poetry shell
```

---

## 3. Configure Environment Variables

Create a `.env` file in the backend root directory:

```env
DATABASE_URL=postgresql+asyncpg://USER:PASSWORD@HOST:PORT/DB_NAME

JWT_SECRET_KEY=your-secret-key

REDIS_URL=redis://localhost:6379/0

EMAIL_API_KEY=your-email-provider-key

FCM_SERVER_KEY=your-firebase-key

SUPER_ADMIN_SECRET=dev-secret
```

---

# ⚡ Poetry Task Commands (npm-like scripts)

This project uses `poethepoet` to simplify command execution.

Install:

```bash
poetry add --group dev poethepoet
```

---

## Add the following in `pyproject.toml`

```toml
[tool.poe.tasks]

dev = "uvicorn app.main:app --reload"

start = "uvicorn app.main:app --host 0.0.0.0 --port 8000"

worker = "celery -A app.background.celery_app:celery_app worker -Q critical -P threads --concurrency=4 -l info"

worker-prod = "celery -A app.background.celery_app:celery_app worker -Q critical --concurrency=4 -l warning"

beat = "celery -A app.background.celery_app:celery_app beat -l info"

flower = "celery -A app.background.celery_app:celery_app flower"

migrate = "alembic upgrade head"

makemigrations = "alembic revision --autogenerate -m"

lint = "ruff check ."

format = "ruff format ."

test = "pytest"
```

---

# 🖥️ Development Commands (Windows)

## Run FastAPI Development Server

```bash
poetry run poe dev
```

---

## Run Celery Worker (Windows Safe)

```bash
poetry run poe worker
```

This uses:

```bash
-P threads
```

because Celery prefork pool is unstable on Windows.

---

## Run Celery Beat Scheduler

```bash
poetry run poe beat
```

---

## Run Flower Monitoring Dashboard

Install Flower first:

```bash
poetry add flower
```

Run:

```bash
poetry run poe flower
```

Dashboard:

```text
http://localhost:5555
```

---

## Run Database Migrations

```bash
poetry run poe migrate
```

---

## Create New Migration

```bash
poetry run poe makemigrations "create users table"
```

---

# 🐳 Production Commands (Linux/Docker)

## Run API Server

```bash
poetry run poe start
```

---

## Run Celery Worker (Production)

```bash
poetry run poe worker-prod
```

Linux supports Celery prefork pool natively.

---

# 🔴 Redis Setup

## Windows

Use Docker:

```bash
docker run -d -p 6379:6379 redis
```

---

## Linux

```bash
sudo systemctl start redis
```
---

# 📋 Recommended Development Workflow

Open separate terminals:

## Terminal 1 - FastAPI

```bash
poetry run poe dev
```

## Terminal 2 - Celery Worker

```bash
poetry run poe worker
```

## Terminal 3 - Celery Beat

```bash
poetry run poe beat
```

---

# 📡 Services Used

| Service                   | Purpose             |
| ------------------------- | ------------------- |
| FastAPI                   | Backend API         |
| PostgreSQL / Supabase     | Database            |
| Redis                     | Celery broker       |
| Celery                    | Background jobs     |
| APScheduler / Celery Beat | Scheduled reminders |
| Firebase FCM              | Push notifications  |
| Resend / SendGrid         | Email notifications |

---

# 🛠️ Important Notes

## Windows Development

Celery workers must use:

```bash
-P threads
```

Avoid:

```bash
-P prefork
```

because multiprocessing pools are unstable on Windows.

---

# 🔐 Super Admin Registration

Super Admin registration requires:

```env
SUPER_ADMIN_SECRET=dev-secret
```

Requests without the correct secret are rejected with HTTP 403.

---

# 📦 Build Status

Current Phase:

* Planning & Architecture
* Backend Foundation Setup
* Multi-tenant Design
* Celery Infrastructure
* Notification Architecture

```
```
