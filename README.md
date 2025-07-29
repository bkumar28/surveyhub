**surveyhub** is a Django-based Survey Management System designed to let organizations or individuals create, distribute, and analyze surveys with ease. It provides a robust backend, API support, and is ready for production deployment with Docker.

##  Key Features

- **Create surveys with customizable questions** - Build surveys with various question types (text, choice, rating, etc.), set required/optional fields, and order questions as needed
- **Manage survey lifecycle** - Save as drafts, publish for responses, pause, or mark as expired/completed with flexible management and scheduling
- **Collect responses** - Support both invited users (email, token) and anonymous responses
- **Generate analytics reports** - Aggregate responses and provide insights like popular/unpopular answers, completion rates, and data analytics
- **Swagger API documentation** - All endpoints documented and browsable via Swagger UI for easy integration and testing
- ** Admin interface** - Django admin for managing surveys, questions, responses, and users
- ** Dynamic question handling** - Advanced question logic with conditional questions and various field types
- **Dockerized deployment** - Complete Docker and Docker Compose support for easy setup and scaling
- **Automated setup scripts** - Scripts for dependencies, database setup, and sample data loading

##  Table of Contents

- [Quick Start](#-quick-start)
- [Available Scripts](#-available-scripts)
- [Testing](#-testing)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [Maintainer](#-maintainer)

##  Quick Start

### Prerequisites
- Python 3.12
- Docker & Docker Compose
- Poetry (recommended) or virtualenv

### 1. Clone the Repository
```bash
git clone https://github.com/Bkumar28/surveyhub.git
cd surveyhub/
```
### 2. Environment Configuration:
```bash
# Generate environment file
./scripts/generate_env.sh

# Edit .env file as needed
nano .env
```

### 3. Setup Development Environment
```bash
# Install all prerequisites (Python, Docker, Poetry, dependencies)
./scripts/pre_requisites.sh
```

### 4. Build and Start Docker Containers
```bash
# Build and start containers
./scripts/docker_build_up.sh

# Or step by step:
./scripts/docker_build_up.sh build    # Build containers only
./scripts/docker_build_up.sh up       # Start containers only
```

### 5. Load Sample Data (Optional)
```bash
./scripts/load_sample_data.sh
```

### 6. Access the Application
- **API Documentation**: [http://localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/)
- **Admin Interface**: [http://localhost:8000/admin/](http://localhost:8000/admin/)

### Additional Development Commands

**Database Management:**
```bash
# Create and apply migrations
./scripts/manage_migrations.sh makemigrations
./scripts/manage_migrations.sh migrate

# Load sample data
./scripts/load_sample_data.sh
# Or load only users
./scripts/load_sample_data.sh --users-only
```

**Docker Management:**
```bash
# Build containers
docker compose build

# Start containers
docker compose up -d

# Stop containers
docker compose down
```

## Available Scripts

The project includes several automation scripts in the `scripts/` directory:

### `pre_requisites.sh`
**Complete development environment setup**
```bash
./scripts/pre_requisites.sh [--use-venv]
```

**Features:**
- Installs Python 3.12, Docker & Docker Compose
- Sets up Poetry for dependency management
- Configures pre-commit hooks with ruff formatting
- Installs project dependencies
- Builds Docker images and runs initial migrations

### `load_sample_data.sh`
**Load sample data fixtures into the database**
```bash
./scripts/load_sample_data.sh [--users-only]
```

**Data loaded in dependency order:**
- users.json → template_categories.json → survey_templates.json
- question_templates.json → surveys.json → questions.json
- question_options.json → survey_invitations.json → survey_responses.json
- answers.json → survey_analytics.json → question_analytics.json

### `manage_migrations.sh`
**Django migration management wrapper for Docker**
```bash
./scripts/manage_migrations.sh <command> [options]
```

**Examples:**
```bash
./scripts/manage_migrations.sh makemigrations myapp
./scripts/manage_migrations.sh migrate --database default
./scripts/manage_migrations.sh showmigrations
./scripts/manage_migrations.sh sqlmigrate auth 0001_initial
```

### `run_tests.sh`
**Run Django pytest tests with coverage support**
```bash
./scripts/run_tests.sh [--venv] [--coverage] [--junit] [pytest_args]
```

**Examples:**
```bash
./scripts/run_tests.sh --coverage           # Generate coverage report
./scripts/run_tests.sh --venv --coverage -v # Local + coverage + verbose
./scripts/run_tests.sh -k test_function     # Run specific test
```

### `generate_env.sh`
**Generate .env file with default development settings**
```bash
./scripts/generate_env.sh
```

**Includes:** Django settings, database config, Redis, email backend, CORS settings

### `docker_build_up.sh`
**Build and start Docker containers**
```bash
./scripts/docker_build_up.sh [build|up]
```

**Usage:**
- `./scripts/docker_build_up.sh` - Build and start containers (default)
- `./scripts/docker_build_up.sh build` - Build containers only
- `./scripts/docker_build_up.sh up` - Start containers only

**Note:** Run `./scripts/pre_requisites.sh` first to install Docker

### `docker_entrypoint.sh`
**Docker container initialization script (auto-executed)**

**Functions:**
- Waits for dependent services (database, Redis)
- Installs Poetry dependencies
- Runs Django migrations and collects static files
- Starts Gunicorn server on port 8000

## Testing

### Run All Tests
```bash
# Docker environment
./scripts/run_tests.sh

# Local environment
./scripts/run_tests.sh --venv
```

### Coverage Reports
```bash
# Generate HTML coverage report
./scripts/run_tests.sh --coverage

# View coverage report
open htmlcov/index.html
```

### CI/CD Integration
```bash
# Generate junit.xml for CI pipelines
./scripts/run_tests.sh --junit --coverage
```

## API Documentation

### Swagger UI
Access interactive API documentation at:
- **Local/Docker**: [http://localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/)





## 💻 Maintainer

**Bharat Kumar**  </br>
_Senior Software Engineer | Cloud & Backend Systems_  </br>
📧 kumar.bhart28@gmail.com </br>
🔗 [LinkedIn](https://www.linkedin.com/in/bharat-kumar28)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
