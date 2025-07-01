
## Poetry Setup & Usage Guide

**Install Poetry globally (if not already):**
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

**Ensure it's in your PATH:**
```bash
export PATH="$HOME/.local/bin:$PATH"
```
Add that line to your shell profile (`~/.bashrc`, `~/.zshrc`, , or `~/.profile`)

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