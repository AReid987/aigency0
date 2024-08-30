#!/bin/bash

# Detect current operating system and install appropriate version of Ollama.

set -eu
status() { echo ">>> $#" >&2; }
error() {
	echo "ERROR $*"
	exit 1
}
warning() { echo "WARNING: $*"; }

TEMP_DIR=$(mktemp -d)
cleanup() { rm -rf "$TEMP_DIR"; }
trap cleanup EXIT

available() { command -v $1 >/dev/null; }

require() {
	local MISSING=''
	for TOOL in "$@"; do
		if ! available "$TOOL"; then
			MISSING="$MISSING $TOOL"
		fi
	done

	echo "$MISSING"
}
[ "$(uname -s)" = "Linux" ] || error 'This script is intended to run on Linux only.'

case "$(uname -m)" in
x86_64) ARCH="amd64" ;;
aarch64 | arm64) ARCH="arm64" ;;
*) error "Unsupported architecture: $ARCH" ;;
esac

SUDO=
if [ "$(id -u)" -ne 0 ]; then
	# Running as root, no need for sudo
	if ! available sudo; then
		error "This script requires superuser permissions. Please re-run as root."
	fi

	SUDO="sudo"
fi

NEEDS=$(require curl awk grep sed tee xargs)
if [ -n "$NEEDS" ]; then
	status "ERROR: The following tools are required but missing:"
	for NEED in $NEEDS; do
		echo "  - $NEED"
	done
	exit 1
fi

status "Downloading ollama..."
curl --fail --show-error --location --progress-bar -o "$TEMP_DIR"/ollama "https://ollama.ai/download/ollama-linux-$ARCH"

for BINDIR in /usr/local/bin /usr/bin /bin; do
	echo "$PATH" | grep -q $BINDIR && break || continue
done

status "Installing ollama to $BINDIR..."
$SUDO install -o0 -g0 -m755 -d "$BINDIR"
$SUDO install -o0 -g0 -m755 "$TEMP_DIR"/ollama "$BINDIR"/ollama

install_success() { status 'Install complete. Run "ollama" from the command line.'; }
trap install_success EXIT

# Everything from this point onwards is optional.

configure_systemd() {
	if ! id ollama >/dev/null 2>&1; then
		status "Creating ollama user..."
		$SUDO useradd -r -s /bin/false -m -d /usr/share/ollama ollama
	fi

	status "Creating ollama systemd service..."
	cat <<EOF | $SUDO tee /etc/systemd/system/ollama.service >/dev/null
[Unit]
Description=Ollama Service
After=network-online.target

[Service]
ExecStart=$BINDIR/ollama serve
User=ollama
Group=ollama
Restart=always
RestartSec=3
Environment="HOME=/usr/share/ollama"
Environment="PATH=$PATH"

[Install]
WantedBy=default.target
EOF
	SYSTEMCTL_RUNNING="$(systemctl is-system-running || true)"
	case $SYSTEMCTL_RUNNING in
	running | degraded)
		status "Enabling and starting ollama service..."
		$SUDO systemctl daemon-reload
		$SUDO systemctl enable ollama

		start_service() { $SUDO systemctl restart ollama; }
		trap start_service EXIT
		;;
	esac
}

if available systemctl; then
	configure_systemd
fi

if ! available lspci && ! available lshw; then
	warning "Unable to detect NVIDIA GPU. Install lspci or lshw to automatically detect and install NVIDIA CUDA drivers."
	exit 0
fi

check_gpu() {
	case $1 in
	lspci) available lspci && lspci -d '10de:' | grep -q 'NVIDIA' || return 1 ;;
	lshw) available lshw && $SUDO lshw -c display -numeric | grep -q 'vendor: .* \[10DE\]' || return 1 ;;
	nvidia-smi) available nvidia-smi || return 1 ;;
	esac
}

if check_gpu nvidia-smi; then
	status "NVIDIA GPU installed."
	exit 0
fi

if ! check_gpu lspci && ! check_gpu lshw; then
	warning "No NVIDIA GPU detected. Ollama will run in CPU-only mode."
	exit 0
fi
