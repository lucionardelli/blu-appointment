.EXPORT_ALL_VARIABLES:

run::
	docker compose up -d

restart::
	docker compose restart

down::
	docker compose down

stop::
	docker compose stop

down-v::
	docker compose down -v

build::
	docker compose build --parallel

backend-test::
	docker compose run --rm tests

backend-test-bash::
	docker compose run tests /bin/bash

db::
	docker compose exec -it backend sqlite3 /app/db/blu.db

backend-bash::
	docker compose exec -ti backend bash

frontend-bash::
	docker compose exec -ti frontend bash

backend-logs::
	docker compose logs -f backend --tail 100

frontend-logs::
	docker compose logs -f frontend --tail 100

celery-logs::
	docker compose logs -f celery-worker --tail 100

migration::
	docker compose exec -ti backend bash -c "alembic revision --autogenerate -m $(message)"

init-db::
	docker compose exec -ti backend bash -c "python -m app.db.seeds all"
