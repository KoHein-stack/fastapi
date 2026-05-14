# FastAPI Learning 02

A simple FastAPI project for learning CRUD API routes with PostgreSQL.

## Requirements

- Python 3.10+
- PostgreSQL
- A PostgreSQL database named `fastapi`

The app currently connects with these database settings:

```text
host=localhost
database=fastapi
user=postgres
password=password
```

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

Create the `posts` table:

```sql
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    content VARCHAR NOT NULL,
    published BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
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
curl -X POST http://127.0.0.1:8000/create_post `
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
