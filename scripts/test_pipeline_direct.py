import sys
sys.path.insert(0, '.')
import asyncio
from backend.templates.registry import classify_problem, get_template, fill_template
from backend.pipeline.solver import solve
from backend.pipeline.formalizer import formalize
from backend.pipeline.statement_judge import judge
from backend.pipeline.lean_runner import verify_async
from backend.main import to_latex

problems = [
    ('Exponential Extrema', r'Find the maximum value of the function $f(x) = x e^{-x}$ for $x \ge 0$.'),
    ('Rational Function Local Extrema', r'Find the local minimum value of the rational function $f(x) = \frac{x^2 + 4}{x}$ for $x > 0$'),
    ('Economic Profit Optimization', r"A company's total revenue is $R(x) = 120x - 0.5x^2$ and total cost is $C(x) = 3000 + 20x$, where $x$ is units produced. What production level $x$ maximizes profit, and what is that maximum profit?"),
    ('Parabola Closest Point', r'Find the point on the parabola $y = x^2$ that is closest to the point $(0, \frac{3}{2})$.'),
    ('Trigonometric Interval Extrema', r'Find the absolute maximum and minimum values of $f(x) = \sin x + \cos x$ on the interval $[0, 2\pi]$.')
]

async def run_all():
    for name, p in problems:
        print(f"=== {name} ===")
        tmpl_id = classify_problem(p)
        print(f"Template ID: {tmpl_id}")
        sol_res = solve(p)
        print(f"Candidate Answer: {sol_res.candidate_answer}")
        
        form_res = formalize(p, sol_res, tmpl_id)
        
        judge_res = judge(p, form_res)
        print(f"Judge Verdict: {judge_res.verdict} | Reason: {judge_res.reason}")
        
        lean_res = await verify_async(form_res.lean_statement)
        print(f"Lean Verdict: {lean_res.verdict}")
        
        latex = to_latex(sol_res.candidate_answer)
        print(f"LaTeX Output: {latex}")
        print()

asyncio.run(run_all())
