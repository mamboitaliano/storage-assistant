.PHONY: first-start

# Boot the dev stack in detached mode, then install frontend deps on the host
first-start:
	git checkout develop && git pull origin develop
	docker compose -f docker-compose.dev.yml up -d --build
	cd frontend && npm install
	docker compose -f docker-compose.dev.yml exec -w /app/backend app python -m app.seed.runner

rebuild:
	docker compose -f docker-compose.dev.yml down
	docker compose -f docker-compose.dev.yml up -d --build
	cd frontend && npm install
	docker compose -f docker-compose.dev.yml exec -w /app/backend app python -m app.seed.runner

install-backend-deps:
	docker compose -f docker-compose.dev.yml exec -w /app/backend app pip install -r requirements.txt

install-frontend-deps:
	docker compose -f docker-compose.dev.yml exec -w /app/frontend app npm install

run-backend:
	docker compose -f docker-compose.dev.yml exec -w /app/backend app uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

run-frontend:
	docker compose -f docker-compose.dev.yml exec -w /app/frontend app npm run dev -- --host --port 5173

run-all:
	make run-backend & make run-frontend

test-backend:
	docker compose -f docker-compose.dev.yml exec -w /app/backend app pytest -v tests/

test-frontend:
	docker compose -f docker-compose.dev.yml exec -w /app/frontend app npm run test

test-all:
	make test-backend & make test-frontend

seed-data:
	docker compose -f docker-compose.dev.yml exec -w /app/backend app python -m app.seed.runner