#!/bin/bash
# -----------------------------------------------------------------------------
# Script: run_tests.sh
#
# Description:
#   Run Django pytest tests (Docker or local) with options:
#     --coverage: generate coverage report (htmlcov/)
#     --junit:    generate junit.xml (for CI pipelines)
#     --app <appname|module|file>: run tests for a specific app, module, or file (e.g. blueprints, blueprints/tests/test_views.py)
#     <appname|module|file>: as first argument, run tests for a specific app, module, or file (e.g. blueprints, blueprints/tests/test_views.py)
#
# Usage:
#   ./run_tests.sh                                 # Run all tests (Docker + Poetry)
#   ./run_tests.sh -k test_func                    # Run specific test by keyword
#   ./run_tests.sh --venv                          # Run all tests locally via Poetry
#   ./run_tests.sh --coverage --junit              # With coverage & junit
#   ./run_tests.sh --venv --coverage -v            # Local + coverage + verbose
#   ./run_tests.sh blueprints                      # Run only blueprints app tests (Docker)
#   ./run_tests.sh blueprints/tests/test_views.py  # Run only view tests (Docker)
#   ./run_tests.sh --venv blueprints               # Run only blueprints app tests (local)
#   ./run_tests.sh --venv blueprints/tests/test_views.py # Run only view tests (local)
#   ./run_tests.sh --app blueprints                # Alternate: Run only blueprints app tests (Docker)
#   ./run_tests.sh --venv --app blueprints         # Alternate: Run only blueprints app tests (local)
# -----------------------------------------------------------------------------

set -e

SERVICE_NAME="web"
DOCKER_APP_DIR="/app/src"
LOCAL_APP_DIR="src"
COV_REPORT_DIR="htmlcov"
JUNIT_FILE="junit.xml"

# Flags
USE_VENV=false
USE_COV=false
USE_JUNIT=false



# Test target (app, module, or file)
TEST_TARGET=""
# Collect pytest args
PYTEST_ARGS=()


# Parse script arguments
# If first argument is not an option, treat as test target (app, module, or file)
if [[ $# -gt 0 && "$1" != --* ]]; then
  TEST_TARGET="$1"
  shift
fi

while [[ $# -gt 0 ]]; do
  case $1 in
    --venv)
      USE_VENV=true
      shift
      ;;
    --coverage)
      USE_COV=true
      shift
      ;;
    --junit)
      USE_JUNIT=true
      shift
      ;;
    --app)
      TEST_TARGET="$2"
      shift 2
      ;;
    *)
      PYTEST_ARGS+=("$1")
      shift
      ;;
  esac
done

# Build optional pytest arguments
EXTRA_ARGS=()
if $USE_COV; then
  EXTRA_ARGS+=(--cov="$LOCAL_APP_DIR" --cov-report=term --cov-report=html:"$COV_REPORT_DIR")
fi

if $USE_JUNIT; then
  EXTRA_ARGS+=(--junitxml="$JUNIT_FILE")
fi

# Run test: local virtualenv
if $USE_VENV; then
  echo "Running tests locally using Poetry virtualenv..."
  # If a test target is specified, run only that app/module/file
  if [[ -n "$TEST_TARGET" ]]; then
    poetry run pytest "$LOCAL_APP_DIR/$TEST_TARGET" "${EXTRA_ARGS[@]}" "${PYTEST_ARGS[@]}"
  else
    poetry run pytest "$LOCAL_APP_DIR" "${EXTRA_ARGS[@]}" "${PYTEST_ARGS[@]}"
  fi
else
  echo "Running tests inside Docker container '$SERVICE_NAME'..."

  # Start container if not running
  if ! docker compose ps | grep -q "$SERVICE_NAME.*running"; then
    echo "Starting Docker container..."
    docker compose up -d "$SERVICE_NAME"
    sleep 5
  fi

  # If a test target is specified, run only that app/module/file
  if [[ -n "$TEST_TARGET" ]]; then
    docker compose exec "$SERVICE_NAME" poetry run pytest "$DOCKER_APP_DIR/$TEST_TARGET" "${EXTRA_ARGS[@]}" "${PYTEST_ARGS[@]}"
  else
    docker compose exec "$SERVICE_NAME" poetry run pytest "$DOCKER_APP_DIR" "${EXTRA_ARGS[@]}" "${PYTEST_ARGS[@]}"
  fi
fi
