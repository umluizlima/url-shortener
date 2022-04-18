.PHONY: environment
environment:
	pyenv install -s 3.10.0
	pyenv uninstall --force url-shortener
	pyenv virtualenv 3.10.0 --force url-shortener
	pyenv local url-shortener

.PHONY: install
install:
	pip freeze | xargs -r pip uninstall -y
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	pre-commit install

.PHONY: db_init
db_init:
	docker-compose up -d database

.PHONY: migrate
migrate: db_init
	python manage.py migrate

.PHONY: generate_migrations
generate_migrations: migrate
	python manage.py makemigrations

.PHONY: test
test:
	python manage.py test

.PHONY: run
run: migrate
	python manage.py runserver
