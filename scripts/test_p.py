import sys
sys.path.insert(0, '.')
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
import asyncio
from backend.templates.registry import classify_problem
from backend.pipeline.solver import solve
from backend.pipeline.formalizer import formalize
from backend.pipeline.statement_judge import judge
from backend.pipeline.lean_runner import verify_async

p = r"A closed right circular cylinder must have a fixed volume of $54\pi\text{ cm}^3$. What radius $r$ minimizes the total surface area?"
print("Problem:", p)
cat = classify_problem(p)
print("Classification:", cat)
sol = solve(p)
print("Candidate answer:", sol.candidate_answer)
form = formalize(p, sol, cat)
print("Formal statement:", form.lean_statement)
print("Form slots:", form.slot_values)
j = judge(p, form)
print("Back-translation:", j.back_translation)
print("Judge:", j.verdict, "Score:", j.similarity_score, "Reason:", j.reason)
lean_res = asyncio.run(verify_async(form.lean_statement))
print("Lean verdict:", lean_res.verdict, "in", lean_res.elapsed_ms, "ms")
