# e-commerce-backend

Django 5 + DRF backend for the multi-vendor marketplace (modular monolith).
Planning docs live in `../docs/`, especially
[10-project-structure.md](../docs/10-project-structure.md) (this repo's
target layout) and [14-execution-checklist.md](../docs/14-execution-checklist.md)
(what to build, in order).

## Prerequisites

Pick **one** of the two setup paths below (Docker is recommended — it's the
one CI and these docs assume). Whichever path you use, you need:

- **Git**
- **Docker path**: Docker Engine + Docker Compose v2 (`docker compose version`
  should print `v2.x` or higher)
- **Standalone path**: Python 3.12, a local PostgreSQL 16 server, a local
  Redis 7 server, `pip`

## Option A — Docker Compose (recommended)

Brings up Postgres, Redis, MinIO (S3-compatible object storage), the Django
backend, Celery worker + beat, and the frontend, all wired together.

1. Clone both repos side by side (Compose references `../e-commerce-frontend`
   for the frontend build context, so they must be sibling directories):

   ```bash
   git clone <backend-repo-url> e-commerce-backend
   git clone <frontend-repo-url> e-commerce-frontend
   ```

2. From `e-commerce-backend/`, create your local env file:

   ```bash
   cp .env.example .env
   ```

   The defaults in `.env.example` already match the Compose service names
   (`db`, `redis`, `minio`) — you don't need to edit anything to get a
   working local stack. See [Environment variables](#environment-variables)
   below if you want to understand or change any value.

3. Build and start everything:

   ```bash
   docker compose up
   ```

   First run builds the backend/frontend images and will take a few minutes.
   The backend container automatically runs `python manage.py migrate`
   before starting the dev server (see the `backend` service `command` in
   `docker-compose.yml`), so the database schema is ready as soon as the
   container is healthy.

4. Verify it's up:

   | Service | URL |
   |---|---|
   | Backend API | http://localhost:8000/api/v1/ |
   | Health check | http://localhost:8000/healthz/ |
   | Django admin | http://localhost:8000/admin/ |
   | Frontend | http://localhost:3000 |
   | MinIO console | http://localhost:9001 (user/pass: `minioadmin` / `minioadmin`) |
   | Postgres (host access) | `localhost:5433` (mapped from container's 5432 — see note below) |

5. Create an admin user (in a second terminal, stack still running):

   ```bash
   docker compose exec backend python manage.py createsuperuser
   ```

6. Stop the stack:

   ```bash
   docker compose down
   ```

   Add `-v` (`docker compose down -v`) if you also want to wipe the
   Postgres/MinIO volumes and start from a clean database next time.

**Useful day-to-day commands:**

```bash
docker compose up -d                          # run in background
docker compose logs -f backend                # tail backend logs
docker compose exec backend bash              # shell into the backend container
docker compose exec backend python manage.py makemigrations
docker compose exec backend python manage.py migrate
docker compose exec backend pytest            # run the test suite
docker compose restart backend                # after changing settings/env
```

Code changes on your host are picked up automatically — the `backend`
service mounts the repo as a volume and Django's dev server auto-reloads.

## Option B — Standalone (no Docker)

Use this if you already run Postgres/Redis locally, or Docker isn't
available.

1. Create and activate a virtualenv, then install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate          # Windows: .venv\Scripts\activate
   pip install -r requirements/dev.txt
   ```

2. Make sure PostgreSQL and Redis are running locally, and create the
   database:

   ```bash
   createdb ecommerce
   ```

3. Copy the env file and point it at your local services:

   ```bash
   cp .env.example .env
   ```

   Edit `.env`:
   - `DATABASE_URL=postgres://<user>:<password>@localhost:5432/ecommerce`
   - `REDIS_URL=redis://localhost:6379/0`
   - `DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1` (drop `backend`, that's the
     Docker service hostname)
   - MinIO vars only matter if you're running MinIO locally too; otherwise
     leave them — nothing hits them until file uploads exist.

4. Run migrations and start the dev server:

   ```bash
   python manage.py migrate
   python manage.py createsuperuser   # optional, for /admin/
   python manage.py runserver
   ```

5. API available at http://localhost:8000/api/v1/, health check at
   http://localhost:8000/healthz/.

6. (Optional) run Celery in separate terminals if you're working on async
   tasks (notifications, payouts, etc.):

   ```bash
   celery -A config worker -l info
   celery -A config beat -l info
   ```

## Environment variables

All variables are documented with defaults in `.env.example`. Never commit
the real `.env` (already gitignored) — see
[11-deployment-infra.md](../docs/11-deployment-infra.md) for how secrets are
handled beyond local dev.

| Variable | Purpose |
|---|---|
| `DJANGO_SETTINGS_MODULE` | Which settings file to load (`config.settings.dev` locally; `manage.py` defaults here too, `wsgi.py`/`asgi.py` default to `production`) |
| `DJANGO_SECRET_KEY` | Django's cryptographic signing key — any value works locally, must be a real secret in staging/production |
| `DJANGO_DEBUG` | `True` locally for tracebacks; must be `False` outside dev |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated hostnames Django will serve | 
| `DATABASE_URL` | `postgres://user:pass@host:port/dbname` |
| `REDIS_URL` | Backs Celery broker/result backend and caching |
| `DJANGO_CORS_ALLOWED_ORIGINS` | Frontend origin(s) allowed to call the API |
| `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` | Credentials for MinIO locally, real S3 credentials in staging/production |
| `AWS_STORAGE_BUCKET_NAME` | Bucket for uploaded media (product images, etc.) |
| `AWS_S3_ENDPOINT_URL` | MinIO endpoint locally; unset/omit for real AWS S3 |
| `AWS_S3_REGION_NAME` | S3 region |
| `SENTRY_DSN` | Left blank until error tracking is wired up (later phase) |

## Structure

- `config/settings/{base,dev,staging,production}.py` — environment-layered
  settings; `manage.py` defaults to `dev`, `wsgi.py`/`asgi.py` default to
  `production` (docs/11-deployment-infra.md).
- `apps/<name>/` — one Django app per domain (`accounts`, `vendors`,
  `catalog`, `inventory`, `cart`, `orders`, `payments`, `payouts`,
  `reviews`, `promotions`, `notifications`, `core`), each following
  `models.py` → `serializers.py` → `views.py` → `services.py` layering
  (docs/10-project-structure.md).
- `config/api_v1_urls.py` — mounts every app's `urls.py` under `/api/v1/`.
- `config/celery.py` — Celery app for async tasks + Celery Beat schedules.

## Tests

```bash
pytest                       # standalone
docker compose exec backend pytest   # Docker
```

Runs against a real PostgreSQL instance (no SQLite-in-tests — see
docs/11-deployment-infra.md), so Postgres must be reachable via
`DATABASE_URL` (Docker Compose's `db` service, or a local instance).

## Linting / formatting

```bash
ruff check .
black .
```

Config lives in `pyproject.toml` (line length 100, `.venv`/migrations
excluded). CI (`.github/workflows/ci.yml`) runs both plus `pytest` on every
push/PR.

## Troubleshooting

- **`docker compose up` fails on `backend` with a DB connection error** —
  the `db`/`redis`/`minio` services take a few seconds to pass their
  healthchecks; `backend` waits on `condition: service_healthy` so this
  should self-resolve. If it doesn't, run `docker compose logs db` to check
  Postgres actually started.
- **Port already in use (5432, 6379, 8000, 3000)** — something else on your
  machine is bound to that port. The Postgres container is already
  remapped to host port `5433` for this reason; stop the conflicting local
  service or change the mapping in `docker-compose.yml` for the others.
- **Migrations out of date after pulling new code** — rerun
  `docker compose exec backend python manage.py migrate` (Docker) or
  `python manage.py migrate` (standalone).
- **`ModuleNotFoundError` after pulling new code** — dependencies changed;
  rerun `pip install -r requirements/dev.txt` (standalone) or
  `docker compose build backend` (Docker, since the image bakes
  dependencies in).
