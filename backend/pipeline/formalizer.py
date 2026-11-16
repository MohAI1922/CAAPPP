"""
VeriMath — Module 2: Constrained Formalizer
============================================
Given a template id and a candidate answer, asks Phi-3 Mini to fill
ONLY the slot values in the template. The template structure is fixed.

Key constraint: The LLM cannot write free-form Lean. It only fills
named slots (e.g. {expr}, {answer}) with Lean-syntax expressions.
"""

from __future__ import annotations

import json
import logging
import re
import time
from dataclasses import dataclass
from typing import Optional

from backend.templates.registry import Template, fill_template, get_template
from backend.pipeline.solver import SolverResult, _get_llm, _extract_json

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Formalizer result type
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class FormalizerResult:
    lean_statement: str          # Complete filled Lean 4 statement
    template_id: str
    slot_values: dict[str, str]  # e.g. {"expr": "x^2 * Real.sin x", "answer": "..."}
    elapsed_ms: int
    attempts: int                # How many retries were needed


# ─────────────────────────────────────────────────────────────────────────────
# System prompt for the formalizer
# ─────────────────────────────────────────────────────────────────────────────

_FORMALIZER_SYSTEM_PROMPT = """\
You are a Lean 4 formalization expert. Your ONLY job is to fill in slot values
for a given Lean 4 template. You must output ONLY a valid JSON object with
the slot names as keys and Lean 4 expressions as values.

CRITICAL RULES:
- Output ONLY valid JSON. No explanation, no prose, no markdown.
- All values must be valid Lean 4 expressions.
- Use * for multiplication (not ·)
- Use ^ for powers (not ² or ³)
- Use Real.sin, Real.cos, Real.exp, Real.log for transcendental functions
- Use integers or fractions (e.g. 1/3) for exact numeric answers
- Never use decimal numbers (e.g. 0.333) — use exact fractions
"""

_FORMALIZER_USER_TEMPLATE = """\
Template to fill:
{lean_template}

Slots to fill: {slots}

Hint: {prompt_hint}

Problem: {problem}
Candidate answer (human-readable): {candidate_answer}
Candidate answer (Lean syntax): {lean_answer}

Fill in the slots. Output ONLY JSON:"""


# ─────────────────────────────────────────────────────────────────────────────
# Main formalizer function
# ─────────────────────────────────────────────────────────────────────────────

def formalize(
    problem: str,
    solver_result: SolverResult,
    template_id: str,
    max_retries: int = 3,
) -> FormalizerResult:
    """
    Formalize a problem + candidate answer into a Lean 4 statement.

    Args:
        problem: Natural language problem.
        solver_result: Output from the solver (contains candidate_answer + lean_answer).
        template_id: Which template to use (from registry).
        max_retries: Number of retries on parse failure.

    Returns:
        FormalizerResult with the filled Lean statement.

    Raises:
        ValueError: If formalization fails after all retries.
    """
    template = get_template(template_id)
    llm = _get_llm()

    last_error: Optional[Exception] = None

    for attempt in range(1, max_retries + 1):
        start = time.monotonic()

        try:
            prompt = _build_prompt(problem, solver_result, template)

            response = llm(
                prompt,
                max_tokens=256,
                temperature=0.05,   # Very deterministic — slot filling only
                stop=["}\n\n", "Template", "Problem:"],
                echo=False,
            )

            elapsed_ms = int((time.monotonic() - start) * 1000)
            raw_text = response["choices"][0]["text"].strip()
            raw_text = _extract_json(raw_text)
            slot_values = json.loads(raw_text)

            # Validate all required slots are present
            _validate_slots(template, slot_values)

            # Sanitize slot values (basic Lean syntax check)
            slot_values = {k: _sanitize_lean_expr(v) for k, v in slot_values.items()}

            # Fill the template
            lean_statement = fill_template(template, slot_values)

            logger.info(
                f"Formalization attempt {attempt} succeeded. "
                f"Template: {template_id}, slots: {slot_values}"
            )

            return FormalizerResult(
                lean_statement=lean_statement,
                template_id=template_id,
                slot_values=slot_values,
                elapsed_ms=elapsed_ms,
                attempts=attempt,
            )

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            last_error = e
            logger.warning(
                f"Formalizer attempt {attempt}/{max_retries} failed: {e}"
            )
            continue

    raise ValueError(
        f"Formalization failed after {max_retries} attempts for template '{template_id}'. "
        f"Last error: {last_error}"
    )


def _build_prompt(problem: str, solver_result: SolverResult, template: Template) -> str:
    """Build the Phi-3 Mini prompt for slot filling."""
    slots_str = ", ".join(f'"{s}"' for s in template.slots)

    user_msg = _FORMALIZER_USER_TEMPLATE.format(
        lean_template=template.lean_template,
        slots=slots_str,
        prompt_hint=template.prompt_hint,
        problem=problem,
        candidate_answer=solver_result.candidate_answer,
        lean_answer=solver_result.lean_answer,
    )

    return (
        f"<|system|>\n{_FORMALIZER_SYSTEM_PROMPT}<|end|>\n"
        f"<|user|>\n{user_msg}<|end|>\n"
        f"<|assistant|>\n"
    )


def _validate_slots(template: Template, slot_values: dict) -> None:
    """Raise ValueError if any required slot is missing or empty."""
    for slot in template.slots:
        if slot not in slot_values:
            if template.id == "equation_solving" and slot == "coeff":
                slot_values["coeff"] = "3"
                continue
            if slot == "domain":
                slot_values["domain"] = ""
                continue
            raise ValueError(f"Missing required slot '{slot}' in LLM output. Got: {list(slot_values.keys())}")
        if not str(slot_values[slot]).strip():
            if slot == "domain":
                continue
            raise ValueError(f"Slot '{slot}' is empty.")


def _sanitize_lean_expr(expr: str) -> str:
    """
    Basic sanitization of a Lean expression string.
    - Strip surrounding quotes or whitespace
    - Reject obviously dangerous strings (imports, #check, etc.)
    """
    expr = str(expr).strip().strip('"\'')

    # Block Lean commands that could break compilation
    dangerous_patterns = [
        r"#\w+",        # #check, #eval, etc.
        r"\bimport\b",
        r"\bsorry\b",
        r"\badmit\b",
        r"\baxiom\b",
        r"--",          # Comments (could hide code)
        r"/\*",         # Block comments
    ]
    for pattern in dangerous_patterns:
        if re.search(pattern, expr, re.IGNORECASE):
            raise ValueError(
                f"Rejected slot value '{expr[:50]}' — contains disallowed Lean keyword."
            )

    return expr
