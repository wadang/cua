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
ENV VNC_RESOLUTION=1024x768
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

# Install Firefox from Mozilla PPA (snap-free) - inline to avoid script issues
RUN apt-get update && \
    add-apt-repository -y ppa:mozillateam/ppa && \
    echo 'Package: *\nPin: release o=LP-PPA-mozillateam\nPin-Priority: 1001' > /etc/apt/preferences.d/mozilla-firefox && \
    apt-get update && \
    apt-get install -y firefox && \
    echo 'pref("datareporting.policy.firstRunURL", "");\npref("datareporting.policy.dataSubmissionEnabled", false);\npref("datareporting.healthreport.service.enabled", false);\npref("datareporting.healthreport.uploadEnabled", false);\npref("trailhead.firstrun.branches", "nofirstrun-empty");\npref("browser.aboutwelcome.enabled", false);' > /usr/lib/firefox/browser/defaults/preferences/firefox.js && \
    update-alternatives --install /usr/bin/x-www-browser x-www-browser /usr/bin/firefox 100 && \
    update-alternatives --install /usr/bin/gnome-www-browser gnome-www-browser /usr/bin/firefox 100 && \
    rm -rf /var/lib/apt/lists/*

# Install noVNC
RUN git clone https://github.com/novnc/noVNC.git /opt/noVNC && \
    git clone https://github.com/novnc/websockify /opt/noVNC/utils/websockify && \
    ln -s /opt/noVNC/vnc.html /opt/noVNC/index.html

# Pre-create cache directory with correct ownership before pip install
RUN mkdir -p /home/cua/.cache && \
    chown -R cua:cua /home/cua/.cache

# Install computer-server
RUN pip3 install cua-computer-server

# Fix any cache files created by pip
RUN chown -R cua:cua /home/cua/.cache

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
RUN mkdir -p $HOME/.config/xfce4/xfconf/xfce-perchannel-xml $HOME/.config/xfce4 $HOME/.config/autostart

# Copy XFCE config to disable browser launching and welcome screens
COPY --chown=cua:cua src/xfce-config/helpers.rc $HOME/.config/xfce4/helpers.rc
COPY --chown=cua:cua src/xfce-config/xfce4-session.xml $HOME/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-session.xml

# Disable panel plugins that might try to open browsers
RUN echo "[Desktop Entry]\nHidden=true" > $HOME/.config/autostart/xfce4-tips-autostart.desktop && \
    chown -R cua:cua $HOME/.config

# Create storage and shared directories, and Firefox cache directory
RUN mkdir -p $HOME/storage $HOME/shared $HOME/.cache/dconf $HOME/.mozilla/firefox && \
    chown -R cua:cua $HOME/storage $HOME/shared $HOME/.cache $HOME/.mozilla $HOME/.vnc

USER root

# Expose ports
EXPOSE $VNC_PORT $NOVNC_PORT $API_PORT

# Start services via supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]
