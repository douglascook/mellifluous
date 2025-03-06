DB_URL="sqlite:db/mellifluous.sqlite3"
DB_MIGRATIONS=./db/migrations

add-migration:
	dbmate --url $(DB_URL) --migrations-dir $(DB_MIGRATIONS) new

migrate:
	dbmate up

run-dev:
	fastapi dev app/main.py
