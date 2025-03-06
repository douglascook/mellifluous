DB_FILE="db/mellifluous.sqlite3"
DB_URL="sqlite:${DB_FILE}"
DB_MIGRATIONS=./db/migrations

add-migration:
	dbmate --url $(DB_URL) --migrations-dir $(DB_MIGRATIONS) new

migrate:
	dbmate up

reset-db:
	rm ${DB_FILE} && dbmate up

run-dev:
	fastapi dev app/main.py
