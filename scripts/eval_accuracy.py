"""
VeriMath — Accuracy Evaluation Script
=======================================
Runs the held-out test set through the pipeline and computes all
design requirement metrics.

Usage:
    python scripts/eval_accuracy.py --split test
    python scripts/eval_accuracy.py --split train
    python scripts/eval_accuracy.py --inject-wrong     # Hallucination rejection test
    python scripts/eval_accuracy.py --judge-stats       # Formalization fidelity only

Outputs a JSON report + prints a summary table.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
import time
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.templates.registry import classify_problem
from backend.pipeline.solver import solve
from backend.pipeline.formalizer import formalize
from backend.pipeline.statement_judge import judge
from backend.pipeline.lean_runner import verify_async, warmup, LeanVerdict
from backend.pipeline.explainer import explain

logging.basicConfig(level=logging.WARNING)  # Quiet during eval
logger = logging.getLogger(__name__)

DATASET_DIR = Path(__file__).parent.parent / "backend" / "tests" / "dataset"


async def evaluate(
    split: str = "test",
    inject_wrong: bool = False,
    judge_only: bool = False,
) -> dict:
    """Run evaluation on the dataset split and return metrics dict."""

    dataset_file = DATASET_DIR / f"{split}.json"
    if not dataset_file.exists():
        print(f"❌ Dataset not found: {dataset_file}")
        print("   Run scripts/build_dataset.py first.")
        sys.exit(1)

    problems = json.loads(dataset_file.read_text(encoding="utf-8"))
    print(f"Loaded {len(problems)} problems from {split}.json")

    # Warm up Lean
    print("Warming up Lean...")
    await warmup()

    metrics = {
        "total": len(problems),
        "verified_correct": 0,      # Req 2: system accuracy
        "rejected_wrong": 0,         # Req 3: hallucination rejection
        "injected_wrong_total": 0,   # Denominator for Req 3
        "judge_match": 0,            # Req 4: formalization fidelity
        "judge_total": 0,
        "elapsed_ms_list": [],       # Req 1: response time
        "unsupported": 0,
        "errors": 0,
        "per_template": {},
    }

    for i, problem_data in enumerate(problems, 1):
        problem_text = problem_data["problem_text"]
        correct_answer = problem_data["correct_answer"]
        ground_truth_template = problem_data.get("template_id")

        print(f"\r[{i:3}/{len(problems)}] {problem_text[:50]:<50}", end="", flush=True)

        start = time.monotonic()

        try:
            # Classify
            template_id = classify_problem(problem_text)
            if not template_id:
                metrics["unsupported"] += 1
                continue

            # If inject_wrong: replace the solver's answer with a wrong one
            solver_result = solve(problem_text)

            if inject_wrong:
                metrics["injected_wrong_total"] += 1
                # Corrupt the answer by appending "+999" to make it wrong
                solver_result.candidate_answer = solver_result.candidate_answer + " + 999"
                solver_result.lean_answer = solver_result.lean_answer + " + 999"

            # Formalize
            try:
                formalizer_result = formalize(problem_text, solver_result, template_id)
            except ValueError:
                metrics["errors"] += 1
                continue

            # Judge
            judge_result = judge(problem_text, formalizer_result)
            metrics["judge_total"] += 1
            if judge_result.verdict == "MATCH":
                metrics["judge_match"] += 1
            else:
                if inject_wrong:
                    # Wrong answer → mismatch → correct rejection
                    metrics["rejected_wrong"] += 1
                continue  # Don't proceed to Lean if judge fails

            if judge_only:
                continue

            # Verify
            lean_result = await verify_async(formalizer_result.lean_statement)
            elapsed_ms = int((time.monotonic() - start) * 1000)
            metrics["elapsed_ms_list"].append(elapsed_ms)

            template_key = template_id or "unknown"
            if template_key not in metrics["per_template"]:
                metrics["per_template"][template_key] = {"verified": 0, "total": 0}
            metrics["per_template"][template_key]["total"] += 1

            if lean_result.verdict == LeanVerdict.VERIFIED:
                if not inject_wrong:
                    metrics["verified_correct"] += 1
                    metrics["per_template"][template_key]["verified"] += 1
                # inject_wrong + VERIFIED = hallucination slipped through (bad)

            elif lean_result.verdict in (LeanVerdict.REJECTED, LeanVerdict.TIMEOUT):
                if inject_wrong:
                    metrics["rejected_wrong"] += 1  # Correctly caught

        except Exception as e:
            metrics["errors"] += 1
            logger.debug(f"Error on '{problem_text[:40]}': {e}")

    print()  # Newline after progress

    # Compute summary metrics
    total_verifiable = metrics["total"] - metrics["unsupported"] - metrics["errors"]
    accuracy = metrics["verified_correct"] / total_verifiable if total_verifiable > 0 else 0.0
    hallucination_rejection = (
        metrics["rejected_wrong"] / metrics["injected_wrong_total"]
        if metrics["injected_wrong_total"] > 0 else None
    )
    fidelity = (
        metrics["judge_match"] / metrics["judge_total"]
        if metrics["judge_total"] > 0 else None
    )

    elapsed_list = metrics["elapsed_ms_list"]
    p50 = sorted(elapsed_list)[len(elapsed_list) // 2] if elapsed_list else None
    p95 = sorted(elapsed_list)[int(len(elapsed_list) * 0.95)] if elapsed_list else None

    summary = {
        "split": split,
        "total_problems": metrics["total"],
        "unsupported": metrics["unsupported"],
        "errors": metrics["errors"],
        # Requirement 1: Response time
        "req1_latency_p50_ms": p50,
        "req1_latency_p95_ms": p95,
        "req1_target_met": p95 is not None and p95 <= 30000,
        # Requirement 2: System accuracy
        "req2_accuracy": round(accuracy, 3),
        "req2_target_met": accuracy >= 0.80,
        # Requirement 3: Hallucination rejection
        "req3_hallucination_rejection": round(hallucination_rejection, 3) if hallucination_rejection else "N/A (run with --inject-wrong)",
        "req3_target_met": hallucination_rejection is not None and hallucination_rejection >= 0.90,
        # Requirement 4: Formalization fidelity
        "req4_fidelity": round(fidelity, 3) if fidelity else None,
        "req4_target_met": fidelity is not None and fidelity >= 0.85,
        # Per-template breakdown
        "per_template": metrics["per_template"],
    }

    return summary


def print_summary(summary: dict) -> None:
    print("\n" + "=" * 70)
    print(f"  VeriMath Evaluation Report — split: {summary['split']}")
    print("=" * 70)
    print(f"  Total problems:      {summary['total_problems']}")
    print(f"  Unsupported:         {summary['unsupported']}")
    print(f"  Errors:              {summary['errors']}")
    print()
    print(f"  Req 1 — Latency p50: {summary['req1_latency_p50_ms']}ms")
    print(f"  Req 1 — Latency p95: {summary['req1_latency_p95_ms']}ms  (target ≤30000ms) {'✅' if summary['req1_target_met'] else '❌'}")
    print(f"  Req 2 — Accuracy:    {summary['req2_accuracy']:.1%}          (target ≥80%)    {'✅' if summary['req2_target_met'] else '❌'}")
    print(f"  Req 3 — Halluc. rej: {summary['req3_hallucination_rejection']}        (target ≥90%)    {'✅' if summary['req3_target_met'] else '❌'}")
    print(f"  Req 4 — Fidelity:    {summary['req4_fidelity']:.1%}          (target ≥85%)    {'✅' if summary['req4_target_met'] else '❌'}")
    print()
    print("  Per-template accuracy:")
    for tid, stats in summary["per_template"].items():
        acc = stats["verified"] / stats["total"] if stats["total"] > 0 else 0
        print(f"    {tid:<30} {stats['verified']}/{stats['total']} ({acc:.0%})")
    print("=" * 70)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VeriMath accuracy evaluation")
    parser.add_argument("--split", choices=["train", "test"], default="test")
    parser.add_argument("--inject-wrong", action="store_true", help="Test hallucination rejection")
    parser.add_argument("--judge-stats", action="store_true", help="Only test formalization fidelity")
    parser.add_argument("--output", type=str, help="Save JSON report to file")
    args = parser.parse_args()

    summary = asyncio.run(evaluate(
        split=args.split,
        inject_wrong=args.inject_wrong,
        judge_only=args.judge_stats,
    ))

    print_summary(summary)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(summary, f, indent=2)
        print(f"\nReport saved to: {args.output}")
