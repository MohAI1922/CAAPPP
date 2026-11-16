"""
VeriMath — Book of Integrals Two-Way Fine-Tuning Dataset Generator & Appender
=============================================================================
Expands verimath_finetune_dataset.jsonl using TWO complementary pathways:
  Way 1: Authentic textbook problem pairs from Parts 1 & 2 (#1–148) and Parts 3 & 4 (#149–399)
         of Miguel Santiago's "Book of Integrals: Exploring Species of Integrals and Their Techniques".
  Way 2: Parametric / Randomized Generalization variations across all 18 technique archetypes
         to prevent overfitting to textbook constants and ensure robust out-of-distribution reasoning.

Each sample conforms to VeriMath's ChatML precision autoformalization format:
  - System prompt (Autoformalization Extractor)
  - User prompt (Mathematical problem with technique cue)
  - Assistant JSON response (template, is_complete, parameters, target, missing_parameters)
"""

import json
import os
import random
import sys

# Ensure repository root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.templates.registry import TEMPLATES, classify_problem

SYSTEM_PROMPT = (
    "You are VeriMath Precision Autoformalization Extractor. Your task is to analyze "
    "mathematical word problems, classify them into the correct template, extract all "
    "parameter values into a structured JSON object, and verify whether all necessary "
    "information is present to solve the problem. If any required variable is missing, "
    "set is_complete to false and identify the missing field. Output valid JSON only."
)

def make_entry(user_text: str, template: str, params: dict, target: str, is_complete: bool = True, missing: list = None):
    assistant_data = {
        "template": template,
        "is_complete": is_complete,
        "parameters": params,
        "target": target,
        "missing_parameters": missing or []
    }
    return {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text.strip()},
            {"role": "assistant", "content": json.dumps(assistant_data, indent=2)}
        ]
    }

def generate_way1_authentic():
    """Way 1: Authentic textbook problem pairs directly from Parts 1 to 4 of Book of Integrals."""
    entries = []

    # 1. pun_integral (Part 1, #1 - #15)
    pun_probs = [
        ("(3*x + 2)/(x^2 + 4*x + 5)", "Evaluate the integral of (3*x + 2)/(x^2 + 4*x + 5) dx using the P.U.N. method"),
        ("(5*x - 3)/(x^2 - 6*x + 25)", "Find the integral of (5*x - 3)/(x^2 - 6*x + 25) dx by the PUN method"),
        ("(2*x + 7)/(x^2 + 2*x + 10)", "Evaluate \\int (2*x + 7)/(x^2 + 2*x + 10) dx using the P.U.N. technique"),
        ("(4*x + 1)/(2*x^2 + 3*x + 5)", "Integrate (4*x + 1)/(2*x^2 + 3*x + 5) dx using the P.U.N. method"),
        ("(x - 4)/(x^2 + 8*x + 20)", "Find the antiderivative of (x - 4)/(x^2 + 8*x + 20) dx using the PUN method"),
        ("(6*x + 5)/(x^2 + 4)", "Evaluate \\int (6*x + 5)/(x^2 + 4) dx using the P.U.N. method"),
        ("(x + 3)/(x^2 + 2*x + 5)", "Integrate (x + 3)/(x^2 + 2*x + 5) dx using the P.U.N. technique"),
        ("(7*x - 2)/(x^2 - 4*x + 13)", "Evaluate \\int (7*x - 2)/(x^2 - 4*x + 13) dx by the PUN method"),
    ]
    for expr, q in pun_probs:
        entries.append(make_entry(q, "pun_integral", {"expr": expr}, "antiderivative"))
    entries.append(make_entry("Evaluate the integral of the rational function using the P.U.N. method", "pun_integral", {"expr": None}, "antiderivative", False, ["expr"]))

    # 2. root_manipulation_integral (Part 1, #16 - #30)
    root_probs = [
        ("x * sqrt(x + 1)", "Evaluate \\int x * sqrt(x + 1) dx by manipulating the root"),
        ("(x^2) / sqrt(2*x - 1)", "Find \\int (x^2)/sqrt(2*x - 1) dx by root manipulation substitution"),
        ("x * (3*x + 2)**(1/3)", "Integrate x * (3*x + 2)^(1/3) dx by manipulating the radical"),
        ("(x + 3) * sqrt(x - 2)", "Evaluate \\int (x + 3)*sqrt(x - 2) dx by manipulating the root"),
        ("(x^3) * sqrt(x^2 + 4)", "Find the antiderivative of x^3 * sqrt(x^2 + 4) dx by manipulating the root"),
        ("(2*x + 1) / sqrt(x - 3)", "Integrate (2*x + 1)/sqrt(x - 3) dx by manipulating the radical"),
        ("x * sqrt(2*x + 5)", "Evaluate \\int x * sqrt(2*x + 5) dx by manipulating the root"),
        ("(x - 1) * (x + 2)**(1/4)", "Find \\int (x - 1)*(x + 2)^(1/4) dx by root manipulation substitution"),
    ]
    for expr, q in root_probs:
        entries.append(make_entry(q, "root_manipulation_integral", {"expr": expr}, "antiderivative"))
    entries.append(make_entry("Find the antiderivative by manipulating the root", "root_manipulation_integral", {"expr": None}, "antiderivative", False, ["expr"]))

    # 3. inverted_quadratic_integral (Part 1, #31 - #45)
    inv_quad_probs = [
        ("1 / (x^2 + 9)", "Evaluate \\int 1/(x^2 + 9) dx using inverted quadratic standard form"),
        ("1 / (x^2 - 16)", "Find \\int 1/(x^2 - 16) dx by inverted quadratic method"),
        ("1 / (4*x^2 + 25)", "Integrate 1/(4*x^2 + 25) dx using inverted quadratic form"),
        ("exp(x) / (exp(2*x) + 4)", "Evaluate \\int e^x / (e^(2x) + 4) dx by inverted quadratic substitution"),
        ("cos(x) / (sin(x)^2 + 9)", "Find the antiderivative of cos(x)/(sin(x)^2 + 9) dx using inverted quadratic"),
        ("1 / (x * (log(x)^2 + 16))", "Evaluate \\int 1/(x*(ln(x)^2 + 16)) dx using inverted quadratic form"),
        ("1 / (9*x^2 - 4)", "Find \\int 1/(9*x^2 - 4) dx using inverted quadratic form"),
        ("exp(x) / (exp(2*x) - 9)", "Integrate e^x / (e^(2x) - 9) dx using inverted quadratic method"),
    ]
    for expr, q in inv_quad_probs:
        entries.append(make_entry(q, "inverted_quadratic_integral", {"expr": expr}, "antiderivative"))
    entries.append(make_entry("Evaluate the integral using inverted quadratic form", "inverted_quadratic_integral", {"expr": None}, "antiderivative", False, ["expr"]))

    # 4. trig_substitution_integral (Part 1, #46 - #60)
    trig_sub_probs = [
        ("sqrt(9 - x^2)", "Evaluate \\int sqrt(9 - x^2) dx using trigonometric substitution"),
        ("1 / (x^2 * sqrt(x^2 + 4))", "Find \\int 1/(x^2 * sqrt(x^2 + 4)) dx by trig substitution"),
        ("sqrt(x^2 - 16) / x", "Integrate sqrt(x^2 - 16)/x dx using secant trigonometric substitution"),
        ("(x^3) / sqrt(4 - x^2)", "Evaluate \\int x^3 / sqrt(4 - x^2) dx using trigonometric substitution"),
        ("1 / (x^2 + 25)**(3/2)", "Find \\int 1/(x^2 + 25)^(3/2) dx using tangent trigonometric substitution"),
        ("(x^2) * sqrt(16 - x^2)", "Integrate x^2 * sqrt(16 - x^2) dx by trig substitution"),
        ("sqrt(25 - x^2) / x^2", "Evaluate \\int sqrt(25 - x^2)/x^2 dx using trigonometric substitution"),
        ("1 / (x * sqrt(x^2 - 9))", "Find the antiderivative of 1/(x * sqrt(x^2 - 9)) dx using trigonometric substitution"),
    ]
    for expr, q in trig_sub_probs:
        entries.append(make_entry(q, "trig_substitution_integral", {"expr": expr}, "antiderivative"))
    entries.append(make_entry("Evaluate using trigonometric substitution", "trig_substitution_integral", {"expr": None}, "antiderivative", False, ["expr"]))

    # 5. partial_fraction_integral (Part 1, #61 - #72)
    pfd_probs = [
        ("(2*x + 3) / ((x - 1)*(x + 2))", "Evaluate \\int (2*x + 3)/((x - 1)*(x + 2)) dx using partial fractions"),
        ("1 / (x * (x + 1) * (x + 2))", "Find \\int 1/(x*(x + 1)*(x + 2)) dx by partial fraction decomposition"),
        ("(x^2 + 1) / ((x - 1)^2 * (x + 2))", "Integrate (x^2 + 1)/((x - 1)^2 * (x + 2)) dx using partial fractions"),
        ("(3*x^2 + x + 1) / (x * (x^2 + 1))", "Evaluate \\int (3*x^2 + x + 1)/(x*(x^2 + 1)) dx using irreducible partial fractions"),
        ("(5*x - 2) / ((x - 2)*(x + 3))", "Find the antiderivative of (5*x - 2)/((x - 2)*(x + 3)) dx using PFD"),
        ("1 / (x^2 - 5*x + 6)", "Integrate 1/(x^2 - 5*x + 6) dx by decomposing into partial fractions"),
        ("(x + 4) / (x * (x^2 + 4))", "Evaluate \\int (x + 4)/(x*(x^2 + 4)) dx using partial fractions"),
        ("(4*x^2 + 2*x - 1) / ((x - 1)*(x + 1)*(x + 2))", "Find \\int (4*x^2 + 2*x - 1)/((x - 1)*(x + 1)*(x + 2)) dx using partial fractions"),
    ]
    for expr, q in pfd_probs:
        entries.append(make_entry(q, "partial_fraction_integral", {"expr": expr}, "antiderivative"))
    entries.append(make_entry("Decompose into partial fractions and integrate", "partial_fraction_integral", {"expr": None}, "antiderivative", False, ["expr"]))

    # 6. long_division_integral (Part 1, #73 - #80)
    ld_probs = [
        ("(x^3 + 2*x^2 + 1) / (x + 1)", "Evaluate \\int (x^3 + 2*x^2 + 1)/(x + 1) dx using polynomial long division"),
        ("(x^4 + 1) / (x^2 + 1)", "Find \\int (x^4 + 1)/(x^2 + 1) dx using long division"),
        ("(2*x^3 - x + 4) / (x^2 - 1)", "Integrate (2*x^3 - x + 4)/(x^2 - 1) dx by polynomial division"),
        ("(x^2 + 3*x + 5) / (x + 2)", "Evaluate \\int (x^2 + 3*x + 5)/(x + 2) dx using long division"),
        ("(3*x^4 - 2*x^2 + 1) / (x^2 + 2)", "Find the antiderivative of (3*x^4 - 2*x^2 + 1)/(x^2 + 2) dx via long division"),
        ("(x^5) / (x^2 + 1)", "Integrate x^5 / (x^2 + 1) dx using polynomial long division"),
        ("(x^3 + x^2 - x + 2) / (x - 1)", "Evaluate \\int (x^3 + x^2 - x + 2)/(x - 1) dx using long division"),
        ("(2*x^4 + 3) / (x^2 + 4)", "Find \\int (2*x^4 + 3)/(x^2 + 4) dx using polynomial long division"),
    ]
    for expr, q in ld_probs:
        entries.append(make_entry(q, "long_division_integral", {"expr": expr}, "antiderivative"))
    entries.append(make_entry("Evaluate the improper rational integral using long division", "long_division_integral", {"expr": None}, "antiderivative", False, ["expr"]))

    # 7. rational_root_integral (Part 1, #81 - #85)
    rr_probs = [
        ("1 / (x^3 - 3*x^2 - x + 3)", "Evaluate \\int 1/(x^3 - 3*x^2 - x + 3) dx using rational root theorem"),
        ("(x + 1) / (x^3 - 4*x^2 + x + 6)", "Find \\int (x + 1)/(x^3 - 4*x^2 + x + 6) dx by finding rational roots of the denominator"),
        ("(2*x - 1) / (x^3 + x^2 - 4*x - 4)", "Integrate (2*x - 1)/(x^3 + x^2 - 4*x - 4) dx using rational root theorem"),
        ("1 / (x^3 - 7*x + 6)", "Evaluate \\int 1/(x^3 - 7*x + 6) dx by synthetic division and rational roots"),
        ("(3*x + 2) / (x^3 - 2*x^2 - 5*x + 6)", "Find \\int (3*x + 2)/(x^3 - 2*x^2 - 5*x + 6) dx using the rational root theorem"),
        ("1 / (x^3 - 6*x^2 + 11*x - 6)", "Integrate 1/(x^3 - 6*x^2 + 11*x - 6) dx using the rational root theorem"),
        ("x / (x^3 + 3*x^2 - x - 3)", "Evaluate \\int x/(x^3 + 3*x^2 - x - 3) dx using rational root theorem"),
        ("(x - 2) / (x^3 - 2*x^2 - x + 2)", "Find the antiderivative of (x - 2)/(x^3 - 2*x^2 - x + 2) dx using rational root theorem"),
    ]
    for expr, q in rr_probs:
        entries.append(make_entry(q, "rational_root_integral", {"expr": expr}, "antiderivative"))
    entries.append(make_entry("Find the roots using rational root theorem and integrate", "rational_root_integral", {"expr": None}, "antiderivative", False, ["expr"]))

    # 8. integration_by_parts (Part 2, #86 - #105)
    ibp_probs = [
        ("x * cos(x)", "Evaluate \\int x * cos(x) dx using integration by parts"),
        ("log(x)", "Find \\int ln(x) dx using integration by parts with ghost function"),
        ("atan(x)", "Integrate arctan(x) dx by parts"),
        ("x * exp(2*x)", "Evaluate \\int x * e^(2x) dx using integration by parts"),
        ("x * sin(3*x)", "Find the antiderivative of x * sin(3x) dx using IBP"),
        ("(x^2) * log(x)", "Integrate x^2 * ln(x) dx by parts"),
        ("asin(x)", "Evaluate \\int arcsin(x) dx using integration by parts"),
        ("x * sec(x)^2", "Find \\int x * sec(x)^2 dx using integration by parts"),
    ]
    for expr, q in ibp_probs:
        entries.append(make_entry(q, "integration_by_parts", {"expr": expr}, "antiderivative"))
    entries.append(make_entry("Evaluate the integral using integration by parts", "integration_by_parts", {"expr": None}, "antiderivative", False, ["expr"]))

    # 9. cyclic_ibp_integral (Part 2, #106 - #120)
    cyclic_probs = [
        ("exp(2*x) * sin(3*x)", "Evaluate \\int e^(2x) * sin(3x) dx using cyclic integration by parts"),
        ("exp(x) * cos(x)", "Find \\int e^x * cos(x) dx by cycling integration by parts"),
        ("exp(-x) * cos(2*x)", "Integrate e^(-x) * cos(2x) dx using cyclic IBP"),
        ("sec(x)**3", "Evaluate \\int sec^3(x) dx using cyclic integration by parts"),
        ("exp(3*x) * sin(4*x)", "Find \\int e^(3x) * sin(4x) dx using cyclic integration by parts"),
        ("exp(2*x) * cos(5*x)", "Integrate e^(2x) * cos(5x) dx by self-referential IBP"),
        ("exp(-2*x) * sin(x)", "Evaluate \\int e^(-2x) * sin(x) dx using cyclic integration by parts"),
        ("exp(x) * sin(2*x)", "Find the antiderivative of e^x * sin(2x) dx using cyclic IBP"),
    ]
    for expr, q in cyclic_probs:
        entries.append(make_entry(q, "cyclic_ibp_integral", {"expr": expr}, "antiderivative"))
    entries.append(make_entry("Evaluate using cyclic integration by parts", "cyclic_ibp_integral", {"expr": None}, "antiderivative", False, ["expr"]))

    # 10. tabular_ibp_integral (Part 2, #121 - #135)
    tab_probs = [
        ("(x^3) * exp(2*x)", "Evaluate \\int x^3 * e^(2x) dx using tabular integration by parts"),
        ("(x^4) * sin(x)", "Find \\int x^4 * sin(x) dx using the tabular method"),
        ("(x^3) * cos(2*x)", "Integrate x^3 * cos(2x) dx using tic-tac-toe integration"),
        ("(x^2 - 3*x + 2) * exp(-x)", "Evaluate \\int (x^2 - 3*x + 2) * e^(-x) dx using tabular integration"),
        ("(x^5) * exp(x)", "Find \\int x^5 * e^x dx by tabular IBP"),
        ("(x^4) * cos(3*x)", "Integrate x^4 * cos(3x) dx using tabular method"),
        ("(x^2) * exp(4*x)", "Evaluate \\int x^2 * e^(4x) dx using tabular integration by parts"),
        ("(x^3) * sin(2*x)", "Find the antiderivative of x^3 * sin(2x) dx using tic-tac-toe tabular method"),
    ]
    for expr, q in tab_probs:
        entries.append(make_entry(q, "tabular_ibp_integral", {"expr": expr}, "antiderivative"))
    entries.append(make_entry("Evaluate the polynomial-exponential integral using tabular integration", "tabular_ibp_integral", {"expr": None}, "antiderivative", False, ["expr"]))

    # 11. trig_power_reduction_integral (Part 2, #136 - #148)
    tpr_probs = [
        ("sin(x)**3 * cos(x)**2", "Evaluate \\int sin^3(x) * cos^2(x) dx using trig power reduction"),
        ("sin(x)**4", "Find \\int sin^4(x) dx using trigonometric power reduction"),
        ("cos(x)**5", "Integrate cos^5(x) dx using odd-power reduction"),
        ("tan(x)**3 * sec(x)**4", "Evaluate \\int tan^3(x) * sec^4(x) dx using trig identity reduction"),
        ("sin(x)**2 * cos(x)**4", "Find \\int sin^2(x) * cos^4(x) dx by half-angle reduction"),
        ("sec(x)**4", "Integrate sec^4(x) dx using trigonometric reduction"),
        ("cos(x)**4", "Evaluate \\int cos^4(x) dx using trig power reduction"),
        ("sin(x)**5", "Find the antiderivative of sin^5(x) dx using power reduction identities"),
    ]
    for expr, q in tpr_probs:
        entries.append(make_entry(q, "trig_power_reduction_integral", {"expr": expr}, "antiderivative"))
    entries.append(make_entry("Evaluate using trigonometric power reduction", "trig_power_reduction_integral", {"expr": None}, "antiderivative", False, ["expr"]))

    # 12. wallis_integral (Part 3, #149 - #165)
    wallis_probs = [
        ("sin(x)**6", "0", "pi/2", "Evaluate the definite integral of sin^6(x) from 0 to pi/2 using Wallis formula"),
        ("cos(x)**7", "0", "pi/2", "Find the integral of cos^7(x) from 0 to pi/2 using Wallis product formula"),
        ("sin(x)**8", "0", "pi/2", "Evaluate \\int_0^{pi/2} sin^8(x) dx using Wallis formula"),
        ("cos(x)**5", "0", "pi/2", "Find \\int_0^{pi/2} cos^5(x) dx by Wallis integral theorem"),
        ("sin(x)**4 * cos(x)**2", "0", "pi/2", "Evaluate the definite integral of sin^4(x) * cos^2(x) from 0 to pi/2 using Wallis formula"),
        ("cos(x)**9", "0", "pi/2", "Calculate \\int_0^{pi/2} cos^9(x) dx using Wallis formula"),
        ("sin(x)**10", "0", "pi/2", "Evaluate \\int_0^{pi/2} sin^10(x) dx using Wallis formula"),
        ("cos(x)**6", "0", "pi/2", "Find \\int_0^{pi/2} cos^6(x) dx using Wallis product formula"),
    ]
    for expr, low, upp, q in wallis_probs:
        entries.append(make_entry(q, "wallis_integral", {"expr": expr, "lower": low, "upper": upp}, "integral_value"))
    entries.append(make_entry("Evaluate the integral of sin^6(x) from 0 using Wallis formula", "wallis_integral", {"expr": "sin(x)^6", "lower": "0", "upper": None}, "integral_value", False, ["upper"]))

    # 13. product_to_sum_trig_integral (Part 3, #166 - #185)
    pts_probs = [
        ("sin(3*x) * cos(5*x)", "Evaluate \\int sin(3x) * cos(5x) dx using product-to-sum identities"),
        ("cos(2*x) * cos(4*x)", "Find \\int cos(2x) * cos(4x) dx using product-to-sum formula"),
        ("sin(4*x) * sin(6*x)", "Integrate sin(4x) * sin(6x) dx by product-to-sum trigonometric identity"),
        ("sin(5*x) * cos(x)", "Evaluate \\int sin(5x) * cos(x) dx using product-to-sum"),
        ("cos(3*x) * cos(7*x)", "Find the antiderivative of cos(3x) * cos(7x) dx using product-to-sum"),
        ("sin(2*x) * sin(3*x)", "Integrate sin(2x) * sin(3x) dx using product to sum formula"),
        ("cos(x) * cos(5*x)", "Evaluate \\int cos(x) * cos(5x) dx using product to sum"),
        ("sin(6*x) * cos(2*x)", "Find \\int sin(6x) * cos(2x) dx using product-to-sum identities"),
    ]
    for expr, q in pts_probs:
        entries.append(make_entry(q, "product_to_sum_trig_integral", {"expr": expr}, "antiderivative"))
    entries.append(make_entry("Evaluate using product to sum identities", "product_to_sum_trig_integral", {"expr": None}, "antiderivative", False, ["expr"]))

    # 14. weierstrass_substitution_integral (Part 3, #186 - #215)
    ws_probs = [
        ("1 / (1 + sin(x) + cos(x))", "Evaluate \\int 1/(1 + sin(x) + cos(x)) dx using the Weierstrass substitution"),
        ("1 / (3 + 5*cos(x))", "Find \\int 1/(3 + 5*cos(x)) dx using tangent half-angle substitution"),
        ("1 / (2 + sin(x))", "Integrate 1/(2 + sin(x)) dx using Weierstrass t = tan(x/2) substitution"),
        ("1 / (5 + 4*cos(x))", "Evaluate \\int 1/(5 + 4*cos(x)) dx by Weierstrass substitution"),
        ("1 / (1 - sin(x))", "Find \\int 1/(1 - sin(x)) dx using Weierstrass half-angle method"),
        ("1 / (3 - 2*cos(x) + sin(x))", "Integrate 1/(3 - 2*cos(x) + sin(x)) dx using Weierstrass substitution"),
        ("1 / (4 + 3*sin(x))", "Evaluate \\int 1/(4 + 3*sin(x)) dx using tangent half-angle substitution"),
        ("1 / (2 + cos(x))", "Find \\int 1/(2 + cos(x)) dx using Weierstrass substitution"),
    ]
    for expr, q in ws_probs:
        entries.append(make_entry(q, "weierstrass_substitution_integral", {"expr": expr}, "antiderivative"))
    entries.append(make_entry("Evaluate using Weierstrass substitution", "weierstrass_substitution_integral", {"expr": None}, "antiderivative", False, ["expr"]))

    # 15. radical_species_integral (Part 3, #216 - #265)
    rad_probs = [
        ("1 / (x + sqrt(x^2 + x + 1))", "Evaluate \\int 1/(x + sqrt(x^2 + x + 1)) dx using Euler substitution"),
        ("(x^2 - 1) / ((x^2 + 1) * sqrt(x^4 + 1))", "Find \\int (x^2 - 1)/((x^2 + 1)*sqrt(x^4 + 1)) dx using radical species substitution"),
        ("1 / (x * sqrt(x^2 + 2*x + 2))", "Integrate 1/(x * sqrt(x^2 + 2*x + 2)) dx using Euler's first substitution"),
        ("sqrt((1 - x)/(1 + x))", "Evaluate \\int sqrt((1 - x)/(1 + x)) dx using rationalizing radical substitution"),
        ("1 / ((x - 1) * sqrt(x^2 - 2*x - 3))", "Find \\int 1/((x - 1)*sqrt(x^2 - 2*x - 3)) dx using radical species method"),
        ("(x + 1) / sqrt(x^2 + 4*x + 13)", "Integrate (x + 1)/sqrt(x^2 + 4*x + 13) dx using radical substitution"),
        ("1 / (sqrt(x) + sqrt(x+1))", "Evaluate \\int 1/(sqrt(x) + sqrt(x+1)) dx using rationalizing radical substitution"),
        ("sqrt(x) / (1 + x**(1/3))", "Find \\int sqrt(x)/(1 + x^(1/3)) dx using radical species rationalizing substitution"),
    ]
    for expr, q in rad_probs:
        entries.append(make_entry(q, "radical_species_integral", {"expr": expr}, "antiderivative"))
    entries.append(make_entry("Integrate radical species without expression", "radical_species_integral", {"expr": None}, "antiderivative", False, ["expr"]))

    # 16. absolute_value_definite_integral (Part 4, #266 - #295)
    abs_probs = [
        ("abs(x^2 - 4)", "0", "3", "Evaluate the definite integral of |x^2 - 4| from 0 to 3"),
        ("abs(x - 1)", "-1", "3", "Find the value of \\int_{-1}^3 |x - 1| dx using absolute value split"),
        ("abs(2*x - 5)", "1", "4", "Evaluate the definite integral of |2x - 5| from 1 to 4"),
        ("abs(x^2 - 3*x + 2)", "0", "4", "Calculate \\int_0^4 |x^2 - 3*x + 2| dx by splitting at roots"),
        ("abs(x^3 - x)", "-2", "2", "Evaluate \\int_{-2}^2 |x^3 - x| dx using absolute value root decomposition"),
        ("abs(sin(x))", "0", "2*pi", "Find the integral of |sin(x)| from 0 to 2*pi"),
        ("abs(3*x - 6)", "0", "5", "Evaluate the definite integral of |3x - 6| from 0 to 5"),
        ("abs(x^2 - 1)", "-2", "2", "Calculate the definite integral of |x^2 - 1| from -2 to 2"),
    ]
    for expr, low, upp, q in abs_probs:
        entries.append(make_entry(q, "absolute_value_definite_integral", {"expr": expr, "lower": low, "upper": upp}, "integral_value"))
    entries.append(make_entry("Evaluate the integral of |x^2 - 4| from 0", "absolute_value_definite_integral", {"expr": "abs(x^2 - 4)", "lower": "0", "upper": None}, "integral_value", False, ["upper"]))

    # 17. se_one_integral (Part 4, #296 - #335)
    se_probs = [
        ("x^5 + cos(x)", "-2", "2", "Evaluate the definite integral of (x^5 + cos(x)) from -2 to 2 using S.E-One symmetry"),
        ("(x^3)/(x^4 + 1) + x^2", "-3", "3", "Find the value of \\int_{-3}^3 (x^3/(x^4 + 1) + x^2) dx using S.E-One"),
        ("x^7 * sin(x^2) + cos(x)", "-pi", "pi", "Evaluate \\int_{-pi}^pi (x^7 * sin(x^2) + cos(x)) dx using S.E-One symmetry property"),
        ("x^3 + 5", "-4", "4", "Calculate the integral of (x^3 + 5) from -4 to 4 using S.E-One"),
        ("x * exp(x^2) + sqrt(1 - x^2)", "-1", "1", "Evaluate \\int_{-1}^1 (x * e^(x^2) + sqrt(1 - x^2)) dx using S.E-One"),
        ("x^9 + 3*x^2 - 4", "-2", "2", "Find \\int_{-2}^2 (x^9 + 3*x^2 - 4) dx using S.E-One symmetry"),
        ("sin(x)**3 + cos(x)", "-pi/2", "pi/2", "Evaluate the definite integral of (sin(x)^3 + cos(x)) from -pi/2 to pi/2 using S.E-One"),
        ("x^5 * exp(x^2) + x^4", "-1", "1", "Calculate \\int_{-1}^1 (x^5 * e^(x^2) + x^4) dx using S.E-One symmetry"),
    ]
    for expr, low, upp, q in se_probs:
        entries.append(make_entry(q, "se_one_integral", {"expr": expr, "lower": low, "upper": upp}, "integral_value"))
    entries.append(make_entry("Evaluate using S.E-One symmetry from -2 to 2", "se_one_integral", {"expr": None, "lower": "-2", "upper": "2"}, "integral_value", False, ["expr"]))

    # 18. quad_root_trick_integral (Part 4, #336 - #399)
    quad_probs = [
        ("sqrt((x + 3)*(x + 4)*(x + 5)*(x + 6) + 1)", "Evaluate \\int sqrt((x + 3)*(x + 4)*(x + 5)*(x + 6) + 1) dx using the quad-root trick"),
        ("sqrt((x + 1)*(x + 2)*(x + 3)*(x + 4) + 1)", "Find \\int sqrt((x + 1)*(x + 2)*(x + 3)*(x + 4) + 1) dx using the quad root product trick"),
        ("sqrt((x - 1)*x*(x + 1)*(x + 2) + 1)", "Integrate sqrt((x - 1)*x*(x + 1)*(x + 2) + 1) dx using the quartic radicand trick"),
        ("sqrt((x + 2)*(x + 4)*(x + 6)*(x + 8) + 16)", "Evaluate \\int sqrt((x + 2)*(x + 4)*(x + 6)*(x + 8) + 16) dx using the quad-root trick"),
        ("sqrt((x - 2)*(x - 1)*x*(x + 1) + 1)", "Find the antiderivative of sqrt((x - 2)*(x - 1)*x*(x + 1) + 1) dx using the quad root trick"),
        ("sqrt((x + 5)*(x + 6)*(x + 7)*(x + 8) + 1)", "Integrate sqrt((x + 5)*(x + 6)*(x + 7)*(x + 8) + 1) dx using the quad-root factorization trick"),
        ("sqrt(x*(x + 1)*(x + 2)*(x + 3) + 1)", "Evaluate \\int sqrt(x*(x + 1)*(x + 2)*(x + 3) + 1) dx using the quad-root trick"),
        ("sqrt((x - 3)*(x - 2)*(x - 1)*x + 1)", "Find \\int sqrt((x - 3)*(x - 2)*(x - 1)*x + 1) dx using the quad root product trick"),
    ]
    for expr, q in quad_probs:
        entries.append(make_entry(q, "quad_root_trick_integral", {"expr": expr}, "antiderivative"))
    entries.append(make_entry("Evaluate the integral using the quad-root trick", "quad_root_trick_integral", {"expr": None}, "antiderivative", False, ["expr"]))

    return entries


def generate_way2_parametric():
    """Way 2: Parametric / Randomized Generalization engine across all 18 technique archetypes."""
    entries = []
    rng = random.Random(42)  # Deterministic seed for reproducibility

    # 1. pun_integral: (A*x + B) / (a*x^2 + b*x + c)
    for _ in range(12):
        A = rng.choice([1, 2, 3, 5, 7, 8])
        B = rng.choice([-7, -5, -3, -1, 1, 3, 4, 7, 9])
        b = rng.choice([2, 4, 6, 8])
        c = (b // 2) ** 2 + rng.choice([1, 4, 9, 16])  # guarantees positive discriminant for irreducible quadratic
        expr = f"({A}*x + {B})/(x^2 + {b}*x + {c})"
        q = f"Evaluate the integral of ({A}*x + {B})/(x^2 + {b}*x + {c}) dx using the P.U.N. method"
        entries.append(make_entry(q, "pun_integral", {"expr": expr}, "antiderivative"))

    # 2. root_manipulation_integral: (a*x + b) * (c*x + d)**(1/n) or /
    for _ in range(12):
        a = rng.choice([1, 2, 3])
        b = rng.choice([-3, -1, 1, 2, 5])
        c = rng.choice([1, 2, 3])
        d = rng.choice([1, 2, 3, 4, 5])
        if rng.random() < 0.5:
            expr = f"({a}*x + {b}) * sqrt({c}*x + {d})"
            q = f"Find the integral of ({a}*x + {b})*sqrt({c}*x + {d}) dx by manipulating the root"
        else:
            expr = f"({a}*x + {b}) / sqrt({c}*x + {d})"
            q = f"Evaluate \\int ({a}*x + {b})/sqrt({c}*x + {d}) dx by root manipulation substitution"
        entries.append(make_entry(q, "root_manipulation_integral", {"expr": expr}, "antiderivative"))

    # 3. inverted_quadratic_integral: 1 / (x^2 +- a^2) or u'(x)/(u(x)^2 +- a^2)
    for _ in range(12):
        a2 = rng.choice([1, 4, 9, 16, 25, 36, 49, 64, 81, 100])
        kind = rng.choice(["poly", "exp", "trig"])
        if kind == "poly":
            sign = rng.choice(["+", "-"])
            expr = f"1 / (x^2 {sign} {a2})"
            q = f"Evaluate \\int 1/(x^2 {sign} {a2}) dx using inverted quadratic standard form"
        elif kind == "exp":
            expr = f"exp(x) / (exp(2*x) + {a2})"
            q = f"Find \\int e^x / (e^(2x) + {a2}) dx using inverted quadratic form"
        else:
            expr = f"cos(x) / (sin(x)^2 + {a2})"
            q = f"Integrate cos(x)/(sin(x)^2 + {a2}) dx using inverted quadratic method"
        entries.append(make_entry(q, "inverted_quadratic_integral", {"expr": expr}, "antiderivative"))

    # 4. trig_substitution_integral: sqrt(a^2 - x^2), sqrt(x^2 + a^2), sqrt(x^2 - a^2)
    for _ in range(12):
        a = rng.choice([2, 3, 4, 5, 6, 7, 8])
        a2 = a * a
        pattern = rng.choice([
            (f"sqrt({a2} - x^2)", f"Evaluate \\int sqrt({a2} - x^2) dx using trigonometric substitution"),
            (f"1 / sqrt({a2} - x^2)", f"Find \\int 1/sqrt({a2} - x^2) dx by trig substitution"),
            (f"1 / (x^2 + {a2})**(3/2)", f"Integrate 1/(x^2 + {a2})^(3/2) dx using tangent trigonometric substitution"),
            (f"sqrt(x^2 - {a2}) / x", f"Evaluate \\int sqrt(x^2 - {a2})/x dx using secant trigonometric substitution"),
        ])
        entries.append(make_entry(pattern[1], "trig_substitution_integral", {"expr": pattern[0]}, "antiderivative"))

    # 5. partial_fraction_integral: (A*x + B) / ((x - r1)*(x - r2))
    for _ in range(12):
        r1, r2 = rng.sample([-4, -3, -2, -1, 1, 2, 3, 4, 5], 2)
        A = rng.choice([1, 2, 3, 4, 5])
        B = rng.choice([-5, -2, 1, 3, 7])
        expr = f"({A}*x + {B}) / ((x - {r1}) * (x - {r2}))"
        q = f"Evaluate \\int ({A}*x + {B})/((x - {r1})*(x - {r2})) dx using partial fractions"
        entries.append(make_entry(q, "partial_fraction_integral", {"expr": expr}, "antiderivative"))

    # 6. long_division_integral: (x^3 + ...)/(x + a) or (x^4 + ...)/(x^2 + a)
    for _ in range(12):
        deg = rng.choice([3, 4])
        a = rng.choice([1, 2, 3])
        c = rng.choice([1, 2, 3, 5])
        if deg == 3:
            expr = f"(x^3 + {c}*x + 1) / (x + {a})"
            q = f"Evaluate \\int (x^3 + {c}*x + 1)/(x + {a}) dx using polynomial long division"
        else:
            expr = f"(x^4 + {c}) / (x^2 + {a})"
            q = f"Find \\int (x^4 + {c})/(x^2 + {a}) dx using long division"
        entries.append(make_entry(q, "long_division_integral", {"expr": expr}, "antiderivative"))

    # 7. rational_root_integral: 1 / ((x - r1)(x - r2)(x - r3))
    for _ in range(12):
        r1, r2, r3 = rng.sample([-3, -2, -1, 1, 2, 3], 3)
        # expanded cubic
        e2 = -(r1 + r2 + r3)
        e1 = r1*r2 + r2*r3 + r3*r1
        e0 = -(r1 * r2 * r3)
        expr = f"1 / (x^3 + {e2}*x^2 + {e1}*x + {e0})"
        q = f"Evaluate \\int 1/(x^3 + {e2}*x^2 + {e1}*x + {e0}) dx using rational root theorem"
        entries.append(make_entry(q, "rational_root_integral", {"expr": expr}, "antiderivative"))

    # 8. integration_by_parts: x^k * f(x)
    for _ in range(12):
        k = rng.choice([1, 2])
        f_type = rng.choice(["sin", "cos", "exp", "log", "atan"])
        if f_type == "sin":
            c = rng.choice([1, 2, 3, 4])
            expr = f"(x^{k}) * sin({c}*x)" if k > 1 else f"x * sin({c}*x)"
            q = f"Evaluate \\int {expr} dx using integration by parts"
        elif f_type == "cos":
            c = rng.choice([1, 2, 3, 4])
            expr = f"(x^{k}) * cos({c}*x)" if k > 1 else f"x * cos({c}*x)"
            q = f"Find \\int {expr} dx using integration by parts"
        elif f_type == "exp":
            c = rng.choice([2, 3, -1, -2])
            expr = f"(x^{k}) * exp({c}*x)" if k > 1 else f"x * exp({c}*x)"
            q = f"Integrate {expr} dx using integration by parts"
        elif f_type == "log":
            expr = f"(x^{k}) * log(x)" if k > 1 else "x * log(x)"
            q = f"Evaluate \\int {expr} dx using integration by parts"
        else:
            expr = "atan(x)"
            q = "Find the antiderivative of arctan(x) dx using integration by parts"
        entries.append(make_entry(q, "integration_by_parts", {"expr": expr}, "antiderivative"))

    # 9. cyclic_ibp_integral: exp(a*x) * sin(b*x) or exp(a*x) * cos(b*x)
    for _ in range(12):
        a = rng.choice([-3, -2, -1, 1, 2, 3, 4])
        b = rng.choice([2, 3, 4, 5])
        trig = rng.choice(["sin", "cos"])
        expr = f"exp({a}*x) * {trig}({b}*x)"
        q = f"Evaluate \\int e^({a}x) * {trig}({b}x) dx using cyclic integration by parts"
        entries.append(make_entry(q, "cyclic_ibp_integral", {"expr": expr}, "antiderivative"))

    # 10. tabular_ibp_integral: x^n * exp(ax) or x^n * trig(ax)
    for _ in range(12):
        n = rng.choice([2, 3, 4, 5])
        target_f = rng.choice(["exp", "sin", "cos"])
        a = rng.choice([1, 2, 3, -1])
        if target_f == "exp":
            expr = f"(x^{n}) * exp({a}*x)"
            q = f"Evaluate \\int x^{n} * e^({a}x) dx using tabular integration by parts"
        elif target_f == "sin":
            expr = f"(x^{n}) * sin({abs(a)}*x)"
            q = f"Find \\int x^{n} * sin({abs(a)}x) dx using tabular method"
        else:
            expr = f"(x^{n}) * cos({abs(a)}*x)"
            q = f"Integrate x^{n} * cos({abs(a)}x) dx using tic-tac-toe tabular integration"
        entries.append(make_entry(q, "tabular_ibp_integral", {"expr": expr}, "antiderivative"))

    # 11. trig_power_reduction_integral: sin^m(x) * cos^n(x)
    for _ in range(12):
        m = rng.choice([2, 3, 4, 5, 6])
        n = rng.choice([0, 2, 3, 4])
        if n == 0:
            expr = f"sin(x)**{m}"
            q = f"Evaluate \\int sin^{m}(x) dx using trig power reduction"
        else:
            expr = f"sin(x)**{m} * cos(x)**{n}"
            q = f"Find the antiderivative of sin^{m}(x) * cos^{n}(x) dx using trigonometric power reduction"
        entries.append(make_entry(q, "trig_power_reduction_integral", {"expr": expr}, "antiderivative"))

    # 12. wallis_integral: sin^n(x) or cos^n(x) from 0 to pi/2
    for _ in range(12):
        n = rng.choice([3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        trig = rng.choice(["sin", "cos"])
        expr = f"{trig}(x)**{n}"
        q = f"Evaluate the definite integral of {trig}^{n}(x) from 0 to pi/2 using Wallis formula"
        entries.append(make_entry(q, "wallis_integral", {"expr": expr, "lower": "0", "upper": "pi/2"}, "integral_value"))

    # 13. product_to_sum_trig_integral: trig1(a*x) * trig2(b*x)
    for _ in range(12):
        a, b = rng.sample([1, 2, 3, 4, 5, 6, 7, 8], 2)
        combo = rng.choice([
            (f"sin({a}*x) * cos({b}*x)", f"Evaluate \\int sin({a}x) * cos({b}x) dx using product-to-sum identities"),
            (f"cos({a}*x) * cos({b}*x)", f"Find \\int cos({a}x) * cos({b}x) dx using product-to-sum formula"),
            (f"sin({a}*x) * sin({b}*x)", f"Integrate sin({a}x) * sin({b}x) dx by product-to-sum trigonometric identity"),
        ])
        entries.append(make_entry(combo[1], "product_to_sum_trig_integral", {"expr": combo[0]}, "antiderivative"))

    # 14. weierstrass_substitution_integral: 1 / (a + b*cos(x) + c*sin(x))
    for _ in range(12):
        a = rng.choice([2, 3, 4, 5])
        b = rng.choice([1, 2, 3])
        if rng.random() < 0.5:
            expr = f"1 / ({a} + {b}*cos(x))"
            q = f"Evaluate \\int 1/({a} + {b}*cos(x)) dx using the Weierstrass substitution"
        else:
            expr = f"1 / ({a} + {b}*sin(x))"
            q = f"Find \\int 1/({a} + {b}*sin(x)) dx using tangent half-angle substitution"
        entries.append(make_entry(q, "weierstrass_substitution_integral", {"expr": expr}, "antiderivative"))

    # 15. radical_species_integral
    for _ in range(12):
        c = rng.choice([1, 2, 3, 4, 5])
        if rng.random() < 0.5:
            expr = f"1 / (x + sqrt(x^2 + {c}))"
            q = f"Evaluate \\int 1/(x + sqrt(x^2 + {c})) dx using Euler substitution"
        else:
            expr = f"sqrt((1 - {c}*x)/(1 + {c}*x))"
            q = f"Find \\int sqrt((1 - {c}*x)/(1 + {c}*x)) dx using radical species rationalizing substitution"
        entries.append(make_entry(q, "radical_species_integral", {"expr": expr}, "antiderivative"))

    # 16. absolute_value_definite_integral: |ax + b| or |x^2 - c|
    for _ in range(12):
        if rng.random() < 0.5:
            a = rng.choice([1, 2, 3])
            b = rng.choice([2, 3, 4, 6])
            root = b / a
            low = int(root - 2)
            upp = int(root + 2)
            expr = f"abs({a}*x - {b})" if a > 1 else f"abs(x - {b})"
            q = f"Evaluate the definite integral of |{a}x - {b}| from {low} to {upp}"
            entries.append(make_entry(q, "absolute_value_definite_integral", {"expr": expr, "lower": str(low), "upper": str(upp)}, "integral_value"))
        else:
            c = rng.choice([1, 4, 9, 16])
            low = 0
            upp = int(c**0.5 + 2)
            expr = f"abs(x^2 - {c})"
            q = f"Evaluate the definite integral of |x^2 - {c}| from {low} to {upp}"
            entries.append(make_entry(q, "absolute_value_definite_integral", {"expr": expr, "lower": str(low), "upper": str(upp)}, "integral_value"))

    # 17. se_one_integral: [-a, a] with odd + even
    for _ in range(12):
        a = rng.choice([1, 2, 3, 4])
        odd_term = rng.choice(["x^3", "x^5", "x^7", "x * cos(x)", "sin(x)"])
        even_term = rng.choice(["cos(x)", "x^2", "x^4", "3", "5"])
        expr = f"{odd_term} + {even_term}"
        q = f"Evaluate the definite integral of ({odd_term} + {even_term}) from -{a} to {a} using S.E-One symmetry"
        entries.append(make_entry(q, "se_one_integral", {"expr": expr, "lower": f"-{a}", "upper": str(a)}, "integral_value"))

    # 18. quad_root_trick_integral: sqrt((x+k)(x+k+1)(x+k+2)(x+k+3) + 1)
    for _ in range(12):
        k = rng.choice([-3, -2, -1, 0, 1, 2, 3, 4, 5])
        f0 = "x" if k == 0 else (f"(x + {k})" if k > 0 else f"(x - {abs(k)})")
        f1 = "x" if k+1 == 0 else (f"(x + {k+1})" if k+1 > 0 else f"(x - {abs(k+1)})")
        f2 = "x" if k+2 == 0 else (f"(x + {k+2})" if k+2 > 0 else f"(x - {abs(k+2)})")
        f3 = "x" if k+3 == 0 else (f"(x + {k+3})" if k+3 > 0 else f"(x - {abs(k+3)})")
        expr = f"sqrt({f0}*{f1}*{f2}*{f3} + 1)"
        q = f"Evaluate \\int sqrt({f0}*{f1}*{f2}*{f3} + 1) dx using the quad-root trick"
        entries.append(make_entry(q, "quad_root_trick_integral", {"expr": expr}, "antiderivative"))

    return entries


def main():
    way1 = generate_way1_authentic()
    way2 = generate_way2_parametric()
    all_entries = way1 + way2

    print(f"Generated Way 1 (Authentic textbook): {len(way1)} entries")
    print(f"Generated Way 2 (Parametric variations): {len(way2)} entries")
    print(f"Total new entries: {len(all_entries)}")

    # Validation pass
    mismatch_count = 0
    for idx, e in enumerate(all_entries):
        user_msg = e["messages"][1]["content"]
        asst = json.loads(e["messages"][2]["content"])
        expected_template = asst["template"]
        assert expected_template in TEMPLATES, f"Template {expected_template} not registered in TEMPLATES!"
        if asst["is_complete"]:
            predicted = classify_problem(user_msg)
            if predicted != expected_template:
                print(f"Warning: classification mismatch at #{idx}: expected {expected_template}, got {predicted}")
                print(f"  User: {user_msg}")
                mismatch_count += 1

    print(f"Validation complete: {len(all_entries) - mismatch_count}/{len(all_entries)} complete classifications matched exactly ({mismatch_count} mismatches).")

    # Target file
    dataset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "verimath_finetune_dataset.jsonl"))
    print(f"Target dataset: {dataset_path}")

    # Read existing count
    with open(dataset_path, "r", encoding="utf-8") as f:
        existing_lines = f.readlines()
    print(f"Existing dataset lines: {len(existing_lines)}")

    # Dry-run or append
    if "--dry-run" in sys.argv:
        print("Dry run requested; not appending.")
        return

    print("Appending new entries to verimath_finetune_dataset.jsonl...")
    with open(dataset_path, "a", encoding="utf-8") as f:
        for e in all_entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")

    with open(dataset_path, "r", encoding="utf-8") as f:
        updated_lines = f.readlines()
    print(f"Updated dataset lines: {len(updated_lines)} (+{len(all_entries)})")
    print("Done! Dataset successfully updated.")

if __name__ == "__main__":
    main()
