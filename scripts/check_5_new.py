from backend.templates.registry import classify_problem
from backend.pipeline.solver import solve

p1 = (
    r"A trapezoid has three equal sides—its bottom base and its two slanted legs each have a fixed length of $10\text{ cm}$—"
    r"while the length of the parallel top base can vary depending on how wide the slanted legs are angled outward. "
    r"If $\theta$ ($0 < \theta < \frac{\pi}{2}$) is the angle between each slanted leg and the vertical "
    r"(or between each slanted leg and the horizontal extension of the bottom base), find the angle $\theta$ "
    r"and the length of the top base that maximize the area of the trapezoid, and calculate that maximum area."
)

p2 = (
    r"A rectangle of width $8\text{ cm}$ and height $6\text{ cm}$ is centered at the origin $(0, 0)$ "
    r"with its sides parallel to the coordinate axes, so its four vertices lie at $(\pm 4, \pm 3)$. "
    r"An ellipse $\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1$ ($a > 4, b > 3$) is circumscribed around the rectangle "
    r"so that all four corners of the rectangle lie on the ellipse. Knowing that the area of an ellipse is "
    r"$A = \pi a b$, find the semi-axes $a$ and $b$ that minimize the area of the ellipse, and state that minimum area."
)

p3 = (
    r"Wait—let's look at a tangent segment on a parabola: a line is tangent to the parabola $y = 12 - x^2$ at a point $P(x_0, y_0)$ "
    r"in the first quadrant ($0 < x_0 < 2\sqrt{3}$). The tangent line intersects the positive $x$-axis at $A$ and the positive $y$-axis at $B$. "
    r"Find the exact coordinates $(x_0, y_0)$ of point $P$ that minimize the sum of the two intercepts ($OA + OB$), and calculate that minimum sum."
)

p4 = (
    r"A right circular cone is inscribed inside a hemisphere of fixed radius $R = 6\text{ cm}$ such that the vertex (apex) "
    r"of the cone is at the center of the flat circular base of the hemisphere, and the circular base of the cone lies in a plane "
    r"parallel to the hemisphere's flat base (touching the curved dome). Find the radius $r$ and height $h$ of the cone that "
    r"maximize its volume, and calculate that maximum volume."
)

p5 = (
    r"A hardware factory produces and sells $12,000$ microcontroller boards per year at a steady rate. "
    r"Each production run of size $x$ boards incurs a fixed machine-calibration setup cost of $\$150$ per run "
    r"(so there are $\frac{12,000}{x}$ runs per year). In addition, storing unsold boards in the warehouse costs $\$4$ "
    r"per board per year based on the average inventory level of $\frac{x}{2}$ boards. Express the total annual cost $C(x)$ "
    r"(setup cost + storage cost) as a function of the batch size $x$, find the batch size $x$ that minimizes total annual cost, "
    r"and state that minimum annual cost."
)

problems = [p1, p2, p3, p4, p5]

for i, p in enumerate(problems, 1):
    c = classify_problem(p)
    print(f"P{i} Template: {c}")
