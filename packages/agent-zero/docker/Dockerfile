# # Use a specific version of Debian Slim
# FROM debian:bullseye-slim

# # Install system dependencies
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     python3 \
#     python3-pip \
#     python3-venv \
#     git \
#     nodejs \
#     npm \
#     openssh-server \
#     sudo \
#     curl \
#     && rm -rf /var/lib/apt/lists/*

# # Create a non-root user with sudo privileges
# RUN useradd -m -s /bin/bash agentuser && \
#     echo "agentuser:agentpassword" | chpasswd && \
#     echo "agentuser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# # Set up SSH
# RUN mkdir /var/run/sshd && \
#     sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config && \
#     ssh-keygen -A

# # Create and activate Python virtual environment
# ENV VIRTUAL_ENV=/opt/venv
# RUN python3 -m venv $VIRTUAL_ENV
# ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# # Install Agent Zero dependencies
# RUN pip install --no-cache-dir \
#     langchain \
#     requests \
#     websockets

# # Copy initialize.sh and .bashrc
# COPY initialize.sh /home/agentuser/initialize.sh
# COPY .bashrc /home/agentuser/.bashrc

# # Set correct permissions
# RUN chown agentuser:agentuser /home/agentuser/initialize.sh /home/agentuser/.bashrc && \
#     chmod +x /home/agentuser/initialize.sh && \
#     chmod 644 /home/agentuser/.bashrc

# # Set up Ollama environment variable
# ENV OLLAMA_BASE_URL="http://ollama:11434"

# # Expose SSH and Agent Zero ports
# EXPOSE 22 5001

# # Switch to non-root user
# USER agentuser

# # Set the working directory
# WORKDIR /home/agentuser/work_dir

# # Start SSH server and run initialize.sh
# CMD sudo /usr/sbin/sshd && /home/agentuser/initialize.sh

# Original Dockerfile. Optimized image above
# Use the latest slim version of Debian
FROM --platform=$TARGETPLATFORM debian:bookworm-slim

# Set ARG for platform-specific commands
ARG TARGETPLATFORM

# Update and install necessary packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    nodejs \
    npm \
    openssh-server \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Set up SSH
RUN mkdir /var/run/sshd && \
    echo 'root:toor' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Create and activate Python virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV

# Copy initial .bashrc with virtual environment activation to a temporary location
COPY ./.bashrc /etc/skel/.bashrc

# Copy the script to ensure .bashrc is in the root directory
COPY ./initialize.sh /usr/local/bin/initialize.sh
RUN chmod +x /usr/local/bin/initialize.sh

# Ensure the virtual environment and pip setup
RUN $VIRTUAL_ENV/bin/pip install --upgrade pip

# Expose SSH port
EXPOSE 22

# Init .bashrc
CMD ["/usr/local/bin/initialize.sh"]