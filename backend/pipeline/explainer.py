"""
VeriMath — Module 5: Intuitive Explainer
=========================================
Given a verified answer, generates a human-readable, student-friendly
explanation using Phi-3 Mini.

Key constraint: The explanation is explicitly grounded in the verified answer.
The explainer NEVER mentions Lean, formal proofs, or verification.
It presents the answer as if it computed it naturally.

Note: This is the only module where LLM "creative" output reaches the student —
but the answer it explains is already verified by Lean, so correctness is guaranteed
at the mathematical level. The explanation may still be unclear or imperfect, which
is why it is framed as supplementary.
"""

from __future__ import annotations

import logging
import time

from backend.pipeline.solver import _get_llm, _extract_json
import json

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# System prompt
# ─────────────────────────────────────────────────────────────────────────────

_EXPLAINER_SYSTEM_PROMPT = """\
You are a friendly and clear mathematics tutor. A student asked you a math question.
You already know the correct answer. Your job is to explain it intuitively.

RULES:
- Address a university-level student (not a child, but assume first-year level).
- Be clear, step-by-step, and use plain language.
- You may use simple math notation (e.g. x², sin(x), ∫) but avoid LaTeX commands.
- NEVER mention "Lean", "formal proof", "verification system", or "proof assistant".
- NEVER say you "checked" or "verified" — just explain naturally.
- Keep the explanation under 200 words.
- End with a one-sentence summary of the key insight.
"""

_EXPLAINER_USER_TEMPLATE = """\
Problem: {problem}

Correct answer: {verified_answer}

Step-by-step working (use this as a guide, but explain in your own words):
{reasoning}

Provide a clear, intuitive explanation for a university student:"""


# ─────────────────────────────────────────────────────────────────────────────
# Main explainer function
# ─────────────────────────────────────────────────────────────────────────────

def explain(
    problem: str,
    verified_answer: str,
    reasoning: str,
) -> str:
    """
    Generate an intuitive explanation for a verified answer.

    Args:
        problem: Original natural language problem.
        verified_answer: The answer that has been verified by Lean.
        reasoning: Step-by-step working from the solver (used as a guide).

    Returns:
        A plain-English explanation string.
    """
    llm = _get_llm()

    start = time.monotonic()

    prompt = _build_prompt(problem, verified_answer, reasoning)

    response = llm(
        prompt,
        max_tokens=350,
        temperature=0.3,    # Slight creativity for natural-sounding explanation
        stop=["Problem:", "<|user|>"],
        echo=False,
    )

    elapsed_ms = int((time.monotonic() - start) * 1000)
    explanation = response["choices"][0]["text"].strip()

    logger.info(f"Explanation generated in {elapsed_ms}ms ({len(explanation)} chars)")

    # Safety: remove any accidental mentions of Lean/verification
    explanation = _scrub_lean_mentions(explanation)

    return explanation


def _build_prompt(problem: str, verified_answer: str, reasoning: str) -> str:
    """Build the Phi-3 Mini prompt for explanation generation."""
    user_msg = _EXPLAINER_USER_TEMPLATE.format(
        problem=problem,
        verified_answer=verified_answer,
        reasoning=reasoning or "No working provided.",
    )

    return (
        f"<|system|>\n{_EXPLAINER_SYSTEM_PROMPT}<|end|>\n"
        f"<|user|>\n{user_msg}<|end|>\n"
        f"<|assistant|>\n"
    )


def _scrub_lean_mentions(text: str) -> str:
    """Remove any accidental references to Lean or formal verification."""
    scrub_words = [
        "lean", "lean 4", "mathlib", "formal proof", "proof assistant",
        "formally verified", "lean kernel", "theorem prover",
    ]
    result = text
    for word in scrub_words:
        # Case-insensitive replacement
        import re
        result = re.sub(re.escape(word), "[the system]", result, flags=re.IGNORECASE)
    return result
