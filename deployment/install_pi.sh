#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# VeriMath — Automated Raspberry Pi 4 / 5 Installation Script
# ─────────────────────────────────────────────────────────────────────────────
# Sets up the entire VeriMath runtime on Raspberry Pi OS (64-bit Bookworm/Trixie):
#   1. 64-bit OS & hardware check + system packages (OCR, camera, MQTT, Node)
#   2. Mosquitto MQTT broker configuration
#   3. Lean 4 (elan) + Mathlib prebuilt .olean cache (`lake exe cache get`)
#   4. Python virtual environment + dependencies (safe RAM limits for Pi)
#   5. Local Qwen2.5 GGUF model download (1.5B default, or --3b for 8GB Pi)
#   6. React frontend production build
#   7. Portable .env configuration (VERIMATH_STRICT_LEAN=true)
#   8. Templated systemd service registration for the current user & repo path
#
# Usage:
#   bash deployment/install_pi.sh          # Default (Qwen2.5-1.5B Q4_K_M)
#   bash deployment/install_pi.sh --3b     # Recommended for 8 GB Pi 4 / Pi 5
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

USE_3B=false
SKIP_MODEL=false
SKIP_SYSTEMD=false
for arg in "$@"; do
    case "$arg" in
        --3b) USE_3B=true ;;
        --skip-model) SKIP_MODEL=true ;;
        --skip-systemd) SKIP_SYSTEMD=true ;;
    esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKDIR="$(cd "$SCRIPT_DIR/.." && pwd)"
TARGET_USER="${SUDO_USER:-$(id -un)}"
TARGET_HOME="$(getent passwd "$TARGET_USER" 2>/dev/null | cut -d: -f6 || echo "$HOME")"
cd "$WORKDIR"

echo "=========================================================="
echo "  VeriMath — Raspberry Pi Automated Deployment"
echo "  Repo Dir : $WORKDIR"
echo "  Run User : $TARGET_USER ($TARGET_HOME)"
echo "=========================================================="

ARCH="$(uname -m)"
if [ "$ARCH" != "aarch64" ] && [ "$ARCH" != "x86_64" ]; then
    echo "ERROR: Detected $ARCH (32-bit). VeriMath requires 64-bit Raspberry Pi OS (aarch64)."
    echo "Please flash Raspberry Pi OS (64-bit) using Raspberry Pi Imager and retry."
    exit 1
fi

# Step 1: System packages
echo ""
echo "[1/8] Updating package lists and installing dependencies..."
sudo apt-get update
sudo apt-get install -y \
    curl git python3-pip python3-venv python3-dev \
    mosquitto mosquitto-clients nodejs npm \
    build-essential cmake pkg-config \
    tesseract-ocr fswebcam v4l-utils

# Install Raspberry Pi CSI camera tools (package name varies by OS release)
if apt-cache show rpicam-apps >/dev/null 2>&1; then
    sudo apt-get install -y rpicam-apps || true
elif apt-cache show libcamera-apps >/dev/null 2>&1; then
    sudo apt-get install -y libcamera-apps || true
fi

# Grant camera device access (/dev/video* and CSI) to service user
if getent group video >/dev/null 2>&1; then
    sudo usermod -aG video "$TARGET_USER" || true
fi

# Step 2: Mosquitto configuration
echo ""
echo "[2/8] Configuring Mosquitto MQTT broker..."
sudo cp "$WORKDIR/deployment/mosquitto.conf" /etc/mosquitto/conf.d/verimath.conf
sudo systemctl restart mosquitto
sudo systemctl enable mosquitto

# Step 3: Lean 4 installation via elan + Mathlib cache
echo ""
echo "[3/8] Setting up Lean 4 & Mathlib..."
export PATH="$TARGET_HOME/.elan/bin:$PATH"
if ! command -v elan >/dev/null 2>&1; then
    echo "Installing elan (Lean 4 version manager)..."
    curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh -s -- -y
    export PATH="$TARGET_HOME/.elan/bin:$PATH"
fi

if [ -d "$WORKDIR/lean/VeriMath" ]; then
    pushd "$WORKDIR/lean/VeriMath" >/dev/null
    elan toolchain install "$(cat lean-toolchain | tr -d '[:space:]')" || true
    if [ ! -d ".lake/packages/mathlib/.lake/build/lib/lean" ]; then
        echo "Fetching prebuilt Mathlib .olean cache (avoids hours of compilation on Pi)..."
        lake exe cache get || echo "Note: lake exe cache get skipped/partial; run 'lake exe cache get' if offline."
    fi
    lake build VeriMath || true
    popd >/dev/null
fi
echo "Lean version: $(lean --version 2>/dev/null || echo 'installed in ~/.elan/bin')"

# Step 4: Python Virtual Environment
echo ""
echo "[4/8] Setting up Python virtual environment..."
if [ ! -d "$WORKDIR/.venv" ]; then
    python3 -m venv "$WORKDIR/.venv"
fi
# shellcheck disable=SC1091
source "$WORKDIR/.venv/bin/activate"
pip install --upgrade pip setuptools wheel
# Limit parallel C++ jobs to avoid OOM when compiling llama-cpp-python on 4 GB Pi
export CMAKE_BUILD_PARALLEL_LEVEL="${CMAKE_BUILD_PARALLEL_LEVEL:-2}"
export MAKEFLAGS="${MAKEFLAGS:--j2}"
pip install -r "$WORKDIR/requirements.txt"

# Step 5: Environment Setup
echo ""
echo "[5/8] Configuring .env for Raspberry Pi..."
if [ ! -f "$WORKDIR/.env" ]; then
    cp "$WORKDIR/.env.example" "$WORKDIR/.env"
fi

python3 - "$WORKDIR/.env" "$WORKDIR" "$TARGET_HOME" <<'PYEOF'
import sys
from pathlib import Path

env_path = Path(sys.argv[1])
workdir = sys.argv[2]
home_dir = sys.argv[3]
lines = env_path.read_text(encoding="utf-8").splitlines()
updates = {
    "LEAN_BINARY_PATH": f"{home_dir}/.elan/bin/lean",
    "LEAN_PROJECT_PATH": f"{workdir}/lean/VeriMath",
    "DEMO_CACHE_PATH": f"{workdir}/demo_cache.db",
    "VERIMATH_STRICT_LEAN": "true",
    "LEAN_TIMEOUT_SECONDS": "45",
}
seen = set()
new_lines = []
for line in lines:
    stripped = line.strip()
    if stripped and not stripped.startswith("#") and "=" in line:
        k = line.split("=", 1)[0].strip()
        if k in updates:
            new_lines.append(f"{k}={updates[k]}")
            seen.add(k)
            continue
    new_lines.append(line)
for k, v in updates.items():
    if k not in seen:
        new_lines.append(f"{k}={v}")
env_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
PYEOF

# Step 6: Download Qwen2.5 Model
echo ""
echo "[6/8] Downloading local GGUF model..."
if [ "$SKIP_MODEL" = true ]; then
    echo "Skipping model download (--skip-model)."
else
    if [ "$USE_3B" = true ]; then
        "$WORKDIR/.venv/bin/python" "$WORKDIR/scripts/download_model.py" --3b
    else
        "$WORKDIR/.venv/bin/python" "$WORKDIR/scripts/download_model.py"
    fi
fi

# Step 7: Frontend Build
echo ""
echo "[7/8] Building React frontend..."
pushd "$WORKDIR/frontend" >/dev/null
npm install
npm run build
sudo npm install -g serve || true
popd >/dev/null
SERVE_BIN="$(command -v serve || echo '/usr/local/bin/serve')"

# Step 8: Systemd service registration
echo ""
echo "[8/8] Registering systemd services..."
if [ "$SKIP_SYSTEMD" = true ]; then
    echo "Skipping systemd setup (--skip-systemd)."
else
    TMP_UNIT_DIR="$(mktemp -d)"
    for unit in verimath-backend.service verimath-frontend.service verimath-mqtt-sync.service; do
        sed \
            -e "s|User=pi|User=$TARGET_USER|g" \
            -e "s|/home/pi/verimath|$WORKDIR|g" \
            -e "s|/home/pi/.elan|$TARGET_HOME/.elan|g" \
            -e "s|/usr/local/bin/serve|$SERVE_BIN|g" \
            "$WORKDIR/deployment/systemd/$unit" > "$TMP_UNIT_DIR/$unit"
        sudo cp "$TMP_UNIT_DIR/$unit" "/etc/systemd/system/$unit"
    done
    rm -rf "$TMP_UNIT_DIR"

    sudo systemctl daemon-reload
    sudo systemctl enable verimath-backend verimath-frontend verimath-mqtt-sync
    sudo systemctl restart verimath-backend verimath-frontend verimath-mqtt-sync
fi

PI_IP="$(hostname -I 2>/dev/null | awk '{print $1}' || echo 'raspberrypi.local')"
echo ""
echo "=========================================================="
echo "  VeriMath Raspberry Pi Deployment Complete!"
echo "  App URL (Same-Origin Low-RAM): http://localhost:8000/app/"
echo "  LAN App URL:                   http://${PI_IP}:8000/app/"
echo "  Frontend Port 3000 (alt):      http://localhost:3000"
echo "  Health Check:                  bash deployment/check_pi.sh"
echo "  Backend Logs:                  sudo journalctl -u verimath-backend -f"
echo "=========================================================="
