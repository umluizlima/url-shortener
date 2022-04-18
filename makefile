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

.PHONY: migrate
migrate:
	python manage.py migrate

.PHONY: test
test:
	python manage.py test

.PHONY: run
run:
	python manage.py runserver
