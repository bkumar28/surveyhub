#  Docker Setup Guide for Django Projects

This guide provides a comprehensive list of Docker and Docker Compose commands needed to set up and manage a Django project in a containerized environment.

---
##  Build and Run Containers

### Build the containers (no cache)
```bash
docker compose build --no-cache
```

### Build normally
```bash
docker compose build
```

### Run containers in detached mode
```bash
docker compose up -d
```

### Run containers in foreground
```bash
docker compose up
```

### View logs
```bash
docker compose logs
docker compose logs -f  # Follow logs
docker compose logs backend  # Logs for a specific service
```

### Stop containers
```bash
docker compose down
```

### Stop containers and remove volumes
```bash
docker compose down -v
```

### Restart containers
```bash
docker compose restart
```

---

##  Useful Docker Commands

### List containers
```bash
docker ps
```

### List all containers (including stopped)
```bash
docker ps -a
```

### List images
```bash
docker images
```

### Remove all stopped containers
```bash
docker container prune
```

### Remove all unused images
```bash
docker image prune -a
```

---

##  File to keep in project root

- `.dockerignore`
- `.gitignore`
- `Dockerfile`
- `docker-compose.yml`
- `.env` (should not be committed)
- `.env.example`

---

##  Run Django commands inside container

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py collectstatic --noinput
```
##  Login to a Running Container
```bash
docker exec -it <container_name_or_id> bash
```

---

##  Install Python Dependencies

```bash
docker compose exec web poetry install
```

---
