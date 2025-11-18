Use UV to to initialise a project and create virtual environment
- uv init
- uv venv .venv

uvicorn main:app --reload --log-level debug --port 8000

export DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/mydb"

Windows
setx DATABASE_URL "postgresql+asyncpg://user:password@localhost:5432/mydb"
