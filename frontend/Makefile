.EXPORT_ALL_VARIABLES:

run::
	docker compose up -d frontend

restart::
	docker compose restart

down::
	docker compose down frontend

stop::
	docker compose stop frontend

down-v::
	docker compose down -v frontend

build::
	docker compose build frontend

backend-test::
	docker compose run --rm fe-tests

backend-test-bash::
	docker compose run fe-tests /bin/bash

db::
	docker compose exec -it backend sqlite3 /app/db/blu.sqlite3

bash::
	docker compose exec -ti frontend bash

logs::
	docker compose logs -f frontend --tail 100
