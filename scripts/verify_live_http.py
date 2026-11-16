import urllib.request
import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

p1 = r"A fish swims upstream a distance $D$ against a river current of speed $u = 4\text{ km/h}$. The total energy $E$ expended by the fish swimming at speed $v > 4$ relative to the water is proportional to its water speed cubed times the travel time $t$: $E(v) = k v^3 t$. Since ground speed is $v - 4$, travel time is $t = \frac{D}{v - 4}$. What swimming speed $v$ minimizes the total energy used?"
p2 = r"Among all right triangles with a fixed area of $A = 18\text{ cm}^2$, find the legs $x$ and $y$ that minimize the sum of the lengths of the two legs ($x + y$), and state the resulting hypotenuse."
p3 = r"Point $A$ is at $(0, 2)$ and point $B$ is at $(6, 4)$. A light ray travels from $A$, reflects off a flat mirror along the $x$-axis at point $P(x, 0)$, and reaches $B$. Use calculus to find the coordinate $x$ that minimizes the total path length $L(x) = AP + PB$."
p4 = r"A right circular cylinder is inscribed in a sphere of fixed radius $R = 5\text{ cm}$. Instead of maximizing volume, find the cylinder radius $r$ and height $H$ that maximize the curved (lateral) surface area $S = 2\pi r H$ of the cylinder."

problems = [p1, p2, p3, p4]

for i, p in enumerate(problems, 1):
    req = urllib.request.Request(
        "http://127.0.0.1:8001/solve",
        data=json.dumps({"problem": p}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        print(f"=== HTTP P{i} ===")
        print("Status:", data.get("status"))
        print("Template:", data.get("template_id"))
        print("Answer:", data.get("verified_answer"))
        print("LaTeX:", data.get("latex_answer"))
        print("Lean:", data.get("lean_statement"))
        print("Rejection:", data.get("rejection_reason"))
        assert data.get("status") == "VERIFIED", f"HTTP P{i} failed: {data}"

print("\n>>> ALL 4 PROBLEMS VERIFIED LIVE VIA HTTP ON 127.0.0.1:8001/solve! <<<")
