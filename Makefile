.EXPORT_ALL_VARIABLES:

# ==============================================================================
# Development Environment
# ==============================================================================

run::
	docker compose -f docker-compose.dev.yml up -d

restart::
	docker compose -f docker-compose.dev.yml restart

down::
	docker compose -f docker-compose.dev.yml down

stop::
	docker compose -f docker-compose.dev.yml stop

down-v::
	docker compose -f docker-compose.dev.yml down -v

build::
	docker compose -f docker-compose.dev.yml build --parallel

backend-test::
	docker compose -f docker-compose.dev.yml run --rm tests

backend-test-bash::
	docker compose -f docker-compose.dev.yml run tests /bin/bash

backend-bash::
	docker compose -f docker-compose.dev.yml exec -ti backend bash

frontend-bash::
	docker compose -f docker-compose.dev.yml exec -ti frontend bash

logs::
	docker compose -f docker-compose.dev.yml logs -f

backend-logs::
	docker compose -f docker-compose.dev.yml logs -f backend --tail 100

frontend-logs::
	docker compose -f docker-compose.dev.yml logs -f frontend --tail 100

celery-logs::
	docker compose -f docker-compose.dev.yml logs -f celery-worker --tail 100

migration::
	docker compose -f docker-compose.dev.yml exec -ti backend bash -c "alembic revision --autogenerate -m $(message)"

init-db::
	docker compose -f docker-compose.dev.yml exec -ti backend bash -c "python -m app.db.seeds all"

import-patients::
	docker compose -f docker-compose.dev.yml exec -ti backend bash -c "python -m app.db.import_scripts.import_patients"

import-appointments::
	docker compose -f docker-compose.dev.yml exec -ti backend bash -c "python -m app.db.import_scripts.import_appointments"


# ==============================================================================
# Production Environment
# ==============================================================================

run-prod::
	docker compose -f docker-compose.prod.yml up -d

restart-prod::
	docker compose -f docker-compose.prod.yml restart

down-prod::
	docker compose -f docker-compose.prod.yml down

stop-prod::
	docker compose -f docker-compose.prod.yml stop

down-v-prod::
	docker compose -f docker-compose.prod.yml down -v

build-prod::
	docker compose -f docker-compose.prod.yml build --parallel

logs-prod::
	docker compose -f docker-compose.prod.yml logs -f

# ==============================================================================
# Database
# ==============================================================================

db::
	docker compose -f docker-compose.dev.yml exec -it backend sqlite3 app/db/blu.sqlite3
