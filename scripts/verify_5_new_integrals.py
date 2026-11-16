import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.templates.registry import classify_problem, TEMPLATES
from backend.pipeline.solver import solve
from backend.pipeline.formalizer import formalize
from backend.pipeline.lean_runner import verify, LeanVerdict

new_templates = [
    ("euler_formula_integral", "Integrate exp(3*x) * sin(x) dx using Euler's formula"),
    ("pfd_linear_power_trick_integral", "Evaluate \\int 1/((x+3)^2 * (x-6)^3) dx using the PFD linear power trick"),
    ("conjugate_radical_integral", "Evaluate \\int 1/(sqrt(3*x + 4) + sqrt(2*x + 1)) dx using conjugate radical method"),
    ("nested_infinite_radical_integral", "Integrate sqrt(x*sqrt(x*sqrt(x...))) dx using the nested radical simplification"),
    ("exp_derivative_sum_integral", "Evaluate the integral of exp(x) * (1/x - 1/x^2) dx using the exponential derivative sum rule"),
]

print(f"Total templates in TEMPLATES: {len(TEMPLATES)}")
print(f"Testing {len(new_templates)} new specialized integration templates...\n")

passed = 0
for i, (expected_cat, prob) in enumerate(new_templates, 1):
    cat = classify_problem(prob)
    class_ok = (cat == expected_cat)
    res = solve(prob)
    solve_ok = (res.candidate_answer != "Could not compute indefinite integral.")
    form_res = formalize(prob, res, cat)
    lean_res = verify(form_res.lean_statement)
    lean_ok = (lean_res.verdict == LeanVerdict.VERIFIED)
    
    st_c = "[OK]" if class_ok else f"[FAIL: {cat}]"
    st_s = "[OK]" if solve_ok else "[FAIL]"
    st_l = "[OK]" if lean_ok else "[FAIL]"
    print(f"[{i:02d}] {expected_cat:<32} | Class: {st_c:<7} | Solve: {st_s:<5} | Lean: {st_l}")
    if class_ok and solve_ok and lean_ok:
        passed += 1
    else:
        print(f"    Ans: {res.candidate_answer}")
        print(f"    Reasoning: {res.reasoning}")

print(f"\nResult: {passed}/{len(new_templates)} passed.")
