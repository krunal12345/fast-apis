# Production-Level FastAPI Project Structure

There are two common philosophies for structuring FastAPI projects. The
**domain/feature-based** layout (recommended) and the **type-based** layout.

## Recommended: Domain/Feature-Based Layout

This scales best because everything about one feature (routes, schemas, DB
logic) lives together.

```
fast-apis/
├── app/                        # application package
│   ├── __init__.py
│   ├── main.py                 # FastAPI() instance, lifespan, router registration
│   │
│   ├── core/                   # cross-cutting concerns
│   │   ├── config.py           # Settings via pydantic-settings (env vars)
│   │   ├── security.py         # password hashing, JWT create/verify
│   │   ├── logging.py          # logging config
│   │   └── exceptions.py       # custom exception classes + handlers
│   │
│   ├── db/
│   │   ├── base.py             # SQLAlchemy Base / metadata
│   │   ├── session.py          # engine + SessionLocal, get_db dependency
│   │   └── init_db.py          # seed/bootstrap data
│   │
│   ├── api/
│   │   ├── deps.py             # shared dependencies (get_current_user, etc.)
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── router.py       # aggregates all v1 feature routers
│   │
│   ├── features/               # one folder per domain (a.k.a. "modules")
│   │   ├── users/
│   │   │   ├── router.py       # APIRouter endpoints
│   │   │   ├── schemas.py      # Pydantic request/response models
│   │   │   ├── models.py       # SQLAlchemy ORM models
│   │   │   ├── service.py      # business logic
│   │   │   ├── repository.py   # DB queries (optional but clean)
│   │   │   └── dependencies.py # feature-specific deps
│   │   └── auth/
│   │       └── ...same shape
│   │
│   └── models/                 # OR keep all ORM models centralized here
│
├── alembic/                    # DB migrations
│   ├── versions/
│   └── env.py
├── alembic.ini
│
├── tests/
│   ├── conftest.py             # fixtures (test client, test db)
│   ├── unit/
│   └── integration/
│
├── scripts/                    # ops scripts (seed, backfill, etc.)
├── .env / .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml              # deps + tooling config (ruff, mypy, pytest)
└── README.md
```

## Key Conventions That Matter in Production

| Concern | What to do |
|---|---|
| **Config** | `pydantic-settings` `BaseSettings` reading from env. Never hardcode secrets. |
| **Layering** | `router` → `service` (logic) → `repository`/ORM. Keep routes thin. |
| **Schemas vs Models** | Pydantic `schemas.py` = API contract; SQLAlchemy `models.py` = DB. Never leak ORM objects directly. |
| **Versioning** | `api/v1/` from day one — cheap insurance. |
| **DB sessions** | One `get_db` dependency, injected via `Depends`. |
| **Migrations** | Alembic, always. Don't rely on `create_all` in prod. |
| **App factory** | A `create_app()` function helps testing and multiple configs. |
| **Dependency mgmt** | `pyproject.toml` with `uv` or Poetry. |

## Alternative: Type-Based Layout

Some teams (and the classic FastAPI tutorial) group by *type* instead of feature:

```
app/
├── routers/      # all endpoints
├── schemas/      # all pydantic models
├── models/       # all ORM models
├── services/     # all business logic
└── crud/         # all db access
```

This is simpler for small apps but gets unwieldy past ~5 features because
changing one feature means touching 5 directories. **Use feature-based for
anything you expect to grow.**

## References

- [`full-stack-fastapi-template`](https://github.com/fastapi/full-stack-fastapi-template) — official template by FastAPI's author
- [Netflix `dispatch`](https://github.com/Netflix/dispatch) — large real-world FastAPI app
