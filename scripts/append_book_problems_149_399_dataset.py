"""
VeriMath — Book of Integrals Problems #149–#399 Two-Way Dataset Generator
========================================================================
Extracts and generates instruction-tuning pairs covering:
  - Rational Root Theorem (#149 - #156)
  - P.U.N. Integrals (#157 - #166)
  - Integration by Parts & Ghost Functions (#167 - #187)
  - Cyclic Integration by Parts (#188 - #192)
  - Tabular / Tic-Tac-Toe (#193 - #200)
  - Trig Power Reduction (#201 - #216)
  - Wallis Integrals (#217 - #219)
  - Product to Sum (#220 - #223)
  - Weierstrass Substitution (#224 - #235)
  - Radical Species & Euler Substitutions (#236 - #244)
  - Fundamental Theorem of Calculus (#245 - #251)
  - Absolute Value Definite Integrals (#252 - #257, #336)
  - King's Rule Contest Integrals (#258 - #265, #296)
  - S.E-One Symmetry Method (#266 - #269, #329)
  - Quad-Root Product Trick (#380)
  - Euler's Formula Integration (#364, #372, #373)
  - PFD Linear Power Ratio Trick (#310, #311, #347)
  - Conjugate Radical Rationalizing (#381, #395)
  - Nested Infinite Radicals (#397)
  - Exponential Derivative Sum Rule (#393)

Pathway 1: Authentic textbook problem formulations.
Pathway 2: Parametric / randomized generalization variations.
"""

import json
import os
import random
import sys

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

def generate_way1():
    entries = []

    # 1. Rational Root Theorem (#149-#156)
    rr_data = [
        ("(6*x^2 - 10*x + 8)/(5*x^3 + 29*x^2 + 19*x - 5)", "Evaluate the integral of (6*x^2 - 10*x + 8)/(5*x^3 + 29*x^2 + 19*x - 5) dx using rational root theorem"),
        ("(7*x^2 + 33*x + 32)/(x^3 + 4*x^2 + x - 6)", "Find \\int (7*x^2 + 33*x + 32)/(x^3 + 4*x^2 + x - 6) dx by factoring with the rational root theorem"),
        ("(x^2 - 12*x + 10)/(-2*x^3 + x^2 - 8*x + 4)", "Integrate (x^2 - 12*x + 10)/(-2*x^3 + x^2 - 8*x + 4) dx using rational root theorem"),
        ("(x^2 + 14*x - 5)/(x^3 + 9*x^2 - 21*x - 2)", "Find \\int (x^2 + 14*x - 5)/(x^3 + 9*x^2 - 21*x - 2) dx using rational root theorem"),
        ("(26*x^3 + 51*x^2 + 13*x - 6)/(5*x^4 + 9*x^3 + 3*x^2 - x)", "Integrate (26*x^3 + 51*x^2 + 13*x - 6)/(5*x^4 + 9*x^3 + 3*x^2 - x) dx using rational root theorem"),
        ("(7*x^2 + 14*x - 1)/(3*x^3 + 11*x^2 + 5*x - 3)", "Evaluate \\int (7*x^2 + 14*x - 1)/(3*x^3 + 11*x^2 + 5*x - 3) dx using rational root theorem"),
    ]
    for expr, q in rr_data:
        entries.append(make_entry(q, "rational_root_integral", {"expr": expr}, "antiderivative"))
    entries.append(make_entry("Evaluate the polynomial quotient using the rational root theorem", "rational_root_integral", {"expr": None}, "antiderivative", False, ["expr"]))

    # 2. PUN Integrals (#157-#166, #270, #370)
    pun_data = [
        ("(6*x - 4)/(3*x^2 - 9*x + 1)", "Evaluate \\int (6*x - 4)/(3*x^2 - 9*x + 1) dx using the P.U.N. method"),
        ("(x - 3)/(2*x^2 + x + 8)", "Integrate (x - 3)/(2*x^2 + x + 8) dx using the PUN method"),
        ("(5*x + 1)/(x^2 + x + 4)", "Find the integral of (5*x + 1)/(x^2 + x + 4) dx using the P.U.N. method"),
        ("(7*x + 2)/(3*x^2 + 5*x + 4)", "Evaluate \\int (7*x + 2)/(3*x^2 + 5*x + 4) dx by the PUN method"),
        ("(3*x - 3)/(x^2 + 5*x + 15)", "Integrate (3*x - 3)/(x^2 + 5*x + 15) dx using P.U.N. method"),
        ("(6*x - 1)/(x^2 + 10*x + 26)", "Find \\int (6*x - 1)/(x^2 + 10*x + 26) dx using the PUN method"),
        ("(2*x + 5)/(x^2 - 3*x + 100)", "Evaluate \\int (2*x + 5)/(x^2 - 3*x + 100) dx using the P.U.N. method"),
        ("(4*x + 5)/(5*x^2 - 20*x + 1)", "Integrate (4*x + 5)/(5*x^2 - 20*x + 1) dx using the PUN method"),
        ("(x - 7)/(8*x^2 + 3*x - 1)", "Evaluate \\int (x - 7)/(8*x^2 + 3*x - 1) dx by the P.U.N. method"),
        ("(3*x - 1)/(4*x^2 - 4*x + 17)", "Find \\int (3*x - 1)/(4*x^2 - 4*x + 17) dx using the PUN method"),
    ]
    for expr, q in pun_data:
        entries.append(make_entry(q, "pun_integral", {"expr": expr}, "antiderivative"))

    # 3. Integration by Parts & Ghost Functions (#167-#187, #282, #309)
    ibp_data = [
        ("x * cos(x)", "Evaluate \\int x * cos(x) dx using integration by parts"),
        ("x^3 * log(x)", "Find \\int x^3 * ln(x) dx using integration by parts"),
        ("sin(x) * log(cos(x))", "Integrate sin(x) * ln(cos(x)) dx using integration by parts"),
        ("4*x * cos(6*x - 1)", "Evaluate \\int 4x * cos(6x - 1) dx using integration by parts"),
        ("asin(x)", "Find \\int arcsin(x) dx using integration by parts with ghost function"),
        ("log(x)", "Integrate ln(x) dx using integration by parts with ghost function"),
        ("atan(x)", "Evaluate \\int arctan(x) dx using integration by parts with ghost function"),
        ("acos(x)", "Find \\int arccos(x) dx using integration by parts with ghost function"),
        ("log(x^2 + 1)", "Evaluate \\int ln(x^2 + 1) dx using integration by parts with ghost function"),
        ("log(x^2 + 2*x - 3)", "Integrate ln(x^2 + 2x - 3) dx using integration by parts with ghost function"),
        ("log(3*x^2 + x + 1)", "Find \\int ln(3x^2 + x + 1) dx using integration by parts with ghost function"),
        ("log(x^2 - 1)", "Evaluate \\int ln(x^2 - 1) dx using integration by parts with ghost function"),
        ("log(x^2 + 4)", "Integrate ln(x^2 + 4) dx using integration by parts with ghost function"),
        ("log(1 + x)", "Evaluate \\int ln(1 + x) dx using integration by parts with ghost function"),
        ("log(x) / x^2", "Find \\int (ln(x)/x^2) dx using integration by parts"),
    ]
    for expr, q in ibp_data:
        entries.append(make_entry(q, "integration_by_parts", {"expr": expr}, "antiderivative"))

    # 4. Cyclic IBP (#188-#192)
    cyclic_data = [
        ("exp(x) * cos(x)", "Evaluate \\int e^x * cos(x) dx using cyclic integration by parts"),
        ("exp(2*x) * sin(x)", "Find \\int e^(2x) * sin(x) dx using cyclic integration by parts"),
        ("exp(2*x) * cos(6*x + 2)", "Integrate e^(2x) * cos(6x + 2) dx using cyclic integration by parts"),
        ("sec(x)^3", "Evaluate \\int sec^3(x) dx using cyclic integration by parts"),
        ("exp(3*x) * sin(x)", "Find \\int e^(3x) * sin(x) dx using cyclic integration by parts"),
    ]
    for expr, q in cyclic_data:
        entries.append(make_entry(q, "cyclic_ibp_integral", {"expr": expr}, "antiderivative"))

    # 5. Tabular / Tic-Tac-Toe (#193-#200, #356, #396)
    tab_data = [
        ("x^4 * cos(2*x)", "Evaluate \\int x^4 * cos(2x) dx using tabular integration by parts"),
        ("x^4 * exp(2*x)", "Find \\int x^4 * e^(2x) dx using the tabular method"),
        ("(x^2 + 1) * sin(2*x)", "Integrate (x^2 + 1) * sin(2x) dx using tic-tac-toe tabular integration"),
        ("(2*x)^3 * cos(2*x)", "Evaluate \\int (2x)^3 * cos(2x) dx using tabular integration"),
        ("(2*x + 1)^3 * exp(x)", "Find \\int (2x + 1)^3 * e^x dx by tabular IBP"),
        ("x^10 * sin(x)", "Integrate x^10 * sin(x) dx using tabular integration by parts"),
        ("8*x^2 * sin(2*x + 1)", "Evaluate \\int 8x^2 * sin(2x + 1) dx using tabular integration"),
        ("x^3 * sin(4*x)", "Find \\int x^3 * sin(4x) dx using tabular integration by parts"),
        ("x^4 * sin(2*x)", "Integrate x^4 * sin(2x) dx using tabular integration by parts"),
    ]
    for expr, q in tab_data:
        entries.append(make_entry(q, "tabular_ibp_integral", {"expr": expr}, "antiderivative"))

    # 6. Trig Power Reduction (#201-#216, #291, #314)
    tpr_data = [
        ("sin(x)^6 * cos(x)^3", "Evaluate \\int sin^6(x) * cos^3(x) dx using trig power reduction"),
        ("sin(x)^5 * cos(x)^2", "Find \\int sin^5(x) * cos^2(x) dx using trigonometric power reduction"),
        ("sin(x)^5 * cos(x)^3", "Integrate sin^5(x) * cos^3(x) dx using odd-power reduction"),
        ("sin(x)^4", "Evaluate \\int sin^4(x) dx using trigonometric power reduction"),
        ("cos(2*x)^2", "Find \\int cos^2(2x) dx using half-angle power reduction"),
        ("tan(x)^3 * sec(x)", "Integrate tan^3(x) * sec(x) dx using trig reduction"),
        ("tan(x)^5", "Evaluate \\int tan^5(x) dx using trigonometric power reduction"),
        ("tan(x)^5 * sec(x)^4", "Find \\int tan^5(x) * sec^4(x) dx using trig identity reduction"),
        ("sec(x)^6", "Integrate sec^6(x) dx using trigonometric reduction"),
        ("sec(x)^4", "Evaluate \\int sec^4(x) dx using trig power reduction"),
        ("tan(4*x - 1)^2", "Find \\int tan^2(4x - 1) dx using trigonometric reduction"),
        ("sin(x)^6 * cos(x)^5", "Integrate sin^6(x) * cos^5(x) dx using odd-power reduction"),
    ]
    for expr, q in tpr_data:
        entries.append(make_entry(q, "trig_power_reduction_integral", {"expr": expr}, "antiderivative"))

    # 7. Wallis Integrals (#217-#219)
    wallis_data = [
        ("cos(x)^3", "0", "pi/2", "Evaluate the definite integral of cos^3(x) from 0 to pi/2 using Wallis formula"),
        ("sin(x)^2", "0", "pi/2", "Find the integral of sin^2(x) from 0 to pi/2 using Wallis product formula"),
        ("cos(x)^7", "0", "pi/2", "Evaluate \\int_0^{pi/2} cos^7(x) dx using Wallis formula"),
    ]
    for expr, low, upp, q in wallis_data:
        entries.append(make_entry(q, "wallis_integral", {"expr": expr, "lower": low, "upper": upp}, "integral_value"))

    # 8. Product to Sum (#220-#223)
    pts_data = [
        ("sin(3*x) * cos(2*x)", "Evaluate \\int sin(3x) * cos(2x) dx using product-to-sum identities"),
        ("cos(-3*x) * cos(4*x)", "Find \\int cos(-3x) * cos(4x) dx using product-to-sum formula"),
        ("sin(x) * sin(3*x)", "Integrate sin(x) * sin(3x) dx by product-to-sum trigonometric identity"),
        ("cos(3*x) * sin(-4*x)", "Evaluate \\int cos(3x) * sin(-4x) dx using product-to-sum"),
    ]
    for expr, q in pts_data:
        entries.append(make_entry(q, "product_to_sum_trig_integral", {"expr": expr}, "antiderivative"))

    # 9. Weierstrass Substitution (#224-#235)
    ws_data = [
        ("1 / (1 + cos(x) + sin(x))", "Evaluate \\int 1/(1 + cos(x) + sin(x)) dx using the Weierstrass substitution"),
        ("1 / (2 + cos(x))", "Find \\int 1/(2 + cos(x)) dx using tangent half-angle substitution"),
        ("3 / (5 - 4*cos(x))", "Integrate 3/(5 - 4*cos(x)) dx using Weierstrass substitution"),
        ("6 / (3 - 2*sin(x))", "Evaluate \\int 6/(3 - 2*sin(x)) dx using Weierstrass t = tan(x/2) substitution"),
        ("1 / (sin(x) + cos(x))", "Find \\int 1/(sin(x) + cos(x)) dx using Weierstrass substitution"),
        ("1 / (5*sin(x) + 12*cos(x))", "Evaluate \\int 1/(5*sin(x) + 12*cos(x)) dx using tangent half-angle substitution"),
        ("1 / (5*sin(x) + 2*cos(x) + 2)", "Integrate 1/(5*sin(x) + 2*cos(x) + 2) dx using the Weierstrass substitution"),
        ("1 / (4 + 5*cos(x/2))", "Evaluate \\int 1/(4 + 5*cos(x/2)) dx using tangent half-angle substitution"),
    ]
    for expr, q in ws_data:
        entries.append(make_entry(q, "weierstrass_substitution_integral", {"expr": expr}, "antiderivative"))

    # 10. Radical Species & Euler Substitutions (#236-#244)
    rad_data = [
        ("1 / ((2*x + 3)*sqrt(x + 1))", "Evaluate \\int 1/((2x+3)*sqrt(x+1)) dx using radical species substitution"),
        ("1 / ((x - 1)*sqrt(x^2 - 3))", "Find \\int 1/((x-1)*sqrt(x^2-3)) dx using radical species method"),
        ("1 / ((x + 1)^2 * sqrt(x^2 + 2*x + 2))", "Integrate 1/((x+1)^2*sqrt(x^2+2x+2)) dx using Euler substitution"),
        ("1 / ((x^2 - 3*x + 1)*sqrt(4*x + 1))", "Evaluate \\int 1/((x^2-3x+1)*sqrt(4x+1)) dx using radical species substitution"),
        ("1 / ((x - 4)*sqrt(x^2 - x + 3))", "Find \\int 1/((x-4)*sqrt(x^2-x+3)) dx using Euler substitution"),
        ("1 / ((x^2 + 1)*sqrt(x^2 + 5))", "Integrate 1/((x^2+1)*sqrt(x^2+5)) dx using radical species method"),
        ("(x^2 - 1) / ((x^2 + 1)*sqrt(x^4 + 1))", "Evaluate \\int (x^2 - 1)/((x^2 + 1)*sqrt(x^4 + 1)) dx using radical species substitution"),
        ("1 / ((x + 3)*sqrt(x^2 - 2*x + 5))", "Find \\int 1/((x+3)*sqrt(x^2-2x+5)) dx using radical species method"),
    ]
    for expr, q in rad_data:
        entries.append(make_entry(q, "radical_species_integral", {"expr": expr}, "antiderivative"))

    # 11. Absolute Value Definite Integrals (#252-#257, #336)
    abs_data = [
        ("abs(x^2 + 2*x - 15)", "-2", "10", "Evaluate the definite integral of |x^2 + 2x - 15| from -2 to 10"),
        ("abs(-x^2 + 3*x + 1)", "-2", "6", "Find the value of \\int_{-2}^6 |-x^2 + 3x + 1| dx using absolute value split"),
        ("abs(exp(x - 2) - 4)", "0", "5", "Evaluate the definite integral of |e^(x-2) - 4| from 0 to 5"),
        ("abs(x/3 - 2)", "-3", "5", "Calculate \\int_{-3}^5 |(1/3)x - 2| dx by splitting at roots"),
        ("abs(x^2 - 4*x - 8)", "-3", "5", "Evaluate \\int_{-3}^5 |x^2 - 4x - 8| dx using absolute value root decomposition"),
        ("abs(x^2 - 4*x - 32)", "0", "10", "Find the integral of |x^2 - 4x - 32| from 0 to 10"),
        ("abs(x^2 - 7*x - 18)", "-5", "10", "Evaluate the definite integral of |x^2 - 7x - 18| from -5 to 10"),
    ]
    for expr, low, upp, q in abs_data:
        entries.append(make_entry(q, "absolute_value_definite_integral", {"expr": expr, "lower": low, "upper": upp}, "integral_value"))

    # 12. King's Rule (#258-#265, #296)
    kings_data = [
        ("log(1 + tan(x))", "0", "pi/4", "Evaluate the definite integral of ln(1 + tan(x)) from 0 to pi/4 using King's rule"),
        ("1 / (1 + tan(x)**pi)", "0", "pi/2", "Find the integral of 1/(1 + (tan(x))^pi) from 0 to pi/2 using King's property"),
        ("1 / (4 + 2^x)", "0", "4", "Evaluate \\int_0^4 1/(4 + 2^x) dx using King's rule"),
        ("1 / (1 + exp(sin(x)))", "0", "2*pi", "Calculate \\int_0^{2*pi} 1/(1 + e^(sin(x))) dx using King's property"),
        ("x*sin(x) / (1 + cos(x)^2)", "0", "pi", "Evaluate \\int_0^pi (x*sin(x))/(1 + cos^2(x)) dx using King's rule"),
        ("log((1 + sin(x))/(1 + cos(x)))", "0", "pi/2", "Find \\int_0^{pi/2} ln((1 + sin(x))/(1 + cos(x))) dx using King's rule"),
        ("x / (cos(x)^2 + 9*sin(x)^2)", "0", "pi", "Evaluate the definite integral of x/(cos^2(x) + 9*sin^2(x)) from 0 to pi using King's rule"),
        ("log(1 + x) / (1 + x^2)", "0", "1", "Evaluate \\int_0^1 ln(1+x)/(1+x^2) dx using King's rule"),
    ]
    for expr, low, upp, q in kings_data:
        entries.append(make_entry(q, "kings_rule_integral", {"expr": expr, "lower": low, "upper": upp}, "integral_value"))

    # 13. S.E-One Symmetry (#266-#269, #329)
    se_data = [
        ("x^4 / (exp(x) + 1)", "-2", "2", "Evaluate the definite integral of x^4/(e^x + 1) from -2 to 2 using S.E-One symmetry"),
        ("x*sin(x) / (2^x + 1)", "-pi", "pi", "Find the value of \\int_{-pi}^pi (x*sin(x))/(2^x + 1) dx using S.E-One"),
        ("sqrt(x^2 + 1) / (3^x + 1)", "-pi/4", "pi/4", "Evaluate \\int_{-pi/4}^{pi/4} sqrt(x^2 + 1)/(3^x + 1) dx using S.E-One symmetry property"),
        ("(x^4 + x^2 + 1) / (exp(x) + 1)", "-10", "10", "Calculate the integral of (x^4 + x^2 + 1)/(e^x + 1) from -10 to 10 using S.E-One"),
        ("cos(x) / (6^x + 1)", "-pi/4", "pi/4", "Evaluate \\int_{-pi/4}^{pi/4} cos(x)/(6^x + 1) dx using S.E-One symmetry"),
    ]
    for expr, low, upp, q in se_data:
        entries.append(make_entry(q, "se_one_integral", {"expr": expr, "lower": low, "upper": upp}, "integral_value"))

    # 14. Quad-Root Trick (#380)
    quad_data = [
        ("sqrt((x + 3)*(x + 4)*(x + 5)*(x + 6) + 1)", "Evaluate \\int sqrt((x + 3)*(x + 4)*(x + 5)*(x + 6) + 1) dx using the quad-root trick"),
        ("sqrt((x - 1)*x*(x + 1)*(x + 2) + 1)", "Find \\int sqrt((x - 1)*x*(x + 1)*(x + 2) + 1) dx using the quad root product trick"),
        ("sqrt((x + 2)*(x + 3)*(x + 4)*(x + 5) + 1)", "Integrate sqrt((x + 2)*(x + 3)*(x + 4)*(x + 5) + 1) dx using the quad-root trick"),
    ]
    for expr, q in quad_data:
        entries.append(make_entry(q, "quad_root_trick_integral", {"expr": expr}, "antiderivative"))

    # 15. Euler's Formula Integration (#364, #372, #373)
    euler_data = [
        ("exp(3*x) * sin(x)", "Integrate e^(3x) * sin(x) dx using Euler's formula"),
        ("exp(7*x) * cos(x)", "Evaluate \\int e^(7x) * cos(x) dx using Euler's formula"),
        ("exp(x) * cos(7*x)", "Find \\int e^x * cos(7x) dx by Euler's formula"),
        ("exp(2*x) * sin(4*x)", "Integrate e^(2x) * sin(4x) dx using Euler's formula"),
        ("exp(-x) * cos(3*x)", "Evaluate \\int e^(-x) * cos(3x) dx using Euler's formula"),
    ]
    for expr, q in euler_data:
        entries.append(make_entry(q, "euler_formula_integral", {"expr": expr}, "antiderivative"))
    entries.append(make_entry("Evaluate the integral using Euler's formula", "euler_formula_integral", {"expr": None}, "antiderivative", False, ["expr"]))

    # 16. PFD Linear Power Ratio Trick (#310, #311, #347)
    pfd_trick_data = [
        ("1 / ((x + 3)^2 * (x - 6)^3)", "Evaluate \\int 1/((x + 3)^2 * (x - 6)^3) dx using the PFD linear power trick"),
        ("1 / ((x + 7)^2 * (x - 8)^3)", "Find \\int 1/((x + 7)^2 * (x - 8)^3) dx using the linear power trick"),
        ("1 / ((x - 1)^2 * (x + 1)^5)", "Integrate 1/((x - 1)^2 * (x + 1)^5) dx using the PFD linear power trick"),
        ("1 / ((x + 2)^3 * (x - 4)^2)", "Evaluate \\int 1/((x + 2)^3 * (x - 4)^2) dx using the PFD trick"),
    ]
    for expr, q in pfd_trick_data:
        entries.append(make_entry(q, "pfd_linear_power_trick_integral", {"expr": expr}, "antiderivative"))
    entries.append(make_entry("Integrate using the PFD linear power trick", "pfd_linear_power_trick_integral", {"expr": None}, "antiderivative", False, ["expr"]))

    # 17. Conjugate Radical Rationalizing (#381, #395)
    conj_data = [
        ("1 / (sqrt(3*x + 4) + sqrt(2*x + 1))", "Evaluate \\int 1/(sqrt(3x+4) + sqrt(2x+1)) dx using conjugate radical method"),
        ("1 / (sqrt(1 + x) - sqrt(x))", "Find \\int 1/(sqrt(1+x) - sqrt(x)) dx by conjugate radical rationalization"),
        ("1 / (sqrt(5*x + 2) + sqrt(5*x - 3))", "Integrate 1/(sqrt(5x+2) + sqrt(5x-3)) dx using conjugate radical method"),
        ("1 / (sqrt(x + 4) + sqrt(x))", "Evaluate \\int 1/(sqrt(x+4) + sqrt(x)) dx using conjugate radical rationalization"),
    ]
    for expr, q in conj_data:
        entries.append(make_entry(q, "conjugate_radical_integral", {"expr": expr}, "antiderivative"))
    entries.append(make_entry("Evaluate using the conjugate radical method", "conjugate_radical_integral", {"expr": None}, "antiderivative", False, ["expr"]))

    # 18. Nested Infinite Radicals (#397)
    nested_data = [
        ("x", "Integrate sqrt(x*sqrt(x*sqrt(x...))) dx using the nested radical simplification"),
        ("x", "Evaluate \\int \\sqrt{x\\sqrt{x\\sqrt{x\\dots}}} dx using infinite radical simplification"),
        ("x", "Find the antiderivative of sqrt(x*sqrt(x*sqrt(x*sqrt(x...)))) dx using nested radical identity"),
    ]
    for expr, q in nested_data:
        entries.append(make_entry(q, "nested_infinite_radical_integral", {"expr": expr}, "antiderivative"))
    entries.append(make_entry("Evaluate the infinitely nested radical", "nested_infinite_radical_integral", {"expr": None}, "antiderivative", False, ["expr"]))

    # 19. Exponential Derivative Sum (#393)
    exp_sum_data = [
        ("exp(x) * ((1 - sin(x))/(1 - cos(x)))", "Evaluate \\int e^x * ((1 - sin(x))/(1 - cos(x))) dx using the exponential derivative sum rule"),
        ("exp(x) * (1/x - 1/x^2)", "Find \\int e^x * (1/x - 1/x^2) dx using the exponential derivative sum rule"),
        ("exp(x) * (tan(x) + sec(x)^2)", "Integrate e^x * (tan(x) + sec^2(x)) dx using the exponential derivative sum rule"),
        ("exp(x) * (sin(x) + cos(x))", "Evaluate \\int e^x * (sin(x) + cos(x)) dx using exponential derivative sum rule"),
    ]
    for expr, q in exp_sum_data:
        entries.append(make_entry(q, "exp_derivative_sum_integral", {"expr": expr}, "antiderivative"))
    entries.append(make_entry("Evaluate using the exponential derivative sum rule", "exp_derivative_sum_integral", {"expr": None}, "antiderivative", False, ["expr"]))

    return entries


def generate_way2():
    entries = []
    rng = random.Random(1337)

    # 1. Euler's formula variations: e^(ax) * (sin(bx) or cos(bx))
    for _ in range(12):
        a = rng.choice([-3, -2, -1, 1, 2, 3, 4, 5])
        b = rng.choice([2, 3, 4, 5, 6])
        trig = rng.choice(["sin", "cos"])
        expr = f"exp({a}*x) * {trig}({b}*x)"
        q = f"Evaluate \\int e^({a}x) * {trig}({b}x) dx using Euler's formula"
        entries.append(make_entry(q, "euler_formula_integral", {"expr": expr}, "antiderivative"))

    # 2. PFD Linear power trick variations: 1/((x+a)^m * (x+b)^n)
    for _ in range(12):
        a, b = rng.sample([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5], 2)
        m = rng.choice([2, 3])
        n = rng.choice([2, 3])
        sa = f"(x + {a})" if a > 0 else (f"(x - {abs(a)})" if a < 0 else "x")
        sb = f"(x + {b})" if b > 0 else (f"(x - {abs(b)})" if b < 0 else "x")
        expr = f"1 / ({sa}^{m} * {sb}^{n})"
        q = f"Evaluate \\int 1/({sa}^{m} * {sb}^{n}) dx using the PFD linear power trick"
        entries.append(make_entry(q, "pfd_linear_power_trick_integral", {"expr": expr}, "antiderivative"))

    # 3. Conjugate radical variations: 1/(sqrt(ax+b) +- sqrt(cx+d))
    for _ in range(12):
        a = rng.choice([1, 2, 3, 4])
        b = rng.choice([1, 2, 3, 4, 5])
        c = rng.choice([1, 2, 3, 4])
        d = rng.choice([1, 2, 3, 4, 5])
        sign = rng.choice(["+", "-"])
        expr = f"1 / (sqrt({a}*x + {b}) {sign} sqrt({c}*x + {d}))"
        q = f"Evaluate \\int 1/(sqrt({a}x+{b}) {sign} sqrt({c}x+{d})) dx using conjugate radical method"
        entries.append(make_entry(q, "conjugate_radical_integral", {"expr": expr}, "antiderivative"))

    # 4. Nested infinite radical variations
    for _ in range(8):
        dots = rng.choice(["...", "....", "\\dots"])
        q = f"Evaluate \\int sqrt(x*sqrt(x*sqrt(x{dots}))) dx using the nested radical simplification"
        entries.append(make_entry(q, "nested_infinite_radical_integral", {"expr": "x"}, "antiderivative"))

    # 5. Exponential derivative sum variations: e^x * (f + f')
    for _ in range(12):
        pair = rng.choice([
            ("1/x - 1/x^2", "1/x - 1/x^2"),
            ("tan(x) + sec(x)^2", "tan(x) + sec(x)^2"),
            ("sin(x) + cos(x)", "sin(x) + cos(x)"),
            ("log(x) + 1/x", "log(x) + 1/x"),
            ("x^2 + 2*x", "x^2 + 2*x"),
            ("x^3 + 3*x^2", "x^3 + 3*x^2"),
        ])
        expr = f"exp(x) * ({pair[0]})"
        q = f"Evaluate \\int e^x * ({pair[0]}) dx using the exponential derivative sum rule"
        entries.append(make_entry(q, "exp_derivative_sum_integral", {"expr": expr}, "antiderivative"))

    # 6. Additional PUN variations: (Ax + B)/(ax^2 + bx + c)
    for _ in range(12):
        A = rng.choice([2, 3, 4, 6, 8])
        B = rng.choice([-9, -4, 2, 5, 11])
        b = rng.choice([2, 4, 6, 8, 10])
        c = (b // 2)**2 + rng.choice([1, 4, 9, 25])
        expr = f"({A}*x + {B})/(x^2 + {b}*x + {c})"
        q = f"Find the integral of ({A}*x + {B})/(x^2 + {b}*x + {c}) dx using the P.U.N. method"
        entries.append(make_entry(q, "pun_integral", {"expr": expr}, "antiderivative"))

    # 7. Additional S.E-One variations: [-a, a]
    for _ in range(12):
        a = rng.choice([1, 2, 3, 4, 5])
        odd = rng.choice(["x^3", "x^5", "x^7", "x*cos(x)"])
        base = rng.choice([2, 3, "e"])
        k_str = f"{base}^x + 1" if base != "e" else "exp(x) + 1"
        even = rng.choice(["x^2", "x^4", "cos(x)", "1"])
        expr = f"({even}) / ({k_str})"
        q = f"Evaluate the definite integral of ({even})/({k_str}) from -{a} to {a} using S.E-One symmetry"
        entries.append(make_entry(q, "se_one_integral", {"expr": expr, "lower": f"-{a}", "upper": str(a)}, "integral_value"))

    # 8. Additional King's Rule variations
    for _ in range(12):
        combo = rng.choice([
            ("x*sin(x) / (1 + cos(x)^2)", "0", "pi"),
            ("1 / (1 + tan(x)**3)", "0", "pi/2"),
            ("1 / (1 + tan(x)**5)", "0", "pi/2"),
            ("x / (cos(x)^2 + 4*sin(x)^2)", "0", "pi"),
        ])
        q = f"Evaluate the definite integral of {combo[0]} from {combo[1]} to {combo[2]} using King's rule"
        entries.append(make_entry(q, "kings_rule_integral", {"expr": combo[0], "lower": combo[1], "upper": combo[2]}, "integral_value"))

    # 9. Additional Quad-root variations
    for _ in range(12):
        k = rng.choice([-4, -2, 1, 3, 6])
        f0 = f"(x + {k})" if k > 0 else (f"(x - {abs(k)})" if k < 0 else "x")
        f1 = f"(x + {k+1})" if k+1 > 0 else (f"(x - {abs(k+1)})" if k+1 < 0 else "x")
        f2 = f"(x + {k+2})" if k+2 > 0 else (f"(x - {abs(k+2)})" if k+2 < 0 else "x")
        f3 = f"(x + {k+3})" if k+3 > 0 else (f"(x - {abs(k+3)})" if k+3 < 0 else "x")
        expr = f"sqrt({f0}*{f1}*{f2}*{f3} + 1)"
        q = f"Evaluate \\int sqrt({f0}*{f1}*{f2}*{f3} + 1) dx using the quad-root trick"
        entries.append(make_entry(q, "quad_root_trick_integral", {"expr": expr}, "antiderivative"))

    # 10. Additional Tabular variations
    for _ in range(10):
        n = rng.choice([3, 4, 5])
        a = rng.choice([2, 3, -1])
        trig = rng.choice(["sin", "cos", "exp"])
        if trig == "exp":
            expr = f"x^{n} * exp({a}*x)"
            q = f"Evaluate \\int x^{n} * e^({a}x) dx using tabular integration by parts"
        elif trig == "sin":
            expr = f"x^{n} * sin({abs(a)}*x)"
            q = f"Find \\int x^{n} * sin({abs(a)}x) dx using tabular method"
        else:
            expr = f"x^{n} * cos({abs(a)}*x)"
            q = f"Integrate x^{n} * cos({abs(a)}x) dx using tic-tac-toe tabular integration"
        entries.append(make_entry(q, "tabular_ibp_integral", {"expr": expr}, "antiderivative"))

    # 11. Additional Cyclic variations
    for _ in range(10):
        a = rng.choice([-2, -1, 1, 2, 3])
        b = rng.choice([2, 3, 4, 5])
        trig = rng.choice(["sin", "cos"])
        expr = f"exp({a}*x) * {trig}({b}*x)"
        q = f"Evaluate \\int e^({a}x) * {trig}({b}x) dx using cyclic integration by parts"
        entries.append(make_entry(q, "cyclic_ibp_integral", {"expr": expr}, "antiderivative"))

    # 12. Additional Trig Power Reduction variations
    for _ in range(10):
        m = rng.choice([3, 5, 7])
        n = rng.choice([2, 4])
        expr = f"sin(x)^{m} * cos(x)^{n}"
        q = f"Evaluate \\int sin^{m}(x) * cos^{n}(x) dx using trig power reduction"
        entries.append(make_entry(q, "trig_power_reduction_integral", {"expr": expr}, "antiderivative"))

    # 13. Additional Product to Sum variations
    for _ in range(10):
        a, b = rng.sample([2, 3, 4, 5, 6, 7], 2)
        combo = rng.choice([
            (f"sin({a}*x) * cos({b}*x)", f"Evaluate \\int sin({a}x) * cos({b}x) dx using product-to-sum identities"),
            (f"cos({a}*x) * cos({b}*x)", f"Find \\int cos({a}x) * cos({b}x) dx using product-to-sum formula"),
            (f"sin({a}*x) * sin({b}*x)", f"Integrate sin({a}x) * sin({b}x) dx by product-to-sum trigonometric identity"),
        ])
        entries.append(make_entry(combo[1], "product_to_sum_trig_integral", {"expr": combo[0]}, "antiderivative"))

    # 14. Additional Weierstrass variations
    for _ in range(10):
        a = rng.choice([3, 4, 5])
        b = rng.choice([1, 2])
        if rng.random() < 0.5:
            expr = f"1 / ({a} + {b}*cos(x))"
            q = f"Evaluate \\int 1/({a} + {b}*cos(x)) dx using the Weierstrass substitution"
        else:
            expr = f"1 / ({a} + {b}*sin(x))"
            q = f"Find \\int 1/({a} + {b}*sin(x)) dx using tangent half-angle substitution"
        entries.append(make_entry(q, "weierstrass_substitution_integral", {"expr": expr}, "antiderivative"))

    return entries


def main():
    way1 = generate_way1()
    way2 = generate_way2()
    all_entries = way1 + way2

    print(f"Generated Way 1 (Authentic textbook #149-#399): {len(way1)} entries")
    print(f"Generated Way 2 (Parametric variations): {len(way2)} entries")
    print(f"Total new entries: {len(all_entries)}")

    # Validation pass
    mismatch_count = 0
    for idx, e in enumerate(all_entries):
        user_msg = e["messages"][1]["content"]
        asst = json.loads(e["messages"][2]["content"])
        expected_template = asst["template"]
        assert expected_template in TEMPLATES, f"Template {expected_template} not registered!"
        if asst["is_complete"]:
            predicted = classify_problem(user_msg)
            if predicted != expected_template:
                print(f"Mismatch at #{idx}: expected {expected_template}, got {predicted}")
                print(f"  User: {user_msg}")
                mismatch_count += 1

    print(f"Validation: {len(all_entries) - mismatch_count}/{len(all_entries)} complete classifications matched exactly ({mismatch_count} mismatches).")

    dataset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "verimath_finetune_dataset.jsonl"))
    print(f"Target dataset: {dataset_path}")

    with open(dataset_path, "r", encoding="utf-8") as f:
        existing_lines = f.readlines()
    print(f"Existing dataset lines: {len(existing_lines)}")

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
    print("Dataset expansion successfully appended!")

if __name__ == "__main__":
    main()
