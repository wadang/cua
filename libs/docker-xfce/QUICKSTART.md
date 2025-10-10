# Quick Start Guide

Get up and running with CUA Docker XFCE in 5 minutes.

## Prerequisites

- Docker installed and running
- Python 3.11+ (for using with CUA library)
- `cua-computer` package installed: `pip install cua-computer`

## Quick Start

### Option 1: Using Makefile (Recommended)

```bash
# Build and run
make build
make run

# Check if it's running
make status

# View logs
make logs
```

Access:
- 🌐 **Web VNC**: http://localhost:6901
- 🖥️ **VNC Client**: localhost:5901 (password: `password`)
- 🔌 **API**: http://localhost:8000

### Option 2: Using Docker Compose

```bash
# Start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

### Option 3: Docker Command

```bash
docker run -d \
  --name cua-desktop \
  --shm-size=512m \
  -p 5901:5901 \
  -p 6901:6901 \
  -p 8000:8000 \
  trycua/cua-docker-xfce:latest
```

## Using with Python

```python
import asyncio
from computer import Computer

async def main():
    computer = Computer(
        os_type="linux",
        provider_type="docker",
        image="trycua/cua-docker-xfce:latest"
    )

    async with computer:
        # Take a screenshot
        screenshot = await computer.interface.screenshot()

        # Open terminal
        await computer.interface.hotkey("ctrl", "alt", "t")
        await asyncio.sleep(1)

        # Type and execute command
        await computer.interface.type_text("echo 'Hello!'")
        await computer.interface.press_key("Return")

asyncio.run(main())
```

## Common Tasks

### Run with custom resolution
```bash
make run-hd  # 1280x720
# or
docker run -e VNC_RESOLUTION=1280x720 ...
```

### Run with persistent storage
```bash
make run-persist
# or
docker run -v $(pwd)/storage:/home/cua/storage ...
```

### View specific logs
```bash
make logs-vnc       # VNC server logs
make logs-novnc     # noVNC proxy logs
make logs-api       # Computer-server logs
```

### Open shell in container
```bash
make shell
# or
docker exec -it cua-desktop /bin/bash
```

### Create a snapshot
```bash
make snapshot
```

## Troubleshooting

### Container won't start
```bash
# Check if ports are already in use
lsof -i :6901
lsof -i :8000

# View container logs
docker logs cua-desktop
```

### Black screen in noVNC
```bash
# Restart VNC server
docker exec cua-desktop supervisorctl restart vncserver
```

### API not responding
```bash
# Check if computer-server is running
docker exec cua-desktop supervisorctl status computer-server

# Restart computer-server
docker exec cua-desktop supervisorctl restart computer-server
```

## Next Steps

- Read the [full README](README.md) for detailed documentation
- Check out [example.py](example.py) for more usage examples
- Customize the [Dockerfile](Dockerfile) for your needs

## Clean Up

```bash
# Using Makefile
make clean

# Using docker-compose
docker-compose down -v

# Manual
docker stop cua-desktop
docker rm cua-desktop
docker rmi trycua/cua-docker-xfce:latest
```
