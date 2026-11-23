# VeriMath 🧮✅

**A Lean-Verified AI Math Tutor for Reliable Educational Assistance**

VeriMath is an AI-powered math tutoring system that uses **Lean 4** as an independent correctness oracle. The LLM proposes answers. Lean proves them. Students only see verified answers.

---

## How It Works

```
Student types problem → LLM solves it → LLM formalizes into Lean 4 template
→ Rule-based judge checks faithfulness → Lean 4 verifies the statement
→ ✅ Verified: student sees answer + intuitive explanation
→ ❌ Rejected: student sees "this answer could not be verified"
→ 🚫 Unsupported: "this problem type is outside the verified domain"
```

## Hardware

- **Raspberry Pi 4 (8 GB RAM)** — runs Lean 4 + Python backend + Qwen2.5-1.5B/3B Q4_K_M + MQTT broker
- **HDMI Monitor + USB keyboard/mouse** — student interface
- **Internet** (optional) — for Firebase Firestore telemetry sync

## Quick Start (Development on Laptop)

### Fast Start (No C++ Compiler or Mathlib Build Required)
Uses SymPy CAS + RapidOCR + React so you can test the entire UI, solver, step grader, and laptop webcam OCR in ~2 minutes on Windows, macOS, or Linux:

```bash
# 1. Clone and set up Python environment
git clone https://github.com/MohAI1922/CAAPPP.git verimath
cd verimath
python -m venv .venv
source .venv/bin/activate        # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements-laptop.txt

# 2. Create .env (keep VERIMATH_STRICT_LEAN=false for fast SymPy fallback)
cp .env.example .env             # Windows: copy .env.example .env

# 3. Start backend
uvicorn backend.main:app --reload --port 8000

# 4. Start frontend (in a new terminal)
cd frontend && npm install && npm start
```

Open your browser to `http://localhost:3000`.

### Optional: Full Lean 4 Kernel + Local Qwen2.5 GGUF on Laptop
1. Install Lean 4 (`elan`), then fetch prebuilt Mathlib `.olean` artifacts:
   ```bash
   curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh -s -- -y
   cd lean/VeriMath && lake exe cache get && lake build VeriMath && cd ../..
   ```
2. Set `VERIMATH_STRICT_LEAN=true` in `.env`.
3. Optionally install `llama-cpp-python` (`pip install -r requirements.txt`, requires CMake + C++ compiler) and download the local Qwen2.5 model:
   ```bash
   python scripts/download_model.py        # Qwen2.5-1.5B Q4_K_M (~980 MB)
   ```

## Running on Raspberry Pi 4 / Pi 5 (64-bit Raspberry Pi OS)

1. Flash **Raspberry Pi OS (64-bit / `aarch64`)** and clone the repository:
   ```bash
   git clone https://github.com/MohAI1922/CAAPPP.git verimath
   cd verimath
   ```
2. Run the automated Raspberry Pi installer (configures Mosquitto, Lean 4 + Mathlib cache, Python `.venv`, Qwen2.5 GGUF model, camera/OCR tools, React build, `.env`, and `systemd` services):
   ```bash
   bash deployment/install_pi.sh        # Default: Qwen2.5-1.5B Q4_K_M (4 GB / 8 GB Pi)
   # or for 8 GB Pi 4 / Pi 5:
   bash deployment/install_pi.sh --3b
   ```
3. Verify hardware, Lean 4, OCR, cameras, and services:
   ```bash
   bash deployment/check_pi.sh
   ```
4. Open the app in Chromium on the Pi (or from another device on the same network):
   - Single-process UI + API: `http://localhost:8000/app/`
   - Or manual foreground launch (without `systemd`):
     ```bash
     bash deployment/run_pi.sh
     ```


## Project Structure

```
verimath/
├── backend/          # Python FastAPI backend + pipeline modules
├── frontend/         # React student UI + teacher dashboard
├── lean/             # Lean 4 project (VeriMath package)
├── scripts/          # Utility scripts (warmup, dataset, eval)
├── deployment/       # Raspberry Pi install scripts + systemd units
└── backend/tests/dataset/  # 200-problem dataset (train + test)
```

## Supported Problem Types

| Type | Example | Lean Tactic |
|------|---------|-------------|
| Arithmetic | "What is 47 × 89 + 123?" | `norm_num` |
| Algebraic simplification | "Simplify (x+1)² − x²" | `ring` |
| Equation solving | "Solve 3x + 7 = 22" | `omega` |
| Derivative | "Find the derivative of x² sin(x)" | `simp` + `ring` |
| Definite integral | "Evaluate ∫₀¹ x² dx" | `norm_num` |
| Number theory | "Is 97 prime?" | `decide` |
| Geometry (distance) | "Distance between (1,2) and (4,6)?" | `norm_num` |

## Design Requirements

| Requirement | Target |
|---|---|
| Response time | ≤ 30 seconds |
| System accuracy (held-out test) | ≥ 80% |
| Hallucination rejection rate | ≥ 90% |
| Formalization fidelity | ≥ 85% |
| Battery life (Pi 4 + power bank) | ≥ 2 hours |
| Student comprehension | ≥ 75% agreement |

## Guarantee

> Any answer shown to a student has been formally verified by Lean 4's kernel — a proof assistant with a mathematically certified core. The AI proposes; Lean decides.
