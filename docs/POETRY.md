
## Poetry Usage Guide

## Use Poetry in your project:
**Navigate to the project directory:**
```bash
cd /path/to/surveyhub
```
**Install dependencies:**
```bash
poetry install
```

**(Optional) If you want to enter the virtual environment::**
```
poetry shell
```
**Run Django management commands:**
```bash
poetry run python manage.py makemigrations
poetry run python manage.py migrate
poetry run python manage.py runserver
```
**Run Celery worker:**
```bash
poetry run celery -A src worker --loglevel=info
```
**Run tests:**
```bash
poetry run pytest
```

## Managing Dependencies
**Add a new package:**
```bash
poetry add package-name
```
**Example:**
```bash
poetry add djangorestframework-simplejwt@^4.8.0
```

**Add a development-only dependency:**
```bash
poetry add --group dev package-name
```

**Update specific dependency**
```bash
poetry update numpy
```
**Regenerate lock file without upgrading dependencies:**
```bash
poetry lock --no-update
```

**Export to requirements.txt (for Docker or legacy use):**
```bash
poetry export -f requirements.txt --without-hashes -o requirements.txt
```

## You can always check where poetry is installed with:
```bash
which poetry
```

## Update `pyproject.toml` and install dependency
```bash
poetry lock
poetry install --with dev
```

##  Check what’s outdated

Run this before and after to verify:
```bash
poetry show --outdated
```

## Update bulk outdated packages

```bash
poetry show --outdated --top-level | awk '{print $1}' | xargs -n1 -I{} poetry add "{}@latest"
```
