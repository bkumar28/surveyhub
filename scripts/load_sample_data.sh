#!/bin/bash
# -----------------------------------------------------------------------------
# Script: load_sample_data.sh
#
# Description:
#   Loads all sample data JSON files into the Django database inside Docker.
#   Ensures Docker services are running, migrations are applied, and data
#   fixtures are loaded in dependency order. Supports an option to load only
#   user data.
#
# Usage:
#   ./load_sample_data.sh            # Loads all fixtures
#   ./load_sample_data.sh --users-only  # Loads only users.json
# -----------------------------------------------------------------------------

set -e  # Exit immediately if a command exits with a non-zero status

# =============================================================================
# CONFIGURATION
# =============================================================================

WORKDIR="/app/src"                         # Path to Django project in container
SAMPLEDIR="$WORKDIR/../.sample_data"        # Path to local fixture directory
MANAGE="$WORKDIR/manage.py"                # Full path to manage.py inside container
USERS_ONLY=false                           # Default: load all fixtures

# =============================================================================
# FUNCTIONS
# =============================================================================

# -----------------------------------------------------------------------------
# Function: run_in_docker
# Description:
#   Executes a Python command inside the Docker 'backend' container using Poetry.
# Arguments:
#   $@ - The manage.py command and its arguments
# -----------------------------------------------------------------------------
run_in_docker() {
  docker compose exec backend poetry run python "$@"
}

# -----------------------------------------------------------------------------
# Function: check_file_exists
# Description:
#   Checks if a given file path exists inside the backend container.
# Arguments:
#   $1 - Full file path to check
# -----------------------------------------------------------------------------
check_file_exists() {
  local filepath="$1"
  if ! docker compose exec backend test -f "$filepath"; then
    echo "Error: File not found at $filepath inside the container"
    exit 1
  fi
}

# -----------------------------------------------------------------------------
# Function: wait_for_database
# Description:
#   Waits until the database is ready to accept connections by checking
#   Django's check command against the default DB.
# -----------------------------------------------------------------------------
wait_for_database() {
  local max_attempts=30
  local attempt=0

  echo "Waiting for database to be accessible..."

  while [ $attempt -lt $max_attempts ]; do
    if run_in_docker "$MANAGE" check --database default >/dev/null 2>&1; then
      echo "Database is ready."
      return 0
    fi
    attempt=$((attempt + 1))
    echo "Attempt $attempt/$max_attempts: Database not ready yet, retrying..."
    sleep 3
  done

  echo "Error: Database connection failed after $max_attempts attempts"
  exit 1
}

# -----------------------------------------------------------------------------
# Function: load_data_file
# Description:
#   Loads a single JSON data fixture using Django's loaddata command.
# Arguments:
#   $1 - The name of the JSON file to load
# -----------------------------------------------------------------------------
load_data_file() {
  local filename="$1"
  local filepath="$SAMPLEDIR/$filename"

  echo "Loading $filename..."
  check_file_exists "$filepath"

  if ! run_in_docker "$MANAGE" loaddata "$filepath"; then
    echo "Error: Failed to load $filename"
    exit 1
  fi

  echo "✓ $filename loaded successfully"
}

# -----------------------------------------------------------------------------
# Function: ensure_docker_services
# Description:
#   Checks if required services (backend, db) are running.
#   If not, builds and starts them using Docker Compose.
# -----------------------------------------------------------------------------
ensure_docker_services() {
  echo "Checking if Docker services are already running..."

  local services_running=true

  # Check if both 'backend' and 'db' containers are running
  for service in backend db; do
    if ! docker compose ps --services --filter "status=running" | grep -q "^${service}$"; then
      echo "Service '$service' is not running."
      services_running=false
    fi
  done

  # If already running, skip build/start
  if [ "$services_running" = true ]; then
    echo "All required services are already running. Skipping build/start."
    return 0
  fi

  echo "Building and starting Docker services..."
  docker compose build
  docker compose up -d

  # Small delay for services to settle
  echo "Waiting for services to be ready..."
  sleep 10
}

# =============================================================================
# ARGUMENT PARSING
# =============================================================================

# Parse CLI arguments
for arg in "$@"; do
  case $arg in
    --users-only)
      USERS_ONLY=true
      shift
      ;;
    --help|-h)
      echo "Usage: $0 [--users-only]"
      echo ""
      echo "Options:"
      echo "  --users-only    Load only users.json"
      echo "  --help, -h      Show this help message"
      exit 0
      ;;
    *)
      echo "Unknown option: $arg"
      echo "Run with --help for usage."
      exit 1
      ;;
  esac
done

# =============================================================================
# MAIN EXECUTION
# =============================================================================

echo "=== SurveyHub Sample Data Loader ==="

# Step 1: Ensure Docker containers are running
ensure_docker_services

# Step 2: Confirm manage.py exists in the container
echo "Checking for manage.py..."
check_file_exists "$MANAGE"

# Step 3: Wait for database readiness
wait_for_database

# Step 4: Run migrations to apply DB schema
echo "Running migrations..."
run_in_docker "$MANAGE" migrate

# =============================================================================
# Step 5: Load Fixture Data
# =============================================================================

if [ "$USERS_ONLY" = true ]; then
  echo "=== Loading Users Data Only ==="
  load_data_file "users.json"
  echo "✓ User data loaded successfully."
else
  echo "=== Loading All Sample Data ==="

  # List of fixture files in dependency-safe order
  DATA_FILES=(
    "users.json"
    "blueprint_categories.json"
    "survey_blueprints.json"
    "question_blueprints.json"
    "surveys.json"
    "questions.json"
    "question_options.json"
    "survey_responses.json"
    "answers.json"
    "survey_analytics.json"
    "question_analytics.json"
  )

  echo "Loading ${#DATA_FILES[@]} data files in dependency order..."

  # Loop and load each fixture
  for file in "${DATA_FILES[@]}"; do
    load_data_file "$file"
  done

  echo "✓ All sample data loaded successfully."
fi

echo "=== Data Loading Complete ==="
