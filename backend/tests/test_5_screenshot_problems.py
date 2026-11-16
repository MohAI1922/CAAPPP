"""
Unit tests for the 5 screenshot problems reported by the user:
1. Semicircle rectangle perimeter maximization
2. Isosceles triangle circumscribed around rectangle min area
3. Ellipse tangent min intercepted segment length
4. Y-shaped road network Steiner junction length minimization
5. Curve f(x) = x^{1/3} and line g(x) = x max vertical distance
"""

import unittest
from backend.templates.registry import classify_problem
from backend.pipeline.solver import solve
from backend.pipeline.formalizer import formalize
from backend.pipeline.statement_judge import judge
from backend.main import to_latex


class TestFiveScreenshotProblems(unittest.TestCase):

    def test_problem_1_semicircle_perimeter(self):
        problem = (
            "A rectangle is inscribed in a semicircle of radius $R = 5\\text{ cm}$ with one of its sides lying along the diameter. "
            "Instead of maximizing area, find the dimensions (width $2x$ and height $y$) that maximize the perimeter of the rectangle."
        )
        # 1. Classification
        t_id = classify_problem(problem)
        self.assertEqual(t_id, "semicircle_inscribed_rectangle_perimeter_optimization")

        # 2. Solver
        s_res = solve(problem)
        self.assertIn("width 2x = 4*sqrt(5) cm", s_res.candidate_answer)
        self.assertIn("height y = sqrt(5) cm", s_res.candidate_answer)
        self.assertIn("maximum perimeter P = 10*sqrt(5) cm", s_res.candidate_answer)

        # 3. Formalizer
        f_res = formalize(problem, s_res, t_id)
        self.assertEqual(f_res.slot_values["R"], "5")
        self.assertEqual(f_res.slot_values["x_sq"], "20")
        self.assertEqual(f_res.slot_values["y_sq"], "5")
        self.assertEqual(f_res.slot_values["W_sq"], "80")
        self.assertEqual(f_res.slot_values["P_sq"], "500")

        # 4. Faithfulness judge
        j_res = judge(problem, f_res)
        self.assertEqual(j_res.verdict, "MATCH")

        # 5. LaTeX formatting
        latex = to_latex(s_res.candidate_answer)
        self.assertIn("P_{\\max}", latex)
        self.assertIn("4 \\sqrt{5}", latex)

    def test_problem_2_triangle_circumscribed_rectangle(self):
        problem = (
            "An isosceles triangle is circumscribed around a rectangle of width $8\\text{ cm}$ and height $3\\text{ cm}$ "
            "(such that the base of the rectangle rests on the base of the triangle, and the top two corners of the rectangle "
            "touch the two slanted sides of the triangle). Find the total height $H$ and base $B$ of the triangle that minimize its area."
        )
        # 1. Classification
        t_id = classify_problem(problem)
        self.assertEqual(t_id, "triangle_circumscribed_rectangle_min_area_optimization")

        # 2. Solver
        s_res = solve(problem)
        self.assertIn("height H = 6 cm", s_res.candidate_answer)
        self.assertIn("base B = 16 cm", s_res.candidate_answer)
        self.assertIn("minimum area A = 48 cm^2", s_res.candidate_answer)

        # 3. Formalizer
        f_res = formalize(problem, s_res, t_id)
        self.assertEqual(f_res.slot_values["w"], "8")
        self.assertEqual(f_res.slot_values["h"], "3")
        self.assertEqual(f_res.slot_values["H"], "6")
        self.assertEqual(f_res.slot_values["B"], "16")
        self.assertEqual(f_res.slot_values["A_min"], "48")

        # 4. Faithfulness judge
        j_res = judge(problem, f_res)
        self.assertEqual(j_res.verdict, "MATCH")

        # 5. LaTeX formatting
        latex = to_latex(s_res.candidate_answer)
        self.assertIn("H = 6", latex)
        self.assertIn("B = 16", latex)
        self.assertIn("A_{\\min} = 48", latex)

    def test_problem_3_ellipse_tangent_segment(self):
        problem = (
            "A tangent line is drawn to the ellipse $\\frac{x^2}{9} + \\frac{y^2}{4} = 1$ at a point $(x_0, y_0)$ in the first quadrant. "
            "Find the minimum possible length $L$ of the segment of the tangent line intercepted between the positive $x$- and $y$-axes."
        )
        # 1. Classification
        t_id = classify_problem(problem)
        self.assertEqual(t_id, "ellipse_tangent_min_intercepted_length_optimization")

        # 2. Solver
        s_res = solve(problem)
        self.assertIn("minimum length L = 5 cm", s_res.candidate_answer)
        self.assertIn("X = sqrt(15) cm", s_res.candidate_answer)
        self.assertIn("Y = sqrt(10) cm", s_res.candidate_answer)

        # 3. Formalizer
        f_res = formalize(problem, s_res, t_id)
        self.assertEqual(f_res.slot_values["a"], "3")
        self.assertEqual(f_res.slot_values["b"], "2")
        self.assertEqual(f_res.slot_values["L_min"], "5")
        self.assertEqual(f_res.slot_values["X_sq"], "15")
        self.assertEqual(f_res.slot_values["Y_sq"], "10")

        # 4. Faithfulness judge
        j_res = judge(problem, f_res)
        self.assertEqual(j_res.verdict, "MATCH")

        # 5. LaTeX formatting
        latex = to_latex(s_res.candidate_answer)
        self.assertIn("L_{\\min} = 5", latex)

    def test_problem_4_y_shaped_road_network(self):
        problem = (
            "Two towns $A$ and $B$ are located $12\\text{ km}$ apart along a straight east-west line, and a third town $C$ is located $10\\text{ km}$ "
            "due north of the midpoint $M$ between $A$ and $B$. An engineer builds a Y-shaped road network: roads run from $A$ and $B$ to a junction "
            "point $P$ located $x\\text{ km}$ north of $M$, and a single road runs from $P$ to $C$. Find the distance $x$ that minimizes the total length of road built."
        )
        # 1. Classification
        t_id = classify_problem(problem)
        self.assertEqual(t_id, "y_shaped_road_network_optimization")

        # 2. Solver
        s_res = solve(problem)
        self.assertIn("2*sqrt(3)", s_res.candidate_answer)
        self.assertIn("10 + 6*sqrt(3)", s_res.candidate_answer)

        # 3. Formalizer
        f_res = formalize(problem, s_res, t_id)
        self.assertEqual(f_res.slot_values["AB"], "12")
        self.assertEqual(f_res.slot_values["d"], "6")
        self.assertEqual(f_res.slot_values["h"], "10")
        self.assertEqual(f_res.slot_values["x_sq"], "12")

        # 4. Faithfulness judge
        j_res = judge(problem, f_res)
        self.assertEqual(j_res.verdict, "MATCH")

        # 5. LaTeX formatting
        latex = to_latex(s_res.candidate_answer)
        self.assertIn("L_{\\min}", latex)

    def test_problem_5_curve_line_vertical_distance(self):
        problem = (
            "On the closed interval $[0, 1]$, find the $x$-coordinate that maximizes the vertical distance between the curve $f(x) = x^{1/3}$ "
            "and the line $g(x) = x$, and find that maximum vertical distance."
        )
        # 1. Classification
        t_id = classify_problem(problem)
        self.assertEqual(t_id, "curve_line_max_vertical_distance_optimization")

        # 2. Solver
        s_res = solve(problem)
        self.assertIn("sqrt(3)/9", s_res.candidate_answer)
        self.assertIn("2*sqrt(3)/9", s_res.candidate_answer)

        # 3. Formalizer
        f_res = formalize(problem, s_res, t_id)
        self.assertEqual(f_res.slot_values["interval"], "[0, 1]")
        self.assertEqual(f_res.slot_values["x_sq"], "1/27")
        self.assertEqual(f_res.slot_values["D_sq"], "4/27")

        # 4. Faithfulness judge
        j_res = judge(problem, f_res)
        self.assertEqual(j_res.verdict, "MATCH")

        # 5. LaTeX formatting
        latex = to_latex(s_res.candidate_answer)
        self.assertIn("D_{\\max}", latex)


if __name__ == "__main__":
    unittest.main()
