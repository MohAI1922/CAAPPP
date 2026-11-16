import urllib.request
import json

PROBLEMS = [
    (
        "P1 - Corridor / Hypotenuse Min Length",
        r"A corridor of width $1\text{ m}$ meets a perpendicular corridor of width $8\text{ m}$ (or equivalently, a line in the first quadrant passes through the point $(1, 8)$). What is the minimum length $L$ of the hypotenuse segment intercepted between the positive $x$- and $y$-axes?"
    ),
    (
        "P2 - Potato Farmer Revenue Maximization",
        r"A potato farmer can harvest immediately and get $100\text{ bushels}$, which sell for $\$6\text{ per bushel}$. For every week ($t$) the farmer waits, the crop grows by $20\text{ bushels}$, but the market price drops by $\$0.50\text{ per bushel}$ per week. How many weeks should the farmer wait to maximize total revenue?"
    ),
    (
        "P3 - Cone Circumscribed Around Sphere",
        r"A right circular cone is circumscribed around a sphere of radius $R = 3\text{ cm}$ (meaning the sphere sits inside the cone, tangent to its base and slanted sides). What height $h$ of the cone minimizes the cone's volume?"
    ),
    (
        "P4 - Two Light Sources Illumination",
        r"Two light sources are placed $10\text{ meters}$ apart. Light source $A$ is $8$ times as bright as light source $B$. Since illumination varies directly with brightness and inversely with the square of the distance ($I = \frac{k}{d^2}$), how far from light source $A$ on the line segment between them is the total illumination at a minimum?"
    )
]

for label, p_text in PROBLEMS:
    req = urllib.request.Request(
        "http://127.0.0.1:8001/solve",
        data=json.dumps({"problem": p_text}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        print(f"=== {label} ===")
        print(f"Status: {data.get('status')}")
        print(f"Template ID: {data.get('template_id')}")
        print(f"Verified Answer: {data.get('verified_answer')}")
        print(f"LaTeX Answer: {data.get('latex_answer')}")
        stmt = data.get('lean_statement')
        if stmt:
            stmt = stmt.encode('ascii', 'backslashreplace').decode('ascii')
        print(f"Lean Statement: {stmt}")
        print(f"From Cache: {data.get('from_cache')}")
        print(f"Elapsed: {data.get('elapsed_ms')}ms")
        print()
