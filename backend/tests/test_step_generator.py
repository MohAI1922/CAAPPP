"""
Unit tests for VeriMath Deterministic Step Generator (El-Moasser Curriculum Standards)
"""

import unittest
from backend.pipeline.step_generator import (
    generate_steps,
    generate_rate_of_change_steps,
    generate_power_rule_steps,
    generate_product_rule_steps,
    generate_quotient_rule_steps,
    generate_chain_rule_steps,
    generate_tangent_line_steps,
    generate_normal_line_steps,
    generate_indefinite_integral_steps,
    generate_definite_integral_steps,
)


class TestStepGenerator(unittest.TestCase):

    def test_rate_of_change_steps(self):
        steps = generate_rate_of_change_steps(
            problem="Find the rate of change of f(x) = x^2 + 2x - 5 using the limit definition",
            f_str="x^2 + 2*x - 5",
            answer="2*x + 2"
        )
        self.assertEqual(len(steps), 3)
        self.assertIn("Variation Function", steps[0].title)
        self.assertIn("Average Rate of Change", steps[1].title)
        self.assertIn("Instantaneous Rate of Change", steps[2].title)
        self.assertTrue(all(s.math for s in steps))

    def test_power_rule_steps(self):
        steps = generate_power_rule_steps(
            problem="Find the derivative of 2x^3 + 3x^2 - 4x + 6",
            expr_str="2*x^3 + 3*x^2 - 4*x + 6",
            answer="6*x^2 + 6*x - 4"
        )
        self.assertEqual(len(steps), 3)
        self.assertIn("Sum and Difference", steps[0].title)
        self.assertIn("Power Rule", steps[1].title)
        self.assertIn("6 x^{2}", steps[1].math)

    def test_product_rule_steps(self):
        steps = generate_product_rule_steps(
            problem="Find the derivative of (x^2 + 3)*(2x^3 - 5)",
            expr_str="(x^2 + 3)*(2*x^3 - 5)",
            answer="10*x^4 + 18*x^2 - 10*x"
        )
        self.assertEqual(len(steps), 4)
        self.assertIn("Component Functions", steps[0].title)
        self.assertIn("Product Rule Formula", steps[2].title)
        self.assertIn("Expand", steps[3].title)

    def test_quotient_rule_steps(self):
        steps = generate_quotient_rule_steps(
            problem="Find the derivative of (3x - 4)/(2x + 5)",
            expr_str="(3*x - 4)/(2*x + 5)",
            answer="23/(2*x + 5)^2"
        )
        self.assertEqual(len(steps), 4)
        self.assertIn("Numerator and Denominator", steps[0].title)
        self.assertIn("Quotient Rule Formula", steps[2].title)
        self.assertIn("23", steps[3].math)

    def test_chain_rule_steps(self):
        steps = generate_chain_rule_steps(
            problem="Find the derivative of (2x - 3)^4",
            expr_str="(2*x - 3)^4",
            answer="8*(2*x - 3)^3"
        )
        self.assertEqual(len(steps), 4)
        self.assertIn("Composite Function", steps[0].title)
        self.assertIn("Chain Rule Theorem", steps[2].title)
        self.assertIn("8", steps[3].math)

    def test_tangent_line_steps(self):
        steps = generate_tangent_line_steps(
            problem="Find the tangent line to y = 3x^2 - 5x + 3 at x = 1",
            curve_str="3*x^2 - 5*x + 3",
            x0_val="1",
            answer="y = x"
        )
        self.assertEqual(len(steps), 4)
        self.assertIn("First Derivative", steps[0].title)
        self.assertIn("Slope of the Tangent", steps[1].title)
        self.assertIn("Equation of the Tangent", steps[3].title)

    def test_normal_line_steps(self):
        steps = generate_normal_line_steps(
            problem="Find the normal line to y = x^2 + 2x - 3 at x = 1",
            curve_str="x^2 + 2*x - 3",
            x0_val="1",
            answer="y = -1/4*(x - 1)"
        )
        self.assertEqual(len(steps), 3)
        self.assertIn("Slope of the Tangent", steps[0].title)
        self.assertIn("Perpendicular Normal", steps[1].title)
        self.assertIn("Equation of the Normal", steps[2].title)

    def test_indefinite_integral_steps(self):
        steps = generate_indefinite_integral_steps(
            problem="Find the indefinite integral of 6x^2 - 4x + 5",
            expr_str="6*x^2 - 4*x + 5",
            answer="2*x^3 - 2*x^2 + 5*x + C"
        )
        self.assertEqual(len(steps), 3)
        self.assertIn("Linearity", steps[0].title)
        self.assertIn("Power Rule", steps[1].title)
        self.assertIn("Constant of Integration", steps[2].title)

    def test_definite_integral_steps(self):
        steps = generate_definite_integral_steps(
            problem="Evaluate the integral of x^2 from 0 to 1",
            expr_str="x^2",
            lower_str="0",
            upper_str="1",
            answer="1/3"
        )
        self.assertEqual(len(steps), 3)
        self.assertIn("Antiderivative", steps[0].title)
        self.assertIn("Fundamental Theorem", steps[1].title)

    def test_trig_derivative_steps(self):
        steps = generate_steps(
            "trig_derivative",
            "Find the derivative of sin(3x^2 + 1)",
            "6*x*cos(3*x^2 + 1)",
            {"expr": "sin(3*x^2 + 1)"}
        )
        self.assertEqual(len(steps), 3)
        self.assertIn("Trigonometric", steps[0].title)
        self.assertIn("Chain Rule", steps[2].title)

    def test_log_exp_derivative_steps(self):
        steps = generate_steps(
            "log_exp_derivative",
            "Find the derivative of e^(2x^3) + ln(x^2 + 1)",
            "6*x^2*e^(2*x^3) + 2*x/(x^2 + 1)",
            {"expr": "e^(2*x^3) + ln(x^2 + 1)"}
        )
        self.assertEqual(len(steps), 3)
        self.assertIn("Chain Rule", steps[1].title)

    def test_logarithmic_differentiation_steps(self):
        steps = generate_steps(
            "logarithmic_differentiation",
            "Find dy/dx for y = x^x",
            "x^x*(ln(x) + 1)",
            {"expr": "x^x"}
        )
        self.assertEqual(len(steps), 4)
        self.assertIn("Natural Logarithm", steps[0].title)
        self.assertIn("Implicitly", steps[2].title)

    def test_critical_points_steps(self):
        steps = generate_steps(
            "critical_points",
            "Find critical points of f(x) = x^3 - 3x",
            "x = -1, x = 1",
            {"f": "x^3 - 3*x"}
        )
        self.assertEqual(len(steps), 3)
        self.assertIn("First Derivative", steps[0].title)
        self.assertIn("Stationary Numbers", steps[1].title)

    def test_absolute_extrema_steps(self):
        steps = generate_steps(
            "absolute_extrema_closed_interval",
            "Find absolute extrema of f(x) = 2x^3 - 3x^2 on [-1, 2]",
            "max = 4 at x = 2, min = -5 at x = -1",
            {"f": "2*x^3 - 3*x^2", "a": "-1", "b": "2"}
        )
        self.assertEqual(len(steps), 3)
        self.assertIn("Open Interval", steps[0].title)
        self.assertIn("Compare Values", steps[2].title)

    def test_integration_by_parts_steps(self):
        steps = generate_steps(
            "integration_by_parts",
            "Integrate x*e^x dx",
            "x*e^x - e^x + C",
            {"expr": "x*e^x"}
        )
        self.assertEqual(len(steps), 4)
        self.assertIn("Select Functions", steps[0].title)
        self.assertIn("Integration by Parts Formula", steps[2].title)

    def test_main_dispatcher(self):
        cases = [
            ("derivative_limit_definition", "rate of change f(x) = x^2", "2*x", {"f": "x^2"}),
            ("power_rule_derivative", "derivative of 5x^2", "10*x", {"expr": "5*x^2"}),
            ("product_rule_derivative", "derivative of x*sin(x)", "sin(x) + x*cos(x)", {"expr": "x*sin(x)"}),
            ("quotient_rule_derivative", "derivative of x/(x+1)", "1/(x+1)^2", {"expr": "x/(x+1)"}),
            ("chain_rule_derivative", "derivative of (x+1)^3", "3*(x+1)^2", {"expr": "(x+1)^3"}),
            ("tangent_line", "tangent to y = x^2 at x = 2", "y = 4*x - 4", {"f": "x^2", "x0": "2"}),
            ("normal_line", "normal to y = x^2 at x = 2", "y - 4 = -1/4*(x - 2)", {"curve": "x^2", "x0": "2"}),
            ("indefinite_integral", "integrate x^3 dx", "x^4/4 + C", {"expr": "x^3"}),
            ("definite_integral", "integral of x from 0 to 2", "2", {"expr": "x", "lower": "0", "upper": "2"}),
            ("trig_derivative", "derivative of cos(2x)", "-2*sin(2x)", {"expr": "cos(2*x)"}),
            ("log_exp_derivative", "derivative of e^(3x)", "3*e^(3*x)", {"expr": "e^(3*x)"}),
            ("logarithmic_differentiation", "derivative of x^x", "x^x*(ln(x) + 1)", {"expr": "x^x"}),
            ("critical_points", "critical points of x^2 - 4x", "x = 2", {"f": "x^2 - 4*x"}),
            ("absolute_extrema_closed_interval", "extrema of x^2 on [-1, 2]", "max = 4, min = 0", {"f": "x^2", "a": "-1", "b": "2"}),
            ("integration_by_parts", "integrate x*cos(x) dx", "x*sin(x) + cos(x) + C", {"expr": "x*cos(x)"}),
            ("kings_rule_integral", "integrate sin(x)/(sin(x)+cos(x)) from 0 to pi/2", "pi/4", {"expr": "sin(x)/(sin(x)+cos(x))", "lower": "0", "upper": "pi/2"}),
            ("pun_integral", "integrate (2x+3)/(x^2+4x+5) dx", "ln(x^2+4x+5) - arctan(x+2) + C", {"expr": "(2*x+3)/(x^2+4*x+5)"}),
            ("root_manipulation_integral", "integrate x*sqrt(x+1) dx", "2*(x+1)^(5/2)/5 - 2*(x+1)^(3/2)/3 + C", {"expr": "x*sqrt(x+1)"}),
            ("inverted_quadratic_integral", "integrate 1/(x^2+2x+5) dx", "arctan((x+1)/2)/2 + C", {"expr": "1/(x^2+2*x+5)"}),
            ("trig_substitution_integral", "integrate sqrt(4 - x^2) dx", "2*arcsin(x/2) + x*sqrt(4-x^2)/2 + C", {"expr": "sqrt(4 - x^2)"}),
            ("partial_fraction_integral", "integrate 1/(x^2 - 1) dx", "ln(abs(x-1))/2 - ln(abs(x+1))/2 + C", {"expr": "1/(x^2 - 1)"}),
            ("long_division_integral", "integrate (x^2+1)/(x+1) dx", "x^2/2 - x + 2*ln(abs(x+1)) + C", {"expr": "(x^2+1)/(x+1)"}),
            ("cyclic_ibp_integral", "integrate e^x*cos(x) dx", "e^x*(sin(x)+cos(x))/2 + C", {"expr": "e^x*cos(x)"}),
            ("tabular_ibp_integral", "integrate x^2*e^x dx", "e^x*(x^2 - 2*x + 2) + C", {"expr": "x^2*e^x"}),
            ("trig_power_reduction_integral", "integrate sin(x)^3 dx", "-cos(x) + cos(x)^3/3 + C", {"expr": "sin(x)^3"}),
            ("wallis_integral", "integrate sin(x)^4 from 0 to pi/2 dx", "3*pi/16", {"expr": "sin(x)^4", "lower": "0", "upper": "pi/2"}),
            ("product_to_sum_trig_integral", "integrate sin(3x)*cos(2x) dx", "-cos(5*x)/10 - cos(x)/2 + C", {"expr": "sin(3*x)*cos(2*x)"}),
            ("weierstrass_substitution_integral", "integrate 1/(1+sin(x)) dx", "-2/(tan(x/2)+1) + C", {"expr": "1/(1+sin(x))"}),
            ("se_one_integral", "integrate cos(x)/(e^x+1) from -pi to pi dx", "0", {"expr": "cos(x)/(e^x+1)", "lower": "-pi", "upper": "pi"}),
            ("feynman_technique_integral", "integrate ln(x^2+1)/(x^2+1) from 0 to 1 dx", "pi*ln(2)/2", {"expr": "ln(x^2+1)/(x^2+1)", "lower": "0", "upper": "1"}),
            ("series_expansion_definite_integral", "integrate ln(1-x)/x from 0 to 1 dx", "-pi^2/6", {"expr": "ln(1-x)/x", "lower": "0", "upper": "1"}),
            ("dilogarithm_integral", "integrate -ln(1-t)/t from 0 to 1 dt", "pi^2/6", {"expr": "-ln(1-x)/x", "lower": "0", "upper": "1"}),
            ("quad_root_trick_integral", "integrate sqrt(x*(x+1)*(x+2)*(x+3)+1) dx", "x^3/3 + 3*x^2/2 + x + C", {"expr": "sqrt(x*(x+1)*(x+2)*(x+3)+1)"}),
            ("euler_formula_integral", "integrate e^(2x)*sin(3x) dx", "e^(2*x)*(2*sin(3*x)-3*cos(3*x))/13 + C", {"expr": "e^(2*x)*sin(3*x)"}),
        ]
        for t_id, prob, ans, slots in cases:
            steps = generate_steps(t_id, prob, ans, slots)
            self.assertGreaterEqual(len(steps), 2, f"Failed for {t_id}")
            self.assertTrue(all(s.title and s.explanation and s.math for s in steps))

    def test_book_of_integrals_individual_generators(self):
        """Test each Book of Integrals generator directly."""
        from backend.pipeline.step_generator import (
            generate_kings_rule_steps,
            generate_pun_integral_steps,
            generate_root_manipulation_steps,
            generate_inverted_quadratic_steps,
            generate_trig_substitution_steps,
            generate_partial_fraction_steps,
            generate_long_division_steps,
            generate_cyclic_ibp_steps,
            generate_tabular_ibp_steps,
            generate_trig_power_reduction_steps,
            generate_wallis_integral_steps,
            generate_product_to_sum_trig_steps,
            generate_weierstrass_substitution_steps,
            generate_se_one_integral_steps,
            generate_feynman_technique_steps,
            generate_series_expansion_steps,
            generate_dilogarithm_steps,
            generate_quad_root_steps,
            generate_euler_formula_steps,
        )

        # 1. King's rule
        k_steps = generate_kings_rule_steps("prob", "sin(x)/(sin(x)+cos(x))", "0", "pi/2", "pi/4")
        self.assertEqual(len(k_steps), 4)
        self.assertIn("King's Rule", k_steps[0].explanation)

        # 2. PUN integral
        pun_steps = generate_pun_integral_steps("prob", "(2*x+3)/(x^2+4*x+5)", "ln(x^2+4*x+5) - arctan(x+2)")
        self.assertEqual(len(pun_steps), 4)
        self.assertIn("P.U.N.", pun_steps[0].explanation)

        # 3. Root manipulation
        root_steps = generate_root_manipulation_steps("prob", "x*sqrt(x+1)", "2*(x+1)**(5/2)/5")
        self.assertEqual(len(root_steps), 4)
        self.assertIn("Root Manipulation", root_steps[0].explanation)

        # 4. Inverted quadratic
        inv_steps = generate_inverted_quadratic_steps("prob", "1/(x^2+2*x+5)", "arctan((x+1)/2)/2")
        self.assertEqual(len(inv_steps), 4)
        self.assertIn("Completing the Square", inv_steps[0].explanation)

        # 5. Trig substitution
        trig_sub_steps = generate_trig_substitution_steps("prob", "sqrt(4 - x^2)", "2*arcsin(x/2)")
        self.assertEqual(len(trig_sub_steps), 4)
        self.assertIn("Trigonometric Substitution", trig_sub_steps[0].explanation)

        # 6. Partial fraction
        pfd_steps = generate_partial_fraction_steps("prob", "1/(x^2 - 1)", "ln(abs(x-1))/2")
        self.assertEqual(len(pfd_steps), 4)
        self.assertIn("Partial Fraction", pfd_steps[0].explanation)

        # 7. Long division
        ld_steps = generate_long_division_steps("prob", "(x^2+1)/(x+1)", "x^2/2 - x")
        self.assertEqual(len(ld_steps), 5)
        self.assertIn("Long Division", ld_steps[0].explanation)

        # 8. Cyclic IBP
        cyc_steps = generate_cyclic_ibp_steps("prob", "e^x*cos(x)", "e^x*(sin(x)+cos(x))/2")
        self.assertEqual(len(cyc_steps), 4)
        self.assertIn("Cyclic", cyc_steps[0].explanation)

        # 9. Tabular IBP
        tab_steps = generate_tabular_ibp_steps("prob", "x^2*e^x", "e^x*(x^2 - 2*x + 2)")
        self.assertEqual(len(tab_steps), 4)
        self.assertIn("Tic-Tac-Toe", tab_steps[0].explanation)

        # 10. Trig power reduction
        tpr_steps = generate_trig_power_reduction_steps("prob", "sin(x)^3", "-cos(x) + cos(x)^3/3")
        self.assertEqual(len(tpr_steps), 4)
        self.assertIn("Power Reduction", tpr_steps[0].explanation)

        # 11. Wallis
        w_steps = generate_wallis_integral_steps("prob", "sin(x)^4", "0", "pi/2", "3*pi/16")
        self.assertEqual(len(w_steps), 3)
        self.assertIn("Wallis", w_steps[0].explanation)

        # 12. Product to sum
        pts_steps = generate_product_to_sum_trig_steps("prob", "sin(3*x)*cos(2*x)", "-cos(5*x)/10")
        self.assertEqual(len(pts_steps), 4)
        self.assertIn("Product-to-Sum", pts_steps[0].explanation)

        # 13. Weierstrass
        ws_steps = generate_weierstrass_substitution_steps("prob", "1/(1+sin(x))", "-2/(tan(x/2)+1)")
        self.assertEqual(len(ws_steps), 4)
        self.assertIn("Weierstrass", ws_steps[0].explanation)

        # 14. SE-One
        se_steps = generate_se_one_integral_steps("prob", "cos(x)/(e^x+1)", "-pi", "pi", "0")
        self.assertEqual(len(se_steps), 4)
        self.assertIn("S.E - One", se_steps[0].explanation)

        # 15. Feynman
        feyn_steps = generate_feynman_technique_steps("prob", "ln(x^2+1)/(x^2+1)", "0", "1", "pi*ln(2)/2")
        self.assertEqual(len(feyn_steps), 4)
        self.assertIn("Feynman", feyn_steps[0].explanation)

        # 16. Series expansion
        ser_steps = generate_series_expansion_steps("prob", "ln(1-x)/x", "0", "1", "-pi^2/6")
        self.assertEqual(len(ser_steps), 4)
        self.assertIn("Series", ser_steps[0].explanation)

        # 17. Dilogarithm
        dilog_steps = generate_dilogarithm_steps("prob", "-ln(1-x)/x", "0", "1", "pi^2/6")
        self.assertEqual(len(dilog_steps), 4)
        self.assertIn("Dilogarithm", dilog_steps[0].explanation)

        # 18. Quad root
        qr_steps = generate_quad_root_steps("prob", "x*(x+1)*(x+2)*(x+3)+1", "x^3/3")
        self.assertEqual(len(qr_steps), 4)
        self.assertIn("Quad-Root", qr_steps[0].explanation)

        # 19. Euler formula
        ef_steps = generate_euler_formula_steps("prob", "e^(2*x)*sin(3*x)", "e^(2*x)*(2*sin(3*x)-3*cos(3*x))/13")
        self.assertEqual(len(ef_steps), 3)
        self.assertIn("Euler's Formula", ef_steps[0].explanation)



    def test_tangent_line_coherence_without_slots(self):
        """Audit Test 1: Verify tangent line at x = 2 has exact slope and point-slope coherence without slots."""
        steps = generate_steps(
            template_id="tangent_line",
            problem="Find the equation of the tangent line to y = x^2 at x = 2",
            answer="y = 4*x - 4",
            slots=None
        )
        self.assertEqual(len(steps), 4)
        # Step 2: slope must be 4 at x = 2
        self.assertIn("x = 2", steps[1].math)
        self.assertIn("4", steps[1].math)
        # Step 3: tangency point must be (2, 4)
        self.assertIn("2", steps[2].math)
        self.assertIn("4", steps[2].math)
        # Step 4: point-slope formula y - 4 = 4(x - 2)
        self.assertIn("y - (4)", steps[3].math)
        self.assertIn("4(x - (2))", steps[3].math)
        self.assertIn("y = 4*x - 4", steps[3].math)

    def test_critical_points_no_truncation_without_slots(self):
        """Audit Test 2: Verify critical points prompt does not truncate expressions with minus/spaces."""
        steps = generate_steps(
            template_id="critical_points",
            problem="Find the critical points of f(x) = x^3 - 3*x",
            answer="x = -1, x = 1",
            slots=None
        )
        self.assertEqual(len(steps), 3)
        # Step 1: full derivative 3*x^2 - 3
        self.assertIn("3 x^{2} - 3", steps[0].math)
        # Step 2: stationary numbers x = -1, x = 1
        self.assertIn("x = -1", steps[1].math)
        self.assertIn("x = 1", steps[1].math)

    def test_definite_integral_non_empty_without_slots(self):
        """Audit Test 3: Definite integral without slots must extract integrand and limits cleanly."""
        steps = generate_steps(
            template_id="definite_integral",
            problem="Evaluate the integral from 0 to 1 of x^2 dx",
            answer="1/3",
            slots=None
        )
        self.assertEqual(len(steps), 3)
        # Step 1: Antiderivative F(x) = x^3/3
        self.assertIn(r"\frac{x^{3}}{3}", steps[0].math)
        self.assertNotIn(r"\int \left(\right)", steps[0].math)
        # Step 2: Bracket [x^3/3]_0^1
        self.assertIn(r"\int_{0}^{1}", steps[1].math)
        self.assertIn(r"\frac{x^{3}}{3}", steps[1].math)
        # Step 3: Bounds difference
        self.assertIn("1/3", steps[2].math)

    def test_chain_rule_concrete_components(self):
        """Audit Test 4: Chain rule identifies inner function and outer function concretely."""
        steps = generate_steps(
            template_id="chain_rule_derivative",
            problem="Find the derivative of (3*x^2 + 5)^4 with respect to x",
            answer="24*x*(3*x^2 + 5)^3",
            slots={"expr": "(3*x^2 + 5)^4"}
        )
        self.assertEqual(len(steps), 4)
        # Step 1: Inner function z = 3x^2 + 5, outer y = z^4
        self.assertIn("3 x^{2} + 5", steps[0].math)
        self.assertIn("z^{4}", steps[0].math)
        # Step 2: dy/dz = 4z^3, dz/dx = 6x
        self.assertIn("4 z^{3}", steps[1].math)
        self.assertIn("6 x", steps[1].math)

    def test_integration_by_parts_liate_concrete(self):
        """Audit Test 5: Integration by Parts performs authentic LIATE decomposition."""
        steps = generate_steps(
            template_id="integration_by_parts",
            problem="Integrate x*e^x dx",
            answer="x*e^x - e^x + C",
            slots={"expr": "x*e^x"}
        )
        self.assertEqual(len(steps), 4)
        # Step 1: u = x, dv = e^x
        self.assertIn("u = x", steps[0].math)
        self.assertIn("e^{x}", steps[0].math)
        # Step 2: du = 1 dx, v = e^x
        self.assertIn("du = 1", steps[1].math)
        self.assertIn("= e^{x}", steps[1].math)
        # Step 3: uv - int v du
        self.assertIn(r"\left(x\right)\left(e^{x}\right)", steps[2].math)

    def test_single_variable_derivative_smart_dispatch(self):
        """Audit Test 6: single_variable_derivative routes to exact textbook rules, not 2-step stub."""
        # Product rule dispatch
        p_steps = generate_steps(
            template_id="single_variable_derivative",
            problem="Find the derivative of x^2 * sin(x) with respect to x",
            answer="2*x*sin(x) + x^2*cos(x)",
            slots=None
        )
        self.assertEqual(len(p_steps), 4)
        self.assertIn("Product Rule", p_steps[2].title)

        # Quotient rule dispatch
        q_steps = generate_steps(
            template_id="single_variable_derivative",
            problem="Find the derivative of (3*x - 4)/(2*x + 5) with respect to x",
            answer="23/(2*x + 5)^2",
            slots=None
        )
        self.assertEqual(len(q_steps), 4)
        self.assertIn("Quotient Rule", q_steps[2].title)

        # Chain rule dispatch
        c_steps = generate_steps(
            template_id="single_variable_derivative",
            problem="Find the derivative of (2*x - 3)^4 with respect to x",
            answer="8*(2*x - 3)^3",
            slots=None
        )
        self.assertEqual(len(c_steps), 4)
        self.assertIn("Chain Rule", c_steps[2].title)


if __name__ == "__main__":
    unittest.main()
