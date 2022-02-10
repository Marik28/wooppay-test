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