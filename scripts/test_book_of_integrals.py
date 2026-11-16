import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.templates.registry import classify_problem
from backend.pipeline.solver import solve
from backend.pipeline.lean_runner import verify, LeanVerdict

test_problems = [
    # Ch 1: Power rule & radicals
    "Find the indefinite integral of x^2 + 3*x with respect to x",
    "Integrate 6*sqrt(x) - 4/x^3 with respect to x",
    "Find the antiderivative of (x^2 + 3)^3 with respect to x",
    "Evaluate the integral of (6*x^3 - 4*x^2 + 100)/sqrt(x) dx",
    
    # Ch 2: Trig, exp, log
    "Find the indefinite integral of sin(x) + cos(x) with respect to x",
    "Integrate 6^x + exp(x) with respect to x",
    "Evaluate the integral of (csc(x)^2 + sec(x)*tan(x)) dx",
    "Find the antiderivative of 6/x with respect to x",
    
    # Ch 3: U-sub
    "Evaluate the integral of (3*x + 8)^5 dx",
    "Find the indefinite integral of (3*x^2 + 6)/(x^3 + 6*x + 8) with respect to x",
    "Integrate x*sqrt(6*x^2 - 1) dx",
    
    # Ch 4: Manipulating root
    "Integrate 4*x^5*sqrt(x^3 + 1) dx",
    "Find the indefinite integral of x^3/sqrt(x^2 + 1) with respect to x",
    
    # Ch 5: Special trig & completing square
    "Integrate 1 / ((x + 2)^2 + 25) dx",
    "Find the indefinite integral of sec(4*x)^3 with respect to x",
    "Find the antiderivative of 1 / (x^2 + 10*x + 61) with respect to x",
    "Integrate 1 / (3*x^2 + 12*x + 80) dx",
    
    # Ch 7: Trig sub
    "Find the integral of sqrt(x^2 - 16) with respect to x",
    "Integrate 1 / sqrt(4 - x^2) dx",
    "Find the antiderivative of 1 / sqrt(x^2 + 6*x - 72) with respect to x",
    
    # Ch 8: PFD
    "Integrate 8 / (x^2 + 4*x - 12) dx",
    "Find the indefinite integral of (3*x^2 - 6*x + 4) / ((x - 3)*(x^2 + 4)) with respect to x",
    "Integrate (2*x - 2) / (x^2 + 4*x + 4) dx",
    
    # Ch 9: Long division then PFD
    "Evaluate the integral of (x^2 - 7*x - 11) / (x - 8) dx",
    "Integrate (3*x^3 - x + 12) / (x^2 - 1) dx",
]

print(f"Testing {len(test_problems)} representative problems from Book of Integrals...\n")
passed = 0
for i, prob in enumerate(test_problems, 1):
    cat = classify_problem(prob)
    res = solve(prob)
    cand_ans = res.candidate_answer
    lean_ans = res.lean_answer
    
    # Indefinite integral: candidate answer is F(x) + C, so antideriv is F(x)
    antideriv = lean_ans.replace(" + C", "").strip()
    
    # Test through lean_runner
    import re
    # Formulate Lean theorem
    clean_p = prob.replace("Find the indefinite integral of ", "").replace("Integrate ", "").replace("Find the antiderivative of ", "").replace("Evaluate the integral of ", "").replace("Find the integral of ", "")
    clean_p = re.sub(r"\s+with\s+respect\s+to\s+x", "", clean_p)
    clean_p = re.sub(r"\s+dx$", "", clean_p)
    
    lean_code = (
        f"import Mathlib\n\n"
        f"example (x : ℝ) : deriv (fun x => {antideriv}) x = {clean_p} := by\n"
        f"  simp\n  ring\n"
    )
    res_lean = verify(lean_code)
    verified = (res_lean.verdict == LeanVerdict.VERIFIED)
    
    status = "[PASS]" if verified else "[FAIL]"
    if verified:
        passed += 1
    print(f"[{i:02d}] {cat:<20} | {status} | {prob[:45]}...")
    if not verified:
        print(f"     Ans: {cand_ans}")
        print(f"     Lean Ans: {lean_ans}")

print(f"\nResult: {passed}/{len(test_problems)} passed Lean/SymPy verification.")
