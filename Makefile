lint:
	poetry run ruff check .

lint-fix:
	poetry run ruff check --fix .

format:
	poetry run black .

dev:
	nodemon --watch '*.py' --exec 'poetry run python main.py' --verbose

run:
	docker compose -f docker-compose.dev.yml up --build -d