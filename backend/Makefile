include .env

run:
	poetry run python manage.py runserver 0.0.0.0:$(WEB_PORT)

makemigrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

superuser:
	poetry run python manage.py createsuperuser

shell:
	poetry run python manage.py shell

test:
	poetry run pytest
	