#!/bin/bash

set -e  # Exit immediately on any error

# -------------------------------
# Step 1: Install Python 3.12 (if not present)
# -------------------------------

# Installs Python 3.12 using deadsnakes PPA if it's not already available
install_python() {
  if ! command -v python3.12 &> /dev/null; then
    echo "Installing Python 3.12..."
    sudo apt update
    sudo apt install -y software-properties-common
    sudo add-apt-repository -y ppa:deadsnakes/ppa
    sudo apt update
    sudo apt install -y python3.12 python3.12-venv python3.12-distutils
  else
    echo "Python 3.12 already installed."
  fi
}

# -------------------------------
# Step 2: Install Docker & Docker Compose Plugin
# -------------------------------

# Installs Docker Engine, CLI, and Docker Compose plugin
install_docker() {
  echo "Installing Docker..."

  sudo apt update
  sudo apt install -y ca-certificates curl gnupg

  # Create keyrings directory for Docker GPG key
  sudo install -m 0755 -d /etc/apt/keyrings
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
    | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

  # Add Docker APT repository dynamically based on Ubuntu version
  UBUNTU_CODENAME=$(lsb_release -cs)
  echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
    https://download.docker.com/linux/ubuntu $UBUNTU_CODENAME stable" \
    | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

  echo "Installing Docker Engine, CLI, Buildx and Compose plugin..."
  sudo apt update
  sudo apt install -y \
      docker-ce \
      docker-ce-cli \
      containerd.io \
      docker-buildx-plugin \
      docker-compose-plugin

  echo "Docker installed."

  # Add current user to docker group (to run Docker without sudo)
  sudo usermod -aG docker "$USER"
  echo "You may need to log out and back in or run 'newgrp docker' for Docker group permissions."

  # Test Docker installation
  echo "Testing Docker..."
  sudo docker run hello-world
}

# -------------------------------
# Step 3: Install Poetry (for managing dependencies)
# -------------------------------

# Installs Python Poetry and disables virtualenv creation
install_poetry() {
  echo "Installing Poetry..."
  curl -sSL https://install.python-poetry.org | python3 -
  export PATH="$HOME/.local/bin:$PATH"

  # Prevent Poetry from creating its own virtual environment
  poetry config virtualenvs.create false
}

# -------------------------------
# Step 4: Setup pre-commit using Poetry or venv
# -------------------------------

# Installs and configures pre-commit using Poetry or virtual environment
setup_precommit() {
  if [ ! -f .pre-commit-config.yaml ]; then
    echo "No .pre-commit-config.yaml found. Skipping pre-commit setup."
    return
  fi

  echo "Setting up pre-commit..."

  USE_POETRY=true
  for arg in "$@"; do
    if [ "$arg" == "--use-venv" ]; then
      USE_POETRY=false
      break
    fi
  done

  if [ "$USE_POETRY" = true ] && command -v poetry &> /dev/null; then
    echo "Installing pre-commit with Poetry..."
    poetry add --group dev pre-commit ruff
    poetry run pre-commit install
    echo "Pre-commit installed and configured with Poetry."
  else
    echo "Setting up pre-commit with virtual environment..."

    if [ -z "$VIRTUAL_ENV" ]; then
      if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3.12 -m venv venv
      fi
      echo "Activating virtual environment..."
      source venv/bin/activate
    fi

    pip install --upgrade pip
    pip install pre-commit ruff
    pre-commit install
    echo "Pre-commit installed and configured with virtual environment."
  fi
}

# -------------------------------
# Step 5: Install Python Dependencies
# -------------------------------

# Installs dependencies using Poetry or pip depending on flag
install_dependencies() {
  USE_POETRY=true
  for arg in "$@"; do
    if [ "$arg" == "--use-venv" ]; then
      USE_POETRY=false
      break
    fi
  done

  if [ "$USE_POETRY" = true ] && [ -f pyproject.toml ]; then
    echo "Installing dependencies with Poetry..."
    poetry install
  else
    echo "Installing dependencies with pip..."

    if [ -z "$VIRTUAL_ENV" ]; then
      if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3.12 -m venv venv
      fi
      echo "Activating virtual environment..."
      source venv/bin/activate
    fi

    if [ -f requirements_dev.txt ]; then
      echo "Installing dependencies from requirements_dev.txt..."
      pip install --upgrade pip
      pip install -r requirements_dev.txt
    elif [ -f requirements.txt ]; then
      echo "Installing dependencies from requirements.txt..."
      pip install --upgrade pip
      pip install -r requirements.txt
    else
      echo "No requirements files found."
    fi
  fi
}

# -------------------------------
# Step 6: Run Django Migrations in Docker
# -------------------------------

# Builds Docker image and runs Django migrations inside container
run_migrations() {
  if [ -f docker-compose.yml ]; then
    echo "Building Docker image..."
    docker compose build

    echo "Running Django migrations inside Docker container..."
    docker compose run --rm --workdir /app/src web python manage.py makemigrations
    docker compose run --rm --workdir /app/src web python manage.py migrate

    echo "Collecting static files inside Docker container..."
    docker compose run --rm --workdir /app/src web python manage.py collectstatic --noinput
  else
    echo "docker-compose.yml not found. Cannot run migrations or collect static files inside Docker."
    exit 1
  fi
}

# -------------------------------
# Step 7: Install Yarn for Frontend
# -------------------------------

install_yarn() {
  FRONTEND_DIR="$(dirname "$0")/../frontend"  # Get the absolute path to the frontend directory
  FRONTEND_DIR="$(realpath "$FRONTEND_DIR")"  # Resolve the absolute path

  if [ -d "$FRONTEND_DIR" ]; then
    echo "Navigating to frontend directory: $FRONTEND_DIR"
    cd "$FRONTEND_DIR" || { echo "Failed to navigate to frontend directory. Skipping Yarn installation."; return; }

    echo "Installing Yarn package manager..."
    curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
    echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
    sudo apt update
    sudo apt install yarn -y
    echo "Yarn installation completed."

    echo "Installing frontend dependencies..."
    yarn install
    echo "Frontend dependencies installed."
  else
    echo "Frontend directory not found at $FRONTEND_DIR. Skipping Yarn installation."
  fi
}

# -------------------------------
# Main Execution
# -------------------------------

# Orchestrates the setup process for local development
main() {
  echo "Starting development environment setup..."

  install_python
  install_docker
  install_poetry
  install_dependencies "$@"
  setup_precommit "$@"
  install_yarn
  run_migrations

  echo "Setup complete!"
  echo ""
  echo "Pre-commit is now configured to run automatically before each commit."
  echo "To manually run pre-commit on all files: pre-commit run --all-files"
  echo ""
  echo "If using Docker group permissions, you may need to:"
  echo "  - Log out and back in, or"
  echo "  - Run 'newgrp docker' to apply group changes"
}

# Run main function with script arguments
main "$@"
