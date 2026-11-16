"""
Unit tests for the 5 new screenshot problems:
1. Right circular cone fixed volume lateral area minimization
2. Rancher divided corral budget area maximization
3. Parabola inscribed isosceles triangle with apex at origin max area
4. Open-top cylindrical water tank material cost ratio minimization
5. Exponential curve y = e^{2x} closest point to straight line y = 2x - 3
"""

import unittest
from backend.templates.registry import classify_problem
from backend.pipeline.solver import solve
from backend.pipeline.formalizer import formalize
from backend.pipeline.statement_judge import judge
from backend.main import to_latex


class TestFiveNewScreenshotProblems(unittest.TestCase):

    def test_problem_1_cone_lateral_area(self):
        problem = (
            r"A right circular cone is to be constructed with a fixed volume $V = 36\pi\sqrt{2}\text{ cm}^3$. "
            r"Find the exact base radius $r$ and height $h$ that minimize the lateral surface area $S = \pi r \sqrt{r^2 + h^2}$."
        )
        # 1. Classification
        t_id = classify_problem(problem)
        self.assertEqual(t_id, "cone_fixed_volume_min_lateral_area_optimization")

        # 2. Solver
        s_res = solve(problem)
        self.assertIn("3*4^(1/3)", s_res.candidate_answer)
        self.assertIn("3*sqrt(2)*4^(1/3)", s_res.candidate_answer)

        # 3. Formalizer
        f_res = formalize(problem, s_res, t_id)
        self.assertEqual(f_res.slot_values["r_cube"], "108")
        self.assertIn("norm_num", f_res.lean_statement)

        # 4. Faithfulness judge
        j_res = judge(problem, f_res)
        self.assertEqual(j_res.verdict, "MATCH")

        # 5. LaTeX formatting
        latex = to_latex(s_res.candidate_answer)
        self.assertIn("r =", latex)
        self.assertIn("h =", latex)

    def test_problem_2_rancher_corral_budget(self):
        problem = (
            r"A rancher wants to build a large rectangular corral and divide it into three smaller rectangular pens of equal size "
            r"by placing two interior fences parallel to one of the outer sides. The outer boundary fence costs $\$20\text{ per meter}$, "
            r"while the two lighter interior dividing fences cost $\$10\text{ per meter}$. If the rancher has a total budget of $\$2,400$, "
            r"what overall outer dimensions ($L$ and $W$) will maximize the total enclosed area, and what is that maximum area?"
        )
        # 1. Classification
        t_id = classify_problem(problem)
        self.assertEqual(t_id, "rancher_divided_corral_budget_optimization")

        # 2. Solver
        s_res = solve(problem)
        self.assertIn("L = 30 m", s_res.candidate_answer)
        self.assertIn("W = 20 m", s_res.candidate_answer)
        self.assertIn("maximum area A = 600 m^2", s_res.candidate_answer)

        # 3. Formalizer
        f_res = formalize(problem, s_res, t_id)
        self.assertEqual(f_res.slot_values["L"], "30")
        self.assertEqual(f_res.slot_values["W"], "20")
        self.assertEqual(f_res.slot_values["A_max"], "600")

        # 4. Faithfulness judge
        j_res = judge(problem, f_res)
        self.assertEqual(j_res.verdict, "MATCH")

        # 5. LaTeX formatting
        latex = to_latex(s_res.candidate_answer)
        self.assertIn("A_{\\max} = 600", latex)

    def test_problem_3_parabola_inscribed_triangle_origin(self):
        problem = (
            r"An isosceles triangle is inscribed in the region bounded by the parabola $y = 16 - x^2$ and the $x$-axis, "
            r"such that its apex is at the origin $(0, 0)$ and its horizontal base connects two symmetric points $(-x, y)$ "
            r"and $(x, y)$ on the parabola above the $x$-axis. Find the coordinates $(x, y)$ of the right-hand vertex that "
            r"maximize the area of the triangle, and calculate the maximum area."
        )
        # 1. Classification
        t_id = classify_problem(problem)
        self.assertEqual(t_id, "parabola_inscribed_triangle_origin_apex_optimization")

        # 2. Solver
        s_res = solve(problem)
        self.assertIn("4*sqrt(3)/3", s_res.candidate_answer)
        self.assertIn("32/3", s_res.candidate_answer)
        self.assertIn("128*sqrt(3)/9", s_res.candidate_answer)

        # 3. Formalizer
        f_res = formalize(problem, s_res, t_id)
        self.assertEqual(f_res.slot_values["H"], "16")
        self.assertEqual(f_res.slot_values["x_sq"], "16/3")
        self.assertEqual(f_res.slot_values["y_exact"], "32/3")

        # 4. Faithfulness judge
        j_res = judge(problem, f_res)
        self.assertEqual(j_res.verdict, "MATCH")

        # 5. LaTeX formatting
        latex = to_latex(s_res.candidate_answer)
        self.assertIn("A_{\\max}", latex)

    def test_problem_4_open_top_cylinder_cost(self):
        problem = (
            r"An open-top cylindrical water tank (flat circular bottom, curved vertical side, no roof) must hold a fixed volume "
            r"of $64\pi\text{ m}^3$. If the material for the circular bottom costs three times as much per square meter as the "
            r"material for the curved vertical wall, find the radius $r$ and height $h$ that minimize the total material cost."
        )
        # 1. Classification
        t_id = classify_problem(problem)
        self.assertEqual(t_id, "open_top_cylinder_material_cost_ratio_optimization")

        # 2. Solver
        s_res = solve(problem)
        self.assertIn("4/3^(1/3)", s_res.candidate_answer)
        self.assertIn("4*3^(2/3)", s_res.candidate_answer)

        # 3. Formalizer
        f_res = formalize(problem, s_res, t_id)
        self.assertEqual(f_res.slot_values["V_num"], "64")
        self.assertEqual(f_res.slot_values["r_cube"], "64/3")

        # 4. Faithfulness judge
        j_res = judge(problem, f_res)
        self.assertEqual(j_res.verdict, "MATCH")

        # 5. LaTeX formatting
        latex = to_latex(s_res.candidate_answer)
        self.assertIn("r =", latex)
        self.assertIn("h =", latex)

    def test_problem_5_curve_closest_point_to_line(self):
        problem = (
            r"Find the point $(x_0, y_0)$ on the exponential curve $y = e^{2x}$ that is closest to the straight line $y = 2x - 3$, "
            r"and determine the exact perpendicular distance between that point and the line."
        )
        # 1. Classification
        t_id = classify_problem(problem)
        self.assertEqual(t_id, "curve_closest_point_to_line_optimization")

        # 2. Solver
        s_res = solve(problem)
        self.assertIn("point (0, 1)", s_res.candidate_answer)
        self.assertIn("4*sqrt(5)/5", s_res.candidate_answer)

        # 3. Formalizer
        f_res = formalize(problem, s_res, t_id)
        self.assertEqual(f_res.slot_values["x0"], "0")
        self.assertEqual(f_res.slot_values["y0"], "1")

        # 4. Faithfulness judge
        j_res = judge(problem, f_res)
        self.assertEqual(j_res.verdict, "MATCH")

        # 5. LaTeX formatting
        latex = to_latex(s_res.candidate_answer)
        self.assertIn("d_{\\min}", latex)
        self.assertIn("(x_0, y_0) = \\left(0, 1\\right)", latex)


if __name__ == "__main__":
    unittest.main()
