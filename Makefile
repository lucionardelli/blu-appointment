.EXPORT_ALL_VARIABLES:

run:: .check-env
	docker compose -f docker-compose.yml up -d

down::
	docker compose -f docker-compose.yml down

stop::
	docker compose -f docker-compose.yml stop

down-v::
	docker compose -f docker-compose.yml down -v

build::
	docker compose build --parallel

# db::
# 	docker compose exec postgres psql -U dfdconsumerdb ebdb
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

## Running tests inside Docker

test::
	docker compose exec -e TESTING=1 -ti backend python -m pytests tests

migration::
	docker compose exec -ti backend bash -c "alembic revision --autogenerate -m $(message)"
