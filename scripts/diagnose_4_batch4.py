from backend.templates.registry import classify_problem, get_template, fill_template, get_back_translation
from backend.pipeline.solver import solve
from backend.pipeline.formalizer import formalize
from backend.pipeline.statement_judge import judge
from backend.pipeline.lean_runner import verify

problems = [
    (
        "Q1 - Fish Swimming Upstream Energy Minimization",
        r"A fish swims upstream a distance $D$ against a river current of speed $u = 4\text{ km/h}$. The total energy $E$ expended by the fish swimming at speed $v > 4$ relative to the water is proportional to its water speed cubed times the travel time $t$: $E(v) = k v^3 t$. Since ground speed is $v - 4$, travel time is $t = \frac{D}{v - 4}$. What swimming speed $v$ minimizes the total energy used?"
    ),
    (
        "Q2 - Right Triangle Fixed Area Minimum Legs Sum",
        r"Among all right triangles with a fixed area of $A = 18\text{ cm}^2$, find the legs $x$ and $y$ that minimize the sum of the lengths of the two legs ($x + y$), and state the resulting hypotenuse."
    ),
    (
        "Q3 - Light Ray Reflection Fermat Path Length Minimization",
        r"Point $A$ is at $(0, 2)$ and point $B$ is at $(6, 4)$. A light ray travels from $A$, reflects off a flat mirror along the $x$-axis at point $P(x, 0)$, and reaches $B$. Use calculus to find the coordinate $x$ that minimizes the total path length $L(x) = AP + PB$."
    ),
    (
        "Q4 - Inscribed Cylinder Lateral Surface Area Maximization",
        r"A right circular cylinder is inscribed in a sphere of fixed radius $R = 5\text{ cm}$. Instead of maximizing volume, find the cylinder radius $r$ and height $H$ that maximize the curved (lateral) surface area $S = 2\pi r H$ of the cylinder."
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
