"""
VeriMath — Demo Problem Warmup Script
======================================
Pre-runs all exhibition demo problems through the full pipeline and
caches the results in demo_cache.db.

Run this BEFORE the exhibition to ensure instant responses for demo problems.
Novel problems (not in the list below) will still run the full live pipeline.

Usage:
    python scripts/warmup_lean.py
    python scripts/warmup_lean.py --dry-run   (just check Lean is working)
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.pipeline.lean_runner import warmup, verify_async, LeanVerdict
from backend.pipeline import cache as demo_cache
from backend.pipeline.solver import solve
from backend.pipeline.formalizer import formalize
from backend.pipeline.statement_judge import judge
from backend.pipeline.explainer import explain
from backend.templates.registry import classify_problem

logging.basicConfig(level=logging.INFO, format="%(asctime)s [warmup] %(levelname)s — %(message)s")
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Demo problems to pre-cache (exhibition day script)
# ─────────────────────────────────────────────────────────────────────────────

DEMO_PROBLEMS = [
    # ✅ Should all verify
    "What is 47 × 89 + 123?",
    "Simplify (x + 1)² − x²",
    "Solve 3x + 7 = 22",
    "Find the derivative of x² sin(x) with respect to x",
    "Evaluate the definite integral of x² from 0 to 1",
    "Is 97 prime?",
    "Find the distance between the points (1, 2) and (4, 6)",

    # Additional nice demos
    "What is 2^10?",
    "Simplify x³ − x",
    "Is 101 prime?",
]


async def main(dry_run: bool = False) -> None:
    demo_cache.init_db()

    if dry_run:
        logger.info("Dry run: testing Lean installation only...")
        ok = await warmup()
        if ok:
            logger.info("✅ Lean is working correctly!")
        else:
            logger.error("❌ Lean check failed. See logs above.")
        return

    logger.info(f"Pre-caching {len(DEMO_PROBLEMS)} demo problems...")
    logger.info("First, warming up Lean (loads Mathlib cache into RAM)...")

    ok = await warmup()
    if not ok:
        logger.error(
            "Lean warmup failed. Cannot pre-cache demo problems. "
            "Check that Lean 4 is installed and Mathlib is pre-compiled."
        )
        sys.exit(1)

    results = {"verified": 0, "failed": 0, "skipped": 0}

    for i, problem in enumerate(DEMO_PROBLEMS, 1):
        print(f"\n[{i}/{len(DEMO_PROBLEMS)}] Problem: '{problem}'")

        # Check if already cached
        cached = demo_cache.get(problem)
        if cached:
            print(f"  ⚡ Already cached (template: {cached.template_id})")
            results["skipped"] += 1
            continue

        try:
            start = time.monotonic()

            # Classify
            template_id = classify_problem(problem)
            if not template_id:
                print(f"  🚫 Unsupported template — skipping")
                results["skipped"] += 1
                continue

            print(f"  Template: {template_id}")

            # Solve
            solver_result = solve(problem)
            print(f"  Candidate answer: {solver_result.candidate_answer}")

            # Formalize
            formalizer_result = formalize(problem, solver_result, template_id)
            print(f"  Lean statement: {formalizer_result.lean_statement[:80]}...")

            # Judge
            judge_result = judge(problem, formalizer_result)
            print(f"  Statement judge: {judge_result.verdict} (score={judge_result.similarity_score:.2f})")

            if judge_result.verdict == "MISMATCH":
                print(f"  ⚠️  Judge MISMATCH: {judge_result.reason}")
                results["failed"] += 1
                continue

            # Verify
            lean_result = await verify_async(formalizer_result.lean_statement)
            print(f"  Lean verdict: {lean_result.verdict} ({lean_result.elapsed_ms}ms)")

            if lean_result.verdict != LeanVerdict.VERIFIED:
                print(f"  ❌ Lean rejected. Output: {lean_result.lean_output[:100]}")
                results["failed"] += 1
                continue

            # Explain
            explanation = explain(problem, solver_result.candidate_answer, solver_result.reasoning)

            elapsed_ms = int((time.monotonic() - start) * 1000)

            # Cache
            demo_cache.put(
                problem=problem,
                template_id=template_id,
                verified_answer=solver_result.candidate_answer,
                lean_statement=formalizer_result.lean_statement,
                back_translation=judge_result.back_translation,
                explanation=explanation,
                elapsed_ms=elapsed_ms,
            )

            print(f"  ✅ Cached! Total: {elapsed_ms}ms")
            results["verified"] += 1

        except Exception as e:
            logger.error(f"  ❌ Error: {e}")
            results["failed"] += 1

    print("\n" + "=" * 60)
    print(f"Warmup complete:")
    print(f"  ✅ Verified and cached: {results['verified']}")
    print(f"  ⚡ Already cached:      {results['skipped']}")
    print(f"  ❌ Failed:             {results['failed']}")
    print("=" * 60)

    if results["failed"] > 0:
        print("\n⚠️  Some problems failed. Check logs above.")
        print("   These will run the live pipeline on exhibition day (slower).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VeriMath demo warmup script")
    parser.add_argument("--dry-run", action="store_true", help="Only test Lean, don't cache problems")
    args = parser.parse_args()

    asyncio.run(main(dry_run=args.dry_run))
