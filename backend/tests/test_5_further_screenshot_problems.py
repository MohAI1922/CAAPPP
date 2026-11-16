"""
Unit tests for the 5 further screenshot problems:
1. Rectangular sheet box volume maximization (16 cm by 30 cm)
2. Norman window fixed area minimum perimeter (A = 8 + 2*pi m^2)
3. Inscribed inverted cone in larger cone max volume (R = 6 cm, H = 12 cm)
4. Hyperbola xy = 8 tangent line minimum intercepted segment length AB
5. Substation cable cost minimization / Snell's law (A(0, 4) to B(10, 0))
"""

import unittest
from backend.templates.registry import classify_problem
from backend.pipeline.solver import solve
from backend.pipeline.formalizer import formalize
from backend.pipeline.statement_judge import judge
from backend.pipeline.lean_runner import verify
from backend.main import to_latex


class TestFiveFurtherScreenshotProblems(unittest.TestCase):

    def test_problem_1_rectangular_sheet_box_volume(self):
        problem = (
            "An open-top box is made from a rectangular sheet of metal measuring 16 cm by 30 cm "
            "by cutting out equal squares of side length x from each of the four corners and bending up the sides. "
            "Find the value of x that maximizes the volume of the box, and calculate that maximum volume."
        )
        # 1. Classification
        t_id = classify_problem(problem)
        self.assertEqual(t_id, "rectangular_sheet_box_volume_optimization")

        # 2. Solver
        s_res = solve(problem)
        self.assertIn("10/3", s_res.candidate_answer)
        self.assertIn("19600/27", s_res.candidate_answer)

        # 3. Formalizer
        f_res = formalize(problem, s_res, t_id)
        self.assertEqual(f_res.slot_values["W"], "16")
        self.assertEqual(f_res.slot_values["L"], "30")
        self.assertEqual(f_res.slot_values["x_exact"], "10/3")
        self.assertEqual(f_res.slot_values["V_max_exact"], "19600/27")

        # 4. Lean verification
        v_res = verify(f_res.lean_statement)
        self.assertEqual(v_res.verdict, "VERIFIED")

        # 5. Faithfulness judge
        j_res = judge(problem, f_res)
        self.assertEqual(j_res.verdict, "MATCH")

        # 6. KaTeX formatting
        latex = to_latex(s_res.candidate_answer)
        self.assertIn("V_{\\max}", latex)
        self.assertIn(r"\frac{10}{3}", latex)

    def test_problem_2_norman_window_fixed_area(self):
        problem = (
            r"A Norman window consists of a rectangle of width 2r and height h surmounted by a semicircle of radius r. "
            r"If the total area of the window is fixed at A = 8 + 2\pi m^2, find the radius r and rectangle height h "
            r"that minimize the total outer perimeter of the window."
        )
        # 1. Classification
        t_id = classify_problem(problem)
        self.assertEqual(t_id, "norman_window_fixed_area_min_perimeter_optimization")

        # 2. Solver
        s_res = solve(problem)
        self.assertIn("r = 2 m", s_res.candidate_answer)
        self.assertIn("h = 2 m", s_res.candidate_answer)
        self.assertIn("8 + 2*pi", s_res.candidate_answer)

        # 3. Formalizer
        f_res = formalize(problem, s_res, t_id)
        self.assertEqual(f_res.slot_values["r"], "2")
        self.assertEqual(f_res.slot_values["h"], "2")

        # 4. Lean verification
        v_res = verify(f_res.lean_statement)
        self.assertEqual(v_res.verdict, "VERIFIED")

        # 5. Faithfulness judge
        j_res = judge(problem, f_res)
        self.assertEqual(j_res.verdict, "MATCH")

        # 6. KaTeX formatting
        latex = to_latex(s_res.candidate_answer)
        self.assertIn("P_{\\min}", latex)

    def test_problem_3_cone_inscribed_inverted_cone(self):
        problem = (
            "A right circular cone is inscribed upside-down inside a larger right circular cone of base radius R = 6 cm "
            "and height H = 12 cm, such that the vertex (apex) of the inscribed cone sits at the center of the base "
            "of the larger cone, and the circular base of the inscribed cone is parallel to the base of the larger cone. "
            "Find the radius r and height h of the inscribed cone that maximize its volume, and find that maximum volume."
        )
        # 1. Classification
        t_id = classify_problem(problem)
        self.assertEqual(t_id, "cone_inscribed_inverted_cone_max_volume_optimization")

        # 2. Solver
        s_res = solve(problem)
        self.assertIn("r = 4 cm", s_res.candidate_answer)
        self.assertIn("h = 4 cm", s_res.candidate_answer)
        self.assertIn("64*pi/3", s_res.candidate_answer)

        # 3. Formalizer
        f_res = formalize(problem, s_res, t_id)
        self.assertEqual(f_res.slot_values["R"], "6")
        self.assertEqual(f_res.slot_values["H"], "12")
        self.assertEqual(f_res.slot_values["r"], "4")
        self.assertEqual(f_res.slot_values["h"], "4")

        # 4. Lean verification
        v_res = verify(f_res.lean_statement)
        self.assertEqual(v_res.verdict, "VERIFIED")

        # 5. Faithfulness judge
        j_res = judge(problem, f_res)
        self.assertEqual(j_res.verdict, "MATCH")

        # 6. KaTeX formatting
        latex = to_latex(s_res.candidate_answer)
        self.assertIn("V_{\\max}", latex)

    def test_problem_4_hyperbola_tangent_min_length(self):
        problem = (
            "A line is tangent to the hyperbola xy = 8 at a point (x_0, y_0) in the first quadrant (x_0 > 0). "
            "The tangent line intersects the positive x-axis at point A and the positive y-axis at point B. "
            "Find the coordinates (x_0, y_0) that minimize the length of the line segment AB, and state that minimum length."
        )
        # 1. Classification
        t_id = classify_problem(problem)
        self.assertEqual(t_id, "hyperbola_tangent_min_segment_length_optimization")

        # 2. Solver
        s_res = solve(problem)
        self.assertIn("2*sqrt(2)", s_res.candidate_answer)
        self.assertIn("minimum length AB = 8", s_res.candidate_answer)

        # 3. Formalizer
        f_res = formalize(problem, s_res, t_id)
        self.assertEqual(f_res.slot_values["k"], "8")
        self.assertEqual(f_res.slot_values["L_min"], "8")

        # 4. Lean verification
        v_res = verify(f_res.lean_statement)
        self.assertEqual(v_res.verdict, "VERIFIED")

        # 5. Faithfulness judge
        j_res = judge(problem, f_res)
        self.assertEqual(j_res.verdict, "MATCH")

        # 6. KaTeX formatting
        latex = to_latex(s_res.candidate_answer)
        self.assertIn("L_{\\min} = 8", latex)

    def test_problem_5_cable_pipeline_cost_snell(self):
        problem = (
            "Suppose substation A is at (0, 4), substation B is at (10, 0) along the x-axis, "
            "and P(x, 0) lies on the x-axis between (0, 0) and (10, 0). Cable from A(0, 4) to P(x, 0) "
            "runs diagonally underground at $50,000/km, and cable from P(x, 0) to B(10, 0) runs along the road at $30,000/km. "
            "Find x to minimize total cable cost, and calculate that minimum cost."
        )
        # 1. Classification
        t_id = classify_problem(problem)
        self.assertEqual(t_id, "cable_pipeline_cost_minimization")

        # 2. Solver
        s_res = solve(problem)
        self.assertIn("x = 3 km", s_res.candidate_answer)
        self.assertIn("460,000", s_res.candidate_answer)

        # 3. Formalizer
        f_res = formalize(problem, s_res, t_id)
        self.assertEqual(f_res.slot_values["x"], "3")
        self.assertEqual(f_res.slot_values["AP"], "5")
        self.assertEqual(f_res.slot_values["min_cost"], "460000")

        # 4. Lean verification
        v_res = verify(f_res.lean_statement)
        self.assertEqual(v_res.verdict, "VERIFIED")

        # 5. Faithfulness judge
        j_res = judge(problem, f_res)
        self.assertEqual(j_res.verdict, "MATCH")

        # 6. KaTeX formatting
        latex = to_latex(s_res.candidate_answer)
        self.assertIn("C_{\\min} = \\$460,000", latex)
