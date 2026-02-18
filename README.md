# CRUD API

Generic SOLID CRUD API built with FastAPI. Designed as a flexible base for any project.

## Tech Stack

| Component | Technology |
|---|---|
| Framework | FastAPI |
| ORM | SQLAlchemy 2.0 (async) |
| Validation | Pydantic v2 |
| Migrations | Alembic |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Tests | pytest + pytest-asyncio + httpx |
| Linting | ruff |
| CI/CD | GitHub Actions |

## Architecture (SOLID)

```
app/
├── api/v1/endpoints/   # HTTP layer (routes, status codes)
├── services/           # Business logic layer
├── repositories/       # Data access layer (queries)
├── models/             # ORM models (database schema)
├── schemas/            # Pydantic models (validation)
├── core/               # Exceptions, shared utilities
└── db/                 # Engine, session, base model
```

Each layer has a single responsibility and depends on abstractions (Protocols), not concrete implementations.

## Quick Start

```bash
# Install dependencies
pip install -e ".[dev]"

# Copy environment file
cp .env.example .env

# Run the server
uvicorn app.main:app --reload

# Access Swagger UI
# http://localhost:8000/docs
```

## Endpoints

| Method | Route | Description |
|---|---|---|
| POST | `/api/v1/items/` | Create a new item |
| GET | `/api/v1/items/` | List all items (paginated) |
| GET | `/api/v1/items/{id}` | Get item by ID |
| PUT | `/api/v1/items/{id}` | Update an item |
| DELETE | `/api/v1/items/{id}` | Delete an item |

## Running Tests

```bash
# Run all tests with coverage
pytest

# Run only unit tests
pytest tests/unit/

# Run only integration tests
pytest tests/integration/
```

## Linting

```bash
ruff check .
ruff format .
```

## Adding a New Entity

1. Create model in `app/models/`
2. Create schemas in `app/schemas/`
3. Create repository in `app/repositories/` (extend `BaseRepository`)
4. Create service in `app/services/` (extend `BaseService`)
5. Create endpoints in `app/api/v1/endpoints/`
6. Register router in `app/api/v1/router.py`
7. Add dependency providers in `app/api/v1/dependencies.py`

## Database Migrations

```bash
# Generate a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1
```
