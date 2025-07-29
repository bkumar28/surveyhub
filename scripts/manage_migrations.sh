#!/bin/bash
# -----------------------------------------------------------------------------
# Script: manage_migrations.sh
#
# Description:
#   A helper script to run Django migration-related commands inside a Docker
#   container using Poetry. It wraps around manage.py and supports passing
#   additional arguments (e.g., app names, database options).
#
# Usage Examples:
#   ./manage_migrations.sh makemigrations
#   ./manage_migrations.sh makemigrations myapp
#   ./manage_migrations.sh migrate
#   ./manage_migrations.sh migrate --database default
#   ./manage_migrations.sh showmigrations
#   ./manage_migrations.sh sqlmigrate auth 0001_initial
#   ./manage_migrations.sh squashmigrations myapp
# -----------------------------------------------------------------------------

set -e  # Exit immediately if a command exits with a non-zero status

# ------------------------------
# Configuration
# ------------------------------
WORKDIR="/app/src"                # Django project root path inside the container
MANAGE="$WORKDIR/manage.py"      # Full path to manage.py inside the container

# ------------------------------
# Function: run_in_docker
# Description:
#   Executes the Django manage.py command inside the Docker container
#   using Poetry's virtual environment.
# Arguments:
#   $@ - The full manage.py command with arguments
# ------------------------------
run_in_docker() {
  docker compose exec web poetry run python "$@"
}

# ------------------------------
# Function: ensure_docker_services
# Description:
#   Ensures required Docker services ('web' and 'db') are running.
#   If not, it builds and starts the containers.
#   Waits for the web container to become responsive.
# ------------------------------
ensure_docker_services() {
  echo "Checking if Docker services are already running..."

  local services_running=true

  # Loop through required services and check if they are running
  for service in web db; do
    if ! docker compose ps --services --filter "status=running" | grep -q "^${service}$"; then
      echo "Service '$service' is not running."
      services_running=false
    fi
  done

  # If all required services are running, skip build and startup
  if [ "$services_running" = true ]; then
    echo "All required services are running."
    return 0
  fi

  # Build and start services if not already running
  echo "Building and starting Docker services..."
  docker compose build
  docker compose up -d

  # Wait briefly to allow services to initialize
  echo "Waiting for services to be ready..."
  sleep 10

  # Retry loop to check container readiness
  local max_attempts=30
  local attempt=0

  while [ $attempt -lt $max_attempts ]; do
    if docker compose exec web echo "Container ready" >/dev/null 2>&1; then
      echo "Docker services are ready."
      return 0
    fi
    attempt=$((attempt + 1))
    echo "Attempt $attempt/$max_attempts: Services not ready yet, waiting..."
    sleep 3
  done

  echo "Error: Docker services failed to become ready after $max_attempts attempts."
  exit 1
}

# ------------------------------
# Function: show_help
# Description:
#   Prints the usage/help message for the script.
# ------------------------------
show_help() {
  echo "Usage: $0 <command> [options]"
  echo ""
  echo "Supported Django management commands:"
  echo "  makemigrations [app_label]     Create new migrations"
  echo "  migrate [app_label]            Apply migrations"
  echo "  showmigrations                 List migrations and their status"
  echo "  sqlmigrate <app> <migration>   Show SQL for a specific migration"
  echo "  squashmigrations <app_label>   Combine migrations into one"
  echo "  flush --noinput                Clear all data from the database"
  echo ""
  echo "Examples:"
  echo "  $0 makemigrations"
  echo "  $0 migrate --database default"
  echo "  $0 sqlmigrate auth 0001_initial"
  echo ""
  exit 1
}

# ------------------------------
# Main Script Logic
# ------------------------------

# Step 1: Ensure a command is provided
if [ $# -lt 1 ]; then
  echo "Error: No command provided."
  show_help
fi

# Step 2: Extract the command and arguments
COMMAND=$1        # e.g., migrate
shift             # Remove command from args
ARGS="$@"         # All remaining arguments

# Step 3: Ensure containers are running
ensure_docker_services

# Step 4: Confirm manage.py exists inside the container
if ! docker compose exec web test -f "$MANAGE"; then
  echo "Error: manage.py not found at $MANAGE inside the container."
  exit 1
fi

# Step 5: Dispatch and execute the Django management command
case "$COMMAND" in
  makemigrations|migrate|showmigrations|sqlmigrate|squashmigrations|flush)
    # Auto-append --noinput for flush if not provided
    if [ "$COMMAND" = "flush" ] && [[ ! "$ARGS" =~ "--noinput" ]]; then
      ARGS="$ARGS --noinput"
    fi
    echo "Running: python $MANAGE $COMMAND $ARGS"
    run_in_docker "$MANAGE" $COMMAND $ARGS
    ;;
  --help|-h|help)
    show_help
    ;;
  *)
    echo "Error: Invalid command '$COMMAND'"
    show_help
    ;;
esac
