"""
VeriMath — Book of Integrals Pages 152–201 & Complete Answer Key Dataset Expansion
=================================================================================
Two-Way instruction-tuning dataset expansion covering:
  - De Moivre's Roots Partial Fractions (#405, and x^n +- 1 archetypes)
  - Feynman's Technique / Differentiation Under the Integral Sign (#417, #423 - #426)
  - MacLaurin / Taylor Series Term-by-Term Integration (#427 - #432)
  - Dilogarithm Function Li_2 (#433 - #438 and foundational identities)
  - Authentic Mixed Integrals (#400 - #416)
  - Official Complete Answer Key Highlights (#1 - #216)

Pathway 1: Authentic textbook problems with literal technique attribution.
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

    # 1. De Moivre's Roots Partial Fractions (#405)
    demoivre_data = [
        ("1/(x^5 + 1)", "Evaluate the integral of 1/(x^5 + 1) dx using De Moivre's theorem for partial fractions"),
        ("1/(x^5 - 1)", "Find \\int 1/(x^5 - 1) dx using De Moivre's roots of unity decomposition"),
        ("1/(x^4 + 1)", "Integrate 1/(x^4 + 1) dx using complex roots partial fractions by De Moivre's theorem"),
        ("1/(x^6 + 1)", "Evaluate \\int 1/(x^6 + 1) dx using De Moivre's theorem to find denominator factors"),
        ("1/(x^3 - 1)", "Find \\int 1/(x^3 - 1) dx using De Moivre's roots of unity"),
        ("1/(x^7 + 1)", "Integrate 1/(x^7 + 1) dx using De Moivre's theorem for partial fractions"),
        ("1/(x^8 - 1)", "Evaluate \\int 1/(x^8 - 1) dx using De Moivre's roots of unity decomposition"),
        ("x/(x^4 + 1)", "Find \\int x/(x^4 + 1) dx using De Moivre's roots of unity"),
        ("x^2/(x^6 + 1)", "Integrate x^2/(x^6 + 1) dx using De Moivre's theorem for complex roots"),
        ("1/(x^4 + 4)", "Evaluate \\int 1/(x^4 + 4) dx using De Moivre's roots factorization"),
    ]
    for expr, q in demoivre_data:
        entries.append(make_entry(q, "demoivre_roots_integral", {"expr": expr}, "antiderivative"))
    entries.append(make_entry("Evaluate the integral using De Moivre's theorem for partial fractions", "demoivre_roots_integral", {"expr": None}, "antiderivative", False, ["expr"]))

    # 2. Feynman's Technique (#417, #423 - #426)
    feynman_data = [
        ("(x^2 - 1)/log(x)", "0", "1", "Evaluate the definite integral of (x^2 - 1)/ln(x) from 0 to 1 using Feynman's technique of differentiation under the integral sign"),
        ("(x^3 - 1)/log(x)", "0", "1", "Find the integral of (x^3 - 1)/ln(x) from 0 to 1 using Feynman's technique"),
        ("(x^4 - 1)/log(x)", "0", "1", "Evaluate \\int_0^1 (x^4 - 1)/ln(x) dx using differentiation under the integral sign"),
        ("(x^5 - 1)/log(x)", "0", "1", "Find \\int_0^1 (x^5 - 1)/ln(x) dx by Feynman's trick"),
        ("(atan(pi*x) - atan(2*x))/x", "0", "oo", "Evaluate \\int_0^\\infty (arctan(pi*x) - arctan(2*x))/x dx using Feynman's technique"),
        ("(atan(3*x) - atan(x))/x", "0", "oo", "Find \\int_0^\\infty (arctan(3*x) - arctan(x))/x dx using Feynman's technique of differentiation under the integral sign"),
        ("(atan(4*x) - atan(2*x))/x", "0", "oo", "Evaluate the definite integral of (arctan(4*x) - arctan(2*x))/x from 0 to oo using Feynman's technique"),
        ("log(x)/(1 + x^2)", "0", "oo", "Evaluate \\int_0^\\infty (ln(x)/(1 + x^2)) dx using Feynman's technique"),
        ("sin(x)/x", "0", "oo", "Find the Dirichlet integral \\int_0^\\infty (sin(x)/x) dx using Feynman's technique"),
        ("log(5 - 4*cos(x))", "0", "pi", "Evaluate \\int_0^\\pi ln(5 - 4*cos(x)) dx using Feynman's technique of differentiation under the integral sign"),
        ("log(1 - 2*alpha*cos(x) + alpha^2)", "0", "pi", "Evaluate \\int_0^\\pi ln(1 - 2*alpha*cos(x) + alpha^2) dx using differentiation under the integral sign"),
        ("(exp(-x) - exp(-2*x))/x", "0", "oo", "Evaluate \\int_0^\\infty (e^(-x) - e^(-2x))/x dx using Feynman's technique"),
        ("(exp(-2*x) - exp(-5*x))/x", "0", "oo", "Find the integral of (e^(-2x) - e^(-5x))/x from 0 to oo using Feynman's trick"),
    ]
    for expr, low, up, q in feynman_data:
        entries.append(make_entry(q, "feynman_technique_integral", {"expr": expr, "lower": low, "upper": up}, "integral_value"))
    entries.append(make_entry("Evaluate the integral from 0 to 1 using Feynman's technique", "feynman_technique_integral", {"expr": None, "lower": "0", "upper": "1"}, "integral_value", False, ["expr"]))

    # 3. Series Expansion Definite Integrals (#427 - #432)
    series_data = [
        ("sin(x)/x", "0", "1", "Evaluate the definite integral of sin(x)/x from 0 to 1 using MacLaurin series expansion"),
        ("log(1 + x)/x", "0", "1/2", "Find \\int_0^(1/2) (ln(1+x)/x) dx using MacLaurin series expansion"),
        ("atan(x)/x", "0", "0.3", "Evaluate the definite integral of arctan(x)/x from 0 to 0.3 using MacLaurin series expansion"),
        ("(exp(3*x) - 1)/(10*x)", "-1", "0", "Integrate (e^(3x) - 1)/(10x) from -1 to 0 using MacLaurin series expansion"),
        ("(1 - exp(-x))/x", "0", "1", "Evaluate the definite integral of (1 - e^(-x))/x from 0 to 1 using MacLaurin series expansion"),
        ("(sin(x) - 4)/x", "1/2", "pi/6", "Evaluate \\int_(1/2)^(pi/6) ((sin(x) - 4)/x) dx using MacLaurin series expansion"),
        ("(1 - cos(x))/x^2", "0", "1", "Evaluate the definite integral of (1 - cos(x))/x^2 from 0 to 1 using MacLaurin series expansion"),
        ("(exp(x) - 1)/x", "0", "1", "Find \\int_0^1 ((e^x - 1)/x) dx using MacLaurin series expansion"),
        ("sin(x^2)", "0", "1", "Evaluate \\int_0^1 sin(x^2) dx using MacLaurin series expansion"),
        ("cos(x^2)", "0", "1", "Find the definite integral of cos(x^2) from 0 to 1 using MacLaurin series expansion"),
        ("exp(-x^2)", "0", "1", "Evaluate \\int_0^1 e^(-x^2) dx using MacLaurin series expansion"),
        ("(1 - cos(2*x))/x^2", "0", "1", "Find \\int_0^1 (1 - cos(2x))/x^2 dx using MacLaurin series expansion"),
    ]
    for expr, low, up, q in series_data:
        entries.append(make_entry(q, "series_expansion_definite_integral", {"expr": expr, "lower": low, "upper": up}, "integral_value"))
    entries.append(make_entry("Evaluate the definite integral from 0 to 1 using MacLaurin series expansion", "series_expansion_definite_integral", {"expr": None, "lower": "0", "upper": "1"}, "integral_value", False, ["expr"]))

    # 4. Dilogarithm Function (#433 - #438)
    dilog_data = [
        ("log(1 - exp(-x))", "0", "oo", "Evaluate the definite integral of ln(1 - exp(-x)) from 0 to oo using the dilogarithm function"),
        ("log((exp(x) - 1)/(exp(x) + 1))", "0", "oo", "Evaluate \\int_0^\\infty ln((e^x - 1)/(e^x + 1)) dx using the dilogarithm function"),
        ("log(1 + exp(-x))", "0", "oo", "Find \\int_0^\\infty ln(1 + e^(-x)) dx using the dilogarithm function"),
        ("log(2^x - 1) - log(2^x)", "0", "oo", "Evaluate \\int_0^\\infty (ln(2^x - 1) - ln(2^x)) dx using the dilogarithm function"),
        ("atan(3*x)/x", "0", "1", "Evaluate the integral of arctan(3x)/x dx using the dilogarithm function"),
        ("log(1 - x)/x", "0", "1", "Find the definite integral of ln(1-x)/x from 0 to 1 using the dilogarithm function"),
        ("log(1 + x)/x", "0", "1", "Evaluate \\int_0^1 (ln(1+x)/x) dx using the dilogarithm function"),
        ("log(1 - x)/x", "0", "1/2", "Find \\int_0^(1/2) (ln(1-x)/x) dx using the dilogarithm function"),
        ("x * cot(x)", "0", "pi/2", "Evaluate \\int_0^(pi/2) x*cot(x) dx using the dilogarithm function"),
        ("asin(x)/x", "0", "1", "Find \\int_0^1 (arcsin(x)/x) dx using the dilogarithm function"),
    ]
    for expr, low, up, q in dilog_data:
        entries.append(make_entry(q, "dilogarithm_integral", {"expr": expr, "lower": low, "upper": up}, "integral_value"))
    entries.append(make_entry("Evaluate the integral from 0 to oo using the dilogarithm function", "dilogarithm_integral", {"expr": None, "lower": "0", "upper": "oo"}, "integral_value", False, ["expr"]))

    # 5. Authentic Mixed Integrals (#400 - #416)
    mixed_data = [
        ("(1 - x)*(1 - 2*x)*(1 - 3*x)", "Evaluate \\int (1-x)(1-2x)(1-3x) dx", "indefinite_integral"),
        ("x^2 / (1 - x)^100", "Evaluate \\int x^2 / (1-x)^100 dx", "indefinite_integral"),
        ("(sin(x)*cos(x)) / sqrt(3 - sin(x)^4)", "Find the integral of sin(x)*cos(x)/sqrt(3 - sin^4(x)) dx", "indefinite_integral"),
        ("(x^4 - 5*x^3 + 6*x^2 - 18)/(x^3 - 3*x^2)", "Evaluate \\int (x^4 - 5*x^3 + 6*x^2 - 18)/(x^3 - 3*x^2) dx using polynomial long division", "long_division_integral"),
        ("sin(log(x))^2", "0", "1", "Evaluate the definite integral of sin^2(ln(x)) from 0 to 1", "definite_integral"),
        ("(x^2 + 4)/(3*x^3 + 4*x^2 - 4*x)", "Find \\int (x^2 + 4)/(3*x^3 + 4*x^2 - 4*x) dx using partial fractions", "partial_fraction_integral"),
        ("(6*x - 1)/(4*x^2 - 8*x + 1)", "Evaluate \\int (6*x - 1)/(4*x^2 - 8*x + 1) dx using the P.U.N. method", "pun_integral"),
        ("1/(x^2 + 2*x + 5)", "Integrate 1/(x^2 + 2*x + 5) dx using inverted quadratic", "inverted_quadratic_integral"),
        ("x*sqrt(x^2 + cos(x))", "-5", "5", "Evaluate the definite integral of x*sqrt(x^2 + cos(x)) from -5 to 5 using S.E-One symmetry", "se_one_integral"),
        ("cot(x)*(1 - cos(2*x))", "Find \\int cot(x)*(1 - cos(2x)) dx", "indefinite_integral"),
        ("(5*x + 1 - x^3)/exp(2*x)", "Evaluate \\int (5*x + 1 - x^3)/e^(2x) dx using tabular integration by parts", "tabular_ibp_integral"),
        ("4*x*exp(x)*sin(x)", "Integrate 4*x*e^x*sin(x) dx using integration by parts", "integration_by_parts"),
        ("sqrt(3*x - x^2)", "Find \\int sqrt(3x - x^2) dx using trig substitution", "trig_substitution_integral"),
        ("cos(x)^2 / (cos(x)^2 + 4*sin(x)^2)", "0", "pi/2", "Evaluate the definite integral of cos^2(x)/(cos^2(x) + 4*sin^2(x)) from 0 to pi/2 using King's rule", "kings_rule_integral"),
        ("(2*x^3 - x^2 + 4*x + 34)/(x^4 - 6*x^2 - 8*x + 24)", "Evaluate \\int (2*x^3 - x^2 + 4*x + 34)/(x^4 - 6*x^2 - 8*x + 24) dx using rational root theorem", "rational_root_integral"),
        ("(2*x^3 - 2*x^2 + 8*x + 30)/(x^4 - 6*x^2 - 8*x + 24)", "Find \\int (2*x^3 - 2*x^2 + 8*x + 30)/(x^4 - 6*x^2 - 8*x + 24) dx using rational root theorem", "rational_root_integral"),
    ]
    for item in mixed_data:
        if len(item) == 3:
            expr, q, tmpl = item
            entries.append(make_entry(q, tmpl, {"expr": expr}, "antiderivative"))
        else:
            expr, low, up, q, tmpl = item
            entries.append(make_entry(q, tmpl, {"expr": expr, "lower": low, "upper": up}, "integral_value"))

    # 6. Official Complete Answer Key Highlights (#1 - #216)
    key_highlights = [
        ("16*x - 8*x^(5/6) + x^(2/3)", "Evaluate \\int (16*x - 8*x^(5/6) + x^(2/3)) dx", "indefinite_integral"),
        ("x^(5/4) - 6*x^2", "Integrate (x^(5/4) - 6*x^2) dx", "indefinite_integral"),
        ("x^4 + 2*x^2 + 1 + x^(3/2) + x^(1/2)", "Find \\int (x^4 + 2*x^2 + 1 + x^(3/2) + x^(1/2)) dx", "indefinite_integral"),
        ("x^12 + 3*x^8 + 3*x^4 + 1", "Evaluate \\int (x^12 + 3*x^8 + 3*x^4 + 1) dx", "indefinite_integral"),
        ("(x^2 - 3*x + 1)/x^(1/3)", "Integrate (x^2 - 3*x + 1)/x^(1/3) dx", "indefinite_integral"),
        ("(2*x + 1)/(x^2 + x + 7)", "Evaluate \\int (2*x + 1)/(x^2 + x + 7) dx using u-substitution", "indefinite_integral"),
        ("cos(x)*sin(x)^4", "Find \\int cos(x)*sin^4(x) dx using u-substitution", "indefinite_integral"),
        ("exp(tan(x))*sec(x)^2", "Integrate e^(tan(x))*sec^2(x) dx using u-substitution", "indefinite_integral"),
        ("1/(x^2 + 9)", "Evaluate \\int 1/(x^2 + 9) dx using inverted quadratic", "inverted_quadratic_integral"),
        ("1/(x^2 - 16)", "Find \\int 1/(x^2 - 16) dx using inverted quadratic", "inverted_quadratic_integral"),
        ("1/sqrt(25 - x^2)", "Evaluate \\int 1/sqrt(25 - x^2) dx using trig substitution", "trig_substitution_integral"),
        ("sqrt(16 - x^2)", "Integrate sqrt(16 - x^2) dx using trig substitution", "trig_substitution_integral"),
        ("1/(x^2 + 6*x + 13)", "Evaluate \\int 1/(x^2 + 6*x + 13) dx using inverted quadratic", "inverted_quadratic_integral"),
        ("1/(x^2 - 4*x - 5)", "Find \\int 1/(x^2 - 4*x - 5) dx using partial fractions", "partial_fraction_integral"),
        ("x*exp(3*x)", "Integrate x*e^(3x) dx using integration by parts", "integration_by_parts"),
        ("x^2 * sin(x)", "Evaluate \\int x^2 * sin(x) dx using tabular integration by parts", "tabular_ibp_integral"),
        ("sin(x)^3", "Integrate sin^3(x) dx using trig power reduction", "trig_power_reduction_integral"),
        ("cos(x)^4", "Evaluate \\int cos^4(x) dx using trig power reduction", "trig_power_reduction_integral"),
        ("sin(x)^6", "0", "pi/2", "Evaluate \\int_0^(pi/2) sin^6(x) dx using Wallis formula", "wallis_integral"),
        ("cos(x)^7", "0", "pi/2", "Find \\int_0^(pi/2) cos^7(x) dx using Wallis formula", "wallis_integral"),
        ("1/(3 + 5*cos(x))", "Evaluate \\int 1/(3 + 5*cos(x)) dx using Weierstrass substitution", "weierstrass_substitution_integral"),
        ("1/(2 + sin(x))", "Find \\int 1/(2 + sin(x)) dx using Weierstrass substitution", "weierstrass_substitution_integral"),
    ]
    for item in key_highlights:
        if len(item) == 3:
            expr, q, tmpl = item
            entries.append(make_entry(q, tmpl, {"expr": expr}, "antiderivative"))
        else:
            expr, low, up, q, tmpl = item
            entries.append(make_entry(q, tmpl, {"expr": expr, "lower": low, "upper": up}, "integral_value"))

    return entries

def generate_way2():
    entries = []
    rng = random.Random(42)

    # 1. Parametric De Moivre roots
    for _ in range(25):
        n = rng.choice([3, 4, 5, 6, 7, 8])
        sign = rng.choice(["+", "-"])
        a = rng.choice([1, 2])
        const = a**n
        expr = f"1/(x^{n} {sign} {const})"
        q = f"Evaluate \\int 1/(x^{n} {sign} {const}) dx using De Moivre's theorem for partial fractions"
        entries.append(make_entry(q, "demoivre_roots_integral", {"expr": expr}, "antiderivative"))

    for _ in range(15):
        n = rng.choice([4, 6, 8])
        m = rng.choice([1, 2])
        expr = f"x^{m} / (x^{n} + 1)"
        q = f"Integrate x^{m}/(x^{n} + 1) dx using De Moivre's roots of unity decomposition"
        entries.append(make_entry(q, "demoivre_roots_integral", {"expr": expr}, "antiderivative"))

    # 2. Parametric Feynman Technique
    for _ in range(25):
        a = rng.choice([2, 3, 4, 5, 6, 7, 8])
        expr = f"(x^{a} - 1)/log(x)"
        q = f"Evaluate the definite integral of (x^{a} - 1)/ln(x) from 0 to 1 using Feynman's technique of differentiation under the integral sign"
        entries.append(make_entry(q, "feynman_technique_integral", {"expr": expr, "lower": "0", "upper": "1"}, "integral_value"))

    for _ in range(20):
        a, b = rng.sample([1, 2, 3, 4, 5, "pi"], 2)
        expr = f"(atan({a}*x) - atan({b}*x))/x"
        q = f"Evaluate \\int_0^\\infty (arctan({a}*x) - arctan({b}*x))/x dx using Feynman's technique"
        entries.append(make_entry(q, "feynman_technique_integral", {"expr": expr, "lower": "0", "upper": "oo"}, "integral_value"))

    for _ in range(15):
        a, b = rng.sample([1, 2, 3, 4], 2)
        expr = f"(exp(-{a}*x) - exp(-{b}*x))/x"
        q = f"Find \\int_0^\\infty (e^(-{a}x) - e^(-{b}x))/x dx using Feynman's trick of differentiation under the integral sign"
        entries.append(make_entry(q, "feynman_technique_integral", {"expr": expr, "lower": "0", "upper": "oo"}, "integral_value"))

    for _ in range(15):
        k = rng.choice([2, 3, 4, 5])
        expr = f"log({k**2 + 1} - {2*k}*cos(x))"
        q = f"Evaluate the definite integral of ln({k**2 + 1} - {2*k}*cos(x)) from 0 to pi using Feynman's technique"
        entries.append(make_entry(q, "feynman_technique_integral", {"expr": expr, "lower": "0", "upper": "pi"}, "integral_value"))

    # 3. Parametric Series Expansion Definite Integrals
    for _ in range(25):
        k = rng.choice([1, 2, 3, 4])
        b = rng.choice(["1", "0.5", "1/2", "0.2"])
        expr = f"(1 - cos({k}*x))/x^2" if k > 1 else "(1 - cos(x))/x^2"
        q = f"Evaluate the definite integral of {expr} from 0 to {b} using MacLaurin series expansion"
        entries.append(make_entry(q, "series_expansion_definite_integral", {"expr": expr, "lower": "0", "upper": b}, "integral_value"))

    for _ in range(20):
        k = rng.choice([1, 2, 3, 4])
        b = rng.choice(["1", "0.5", "1/2"])
        expr = f"sin({k}*x)/x" if k > 1 else "sin(x)/x"
        q = f"Find \\int_0^{b} ({expr}) dx using MacLaurin series expansion"
        entries.append(make_entry(q, "series_expansion_definite_integral", {"expr": expr, "lower": "0", "upper": b}, "integral_value"))

    for _ in range(20):
        k = rng.choice([1, 2, 3])
        b = rng.choice(["0.5", "1/2", "0.3", "1"])
        expr = f"log(1 + {k}*x)/x" if k > 1 else "log(1 + x)/x"
        q = f"Evaluate the definite integral of {expr} from 0 to {b} using MacLaurin series expansion"
        entries.append(make_entry(q, "series_expansion_definite_integral", {"expr": expr, "lower": "0", "upper": b}, "integral_value"))

    for _ in range(20):
        k = rng.choice([1, 2, 3])
        b = rng.choice(["1", "0.5", "1/2"])
        expr = f"(exp({k}*x) - 1)/x" if k > 1 else "(exp(x) - 1)/x"
        q = f"Integrate ({expr}) from 0 to {b} using MacLaurin series expansion"
        entries.append(make_entry(q, "series_expansion_definite_integral", {"expr": expr, "lower": "0", "upper": b}, "integral_value"))

    # 4. Parametric Dilogarithm Integrals
    for _ in range(25):
        k = rng.choice([1, 2, 3, 4])
        expr = f"log(1 - exp(-{k}*x))" if k > 1 else "log(1 - exp(-x))"
        q = f"Evaluate \\int_0^\\infty {expr} dx using the dilogarithm function"
        entries.append(make_entry(q, "dilogarithm_integral", {"expr": expr, "lower": "0", "upper": "oo"}, "integral_value"))

    for _ in range(20):
        k = rng.choice([1, 2, 3])
        expr = f"log(1 + exp(-{k}*x))" if k > 1 else "log(1 + exp(-x))"
        q = f"Find the definite integral of {expr} from 0 to oo using the dilogarithm function"
        entries.append(make_entry(q, "dilogarithm_integral", {"expr": expr, "lower": "0", "upper": "oo"}, "integral_value"))

    for _ in range(15):
        k = rng.choice([1, 2])
        b = rng.choice(["1", "1/2", "0.5"])
        expr = f"log(1 - {k}*x)/x" if k > 1 else "log(1 - x)/x"
        q = f"Evaluate \\int_0^{b} ({expr}) dx using the dilogarithm function"
        entries.append(make_entry(q, "dilogarithm_integral", {"expr": expr, "lower": "0", "upper": b}, "integral_value"))

    # 5. Additional Parametric Answer Key Archetypes
    for _ in range(25):
        a = rng.choice([2, 3, 4, 5])
        b = rng.choice([1, 2, 3])
        expr = f"1/(x^2 + {a**2})"
        q = f"Evaluate \\int 1/(x^2 + {a**2}) dx using inverted quadratic"
        entries.append(make_entry(q, "inverted_quadratic_integral", {"expr": expr}, "antiderivative"))

    for _ in range(20):
        a = rng.choice([2, 3, 4, 5])
        expr = f"1/sqrt({a**2} - x^2)"
        q = f"Evaluate \\int 1/sqrt({a**2} - x^2) dx using trig substitution"
        entries.append(make_entry(q, "trig_substitution_integral", {"expr": expr}, "antiderivative"))

    for _ in range(20):
        a = rng.choice([1, 2, 3, 4])
        b = rng.choice([1, 2, 3, 4])
        expr = f"(x + {a})/(x^2 + {2*b}*x + {b**2 + 4})"
        q = f"Evaluate \\int (x + {a})/(x^2 + {2*b}*x + {b**2 + 4}) dx using the P.U.N. method"
        entries.append(make_entry(q, "pun_integral", {"expr": expr}, "antiderivative"))

    return entries

def main():
    print("Generating Two-Way final book dataset expansion...")
    w1 = generate_way1()
    print(f"Way 1 (Authentic Book of Integrals #400–#438 & Key #1–#216): {len(w1)} examples")
    w2 = generate_way2()
    print(f"Way 2 (Parametric Climax Variations): {len(w2)} examples")

    total = w1 + w2
    print(f"Total new examples to append: {len(total)}")

    out_path = os.path.join(os.path.dirname(__file__), "..", "verimath_finetune_dataset.jsonl")
    initial_count = 0
    if os.path.exists(out_path):
        with open(out_path, "r", encoding="utf-8") as f:
            initial_count = sum(1 for _ in f)

    with open(out_path, "a", encoding="utf-8") as f:
        for entry in total:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    with open(out_path, "r", encoding="utf-8") as f:
        final_count = sum(1 for _ in f)

    print(f"Initial dataset size: {initial_count}")
    print(f"Appended: {len(total)}")
    print(f"Final dataset size: {final_count}")

if __name__ == "__main__":
    main()
