# Docker Guestbook

A simple multi-container guestbook web app I built with **Flask** and **Redis** db. Containerized with **Docker** and orchestrated with **Docker Compose**. 
Users can sign the guestbook, with the messages stored via Redis.

## Features
- Live page-visit counter
- Sign the guestbook with your name and a message
- Shows which container served the request
- Persistent storage

| Service | Image | Role |
|---|---|---|
| `web` | Built from `Dockerfile` | Flask app serving the guestbook page |
| `redis` | `redis:7-alpine` (official) | Stores messages and visit counter |

- The two containers talk over a private network that Docker Compose creates. The app reaches the database at the hostname `redis` (the service name).
- Redis data is stored in a named volume (`redis-data`) with append-only persistence enabled, so it survives `docker compose down`.

## Usage

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### Run
```bash
git clone https://github.com/YOUR-USERNAME/docker-guestbook.git
cd docker-guestbook
docker compose up -d --build
```

Then open **http://localhost:8000** and sign the guestbook.

### Stop container
```bash
docker compose down # stop and remove container
docker compose down -v # deletes the volume too
```

## Inspect container
```bash
docker compose ps # see running services
docker compose logs -f web # view logs
docker compose exec redis redis-cli LRANGE messages 0 -1 # view stored messages
docker compose exec redis redis-cli GET visits # view visit count
```

## Common Docker Commands

### Images

| Command | What it does |
|---|---|
| `docker build -t <image_name> .` | Build an image from the Dockerfile in the current folder and names it ‘image_name’ |
| `docker images` | List all images on the machine |
| `docker pull <image>` | Downloads an image from Docker Hub without running it. |
| `docker rmi <image_name>` | Deletes an image. Any containers using it must be removed first. |
| `docker push <image_name>` | Uploads an image to Docker registry on Docker Hub |

### Running Containers

| Command | What it does |
|---|---|
| `docker run <image_name>` | Creates and starts a container from an image |
| `docker run -d …` | Runs detached in the background |
| `docker run -p <LOCAL PORT: CONTAINER PORT>` | Maps port ‘LOCAL PORT’ to ‘CONTAINER PORT’ in the container. |
| `docker run --name <container_name>` | Names the container. |
| `docker run --rm …` | Automatically deletes the container when it stops. |
| `docker run -e KEY=value ...` | Pass in an ENV into the container. |
| `docker run -v ~/folder:/app …` | Mounts a folder from your Mac into the container |

### Managing Containers

| Command | What it does |
|---|---|
| `docker ps` | Lists running containers |
| `docker ps -a` | Lists all containers including stopped ones |
| `docker stop <container_name>` | Stops a running container |
| `docker start <container_name>` | Starts a stopped container again. |
| `docker restart <container_name>` | Stops and starts a container. |
| `docker rm <container_name>` | Deletes a stopped container |
| `docker rm -f <container_name>` | Stop and delete a container (force). |

### Logs and Debugging

| Command | What it does |
|---|---|
| `docker logs <container_name>` | Shows a container’s output |
| `docker logs -f <container_name>` | Follows the logs live. |
| `docker exec <container_name> <some_command>` | Run a one-off command inside of a running container. |
| `docker exec -it <container_name> bash` | Opens a shell inside a running container. |
| `docker inspect <container_name>` | Shows important details such as ports, IP, mounts, etc… |
| `docker stats` | Live CPU and memory usage of running containers |

### Cleanup

| Command | What it does |
|---|---|
| `docker container prune` | Deletes all stopped containers |
| `docker image prune` | Deletes unused, untagged images |
| `docker system prune` | Deletes stopped containers, unused networks, dangling images, and build cache |
| `docker system df` | Shows how much disk space Docker is using up. |

### Docker Compose

| Command | What it does |
|---|---|
| `docker compose up -d` | Builds (if needed) and starts every container defined in compose.yaml |
| `docker compose up -d --build` | Same, but forces a rebuild first, which is useful after code changes |
| `docker compose ps` | Lists the containers in this project |
| `docker compose logs -f` | Follows logs from all the project’s containers |
| `docker compose down` | Stops and removes the project’s containers and network |
| `docker compose down -v` | Same, and also deletes the project’s stored data (volumes) |
