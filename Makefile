setup:
	@echo "Instalando dependências..."
	@uv run pip install -r requirements.txt

dependencies:
	@make setup
	@uv run pip install -U pip
	@uv run pip install -e .

lint:
	@echo "Checking code style ..."
	@uv run python -m ruff check . --exclude=utils

style:
	@echo "Applying code style ..."
	@uv run python -m ruff . --fix --exclude=utils

run:
	@echo "Iniciando o servidor de desenvolvimento..."
	@uv run python manage.py runserver

showmigrations:
	@echo "Listando migrações aplicadas e pendentes..."
	@uv run python manage.py showmigrations

migrate:
	@echo "Aplicando migrações a todos os bancos de dados..."
	@uv run python manage.py migrate

makemigrations:
	@echo "Criando novas migrações..."
	@uv run python manage.py makemigrations

superuser:
	@echo "Criando um superusuário..."
	@-uv run python manage.py createsuperuser --noinput

shell:
	@echo "Acessando o shell do Django..."
	@uv run python manage.py shell

unit:
	@echo "Rodando testes..."
	# @uv run python manage.py test
	APP_NAME=sample-app ENV=test DEBUG=0 DJANGO_SETTINGS_MODULE=tests.settings uv python -m pytest --pdb

start:
	@echo "Criando novas migrações..."
	@uv run python manage.py makemigrations
	@echo "Aplicando migrações..."
	@uv run python manage.py migrate
	@echo "Criando superusuário..."
	@-uv python manage.py createsuperuser --noinput
	@echo "Iniciando o servidor..."
	@uv run python manage.py runserver 0.0.0.0:8000
