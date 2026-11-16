import sys
import os
sys.path.insert(0, os.path.abspath("."))
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from backend.pipeline.solver import solve
from backend.templates.registry import classify_problem, fill_template, get_back_translation
from backend.pipeline.formalizer import FormalizerResult
from backend.pipeline.statement_judge import judge

problems = [
    r"Find the absolute maximum value of $f(x) = x\sqrt{4 - x^2}$ on the closed interval $[-2, 2]$.",
    r"A lifeguard is at point $A$ on a straight beach and needs to reach a swimmer located $30\text{ m}$ offshore and $50\text{ m}$ down the beach. She runs at $5\text{ m/s}$ on sand and swims at $3\text{ m/s}$ in water. How far from the point on the beach directly opposite the swimmer ($x$) should she enter the water to minimize travel time?",
    r"The illumination $I$ at a point on a table from a lightbulb hanging at height $h$ directly above the center of a circular table of radius $R = 4\text{ m}$ is given by $I(h) = \frac{h}{(h^2 + 16)^{3/2}}$ at the table's edge. What height $h$ maximizes the illumination at the edge?",
    r"A rain gutter is formed from a long sheet of metal $30\text{ cm}$ wide by bending up one-third of the sheet ($10\text{ cm}$) on each side through an angle $\theta$. What angle $\theta$ maximizes the cross-sectional area of the gutter?",
    r"A line in the first quadrant passes through the point $(1, 8)$ and intersects the positive $x$-axis at $(a, 0)$ and the positive $y$-axis at $(0, b)$. Find the minimum possible sum of the intercepts, $S = a + b$."
]

for i, p in enumerate(problems, 1):
    t_id = classify_problem(p)
    res = solve(p)
    print(f"=== Problem {i} ===")
    print("Problem:", p)
    print("Classified Template:", t_id)
    print("Candidate Answer:", res.candidate_answer if res else None)
    print("Slots:", res.slots if res else None)
    if res and res.slots:
        f_res = FormalizerResult(
            lean_statement=res.lean_statement or "",
            template_id=t_id,
            slot_values=res.slots,
            raw_formalization=""
        )
        j_res = judge(p, f_res)
        print(f"Judge: verdict={j_res.verdict}, score={j_res.similarity_score:.2f}, reason={j_res.reason}")
        print("Back Translation:", j_res.back_translation)
    print()
