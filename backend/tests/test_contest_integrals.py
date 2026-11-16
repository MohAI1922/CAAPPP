"""
Unit tests for general-purpose definite integral solving and Lean verification.
Verifies that contest and advanced integrals evaluate correctly via PSLQ / King's rule / quadrature
without hanging or hardcoding one-off cases.
"""

import unittest
import asyncio
from backend.pipeline.solver import solve
from backend.pipeline.formalizer import formalize
from backend.pipeline.lean_runner import verify_async
from backend.templates.registry import classify_problem


class TestContestIntegrals(unittest.TestCase):
    def _test_problem(self, problem: str, expected_substr: str):
        sol = solve(problem)
        self.assertIn(expected_substr, sol.candidate_answer, f"Failed on: {problem}")

        cat = classify_problem(problem) or "definite_integral"
        form = formalize(problem, sol, cat)
        
        ver = asyncio.run(verify_async(form.lean_statement))
        self.assertEqual(ver.verdict.value, "VERIFIED", f"Verification rejected: {ver.lean_output}")

    def test_arccos_rational_trig_contest(self):
        # The user's exact problem
        self._test_problem(
            "Evaluate the definite integral of arccos(cos(x) / (1 + 2 * cos(x))) from 0 to pi/2",
            "5*pi^2/24"
        )

    def test_serret_putnam_log_tan(self):
        self._test_problem(
            "Evaluate the definite integral of ln(1 + tan(x)) from 0 to pi/4",
            "pi*log(2)/8"
        )

    def test_euler_catalan_log_sin_cos(self):
        self._test_problem(
            "Evaluate the definite integral of ln(sin(x) + cos(x)) from 0 to pi/2",
            "Catalan"
        )

    def test_quartic_trig_rational(self):
        self._test_problem(
            "Evaluate the definite integral of cos(x)^2 / (cos(x)^2 + 4 * sin(x)^2)^2 from 0 to pi/2",
            "pi/8"
        )

    def test_kings_rule_symmetric_fraction(self):
        self._test_problem(
            "Evaluate the definite integral of sin(x) / (sin(x) + cos(x)) from 0 to pi/2",
            "pi/4"
        )

    def test_rational_standard_integral(self):
        self._test_problem(
            "Evaluate the definite integral of 1 / (1 + x^2) from 0 to 1",
            "pi/4"
        )

    def test_polynomial_integral(self):
        self._test_problem(
            "Evaluate the definite integral of x^2 from 0 to 2",
            "8/3"
        )

    def test_non_elementary_never_hangs(self):
        sol = solve("Evaluate the definite integral of exp(-x^2) from 0 to 1")
        self.assertTrue(sol.candidate_answer.startswith("~") or "0.7468" in sol.candidate_answer)


if __name__ == "__main__":
    unittest.main()
