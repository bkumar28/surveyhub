#!/bin/bash
# -----------------------------------------------------------------------------
# Script: docker_setup.sh
#
# Description:
#   A comprehensive Docker setup script for SurveyHub project
#   Handles building, starting, stopping, and managing Docker containers
#
# Usage:
#   ./docker_setup.sh build                 # Build containers
#   ./docker_setup.sh up                    # Start containers
#   ./docker_setup.sh down                  # Stop containers
#   ./docker_setup.sh restart               # Restart containers
#   ./docker_setup.sh logs                  # View container logs
#   ./docker_setup.sh status                # Check container status
#   ./docker_setup.sh clean                 # Clean up containers and volumes
# -----------------------------------------------------------------------------

set -e

# Configuration
COMPOSE_FILE="docker-compose.yml"


# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
}

# Function to build Docker containers
build_containers() {
    print_status "Building Docker containers..."
    docker compose -f "$COMPOSE_FILE" build
    print_success "Docker containers built successfully"
}

# Function to start containers
start_containers() {
    print_status "Starting Docker containers..."
    docker compose -f "$COMPOSE_FILE" up -d

    print_status "Waiting for containers to be ready..."
    sleep 10

    # Check if containers are running
    if docker compose ps | grep -q "running"; then
        print_success "Containers started successfully"
        print_status "Application will be available at:"
        echo "  - API Documentation: http://localhost:8000/api/schema/swagger-ui/"
        echo "  - Admin Interface: http://localhost:8000/admin/"
    else
        print_error "Failed to start containers properly"
        exit 1
    fi
}

# Function to stop containers
stop_containers() {
    print_status "Stopping Docker containers..."
    docker compose -f "$COMPOSE_FILE" down
    print_success "Containers stopped successfully"
}

# Function to restart containers
restart_containers() {
    print_status "Restarting Docker containers..."
    stop_containers
    start_containers
}

# Function to view logs
view_logs() {
    print_status "Viewing container logs..."
    docker compose -f "$COMPOSE_FILE" logs -f
}

# Function to check container status
check_status() {
    print_status "Container Status:"
    docker compose -f "$COMPOSE_FILE" ps

    print_status "Container Health:"
    docker compose -f "$COMPOSE_FILE" top
}

# Function to clean up containers and volumes
clean_containers() {
    print_warning "This will remove all containers, networks, and volumes!"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Cleaning up containers and volumes..."
        docker compose -f "$COMPOSE_FILE" down -v --remove-orphans
        docker system prune -f
        print_success "Cleanup completed"
    else
        print_status "Cleanup cancelled"
    fi
}

# Function to run full setup
full_setup() {
    print_status "Starting full Docker setup..."

    # Build containers
    build_containers

    # Start containers
    start_containers

    # Wait a bit more for services to be fully ready
    print_status "Waiting for services to be fully ready..."
    sleep 15

    # Load sample data
    print_status "Loading sample data..."
    if [ -f "./scripts/load_sample_data.sh" ]; then
        ./scripts/load_sample_data.sh
        print_success "Sample data loaded successfully"
    else
        print_warning "Sample data script not found, skipping..."
    fi

    print_success "Full setup completed successfully!"
    print_status "Your application is ready at:"
    echo "  - API Documentation: http://localhost:8000/api/schema/swagger-ui/"
    echo "  - Admin Interface: http://localhost:8000/admin/"
}

# Function to show help
show_help() {
    echo "Usage: $0 <command>"
    echo ""
    echo "Available commands:"
    echo "  build        Build Docker containers"
    echo "  up           Start containers in detached mode"
    echo "  down         Stop and remove containers"
    echo "  restart      Restart containers"
    echo "  logs         View container logs"
    echo "  status       Check container status"
    echo "  clean        Clean up containers and volumes"
    echo "  help         Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 build"
    echo "  $0 up"
    echo ""
}

# Main execution
main() {
    # Check if Docker is running
    check_docker

    # Parse command
    case "${1:-help}" in
        build)
            build_containers
            ;;
        up)
            start_containers
            ;;
        down)
            stop_containers
            ;;
        restart)
            restart_containers
            ;;
        logs)
            view_logs
            ;;
        status)
            check_status
            ;;
        clean)
            clean_containers
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
