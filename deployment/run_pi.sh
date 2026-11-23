#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# VeriMath — Raspberry Pi Foreground Runner (Low-RAM Single-Process Mode)
# ─────────────────────────────────────────────────────────────────────────────
# Starts the FastAPI backend + built React frontend at http://0.0.0.0:8000/app/
# without requiring systemd or a separate Node static server process.
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKDIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$WORKDIR"

export PATH="$HOME/.elan/bin:$PATH"

if [ -f "$WORKDIR/.env" ]; then
    set -a
    # shellcheck disable=SC1091
    source "$WORKDIR/.env"
    set +a
fi

export VERIMATH_STRICT_LEAN="${VERIMATH_STRICT_LEAN:-true}"
export LEAN_TIMEOUT_SECONDS="${LEAN_TIMEOUT_SECONDS:-45}"

PYTHON_BIN="$WORKDIR/.venv/bin/python"
if [ ! -x "$PYTHON_BIN" ]; then
    PYTHON_BIN="$(command -v python3)"
fi

if [ ! -f "$WORKDIR/frontend/build/index.html" ]; then
    echo "Building React frontend (frontend/build not found)..."
    (cd "$WORKDIR/frontend" && npm install && npm run build)
fi

PI_IP="$(hostname -I 2>/dev/null | awk '{print $1}' || echo '127.0.0.1')"
echo "=========================================================="
echo "  Starting VeriMath on Raspberry Pi"
echo "  Strict Lean Mode : $VERIMATH_STRICT_LEAN"
echo "  Local Browser UI : http://localhost:8000/app/"
echo "  LAN Browser UI   : http://${PI_IP}:8000/app/"
echo "=========================================================="

exec "$PYTHON_BIN" -m uvicorn backend.main:app --host "${APP_HOST:-0.0.0.0}" --port "${APP_PORT:-8000}"
