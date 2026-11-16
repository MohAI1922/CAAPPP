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
        "Problem 1: Paper Cup Cone Volume Maximization",
        r"A paper cup in the shape of a right circular cone is made by cutting a sector from a flat circular disk of radius $R = 6\text{ cm}$ and joining the cut edges. What height $h$ of the cone maximizes its volume?",
        "disk_cone_volume_optimization"
    ),
    (
        "Problem 2: Medication Concentration Extrema",
        r"The concentration $C(t)$ of a medication in the bloodstream $t$ hours after injection is given by $C(t) = \frac{4t}{t^2 + 9}$ for $t \ge 0$. Find the time at which the maximum concentration occurs and the maximum concentration.",
        "extrema_points"
    ),
    (
        "Problem 3: Two Ships Closest Approach",
        r"At noon ($t = 0$), Ship A is $10\text{ km}$ due west of Ship B. Ship A sails east at $4\text{ km/h}$, while Ship B sails north at $3\text{ km/h}$. At what time $t$ are the two ships closest to each other, and what is that minimum distance?",
        "moving_objects_closest_approach_optimization"
    ),
    (
        "Problem 4: Real Exponential 1D Extrema",
        r"Find all local and absolute extrema of $f(x) = e^{2x} + 8e^{-x}$ for all real $x$.",
        "extrema_points"
    ),
]

async def run_all():
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
        assert lean_res.verdict.name == "VERIFIED", f"Lean verification failed: {lean_res.lean_output}"
        
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
