"""
End-to-end and unit tests for VeriMath pipeline
"""

import unittest
from backend.pipeline.solver import solve, SolverResult
from backend.pipeline.formalizer import formalize
from backend.pipeline.statement_judge import judge
from backend.pipeline.cache import init_db, get, put, clear
from backend.templates.registry import get_template

class TestPipeline(unittest.TestCase):
    def test_cache_lifecycle(self):
        import os
        from backend.pipeline import cache
        old_cache_path = cache.CACHE_PATH
        test_db = os.path.normpath(os.path.join(os.path.dirname(__file__), "test_cache.db"))
        cache.CACHE_PATH = test_db
        try:
            cache.init_db()
            cache.clear()
            self.assertIsNone(cache.get("What is 9999 + 9999?"))

            cache.put(
                problem="What is 9999 + 9999?",
                template_id="arithmetic",
                verified_answer="19998",
                lean_statement="example : 9999 + 9999 = 19998 := by norm_num",
                back_translation="Compute 9999 + 9999. The answer should be 19998.",
                explanation="Nine thousand nine hundred ninety-nine plus nine thousand nine hundred ninety-nine equals nineteen thousand nine hundred ninety-eight.",
                elapsed_ms=10,
            )

            cached = cache.get("What is 9999 + 9999?")
            self.assertIsNotNone(cached)
            self.assertEqual(cached.verified_answer, "19998")
            self.assertEqual(cached.template_id, "arithmetic")
        finally:
            cache.CACHE_PATH = old_cache_path
            if os.path.exists(test_db):
                try:
                    os.remove(test_db)
                except Exception:
                    pass

    def test_solver_mock_fallback(self):
        # When llama-cpp-python or model is missing, solver uses fallback mock
        res = solve("Find the derivative of x^2")
        self.assertIsInstance(res, SolverResult)
        self.assertIsNotNone(res.candidate_answer)

    def test_statement_judge_match(self):
        solver_res = SolverResult(
            candidate_answer="5",
            lean_answer="5",
            reasoning="3x + 7 = 22 => x = 5",
            confidence="high",
            elapsed_ms=10,
        )
        tmpl = get_template("equation_solving")
        formalizer_res = formalize("Solve 3x + 7 = 22", solver_res, "equation_solving")
        judge_res = judge("Solve 3x + 7 = 22", formalizer_res)

        self.assertEqual(judge_res.verdict, "MATCH")
        self.assertGreaterEqual(judge_res.similarity_score, 0.45)

    def test_advanced_derivatives(self):
        res1 = solve("Find the derivative of ln(x) x^2 with respect to x")
        self.assertIn("ln", res1.candidate_answer)
        self.assertIn("log", res1.lean_answer)

        res2 = solve("Find the derivative of x^2 cos(2x) with respect to x")
        self.assertIn("sin", res2.candidate_answer)
        self.assertIn("cos", res2.candidate_answer)

    def test_statement_judge_function_mismatch(self):
        from backend.pipeline.formalizer import FormalizerResult
        # Dropping 'ln' from problem should trigger MISMATCH
        fake_fr = FormalizerResult(
            lean_statement="example (x : ℝ) : deriv (fun x => x^2) x = 2*x := by simp; ring",
            template_id="derivative",
            slot_values={"expr": "x^2", "answer": "2*x"},
            attempts=1,
            elapsed_ms=5.0,
        )
        jres = judge("Find the derivative of ln(x) x^2 with respect to x", fake_fr)
        self.assertEqual(jres.verdict, "MISMATCH")
        self.assertIn("ln", jres.reason)

    def test_indefinite_integral_with_uppercase_var(self):
        res = solve("integrate 1/(X^2 + 5)")
        self.assertIn("arctan", res.candidate_answer)
        self.assertIn("arctan", res.lean_answer)

    def test_to_latex_conversion(self):
        from backend.main import to_latex
        # Indefinite integral with arctan and + C
        latex_int = to_latex("sqrt(3)*arctan(sqrt(3)*x/3)/3 + C")
        self.assertIn(r"\arctan", latex_int)
        self.assertIn(r"\sqrt{3}", latex_int)
        self.assertTrue(latex_int.endswith("+ C"))

        # Derivative with sin and cos
        latex_deriv = to_latex("-2*x**2*sin(2*x) + 2*x*cos(2*x)")
        self.assertIn(r"\sin", latex_deriv)
        self.assertIn(r"\cos", latex_deriv)

        # Quadratic equation
        latex_quad = to_latex("x = -4 \\lor x = 3")
        self.assertIn(r"\text{or}", latex_quad)

        # Fractions
        latex_frac = to_latex("1/3")
        self.assertEqual(latex_frac, r"\frac{1}{3}")

        # Rates with pi and units
        latex_rate = to_latex("1/pi m/min (~0.3183 m/min)")
        self.assertIn(r"\frac{1}{\pi}", latex_rate)
        self.assertIn(r"\text{ m/min}", latex_rate)
        self.assertIn(r"\approx 0.3183", latex_rate)

    def test_solve_with_feedback(self):
        from backend.pipeline.solver import _build_prompt
        prompt_with_fb = _build_prompt(
            "Solve 3x + 7 = 22",
            feedback="The candidate answer '4' was REJECTED by Lean 4. Please correct the calculation."
        )
        self.assertIn("[PREVIOUS VERIFICATION FEEDBACK - CORRECTION REQUIRED]", prompt_with_fb)
        self.assertIn("REJECTED by Lean 4", prompt_with_fb)

    def test_conical_tank_pipeline_e2e(self):
        import asyncio
        from backend.main import solve_endpoint, SolveRequest
        req = SolveRequest(
            problem=(
                "A conical water tank is shaped like an inverted cone (point down). "
                "The tank has a height of 10 meters and a top radius of 5 meters. "
                "Water is being pumped into the tank at a constant rate of 9 cubic meters per minute. "
                "How fast is the water level rising at the exact moment when the water is 6 meters deep?"
            )
        )
        resp = asyncio.run(solve_endpoint(req))
        self.assertEqual(resp.status, "VERIFIED")
        self.assertEqual(resp.template_id, "conical_tank_rates")
        self.assertIn("1/pi m/min", resp.verified_answer)
        self.assertIn(r"\frac{1}{\pi}", resp.latex_answer)

    def test_orthogonal_motion_pipeline_e2e(self):
        import asyncio
        from backend.main import solve_endpoint, SolveRequest
        req = SolveRequest(
            problem=(
                "Two cars start moving from the same intersection. Car A travels north at 30 miles per hour, "
                "and Car B travels east at 40 miles per hour. How fast is the straight-line distance between the two "
                "cars increasing exactly 2 hours after they start?"
            )
        )
        resp = asyncio.run(solve_endpoint(req))
        self.assertEqual(resp.status, "VERIFIED")
        self.assertEqual(resp.template_id, "orthogonal_motion_rates")
        self.assertEqual(resp.verified_answer, "50 mph")
        self.assertIn(r"50\text{ mph}", resp.latex_answer)

    def test_streetlamp_shadow_pipeline_e2e(self):
        import asyncio
        from backend.main import solve_endpoint, SolveRequest
        req = SolveRequest(
            problem=(
                "A streetlamp is mounted at the top of a 15-foot-tall pole. A boy who is 5 feet tall walks straight away "
                "from the pole at a constant speed of 6 feet per second. How fast is the length of his shadow changing when "
                "he is 40 feet away from the pole?"
            )
        )
        resp = asyncio.run(solve_endpoint(req))
        self.assertEqual(resp.status, "VERIFIED")
        self.assertEqual(resp.template_id, "streetlamp_shadow_rates")
        self.assertEqual(resp.verified_answer, "3 ft/s")
        self.assertIn(r"3\text{ ft/s}", resp.latex_answer)

if __name__ == "__main__":
    unittest.main()
