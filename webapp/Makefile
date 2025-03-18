rebuild:
	docker compose build --no-cache

run:
	docker compose up --build

down:
	docker compose down

prune-db:
	docker volume rm webapp_webapp_db_data

prune-minio:
	docker volume rm webapp_minio_data

prune-all:
	docker system prune --volumes

push:
	bash ./scripts/source.auth_ecr.sh
	# or source ./scripts/source.auth_ecr.sh for later interactive use
	docker compose push web
