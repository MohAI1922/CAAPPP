import sys, os
sys.path.insert(0, os.path.abspath("."))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import asyncio
from backend.main import solve_endpoint, SolveRequest

p1 = r"A fish swims upstream a distance $D$ against a river current of speed $u = 4\text{ km/h}$. The total energy $E$ expended by the fish swimming at speed $v > 4$ relative to the water is proportional to its water speed cubed times the travel time $t$: $E(v) = k v^3 t$. Since ground speed is $v - 4$, travel time is $t = \frac{D}{v - 4}$. What swimming speed $v$ minimizes the total energy used?"
p2 = r"Among all right triangles with a fixed area of $A = 18\text{ cm}^2$, find the legs $x$ and $y$ that minimize the sum of the lengths of the two legs ($x + y$), and state the resulting hypotenuse."
p3 = r"Point $A$ is at $(0, 2)$ and point $B$ is at $(6, 4)$. A light ray travels from $A$, reflects off a flat mirror along the $x$-axis at point $P(x, 0)$, and reaches $B$. Use calculus to find the coordinate $x$ that minimizes the total path length $L(x) = AP + PB$."
p4 = r"A right circular cylinder is inscribed in a sphere of fixed radius $R = 5\text{ cm}$. Instead of maximizing volume, find the cylinder radius $r$ and height $H$ that maximize the curved (lateral) surface area $S = 2\pi r H$ of the cylinder."

problems = [p1, p2, p3, p4]

async def main():
    for i, p in enumerate(problems, 1):
        res = await solve_endpoint(SolveRequest(problem=p))
        print(f"=== P{i} ===")
        print("Status:", res.status)
        print("Template:", res.template_id)
        print("Answer:", res.verified_answer)
        print("LaTeX Answer:", res.latex_answer)
        print("Lean stmt:", res.lean_statement)
        print("Back translation:", res.back_translation)
        print("From cache:", res.from_cache)
        if res.rejection_reason:
            print("REJECTION:", res.rejection_reason)
        assert res.status == "VERIFIED", f"P{i} failed: {res.status} ({res.rejection_reason})"
    print("\n>>> ALL 4 PROBLEMS VERIFIED SUCCESSFULLY! <<<")

if __name__ == "__main__":
    asyncio.run(main())

