MANAGE := poetry run python manage.py
PORT ?= 8000

.PHONY: install
install:
	@poetry install

.PHONY: build
build:
	@poetry install --no-dev

.PHONY: create_migrations
create_migrations:
	@$(MANAGE) makemigrations

.PHONY: create_migrations migrate
migrate:
	@$(MANAGE) migrate

.PHONY: shell
shell:
	@$(MANAGE) shell_plus --ipython

.PHONY: lint
lint:
	@poetry run flake8 task_manager

.PHONY: dev
dev:
	@$(MANAGE) runserver

.PHONY: collectstatic
collectstatic:
	@$(MANAGE) collectstatic --noinput

.PHONY: start
start: migrate collectstatic
	@poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi:application

.PHONY: translate
translate:
	@poetry run django-admin makemessages --ignore="static" --ignore=".env"  -l ru

.PHONY: upload_translate
upload_translate:
	@poetry run django-admin compilemessages

.PHONY: test
test:
	poetry run pytest

.PHONY: test-coverage
test-coverage:
	poetry run pytest --cov=task_manager --cov-report xml
