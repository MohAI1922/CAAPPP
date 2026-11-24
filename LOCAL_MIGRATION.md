# VeriMath — Full Cloud-to-Local Migration Guide

> **Goal**: Run VeriMath **100% locally** on your Laptop/PC or Raspberry Pi 4/5 with **zero cloud dependencies** (no Colab runtime, no Firebase/Firestore, no Gemini API, no external internet required after setup).

---

## 1. Cloud → Local Component Map

Every cloud-optional feature in VeriMath already has a local implementation or automatic fallback:

| Subsystem | Cloud Mode (Disabled) | 100% Local Replacement | Source File(s) |
|---|---|---|---|
| **LLM Autoformalizer** | Google Colab T4 training session | Fine-tuned `qwen2_5_1_5b_verimath_pi4-q4_k_m.gguf` (`940.4 MB`) via `llama-cpp-python` | [`backend/pipeline/solver.py`](backend/pipeline/solver.py), [`backend/pipeline/generalized_prover.py`](backend/pipeline/generalized_prover.py) |
| **Symbolic Math & Verification** | None (always local) | SymPy CAS + **Lean 4.36.0 + Mathlib4** kernel (`VERIMATH_STRICT_LEAN=true`) | [`backend/pipeline/lean_runner.py`](backend/pipeline/lean_runner.py), [`lean/VeriMath/`](lean/VeriMath/) |
| **Teacher Dashboard Telemetry** | Firebase Firestore (`firestore_sync.py`) | Local SQLite store (`telemetry_events.db`) | [`backend/iot/event_store.py`](backend/iot/event_store.py), [`backend/dashboard/router.py`](backend/dashboard/router.py) |
| **Teacher Session Summary** | Gemini 1.5 Flash (`GOOGLE_API_KEY`) | Built-in **Local Analytics Engine** | [`backend/dashboard/gemini_summary.py`](backend/dashboard/gemini_summary.py) |
| **Camera & Handwriting OCR** | `gemini_vision` | Local `rapidocr` (PP-OCRv4 ONNX) → `tesseract` (5.x LSTM), plus optional offline `trocr` / `pix2tex` | [`backend/connectors/vision_ocr.py`](backend/connectors/vision_ocr.py) |
| **Problem Cache** | None (always local) | Local SQLite cache (`demo_cache.db`) | [`backend/pipeline/cache.py`](backend/pipeline/cache.py) |

---

## 2. Step 1 — Move Your Fine-Tuned Model into `models/`

Do **not** commit `.gguf` files to Git (they are ignored by [`.gitignore`](.gitignore)).

1. Place your exported Colab model in `models/`:
   ```bash
   mkdir -p models
   mv ~/Downloads/qwen2_5_1_5b_verimath_pi4-q4_k_m.gguf models/
   ```
2. Verify the file integrity against your Colab export checksum:
   - **Linux / macOS / Raspberry Pi:**
     ```bash
     sha256sum models/qwen2_5_1_5b_verimath_pi4-q4_k_m.gguf
     ```
   - **Windows PowerShell:**
     ```powershell
     Get-FileHash .\models\qwen2_5_1_5b_verimath_pi4-q4_k_m.gguf -Algorithm SHA256
     ```
   - Expected SHA-256:
     `e95f1239fe81a2e81e1ae7434678eac8957bf98daf9e39a78309091187ff6c80`

> **Note**: Do **not** run `scripts/download_model.py` once your fine-tuned `.gguf` is in `models/`, or make sure `LLM_MODEL_PATH` already points to `qwen2_5_1_5b_verimath_pi4-q4_k_m.gguf` so the script skips downloading the un-fine-tuned base model.

---

## 3. Step 2 — Configure a 100% Local `.env`

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Replace the contents with the appropriate profile below (leaving all cloud keys **blank**):

### Option A: Laptop / Desktop (Linux, macOS, or Windows)
```dotenv
# ── Cloud Services (Disabled for 100% Local Mode) ──
GOOGLE_API_KEY=
FIREBASE_SERVICE_ACCOUNT_PATH=
FIREBASE_PROJECT_ID=

# ── Lean 4 (Local Kernel Verification) ──
# Leave LEAN_BINARY_PATH blank to auto-detect ~/.elan/bin/lean (or set full path)
LEAN_BINARY_PATH=
LEAN_PROJECT_PATH=./lean/VeriMath
VERIMATH_STRICT_LEAN=true
LEAN_TIMEOUT_SECONDS=45

# ── Local LLM (Fine-tuned Qwen2.5-1.5B Q4_K_M GGUF) ──
LLM_MODEL_PATH=./models/qwen2_5_1_5b_verimath_pi4-q4_k_m.gguf
LLM_N_CTX=4096
LLM_N_THREADS=4

# ── Local Cache & App ──
MAX_FORMALIZATION_RETRIES=3
DEMO_CACHE_PATH=./demo_cache.db
APP_HOST=127.0.0.1
APP_PORT=8000
APP_ENV=production

# ── Local Camera & Handwriting OCR ──
OCR_BACKEND=auto
TROCR_MODEL_ID=microsoft/trocr-base-handwritten
TROCR_LOCAL_FILES_ONLY=true
```

### Option B: Raspberry Pi 4 / 5 (64-bit Raspberry Pi OS)
Use absolute paths under `/home/pi/verimath` (matching `deployment/systemd/*.service`) and `APP_HOST=0.0.0.0` so devices on your LAN can open the UI:
```dotenv
GOOGLE_API_KEY=
FIREBASE_SERVICE_ACCOUNT_PATH=
FIREBASE_PROJECT_ID=

LEAN_BINARY_PATH=/home/pi/.elan/bin/lean
LEAN_PROJECT_PATH=/home/pi/verimath/lean/VeriMath
VERIMATH_STRICT_LEAN=true
LEAN_TIMEOUT_SECONDS=45

LLM_MODEL_PATH=/home/pi/verimath/models/qwen2_5_1_5b_verimath_pi4-q4_k_m.gguf
LLM_N_CTX=4096
LLM_N_THREADS=4

MAX_FORMALIZATION_RETRIES=3
DEMO_CACHE_PATH=/home/pi/verimath/demo_cache.db
APP_HOST=0.0.0.0
APP_PORT=8000
APP_ENV=production

OCR_BACKEND=auto
TROCR_MODEL_ID=microsoft/trocr-base-handwritten
TROCR_LOCAL_FILES_ONLY=true
```

---

## 4. Step 3 — Install Local Toolchain (Lean 4 + Mathlib4, Python, OCR, Frontend)

### 4.1 Lean 4.36.0 & Mathlib4 Prebuilt Cache
The project toolchain is pinned in [`lean/VeriMath/lean-toolchain`](lean/VeriMath/lean-toolchain) (`leanprover/lean4:v4.36.0`).

```bash
# 1. Install elan (skip if `lean --version` already works)
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh -s -- -y
source "$HOME/.elan/env"

# 2. Fetch prebuilt Mathlib4 .olean cache (avoids compiling Mathlib from source)
cd lean/VeriMath
lake exe cache get || lake build
cd ../..
```

### 4.2 System Packages for Local OCR & Camera
- **Ubuntu / Debian / Raspberry Pi OS:**
  ```bash
  sudo apt update
  sudo apt install -y tesseract-ocr fswebcam build-essential cmake python3-venv nodejs npm
  ```
- **Windows:**
  - Install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) and ensure `tesseract.exe` is on `PATH` (RapidOCR works out-of-the-box via pip without Tesseract).
  - Browser webcam capture (`CameraScannerModal`) works directly in Chrome/Edge on `localhost`.

### 4.3 Python Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows PowerShell: .\.venv\Scripts\Activate.ps1
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```
> **Optional offline handwriting/LaTeX models**: RapidOCR + Tesseract work immediately. If you want offline `trocr` or `pix2tex` as well, install `transformers torch` (for `microsoft/trocr-base-handwritten`, cached once while online so `TROCR_LOCAL_FILES_ONLY=true` works offline) or `pix2tex`.

### 4.4 Build the React Frontend
```bash
cd frontend
npm install
npm run build
cd ..
```

### 4.5 Warm Up Lean 4 Once
```bash
python scripts/warmup_lean.py
```

---

## 5. Step 4 — Start Locally (No Cloud Processes)

### Laptop / Desktop
You only need the FastAPI backend + frontend (no Mosquitto, no `firestore_sync.py`):
```bash
# Terminal 1: Backend (API + Lean 4 + Qwen2.5 GGUF + Local OCR)
.venv/bin/python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000

# Terminal 2: Frontend (dev mode) OR serve frontend/build/
cd frontend && npm start
```
Open **`http://localhost:3000`** (or **`http://localhost:8000/app`** if serving the production build via FastAPI).

### Raspberry Pi 4 / 5
1. Run `deployment/install_pi.sh` (only if not yet installed; since `models/qwen2_5_1_5b_verimath_pi4-q4_k_m.gguf` is already in place, Step 5 won't overwrite it).
2. Enable only the local services and **disable** the cloud Firestore sync service:
   ```bash
   sudo systemctl disable --now verimath-mqtt-sync || true
   sudo systemctl enable --now verimath-backend verimath-frontend
   sudo systemctl restart verimath-backend verimath-frontend
   ```

---

## 6. Step 5 — Verify 100% Local Operation

Run these checks with internet disconnected (or cloud keys blank):

1. **System health & model detection:**
   ```bash
   curl -s http://localhost:8000/health
   ```
   Confirm:
   - `"lean_installed": true`
   - `"strict_lean_mode": true`
   - `"model_loaded": true`

2. **Connectors status (confirm local OCR ready & cloud disabled):**
   ```bash
   curl -s http://localhost:8000/connectors/status
   ```
   Confirm:
   - `ocr_engines.rapidocr: true` and/or `ocr_engines.tesseract: true`
   - `ocr_engines.gemini_vision: false`
   - `firebase.configured: false`
   - `gemini_summary_configured: false`

3. **Run the regression test suite:**
   ```bash
   python3 -m unittest discover -s backend/tests -t .
   ```
   *(If tests modify `demo_cache.db`, `telemetry_events.db`, or `backend/tests/test_cache.db`, restore them with `git checkout -- demo_cache.db telemetry_events.db backend/tests/test_cache.db`.)*

---

## 7. Recommended Code Cleanups for Pure-Local Quality

1. **Align ChatML prompt tags for your fine-tuned Qwen2.5-1.5B GGUF:**
   - [`backend/pipeline/generalized_prover.py`](backend/pipeline/generalized_prover.py) and [`backend/pipeline/explainer.py`](backend/pipeline/explainer.py) already use Qwen2.5 ChatML (`<|im_start|>system ... <|im_end|>`).
   - [`backend/pipeline/solver.py`](backend/pipeline/solver.py) (`_build_prompt`) and [`backend/pipeline/formalizer.py`](backend/pipeline/formalizer.py) (`_build_prompt`) still use legacy Phi-3 tags (`<|system|>...<|end|>`). Updating those two functions to `<|im_start|>` / `<|im_end|>` ensures your fine-tuned Qwen2.5 model follows instructions cleanly on every template problem.
2. **Optional cloud-package & UI cleanup:**
   - Remove `firebase-admin` and `google-generativeai` from [`requirements.txt`](requirements.txt) if you want zero cloud SDKs installed.
   - Remove the `<option value="gemini_vision">Gemini Vision (Cloud)</option>` entry from [`frontend/src/components/CameraScannerModal.jsx`](frontend/src/components/CameraScannerModal.jsx) and rebuild `frontend/`.
3. **Clean up uncommitted working tree edits** (`git status`) before deploying across machines so Laptop and Pi stay in sync.
