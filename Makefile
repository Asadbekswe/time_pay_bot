run:
	python3 main.py

create_migrate:
	alembic init migrations

create_async_migrate:
	alembic init -t async migrations

makemigrations:
	alembic revision --autogenerate -m "Initial migration"

migrate:
	alembic upgrade head

down_migrate:
	alembic downgrade -1