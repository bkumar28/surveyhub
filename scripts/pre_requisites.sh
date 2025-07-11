#!/bin/bash

set -e

# Ensure Python 3.12 is installed
if ! command -v python3.12 &> /dev/null; then
  echo "Python 3.12 not found. Installing Python 3.12..."
  sudo apt update
  sudo apt install -y software-properties-common
  sudo add-apt-repository -y ppa:deadsnakes/ppa
  sudo apt update
  sudo apt install -y python3.12 python3.12-venv python3.12-distutils
else
  echo "Python 3.12 is already installed."
fi

echo "Installing Docker GPG key and setting up repository..."

sudo apt update
sudo apt install -y ca-certificates curl gnupg

sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu noble stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

echo "Installing Docker Engine, CLI, Buildx and Compose plugin..."

sudo apt update
sudo apt install -y \
    docker-ce \
    docker-ce-cli \
    containerd.io \
    docker-buildx-plugin \
    docker-compose-plugin

echo "Docker and Docker Compose plugin installed successfully."

echo "Testing Docker:"
sudo docker run hello-world

echo "Optional: Add your user to the docker group to run without sudo:"
sudo usermod -aG docker "$USER"
echo "Done! Log out and back in or run 'newgrp docker' to apply changes."


# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -
export PATH="$HOME/.local/bin:$PATH"

# Configure Poetry to not create a virtual environment
poetry config virtualenvs.create false

# Install Python dependencies
USE_POETRY=true
for arg in "$@"; do
  if [ "$arg" == "--use-venv" ]; then
    USE_POETRY=false
    break
  fi
done

if [ "$USE_POETRY" = true ]; then
  if [ -f pyproject.toml ]; then
    echo "Installing Python dependencies with Poetry..."
    poetry install
  fi
else
  # Create and activate virtualenv if not already active
  if [ -z "$VIRTUAL_ENV" ]; then
    if [ ! -d "venv" ]; then
      echo "Creating Python virtual environment..."
      python3 -m venv venv
    fi
    echo "Activating virtual environment..."
    source venv/bin/activate
  fi
  if [ -f requirements.txt ]; then
    echo "Installing Python dependencies from requirements.txt..."
    pip3 install -r requirements.txt
  fi
fi

# Run Django migrations
if [ -f src/manage.py ]; then
  echo "Running Django migrations..."
  python3 src/manage.py makemigrations
  python3 src/manage.py migrate
fi

# Optionally load sample data if --with-sample-data flag is provided
if [[ "$*" == *--with-sample-data* ]]; then
  echo "Loading sample data..."
  ./scripts/load_sample_data.sh
fi
