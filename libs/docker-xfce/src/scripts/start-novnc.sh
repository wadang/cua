#!/bin/bash
set -e

# Wait for VNC server to be ready
echo "Waiting for VNC server to start..."
while ! nc -z localhost ${VNC_PORT:-5901}; do
    sleep 1
done
echo "VNC server is ready"

# Start noVNC
cd /opt/noVNC
/opt/noVNC/utils/novnc_proxy \
    --vnc localhost:${VNC_PORT:-5901} \
    --listen ${NOVNC_PORT:-6901}
