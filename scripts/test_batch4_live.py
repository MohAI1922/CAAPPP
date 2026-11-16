import sys, os
sys.path.insert(0, os.path.abspath("."))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import asyncio
from backend.main import solve_endpoint, SolveRequest

# Novel numbers not in demo cache:
# P1: u = 6 km/h => v = 3/2 * 6 = 9 km/h
p1 = r"A fish swims upstream a distance $D$ against a river current of speed $u = 6\text{ km/h}$. The total energy $E$ expended by the fish swimming at speed $v > 6$ relative to the water is proportional to its water speed cubed times the travel time $t$: $E(v) = k v^3 t$. Since ground speed is $v - 6$, travel time is $t = \frac{D}{v - 6}$. What swimming speed $v$ minimizes the total energy used?"

# P2: A = 32 cm^2 => x = y = sqrt(64) = 8 cm, h = sqrt(128) = 8*sqrt(2) cm
p2 = r"Among all right triangles with a fixed area of $A = 32\text{ cm}^2$, find the legs $x$ and $y$ that minimize the sum of the lengths of the two legs ($x + y$), and state the resulting hypotenuse."

# P3: A(0, 3), B(8, 5) => x = 3*8/(3+5) = 24/8 = 3, L_sq = 8^2 + (3+5)^2 = 64 + 64 = 128 => L = 8*sqrt(2)
p3 = r"Point $A$ is at $(0, 3)$ and point $B$ is at $(8, 5)$. A light ray travels from $A$, reflects off a flat mirror along the $x$-axis at point $P(x, 0)$, and reaches $B$. Use calculus to find the coordinate $x$ that minimizes the total path length $L(x) = AP + PB$."

# P4: R = 4 cm => r^2 = 16/2 = 8, H^2 = 32, S_pi = 32
p4 = r"A right circular cylinder is inscribed in a sphere of fixed radius $R = 4\text{ cm}$. Instead of maximizing volume, find the cylinder radius $r$ and height $H$ that maximize the curved (lateral) surface area $S = 2\pi r H$ of the cylinder."

problems = [p1, p2, p3, p4]

async def main():
    for i, p in enumerate(problems, 1):
        res = await solve_endpoint(SolveRequest(problem=p))
        print(f"=== NOVEL P{i} ===")
        print("Status:", res.status)
        print("Template:", res.template_id)
        print("Answer:", res.verified_answer)
        print("LaTeX Answer:", res.latex_answer)
        print("Lean stmt:", res.lean_statement)
        print("Back translation:", res.back_translation)
        print("From cache:", res.from_cache)
        if res.rejection_reason:
            print("REJECTION:", res.rejection_reason)
        assert res.status == "VERIFIED", f"Novel P{i} failed: {res.status} ({res.rejection_reason})"
        assert not res.from_cache, f"Novel P{i} was unexpectedly from cache!"
    print("\n>>> ALL 4 NOVEL VARIATIONS VERIFIED DYNAMICALLY FROM SCRATCH! <<<")

if __name__ == "__main__":
    asyncio.run(main())
