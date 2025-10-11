# CUA Docker XFCE Container
# Vanilla XFCE desktop with noVNC and computer-server

FROM ubuntu:22.04

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Set environment variables
ENV HOME=/home/cua
ENV DISPLAY=:1
ENV VNC_PORT=5901
ENV NOVNC_PORT=6901
ENV API_PORT=8000
ENV VNC_RESOLUTION=1920x1080
ENV VNC_COL_DEPTH=24

# Create user
RUN useradd -m -s /bin/bash -G sudo cua && \
    echo "cua:password" | chpasswd && \
    echo "cua ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # Desktop environment
    xfce4 \
    xfce4-terminal \
    xfce4-goodies \
    dbus-x11 \
    # VNC server
    tigervnc-standalone-server \
    tigervnc-common \
    # noVNC dependencies
    python3 \
    python3-pip \
    python3-numpy \
    git \
    net-tools \
    netcat \
    supervisor \
    # Computer-server dependencies
    python3-tk \
    python3-dev \
    gnome-screenshot \
    wmctrl \
    ffmpeg \
    socat \
    xclip \
    # Browser
    wget \
    software-properties-common \
    # Build tools
    build-essential \
    libncursesw5-dev \
    libssl-dev \
    libsqlite3-dev \
    tk-dev \
    libgdbm-dev \
    libc6-dev \
    libbz2-dev \
    libffi-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Remove power manager to avoid popup in container
RUN apt-get remove -y xfce4-power-manager xfce4-power-manager-data || true

# Install noVNC
RUN git clone https://github.com/novnc/noVNC.git /opt/noVNC && \
    git clone https://github.com/novnc/websockify /opt/noVNC/utils/websockify && \
    ln -s /opt/noVNC/vnc.html /opt/noVNC/index.html

# Install computer-server
RUN pip3 install cua-computer-server

# Install Firefox
RUN add-apt-repository -y ppa:mozillateam/ppa && \
    echo 'Package: *\nPin: release o=LP-PPA-mozillateam\nPin-Priority: 1001' > /etc/apt/preferences.d/mozilla-firefox && \
    apt-get update && \
    apt-get install -y firefox && \
    rm -rf /var/lib/apt/lists/*

# Configure Firefox defaults
RUN mkdir -p /etc/firefox && \
    echo 'pref("datareporting.policy.firstRunURL", "");' > /etc/firefox/syspref.js && \
    echo 'pref("datareporting.policy.dataSubmissionEnabled", false);' >> /etc/firefox/syspref.js && \
    echo 'pref("datareporting.healthreport.service.enabled", false);' >> /etc/firefox/syspref.js && \
    echo 'pref("datareporting.healthreport.uploadEnabled", false);' >> /etc/firefox/syspref.js && \
    echo 'pref("browser.aboutwelcome.enabled", false);' >> /etc/firefox/syspref.js

# Copy startup scripts
COPY src/supervisor/ /etc/supervisor/conf.d/
COPY src/scripts/ /usr/local/bin/

# Make scripts executable
RUN chmod +x /usr/local/bin/*.sh

# Setup VNC
USER cua
WORKDIR /home/cua

# Create VNC password file
RUN mkdir -p $HOME/.vnc && \
    echo "password" | vncpasswd -f > $HOME/.vnc/passwd && \
    chmod 600 $HOME/.vnc/passwd

# Configure XFCE for first start
RUN mkdir -p $HOME/.config/xfce4/xfconf/xfce-perchannel-xml

# Create storage and shared directories
RUN mkdir -p $HOME/storage $HOME/shared

USER root

# Expose ports
EXPOSE $VNC_PORT $NOVNC_PORT $API_PORT

# Start services via supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]
