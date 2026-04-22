.PHONY: up down logs migrate

up:
	docker compose -f infrastructure/docker-compose.yml up --build

down:
	docker compose -f infrastructure/docker-compose.yml down

logs:
	docker compose -f infrastructure/docker-compose.yml logs -f

migrate:
	cd services/core-api && alembic upgrade head
