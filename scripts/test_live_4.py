import urllib.request
import json
import time

p1 = (
    r"A right circular cylinder of radius $r$ and height $h$ is inscribed inside a sphere of fixed radius $R = \sqrt{5}\text{ cm}$. "
    r"Find the cylinder radius $r$ and height $h$ that maximize the total surface area of the closed cylinder "
    r"(including both circular ends and the curved side: $S = 2\pi r^2 + 2\pi r h$), and calculate that maximum surface area."
)

p2 = (
    r"Consider the curve $y = 4/x^2$ in the first quadrant ($x_0 > 0$). "
    r"A tangent line drawn at $(x_0, y_0)$ intersects the positive $x$-axis at $A$ and the positive $y$-axis at $B$. "
    r"Find the exact coordinates $(x_0, y_0)$ that minimize the sum of the two intercepts ($OA + OB$), and calculate that minimum sum."
)

p3 = (
    r"A delivery drone flies a fixed horizontal distance of $D = 30\text{ km}$ directly against a steady headwind of $w = 10\text{ km/h}$. "
    r"When the drone flies at an airspeed of $v\text{ km/h}$ relative to the air ($v > 10$), its ground speed is $(v - 10)\text{ km/h}$, "
    r"and its power draw is $P(v) = (v^2 + 300)\text{ Wh/hour}$. What airspeed $v$ minimizes the total battery energy $E(v)$ consumed over the $30\text{ km}$ trip, "
    r"and how many Watt-hours does the trip use?"
)

p4 = (
    r"A semicircle of radius $R = 2\text{ cm}$ rests with its flat diameter along the base of an isosceles triangle, "
    r"and the two equal slanted sides of the triangle are tangent to the curved arc of the semicircle. "
    r"If $\theta \in (0, \pi/2)$ is the base angle of the isosceles triangle, find the angle $\theta$ (or its trig ratios) "
    r"that minimizes the total area of the circumscribed isosceles triangle, and calculate that minimum area."
)

problems = [p1, p2, p3, p4]

for i, p in enumerate(problems, 1):
    req = urllib.request.Request(
        "http://localhost:8000/solve",
        data=json.dumps({"problem": p}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        print(f"=== Problem {i} ===")
        print("Status:", data.get("status"))
        print("Template:", data.get("template_id"))
        print("From Cache:", data.get("from_cache"))
        print("Verified Answer:", data.get("verified_answer"))
        print("LaTeX Answer:", data.get("latex_answer"))
        print("Rejection Reason:", data.get("rejection_reason"))
