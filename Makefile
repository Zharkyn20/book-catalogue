 all: install env migrate run

install:
	pip install -r requirements.txt

env:
	cp example.env .env

migrate:
	python3 manage.py makemigrations
	python3	manage.py migrate

run:
	python3 manage.py runserver 0.0.0.0:8000

del_migrations:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete
