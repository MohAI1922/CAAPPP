"""
Unit tests for the 5 latest failure problems reported by user:
1. Trapezoid channel with 3 equal sides of length L = 10 cm maximizing area
2. Ellipse circumscribed around rectangle 8 cm by 6 cm minimizing area
3. Parabola y = 12 - x^2 tangent line intercepts sum OA + OB minimization
4. Right circular cone inscribed in hemisphere R = 6 cm maximizing volume
5. Inventory EOQ microcontroller batch size cost minimization (D = 12000, K = 150, H = 4)
"""

import unittest
from backend.templates.registry import classify_problem
from backend.pipeline.solver import solve
from backend.pipeline.formalizer import formalize
from backend.pipeline.statement_judge import judge
from backend.pipeline.lean_runner import verify
from backend.main import to_latex


class TestFiveLatestFailureProblems(unittest.TestCase):

    def test_problem_1_trapezoid_channel_max_area(self):
        problem = (
            "A water channel has a cross-section in the shape of an isosceles trapezoid whose bottom and two slanted sides each have a length of $10\\text{ cm}$. "
            "If $\\theta$ is the angle that each slanted side makes with the horizontal ($0 < \\theta < \\frac{\\pi}{2}$), what angle $\\theta$ (or upper width $B$) "
            "maximizes the cross-sectional area, and what is that maximum area?"
        )
        # 1. Classification
        t_id = classify_problem(problem)
        self.assertEqual(t_id, "trapezoid_three_equal_sides_max_area_optimization")

        # 2. Solver
        s_res = solve(problem)
        self.assertIn("theta = pi/3", s_res.candidate_answer)
        self.assertIn("B = 20 cm", s_res.candidate_answer)
        self.assertIn("75*sqrt(3) cm^2", s_res.candidate_answer)

        # 3. Formalizer
        f_res = formalize(problem, s_res, t_id)
        self.assertEqual(f_res.slot_values["L"], "10")
        self.assertEqual(f_res.slot_values["B"], "20")
        self.assertEqual(f_res.slot_values["h_exact"], "5*Real.sqrt 3")
        self.assertEqual(f_res.slot_values["A_max_exact"], "75*Real.sqrt 3")

        # 4. Lean verification
        v_res = verify(f_res.lean_statement)
        self.assertEqual(v_res.verdict, "VERIFIED")

        # 5. Faithfulness judge
        j_res = judge(problem, f_res)
        self.assertEqual(j_res.verdict, "MATCH")

        # 6. KaTeX formatting
        latex = to_latex(s_res.candidate_answer)
        self.assertIn(r"\theta = \frac{\pi}{3}", latex)
        self.assertIn(r"B = 20\text{ cm}", latex)
        self.assertIn(r"A_{\max} = 75 \sqrt{3}\text{ cm}^2", latex)

    def test_problem_2_ellipse_circumscribed_rectangle(self):
        problem = (
            "An ellipse centered at the origin with horizontal semi-axis $a$ and vertical semi-axis $b$ is circumscribed around a rectangle of dimensions "
            "$8\\text{ cm}$ by $6\\text{ cm}$ (so the rectangle vertices at $(\\pm 4, \\pm 3)$ lie on the ellipse: $\\frac{16}{a^2} + \\frac{9}{b^2} = 1$). "
            "What semi-axes $a$ and $b$ minimize the area of the circumscribed ellipse, and what is that minimum area?"
        )
        # 1. Classification
        t_id = classify_problem(problem)
        self.assertEqual(t_id, "ellipse_circumscribed_rectangle_min_area_optimization")

        # 2. Solver
        s_res = solve(problem)
        self.assertIn("a = 4*sqrt(2) cm", s_res.candidate_answer)
        self.assertIn("b = 3*sqrt(2) cm", s_res.candidate_answer)
        self.assertIn("24*pi cm^2", s_res.candidate_answer)

        # 3. Formalizer
        f_res = formalize(problem, s_res, t_id)
        self.assertEqual(f_res.slot_values["W"], "8")
        self.assertEqual(f_res.slot_values["H"], "6")
        self.assertEqual(f_res.slot_values["a_exact"], "4*Real.sqrt 2")
        self.assertEqual(f_res.slot_values["b_exact"], "3*Real.sqrt 2")
        self.assertEqual(f_res.slot_values["A_min_exact"], "24*Real.pi")

        # 4. Lean verification
        v_res = verify(f_res.lean_statement)
        self.assertEqual(v_res.verdict, "VERIFIED")

        # 5. Faithfulness judge
        j_res = judge(problem, f_res)
        self.assertEqual(j_res.verdict, "MATCH")

        # 6. KaTeX formatting
        latex = to_latex(s_res.candidate_answer)
        self.assertIn(r"a = 4 \sqrt{2}\text{ cm}", latex)
        self.assertIn(r"b = 3 \sqrt{2}\text{ cm}", latex)
        self.assertIn(r"A_{\min} = 24 \pi\text{ cm}^2", latex)

    def test_problem_3_parabola_tangent_intercepts(self):
        problem = (
            "A tangent line is drawn to the parabola $y = 12 - x^2$ at a point $P(x_0, y_0)$ in the first quadrant ($x_0 > 0, y_0 > 0$). "
            "The tangent line intersects the positive $x$-axis at $A$ and the positive $y$-axis at $B$. "
            "Find the coordinates of $P(x_0, y_0)$ that minimize the sum of the intercepts $OA + OB$, and calculate that minimum sum."
        )
        # 1. Classification
        t_id = classify_problem(problem)
        self.assertEqual(t_id, "parabola_tangent_intercepts_min_sum_optimization")

        # 2. Solver
        s_res = solve(problem)
        self.assertIn("1.3635", s_res.candidate_answer)
        self.assertIn("10.1407", s_res.candidate_answer)
        self.assertIn("18.9413", s_res.candidate_answer)

        # 3. Formalizer
        f_res = formalize(problem, s_res, t_id)
        self.assertEqual(f_res.slot_values["c"], "12")
        self.assertEqual(f_res.slot_values["x0_val"], "1.3635")
        self.assertEqual(f_res.slot_values["y0_val"], "10.1407")
        self.assertEqual(f_res.slot_values["S_min_approx"], "18.9413")

        # 4. Lean verification
        v_res = verify(f_res.lean_statement)
        self.assertEqual(v_res.verdict, "VERIFIED")

        # 5. Faithfulness judge
        j_res = judge(problem, f_res)
        self.assertEqual(j_res.verdict, "MATCH")

        # 6. KaTeX formatting
        latex = to_latex(s_res.candidate_answer)
        self.assertIn(r"\left(1.3635, 10.1407\right)", latex)
        self.assertIn(r"\left(OA + OB\right)_{\min} \approx 18.9413", latex)

    def test_problem_4_hemisphere_inscribed_cone(self):
        problem = (
            "A right circular cone is inscribed in a hemisphere of fixed radius $R = 6\\text{ cm}$ such that its base lies on the circular flat base of the hemisphere "
            "and its vertex touches the curved spherical surface. What base radius $r$ and height $h$ maximize the volume of the cone, and what is that maximum volume?"
        )
        # 1. Classification
        t_id = classify_problem(problem)
        self.assertEqual(t_id, "hemisphere_inscribed_cone_max_volume_optimization")

        # 2. Solver
        s_res = solve(problem)
        self.assertIn("2*sqrt(6) cm", s_res.candidate_answer)
        self.assertIn("2*sqrt(3) cm", s_res.candidate_answer)
        self.assertIn("16*sqrt(3)*pi cm^3", s_res.candidate_answer)

        # 3. Formalizer
        f_res = formalize(problem, s_res, t_id)
        self.assertEqual(f_res.slot_values["R"], "6")
        self.assertEqual(f_res.slot_values["r_exact"], "2*Real.sqrt 6")
        self.assertEqual(f_res.slot_values["h_exact"], "2*Real.sqrt 3")
        self.assertEqual(f_res.slot_values["V_max_exact"], "16*Real.sqrt 3 * Real.pi")

        # 4. Lean verification
        v_res = verify(f_res.lean_statement)
        self.assertEqual(v_res.verdict, "VERIFIED")

        # 5. Faithfulness judge
        j_res = judge(problem, f_res)
        self.assertEqual(j_res.verdict, "MATCH")

        # 6. KaTeX formatting
        latex = to_latex(s_res.candidate_answer)
        self.assertIn(r"r = 2 \sqrt{6}\text{ cm}", latex)
        self.assertIn(r"h = 2 \sqrt{3}\text{ cm}", latex)
        self.assertIn(r"V_{\max} = 16 \sqrt{3} \pi\text{ cm}^3", latex)

    def test_problem_5_inventory_eoq(self):
        problem = (
            "A hardware startup manufactures IoT devices and needs 12,000 microcontroller chips per year. The fixed setup and ordering cost for each production batch is $150, "
            "and the annual holding/storage cost per chip is $4. What batch size $x$ minimizes the total annual inventory cost "
            "$C(x) = \\frac{12000 \\times 150}{x} + 4 \\left(\\frac{x}{2}\\right)$, and what is that minimum annual cost?"
        )
        # 1. Classification
        t_id = classify_problem(problem)
        self.assertEqual(t_id, "inventory_eoq_batch_size_cost_optimization")

        # 2. Solver
        s_res = solve(problem)
        self.assertIn("300*sqrt(10)", s_res.candidate_answer)
        self.assertIn("949", s_res.candidate_answer)
        self.assertIn("1200*sqrt(10)", s_res.candidate_answer)

        # 3. Formalizer
        f_res = formalize(problem, s_res, t_id)
        self.assertEqual(f_res.slot_values["D"], "12000")
        self.assertEqual(f_res.slot_values["K"], "150")
        self.assertEqual(f_res.slot_values["H"], "4")
        self.assertEqual(f_res.slot_values["x_exact"], "300*Real.sqrt (10)")
        self.assertEqual(f_res.slot_values["C_min_exact"], "1200*Real.sqrt (10)")

        # 4. Lean verification
        v_res = verify(f_res.lean_statement)
        self.assertEqual(v_res.verdict, "VERIFIED")

        # 5. Faithfulness judge
        j_res = judge(problem, f_res)
        self.assertEqual(j_res.verdict, "MATCH")

        # 6. KaTeX formatting
        latex = to_latex(s_res.candidate_answer)
        self.assertIn(r"x^* = 300 \sqrt{10}", latex)
        self.assertIn(r"C_{\min} = \text{\$}1200 \sqrt{10}", latex)


if __name__ == "__main__":
    unittest.main()
