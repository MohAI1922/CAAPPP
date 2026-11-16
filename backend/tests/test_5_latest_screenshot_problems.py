"""
Unit tests for the 5 latest screenshot problems:
1. Friction pull angle force minimization (W = 100 N, mu = 0.75)
2. Rectangle inscribed between two horizontal parabolas (x = y^2 - 6 and x = 6 - y^2)
3. Cone with fixed slant height L = 6*sqrt(3) cm maximizing volume
4. Curves maximum vertical distance between f(x) = 6*sqrt(x) and g(x) = x^2 - 4x on [0, 4]
5. Painting viewing angle maximization (Regiomontanus: h = 5 m, a = 4 m, b = 9 m)
"""

import unittest
from backend.templates.registry import classify_problem
from backend.pipeline.solver import solve
from backend.pipeline.formalizer import formalize
from backend.pipeline.statement_judge import judge
from backend.pipeline.lean_runner import verify
from backend.main import to_latex


class TestFiveLatestScreenshotProblems(unittest.TestCase):

    def test_problem_1_friction_pull_angle(self):
        problem = (
            "A heavy block of weight $W = 100\\text{ N}$ rests on a rough horizontal floor with a coefficient of static friction $\\mu = 0.75$ ($\\frac{3}{4}$). "
            "A rope attached to the block is pulled upward at an angle $\\theta$ ($0 \\le \\theta \\le \\frac{\\pi}{2}$) above the horizontal. "
            "By balancing horizontal and vertical forces at the verge of slipping, the tension force $F(\\theta)$ required to start moving the block is: "
            "$$F(\\theta) = \\frac{\\mu W}{\\cos\\theta + \\mu\\sin\\theta} = \\frac{75}{\\cos\\theta + 0.75\\sin\\theta}$$ "
            "Find the pulling angle $\\theta$ (or $\\tan\\theta$) that minimizes the required force $F$, and calculate that minimum force."
        )
        # 1. Classification
        t_id = classify_problem(problem)
        self.assertEqual(t_id, "friction_pull_angle_force_minimization")

        # 2. Solver
        s_res = solve(problem)
        self.assertIn("tan(theta) = 3/4", s_res.candidate_answer)
        self.assertIn("60 N", s_res.candidate_answer)

        # 3. Formalizer
        f_res = formalize(problem, s_res, t_id)
        self.assertEqual(f_res.slot_values["W"], "100")
        self.assertIn(f_res.slot_values["mu"], ["0.75", "3/4"])
        self.assertEqual(f_res.slot_values["tan_theta_exact"], "3/4")
        self.assertEqual(f_res.slot_values["F_min_exact"], "60")

        # 4. Lean verification
        v_res = verify(f_res.lean_statement)
        self.assertEqual(v_res.verdict, "VERIFIED")

        # 5. Faithfulness judge
        j_res = judge(problem, f_res)
        self.assertEqual(j_res.verdict, "MATCH")

        # 6. KaTeX formatting
        latex = to_latex(s_res.candidate_answer)
        self.assertIn(r"\tan\theta", latex)
        self.assertIn(r"F_{\min} = 60\text{ N}", latex)

    def test_problem_2_rectangle_between_two_horizontal_parabolas(self):
        problem = (
            "Find the dimensions (width and height) and the maximum area of a rectangle (with sides parallel to the coordinate axes) "
            "that can be inscribed inside the closed lens-shaped region bounded by the two horizontal parabolas $x = y^2 - 6$ and $x = 6 - y^2$."
        )
        # 1. Classification
        t_id = classify_problem(problem)
        self.assertEqual(t_id, "rectangle_between_two_horizontal_parabolas_optimization")

        # 2. Solver
        s_res = solve(problem)
        self.assertIn("W = 8", s_res.candidate_answer)
        self.assertIn("2*sqrt(2)", s_res.candidate_answer)
        self.assertIn("16*sqrt(2)", s_res.candidate_answer)

        # 3. Formalizer
        f_res = formalize(problem, s_res, t_id)
        self.assertEqual(f_res.slot_values["a"], "6")
        self.assertEqual(f_res.slot_values["W"], "8")
        self.assertEqual(f_res.slot_values["H_exact"], "2*Real.sqrt 2")
        self.assertEqual(f_res.slot_values["A_max_exact"], "16*sqrt(2)")

        # 4. Lean verification
        v_res = verify(f_res.lean_statement)
        self.assertEqual(v_res.verdict, "VERIFIED")

        # 5. Faithfulness judge
        j_res = judge(problem, f_res)
        self.assertEqual(j_res.verdict, "MATCH")

        # 6. KaTeX formatting
        latex = to_latex(s_res.candidate_answer)
        self.assertIn("W = 8", latex)
        self.assertIn(r"H = 2 \sqrt{2}", latex)
        self.assertIn(r"A_{\max} = 16 \sqrt{2}", latex)

    def test_problem_3_cone_fixed_slant_height(self):
        problem = (
            "A right circular cone has a fixed base radius $R = 6\\text{ cm}$ and height $H = 8\\text{ cm}$. "
            "That single cone actually fixes its inscribed sphere-so instead, suppose a family of right circular cones all have a fixed slant height $L = 6\\text{ cm}$, "
            "and we want to choose the cone's base radius $R$ and height $H$ to maximize its total surface area? "
            "Even better: suppose a right circular cone has a fixed slant height $L = 6\\sqrt{3}\\text{ cm}$. "
            "What base radius $r$ and height $h$ maximize the volume of the cone, and what is that maximum volume?"
        )
        # 1. Classification
        t_id = classify_problem(problem)
        self.assertEqual(t_id, "cone_fixed_slant_height_max_volume_optimization")

        # 2. Solver
        s_res = solve(problem)
        self.assertIn("6*sqrt(2)", s_res.candidate_answer)
        self.assertIn("h = 6", s_res.candidate_answer)
        self.assertIn("144*pi", s_res.candidate_answer)

        # 3. Formalizer
        f_res = formalize(problem, s_res, t_id)
        self.assertEqual(f_res.slot_values["h_exact"], "6")
        self.assertEqual(f_res.slot_values["r_exact"], "6*Real.sqrt 2")
        self.assertEqual(f_res.slot_values["V_max_exact"], "144*Real.pi")

        # 4. Lean verification
        v_res = verify(f_res.lean_statement)
        self.assertEqual(v_res.verdict, "VERIFIED")

        # 5. Faithfulness judge
        j_res = judge(problem, f_res)
        self.assertEqual(j_res.verdict, "MATCH")

        # 6. KaTeX formatting
        latex = to_latex(s_res.candidate_answer)
        self.assertIn(r"r = 6 \sqrt{2}\text{ cm}", latex)
        self.assertIn(r"h = 6\text{ cm}", latex)
        self.assertIn(r"V_{\max} = 144 \pi\text{ cm}^3", latex)

    def test_problem_4_curves_maximum_vertical_distance(self):
        problem = (
            "On the closed interval $[0, 4]$, the curve $f(x) = 6\\sqrt{x}$ lies above the parabola $g(x) = x^2 - 4x$ (at least for part of the interval). "
            "Find the $x$-coordinate in $[0, 4]$ that maximizes the vertical distance $D(x) = f(x) - g(x)$ between the two curves, and calculate that maximum vertical distance."
        )
        # 1. Classification
        t_id = classify_problem(problem)
        self.assertEqual(t_id, "curves_maximum_vertical_distance_optimization")

        # 2. Solver
        s_res = solve(problem)
        self.assertIn("2.8834", s_res.candidate_answer)
        self.assertIn("13.4080", s_res.candidate_answer)

        # 3. Formalizer
        f_res = formalize(problem, s_res, t_id)
        self.assertEqual(f_res.slot_values["x_val"], "2.8834")
        self.assertEqual(f_res.slot_values["D_val"], "13.4080")

        # 4. Lean verification
        v_res = verify(f_res.lean_statement)
        self.assertEqual(v_res.verdict, "VERIFIED")

        # 5. Faithfulness judge
        j_res = judge(problem, f_res)
        self.assertEqual(j_res.verdict, "MATCH")

        # 6. KaTeX formatting
        latex = to_latex(s_res.candidate_answer)
        self.assertIn(r"x \approx 2.8834", latex)
        self.assertIn(r"D_{\max} \approx 13.4080", latex)

    def test_problem_5_painting_viewing_angle(self):
        problem = (
            "A painting $5\\text{ meters}$ tall hangs on a vertical wall such that its lower edge is $4\\text{ meters}$ above an observer's eye level "
            "(so its upper edge is $9\\text{ meters}$ above eye level). How far ($x$) from the wall should the observer stand to maximize the vertical viewing angle "
            "$\\theta$ subtended by the painting at the observer's eye, and what is the tangent of that maximum angle ($\\tan\\theta$)?"
        )
        # 1. Classification
        t_id = classify_problem(problem)
        self.assertEqual(t_id, "painting_viewing_angle_maximization")

        # 2. Solver
        s_res = solve(problem)
        self.assertIn("x = 6 meters", s_res.candidate_answer)
        self.assertIn("tan(theta) = 5/12", s_res.candidate_answer)

        # 3. Formalizer
        f_res = formalize(problem, s_res, t_id)
        self.assertEqual(f_res.slot_values["x"], "6")
        self.assertEqual(f_res.slot_values["tan_theta_exact"], "5/12")

        # 4. Lean verification
        v_res = verify(f_res.lean_statement)
        self.assertEqual(v_res.verdict, "VERIFIED")

        # 5. Faithfulness judge
        j_res = judge(problem, f_res)
        self.assertEqual(j_res.verdict, "MATCH")

        # 6. KaTeX formatting
        latex = to_latex(s_res.candidate_answer)
        self.assertIn(r"x = 6\text{ meters}", latex)
        self.assertIn(r"\tan\theta = \frac{5}{12}", latex)


if __name__ == "__main__":
    unittest.main()
