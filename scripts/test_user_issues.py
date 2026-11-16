import urllib.request
import json

test_problems = [
    (
        "Local Extrema (Problem 1)",
        "Find the local maximum or minimum value of the function x 2 - 6x + 11"
    ),
    (
        "Local Extrema Cubic (Problem 2)",
        "Find both the local maximum and local minimum values of $f(x) = x^3 - 3x^2 - 9x + 5$."
    ),
    (
        "Absolute Extrema Interval (Problem 3)",
        "Find the absolute maximum and absolute minimum values of $f(x) = x^3 - 12x$ on the closed interval $[0, 3]$."
    ),
    (
        "Sum Max Product (Problem 4)",
        "Find two positive numbers whose sum is $20$ and whose product is as large as possible."
    ),
    (
        "Garden Cost Optimization (User Latest)",
        "A rectangular garden with an area of $200\\text{ m}^2$ is to be enclosed by a fence. The fencing for the front side facing the street costs $\\$12\\text{ per meter}$, while the fencing for the other three sides costs $\\$4\\text{ per meter}$. Find the dimensions of the garden that will minimize the total cost of the fencing, and state that minimum cost."
    ),
    (
        "Sphere in Conical Tank",
        "An inverted conical tank has a height of $H = 12\\text{ m}$ and a top radius of $R = 6\\text{ m}$. It initially contains water to a depth of $h_0$. A solid heavy sphere of radius $a = \\sqrt{5}\\text{ m}$ is lowered into the tank along its vertical central axis at a constant downward speed of $u = 0.5\\text{ m/s}$. At the exact instant when the sphere is exactly half-submerged, the water level is just touching the horizontal great circle (equator) of the sphere, and there is no water spilling over the top of the cone. Find the rate at which the water level $h$ is rising with respect to the vertex of the cone at that exact instant."
    ),
    (
        "Weierstrass Definite Integral",
        "Evaluate the definite integral \\int_{0}^{\\pi/2} \\frac{x}{(1 + \\sin x + \\cos x)^2} \\, dx"
    )
]

for name, p in test_problems:
    req = urllib.request.Request(
        "http://localhost:8000/solve",
        data=json.dumps({"problem": p}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            print(f"=== {name} ===")
            print(f"Status: {data.get('status')} | Template: {data.get('template_id')} | Elapsed: {data.get('elapsed_ms')}ms")
            print(f"Answer: {data.get('verified_answer')}")
            print(f"LaTeX: {data.get('latex_answer')}")
            if data.get('rejection_reason'):
                print(f"Rejection: {data.get('rejection_reason')}")
            print()
    except Exception as e:
        print(f"=== {name} ===")
        print(f"HTTP Error: {e}")
        print()
