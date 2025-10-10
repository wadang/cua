.PHONY: build run stop push clean test logs shell

IMAGE_NAME := trycua/cua-docker-xfce
TAG := latest
CONTAINER_NAME := cua-docker-xfce-test

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME):$(TAG) .

# Run the container
run:
	docker run -d \
		--name $(CONTAINER_NAME) \
		--shm-size=512m \
		-p 5901:5901 \
		-p 6901:6901 \
		-p 8000:8000 \
		$(IMAGE_NAME):$(TAG)
	@echo "Container started!"
	@echo "noVNC: http://localhost:6901"
	@echo "VNC: localhost:5901 (password: password)"
	@echo "API: http://localhost:8000"

# Run with custom resolution
run-hd:
	docker run -d \
		--name $(CONTAINER_NAME) \
		--shm-size=512m \
		-p 5901:5901 \
		-p 6901:6901 \
		-p 8000:8000 \
		-e VNC_RESOLUTION=1280x720 \
		$(IMAGE_NAME):$(TAG)

# Run with persistent storage
run-persist:
	mkdir -p ./storage ./shared
	docker run -d \
		--name $(CONTAINER_NAME) \
		--shm-size=512m \
		-p 5901:5901 \
		-p 6901:6901 \
		-p 8000:8000 \
		-v $(PWD)/storage:/home/cua/storage \
		-v $(PWD)/shared:/home/cua/shared \
		$(IMAGE_NAME):$(TAG)

# Stop and remove the container
stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

# Push to Docker Hub
push:
	docker push $(IMAGE_NAME):$(TAG)

# Clean up everything
clean: stop
	docker rmi $(IMAGE_NAME):$(TAG) || true
	rm -rf ./storage ./shared

# Run tests
test: build run
	@echo "Waiting for services to start..."
	@sleep 10
	@echo "Testing noVNC..."
	@curl -f http://localhost:6901 > /dev/null && echo "✓ noVNC is running" || echo "✗ noVNC failed"
	@echo "Testing API..."
	@curl -f http://localhost:8000 > /dev/null && echo "✓ API is running" || echo "✗ API failed"
	@$(MAKE) stop

# View logs
logs:
	docker logs -f $(CONTAINER_NAME)

# View supervisor logs
logs-supervisor:
	docker exec $(CONTAINER_NAME) tail -f /var/log/supervisor/supervisord.log

# View individual service logs
logs-vnc:
	docker exec $(CONTAINER_NAME) tail -f /var/log/supervisor/vncserver.log

logs-novnc:
	docker exec $(CONTAINER_NAME) tail -f /var/log/supervisor/novnc.log

logs-api:
	docker exec $(CONTAINER_NAME) tail -f /var/log/supervisor/computer-server.log

# Open a shell in the container
shell:
	docker exec -it $(CONTAINER_NAME) /bin/bash

# Check supervisor status
status:
	docker exec $(CONTAINER_NAME) supervisorctl status

# Restart services
restart-services:
	docker exec $(CONTAINER_NAME) supervisorctl restart all

# Create a snapshot
snapshot:
	docker commit $(CONTAINER_NAME) $(IMAGE_NAME):snapshot
	@echo "Snapshot created: $(IMAGE_NAME):snapshot"

# Build and run
dev: build run logs

# Help
help:
	@echo "Available targets:"
	@echo "  build         - Build the Docker image"
	@echo "  run           - Run the container"
	@echo "  run-hd        - Run with 720p resolution"
	@echo "  run-persist   - Run with persistent storage"
	@echo "  stop          - Stop and remove container"
	@echo "  push          - Push to Docker Hub"
	@echo "  clean         - Remove image and container"
	@echo "  test          - Build, run tests, and stop"
	@echo "  logs          - View container logs"
	@echo "  logs-*        - View specific service logs"
	@echo "  shell         - Open shell in container"
	@echo "  status        - Check supervisor status"
	@echo "  snapshot      - Create container snapshot"
	@echo "  dev           - Build, run, and follow logs"
