
## Backend Project Structure

```bash
my_fastapi_app/
├── app/
│   ├── __init__.py           # makes "app" a python package
│   ├── main.py               # entry point, creates FastAPI app
│   ├── api/                  
│   │   ├── __init__.py
│   │   ├── routes/           # all endpoints (organized by feature)
│   │   │   ├── __init__.py
│   │   │   ├── vehicles.py   # vehicle-related endpoints
│   │   │   └── users.py      # user-related endpoints
│   │   └── deps.py           # dependencies (auth, db sessions, etc.)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py         # settings/env vars (like DB URL, secrets)
│   │   └── security.py       # auth utils (JWT, password hashing)
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py           # base SQLAlchemy metadata
│   │   ├── session.py        # DB session creator
│   │   └── init_db.py        # first-time DB seeding
│   ├── models/
│   │   ├── __init__.py
│   │   ├── vehicle.py        # Vehicle SQLAlchemy model
│   │   └── user.py           # User SQLAlchemy model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── vehicle.py        # Pydantic schemas for vehicles
│   │   └── user.py           # Pydantic schemas for users
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── vehicle.py        # CRUD functions for vehicles
│   │   └── user.py           # CRUD functions for users
│   └── utils/
│       ├── __init__.py
│       └── logger.py         # custom logging setup
│
├── alembic/                  # migration folder (created by Alembic)
│   └── versions/             # migration scripts
├── tests/                    # pytest unit + integration tests
│   ├── __init__.py
│   ├── test_vehicles.py
│   └── test_users.py
├── .env                      # environment variables (never commit in prod)
├── alembic.ini               # alembic config file
├── requirements.txt          # project dependencies
└── run.sh                    # helper script to run app (optional)
```