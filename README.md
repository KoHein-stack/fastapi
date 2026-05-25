# FastAPI Learning 02

A simple FastAPI project for learning CRUD API routes with PostgreSQL.

## Requirements

- Python 3.10+
- PostgreSQL
- A PostgreSQL database named `fastapi`

The app reads database and JWT settings from `.env`. Use `.env.example` as the template.

Do not commit `.env` to Git.

## Setup Commands

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install project dependencies:

```powershell
pip install -r requirements.txt
```

Install a new dependency:

```powershell
pip install package-name
```

Update `requirements.txt` after installing new dependencies:

```powershell
pip freeze > requirements.txt
```

Create the PostgreSQL database:

```sql
CREATE DATABASE fastapi;
```

For a fresh empty database, apply all migrations:

```powershell
alembic upgrade head
```

For an existing local database that already has the current tables, mark it as migrated:

```powershell
alembic stamp head
```

Create a new migration after changing SQLAlchemy models:

```powershell
alembic revision --autogenerate -m "describe change"
```

Apply pending migrations:

```powershell
alembic upgrade head
```

Check current migration version:

```powershell
alembic current
```

## Docker Commands

Build and start FastAPI with PostgreSQL:

```powershell
docker compose up --build
```

Run containers in the background:

```powershell
docker compose up -d --build
```

Apply Alembic migrations inside the API container:

```powershell
docker compose exec api alembic upgrade head
```

Check migration version inside the API container:

```powershell
docker compose exec api alembic current
```

Stop containers:

```powershell
docker compose down
```

Stop containers and remove the PostgreSQL volume:

```powershell
docker compose down -v
```

Build and run with the production compose file:

```powershell
docker compose -f docker-compose.prod.yml up -d --build
```

Apply migrations in production compose:

```powershell
docker compose -f docker-compose.prod.yml exec api alembic upgrade head
```

View production logs:

```powershell
docker compose -f docker-compose.prod.yml logs -f api
```

## Run The App

Start the FastAPI development server:

```powershell
uvicorn app.main:app --reload
```

Open the API in your browser:

```text
http://127.0.0.1:8000
```

Open the interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

Open the alternative API documentation:

```text
http://127.0.0.1:8000/redoc
```

## API Commands

Get the root welcome message:

```powershell
curl http://127.0.0.1:8000/
```

Get all posts:

```powershell
curl http://127.0.0.1:8000/posts
```

Create a post:

```powershell
curl -X POST http://127.0.0.1:8000/posts/create_post `
  -H "Content-Type: application/json" `
  -d "{\"title\":\"My first post\",\"content\":\"Hello FastAPI\",\"published\":true}"
```

Get the latest in-memory post:

```powershell
curl http://127.0.0.1:8000/posts/latest
```

Get one post by id:

```powershell
curl http://127.0.0.1:8000/posts/1
```

Update one post by id:

```powershell
curl -X PUT http://127.0.0.1:8000/posts/1 `
  -H "Content-Type: application/json" `
  -d "{\"title\":\"Updated post\",\"content\":\"Updated content\",\"published\":true}"
```

Delete one post by id:

```powershell
curl -X DELETE http://127.0.0.1:8000/posts/1
```

## Project Structure

```text
.
+-- app/
|   +-- main.py
+-- requirements.txt
+-- LICENSE
+-- README.md
```
