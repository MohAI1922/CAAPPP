#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# VeriMath — Mathlib Pre-compilation Script
# ─────────────────────────────────────────────────────────────────────────────
# ⚠️  RUN THIS ON YOUR LAPTOP/DESKTOP — NOT ON THE RASPBERRY PI ⚠️
#
# What this does:
#   1. Downloads Lean 4 (via elan) if not installed
#   2. Runs `lake build` to compile Mathlib and the VeriMath package
#   3. The resulting .lake/build/ directory contains .olean cache files
#
# After this script completes:
#   - Compress: tar -czf mathlib_cache.tar.gz .lake/
#   - Copy to Pi: scp mathlib_cache.tar.gz pi@raspberrypi.local:~/verimath/lean/VeriMath/
#   - On Pi: cd ~/verimath/lean/VeriMath && tar -xzf mathlib_cache.tar.gz
#
# Time estimates:
#   - First run (download + compile): 30–90 minutes on a modern laptop
#   - Subsequent runs (cache hit): < 30 seconds
#   - On Raspberry Pi 4: 6–12+ hours (DO NOT DO THIS ON PI)
#
# Requirements:
#   - 8 GB+ RAM
#   - 20 GB+ free disk space (Mathlib is large)
#   - Internet connection
# ─────────────────────────────────────────────────────────────────────────────

set -e  # Exit on any error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LEAN_PROJECT_DIR="$SCRIPT_DIR"

echo "============================================================"
echo "  VeriMath — Mathlib Pre-compilation"
echo "  Project: $LEAN_PROJECT_DIR"
echo "============================================================"
echo ""
echo "⚠️  WARNING: This should run on a laptop/desktop, NOT on Raspberry Pi."
echo "   Estimated time: 30–90 minutes (first run)"
echo ""
read -p "Continue? [y/N] " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 0
fi

# ── Step 1: Check / install elan (Lean version manager) ──────────────────────
if ! command -v elan &> /dev/null; then
    echo "Installing elan (Lean version manager)..."
    curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh -s -- -y
    source "$HOME/.elan/env"
fi

echo "Lean version: $(lean --version)"

# ── Step 2: Navigate to project directory ────────────────────────────────────
cd "$LEAN_PROJECT_DIR"

# ── Step 3: Update dependencies (downloads Mathlib) ──────────────────────────
echo ""
echo "Step 1/2: Downloading Mathlib (this may take 10–20 minutes)..."
lake update

# ── Step 4: Build (compile Mathlib + VeriMath) ───────────────────────────────
echo ""
echo "Step 2/2: Compiling Mathlib (this is the slow step — 30–90 min)..."
echo "You can leave this running and come back."
echo ""
time lake build

echo ""
echo "✅ Mathlib pre-compilation complete!"
echo ""
echo "Next steps — copy cache to Raspberry Pi:"
echo ""
echo "  1. Compress:"
echo "     tar -czf mathlib_cache.tar.gz .lake/"
echo ""
echo "  2. Copy to Pi (replace raspberrypi.local with your Pi's IP):"
echo "     scp mathlib_cache.tar.gz pi@raspberrypi.local:~/verimath/lean/VeriMath/"
echo ""
echo "  3. On the Pi, extract:"
echo "     ssh pi@raspberrypi.local"
echo "     cd ~/verimath/lean/VeriMath"
echo "     tar -xzf mathlib_cache.tar.gz"
echo ""
echo "  4. Verify on Pi:"
echo "     lake env lean --version"
echo "     echo 'example : 1 + 1 = 2 := by norm_num' > /tmp/test.lean"
echo "     lake env lean /tmp/test.lean && echo 'Lean works! ✅'"
