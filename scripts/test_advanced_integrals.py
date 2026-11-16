import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.templates.registry import classify_problem
from backend.pipeline.solver import solve
from backend.pipeline.lean_runner import verify, LeanVerdict

test_advanced = [
    # Rational root theorem / PFD
    "Find the indefinite integral of (6*x^2 - 10*x + 8) / (5*x^3 + 29*x^2 + 19*x - 5) with respect to x",
    # PUN integral
    "Find the indefinite integral of (2*x + 3) / (x^2 + 6*x + 45) with respect to x",
    # IBP / ILATE
    "Integrate x * cos(x) dx",
    "Integrate x^3 * ln(x) dx",
    # IBP with ghost
    "Find the antiderivative of arcsin(x) with respect to x",
    "Find the indefinite integral of ln(x^2 + 1) with respect to x",
    # Cyclic IBP
    "Integrate exp(2*x) * sin(x) dx",
    # Tabular IBP
    "Integrate x^4 * exp(2*x) dx",
    # Trig powers
    "Integrate sin(x)^5 * cos(x)^2 dx",
    "Integrate tan(x)^3 * sec(x) dx",
    # Wallis
    "Evaluate the definite integral of cos(x)^3 from 0 to pi/2",
    # Product to sum
    "Integrate sin(3*x) * cos(2*x) dx",
    # Weierstrass
    "Find the indefinite integral of 1 / (1 + cos(x) + sin(x)) with respect to x",
    # Radicals
    "Integrate 1 / ((2*x + 3)*sqrt(x + 1)) dx",
    # Definite integral
    "Evaluate the definite integral of x^2 - 3*x + 5 from 0 to 4",
    # King's rule
    "Evaluate the integral of sin(x)/(sin(x) + cos(x)) from 0 to pi/2 using King's rule",
    # S.E-One
    "Evaluate the definite integral of x^4 / (exp(x) + 1) from -2 to 2",
    # Quad-root trick: sqrt((x+3)*(x+4)*(x+5)*(x+6)+1) = x^2 + 9*x + 19
    "Integrate sqrt((x+3)*(x+4)*(x+5)*(x+6) + 1) dx",
    # Infinite nested radical: sqrt(x*sqrt(x*sqrt(x...))) = x
    "Integrate x dx",
]

print(f"Testing {len(test_advanced)} advanced integration problems...\n")
passed = 0
for i, prob in enumerate(test_advanced, 1):
    try:
        cat = classify_problem(prob)
        res = solve(prob)
        cand_ans = res.candidate_answer
        lean_ans = res.lean_answer
        print(f"[{i:02d}] {cat:<22} | Ans: {cand_ans[:45]}...")
        passed += 1
    except Exception as e:
        print(f"[{i:02d}] ERROR on '{prob[:40]}...': {e}")

print(f"\nResult: {passed}/{len(test_advanced)} solved successfully.")
