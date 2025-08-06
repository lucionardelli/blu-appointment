.EXPORT_ALL_VARIABLES:

run::
	docker compose up -d backend

restart::
	docker compose restart

down::
	docker compose down backend

stop::
	docker compose stop backend

down-v::
	docker compose down -v backend

build::
	docker compose build backend

test::
	docker compose run --rm tests

test-bash::
	docker compose run tests /bin/bash

db::
	docker compose exec -it backend sqlite3 /app/db/blu.db

bash::
	docker compose exec -ti backend bash

logs::
	docker compose logs --tail 100

migration::
	docker compose exec -ti backend bash -c "alembic revision --autogenerate -m $(message)"
