#!/bin/bash
# Script to load all sample data JSON files into the Django database in dependency order
# Usage: ./load_sample_data.sh

set -e

WORKDIR="$(dirname "$0")"
SAMPLEDIR="$WORKDIR/../sample_data"
MANAGE="../src/manage.py"

if [ ! -f "$MANAGE" ]; then
  echo "Error: manage.py not found at $MANAGE"
  exit 1
fi

cd "$WORKDIR/.."

# Check for --users-only flag
USERS_ONLY=false
for arg in "$@"; do
  if [ "$arg" == "--users-only" ]; then
    USERS_ONLY=true
    break
  fi
done

if [ "$USERS_ONLY" = true ]; then
  echo "Loading only users.json ..."
  FILEPATH="$SAMPLEDIR/users.json"
  if [ ! -f "$FILEPATH" ]; then
    echo "Error: users.json not found in $SAMPLEDIR"
    exit 1
  fi
  python src/manage.py loaddata "$FILEPATH"
  echo "User data loaded successfully."
else
  # List of sample data files in dependency order
  DATA_FILES=(
    "users.json"
    "template_categories.json"
    "survey_templates.json"
    "question_templates.json"
    "surveys.json"
    "questions.json"
    "question_options.json"
    "survey_invitations.json"
    "survey_responses.json"
    "answers.json"
    "survey_analytics.json"
    "question_analytics.json"
  )

  for file in "${DATA_FILES[@]}"; do
    FILEPATH="$SAMPLEDIR/$file"
    if [ ! -f "$FILEPATH" ]; then
      echo "Error: $file not found in $SAMPLEDIR"
      exit 1
    fi
    echo "Loading $file ..."
    python src/manage.py loaddata "$FILEPATH"
  done
  echo "Sample data loaded successfully in dependency order."
fi
