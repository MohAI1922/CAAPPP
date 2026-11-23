#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# VeriMath — Raspberry Pi Hardware & Runtime Readiness Check
# ─────────────────────────────────────────────────────────────────────────────

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKDIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$WORKDIR"

export PATH="$HOME/.elan/bin:$PATH"

echo "=========================================================="
echo "  VeriMath — Raspberry Pi Readiness Check"
echo "=========================================================="

echo "[1] Hardware & OS:"
echo "  Arch   : $(uname -m)"
echo "  Kernel : $(uname -r)"
free -h | awk 'NR==1 || NR==2 {print "  " $0}'

echo ""
echo "[2] Lean 4 & Mathlib:"
if command -v lean >/dev/null 2>&1 && command -v lake >/dev/null 2>&1; then
    echo "  lean   : $(lean --version)"
    echo "  lake   : $(lake --version)"
    if [ -d "$WORKDIR/lean/VeriMath/.lake/packages/mathlib/.lake/build/lib/lean" ]; then
        echo "  Mathlib: prebuilt .olean cache present"
    else
        echo "  Mathlib: .olean cache missing (run: cd lean/VeriMath && lake exe cache get && lake build VeriMath)"
    fi
else
    echo "  WARNING: lean/lake not found in PATH ($HOME/.elan/bin)"
fi

echo ""
echo "[3] Python Environment & OCR / LLM:"
PYTHON_BIN="$WORKDIR/.venv/bin/python"
if [ ! -x "$PYTHON_BIN" ]; then
    PYTHON_BIN="$(command -v python3)"
fi
"$PYTHON_BIN" - <<'PYEOF'
import importlib.util
for pkg in ("fastapi", "uvicorn", "sympy", "llama_cpp", "rapidocr_onnxruntime", "pytesseract", "paho.mqtt"):
    ok = importlib.util.find_spec(pkg) is not None
    print(f"  {pkg:22s}: {'OK' if ok else 'MISSING'}")
PYEOF

echo ""
echo "[4] Local GGUF Models & Frontend Build:"
ls -lh "$WORKDIR/models"/*.gguf 2>/dev/null || echo "  No .gguf found in models/ (run: python3 scripts/download_model.py)"
if [ -f "$WORKDIR/frontend/build/index.html" ]; then
    echo "  React build          : OK ($WORKDIR/frontend/build)"
else
    echo "  React build          : MISSING (run: cd frontend && npm run build)"
fi

echo ""
echo "[5] External Connectors (Camera, Tesseract OCR, MQTT):"
echo "  tesseract            : $(command -v tesseract >/dev/null 2>&1 && tesseract --version | head -n 1 || echo 'MISSING')"
echo "  rpicam-still         : $(command -v rpicam-still || command -v libcamera-still || echo 'not installed')"
echo "  fswebcam             : $(command -v fswebcam || echo 'not installed')"
ls -1 /dev/video* 2>/dev/null | head -n 5 || echo "  /dev/video*          : none detected (USB webcam not attached)"
echo "  mosquitto            : $(systemctl is-active mosquitto 2>/dev/null || true)"

echo ""
echo "[6] Live Backend /health (if running):"
if curl -sf http://127.0.0.1:8000/health; then
    echo ""
else
    echo "  Backend not currently listening on port 8000 (start with: bash deployment/run_pi.sh)"
fi
echo "=========================================================="
