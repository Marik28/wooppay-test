install:
	pip install -U pip setuptools
	pip install -r requirements.txt

notebook:
	jupyter notebook

makemigrations:
	cd src; alembic revision --autogenerate

migrate:
	cd src; alembic upgrade head

downgrade:
	cd src; alembic downgrade -1

db:
	docker compose --env-file .env -p wooppay-test -f devops/docker-compose.yaml up db --build --detach

app-dev:
	cd src; python -m app

app-docker:
	docker compose --env-file .env -p wooppay-test -f devops/docker-compose.yaml up app --build --detach


admin-dev:
	cd src; python -m admin

test:
	export PYTHONPATH=src/; pytest -vs

createsuperuser:
	cd src; python -m scripts.createsuperuser