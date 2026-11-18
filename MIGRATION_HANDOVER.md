# VeriMath — Complete Project Migration & Handover Brief
> **Target Audience**: Incoming AI Assistant / Human Engineering Collaborators  
> **Date Generated**: November 18, 2026  
> **Repository**: [https://github.com/abdullahmosbah11-cmyk/CAAPPP.git](https://github.com/abdullahmosbah11-cmyk/CAAPPP.git)  
> **Local Workspace**: `d:\New folder (3)\verimath`

---

## 1. Directive for the Incoming AI Assistant

If you are an AI assistant reading this file at the start of a new chat session:
1. **You are Antigravity working on VeriMath** — an offline-first, zero-trust mathematical tutor where an LLM proposes solutions and **Lean 4 formally proves or rejects them**.
2. **Silently adopt all 23 Operating Rules** listed in Section 4 of this document. They are strict project invariants.
3. **Do not hallucinate or change the established architecture**:
   - Never use probabilistic LLMs for multi-step intermediate algebra or coefficient calculations.
   - Never generate multiple-choice questions (A, B, C, D). All problems are **open-response**.
   - Never mention external textbook names or page numbers ("El-Moasser", "The Book of Integrals", "Senior 3") in student-facing step text or explanations.
   - Keep Lean 4 formal syntax (`Real.sin`, `Real.cos`, `(x : ℝ)`) strictly isolated to the Lean verification panel; student-facing views must always use clean standard mathematical notation (`sin(x)`, `cos(x)`).
4. **Current Status**: All code, tests, and step generators are **100% operational and verified (250/250 unit tests passing)**. The next task in queue is **Colab Fine-Tuning Execution** (`scripts/VeriMath_Colab_FineTuning.ipynb`).

---

## 2. Project Overview & System Architecture

VeriMath eliminates AI math hallucinations in educational tutoring by separating natural language understanding from mathematical proof verification.

```
                  ┌────────────────────────────────────────────────────────┐
                  │                 Student Input (Open Response)          │
                  └───────────────────────────┬────────────────────────────┘
                                              ▼
                  ┌────────────────────────────────────────────────────────┐
                  │           Stage 1: Intent & Template Classifier         │
                  │        (244 Registered Symbolic Calculus Templates)     │
                  └───────────────────────────┬────────────────────────────┘
                                              ▼
                  ┌────────────────────────────────────────────────────────┐
                  │         Stage 2: Deterministic CAS Solver (SymPy)       │
                  │         - Exact symbolic differentiation & integration │
                  │         - Algebraic simplification & coordinate parsing│
                  └───────────────────────────┬────────────────────────────┘
                                              ▼
                  ┌────────────────────────────────────────────────────────┐
                  │         Stage 3: Formalizer (Lean 4 AST Construction)   │
                  │         - Mathlib real type annotations: (x : ℝ)       │
                  │         - Standard tactics: simp, ring, norm_num, omega│
                  └───────────────────────────┬────────────────────────────┘
                                              ▼
                  ┌────────────────────────────────────────────────────────┐
                  │         Stage 4: Statement Judge (Faithfulness Guard)   │
                  │         - Back-translation token set similarity ≥ 0.38 │
                  │         - Entity, function, and parameter preservation │
                  └───────────────────────────┬────────────────────────────┘
                                              ▼
                  ┌────────────────────────────────────────────────────────┐
                  │         Stage 5: Lean 4 Kernel Proof Verification      │
                  │         - Mechanical kernel check (Zero Trust)         │
                  │         - Proves or rejects statement with no bypasses │
                  └───────────────┬────────────────────────┬───────────────┘
                                  │                        │
                          [VERIFIED]                  [REJECTED]
                                  ▼                        ▼
                  ┌────────────────────────┐      ┌────────────────────────┐
                  │ Stage 6: Step Engine   │      │ Rejection Explanation  │
                  │ 4–5 Step CAS Derivations│      │ "Answer could not be   │
                  │ Zero Book Citations    │      │ formally verified"     │
                  └────────────────────────┘      └────────────────────────┘
```

### Why "Double AI" Was Explicitly Rejected
A common temptation is to use two LLMs: one to solve the problem and a second to write the pedagogical steps. In VeriMath, this was tested and strictly rejected:
1. **Edge Hardware Constraint**: VeriMath runs offline on a **Raspberry Pi 4 CPU** (4 cores, 4GB RAM). Running two sequential LLM inferences takes 20–35 seconds per problem, violating the $\le 15\text{ ms}$ offline edge SLA.
2. **Intermediate Arithmetic Hallucination**: LLMs frequently drop constants (e.g. dropping a $1/3$ factor), flip negative signs, or miscalculate polynomial divisions. Showing an AI-hallucinated intermediate step next to a verified final answer destroys student trust.
3. **The Solution (Neurosymbolic)**: SymPy CAS performs exact algebraic decomposition ($u$-substitution, polynomial long division, partial fractions, integration by parts), and deterministic step generators format authentic 4- to 5-step derivations in under $5\text{ ms}$.

---

## 3. Verified System Inventory & Metrics

| Component | Status | Details |
| :--- | :--- | :--- |
| **Git Remote** | `https://github.com/abdullahmosbah11-cmyk/CAAPPP.git` | Clean repository, branch `main`, protected with `.gitignore`. |
| **Registered Templates** | **244 Templates** | Defined in `backend/templates/registry.py`. Full calculus coverage: derivatives, higher-order, implicit differentiation, related rates, optimization, definite & indefinite integrals. |
| **Fine-Tuning Dataset** | **9,888 Entries** | File: `verimath_finetune_dataset.jsonl`. Verified ChatML format pairing authentic textbook problems with exact Lean 4 formalizations. |
| **Pre-Seeded Edge Cache** | **1,828 Entries** | File: `demo_cache.db`. Pre-seeded SQLite cache providing $\le 4\text{ ms}$ latency offline on Raspberry Pi 4 CPU. Zero Lean tokens in student fields. |
| **Unit Test Suite** | **250 / 250 Passing (100%)** | Located in `backend/tests/`. All 13 test suites pass in ~33 seconds (0 failures, 0 regressions). |
| **Pedagogical Step Engine** | **100% Remediated** | File: `backend/pipeline/step_generator.py`. AST-resilient $u$-sub, polynomial long division, and rational function decomposition. Zero textbook citations. |
| **Frontend UI** | **React + Tailwind** | Located in `frontend/`. Clean KaTeX rendering, walkthrough step navigation, teacher dashboard, and student view. |

---

## 4. The 23 Strict Operating Rules (Non-Negotiable)

* **Rule 1 (Context Refresh)**: Before initiating any task, silently inspect `project_state.md` to load all mathematical constraints, formatting standards, and the active task queue.
* **Rule 2 (Task Maintenance)**: Upon completing any task, update `project_state.md`: mark completed items, shift remaining tasks up, and record new engineering decisions.
* **Rule 3 (Historical Logging)**: Maintain `progress_tracker.md` as the cumulative chronological audit log of all completed milestones.
* **Rule 4 (Open-Response Standard)**: Never present, accept, or generate multiple-choice options (A, B, C, D). All problems and evaluations must be strictly open-response.
* **Rule 5 (Edge Hardware SLA)**: All core components must run offline on edge hardware (Raspberry Pi 4 CPU, 4 threads, 2048 ctx) with $\le 4\text{ ms}$ latency via `demo_cache.db`.
* **Rule 6 (Zero Regression Guarantee)**: The test suite (`backend/tests/`) must maintain a 100.0% pass rate at all times (250/250 passing tests).
* **Rule 7 (Neurosymbolic Division of Labor)**: Neural models parse informal intent and fill structured JSON slots; deterministic CAS (SymPy) solves and simplifies; Lean 4 checks proofs. Never use LLMs for intermediate algebraic arithmetic.
* **Rule 8 (Two-Way Fine-Tuning)**: Train via Way 1 (Authentic textbook wording & pedagogy) and Way 2 (Parametric variation of coefficients, powers, and roots).
* **Rule 9 (Hallucination Rejection)**: If required parameters are missing from a problem prompt, return `"is_complete": false` rather than inventing numerical values.
* **Rule 10 (Balanced-Parenthesis Coordinate Extraction)**: When extracting evaluation coordinates $(x_0, y_0)$, count parenthesis nesting depth to correctly parse nested function values (e.g., $(4, \sqrt{19})$, $(1, 6e^{-2})$).
* **Rule 11 (Point-Free Tangent Slopes)**: Prompts phrasing *"Find the slope of the tangent for f(x) = ..."* without an evaluation point $x_0$ represent queries for the derivative function $f'(x)$.
* **Rule 12 (Difference Quotient Limit Definition)**: Limits of difference quotients $\lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$ must map to the derivative of the depth-0 subtrahend $f(x)$.
* **Rule 13 (Constant & Identity Traps)**: Expressions evaluating to constants (e.g. $\sin^2 x + \cos^2 x = 1$, $10^{10\log(u)} = u^{10}$) must simplify to $f'(x) = 0$ via CAS.
* **Rule 14 (Universal Square Bracket Normalization)**: Normalize `[` `]` to `(` `)` across all mathematical parsing to ensure standard SymPy compatibility.
* **Rule 15 (Faithfulness Threshold)**: Statement Judge back-translations must meet a minimum token set similarity threshold ($\ge 0.38$) against the user's natural language prompt.
* **Rule 16 (Cache Key Normalization)**: Always lowercase, collapse spaces, strip terminal punctuation (`?`, `.`, `!`), and convert Unicode minus/powers (`−` $\to$ `-`, `²` $\to$ `^2`) before querying or writing to `demo_cache.db`.
* **Rule 17 (Implicit Multiplication Parsing)**: Multi-letter variables (e.g. $xy, yx, xy^2$) in implicit equations must be parsed with `implicit_multiplication_application` to prevent creating composite atom symbols.
* **Rule 18 (Euler Exponential Normalization)**: Expressions in Lean statements containing bare $e^{\dots}$ must be normalized to $\exp(\dots)$ in verifier pipelines so Euler's number $E$ is evaluated as a mathematical constant.
* **Rule 19 (Functional Substitution Resolution)**: Multi-function declarations (`Given g(x) = ..., f(x) = ... find derivative of h(x) = g(x)*f(x)`) must substitute definitions prior to differentiation.
* **Rule 20 (Radial Fraction Point Evaluation)**: Coordinate parsing for trigonometric slopes must parse exact fractional multiples of $\pi$ ($\pi/6, \pi/4, \pi/3, \pi/2$) prior to bare $\pi$, and poles must evaluate to `undefined` rather than `nan`.
* **Rule 21 (Deterministic Step Generation)**: Step derivations must be generated symbolically via `backend/pipeline/step_generator.py` in sub-15ms latency with zero LLM intermediate hallucination.
* **Rule 22 (Lean 4 Syntax Isolation & KaTeX Safety)**: Lean 4 formal syntax (`Real.sin x`, `Real.cos x`, `Real.exp x`, `Real.pi`) belongs exclusively in `lean_statement`. Student-facing fields (`verified_answer`, `candidate_answer`) must strictly use standard mathematical notation (`sin(x)`, `cos(x)`, `e^x`, `\pi`). `to_latex()` must sanitize any Lean namespaces and must NEVER wrap expressions containing operators (`^`, `*`, `+`, `-`, `/`, `=`) inside `\text{...}`.
* **Rule 23 (Pedagogical Explanation Cleanliness & Citation Prohibition)**: Student-facing explanations and step texts must strictly avoid external textbook names, authors, or page numbers (e.g., no "According to El-Moasser", "The Book of Integrals, p. 58", "Senior 3 Calculus"). Mathematical derivations must stand on their own objective logical grounds using standard universal mathematical terminology.

---

## 5. Key File Tree & Directory Map

```text
d:\New folder (3)\verimath\
├── backend/
│   ├── main.py                      # FastAPI orchestrator (POST /solve endpoint)
│   ├── pipeline/
│   │   ├── solver.py                # LLM solver + fallback intelligent SymPy CAS solver
│   │   ├── formalizer.py            # Converts candidate answer to Lean 4 statement
│   │   ├── statement_judge.py       # Faithfulness & token-set validation guardrail
│   │   ├── lean_runner.py           # Lean 4 subprocess execution & verification
│   │   ├── explainer.py             # Intuitive natural language explanation
│   │   ├── cache.py                 # SQLite edge demo cache interface
│   │   └── step_generator.py        # 4–5 step deterministic CAS derivations
│   ├── templates/
│   │   └── registry.py              # 244 Lean 4 verified problem templates
│   ├── tests/                       # 250 unit tests across 13 test suites (100% pass)
│   ├── dashboard/                   # Teacher analytics & telemetry router
│   └── iot/                         # MQTT telemetry publisher
├── frontend/                        # React 18 + Tailwind student & dashboard UI
│   ├── src/
│   │   ├── components/ResultPanel.jsx  # Renders verified answer, KaTeX, & step derivation
│   │   └── pages/StudentView.jsx       # Student problem input & live feedback
│   └── package.json
├── lean/
│   └── VeriMath/
│       ├── lakefile.lean            # Lean 4 / Mathlib build configuration
│       └── VeriMath/Tactics.lean    # Custom verification tactics
├── models/                          # Storage for GGUF model files (ignored in git)
├── scripts/
│   ├── VeriMath_Colab_FineTuning.ipynb  # Active notebook for GPU fine-tuning
│   ├── download_model.py            # Automated downloader for Qwen2.5/Phi-3 GGUF models
│   └── clean_citations.py           # Verification script ensuring zero textbook citations
├── demo_cache.db                    # 1,828 pre-seeded offline edge responses (SQLite)
├── verimath_finetune_dataset.jsonl  # 9,888 verified ChatML training examples
├── project_state.md                 # Living state & operating protocol (Rule 1 & 2)
├── progress_tracker.md              # Cumulative historical progress log (Rule 3)
├── requirements.txt                 # Python dependencies
├── serve.py                         # Production server launcher
└── Push_To_GitHub.bat               # Helper script to sync with remote repo
```

---

## 6. How to Run the System

### 1. Run the Backend Server
```bash
cd "d:\New folder (3)\verimath"
uvicorn backend.main:app --reload --port 8000
# or: python serve.py
```
* API Health Check: `http://127.0.0.1:8000/docs`
* Main Endpoint: `POST http://127.0.0.1:8000/solve` with body `{"problem": "Integrate: x^2 * sqrt(x^3 + 4) dx"}`

### 2. Run the Frontend UI
```bash
cd "d:\New folder (3)\verimath\frontend"
npm start
```
* Opens automatically at `http://localhost:3000`

### 3. Run the Complete Test Suite
```bash
cd "d:\New folder (3)\verimath"
python -m unittest discover -s backend/tests -t .
# Expected: Ran 250 tests in ~33s -> OK (100% pass rate)
```

---

## 7. Active Task Queue (What Needs to Be Done Next)

### Immediate Next Task: Colab Fine-Tuning Execution
* **File**: [`scripts/VeriMath_Colab_FineTuning.ipynb`](file:///d:/New%20folder%20(3)/verimath/scripts/VeriMath_Colab_FineTuning.ipynb)
* **Goal**: Fine-tune `Qwen/Qwen2.5-1.5B-Instruct` on the completed 9,888 verified ChatML dataset (`verimath_finetune_dataset.jsonl`) on a free Google Colab T4 GPU.
* **Hyperparameters**:
  - Framework: Unsloth (4-bit QLoRA)
  - LoRA Rank: $r = 16$, $\alpha = 32$, target modules: `q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj`
  - Epochs: 2
  - Batch Size: 2 with Gradient Accumulation 4 (Effective batch size = 8)
  - Learning Rate: $2 \times 10^{-4}$ with cosine decay

### Queued Follow-Up Tasks
1. **Quantization & GGUF Export**: Export the fine-tuned LoRA adapter into `Q4_K_M` GGUF format (`models/qwen2_5_1_5b_verimath_pi4-q4_k_m.gguf`).
2. **Raspberry Pi 4 Physical Hardware Benchmarking**: Transfer the GGUF model and `demo_cache.db` to a physical Raspberry Pi 4 CPU (4 threads, 2048 ctx) to verify token/sec speed and $\le 4\text{ ms}$ cache lookup.
3. **End-to-End Edge Verification**: Validate offline Lean 4 type-checking and automated fallback on live hardware without internet access.
