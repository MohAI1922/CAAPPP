import sys
sys.path.insert(0, '.')
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
import asyncio
from backend.templates.registry import classify_problem
from backend.pipeline.solver import solve
from backend.pipeline.formalizer import formalize
from backend.pipeline.statement_judge import judge
from backend.pipeline.lean_runner import verify_async
from backend.main import to_latex

problems = [
    (
        "Problem 1: Closed Cylinder Surface Area Minimization",
        r"A closed right circular cylinder must have a fixed volume of $54\pi\text{ cm}^3$. What radius $r$ minimizes the total surface area?",
        "closed_cylinder_optimization"
    ),
    (
        "Problem 2: Sphere Inscribed Cone Volume Maximization",
        r"A right circular cone is inscribed in a sphere of fixed radius $R = 9\text{ cm}$. What is the maximum possible volume of this cone?",
        "sphere_inscribed_cone_optimization"
    ),
    (
        "Problem 3: Line Closest Point",
        r"Find the point on the line $y = 2x + 1$ that is closest to the point $(4, 1)$.",
        "line_closest_point_optimization"
    ),
    (
        "Problem 4: Average Cost Minimization",
        r"A manufacturing company has a total cost function $C(x) = x^2 + 36$, where $x$ is the number of units produced. Find the production level $x$ that minimizes the average cost per unit, $AC(x) = \frac{C(x)}{x}$.",
        "average_cost_minimization"
    ),
]

async def run_all():
    all_ok = True
    for title, prob, expected_cat in problems:
        print(f"================================================================")
        print(f"TEST: {title}")
        print(f"Problem: {prob}")
        
        # 1. Classify
        cat = classify_problem(prob)
        print(f"Classification: {cat} (expected: {expected_cat})")
        assert cat == expected_cat, f"Classification mismatch: {cat} != {expected_cat}"
        
        # 2. Solve
        sol = solve(prob)
        print(f"Candidate Answer: {sol.candidate_answer}")
        print(f"Lean Answer: {sol.lean_answer}")
        
        # 3. Formalize
        form = formalize(prob, sol, cat)
        print(f"Formal Statement: {form.lean_statement}")
        
        # 4. Judge
        j = judge(prob, form)
        print(f"Judge Verdict: {j.verdict} (score: {j.similarity_score:.2f})")
        print(f"Back-Translation: {j.back_translation}")
        if j.reason:
            print(f"Judge Reason: {j.reason}")
        assert j.verdict == "MATCH", f"Judge rejected: {j.reason}"
        
        # 5. Lean Verify
        lean_res = await verify_async(form.lean_statement)
        print(f"Lean Verdict: {lean_res.verdict} in {lean_res.elapsed_ms}ms")
        assert lean_res.verdict.name == "VERIFIED", f"Lean verification failed: {lean_res.error_message}"
        
        # 6. LaTeX Formatter
        tex = to_latex(sol.candidate_answer)
        print(f"LaTeX Output: {tex}")
        print(">>> SUCCESS! <<<")
        print()
        
    print("================================================================")
    print("ALL 4 USER CALCULUS PROBLEMS FULLY VERIFIED AND PASSING!")
    print("================================================================")

if __name__ == "__main__":
    asyncio.run(run_all())
