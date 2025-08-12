param(
    [string]$msg = "auto migration"
)
.\.venv\Scripts\activate

alembic revision --autogenerate -m "$msg"

alembic upgrade head