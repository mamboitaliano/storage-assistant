.PHONY: first-start

# Boot the dev stack in detached mode, then install frontend deps on the host
first-start:
	docker compose -f docker-compose.dev.yml up -d --build
	cd frontend && npm install
	docker compose -f docker-compose.dev.yml exec -w /app/backend app python -m app.seed.runner
