# Default compose file and env
COMPOSE_ROOT=docker-compose.yml
ENV_FILE=.env

# Docker Compose commands
DC=docker-compose -f $(COMPOSE_ROOT) --env-file $(ENV_FILE)

# Targets
.PHONY: up down clean restart logs shell migrate collectstatic createsuperuser test dumpdata loaddata makemigrations

# Run full stack (backend + frontend + nginx + db)
up:
    $(DC) up --build

# Stop all services
down:
    $(DC) down

# Clean up everything
clean:
    $(DC) down -v --remove-orphans

# Restart stack
restart:
    make down && make up

# Tail logs
logs:
    $(DC) logs -f

# Run shell inside backend container
shell:
    $(DC) exec backend sh

# Run Python shell
python:
    $(DC) exec backend python manage.py shell

# Run migrations
migrate:
    $(DC) exec backend python manage.py migrate

# Make migrations
makemigrations:
    $(DC) exec backend python manage.py makemigrations

# Create superuser
createsuperuser:
    $(DC) exec backend python manage.py createsuperuser

# Collect static files
collectstatic:
    $(DC) exec backend python manage.py collectstatic --noinput

# Run backend tests
test:
    $(DC) exec backend python manage.py test

# Dump data to fixture
dumpdata:
    $(DC) exec backend python manage.py dumpdata --indent 2 > sample_data/data.json

# Load data from fixture using the load_data.sh script
loaddata:
    bash scripts/load_data.sh
