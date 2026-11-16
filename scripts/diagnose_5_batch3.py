from backend.templates.registry import classify_problem, get_template, fill_template, get_back_translation
from backend.pipeline.solver import solve
from backend.pipeline.formalizer import formalize
from backend.pipeline.statement_judge import judge
from backend.pipeline.lean_runner import verify

problems = [
    (
        "P1 - Triangle Included Angle Area Maximization",
        r"Two sides of a triangle have fixed lengths $a = 6\text{ cm}$ and $b = 10\text{ cm}$, with an included angle $\theta$ between them. What angle $\theta$ maximizes the area of the triangle, and what is that maximum area?"
    ),
    (
        "P2 - Open-top Box Length Twice Width",
        r"An open-top rectangular box must hold a fixed volume of $72\text{ cm}^3$, and the length of its base must be twice its width ($L = 2W$). Find the dimensions of the box that minimize the total surface area of material used."
    ),
    (
        "P3 - Projectile Range Angle Maximization",
        r"The horizontal range of a projectile launched at speed $v_0 = 20\text{ m/s}$ at an angle $\theta$ above flat ground (with $g = 10\text{ m/s}^2$) is $R(\theta) = \frac{v_0^2}{g}\sin\theta\cos\theta = 40\sin\theta\cos\theta$. Use calculus to find the launch angle $\theta$ that maximizes the range."
    ),
    (
        "P4 - Horizontal Parabola Inscribed Rectangle",
        r"Find the dimensions and maximum area of a rectangle inscribed in the region bounded by the horizontal parabola $x = 9 - y^2$ and the $y$-axis ($x = 0$)."
    ),
    (
        "P5 - Cubic Tangent Minimum Slope",
        r"Find the point $(x, y)$ on the cubic curve $y = x^3 - 6x^2 + 15x - 2$ where the tangent line has the smallest (least) slope, and state what that minimum slope is."
    )
]

for label, p in problems:
    tid = classify_problem(p)
    print(f"=== {label} ===")
    print(f"Classified template: {tid}")
    if tid:
        sr = solve(p)
        print(f"Solver answer: {sr.candidate_answer}")
        fr = formalize(p, sr, tid)
        tmpl = get_template(tid)
        bt = get_back_translation(tmpl, fr.slot_values)
        safe_bt = bt.encode('ascii', 'backslashreplace').decode('ascii')
        print(f"Back-translation: {safe_bt}")
        jr = judge(p, fr)
        print(f"Judge: verdict={jr.verdict}, score={jr.similarity_score:.3f}, reason={jr.reason}")
        if fr.lean_statement:
            lr = verify(fr.lean_statement)
            print(f"Lean: {lr.verdict}")
    else:
        print("-> UNSUPPORTED")
    print()
