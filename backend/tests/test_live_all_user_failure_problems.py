"""
Test Suite for All 13 User Failure Problems and Curriculum Generalizations
Validates the full VeriMath pipeline end-to-end:
classify_problem -> solve -> formalize -> verify -> judge -> to_latex.
"""
import unittest
from backend.templates.registry import classify_problem, get_template
from backend.pipeline.solver import solve
from backend.pipeline.formalizer import formalize
from backend.pipeline.lean_runner import verify
from backend.pipeline.statement_judge import judge
from backend.main import to_latex


class TestAllUserFailureProblems(unittest.TestCase):

    def test_p1_spherical_balloon_rate(self):
        p = "A spherical balloon is being inflated. Find the rate of change of its volume $V$ with respect to time when the radius is $4 \\text{ cm}$, if the radius is increasing at a rate of $2 \\text{ cm/min}$."
        t_id = classify_problem(p)
        self.assertEqual(t_id, "spherical_expansion_rates")
        s = solve(p)
        self.assertIn("128*pi", s.candidate_answer)
        f = formalize(p, s, t_id)
        j = judge(p, f)
        self.assertEqual(j.verdict, "MATCH")
        v = verify(f.lean_statement)
        self.assertEqual(v.verdict.value, "VERIFIED")
        latex = to_latex(s.candidate_answer)
        self.assertIn(r"\frac{dV}{dt}", latex)

    def test_p2_circular_puddle_rate(self):
        p = "A circular puddle of water is expanding. The radius $r$ of the puddle is growing at a rate of $3 \\text{ cm/s}$. How fast is the area $A$ of the puddle increasing when the radius is $5 \\text{ cm}$?"
        t_id = classify_problem(p)
        self.assertEqual(t_id, "circular_expansion_rates")
        s = solve(p)
        self.assertIn("30*pi", s.candidate_answer)
        f = formalize(p, s, t_id)
        j = judge(p, f)
        self.assertEqual(j.verdict, "MATCH")
        v = verify(f.lean_statement)
        self.assertEqual(v.verdict.value, "VERIFIED")
        latex = to_latex(s.candidate_answer)
        self.assertIn(r"\frac{dA}{dt}", latex)

    def test_p3_arctan_half_angle_trig_derivative(self):
        p = "Find the derivative of arctan( sqrt((1 - cos(x)) / (1 + cos(x))) ) with respect to x"
        t_id = classify_problem(p)
        self.assertEqual(t_id, "derivative")
        s = solve(p)
        self.assertEqual(s.candidate_answer.strip(), "1/2")
        f = formalize(p, s, t_id)
        j = judge(p, f)
        self.assertEqual(j.verdict, "MATCH")
        latex = to_latex(s.candidate_answer)
        self.assertIn(r"\frac{1}{2}", latex)

    def test_p4_implicit_folium_derivative(self):
        p = "Find the derivative of x^3 + y^3 - 3axy with respect to x"
        t_id = classify_problem(p)
        self.assertEqual(t_id, "implicit_derivative")
        s = solve(p)
        self.assertIn("dy/dx", s.candidate_answer)
        self.assertIn("ay - x^2", s.candidate_answer)
        f = formalize(p, s, t_id)
        j = judge(p, f)
        self.assertEqual(j.verdict, "MATCH")
        latex = to_latex(s.candidate_answer)
        self.assertIn(r"\frac{dy}{dx}", latex)

    def test_p5_1_cone_inscribed_cylinder_symbolic(self):
        p = "A right circular cone has height H and base radius R. Find the dimensions (radius r and height h) of the right circular cylinder of maximum volume that can be inscribed in the cone."
        t_id = classify_problem(p)
        self.assertEqual(t_id, "cone_inscribed_cylinder_optimization")
        s = solve(p)
        self.assertIn("(2/3)R", s.candidate_answer)
        self.assertIn("(1/3)H", s.candidate_answer)
        f = formalize(p, s, t_id)
        j = judge(p, f)
        self.assertEqual(j.verdict, "MATCH")
        v = verify(f.lean_statement)
        self.assertEqual(v.verdict.value, "VERIFIED")
        latex = to_latex(s.candidate_answer)
        self.assertIn(r"\frac{2}{3}R", latex)
        self.assertIn(r"\frac{1}{3}H", latex)

    def test_p5_2_lifeguard_snell_angle_condition(self):
        p = "A swimmer in distress at point B in the ocean is a distance 'b' from the shoreline, offset horizontally by a total distance 'L'. The lifeguard runs on land at speed v1 and swims at speed v2 (where v1 > v2). Find the condition on the angles theta1 (running path to shore normal) and theta2 (swimming path to shore normal) that minimizes the total travel time."
        t_id = classify_problem(p)
        self.assertEqual(t_id, "lifeguard_snell_angle_condition_optimization")
        s = solve(p)
        self.assertIn("sin(theta1)/v1 = sin(theta2)/v2", s.candidate_answer)
        f = formalize(p, s, t_id)
        j = judge(p, f)
        self.assertEqual(j.verdict, "MATCH")
        v = verify(f.lean_statement)
        self.assertEqual(v.verdict.value, "VERIFIED")
        latex = to_latex(s.candidate_answer)
        self.assertIn(r"\sin", latex)

    def test_p6_riverbank_pasture_fencing(self):
        p = "A farmer has 120 meters of fencing to enclose a rectangular plot of land along a straight riverbank. No fence is needed along the river. Find the dimensions that maximize the enclosed area."
        t_id = classify_problem(p)
        self.assertEqual(t_id, "farmer_fence_optimization")
        s = solve(p)
        self.assertIn("30 m", s.candidate_answer)
        self.assertIn("60 m", s.candidate_answer)
        self.assertIn("1800", s.candidate_answer)
        f = formalize(p, s, t_id)
        j = judge(p, f)
        self.assertEqual(j.verdict, "MATCH")
        v = verify(f.lean_statement)
        self.assertEqual(v.verdict.value, "VERIFIED")
        latex = to_latex(s.candidate_answer)
        self.assertIn("1800", latex)

    def test_p7_p8_line_closest_to_origin(self):
        p1 = "Find the point $(x, y)$ on the line $y = 2x + 1$ closest to the origin $(0, 0)$."
        t_id1 = classify_problem(p1)
        self.assertEqual(t_id1, "line_closest_point_optimization")
        s1 = solve(p1)
        self.assertIn("-2/5", s1.candidate_answer)
        self.assertIn("1/5", s1.candidate_answer)
        f1 = formalize(p1, s1, t_id1)
        j1 = judge(p1, f1)
        self.assertEqual(j1.verdict, "MATCH")
        v1 = verify(f1.lean_statement)
        self.assertEqual(v1.verdict.value, "VERIFIED")

        p2 = "Find the point on the line y = 2x + 1 that is closest to the origin point."
        t_id2 = classify_problem(p2)
        self.assertEqual(t_id2, "line_closest_point_optimization")
        s2 = solve(p2)
        self.assertIn("-2/5", s2.candidate_answer)
        self.assertIn("1/5", s2.candidate_answer)
        f2 = formalize(p2, s2, t_id2)
        j2 = judge(p2, f2)
        self.assertEqual(j2.verdict, "MATCH")
        v2 = verify(f2.lean_statement)
        self.assertEqual(v2.verdict.value, "VERIFIED")

    def test_p9_p10_sum_power_product(self):
        p1 = "Two positive numbers x and y satisfy x + y = 12. Find x and y such that the product P = x * y^2 is maximized."
        t_id1 = classify_problem(p1)
        self.assertEqual(t_id1, "sum_power_product_optimization")
        s1 = solve(p1)
        self.assertIn("x = 4", s1.candidate_answer)
        self.assertIn("y = 8", s1.candidate_answer)
        self.assertIn("256", s1.candidate_answer)
        f1 = formalize(p1, s1, t_id1)
        j1 = judge(p1, f1)
        self.assertEqual(j1.verdict, "MATCH")
        v1 = verify(f1.lean_statement)
        self.assertEqual(v1.verdict.value, "VERIFIED")

        p2 = "Two positive numbers satisfy x + y = 12. Maximize P = x * y^2."
        t_id2 = classify_problem(p2)
        self.assertEqual(t_id2, "sum_power_product_optimization")
        s2 = solve(p2)
        self.assertIn("x = 4", s2.candidate_answer)
        self.assertIn("y = 8", s2.candidate_answer)
        self.assertIn("256", s2.candidate_answer)
        f2 = formalize(p2, s2, t_id2)
        j2 = judge(p2, f2)
        self.assertEqual(j2.verdict, "MATCH")
        v2 = verify(f2.lean_statement)
        self.assertEqual(v2.verdict.value, "VERIFIED")

    def test_p11_top_parabola_rectangle(self):
        p = "A rectangle has its lower edge on the x-axis and its upper vertices on $y = 12 - x^2$. Find the dimensions that maximize its area."
        t_id = classify_problem(p)
        self.assertEqual(t_id, "parabola_inscribed_rectangle_optimization")
        s = solve(p)
        self.assertIn("width = 4", s.candidate_answer)
        self.assertIn("height = 8", s.candidate_answer)
        self.assertIn("32", s.candidate_answer)
        f = formalize(p, s, t_id)
        j = judge(p, f)
        self.assertEqual(j.verdict, "MATCH")
        v = verify(f.lean_statement)
        self.assertEqual(v.verdict.value, "VERIFIED")

    def test_p11_bot_asymmetric_street_fence_cost(self):
        p = "A rectangular area of $1200 \\text{ m}^2$ requires fencing. One side (length $x$) faces a street and costs $\$15\\text{/m}$, while the remaining three sides (one of length $x$ and two of length $y$) cost $\$5\\text{/m}$. Find the dimensions that minimize total cost"
        t_id = classify_problem(p)
        self.assertEqual(t_id, "garden_cost_optimization")
        s = solve(p)
        self.assertIn("10*sqrt(6)", s.candidate_answer)
        self.assertIn("20*sqrt(6)", s.candidate_answer)
        self.assertIn("400*sqrt(6)", s.candidate_answer)
        f = formalize(p, s, t_id)
        j = judge(p, f)
        self.assertEqual(j.verdict, "MATCH")
        v = verify(f.lean_statement)
        self.assertEqual(v.verdict.value, "VERIFIED")

    def test_p12_top_cylinder_material_cost_ratio(self):
        p = "A closed cylinder has volume $V = 54\\pi \\text{ cm}^3$. The circular ends (top and bottom) cost $\$3\\text{/cm}^2$, and the curved lateral side costs $\$2\\text{/cm}^2$. Minimize the total material cost"
        t_id = classify_problem(p)
        self.assertEqual(t_id, "can_material_cost_ratio_optimization")
        s = solve(p)
        self.assertIn("18^(1/3)", s.candidate_answer)
        self.assertIn("3*18^(1/3)", s.candidate_answer)
        f = formalize(p, s, t_id)
        j = judge(p, f)
        self.assertEqual(j.verdict, "MATCH")
        v = verify(f.lean_statement)
        self.assertEqual(v.verdict.value, "VERIFIED")

    def test_p12_bot_rectangular_partition_fence_cost(self):
        p = "A rectangular area of $600\\text{ m}^2$ has an exterior perimeter fence costing $\$10\\text{/m}$ and one interior partition parallel to side $y$ costing $\$6\\text{/m}$. Minimize the total cost."
        t_id = classify_problem(p)
        self.assertEqual(t_id, "rectangular_area_partition_fence_cost_optimization")
        s = solve(p)
        self.assertIn("2*sqrt(195)", s.candidate_answer)
        self.assertIn("80*sqrt(195)", s.candidate_answer)
        f = formalize(p, s, t_id)
        j = judge(p, f)
        self.assertEqual(j.verdict, "MATCH")
        v = verify(f.lean_statement)
        self.assertEqual(v.verdict.value, "VERIFIED")
        latex = to_latex(s.candidate_answer)
        self.assertIn(r"\sqrt", latex)

    def test_p13_open_box_cost(self):
        p1 = "An open-top box with a square base of side $x$ and height $y$ holds $4\\text{ m}^3$. The base material costs $\$6\\text{/m}^2$, and the four sides cost $\$3\\text{/m}^2$. Minimize the total cost."
        t_id1 = classify_problem(p1)
        self.assertEqual(t_id1, "open_box_cost_optimization")
        s1 = solve(p1)
        self.assertIn("2^(2/3)", s1.candidate_answer)
        self.assertIn("36*2^(1/3)", s1.candidate_answer)
        f1 = formalize(p1, s1, t_id1)
        j1 = judge(p1, f1)
        self.assertEqual(j1.verdict, "MATCH")
        v1 = verify(f1.lean_statement)
        self.assertEqual(v1.verdict.value, "VERIFIED")

        p2 = "An open-top storage box with a square base of side length x and height y must have a volume of 4 m^3. The material for the bottom base costs $6 per m^2, while the material for the four vertical sides costs $3 per m^2. Find the dimensions of the box that minimize the total cost."
        t_id2 = classify_problem(p2)
        self.assertEqual(t_id2, "open_box_cost_optimization")
        s2 = solve(p2)
        self.assertIn("2^(2/3)", s2.candidate_answer)
        self.assertIn("36*2^(1/3)", s2.candidate_answer)
        f2 = formalize(p2, s2, t_id2)
        j2 = judge(p2, f2)
        self.assertEqual(j2.verdict, "MATCH")
        v2 = verify(f2.lean_statement)
        self.assertEqual(v2.verdict.value, "VERIFIED")


if __name__ == "__main__":
    unittest.main()
