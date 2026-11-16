#!/usr/bin/env python3
"""
VeriMath — Instant Edge CLI Tester
Usage:
    python cli_solve.py "integrate 1 / sqrt(sin^3(x) * cos^5(x)) dx"
    python cli_solve.py "\\int \\frac{1}{\\sqrt{\\sin^3(x) \\cos^5(x)}} dx"
    python cli_solve.py "Solve 3x + 7 = 22"
    python cli_solve.py "Find the derivative of x^2 * sin(x)"
    python cli_solve.py --interactive
"""

import sys
import time
import asyncio
from pathlib import Path

# Ensure root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from backend.templates.registry import classify_problem
from backend.pipeline.solver import solve
from backend.pipeline.formalizer import formalize
from backend.pipeline.statement_judge import judge
from backend.pipeline.lean_runner import verify_async, LeanVerdict
from backend.pipeline.explainer import explain
from backend.main import to_latex


async def run_test(problem: str):
    print("=" * 65)
    print(f"📥 PROBLEM: {problem}")
    print("=" * 65)

    start = time.monotonic()

    # Step 1: Classify
    template_id = classify_problem(problem)
    print(f"🏷️  TEMPLATE: {template_id or 'UNSUPPORTED'}")
    if not template_id:
        print("❌ Status: UNSUPPORTED (outside verified domain)")
        return

    # Step 2: Solve
    t0 = time.monotonic()
    s_res = solve(problem)
    s_ms = int((time.monotonic() - t0) * 1000)
    print(f"💡 SOLVER ANSWER: {s_res.candidate_answer} ({s_ms}ms)")
    latex_ans = to_latex(s_res.candidate_answer)
    if latex_ans:
        print(f"📐 LATEX ANSWER : {latex_ans}")

    # Step 3: Formalize
    t0 = time.monotonic()
    f_res = formalize(problem, s_res, template_id)
    f_ms = int((time.monotonic() - t0) * 1000)
    print(f"\n📜 LEAN 4 STATEMENT ({f_ms}ms):")
    print("---")
    print(f_res.lean_statement)
    print("---")

    # Step 4: Statement Judge
    j_res = judge(problem, f_res)
    print(f"⚖️  JUDGE VERDICT : {j_res.verdict} (similarity score: {j_res.similarity_score:.2f})")

    # Step 5: Verification (Lean 4 / CAS)
    t0 = time.monotonic()
    v_res = await verify_async(f_res.lean_statement)
    v_ms = int((time.monotonic() - t0) * 1000)
    status_icon = "✅" if v_res.verdict == LeanVerdict.VERIFIED else "❌"
    print(f"{status_icon} VERIFICATION  : {v_res.verdict.value.upper()} ({v_ms}ms)")

    # Step 6: Explanation
    exp = explain(problem, s_res.candidate_answer, s_res.reasoning)
    print(f"\n📖 TUTOR EXPLANATION:\n{exp.strip()}")

    total_ms = int((time.monotonic() - start) * 1000)
    print("=" * 65)
    print(f"⚡ TOTAL EDGE LATENCY: {total_ms}ms | STATUS: {v_res.verdict.value.upper()}")
    print("=" * 65)


def main():
    if len(sys.argv) > 1 and sys.argv[1] != "--interactive":
        prob = " ".join(sys.argv[1:])
        asyncio.run(run_test(prob))
    else:
        print("🚀 VeriMath Edge CLI Tester (type 'quit' or 'exit' to stop)\n")
        while True:
            try:
                prob = input("\nEnter math problem > ").strip()
                if not prob or prob.lower() in ("quit", "exit"):
                    break
                asyncio.run(run_test(prob))
            except (KeyboardInterrupt, EOFError):
                break


if __name__ == "__main__":
    main()
