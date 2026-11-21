"""
VeriMath — Module 6 (Novel Contribution): Generalized Out-of-Domain Autoformalizer & Prover
=============================================================================================
Invoked IF AND ONLY IF a problem does NOT match any of VeriMath's 244 assigned
templates (`classify_problem(problem) is None`) and is not in `demo_cache.db`.

Architecture (Zero-Trust Propose → Formalize → Judge → Lean Verify / Reject):
  1. Domain Gate: Rejects non-mathematical prompts cleanly.
  2. Proposal Generation:
       a) When a trained/local GGUF LLM is loaded, prompts it to propose a
          candidate answer AND a standalone Lean 4 theorem (`example ... := by ...`)
          without `sorry`/`admit`/`axiom`.
       b) Deterministic Generalized Symbolic Autoformalizer handles broad unseen
          mathematical structures outside the fixed templates:
            - Algebraic / polynomial identities & false-identity stress tests
            - Inequalities (<, >, <=, >=)
            - Modular arithmetic, divisibility (a ∣ b), GCD / LCM
            - Factorials, binomial coefficients, finite sums
            - Multivariable partial derivatives (∂/∂x, ∂/∂y)
            - 2x2 matrix determinants & vector dot products
  3. Faithfulness & Zero-Trust Lean 4 Kernel Gate:
       - Rejects any `sorry`/`admit`/`axiom`.
       - Verifies with `verify_async()` (Lean 4.36.0 + Mathlib4).
       - If the proposed claim is false or unprovable by Lean, REJECTS entirely
         (`status = "REJECTED"`) — never leaks unverified answers to students.
"""

from __future__ import annotations

import json
import logging
import math
import re
from dataclasses import dataclass
from typing import Optional

import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)

from backend.pipeline.solver import _get_llm, _extract_json

logger = logging.getLogger(__name__)

_TRANSFORMS = standard_transformations + (implicit_multiplication_application, convert_xor)


@dataclass
class GeneralizedProposal:
    subkind: str                 # e.g. "generalized_identity", "generalized_inequality", ...
    candidate_answer: str        # Human-readable proposed answer
    lean_statement: str          # Standalone Lean 4 `example ... := by ...`
    back_translation: str        # Plain-English restatement for faithfulness check
    reasoning: str               # Conceptual reasoning summary
    is_math_problem: bool = True


_GENERALIZED_SYSTEM_PROMPT = """\
You are VeriMath Generalized Autoformalizer. The user's math problem is OUTSIDE the predefined template set.
Propose a concise candidate answer AND a standalone, valid Lean 4 theorem (using Mathlib tactics like norm_num, ring, omega, linarith, decide, or simp) that formally proves the answer.

STRICT RULES:
1. NEVER use `sorry`, `admit`, or custom `axiom`.
2. Output ONLY valid JSON with keys:
   {"is_math": true, "answer": "...", "lean_statement": "example ... := by ...", "back_translation": "...", "reasoning": "..."}
3. If the prompt is NOT a mathematical problem, output: {"is_math": false}.
"""


def _looks_like_math(problem: str) -> bool:
    p_l = problem.lower()
    if re.search(r"[0-9=<>+\-*/^∫∂√π]|<=|>=|≠|≤|≥|∣", problem):
        return True
    if re.search(r"\bis\s+(?:\d|prime|divisible|equal|greater|less)", p_l):
        return True
    math_words = (
        "prove", "verify", "show that", "does ", "divide", "divisible",
        "mod", "modulo", "remainder", "gcd", "lcm", "factorial", "choose",
        "binomial", "sum of", "partial derivative", "determinant", "matrix",
        "dot product", "inequality", "identity", "polynomial", "factor",
        "simplify", "expand", "evaluate", "compute", "calculate", "derivative",
        "integral", "solve", "prime", "square", "cube", "root",
    )
    return any(w in p_l for w in math_words)


def _to_lean_expr(expr_str: str) -> str:
    s = expr_str.strip().replace("**", "^")
    s = re.sub(r"\bsin\(", "Real.sin (", s)
    s = re.sub(r"\bcos\(", "Real.cos (", s)
    s = re.sub(r"\btan\(", "Real.tan (", s)
    s = re.sub(r"\bexp\(", "Real.exp (", s)
    s = re.sub(r"\blog\(", "Real.log (", s)
    s = re.sub(r"\bln\(", "Real.log (", s)
    s = re.sub(r"\bsqrt\(", "Real.sqrt (", s)
    s = re.sub(r"\bpi\b", "Real.pi", s)
    return s


def _safe_sympy(expr_str: str) -> sp.Expr:
    cleaned = expr_str.strip()
    cleaned = cleaned.replace("[", "(").replace("]", ")").replace("−", "-").replace("×", "*").replace("·", "*")
    cleaned = cleaned.replace("²", "^2").replace("³", "^3").replace("π", "pi")
    local_dict = {
        "x": sp.Symbol("x"),
        "y": sp.Symbol("y"),
        "z": sp.Symbol("z"),
        "a": sp.Symbol("a"),
        "b": sp.Symbol("b"),
        "c": sp.Symbol("c"),
        "n": sp.Symbol("n"),
        "k": sp.Symbol("k"),
        "t": sp.Symbol("t"),
        "e": sp.E,
        "pi": sp.pi,
        "ln": sp.log,
    }
    return parse_expr(cleaned, local_dict=local_dict, transformations=_TRANSFORMS)


def _propose_symbolic(problem: str) -> Optional[GeneralizedProposal]:
    p = problem.strip()
    p_l = p.lower()

    # 1. Partial Derivatives: ∂/∂x or "partial derivative of ... with respect to x/y/z"
    m_pd = re.search(
        r"(?:partial\s+derivative\s+(?:of\s+)?|∂\s*/\s*∂\s*([xyz])\s*(?:of\s+)?)(.+?)(?:\s+(?:with\s+respect\s+to|w\.?r\.?t\.?)\s+([xyz]))?$",
        p,
        re.I,
    )
    if "partial" in p_l or "∂" in p:
        var_m = re.search(r"(?:with\s+respect\s+to|w\.?r\.?t\.?|∂\s*/\s*∂)\s*([xyz])", p_l)
        wrt = var_m.group(1) if var_m else "x"
        expr_m = re.search(r"(?:partial\s+derivative\s+(?:of\s+)?|∂/∂[xyz]\s*(?:of\s+)?)(.+?)(?:\s+(?:with\s+respect\s+to|w\.?r\.?t\.?)\s+[xyz].*)?$", p, re.I)
        if expr_m:
            raw_expr = re.sub(r"^[fgh]\([^)]+\)\s*=\s*", "", expr_m.group(1).strip()).rstrip("?.!")
            try:
                sym_expr = _safe_sympy(raw_expr)
                v = sp.Symbol(wrt)
                ans_expr = sp.simplify(sp.diff(sym_expr, v))
                free_vars = sorted({str(s) for s in (sym_expr.free_symbols | ans_expr.free_symbols | {v})})
                binders = " ".join(free_vars)
                lean_expr = _to_lean_expr(str(sym_expr))
                lean_ans = _to_lean_expr(str(ans_expr))
                ans_disp = str(ans_expr).replace("**", "^").replace("log(", "ln(")
                lean_stmt = (
                    f"example ({binders} : ℝ) : deriv (fun {wrt} => {lean_expr}) {wrt} = {lean_ans} := by\n"
                    f"  simp (disch := fun_prop) [deriv_comp, deriv_mul, deriv_add, deriv_sub, deriv_div, deriv_pow, Real.deriv_sin, Real.deriv_cos, Real.deriv_exp, Real.deriv_log]\n"
                    f"  try ring"
                )
                return GeneralizedProposal(
                    subkind="generalized_partial_derivative",
                    candidate_answer=ans_disp,
                    lean_statement=lean_stmt,
                    back_translation=f"Find the partial derivative of {raw_expr} with respect to {wrt}. The result is {ans_disp}.",
                    reasoning=f"Holding all variables other than {wrt} constant and differentiating {raw_expr} with respect to {wrt} yields {ans_disp}.",
                )
            except Exception:
                pass

    # 2. 2x2 Matrix Determinant: [[a, b], [c, d]]
    m_det = re.search(
        r"determinant.*?\[\s*\[\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\]\s*,\s*\[\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\]\s*\]",
        p_l,
    )
    if m_det:
        a, b, c, d = m_det.groups()
        det_val = sp.Rational(a) * sp.Rational(d) - sp.Rational(b) * sp.Rational(c)
        det_s = str(int(det_val)) if det_val == int(det_val) else str(det_val)
        lean_stmt = f"example : ({a} : ℝ) * ({d}) - ({b}) * ({c}) = {det_s} := by norm_num"
        return GeneralizedProposal(
            subkind="generalized_linear_algebra",
            candidate_answer=det_s,
            lean_statement=lean_stmt,
            back_translation=f"Find the determinant of the 2x2 matrix [[{a}, {b}], [{c}, {d}]]. The determinant is {det_s}.",
            reasoning=f"For a 2x2 matrix [[a, b], [c, d]], det = a*d - b*c = ({a})*({d}) - ({b})*({c}) = {det_s}.",
        )

    # 3. Vector Dot Product: dot product of (a, b, ...) and (c, d, ...)
    m_dot = re.search(
        r"dot\s+product.*?\(\s*([^\)]+)\s*\)\s*(?:and|with|·|\*)\s*\(\s*([^\)]+)\s*\)",
        p_l,
    )
    if m_dot:
        v1 = [x.strip() for x in m_dot.group(1).split(",")]
        v2 = [x.strip() for x in m_dot.group(2).split(",")]
        if len(v1) == len(v2) and v1:
            try:
                terms = [f"({a} : ℝ) * ({b})" for a, b in zip(v1, v2)]
                total = sum(sp.Rational(a) * sp.Rational(b) for a, b in zip(v1, v2))
                tot_s = str(int(total)) if total == int(total) else str(total)
                lean_stmt = f"example : {' + '.join(terms)} = {tot_s} := by norm_num"
                return GeneralizedProposal(
                    subkind="generalized_linear_algebra",
                    candidate_answer=tot_s,
                    lean_statement=lean_stmt,
                    back_translation=f"Find the dot product of ({', '.join(v1)}) and ({', '.join(v2)}). The answer is {tot_s}.",
                    reasoning=f"Multiply matching components and sum: {' + '.join(terms)} = {tot_s}.",
                )
            except Exception:
                pass

    # 4. Divisibility: "Does a divide b?" / "Is b divisible by a?"
    m_div1 = re.search(r"does\s+(\d+)\s+divide\s+(\d+)", p_l)
    m_div2 = re.search(r"is\s+(\d+)\s+divisible\s+by\s+(\d+)", p_l)
    if m_div1 or m_div2:
        a, b = (m_div1.group(1), m_div1.group(2)) if m_div1 else (m_div2.group(2), m_div2.group(1))
        a_i, b_i = int(a), int(b)
        is_true = (a_i != 0 and b_i % a_i == 0)
        # Propose the literal affirmative divisibility theorem if asked to prove/check;
        # Wait: if asked "Does 7 divide 100?", Lean verifies `7 ∣ 100` (which Lean REJECTS if false!).
        # If the question asks "Does a divide b?", propose the positive claim only if true?
        # Even better: when user asserts or tests divisibility, let Lean prove `a ∣ b` when true,
        # OR if user says "Prove that 7 divides 100", propose `7 ∣ 100` so Lean REJECTS the false claim!
        if "prove" in p_l or "show" in p_l or "verify" in p_l or is_true:
            lean_stmt = f"example : ({a_i} : ℕ) ∣ {b_i} := by decide"
            return GeneralizedProposal(
                subkind="generalized_number_theory",
                candidate_answer=f"Yes, {a_i} divides {b_i}" if is_true else f"{a_i} divides {b_i}",
                lean_statement=lean_stmt,
                back_translation=f"Does {a_i} divide {b_i}? Claim: {a_i} divides {b_i}.",
                reasoning=f"Check divisibility {b_i} mod {a_i} = {b_i % a_i if a_i else 'undefined'}.",
            )
        else:
            # Question "Does 7 divide 100?" when false: verify the negative theorem `¬ (7 ∣ 100)`
            lean_stmt = f"example : ¬ (({a_i} : ℕ) ∣ {b_i}) := by decide"
            return GeneralizedProposal(
                subkind="generalized_number_theory",
                candidate_answer=f"No, {a_i} does not divide {b_i}",
                lean_statement=lean_stmt,
                back_translation=f"Does {a_i} divide {b_i}? No, {a_i} does not divide {b_i}.",
                reasoning=f"{b_i} divided by {a_i} leaves remainder {b_i % a_i} ≠ 0, so {a_i} does not divide {b_i}.",
            )

    # 5. Modular arithmetic / GCD / LCM / Binomial / Factorial
    m_mod = re.search(r"(\d+)\s*(?:mod|modulo|%)\s*(\d+)", p_l)
    if m_mod:
        a_i, m_i = int(m_mod.group(1)), int(m_mod.group(2))
        if m_i > 0:
            rem = a_i % m_i
            return GeneralizedProposal(
                subkind="generalized_number_theory",
                candidate_answer=str(rem),
                lean_statement=f"example : ({a_i} : ℕ) % {m_i} = {rem} := by norm_num",
                back_translation=f"Compute {a_i} mod {m_i}. The remainder is {rem}.",
                reasoning=f"Dividing {a_i} by {m_i} leaves remainder {rem}.",
            )

    m_gcd = re.search(r"\bgcd\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)", p_l)
    if m_gcd:
        a_i, b_i = int(m_gcd.group(1)), int(m_gcd.group(2))
        g = math.gcd(a_i, b_i)
        return GeneralizedProposal(
            subkind="generalized_number_theory",
            candidate_answer=str(g),
            lean_statement=f"example : Nat.gcd {a_i} {b_i} = {g} := by decide",
            back_translation=f"Find gcd({a_i}, {b_i}). The answer is {g}.",
            reasoning=f"Using Euclidean division, the greatest common divisor of {a_i} and {b_i} is {g}.",
        )

    m_choose = re.search(r"(?:choose|C)\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)", p, re.I)
    if m_choose:
        n_i, k_i = int(m_choose.group(1)), int(m_choose.group(2))
        if n_i <= 20 and k_i <= n_i:
            val = math.comb(n_i, k_i)
            return GeneralizedProposal(
                subkind="generalized_series_combinatorics",
                candidate_answer=str(val),
                lean_statement=f"example : Nat.choose {n_i} {k_i} = {val} := by decide",
                back_translation=f"Compute choose({n_i}, {k_i}). The value is {val}.",
                reasoning=f"C({n_i}, {k_i}) = {n_i}! / ({k_i}! * ({n_i}-{k_i})!) = {val}.",
            )

    m_sum = re.search(r"sum\s+of\s+(?:the\s+)?first\s+(\d+)\s+positive\s+integers", p_l)
    if m_sum:
        n_i = int(m_sum.group(1))
        if 1 <= n_i <= 200:
            total = n_i * (n_i + 1) // 2
            return GeneralizedProposal(
                subkind="generalized_series_combinatorics",
                candidate_answer=str(total),
                lean_statement=f"example : (∑ k ∈ Finset.Icc 1 {n_i}, k) = {total} := by decide",
                back_translation=f"Find the sum of the first {n_i} positive integers. The sum is {total}.",
                reasoning=f"Summing 1 + 2 + ... + {n_i} using Gauss pairing gives {n_i}*({n_i}+1)/2 = {total}.",
            )

    # 6. Numeric Inequalities: e.g. "Prove that 2^10 > 1000" or "Is 3/7 < 1/2?"
    m_ineq = re.search(
        r"(?:prove\s+that|show\s+that|verify\s+that|is|check\s+(?:whether|if))?\s*([0-9\+\-\*\/\^\(\)\s\.]+?)\s*(<=|>=|≤|≥|<|>)\s*([0-9\+\-\*\/\^\(\)\s\.]+?)[?.!]*$",
        p_l,
    )
    if m_ineq and not re.search(r"[a-zA-Z]", m_ineq.group(1) + m_ineq.group(3)):
        lhs_s, op_s, rhs_s = m_ineq.group(1).strip(), m_ineq.group(2), m_ineq.group(3).strip()
        op_map = {"<=": "≤", ">=": "≥", "≤": "≤", "≥": "≥", "<": "<", ">": ">"}
        lean_op = op_map[op_s]
        try:
            l_val = _safe_sympy(lhs_s)
            r_val = _safe_sympy(rhs_s)
            is_true = bool(
                (lean_op == "<" and l_val < r_val)
                or (lean_op == ">" and l_val > r_val)
                or (lean_op == "≤" and l_val <= r_val)
                or (lean_op == "≥" and l_val >= r_val)
            )
            if "prove" in p_l or "show" in p_l or "verify" in p_l or is_true:
                lean_stmt = f"example : ({lhs_s} : ℝ) {lean_op} ({rhs_s} : ℝ) := by norm_num"
                ans_txt = f"True ({lhs_s} {lean_op} {rhs_s})" if is_true else f"{lhs_s} {lean_op} {rhs_s}"
            else:
                lean_stmt = f"example : ¬ (({lhs_s} : ℝ) {lean_op} ({rhs_s} : ℝ)) := by norm_num"
                ans_txt = f"False (¬ ({lhs_s} {lean_op} {rhs_s}))"
            return GeneralizedProposal(
                subkind="generalized_inequality",
                candidate_answer=ans_txt,
                lean_statement=lean_stmt,
                back_translation=f"Compare {lhs_s} {op_s} {rhs_s}. Result: {ans_txt}.",
                reasoning=f"Evaluating both sides numerically: {lhs_s} = {l_val} and {rhs_s} = {r_val}.",
            )
        except Exception:
            pass

    # 7. Algebraic / Polynomial Identities (both true & false claim stress tests!)
    # Matches "Prove that <LHS> = <RHS>", "Verify <LHS> = <RHS>", "Check whether <LHS> = <RHS>"
    m_id = re.search(
        r"(?:prove\s+that|show\s+that|verify\s+that|verify|check\s+(?:whether|if)|is\s+it\s+true\s+that)\s+(.+?)\s*=\s*(.+?)[?.!]*$",
        p_l,
    )
    if m_id:
        lhs_raw = re.sub(r"\s+for\s+all\b.*$", "", m_id.group(1).strip())
        rhs_raw = re.sub(r"\s+for\s+all\b.*$", "", m_id.group(2).strip())
        try:
            l_sym = _safe_sympy(lhs_raw)
            r_sym = _safe_sympy(rhs_raw)
            free_vars = sorted({str(s) for s in (l_sym.free_symbols | r_sym.free_symbols)})
            lean_lhs = _to_lean_expr(str(l_sym))
            lean_rhs = _to_lean_expr(str(r_sym))
            if free_vars:
                binders = " ".join(free_vars)
                lean_stmt = f"example ({binders} : ℝ) : {lean_lhs} = {lean_rhs} := by ring"
            else:
                lean_stmt = f"example : ({lean_lhs} : ℝ) = ({lean_rhs} : ℝ) := by norm_num"
            return GeneralizedProposal(
                subkind="generalized_identity",
                candidate_answer=f"{lhs_raw} = {rhs_raw}",
                lean_statement=lean_stmt,
                back_translation=f"Verify whether {lhs_raw} = {rhs_raw}.",
                reasoning=f"Checking algebraic equivalence between {lhs_raw} and {rhs_raw}.",
            )
        except Exception:
            pass

    # 8. General polynomial expansion / factorization ("Expand (x+y)^3", "Factor x^3 - y^3")
    m_exp = re.search(r"^(?:expand|multiply\s+out)\s+(.+?)[?.!]*$", p_l)
    if m_exp:
        raw_expr = m_exp.group(1).strip()
        try:
            sym_e = _safe_sympy(raw_expr)
            expanded = sp.expand(sym_e)
            free_vars = sorted({str(s) for s in (sym_e.free_symbols | expanded.free_symbols)})
            binders = f"({' '.join(free_vars)} : ℝ) " if free_vars else ""
            lean_lhs = _to_lean_expr(str(sym_e))
            lean_rhs = _to_lean_expr(str(expanded))
            ans_disp = str(expanded).replace("**", "^")
            lean_stmt = f"example {binders}: {lean_lhs} = {lean_rhs} := by ring"
            return GeneralizedProposal(
                subkind="generalized_identity",
                candidate_answer=ans_disp,
                lean_statement=lean_stmt,
                back_translation=f"Expand {raw_expr}. The expanded form is {ans_disp}.",
                reasoning=f"Expanding {raw_expr} by distributivity yields {ans_disp}.",
            )
        except Exception:
            pass

    m_fac = re.search(r"^(?:factor|factorize)\s+(.+?)[?.!]*$", p_l)
    if m_fac:
        raw_expr = m_fac.group(1).strip()
        try:
            sym_e = _safe_sympy(raw_expr)
            factored = sp.factor(sym_e)
            free_vars = sorted({str(s) for s in (sym_e.free_symbols | factored.free_symbols)})
            binders = f"({' '.join(free_vars)} : ℝ) " if free_vars else ""
            lean_lhs = _to_lean_expr(str(sym_e))
            lean_rhs = _to_lean_expr(str(factored))
            ans_disp = str(factored).replace("**", "^")
            lean_stmt = f"example {binders}: {lean_lhs} = {lean_rhs} := by ring"
            return GeneralizedProposal(
                subkind="generalized_identity",
                candidate_answer=ans_disp,
                lean_statement=lean_stmt,
                back_translation=f"Factor {raw_expr}. The factored form is {ans_disp}.",
                reasoning=f"Factoring {raw_expr} yields {ans_disp}.",
            )
        except Exception:
            pass

    return None


def propose_generalized(problem: str, feedback: Optional[str] = None) -> GeneralizedProposal:
    """
    Propose a candidate solution and standalone Lean 4 theorem for an unseen,
    out-of-domain mathematical problem (outside all 244 trained templates).
    """
    if not _looks_like_math(problem):
        return GeneralizedProposal(
            subkind="non_math",
            candidate_answer="",
            lean_statement="",
            back_translation="",
            reasoning="Prompt does not appear to be a mathematical problem.",
            is_math_problem=False,
        )

    # 1. Try local LLM synthesis if a real GGUF model is loaded
    llm = _get_llm()
    if llm.__class__.__name__ != "_MockLLM":
        fb = f"\nPrevious verification feedback (fix this): {feedback}" if feedback else ""
        prompt = (
            f"<|im_start|>system\n{_GENERALIZED_SYSTEM_PROMPT}<|im_end|>\n"
            f"<|im_start|>user\n{problem}{fb}<|im_end|>\n"
            f"<|im_start|>assistant\n"
        )
        try:
            resp = llm(
                prompt,
                max_tokens=380,
                temperature=0.1,
                stop=["<|im_end|>", "<|user|>"],
                echo=False,
            )
            raw = resp["choices"][0]["text"].strip()
            parsed = _extract_json(raw)
            if isinstance(parsed, dict):
                if parsed.get("is_math") is False:
                    return GeneralizedProposal(
                        subkind="non_math",
                        candidate_answer="",
                        lean_statement="",
                        back_translation="",
                        reasoning="Classified as non-mathematical prompt.",
                        is_math_problem=False,
                    )
                stmt = str(parsed.get("lean_statement", "")).strip()
                ans = str(parsed.get("answer", "")).strip()
                if stmt and ans:
                    return GeneralizedProposal(
                        subkind="generalized_llm_synthesis",
                        candidate_answer=ans,
                        lean_statement=stmt,
                        back_translation=str(parsed.get("back_translation", f"{problem} Answer: {ans}.")),
                        reasoning=str(parsed.get("reasoning", "")),
                        is_math_problem=True,
                    )
        except Exception as e:
            logger.warning(f"Generalized LLM proposal failed, trying symbolic autoformalizer: {e}")

    # 2. Generalized Symbolic Autoformalizer (covers unseen identities, inequalities,
    #    divisibility/mod/gcd, sums/combinatorics, partial derivatives, matrices/vectors)
    sym_prop = _propose_symbolic(problem)
    if sym_prop is not None:
        return sym_prop

    # 3. Unformalizable mathematical claim -> empty Lean statement (will be REJECTED by gate)
    return GeneralizedProposal(
        subkind="generalized_unformalized",
        candidate_answer="",
        lean_statement="",
        back_translation="",
        reasoning="Could not construct a valid formal Lean 4 statement for this out-of-domain problem.",
        is_math_problem=True,
    )
