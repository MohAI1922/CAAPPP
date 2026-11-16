import sys
sys.stdout.reconfigure(encoding='utf-8')
from backend.templates.registry import classify_problem, get_template, fill_template, get_back_translation
from backend.pipeline.cache import get as cache_get
from backend.main import solve, SolveRequest
import asyncio

problems = [
    ("1. Semicircle rect max perimeter", r"A rectangle is inscribed in a semicircle of radius $R = 5\text{ cm}$ with one of its sides lying along the diameter. Instead of maximizing area, find the dimensions (width $2x$ and height $y$) that maximize the perimeter of the rectangle."),
    ("2. Triangle circumscribed rect min area", r"An isosceles triangle is circumscribed around a rectangle of width $8\text{ cm}$ and height $3\text{ cm}$ (such that the base of the rectangle rests on the base of the triangle, and the top two corners of the rectangle touch the two slanted sides of the triangle). Find the total height $H$ and base $B$ of the triangle that minimize its area."),
    ("3. Ellipse tangent min intercepted length", r"A tangent line is drawn to the ellipse $\frac{x^2}{9} + \frac{y^2}{4} = 1$ at a point $(x_0, y_0)$ in the first quadrant. Find the minimum possible length $L$ of the segment of the tangent line intercepted between the positive $x$- and $y$-axes."),
    ("4. Y-shaped road network", r"Two towns $A$ and $B$ are located $12\text{ km}$ apart along a straight east-west line, and a third town $C$ is located $10\text{ km}$ due north of the midpoint $M$ between $A$ and $B$. An engineer builds a Y-shaped road network: roads run from $A$ and $B$ to a junction point $P$ located $x\text{ km}$ north of $M$, and a single road runs from $P$ to $C$. Find the distance $x$ that minimizes the total length of road built."),
    ("5. Curve and line max vertical distance", r"On the closed interval $[0, 1]$, find the $x$-coordinate that maximizes the vertical distance between the curve $f(x) = x^{1/3}$ and the line $g(x) = x$, and find that maximum vertical distance.")
]

for name, p in problems:
    c = cache_get(p)
    cat = classify_problem(p)
    print(f"=== {name} ===")
    print("Cache hit:", bool(c))
    if c:
        print("Cached template:", c.template_id)
        print("Cached answer:", c.verified_answer)
    print("Classified as:", cat)
    
    # Run full solve pipeline
    resp = asyncio.run(solve(SolveRequest(problem=p)))
    print("Solve status:", resp.status)
    print("Verified answer:", resp.verified_answer)
    print("Rejection reason:", resp.rejection_reason)
    print()
