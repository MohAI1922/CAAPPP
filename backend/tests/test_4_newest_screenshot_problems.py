"""
Unit tests for the 4 newest screenshot problems:
1. Sphere inscribed closed cylinder maximizing total surface area (R = sqrt(5) cm)
2. Tangent line to curve y = 4/x^2 minimizing sum of coordinate intercepts OA + OB
3. Delivery drone airspeed minimizing battery energy against headwind (D = 30 km, w = 10 km/h, P(v) = v^2 + 300 Wh/h)
4. Semicircle of radius R = 2 cm inscribed in isosceles triangle minimizing area
"""

import unittest
from backend.templates.registry import classify_problem
from backend.pipeline.solver import solve
from backend.pipeline.formalizer import formalize
from backend.pipeline.statement_judge import judge
from backend.pipeline.lean_runner import verify
from backend.main import to_latex


class TestFourNewestScreenshotProblems(unittest.TestCase):

    def test_problem_1_sphere_inscribed_closed_cylinder(self):
        problem = (
            r"A right circular cylinder of radius $r$ and height $h$ is inscribed inside a sphere of fixed radius $R = \sqrt{5}\text{ cm}$. "
            r"Find the cylinder radius $r$ and height $h$ that maximize the total surface area of the closed cylinder "
            r"(including both circular ends and the curved side: $S = 2\pi r^2 + 2\pi r h$), and calculate that maximum surface area."
        )
        # 1. Classification
        t_id = classify_problem(problem)
        self.assertEqual(t_id, "sphere_inscribed_closed_cylinder_total_surface_area_optimization")

        # 2. Solver
        s_res = solve(problem)
        self.assertIn("1.9021", s_res.candidate_answer)
        self.assertIn("2.3511", s_res.candidate_answer)
        self.assertIn("50.8320", s_res.candidate_answer)

        # 3. Formalizer
        f_res = formalize(problem, s_res, t_id)
        self.assertEqual(f_res.slot_values["R_sq"], "5")
        self.assertEqual(f_res.slot_values["r_val"], "1.9021")
        self.assertEqual(f_res.slot_values["h_val"], "2.3511")
        self.assertEqual(f_res.slot_values["S_val"], "50.8320")

        # 4. Lean verification
        v_res = verify(f_res.lean_statement)
        self.assertEqual(v_res.verdict, "VERIFIED")

        # 5. Faithfulness judge
        j_res = judge(problem, f_res)
        self.assertEqual(j_res.verdict, "MATCH")

        # 6. KaTeX formatting
        latex = to_latex(s_res.candidate_answer)
        self.assertIn(r"r =", latex)
        self.assertIn(r"h =", latex)
        self.assertIn(r"S_{\max}", latex)

    def test_problem_2_curve_tangent_intercepts_min_sum(self):
        problem = (
            r"Consider the curve $y = 4/x^2$ in the first quadrant ($x_0 > 0$). "
            r"A tangent line drawn at $(x_0, y_0)$ intersects the positive $x$-axis at $A$ and the positive $y$-axis at $B$. "
            r"Find the exact coordinates $(x_0, y_0)$ that minimize the sum of the two intercepts ($OA + OB$), and calculate that minimum sum."
        )
        # 1. Classification
        t_id = classify_problem(problem)
        self.assertEqual(t_id, "curve_tangent_intercepts_min_sum_optimization")

        # 2. Solver
        s_res = solve(problem)
        self.assertIn("2*2^(1/3)", s_res.candidate_answer)
        self.assertIn("1/4^(1/3)", s_res.candidate_answer)
        self.assertIn("9*2^(1/3)/2", s_res.candidate_answer)

        # 3. Formalizer
        f_res = formalize(problem, s_res, t_id)
        self.assertEqual(f_res.slot_values["c"], "4")
        self.assertEqual(f_res.slot_values["x0_cubed"], "16")
        self.assertEqual(f_res.slot_values["three_x0_cubed"], "48")
        self.assertEqual(f_res.slot_values["x0_val"], "2.5198")
        self.assertEqual(f_res.slot_values["y0_val"], "0.6300")
        self.assertEqual(f_res.slot_values["S_min_val"], "5.6696")

        # 4. Lean verification
        v_res = verify(f_res.lean_statement)
        self.assertEqual(v_res.verdict, "VERIFIED")

        # 5. Faithfulness judge
        j_res = judge(problem, f_res)
        self.assertEqual(j_res.verdict, "MATCH")

        # 6. KaTeX formatting
        latex = to_latex(s_res.candidate_answer)
        self.assertIn(r"(x_0, y_0)", latex)
        self.assertIn(r"S_{\min}", latex)

    def test_problem_3_delivery_drone_headwind_energy(self):
        problem = (
            r"A delivery drone flies a fixed horizontal distance of $D = 30\text{ km}$ directly against a steady headwind of $w = 10\text{ km/h}$. "
            r"When the drone flies at an airspeed of $v\text{ km/h}$ relative to the air ($v > 10$), its ground speed is $(v - 10)\text{ km/h}$, "
            r"and its power draw is $P(v) = (v^2 + 300)\text{ Wh/hour}$. "
            r"What airspeed $v$ minimizes the total battery energy $E(v)$ consumed over the $30\text{ km}$ trip, and how many Watt-hours does the trip use?"
        )
        # 1. Classification
        t_id = classify_problem(problem)
        self.assertEqual(t_id, "delivery_drone_headwind_energy_optimization")

        # 2. Solver
        s_res = solve(problem)
        self.assertIn("30 km/h", s_res.candidate_answer)
        self.assertIn("1800 Wh", s_res.candidate_answer)

        # 3. Formalizer
        f_res = formalize(problem, s_res, t_id)
        self.assertEqual(f_res.slot_values["D"], "30")
        self.assertEqual(f_res.slot_values["w"], "10")
        self.assertEqual(f_res.slot_values["F"], "300")
        self.assertEqual(f_res.slot_values["v_opt"], "30")
        self.assertEqual(f_res.slot_values["T_opt"], "1.5")
        self.assertEqual(f_res.slot_values["P_opt"], "1200")
        self.assertEqual(f_res.slot_values["E_min"], "1800")

        # 4. Lean verification
        v_res = verify(f_res.lean_statement)
        self.assertEqual(v_res.verdict, "VERIFIED")

        # 5. Faithfulness judge
        j_res = judge(problem, f_res)
        self.assertEqual(j_res.verdict, "MATCH")

        # 6. KaTeX formatting
        latex = to_latex(s_res.candidate_answer)
        self.assertIn(r"v = 30\text{ km/h}", latex)
        self.assertIn(r"E_{\min} = 1800\text{ Wh}", latex)

    def test_problem_4_semicircle_circumscribed_isosceles_triangle(self):
        problem = (
            r"A semicircle of radius $R = 2\text{ cm}$ rests with its flat diameter along the base of an isosceles triangle, "
            r"and the two equal slanted sides of the triangle are tangent to the curved arc of the semicircle. "
            r"If $\theta \in (0, \pi/2)$ is the base angle of the isosceles triangle, find the angle $\theta$ (or its trig ratios) "
            r"that minimizes the total area of the circumscribed isosceles triangle, and calculate that minimum area."
        )
        # 1. Classification
        t_id = classify_problem(problem)
        self.assertEqual(t_id, "semicircle_circumscribed_isosceles_triangle_min_area_optimization")

        # 2. Solver
        s_res = solve(problem)
        self.assertIn("pi/4", s_res.candidate_answer)
        self.assertIn("45 deg", s_res.candidate_answer)
        self.assertIn("8 cm^2", s_res.candidate_answer)

        # 3. Formalizer
        f_res = formalize(problem, s_res, t_id)
        self.assertEqual(f_res.slot_values["R"], "2")
        self.assertEqual(f_res.slot_values["R_sq"], "4")
        self.assertEqual(f_res.slot_values["theta_exact"], "pi/4")
        self.assertEqual(f_res.slot_values["A_min"], "8")

        # 4. Lean verification
        v_res = verify(f_res.lean_statement)
        self.assertEqual(v_res.verdict, "VERIFIED")

        # 5. Faithfulness judge
        j_res = judge(problem, f_res)
        self.assertEqual(j_res.verdict, "MATCH")

        # 6. KaTeX formatting
        latex = to_latex(s_res.candidate_answer)
        self.assertIn(r"\frac{\pi}{4}", latex)
        self.assertIn(r"A_{\min} = 8", latex)


if __name__ == "__main__":
    unittest.main()
