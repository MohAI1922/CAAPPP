"""
VeriMath — Student Multi-Step Derivation Grader (SymPy CAS)
=============================================================
Grades and diagnoses a student's own step-by-step mathematical derivation
rather than only solving from scratch.

Supported modes:
  - algebra:    verifies step_i == step_{i+1} symbolically
  - equation:   verifies equation solution equivalence across steps
  - derivative: verifies d/dx(step_0) == step_1 (or prompt expression) and subsequent simplifications
  - integral:   verifies d/dx(step_1) == step_0 (ignoring + C) and subsequent simplifications
  - auto:       infers mode from problem prompt
"""

from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from typing import List, Optional

import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)

_TRANSFORMS = standard_transformations + (implicit_multiplication_application, convert_xor)


@dataclass
class StepGrade:
    step_index: int
    step_text: str
    valid: bool
    feedback: str
    error_type: Optional[str] = None  # None | "sign_error" | "constant_error" | "factor_error" | "algebra_mismatch" | "parse_error"


@dataclass
class DerivationGradeResult:
    overall_correct: bool
    operation: str
    first_error_step: Optional[int]
    step_results: List[StepGrade]
    summary: str

    def to_dict(self) -> dict:
        return {
            "overall_correct": self.overall_correct,
            "operation": self.operation,
            "first_error_step": self.first_error_step,
            "step_results": [asdict(s) for s in self.step_results],
            "summary": self.summary,
        }


def _clean_math_text(s: str) -> str:
    s = s.strip()
    s = s.replace("[", "(").replace("]", ")").replace("−", "-").replace("·", "*").replace("×", "*")
    s = s.replace("²", "^2").replace("³", "^3")
    # Strip trailing "+ C" or "+ c" in antiderivatives
    s = re.sub(r"\+\s*[cC]\s*$", "", s).strip()
    # Strip common prefixes like "f'(x) =", "dy/dx =", "y' =", "Step 1:"
    s = re.sub(r"^(?:step\s*\d+\s*:\s*)", "", s, flags=re.I)
    s = re.sub(r"^(?:f'\(x\)|dy/dx|y'|d/dx\([^)]+\))\s*=\s*", "", s, flags=re.I)
    return s.strip()


def _parse_math(s: str) -> sp.Expr:
    cleaned = _clean_math_text(s)
    local_dict = {
        "x": sp.Symbol("x"),
        "y": sp.Symbol("y"),
        "t": sp.Symbol("t"),
        "e": sp.E,
        "pi": sp.pi,
        "ln": sp.log,
    }
    return parse_expr(cleaned, local_dict=local_dict, transformations=_TRANSFORMS)


def _infer_operation(problem: str, steps: List[str], operation: str) -> str:
    if operation != "auto":
        return operation
    p_l = problem.lower()
    if any(k in p_l for k in ("integral", "integrate", "antiderivative", "∫")):
        return "integral"
    if any(k in p_l for k in ("derivative", "differentiate", "d/dx", "f'(x)", "dy/dx")):
        return "derivative"
    if any("=" in s for s in steps) or "solve" in p_l:
        return "equation"
    return "algebra"


def _diagnose_expr_mismatch(expected: sp.Expr, actual: sp.Expr, var: sp.Symbol) -> tuple[str, str]:
    try:
        if sp.simplify(expected + actual) == 0:
            return "sign_error", "Sign inversion detected: your expression has the opposite sign."
        diff_expr = sp.simplify(expected - actual)
        if diff_expr.is_number and diff_expr != 0:
            return "constant_error", f"Constant term mismatch (off by {diff_expr})."
        if actual != 0:
            ratio = sp.simplify(expected / actual)
            if ratio.is_number and ratio != 1:
                return "factor_error", f"Missing or incorrect constant coefficient factor (off by a factor of {ratio})."
    except Exception:
        pass
    return "algebra_mismatch", f"Expression is not equivalent to the expected value ({expected})."


def grade_student_steps(
    problem: str,
    student_steps: List[str],
    operation: str = "auto",
) -> DerivationGradeResult:
    if not student_steps:
        return DerivationGradeResult(
            overall_correct=False,
            operation=operation,
            first_error_step=0,
            step_results=[],
            summary="No student steps provided to grade.",
        )

    op = _infer_operation(problem, student_steps, operation)
    x = sp.Symbol("x")
    results: List[StepGrade] = []
    first_error: Optional[int] = None

    # Parse all steps
    parsed_steps: List[Optional[object]] = []
    for idx, raw in enumerate(student_steps):
        try:
            if op == "equation" and "=" in raw:
                lhs_s, rhs_s = _clean_math_text(raw).split("=", 1)
                parsed_steps.append(("eq", _parse_math(lhs_s) - _parse_math(rhs_s)))
            else:
                parsed_steps.append(("expr", _parse_math(raw)))
        except Exception as e:
            parsed_steps.append(None)
            if first_error is None:
                first_error = idx
            results.append(
                StepGrade(
                    step_index=idx,
                    step_text=raw,
                    valid=False,
                    feedback=f"Could not parse mathematical expression: {e}",
                    error_type="parse_error",
                )
            )
            return DerivationGradeResult(
                overall_correct=False,
                operation=op,
                first_error_step=first_error,
                step_results=results,
                summary=f"Syntax/parse error at step {idx + 1}.",
            )

    # Step 0 is always accepted as the starting expression/equation
    results.append(
        StepGrade(
            step_index=0,
            step_text=student_steps[0],
            valid=True,
            feedback="Starting expression/equation parsed successfully.",
        )
    )

    for idx in range(1, len(student_steps)):
        prev_kind, prev_val = parsed_steps[idx - 1]  # type: ignore[misc]
        curr_kind, curr_val = parsed_steps[idx]      # type: ignore[misc]

        valid = False
        feedback = ""
        err_type: Optional[str] = None

        if op == "equation" and prev_kind == "eq" and curr_kind == "eq":
            sol_prev = sp.solve(prev_val, x)
            sol_curr = sp.solve(curr_val, x)
            if sol_prev == sol_curr:
                valid = True
                feedback = "Valid equivalent equation transformation."
            else:
                err_type = "algebra_mismatch"
                feedback = f"Solution set changed from {sol_prev} to {sol_curr}."

        elif op == "derivative" and idx == 1 and prev_kind == "expr" and curr_kind == "expr":
            expected_deriv = sp.diff(prev_val, x)
            if sp.simplify(expected_deriv - curr_val) == 0:
                valid = True
                feedback = "Correct differentiation step."
            else:
                err_type, feedback = _diagnose_expr_mismatch(expected_deriv, curr_val, x)

        elif op == "integral" and idx == 1 and prev_kind == "expr" and curr_kind == "expr":
            recovered = sp.diff(curr_val, x)
            if sp.simplify(recovered - prev_val) == 0:
                valid = True
                feedback = "Correct antiderivative step (verified via d/dx)."
            else:
                expected_int = sp.integrate(prev_val, x)
                err_type, feedback = _diagnose_expr_mismatch(expected_int, curr_val, x)

        elif prev_kind == "expr" and curr_kind == "expr":
            if sp.simplify(prev_val - curr_val) == 0:
                valid = True
                feedback = "Valid algebraic simplification."
            else:
                err_type, feedback = _diagnose_expr_mismatch(prev_val, curr_val, x)

        if not valid and first_error is None:
            first_error = idx

        results.append(
            StepGrade(
                step_index=idx,
                step_text=student_steps[idx],
                valid=valid,
                feedback=feedback,
                error_type=err_type,
            )
        )

    overall = first_error is None
    summary = (
        f"All {len(student_steps)} steps verified."
        if overall
        else f"Error detected at step {first_error + 1}: {results[first_error].feedback}"
    )

    return DerivationGradeResult(
        overall_correct=overall,
        operation=op,
        first_error_step=first_error,
        step_results=results,
        summary=summary,
    )
