"""
VeriMath — Reference 2: Book of 1000 Derivatives (Chapter 1 & Rules) Dataset Generator
====================================================================================
Grounds the training dataset in Miguel Santiago's "Book of 1000 Derivatives":
  - Reference Rules (Pages 1–3):
      * Power Rule + Sum/Difference Rules
      * Trig Derivatives (sin, cos, tan, sec, csc, cot)
      * Exponential & Logarithmic Derivatives (e^x, a^x, ln(x), log_a(x))
      * Product Rule, Quotient Rule, Chain Rule
  - Chapter 1: Authentic Problems #1–#18:
      #1:  y = x^6 - 5x^2 + 1                  -> 6x^5 - 10x
      #2:  y = 5x^4 - sqrt(x)                 -> 20x^3 - 1/(2*sqrt(x))
      #3:  y = 6*x^(1/3) + x^2                -> 2/x^(2/3) + 2x
      #4:  y = 4x^2 - 10x + 14                -> 8x - 10
      #5:  y = 3/x^2 + 1/x                    -> -6/x^3 - 1/x^2
      #6:  y = 5x^3 - x^2 + 12x - 1000        -> 15x^2 - 2x + 12
      #7:  y = x^(3/5) + x                    -> 3/(5*x^(2/5)) + 1
      #8:  y = 3/sqrt(x) + 7x^3               -> -3/(2*x^(3/2)) + 21x^2
      #9:  y = 10x^2 - 4x + 6                 -> 20x - 4
      #10: y = 3x^3 + 2x^2 + x + 4            -> 9x^2 + 4x + 1
      #11: y = x^(1/3) - sqrt(x) + 1/x        -> 1/(3*x^(2/3)) - 1/(2*sqrt(x)) - 1/x^2
      #12: y = 100x^4 - x^2                   -> 400x^3 - 2x
      #13: y = 13x^2 + 6x - 100               -> 26x + 6
      #14: y = 2/x^23                         -> -46/x^24
      #15: y = 24x^3 - x^2 + x + 1            -> 72x^2 - 2x + 1
      #16: y = x^(3/4) - 2*x^(2/3)            -> 3/(4*x^(1/4)) - 4/(3*x^(1/3))
      #17: y = x^4 - 6x^3 + 12x^2 + x - 90    -> 4x^3 - 18x^2 + 24x + 1
      #18: y = 5x^3 - 14x^2 - 1/x             -> 15x^2 - 28x + 1/x^2

Pathway 1: Authentic textbook problem formulations & rule definitions.
Pathway 2: Parametric / randomized generalization variations spanning integer polynomials,
           fractional root powers, Laurent negative powers, trig, log/exp, product, quotient,
           and chain rules.
"""

import json
import os
import random
import sys
import sympy
from sympy import symbols, diff, sympify

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.templates.registry import TEMPLATES, classify_problem

x = symbols('x')

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

    # Authentic Chapter 1 Problems (#1 - #18)
    ch1_problems = [
        # (prob_num, expr_str, deriv_str, phrasings)
        (1, "x^6 - 5*x^2 + 1", "6*x^5 - 10*x", [
            "Find the derivative of y = x^6 - 5*x^2 + 1 using the power rule",
            "Calculate dy/dx for y = x^6 - 5*x^2 + 1 by power and sum/difference rules",
            "Differentiate y = x^6 - 5x^2 + 1 with respect to x",
            "What is the derivative of x^6 - 5*x^2 + 1 using the power rule?"
        ]),
        (2, "5*x^4 - sqrt(x)", "20*x^3 - 1/(2*sqrt(x))", [
            "Find the derivative of y = 5*x^4 - sqrt(x) using the power rule",
            "Calculate dy/dx for y = 5*x^4 - x^(1/2) using power and difference rules",
            "Differentiate y = 5x^4 - sqrt(x) w.r.t x using the power rule",
        ]),
        (3, "6*x^(1/3) + x^2", "2/x^(2/3) + 2*x", [
            "Find the derivative of y = 6*x^(1/3) + x^2 using the power rule",
            "Calculate dy/dx for y = 6*root(3, x) + x^2 using power and sum rules",
            "Differentiate y = 6*cbrt(x) + x^2 using the power rule",
        ]),
        (4, "4*x^2 - 10*x + 14", "8*x - 10", [
            "Find the derivative of y = 4*x^2 - 10*x + 14 using the power rule",
            "Calculate dy/dx for y = 4x^2 - 10x + 14 using sum and difference rules",
            "Differentiate 4*x^2 - 10*x + 14 with respect to x using the power rule",
        ]),
        (5, "3/x^2 + 1/x", "-6/x^3 - 1/x^2", [
            "Find the derivative of y = 3/x^2 + 1/x using the power rule",
            "Calculate dy/dx for y = 3*x^(-2) + x^(-1) using power and sum rules",
            "Differentiate y = 3/x^2 + 1/x with respect to x",
        ]),
        (6, "5*x^3 - x^2 + 12*x - 1000", "15*x^2 - 2*x + 12", [
            "Find the derivative of y = 5*x^3 - x^2 + 12*x - 1000 using the power rule",
            "Calculate dy/dx for y = 5x^3 - x^2 + 12x - 1000 using power and sum rules",
            "Differentiate y = 5*x^3 - x^2 + 12*x - 1000 with respect to x",
        ]),
        (7, "x^(3/5) + x", "3/(5*x^(2/5)) + 1", [
            "Find the derivative of y = x^(3/5) + x using the power rule",
            "Calculate dy/dx for y = root(5, x^3) + x using power and sum rules",
            "Differentiate y = x^(3/5) + x with respect to x using the power rule",
        ]),
        (8, "3/sqrt(x) + 7*x^3", "-3/(2*x^(3/2)) + 21*x^2", [
            "Find the derivative of y = 3/sqrt(x) + 7*x^3 using the power rule",
            "Calculate dy/dx for y = 3*x^(-1/2) + 7*x^3 using power and sum rules",
            "Differentiate y = 3/sqrt(x) + 7x^3 with respect to x",
        ]),
        (9, "10*x^2 - 4*x + 6", "20*x - 4", [
            "Find the derivative of y = 10*x^2 - 4*x + 6 using the power rule",
            "Calculate dy/dx for y = 10x^2 - 4x + 6 by sum and difference rules",
            "Differentiate y = 10*x^2 - 4*x + 6 with respect to x",
        ]),
        (10, "3*x^3 + 2*x^2 + x + 4", "9*x^2 + 4*x + 1", [
            "Find the derivative of y = 3*x^3 + 2*x^2 + x + 4 using the power rule",
            "Calculate dy/dx for y = 3x^3 + 2x^2 + x + 4 using power and sum rules",
            "Differentiate y = 3*x^3 + 2*x^2 + x + 4 with respect to x",
        ]),
        (11, "x^(1/3) - sqrt(x) + 1/x", "1/(3*x^(2/3)) - 1/(2*sqrt(x)) - 1/x^2", [
            "Find the derivative of y = x^(1/3) - sqrt(x) + 1/x using the power rule",
            "Calculate dy/dx for y = cbrt(x) - sqrt(x) + 1/x using power and sum/difference rules",
            "Differentiate y = x^(1/3) - x^(1/2) + x^(-1) with respect to x",
        ]),
        (12, "100*x^4 - x^2", "400*x^3 - 2*x", [
            "Find the derivative of y = 100*x^4 - x^2 using the power rule",
            "Calculate dy/dx for y = 100x^4 - x^2 using power and difference rules",
            "Differentiate y = 100*x^4 - x^2 with respect to x",
        ]),
        (13, "13*x^2 + 6*x - 100", "26*x + 6", [
            "Find the derivative of y = 13*x^2 + 6*x - 100 using the power rule",
            "Calculate dy/dx for y = 13x^2 + 6x - 100 by sum/difference rules",
            "Differentiate y = 13*x^2 + 6*x - 100 with respect to x",
        ]),
        (14, "2/x^23", "-46/x^24", [
            "Find the derivative of y = 2/x^23 using the power rule",
            "Calculate dy/dx for y = 2*x^(-23) using the power rule",
            "Differentiate y = 2/x^23 with respect to x",
        ]),
        (15, "24*x^3 - x^2 + x + 1", "72*x^2 - 2*x + 1", [
            "Find the derivative of y = 24*x^3 - x^2 + x + 1 using the power rule",
            "Calculate dy/dx for y = 24x^3 - x^2 + x + 1 using power and sum rules",
            "Differentiate y = 24*x^3 - x^2 + x + 1 with respect to x",
        ]),
        (16, "x^(3/4) - 2*x^(2/3)", "3/(4*x^(1/4)) - 4/(3*x^(1/3))", [
            "Find the derivative of y = x^(3/4) - 2*x^(2/3) using the power rule",
            "Calculate dy/dx for y = root(4, x^3) - 2*root(3, x^2) using power and difference rules",
            "Differentiate y = x^(3/4) - 2*x^(2/3) with respect to x",
        ]),
        (17, "x^4 - 6*x^3 + 12*x^2 + x - 90", "4*x^3 - 18*x^2 + 24*x + 1", [
            "Find the derivative of y = x^4 - 6*x^3 + 12*x^2 + x - 90 using the power rule",
            "Calculate dy/dx for y = x^4 - 6x^3 + 12x^2 + x - 90 using power and sum rules",
            "Differentiate y = x^4 - 6*x^3 + 12*x^2 + x - 90 with respect to x",
        ]),
        (18, "5*x^3 - 14*x^2 - 1/x", "15*x^2 - 28*x + 1/x^2", [
            "Find the derivative of y = 5*x^3 - 14*x^2 - 1/x using the power rule",
            "Calculate dy/dx for y = 5x^3 - 14x^2 - x^(-1) using power and difference rules",
            "Differentiate y = 5*x^3 - 14*x^2 - 1/x with respect to x",
        ]),
    ]

    for num, expr, ans, phrasings in ch1_problems:
        for q in phrasings:
            entries.append(make_entry(
                q, "power_rule_derivative",
                {"expr": expr, "answer": ans},
                "derivative"
            ))

    # Incomplete / adversarial examples for power rule
    entries.append(make_entry(
        "Find the derivative using the power rule",
        "power_rule_derivative",
        {"expr": None, "answer": None},
        "derivative",
        False, ["expr"]
    ))
    entries.append(make_entry(
        "Apply power rule and sum/difference rules to differentiate",
        "power_rule_derivative",
        {"expr": None, "answer": None},
        "derivative",
        False, ["expr"]
    ))

    # Trig Derivatives (Page 2 Reference Rules)
    trig_rules_data = [
        ("sin(x)", "cos(x)", "Find the derivative of sin(x) using trigonometric derivative rules"),
        ("cos(x)", "-sin(x)", "Calculate the derivative of cos(x) using trigonometric rules"),
        ("tan(x)", "sec(x)^2", "What is the derivative of tan(x) using trigonometric derivative rules?"),
        ("sec(x)", "sec(x)*tan(x)", "Find dy/dx for y = sec(x) using trigonometric rules"),
        ("csc(x)", "-csc(x)*cot(x)", "Differentiate y = csc(x) using trigonometric derivative rules"),
        ("cot(x)", "-csc(x)^2", "Evaluate the derivative of cot(x) with respect to x using trig derivative rules"),
        ("sin(x) + cos(x)", "cos(x) - sin(x)", "Find the derivative of sin(x) + cos(x) using trigonometric derivative rules"),
        ("sec(x) + tan(x)", "sec(x)*tan(x) + sec(x)^2", "Find the derivative of sec(x) + tan(x) using trigonometric rules"),
        ("3*sin(x) - 4*cos(x)", "3*cos(x) + 4*sin(x)", "Calculate the derivative of 3*sin(x) - 4*cos(x) using trig derivative rules"),
        ("cot(x) - csc(x)", "-csc(x)^2 + csc(x)*cot(x)", "Find the derivative of cot(x) - csc(x) using trigonometric rules"),
    ]
    for expr, ans, q in trig_rules_data:
        entries.append(make_entry(
            q, "trig_derivative",
            {"expr": expr, "answer": ans},
            "derivative"
        ))
    entries.append(make_entry(
        "Differentiate the trig function using trigonometric rules",
        "trig_derivative",
        {"expr": None, "answer": None},
        "derivative",
        False, ["expr"]
    ))

    # Log and Exponential Derivatives (Page 2 Reference Rules)
    log_exp_rules_data = [
        ("exp(x)", "exp(x)", "Find the derivative of e^x using exponential derivative rules"),
        ("ln(x)", "1/x", "Calculate dy/dx for y = ln(x) using logarithmic derivative rules"),
        ("exp(3*x)", "3*exp(3*x)", "Find the derivative of e^(3*x) using exponential derivative rules"),
        ("ln(x) + exp(x)", "1/x + exp(x)", "Differentiate y = ln(x) + e^x using logarithmic derivative rules"),
        ("2^x", "2^x*ln(2)", "Find the derivative of 2^x using exponential derivative rules"),
        ("5^x", "5^x*ln(5)", "Calculate dy/dx for y = 5^x using exponential derivative rules"),
        ("ln(x) - exp(2*x)", "1/x - 2*exp(2*x)", "Find the derivative of ln(x) - e^(2*x) using logarithmic derivative rules"),
        ("4*exp(x) + 3*ln(x)", "4*exp(x) + 3/x", "Calculate the derivative of 4*e^x + 3*ln(x) using logarithmic and exponential derivative rules"),
    ]
    for expr, ans, q in log_exp_rules_data:
        entries.append(make_entry(
            q, "log_exp_derivative",
            {"expr": expr, "answer": ans},
            "derivative"
        ))
    entries.append(make_entry(
        "Compute the derivative of the natural log function using logarithmic derivative rules",
        "log_exp_derivative",
        {"expr": None, "answer": None},
        "derivative",
        False, ["expr"]
    ))

    # Product Rule (Page 2 Reference Rules)
    product_data = [
        ("x^2*sin(x)", "2*x*sin(x) + x^2*cos(x)", "Find the derivative of x^2*sin(x) using the product rule"),
        ("x*exp(x)", "exp(x) + x*exp(x)", "Differentiate y = x*e^x using the product rule"),
        ("x^3*ln(x)", "3*x^2*ln(x) + x^2", "Calculate dy/dx for y = x^3*ln(x) using the product rule"),
        ("sin(x)*cos(x)", "cos(x)^2 - sin(x)^2", "Find the derivative of sin(x)*cos(x) using the product rule"),
        ("exp(x)*sin(x)", "exp(x)*sin(x) + exp(x)*cos(x)", "Evaluate the derivative of e^x*sin(x) using the product rule"),
    ]
    for expr, ans, q in product_data:
        entries.append(make_entry(
            q, "product_rule_derivative",
            {"expr": expr, "answer": ans},
            "derivative"
        ))

    # Quotient Rule (Page 2 Reference Rules)
    quotient_data = [
        ("sin(x)/x", "(x*cos(x) - sin(x))/x^2", "Find the derivative of sin(x)/x using the quotient rule"),
        ("exp(x)/(x^2 + 1)", "exp(x)*(x^2 - 2*x + 1)/(x^2 + 1)^2", "Differentiate y = e^x/(x^2 + 1) using the quotient rule"),
        ("ln(x)/x", "(1 - ln(x))/x^2", "Calculate dy/dx for y = ln(x)/x using the quotient rule"),
        ("(x + 1)/(x - 1)", "-2/(x - 1)^2", "Find the derivative of (x+1)/(x-1) using the quotient rule"),
        ("x/(sin(x) + 1)", "(sin(x) + 1 - x*cos(x))/(sin(x) + 1)^2", "Differentiate y = x/(sin(x) + 1) using the quotient rule"),
    ]
    for expr, ans, q in quotient_data:
        entries.append(make_entry(
            q, "quotient_rule_derivative",
            {"expr": expr, "answer": ans},
            "derivative"
        ))

    # Chain Rule (Page 2 Reference Rules)
    chain_data = [
        ("sin(x^3)", "3*x^2*cos(x^3)", "Find the derivative of sin(x^3) using the chain rule"),
        ("exp(x^2 + 1)", "2*x*exp(x^2 + 1)", "Differentiate y = e^(x^2 + 1) using the chain rule"),
        ("ln(x^2 + 4)", "2*x/(x^2 + 4)", "Calculate dy/dx for y = ln(x^2 + 4) using the chain rule"),
        ("cos(3*x^2 - 5)", "-6*x*sin(3*x^2 - 5)", "Find the derivative of cos(3*x^2 - 5) using the chain rule"),
        ("sqrt(4*x^2 + 9)", "4*x/sqrt(4*x^2 + 9)", "Differentiate y = sqrt(4x^2 + 9) using the chain rule"),
    ]
    for expr, ans, q in chain_data:
        entries.append(make_entry(
            q, "chain_rule_derivative",
            {"expr": expr, "answer": ans},
            "derivative"
        ))

    return entries

def generate_way2():
    """
    Parametric generator creating 250+ mathematically verified derivative variations:
      - Integer power polynomials (degrees 2..7)
      - Fractional radical terms (x^(p/q))
      - Negative Laurent powers (a/x^k)
      - Trig linear combinations
      - Log & Exponential combinations
      - Product, Quotient, Chain rule variations
    """
    entries = []
    random.seed(42)

    # 1. Polynomials with Power Rule
    for _ in range(60):
        deg = random.randint(2, 6)
        coeffs = [random.randint(-15, 15) for _ in range(deg + 1)]
        while coeffs[-1] == 0:
            coeffs[-1] = random.randint(1, 10)
        
        # Build sympy expression
        poly_expr = sum(c * x**i for i, c in enumerate(coeffs) if c != 0)
        if poly_expr == 0:
            poly_expr = x**2
        poly_diff = diff(poly_expr, x)

        expr_str = str(poly_expr).replace("**", "^")
        ans_str = str(poly_diff).replace("**", "^")

        templates_phrasing = [
            f"Find the derivative of y = {expr_str} using the power rule",
            f"Calculate dy/dx for y = {expr_str} using power and sum/difference rules",
            f"Differentiate {expr_str} with respect to x using the power rule",
            f"What is the derivative of y = {expr_str} using the power rule?",
        ]
        q = random.choice(templates_phrasing)
        entries.append(make_entry(q, "power_rule_derivative", {"expr": expr_str, "answer": ans_str}, "derivative"))

    # 2. Fractional Powers & Radicals
    for _ in range(50):
        m = random.choice([2, 3, 4, 5])
        p = random.choice([1, 2, 3, 4, 5, 7])
        if p == m:
            p = m + 1
        c1 = random.randint(1, 12) * random.choice([1, -1])
        c2 = random.randint(1, 10) * random.choice([1, -1])
        deg2 = random.choice([1, 2, 3])

        poly_expr = c1 * x**(sympy.Rational(p, m)) + c2 * x**deg2
        poly_diff = diff(poly_expr, x)

        expr_str = str(poly_expr).replace("**", "^")
        ans_str = str(poly_diff).replace("**", "^")

        q = random.choice([
            f"Find the derivative of y = {expr_str} using the power rule",
            f"Calculate dy/dx for y = {expr_str} by the power rule and sum rule",
            f"Differentiate y = {expr_str} with respect to x using the power rule",
        ])
        entries.append(make_entry(q, "power_rule_derivative", {"expr": expr_str, "answer": ans_str}, "derivative"))

    # 3. Laurent / Negative Powers (Reciprocals)
    for _ in range(40):
        k1 = random.randint(1, 10)
        k2 = random.randint(1, 6)
        a1 = random.randint(1, 9) * random.choice([1, -1])
        a2 = random.randint(1, 9) * random.choice([1, -1])

        poly_expr = a1 * x**(-k1) + a2 * x**(-k2)
        poly_diff = diff(poly_expr, x)

        expr_str = str(poly_expr).replace("**", "^")
        ans_str = str(poly_diff).replace("**", "^")

        q = random.choice([
            f"Find the derivative of y = {expr_str} using the power rule",
            f"Calculate dy/dx for y = {expr_str} using the power rule",
            f"Differentiate y = {expr_str} with respect to x using the power rule",
        ])
        entries.append(make_entry(q, "power_rule_derivative", {"expr": expr_str, "answer": ans_str}, "derivative"))

    # 4. Trig Derivative Combinations
    trig_funcs = [sympy.sin(x), sympy.cos(x), sympy.tan(x), sympy.sec(x)]
    for _ in range(40):
        f1, f2 = random.sample(trig_funcs, 2)
        c1 = random.randint(1, 8) * random.choice([1, -1])
        c2 = random.randint(1, 8) * random.choice([1, -1])

        expr_obj = c1 * f1 + c2 * f2
        diff_obj = diff(expr_obj, x)

        expr_str = str(expr_obj).replace("**", "^")
        ans_str = str(diff_obj).replace("**", "^")

        q = random.choice([
            f"Find the derivative of {expr_str} using trigonometric derivative rules",
            f"Calculate dy/dx for y = {expr_str} using trigonometric derivative rules",
            f"Differentiate y = {expr_str} with respect to x using trig derivative rules",
        ])
        entries.append(make_entry(q, "trig_derivative", {"expr": expr_str, "answer": ans_str}, "derivative"))

    # 5. Log & Exponential Combinations
    for _ in range(35):
        k = random.randint(1, 5)
        c1 = random.randint(1, 6) * random.choice([1, -1])
        c2 = random.randint(1, 6) * random.choice([1, -1])

        expr_obj = c1 * sympy.exp(k * x) + c2 * sympy.ln(x)
        diff_obj = diff(expr_obj, x)

        expr_str = str(expr_obj).replace("**", "^")
        ans_str = str(diff_obj).replace("**", "^")

        q = random.choice([
            f"Find the derivative of {expr_str} using exponential derivative rules",
            f"Calculate dy/dx for y = {expr_str} using logarithmic derivative rules",
            f"Differentiate y = {expr_str} with respect to x using logarithmic and exponential derivative rules",
        ])
        entries.append(make_entry(q, "log_exp_derivative", {"expr": expr_str, "answer": ans_str}, "derivative"))

    # 6. Product Rule Variations
    for _ in range(30):
        deg = random.randint(1, 4)
        c = random.randint(1, 5)
        trig_or_exp = random.choice([sympy.sin(x), sympy.cos(x), sympy.exp(x), sympy.ln(x)])

        expr_obj = c * (x**deg) * trig_or_exp
        diff_obj = diff(expr_obj, x)

        expr_str = str(expr_obj).replace("**", "^")
        ans_str = str(diff_obj).replace("**", "^")

        q = random.choice([
            f"Find the derivative of {expr_str} using the product rule",
            f"Calculate dy/dx for y = {expr_str} using the product rule",
            f"Differentiate y = {expr_str} with respect to x using the product rule",
        ])
        entries.append(make_entry(q, "product_rule_derivative", {"expr": expr_str, "answer": ans_str}, "derivative"))

    # 7. Chain Rule Variations
    for _ in range(30):
        deg = random.randint(2, 4)
        c = random.randint(1, 5)
        inner = c * x**deg + random.randint(1, 9)
        outer_func = random.choice([sympy.sin, sympy.cos, sympy.exp, sympy.ln])

        expr_obj = outer_func(inner)
        diff_obj = diff(expr_obj, x)

        expr_str = str(expr_obj).replace("**", "^")
        ans_str = str(diff_obj).replace("**", "^")

        q = random.choice([
            f"Find the derivative of {expr_str} using the chain rule",
            f"Calculate dy/dx for y = {expr_str} using the chain rule",
            f"Differentiate y = {expr_str} with respect to x using the chain rule",
        ])
        entries.append(make_entry(q, "chain_rule_derivative", {"expr": expr_str, "answer": ans_str}, "derivative"))

    return entries

def main():
    dataset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "verimath_finetune_dataset.jsonl"))
    print(f"Loading existing dataset from: {dataset_path}")
    
    existing_entries = []
    if os.path.exists(dataset_path):
        with open(dataset_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    existing_entries.append(json.loads(line))
    print(f"Existing entries: {len(existing_entries)}")

    way1 = generate_way1()
    print(f"Generated Way 1 (Authentic & Reference Rules): {len(way1)} examples")

    way2 = generate_way2()
    print(f"Generated Way 2 (Parametric & Variational Generalization): {len(way2)} examples")

    new_entries = way1 + way2
    print(f"Total new entries to append: {len(new_entries)}")

    # Check templates exist in registry
    for e in new_entries:
        asst = json.loads(e["messages"][2]["content"])
        tpl_id = asst["template"]
        assert tpl_id in TEMPLATES, f"Template {tpl_id} not in registry!"

    # Append to dataset
    with open(dataset_path, "a", encoding="utf-8") as f:
        for item in new_entries:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"Successfully appended {len(new_entries)} entries.")
    total = len(existing_entries) + len(new_entries)
    print(f"New total dataset size: {total} examples")

if __name__ == "__main__":
    main()
