#!/bin/bash

# Start full stack (backend + frontend + nginx + db)

set -e

BACKEND_FILE="docker-compose.backend.yml"
ROOT_FILE="docker-compose.yml"
ENV_FILE=".env"

# Colors
GREEN="\033[0;32m"
RED="\033[0;31m"
NC="\033[0m"

# Check .env exists
if [ ! -f "$ENV_FILE" ]; then
  echo -e "${RED}.env file not found. Please create one in the project root.${NC}"
  exit 1
fi

echo -e "${GREEN} Starting full stack services...${NC}"
docker-compose -f "$BACKEND_FILE" -f "$ROOT_FILE" --env-file "$ENV_FILE" up --build
