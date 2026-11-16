import json
import urllib.request

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
    req_data = json.dumps({"problem": p}).encode("utf-8")
    req = urllib.request.Request(
        "http://127.0.0.1:8001/solve",
        data=req_data,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(f"=== {label} ===")
            print(f"Status: {data.get('status')}")
            print(f"Template: {data.get('template_id')}")
            print(f"Verified Answer: {data.get('verified_answer')}")
            stmt = data.get('lean_statement', '')
            safe_stmt = stmt.encode('ascii', 'backslashreplace').decode('ascii')
            print(f"Lean Statement: {safe_stmt}")
            lat = data.get('latex_answer', '')
            safe_lat = lat.encode('ascii', 'backslashreplace').decode('ascii')
            print(f"LaTeX Answer: {safe_lat}")
            print(f"Elapsed: {data.get('elapsed_ms')}ms")
            print()
    except Exception as e:
        print(f"Error testing {label}: {e}")
