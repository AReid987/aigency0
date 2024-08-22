# Use Python 3.12 slim as the base image
FROM python:3.12-slim AS base

# Install system dependencies
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    curl jq \
    build-essential \
    git libportaudio2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create and activate virtual environment
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Install additional dependencies for Ollama support
RUN pip install --no-cache-dir requests websockets

# Copy the start script
COPY start_aider.sh /start_aider.sh
RUN chmod +x /start_aider.sh

# Copy initialization script
COPY init_ollama.sh /init_ollama.sh
RUN chmod +x /init_ollama.sh

# Set environment variable for Ollama
ENV OLLAMA_BASE_URL="http://ollama:11434"

# Permission kludges to support `docker run --user xxx`
RUN chmod a+rwx /venv /venv/bin /venv/include /venv/lib /venv/lib/python3.12/site-packages

RUN mkdir /.aider /.cache
RUN chmod a+rwx /.aider /.cache

# So git doesn't complain about unusual permissions
RUN git config --system --add safe.directory /app

#########################
FROM base AS aider-full

ENV AIDER_DOCKER_IMAGE=paulgauthier/aider-full

COPY . /tmp/aider
RUN /venv/bin/python -m pip install --upgrade --no-cache-dir pip \
    && /venv/bin/python -m pip install --no-cache-dir /tmp/aider[help,browser,playwright] \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    && /venv/bin/python -m pip install --no-cache-dir aider-chat[help,browser,playwright] \
    && rm -rf /tmp/aider

RUN find /venv/lib/python3.12/site-packages \( -type d -exec chmod a+rwx {} + \) -o \( -type f -exec chmod a+rw {} + \)
RUN playwright install --with-deps chromium

# Set the entrypoint to run Aider without requiring terminal input
ENTRYPOINT ["/venv/bin/aider"]

#########################
FROM base AS aider

ENV AIDER_DOCKER_IMAGE=paulgauthier/aider-full

COPY . /tmp/aider
RUN /venv/bin/python -m pip install --upgrade --no-cache-dir pip \
    && /venv/bin/python -m pip install --no-cache-dir /tmp/aider \
    --extra-index-url https://download.pytorch.org/whl/cpu \
    && /venv/bin/python -m pip install --no-cache-dir aider-chat[browser] \
    && rm -rf /tmp/aider

RUN find /venv/lib/python3.12/site-packages \( -type d -exec chmod a+rwx {} + \) -o \( -type f -exec chmod a+rw {} + \)

# Copy the update script
COPY update_aider.sh /update_aider.sh
COPY start_aider.sh /start_aider.sh
# RUN chmod +x /update_aider.sh /start_aider.sh

EXPOSE 8501

# Set the entrypoint to the start script
ENTRYPOINT ["/start_aider.sh"]
# # Set the entrypoint to run Aider without requiring terminal input
# ENTRYPOINT ["/venv/bin/aider", "--gui"]