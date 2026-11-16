import urllib.request
import json

problems = [
    (
        "Screenshot 1: Rectangular Garden Perimeter Area Maximization",
        r"A rectangular garden is to be constructed with a total perimeter of $60\text{ meters}$. What dimensions ($L$ and $W$) will maximize the total enclosed area, and what is that maximum area?"
    ),
    (
        "Screenshot 2: Quadratic Minimum Value",
        r"Find the minimum value of the quadratic function $f(x) = 3x^2 - 12x + 7$"
    )
]

for name, p in problems:
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
