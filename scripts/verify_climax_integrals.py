"""
Verification script for the 4 Climax Integrals:
- demoivre_roots_integral
- feynman_technique_integral
- series_expansion_definite_integral
- dilogarithm_integral
"""

import sys
import os

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.templates.registry import TEMPLATES, classify_problem, fill_template
from backend.pipeline.solver import solve
from backend.pipeline.lean_runner import _verify_with_sympy

problems = [
    {
        "id": "demoivre_roots_integral",
        "text": "Evaluate the integral of 1/(x^5 + 1) dx using De Moivre's theorem for partial fractions",
        "expected_template": "demoivre_roots_integral",
    },
    {
        "id": "feynman_technique_integral",
        "text": "Evaluate the definite integral of (x^2 - 1)/ln(x) from 0 to 1 using Feynman's technique of differentiation under the integral sign",
        "expected_template": "feynman_technique_integral",
    },
    {
        "id": "series_expansion_definite_integral",
        "text": "Evaluate the definite integral of (1 - cos(x))/x^2 from 0 to 1 using MacLaurin series expansion",
        "expected_template": "series_expansion_definite_integral",
    },
    {
        "id": "dilogarithm_integral",
        "text": "Evaluate the definite integral of ln(1 - exp(-x)) from 0 to oo using the dilogarithm function",
        "expected_template": "dilogarithm_integral",
    },
]

def main():
    print("Testing 4 Climax Integrals...")
    passed = 0
    for p in problems:
        text = p["text"]
        cat = classify_problem(text)
        print(f"\n--- Testing: {p['id']} ---")
        print(f"Text: {text}")
        print(f"Classified: {cat}")
        assert cat == p["expected_template"], f"Classification failed: got {cat}, expected {p['expected_template']}"

        sol = solve(text)
        print(f"Candidate answer: {sol.candidate_answer}")
        print(f"Lean answer: {sol.lean_answer}")
        print(f"Reasoning: {sol.reasoning}")

        from backend.pipeline.formalizer import formalize
        form_res = formalize(text, sol, cat)
        filled = form_res.lean_statement
        print(f"Slots: {form_res.slot_values}")
        print(f"Lean code:\n{filled}")

        v = _verify_with_sympy(filled)
        print(f"Lean CAS Verification: {'PASS' if v else 'FAIL'}")
        assert v, f"Lean CAS verification failed for {p['id']}"
        passed += 1

    print(f"\nAll {passed}/{len(problems)} climax integrals PASSED perfectly!")

if __name__ == "__main__":
    main()
