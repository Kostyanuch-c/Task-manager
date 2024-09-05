MANAGE := poetry run python manage.py
PORT ?= 8000

.PHONY: install
install:
	@poetry install

.PHONY: migrate
migrate:
	@$(MANAGE) migrate

.PHONY: shell
shell:
	@$(MANAGE) shell_plus --ipython

.PHONY: lint
lint:
	@poetry run flake8 task_manager

.PHONY: run
run:
	@$(MANAGE) runserver

.PHONY: collectstatic
collectstatic:
	@$(MANAGE) collectstatic --noinput

.PHONY: start
start: migrate collectstatic
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi:application

