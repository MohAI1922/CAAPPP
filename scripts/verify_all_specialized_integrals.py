import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.templates.registry import classify_problem, get_template, TEMPLATES
from backend.pipeline.solver import solve
from backend.pipeline.formalizer import formalize
from backend.pipeline.lean_runner import verify, LeanVerdict

templates_to_test = [
    # 1. PUN integral
    ("pun_integral", "Find the indefinite integral of (2*x + 3)/(x^2 + 6*x + 45) with respect to x using the PUN method"),
    # 2. Radical manipulation
    ("root_manipulation_integral", "Integrate 4*x^5*sqrt(x^3 + 1) dx by manipulating the root"),
    # 3. Inverted quadratic
    ("inverted_quadratic_integral", "Integrate 1 / ((x + 2)^2 + 25) dx"),
    # 4. Trig substitution
    ("trig_substitution_integral", "Find the integral of sqrt(x^2 - 16) with respect to x using trig substitution"),
    # 5. Partial fractions
    ("partial_fraction_integral", "Integrate 8 / (x^2 + 4*x - 12) dx using partial fractions"),
    # 6. Long division
    ("long_division_integral", "Evaluate the integral of (x^2 - 7*x - 11) / (x - 8) dx using long division"),
    # 7. Rational root theorem
    ("rational_root_integral", "Integrate (6*x^2 - 10*x + 8)/(5*x^3 + 29*x^2 + 19*x - 5) dx using rational root theorem"),
    # 8. Integration by parts
    ("integration_by_parts", "Integrate x * cos(x) dx using integration by parts"),
    # 9. Cyclic IBP
    ("cyclic_ibp_integral", "Integrate exp(2*x) * sin(x) dx using cyclic ibp"),
    # 10. Tabular IBP
    ("tabular_ibp_integral", "Integrate x^2 * sin(x) dx using the tabular method"),
    # 11. Trig power reduction
    ("trig_power_reduction_integral", "Integrate sin(x)^5 * cos(x)^2 dx using power reducing"),
    # 12. Wallis integral
    ("wallis_integral", "Evaluate the definite integral of cos(x)^3 from 0 to pi/2 using Wallis formula"),
    # 13. Product to sum
    ("product_to_sum_trig_integral", "Integrate sin(3*x) * cos(2*x) dx using different angles"),
    # 14. Weierstrass substitution
    ("weierstrass_substitution_integral", "Find the indefinite integral of 1 / (1 + cos(x) + sin(x)) with respect to x using Weierstrass substitution"),
    # 15. Radical species
    ("radical_species_integral", "Integrate 1 / ((2*x + 3)*sqrt(x + 1)) dx using radical species"),
    # 16. Absolute value definite integral
    ("absolute_value_definite_integral", "Evaluate the definite integral of abs(x^2 - 3*x - 10) from 0 to 7"),
    # 17. S.E-One method
    ("se_one_integral", "Evaluate the definite integral of x^4 / (exp(x) + 1) from -2 to 2 using S.E-One method"),
    # 18. Quad root trick
    ("quad_root_trick_integral", "Integrate sqrt((x+3)*(x+4)*(x+5)*(x+6) + 1) dx using the quad-root trick"),
]

print(f"Total templates in TEMPLATES: {len(TEMPLATES)}")
print(f"Testing {len(templates_to_test)} specialized integration templates...\n")

passed_classification = 0
passed_solving = 0
passed_lean = 0

for i, (expected_cat, prob) in enumerate(templates_to_test, 1):
    cat = classify_problem(prob)
    class_ok = (cat == expected_cat)
    if class_ok:
        passed_classification += 1
    
    res = solve(prob)
    cand_ans = res.candidate_answer
    lean_ans = res.lean_answer
    reasoning = res.reasoning
    solve_ok = (cand_ans != "Could not compute indefinite integral." and cand_ans != "Could not evaluate integral.")
    if solve_ok:
        passed_solving += 1
    
    # Formalize statement
    form_res = formalize(prob, res, cat)
    lean_stmt = form_res.lean_statement
    
    lean_res = verify(lean_stmt)
    lean_ok = (lean_res.verdict == LeanVerdict.VERIFIED)
    if lean_ok:
        passed_lean += 1
    
    status_c = "[OK]" if class_ok else f"[FAIL: got {cat}]"
    status_s = "[OK]" if solve_ok else "[FAIL]"
    status_l = "[OK]" if lean_ok else "[FAIL]"
    
    print(f"[{i:02d}] {expected_cat:<32} | Class: {status_c:<7} | Solve: {status_s:<5} | Lean: {status_l}")
    if not (class_ok and solve_ok and lean_ok):
        print(f"     Ans: {cand_ans}")
        print(f"     Reasoning: {reasoning}")
        clean_stmt = lean_stmt.replace("ℝ", "R").replace("∫", "integral")
        print(f"     Statement: {clean_stmt}")

print(f"\nSummary:")
print(f"Classification : {passed_classification}/{len(templates_to_test)}")
print(f"Solving        : {passed_solving}/{len(templates_to_test)}")
print(f"Lean 4 Verified: {passed_lean}/{len(templates_to_test)}")
