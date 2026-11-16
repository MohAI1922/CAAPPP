"""
Unit tests for VeriMath Template Registry and Classifiers
"""

import unittest
from backend.templates.registry import (
    TEMPLATES,
    classify_problem,
    get_template,
    fill_template,
    get_back_translation,
)

class TestTemplateRegistry(unittest.TestCase):
    def test_all_templates_registered(self):
        expected_ids = {
            "arithmetic",
            "algebraic_simplification",
            "equation_solving",
            "quadratic_equation",
            "derivative",
            "definite_integral",
            "indefinite_integral",
            "related_rates",
            "orthogonal_motion_rates",
            "streetlamp_shadow_rates",
            "streetlamp_shadow_tip_rates",
            "cylindrical_tank_rates",
            "rectangle_rates",
            "spherical_expansion_rates",
            "spherical_surface_rates",
            "cube_expansion_rates",
            "circular_expansion_rates",
            "conical_tank_rates",
            "conical_tank_pump_leak_rates",
            "conical_pile_rates",
            "trough_rates",
            "kite_string_rates",
            "pulley_boat_rates",
            "rocket_elevation_rates",
            "tracking_distance_rates",
            "ladder_angle_rates",
            "number_theory",
            "geometry_distance",
            "spherical_volume_surface_rates",
            "ladder_area_rates",
            "cube_diagonal_rates",
            "trapezoidal_trough_rates",
            "searchlight_rotation_rates",
            "clock_hands_distance_rates",
            "triangle_angle_area_rates",
            "painting_viewing_angle_rates",
            "streetlamp_shadow_dual_rates",
            "skew_3d_motion_rates",
            "non_orthogonal_motion_rates",
            "cylinder_volume_surface_rates",
            "ladder_perimeter_rates",
            "square_diagonal_rates",
            "triangle_angle_third_side_rates",
            "cone_volume_base_rates",
            "cube_diagonal_surface_rates",
            "tangent_line",
            "critical_points",
            "extrema_points",
            "inflection_points",
            "kings_rule_integral",
            "box_volume_optimization",
            "farmer_fence_optimization",
            "product_sum_optimization",
            "rectangle_perimeter_optimization",
            "parabola_closest_point_optimization",
            "divided_pen_optimization",
            "poster_margin_optimization",
            "open_top_cylinder_optimization",
            "product_power_optimization",
            "parabola_inscribed_rectangle_optimization",
            "garden_cost_optimization",
            "open_box_square_base_optimization",
            "semicircle_inscribed_rectangle_optimization",
            "sum_weighted_squares_optimization",
            "closed_cylinder_optimization",
            "norman_window_optimization",
            "wire_cut_square_circle_optimization",
            "sphere_inscribed_cylinder_optimization",
            "cone_inscribed_cylinder_optimization",
            "ladder_over_fence_optimization",
            "number_square_diff_optimization",
            "number_reciprocal_sum_optimization",
            "right_triangle_legs_area_optimization",
            "absolute_extrema_interval",
            "sum_max_product_optimization",
            "rectangle_area_optimization",
            "upward_parabola_closest_point_optimization",
            "revenue_cost_profit_optimization",
            "open_box_min_surface_area_optimization",
            "sphere_inscribed_cone_optimization",
            "line_closest_point_optimization",
            "average_cost_minimization",
            "lifeguard_travel_time_optimization",
            "illumination_height_optimization",
            "rain_gutter_cross_section_optimization",
            "line_intercepts_sum_optimization",
            "moving_objects_closest_approach_optimization",
            "disk_cone_volume_optimization",
            "beam_strength_cylindrical_log_optimization",
            "cubic_extrema_parameters_optimization",
            "sum_power_product_optimization",
            "right_triangle_inscribed_rectangle_optimization",
            "line_triangle_min_area_optimization",
            "rental_unit_revenue_optimization",
            "transport_trip_cost_optimization",
            "closed_box_cost_optimization",
            "cubic_two_parameter_extremum_optimization",
            "can_material_cost_ratio_optimization",
            "curve_tangent_triangle_min_area_optimization",
            "semicircle_inscribed_trapezoid_optimization",
            "sqrt_curve_closest_point_optimization",
            "conical_tent_min_lateral_area_optimization",
            "curve_secant_max_vertical_distance_optimization",
            "group_ticket_revenue_optimization",
            "sphere_cube_volume_sum_min_ratio_optimization",
            "inscribed_isosceles_triangle_circle_optimization",
            "cylindrical_silo_hemispherical_roof_cost_optimization",
            "rectangle_between_parabolas_max_area_optimization",
            "hyperbola_closest_point_optimization",
            "origin_ray_max_slope_cubic_optimization",
            "corridor_perpendicular_hypotenuse_length_optimization",
            "farmer_harvest_revenue_optimization",
            "cone_circumscribed_sphere_volume_optimization",
            "two_light_sources_illumination_optimization",
            "triangle_included_angle_max_area_optimization",
            "open_box_length_twice_width_min_surface_area_optimization",
            "projectile_range_angle_optimization",
            "horizontal_parabola_inscribed_rectangle_optimization",
            "cubic_tangent_min_slope_optimization",
            "fish_swimming_upstream_energy_optimization",
            "right_triangle_fixed_area_min_leg_sum_optimization",
            "light_ray_reflection_fermat_path_optimization",
            "sphere_inscribed_cylinder_lateral_area_optimization",
            "chemical_tank_hemispherical_ends_cost_optimization",
            "damped_oscillator_interval_extrema_optimization",
            "paper_folding_crease_optimization",
            "cubic_cost_average_cost_optimization",
            "semicircle_inscribed_rectangle_perimeter_optimization",
            "triangle_circumscribed_rectangle_min_area_optimization",
            "ellipse_tangent_min_intercepted_length_optimization",
            "y_shaped_road_network_optimization",
            "curve_line_max_vertical_distance_optimization",
            "cone_fixed_volume_min_lateral_area_optimization",
            "rancher_divided_corral_budget_optimization",
            "parabola_inscribed_triangle_origin_apex_optimization",
            "open_top_cylinder_material_cost_ratio_optimization",
            "curve_closest_point_to_line_optimization",
            "rectangular_sheet_box_volume_optimization",
            "norman_window_fixed_area_min_perimeter_optimization",
            "cone_inscribed_inverted_cone_max_volume_optimization",
            "hyperbola_tangent_min_segment_length_optimization",
            "cable_pipeline_cost_minimization",
            "friction_pull_angle_force_minimization",
            "rectangle_between_two_horizontal_parabolas_optimization",
            "cone_fixed_slant_height_max_volume_optimization",
            "curves_maximum_vertical_distance_optimization",
            "painting_viewing_angle_maximization",
            "sphere_inscribed_closed_cylinder_total_surface_area_optimization",
            "curve_tangent_intercepts_min_sum_optimization",
            "delivery_drone_headwind_energy_optimization",
            "semicircle_circumscribed_isosceles_triangle_min_area_optimization",
            "trapezoid_three_equal_sides_max_area_optimization",
            "ellipse_circumscribed_rectangle_min_area_optimization",
            "parabola_tangent_intercepts_min_sum_optimization",
            "hemisphere_inscribed_cone_max_volume_optimization",
            "inventory_eoq_batch_size_cost_optimization",
            "implicit_derivative",
            "rectangular_area_partition_fence_cost_optimization",
            "open_box_cost_optimization",
            "ladder_top_sliding_rates",
            "two_moving_vehicles_rates",
            "conical_tank_filling_leaking_rates",
            "cubic_curve_critical_points",
            "lifeguard_snell_angle_condition_optimization",
            # ── NEW: Pages 14-30 templates ──
            "rope_pulley_tower_rates",
            "man_helicopter_distance_rates",
            "balloon_car_distance_rates",
            "balloon_elevation_angle_rates",
            "helicopter_elevation_angle_rates",
            "cylinder_volume_rate_by_length_diameter",
            "cylinder_water_level_rate",
            "equilateral_triangle_side_rate",
            "rectangle_constant_ratio_rates",
            "concentric_circles_area_rate",
            "circular_wave_time",
            "cube_heating_edge_volume_rate",
            "cube_volume_rate_given",
            "rectangle_changing_dimensions_rates",
            "rectangle_constant_area_perimeter_rate",
            "rectangle_diagonal_rate",
            "isosceles_triangle_angle_changing",
            "triangle_two_sides_angle_changing",
            "kite_thread_release_rate",
            "cuboid_proportional_dimensions",
            "point_on_curve_slope_rate",
            "point_moving_x_axis_distance_rate",
            "regular_hexagon_area_rate",
            "shadow_length_rate",
            "shadow_length_rate_variant",
            "two_trains_different_start_times",
            "gas_law_pressure_volume_rate",
            "ohms_law_resistance_rate",
            "spherical_balloon_gas_leak_rate",
            "absolute_extrema_closed_interval",
            "cubic_two_critical_points",
            "cubic_origin_critical_tangent",
            "pun_integral",
            "root_manipulation_integral",
            "inverted_quadratic_integral",
            "trig_substitution_integral",
            "partial_fraction_integral",
            "long_division_integral",
            "rational_root_integral",
            "integration_by_parts",
            "cyclic_ibp_integral",
            "tabular_ibp_integral",
            "trig_power_reduction_integral",
            "wallis_integral",
            "product_to_sum_trig_integral",
            "weierstrass_substitution_integral",
            "radical_species_integral",
            "absolute_value_definite_integral",
            "se_one_integral",
            "quad_root_trick_integral",
            "euler_formula_integral",
            "pfd_linear_power_trick_integral",
            "conjugate_radical_integral",
            "nested_infinite_radical_integral",
            "exp_derivative_sum_integral",
            "demoivre_roots_integral",
            "feynman_technique_integral",
            "series_expansion_definite_integral",
            "dilogarithm_integral",
            "power_rule_derivative",
            "product_rule_derivative",
            "quotient_rule_derivative",
            "chain_rule_derivative",
            "trig_derivative",
            "log_exp_derivative",
            "tangent_slope_derivative",
            "derivative_limit_definition",
            "particle_velocity_derivative",
            "tabular_derivative",
            "symbolic_linear_rational_derivative",
            "higher_order_derivative",
            "inverse_trig_derivative",
            "logarithmic_differentiation",
            "composition_derivative",
            "normal_line",
            "implicit_derivative_at_point",
            "implicit_tangent_line",
            "implicit_horizontal_tangents",
            "implicit_vertical_tangents",
            "volume_rate_formula",
        }
        self.assertEqual(set(TEMPLATES.keys()), expected_ids)

    def test_classify_arithmetic(self):
        self.assertEqual(classify_problem("What is 47 * 89 + 123?"), "arithmetic")
        self.assertEqual(classify_problem("Calculate 15 × 16 - 45"), "arithmetic")
        self.assertEqual(classify_problem("Evaluate 120 ÷ 4 + 85"), "arithmetic")

    def test_classify_algebraic(self):
        self.assertEqual(classify_problem("Simplify (x + 1)² − x²"), "algebraic_simplification")
        self.assertEqual(classify_problem("Expand (x - 1)(x + 1)"), "algebraic_simplification")

    def test_classify_equation(self):
        self.assertEqual(classify_problem("Solve 3x + 7 = 22"), "equation_solving")
        self.assertEqual(classify_problem("Find x such that 3x + 4 = 25"), "equation_solving")

    def test_classify_quadratic(self):
        self.assertEqual(classify_problem("Solve 2x^2 + 9 = 60"), "quadratic_equation")
        self.assertEqual(classify_problem("Solve x² - 5x + 6 = 0"), "quadratic_equation")

    def test_classify_derivative(self):
        self.assertEqual(classify_problem("Find the derivative of x² sin(x)"), "derivative")
        self.assertEqual(classify_problem("Differentiate x³ with respect to x"), "derivative")

    def test_classify_integral(self):
        self.assertEqual(classify_problem("Evaluate the definite integral of x² from 0 to 1"), "definite_integral")
        self.assertEqual(classify_problem("Evaluate ∫₀¹ x² dx"), "definite_integral")

    def test_classify_number_theory(self):
        self.assertEqual(classify_problem("Is 97 prime?"), "number_theory")
        self.assertEqual(classify_problem("Check primality of 101"), "number_theory")

    def test_classify_geometry(self):
        self.assertEqual(classify_problem("Find the distance between the points (1, 2) and (4, 6)"), "geometry_distance")

    def test_classify_related_rates(self):
        ladder_prob = (
            "A 10-foot ladder is leaning against a vertical wall. The bottom of the ladder slides away "
            "from the wall at a constant rate of 2 feet per second. How fast is the top of the ladder sliding "
            "down the wall at the exact moment when the bottom of the ladder is 6 feet away from the wall?"
        )
        self.assertEqual(classify_problem(ladder_prob), "related_rates")

    def test_classify_unsupported(self):
        self.assertIsNone(classify_problem("Prove Fermat's Last Theorem"))
        self.assertIsNone(classify_problem("What is the capital of Egypt?"))

    def test_fill_template(self):
        tmpl = get_template("arithmetic")
        filled = fill_template(tmpl, {"expr": "2 + 2", "answer": "4"})
        self.assertEqual(filled, "example : 2 + 2 = 4 := by norm_num")

    def test_fill_equation_template_with_coeff(self):
        tmpl = get_template("equation_solving")
        filled = fill_template(tmpl, {"coeff": "3", "a": "x", "b": "7", "c": "22", "answer": "5"})
        self.assertIn("3 * x", filled)
        self.assertIn("x = 5", filled)

    def test_fill_equation_template_coeff_default(self):
        # When coeff is omitted, fill_template should default to "3"
        tmpl = get_template("equation_solving")
        filled = fill_template(tmpl, {"a": "x", "b": "7", "c": "22", "answer": "5"})
        self.assertIn("3 * x", filled)

    def test_fill_equation_template_custom_coeff(self):
        tmpl = get_template("equation_solving")
        filled = fill_template(tmpl, {"coeff": "2", "a": "x", "b": "4", "c": "10", "answer": "3"})
        self.assertIn("2 * x", filled)
        self.assertIn("x = 3", filled)

    def test_back_translation(self):
        tmpl = get_template("derivative")
        bt = get_back_translation(tmpl, {"expr": "x^2", "answer": "2*x"})
        self.assertIn("derivative of x^2", bt)
        self.assertIn("answer is 2*x", bt)

    def test_back_translation_equation(self):
        tmpl = get_template("equation_solving")
        bt = get_back_translation(tmpl, {"coeff": "3", "a": "x", "b": "7", "c": "22", "answer": "5"})
        self.assertIn("3", bt)
        self.assertIn("x = 5", bt)

    def test_classify_quadratic_variations(self):
        self.assertEqual(classify_problem("find the zeros X^2 + x - 12 = 0"), "quadratic_equation")
        self.assertEqual(classify_problem("zeros of x^2 - 16"), "quadratic_equation")
        self.assertEqual(classify_problem("Solve 2x^2 + 9 = 60"), "quadratic_equation")
        self.assertEqual(classify_problem("x^2 + 5x + 6 = 0"), "quadratic_equation")

    def test_fill_and_back_translate_quadratic(self):
        tmpl = get_template("quadratic_equation")
        filled = fill_template(tmpl, {"lhs": "x^2 + x - 12", "rhs": "0", "r1": "-4", "r2": "3"})
        self.assertIn("x^2 + x - 12 = 0", filled)
        self.assertIn("x = -4 ∨ x = 3", filled)
        self.assertIn("nlinarith", filled)

        bt = get_back_translation(tmpl, {"lhs": "x^2 + x - 12", "rhs": "0", "r1": "-4", "r2": "3"})
        self.assertIn("x^2 + x - 12 = 0", bt)
        self.assertIn("x = -4 or x = 3", bt)

    def test_indefinite_integral(self):
        self.assertEqual(classify_problem("Evaluate the indefinite integral of x²"), "indefinite_integral")
        self.assertEqual(classify_problem("Find the antiderivative of x^2"), "indefinite_integral")
        self.assertEqual(classify_problem("Integrate x^2"), "indefinite_integral")
        self.assertEqual(classify_problem("Evaluate the definite integral of x²"), "indefinite_integral")
        self.assertEqual(classify_problem("Evaluate the definite integral of x² from 0 to 1"), "definite_integral")

        tmpl = get_template("indefinite_integral")
        filled = fill_template(tmpl, {"expr": "x^2", "antideriv": "x^3/3"})
        self.assertIn("deriv (fun x => x^3/3)", filled)
        self.assertIn("= x^2", filled)

        bt = get_back_translation(tmpl, {"expr": "x^2", "antideriv": "x^3/3"})
        self.assertIn("x^3/3 + C", bt)

    def test_classify_conical_tank_rates(self):
        cone_prob = (
            "A conical water tank is shaped like an inverted cone (point down). The tank has a height of 10 meters "
            "and a top radius of 5 meters. Water is being pumped into the tank at a constant rate of 9 cubic meters per minute. "
            "How fast is the water level rising at the exact moment when the water is 6 meters deep?"
        )
        self.assertEqual(classify_problem(cone_prob), "conical_tank_rates")
        tmpl = get_template("conical_tank_rates")
        filled = fill_template(tmpl, {"H": "10", "R": "5", "dV": "9", "h": "6", "dh": "1 / Real.pi"})
        self.assertIn("10", filled)
        self.assertIn("5", filled)
        self.assertIn("9", filled)
        self.assertIn("6", filled)
        self.assertIn("1 / Real.pi", filled)
        self.assertIn("ring", filled)
        bt = get_back_translation(tmpl, {"H": "10", "R": "5", "dV": "9", "h": "6", "dh": "1 / Real.pi"})
        self.assertIn("height 10 meters", bt)
        self.assertIn("radius 5 meters", bt)
        self.assertIn("depth is 6 meters", bt)

    def test_classify_orthogonal_motion_rates(self):
        cars_prob = (
            "Two cars start moving from the same intersection. Car A travels north at 30 miles per hour, "
            "and Car B travels east at 40 miles per hour. How fast is the straight-line distance between the two "
            "cars increasing exactly 2 hours after they start?"
        )
        self.assertEqual(classify_problem(cars_prob), "orthogonal_motion_rates")
        tmpl = get_template("orthogonal_motion_rates")
        filled = fill_template(tmpl, {"vx": "40", "vy": "30", "t": "2", "x": "80", "y": "60", "z": "100", "vz": "50"})
        self.assertIn("(80 : ℝ)^2 + 60^2 = 100^2", filled)
        self.assertIn("80 * 40 + 60 * 30 = 100 * (50)", filled)
        self.assertIn("norm_num", filled)
        bt = get_back_translation(tmpl, {"vx": "40", "vy": "30", "t": "2", "x": "80", "y": "60", "z": "100", "vz": "50"})
        self.assertIn("30 mph", bt)
        self.assertIn("40 mph", bt)
        self.assertIn("100 miles", bt)
        self.assertIn("50 mph", bt)

    def test_classify_spherical_expansion_rates(self):
        sphere_prob = "A spherical balloon is being inflated at a rate of 100 cubic centimeters per minute. How fast is the radius increasing when the radius is 5 cm?"
        self.assertEqual(classify_problem(sphere_prob), "spherical_expansion_rates")
        tmpl = get_template("spherical_expansion_rates")
        filled = fill_template(tmpl, {"dV": "100", "r": "5", "dr": "1 / Real.pi"})
        self.assertIn("100", filled)
        self.assertIn("4 * Real.pi * 5^2", filled)
        self.assertIn("ring", filled)

    def test_classify_circular_expansion_rates(self):
        circle_prob = "A stone dropped into a pond creates a circular ripple whose radius increases at 2 ft/s. How fast is the area increasing when the radius is 10 ft?"
        self.assertEqual(classify_problem(circle_prob), "circular_expansion_rates")
        tmpl = get_template("circular_expansion_rates")
        filled = fill_template(tmpl, {"dA": "40 * Real.pi", "r": "10", "dr": "2"})
        self.assertIn("2 * Real.pi * 10 * (2)", filled)
        self.assertIn("ring", filled)

    def test_classify_streetlamp_shadow_rates(self):
        lamp_prob = (
            "A streetlamp is mounted at the top of a 15-foot-tall pole. A boy who is 5 feet tall walks straight away "
            "from the pole at a constant speed of 6 feet per second. How fast is the length of his shadow changing when "
            "he is 40 feet away from the pole?"
        )
        self.assertEqual(classify_problem(lamp_prob), "streetlamp_shadow_rates")
    def test_classify_conical_pile_rates(self):
        pile_prob = (
            "Gravel is being dumped from a conveyor belt at a rate of 30 cubic feet per minute, and its coarseness is "
            "such that it forms a pile in the shape of a cone whose base diameter and height are always equal. "
            "How fast is the height of the pile increasing when the pile is 10 feet high?"
        )
        self.assertEqual(classify_problem(pile_prob), "conical_pile_rates")
        tmpl = get_template("conical_pile_rates")
        filled = fill_template(tmpl, {"dV": "30", "h": "10", "dh": "6 / (5 * Real.pi)"})
        self.assertIn("(Real.pi / 4) * 10^2 * (6 / (5 * Real.pi))", filled)

    def test_classify_trough_rates(self):
        trough_prob = (
            "A trough is 10 feet long and its ends have the shape of an isosceles triangle that is 3 feet across at the "
            "top and has a height of 1 foot. If the trough is being filled with water at the rate of 12 cubic feet per minute, "
            "how fast is the water level rising when the water is 6 inches deep?"
        )
        self.assertEqual(classify_problem(trough_prob), "trough_rates")
        tmpl = get_template("trough_rates")
        filled = fill_template(tmpl, {"L": "10", "W": "3", "H": "1", "dV": "12", "h": "1/2", "dh": "4/5"})
        self.assertIn("(10 * 3 / 1) * 1/2 * (4/5)", filled)

    def test_classify_kite_string_rates(self):
        kite_prob = (
            "A kite 100 feet above the ground moves horizontally at a speed of 8 feet per second. "
            "How fast is the string being let out when 200 feet of string has been let out?"
        )
        self.assertEqual(classify_problem(kite_prob), "kite_string_rates")
        tmpl = get_template("kite_string_rates")
        filled = fill_template(tmpl, {"y": "100", "z": "200", "x": "100 * Real.sqrt 3", "dx": "8", "dz": "4 * Real.sqrt 3"})
        self.assertIn("(100 * Real.sqrt 3 : ℝ)^2 + 100^2 = 200^2", filled)

    def test_classify_cylindrical_tank_leaking(self):
        leak_prob = (
            "A cylindrical water tank with a fixed radius of 4 meters is leaking water from a hole at the bottom. "
            "The water is leaking out at a constant rate of 2 cubic meters per minute. How fast is the water level inside the tank dropping?"
        )
        self.assertEqual(classify_problem(leak_prob), "cylindrical_tank_rates")
        tmpl = get_template("cylindrical_tank_rates")
        filled = fill_template(tmpl, {"dV": "-2", "R": "4", "dh": "-1 / (8 * Real.pi)"})
        self.assertIn("(-2 : ℝ) = Real.pi * 4^2 * (-1 / (8 * Real.pi))", filled)

    def test_classify_rocket_elevation_rates(self):
        rocket_prob = (
            "A rocket blasts off vertically from a launchpad. A camera is placed on the ground 3,000 feet away from the "
            "launchpad to track the lift-off. At the exact moment the rocket is 4,000 feet in the air, it is traveling "
            "upward at a speed of 800 feet per second. How fast must the camera's angle of elevation change to keep the rocket in frame?"
        )
        self.assertEqual(classify_problem(rocket_prob), "rocket_elevation_rates")
        tmpl = get_template("rocket_elevation_rates")
        filled = fill_template(tmpl, {"x": "3000", "y": "4000", "dy": "800", "dtheta": "12/125"})
        self.assertIn("(3000^2 + 4000^2 : ℝ) * (12/125) = 3000 * 800", filled)

    def test_classify_tracking_distance_rates(self):
        radar_prob = (
            "A rocket is launched vertically and is tracked from a radar station on the ground 3 miles away from the launch pad. "
            "When the rocket is 4 miles high, its upward velocity is 3600 mph. How fast is the distance from the radar station to the rocket changing at that moment?"
        )
        self.assertEqual(classify_problem(radar_prob), "tracking_distance_rates")
        tmpl = get_template("tracking_distance_rates")
        filled = fill_template(tmpl, {"x": "3", "y": "4", "z": "5", "dy": "3600", "dz": "2880"})
        self.assertIn("(3 : ℝ)^2 + 4^2 = 5^2", filled)
        self.assertIn("4 * 3600 = 5 * (2880)", filled)

    def test_classify_ladder_angle_rates(self):
        ladder_angle_prob = (
            "A 10-foot ladder slides down a vertical wall. If the top of the ladder is sliding down at a rate of 1.5 ft/s, "
            "at what rate (in radians per second) is the angle theta between the bottom of the ladder and the ground changing "
            "when the top of the ladder is 6 feet above the ground?"
        )
        self.assertEqual(classify_problem(ladder_angle_prob), "ladder_angle_rates")
        tmpl = get_template("ladder_angle_rates")
        filled = fill_template(tmpl, {"L": "10", "y": "6", "x": "8", "dy": "-3/2", "dtheta": "-3/16"})
        self.assertIn("(8 : ℝ)^2 + 6^2 = 10^2", filled)
        self.assertIn("8 * (-3/16) = (-3/2)", filled)

    def test_classify_conical_tank_pump_leak_rates(self):
        tank_prob = (
            "Water is leaking out of an inverted conical tank (vertex down) at a rate of 2 cm^3/min at the same time "
            "that water is being pumped in at a constant rate. The tank has height 6 cm and the diameter at the top is 4 cm. "
            "If the water level is rising at a rate of 0.5 cm/min when the water height is 4 cm, find the rate at which water is being pumped into the tank."
        )
        self.assertEqual(classify_problem(tank_prob), "conical_tank_pump_leak_rates")
        tmpl = get_template("conical_tank_pump_leak_rates")
        filled = fill_template(tmpl, {"H": "6", "D": "4", "R": "2", "L": "2", "h": "4", "dh": "1/2", "P": "2 + 8 * Real.pi / 9"})
        self.assertIn("(2 + 8 * Real.pi / 9 : ℝ) = 2 + (Real.pi * 2^2 / 6^2) * 4^2 * (1/2)", filled)

    def test_classify_streetlamp_with_hyphen(self):
        lamp_prob = (
            "A street light is mounted 15 feet above the ground. A 6-foot-tall person walks away from the light straight "
            "down the street at a speed of 4 ft/s. At what rate is the length of the person's shadow changing when they are 10 feet from the base of the light?"
        )
        self.assertEqual(classify_problem(lamp_prob), "streetlamp_shadow_rates")

    def test_classify_conical_pile_ratio3(self):
        pile_prob = (
            "Sand is being dumped from a conveyor belt at a rate of 10 ft^3 /min onto a conical pile such that the base diameter is always "
            "equal to three times the height. At what rate is the height of the pile increasing when the pile is 5 feet high?"
        )
        self.assertEqual(classify_problem(pile_prob), "conical_pile_rates")
        tmpl = get_template("conical_pile_rates")
        filled = fill_template(tmpl, {"dV": "10", "k": "3", "h": "5", "dh": "8 / (45 * Real.pi)"})
        self.assertIn("(3^2 * Real.pi / 4) * 5^2 * (8 / (45 * Real.pi))", filled)

    def test_classify_streetlamp_tip(self):
        p = "A street light is mounted 15 feet above the ground. A 6-foot-tall person walks away from the light straight down the street at a speed of 4 ft/s. At what rate is the tip of the person's shadow moving when they are 10 feet from the base of the light?"
        self.assertEqual(classify_problem(p), "streetlamp_shadow_tip_rates")
        tmpl = get_template("streetlamp_shadow_tip_rates")
        filled = fill_template(tmpl, {"H": "15", "h": "6", "dx": "4", "x": "10", "s": "20/3", "v_tip": "20/3"})
        self.assertIn("(15 - 6 : ℝ) * (20/3 - 4) = 6 * 4", filled)

    def test_classify_pulley_boat(self):
        p = "A boat is pulled toward a dock by a rope attached to the bow through a pulley on the dock 12 feet above the bow. If the rope is hauled in at a rate of 4 ft/s, how fast is the boat approaching the dock when the length of the rope from bow to pulley is 20 feet?"
        self.assertEqual(classify_problem(p), "pulley_boat_rates")
        tmpl = get_template("pulley_boat_rates")
        filled = fill_template(tmpl, {"y": "12", "z": "20", "x": "16", "dz": "-4", "dz_abs": "4", "dx": "-5", "speed": "5"})
        self.assertIn("(16 : ℝ)^2 + 12^2 = 20^2", filled)
        self.assertIn("16 * (-5) = 20 * (-4)", filled)

    def test_classify_cube_expansion(self):
        p = "The edge length of a cube is increasing at a constant rate of 2 cm/min. At what rate is the volume of the cube increasing when the edge length is 5 cm?"
        self.assertEqual(classify_problem(p), "cube_expansion_rates")
        tmpl = get_template("cube_expansion_rates")
        filled = fill_template(tmpl, {"s": "5", "ds": "2", "dV": "150"})
        self.assertIn("(150 : ℝ) = 3 * 5^2 * (2)", filled)

    def test_classify_spherical_surface(self):
        p = "A spherical snowball melts so that its surface area decreases at a rate of 4 cm^2/min. Find the rate at which the radius is changing when the radius is 3 cm."
        self.assertEqual(classify_problem(p), "spherical_surface_rates")
        tmpl = get_template("spherical_surface_rates")
        filled = fill_template(tmpl, {"dA": "-4", "dA_mag": "4", "r": "3", "dr": "-1 / (6 * Real.pi)"})
    def test_classify_tangent_line(self):
        p = "Find the equation of the tangent line to f(x) = x^2 - 3x at x = 2"
        self.assertEqual(classify_problem(p), "tangent_line")

    def test_classify_critical_points(self):
        p = "Find the critical points of f(x) = x^3 - 3*x^2"
        self.assertEqual(classify_problem(p), "critical_points")

    def test_classify_extrema_points(self):
        p = "Find the local maximum and minimum of f(x) = x^3 - 3*x"
        self.assertEqual(classify_problem(p), "extrema_points")

    def test_classify_inflection_points(self):
        p = "Find the inflection points of f(x) = x^3 - 3*x^2"
        self.assertEqual(classify_problem(p), "inflection_points")

    def test_classify_kings_rule(self):
        p = "Evaluate the integral of sin(x)/(sin(x) + cos(x)) from 0 to pi/2 using King's rule"
        self.assertEqual(classify_problem(p), "kings_rule_integral")

    def test_classify_rectangle_perimeter(self):
        p = "A rectangular garden must be designed to have an exact area of 64 m^2. What length and width will minimize the total perimeter of the fence required to surround all four sides of the garden, and what is that minimum perimeter?"
        self.assertEqual(classify_problem(p), "rectangle_perimeter_optimization")
        tmpl = get_template("rectangle_perimeter_optimization")
        filled = fill_template(tmpl, {"A": "64", "x": "8", "y": "8", "min_perim": "32"})
        self.assertIn("(8 : ℝ) * 8 = 64", filled)
        self.assertIn("2 * (8 : ℝ) + 2 * 8 = 32", filled)

    def test_classify_parabola_closest_point(self):
        p = "Find the coordinates of the point (x, y) in the first quadrant on the parabola y = 4 - x^2 that is closest to the point (0, 1), and find the minimum distance between them."
        self.assertEqual(classify_problem(p), "parabola_closest_point_optimization")
        tmpl = get_template("parabola_closest_point_optimization")
        filled = fill_template(tmpl, {"b": "4", "c": "1", "x": "sqrt(10)/2", "y": "3/2", "x_sq": "5/2", "dist_sq": "11/4", "min_dist": "sqrt(11)/2"})
        self.assertIn("(3/2 : ℝ) = 4 - 5/2", filled)
        self.assertIn("(5/2 : ℝ) + (3/2 - 1)^2 = 11/4", filled)

    def test_classify_divided_pen(self):
        p = "A rancher has $300\\text{ m}$ of fencing to enclose a large rectangular field and then divide it into two smaller equal rectangular pens by placing a fence parallel to one of the outer sides. What outer dimensions of the large field will maximize the total enclosed area, and what is that maximum area?"
        self.assertEqual(classify_problem(p), "divided_pen_optimization")
        tmpl = get_template("divided_pen_optimization")
        filled = fill_template(tmpl, {"L": "300", "x": "50", "y": "75", "L_half": "150", "max_area": "3750"})
        self.assertIn("3 * (50 : ℝ) + 2 * 75 = 300", filled)
        self.assertIn("(50 : ℝ) * 75 = 3750", filled)

    def test_classify_poster_margin(self):
        p = "A rectangular poster must contain $50\\text{ cm}^2$ of printed text, surrounded by top and bottom margins of $4\\text{ cm}$ each and left and right margins of $2\\text{ cm}$ each. What overall dimensions of the entire poster will minimize the total amount of paper used, and what is that minimum total area?"
        self.assertEqual(classify_problem(p), "poster_margin_optimization")
        tmpl = get_template("poster_margin_optimization")
        filled = fill_template(tmpl, {"A_text": "50", "m_tb": "4", "m_lr": "2", "w_text": "5", "h_text": "10", "W": "9", "H": "18", "min_area": "162"})
        self.assertIn("(5 : ℝ) * 10 = 50", filled)
        self.assertIn("(9 : ℝ) * 18 = 162", filled)

    def test_classify_open_top_cylinder(self):
        p = "An open-top cylindrical container (which has a circular bottom base and curved sides, but no top lid) must hold a fixed volume of $64\\pi\\text{ cm}^3$. Find the radius $r$ and height $h$ of the cylinder that will minimize the total surface area of the material used to make it, and find that minimum surface area."
        self.assertEqual(classify_problem(p), "open_top_cylinder_optimization")
        tmpl = get_template("open_top_cylinder_optimization")
        filled = fill_template(tmpl, {"V_pi": "64", "r": "4", "h": "4", "min_S_pi": "48", "min_S_disp": "48π"})
        self.assertIn("(4 : ℝ)^2 * 4 = 64", filled)
        self.assertIn("2 * (4 : ℝ)^3 - 2 * 64 = 0", filled)

    def test_classify_product_power(self):
        p = "The sum of a positive number $x$ and twice a second positive number $y$ is equal to $24$ (so $x + 2y = 24$). Find the values of $x$ and $y$ that maximize the product $P = xy^2$, and calculate that maximum product."
        self.assertEqual(classify_problem(p), "product_power_optimization")
        tmpl = get_template("product_power_optimization")
        filled = fill_template(tmpl, {"S": "24", "x": "8", "y": "8", "max_P": "512"})
        self.assertIn("(8 : ℝ) + 2 * 8 = 24", filled)
        self.assertIn("(8 : ℝ) * 8^2 = 512", filled)

    def test_classify_parabola_inscribed_rectangle(self):
        p = "A rectangle is inscribed in the region bounded above by the parabola $y = 12 - x^2$ and below by the $x$-axis, such that its base lies flat on the $x$-axis and its two upper corners touch the parabola. Find the width and height of the rectangle that has the greatest possible area, and find that maximum area."
        self.assertEqual(classify_problem(p), "parabola_inscribed_rectangle_optimization")
        tmpl = get_template("parabola_inscribed_rectangle_optimization")
        filled = fill_template(tmpl, {"H_val": "12", "x": "2", "W": "4", "H": "8", "max_area": "32"})
        self.assertIn("(8 : ℝ) = 12 - 2^2", filled)
    def test_classify_garden_cost(self):
        p = r"A rectangular garden with an area of $200\text{ m}^2$ is to be enclosed by a fence. The fencing for the front side facing the street costs $\$12\text{ per meter}$, while the fencing for the other three sides costs $\$4\text{ per meter}$. Find the dimensions of the garden that will minimize the total cost of the fencing, and state that minimum cost."
        self.assertEqual(classify_problem(p), "garden_cost_optimization")
        tmpl = get_template("garden_cost_optimization")
        filled = fill_template(tmpl, {"A": "200", "c_front": "12", "c_other": "4", "x": "10", "y": "20", "min_cost": "320"})
        self.assertIn("(10 : ℝ) * 20 = 200", filled)
        self.assertIn("(12 + 4) * (10 : ℝ) + 2 * 4 * 20 = 320", filled)

    def test_classify_open_box_square_base(self):
        p = "An open-top box with a square base is to be constructed from $108\\text{ cm}^2$ of material. Find the dimensions of the box that will maximize its volume, and find that maximum volume."
        self.assertEqual(classify_problem(p), "open_box_square_base_optimization")
        tmpl = get_template("open_box_square_base_optimization")
        filled = fill_template(tmpl, {"S": "108", "x": "6", "h": "3", "max_vol": "108", "S_quarter": "27"})
        self.assertIn("(6 : ℝ)^2 + 4 * 6 * 3 = 108", filled)
        self.assertIn("(6 : ℝ)^2 * 3 = 108", filled)

    def test_classify_semicircle_inscribed_rectangle(self):
        p = "A rectangle is inscribed in a semicircle of radius $R = 6\\text{ cm}$ such that one side lies along the diameter and the other two vertices lie on the semicircle. Find the dimensions of the rectangle that maximize its area, and find that maximum area."
        self.assertEqual(classify_problem(p), "semicircle_inscribed_rectangle_optimization")
        tmpl = get_template("semicircle_inscribed_rectangle_optimization")
        filled = fill_template(tmpl, {"R": "6", "x_sq": "18", "H_sq": "18", "W_disp": "6*sqrt(2)", "H_disp": "3*sqrt(2)", "max_area": "36"})
        self.assertIn("(18 : ℝ) + 18 = 6^2", filled)
        self.assertIn("(36 : ℝ)^2 = 4 * 18 * 18", filled)

    def test_classify_sum_weighted_squares(self):
        p = "Find two positive numbers whose sum is 16 such that the sum of the square of the first number and three times the square of the second number is minimized, and find that minimum sum."
        self.assertEqual(classify_problem(p), "sum_weighted_squares_optimization")
        tmpl = get_template("sum_weighted_squares_optimization")
        filled = fill_template(tmpl, {"sum_val": "16", "k": "3", "x": "12", "y": "4", "min_S": "192"})
        self.assertIn("(12 : ℝ) + 4 = 16", filled)
        self.assertIn("(12 : ℝ)^2 + 3 * 4^2 = 192", filled)

    def test_classify_closed_cylinder(self):
        p = "A closed cylindrical can is to have a volume of $16\\pi\\text{ cm}^3$. Find the radius and height of the can that will minimize the total surface area, and find that minimum surface area."
        self.assertEqual(classify_problem(p), "closed_cylinder_optimization")
        tmpl = get_template("closed_cylinder_optimization")
        filled = fill_template(tmpl, {"V_pi": "16", "r": "2", "h": "4", "min_S_pi": "24", "min_S_disp": "24π"})
        self.assertIn("(2 : ℝ)^2 * 4 = 16", filled)
        self.assertIn("4 * (2 : ℝ)^3 - 2 * 16 = 0", filled)

    def test_classify_norman_window(self):
        p = "A Norman window has the shape of a rectangle surmounted by a semicircle (so the diameter of the semicircle equals the width of the rectangle). If the total outer perimeter of the window is fixed at 12 m, find the radius r of the semicircular top and the height h of the rectangular portion that will allow the maximum amount of light to pass through (maximize the total area), and state that maximum area."
        self.assertEqual(classify_problem(p), "norman_window_optimization")
        tmpl = get_template("norman_window_optimization")
        filled = fill_template(tmpl, {"P": "12", "r_disp": "12/(4 + pi)", "h_disp": "12/(4 + pi)", "A_disp": "72/(4 + pi)", "r": "12 / (4 + Real.pi)", "h": "12 / (4 + Real.pi)", "A": "72 / (4 + Real.pi)"})
        self.assertIn("(2 + Real.pi) * (12 / (4 + Real.pi)) + 2 * (12 / (4 + Real.pi)) = 12", filled)

    def test_classify_wire_cut(self):
        p = "A piece of wire 10 m long is cut into two pieces (or left uncut as one piece). One piece is bent into the shape of a square and the other is bent into the shape of a circle. How much of the wire should be used for the square in order to (a) minimize the combined total area of the two figures, and (b) maximize the combined total area of the two figures?"
        self.assertEqual(classify_problem(p), "wire_cut_square_circle_optimization")
        tmpl = get_template("wire_cut_square_circle_optimization")
        filled = fill_template(tmpl, {"L": "10", "x_min_disp": "40/(4 + pi) m", "x_max_disp": "0 m", "x_min": "40 / (4 + Real.pi)", "x_max": "0"})
        self.assertIn("(4 + Real.pi) * (40 / (4 + Real.pi)) = 4 * 10", filled)

    def test_classify_sphere_inscribed_cylinder(self):
        p = "A right circular cylinder is inscribed inside a solid sphere of fixed radius R = 3*sqrt(3) cm so that the top and bottom circular edges of the cylinder touch the inner surface of the sphere. Find the radius r and height h of the cylinder that has the largest possible volume, and calculate that maximum volume."
        self.assertEqual(classify_problem(p), "sphere_inscribed_cylinder_optimization")
        tmpl = get_template("sphere_inscribed_cylinder_optimization")
        filled = fill_template(tmpl, {"R_disp": "3*sqrt(3)", "R_sq": "27", "r_disp": "3*sqrt(2)", "h": "6", "r_sq": "18", "V_pi": "108", "V_disp": "108π"})
        self.assertIn("(18 : ℝ) + (6)^2 / 4 = 27", filled)

    def test_classify_cone_inscribed_cylinder(self):
        p = "A right circular cylinder is inscribed inside a right circular cone of altitude H = 12 cm and base radius R = 6 cm such that the bottom base of the cylinder rests flat on the base of the cone and the top circular rim touches the slanted inner walls of the cone. Find the radius r and height h of the cylinder that maximize its volume, and find that maximum volume."
        self.assertEqual(classify_problem(p), "cone_inscribed_cylinder_optimization")
        tmpl = get_template("cone_inscribed_cylinder_optimization")
        filled = fill_template(tmpl, {"H": "12", "R": "6", "r": "4", "h": "4", "V_pi": "64", "V_disp": "64π"})
        self.assertIn("(4 : ℝ) = 12 * (1 - 4 / 6)", filled)

    def test_classify_ladder_over_fence(self):
        p = "A vertical fence 8 ft tall stands parallel to a tall vertical building and is located 1 ft away from the wall of the building. What is the length of the shortest straight ladder that can reach from the flat ground outside the fence, pass over the top of the fence, and rest against the wall of the building?"
        self.assertEqual(classify_problem(p), "ladder_over_fence_optimization")
        tmpl = get_template("ladder_over_fence_optimization")
        filled = fill_template(tmpl, {"a": "8", "b": "1", "tan_theta": "2", "u": "4", "v": "1", "min_L_disp": "5*sqrt(5)", "L_sq": "125"})
        self.assertIn("(2 : ℝ)^3 * 1 = 8", filled)

    def test_classify_number_square_diff(self):
        p = "Find the positive real number $x$ that maximizes the value of the expression $x - x^2$ (the difference between the number and its square), and state that maximum value."
        self.assertEqual(classify_problem(p), "number_square_diff_optimization")
        tmpl = get_template("number_square_diff_optimization")
        filled = fill_template(tmpl, {"k": "1", "x_disp": "1/2", "max_disp": "1/4", "x": "1/2", "max_val": "1/4"})
        self.assertIn("(1/2 : ℝ) = 1 / 2", filled)
        self.assertIn("1 * (1/2 : ℝ) - (1/2)^2 = 1/4", filled)

    def test_classify_number_reciprocal_sum(self):
        p = r"Find the positive real number $x$ such that the sum of the number and nine times its reciprocal ($S = x + \frac{9}{x}$) is as small as possible, and state that minimum sum."
        self.assertEqual(classify_problem(p), "number_reciprocal_sum_optimization")
        tmpl = get_template("number_reciprocal_sum_optimization")
        filled = fill_template(tmpl, {"k": "9", "x_disp": "3", "min_sum_disp": "6", "x": "3", "min_sum": "6"})
        self.assertIn("(3 : ℝ)^2 = 9", filled)
        self.assertIn("(3 : ℝ) + 9 / 3 = 6", filled)

    def test_classify_right_triangle_legs_area(self):
        p = r"In a right-angled triangle, the sum of the lengths of the two perpendicular legs (base and height) is equal to $16\text{ cm}$. Find the lengths of the two legs that will maximize the area of the right triangle, and calculate that maximum area."
        self.assertEqual(classify_problem(p), "right_triangle_legs_area_optimization")
        tmpl = get_template("right_triangle_legs_area_optimization")
        filled = fill_template(tmpl, {"L": "16", "L_half": "8", "a": "8", "b": "8", "max_area": "32"})
        self.assertIn("(8 : ℝ) + 8 = 16", filled)
        self.assertIn("(1/2) * (8 : ℝ) * 8 = 32", filled)

    def test_classify_absolute_extrema_interval(self):
        p = "Find the absolute maximum and absolute minimum values of $f(x) = x^3 - 12x$ on the closed interval $[0, 3]$."
        self.assertEqual(classify_problem(p), "absolute_extrema_interval")
        tmpl = get_template("absolute_extrema_interval")
        filled = fill_template(tmpl, {
            "f": "x^3 - 12*x", "a": "0", "b": "3", "x_max": "0", "max_val": "0",
            "x_min": "2", "min_val": "-16", "f_xmax": "(0 : ℝ)^3 - 12 * 0",
            "f_xmin": "(2 : ℝ)^3 - 12 * 2", "fa": "(0 : ℝ)^3 - 12 * 0", "fa_val": "0",
            "fb": "(3 : ℝ)^3 - 12 * 3", "fb_val": "-9"
        })
        self.assertIn("(0 : ℝ)^3 - 12 * 0 = 0", filled)
        self.assertIn("(2 : ℝ)^3 - 12 * 2 = -16", filled)

    def test_classify_sum_max_product(self):
        p = "Find two positive numbers whose sum is $20$ and whose product is as large as possible."
        self.assertEqual(classify_problem(p), "sum_max_product_optimization")
        tmpl = get_template("sum_max_product_optimization")
        filled = fill_template(tmpl, {"S": "20", "x": "10", "y": "10", "max_product": "100"})
        self.assertIn("(10 : ℝ) + 10 = 20", filled)
        self.assertIn("(10 : ℝ) * 10 = 100", filled)

    def test_classify_rectangle_area_optimization(self):
        p = "A rectangular garden is to be constructed with a total perimeter of $60\\text{ meters}$. What dimensions ($L$ and $W$) will maximize the total enclosed area, and what is that maximum area?"
        self.assertEqual(classify_problem(p), "rectangle_area_optimization")
        tmpl = get_template("rectangle_area_optimization")
        filled = fill_template(tmpl, {"P": "60", "L": "15", "W": "15", "max_area": "225", "P_half": "30"})
        self.assertIn("2 * (15 : ℝ) + 2 * 15 = 60", filled)
        self.assertIn("(15 : ℝ) * 15 = 225", filled)

    def test_classify_quadratic_minimum(self):
        p = "Find the minimum value of the quadratic function $f(x) = 3x^2 - 12x + 7$"
        self.assertEqual(classify_problem(p), "extrema_points")

    def test_classify_exponential_extrema(self):
        p = r"Find the maximum value of the function $f(x) = x e^{-x}$ for $x \ge 0$."
        self.assertEqual(classify_problem(p), "extrema_points")

    def test_classify_rational_extrema(self):
        p = r"Find the local minimum value of the rational function $f(x) = \frac{x^2 + 4}{x}$ for $x > 0$"
        self.assertEqual(classify_problem(p), "extrema_points")

    def test_classify_profit_optimization(self):
        p = "A company's total revenue is $R(x) = 120x - 0.5x^2$ and total cost is $C(x) = 3000 + 20x$, where $x$ is units produced. What production level $x$ maximizes profit, and what is that maximum profit?"
        self.assertEqual(classify_problem(p), "revenue_cost_profit_optimization")
        tmpl = get_template("revenue_cost_profit_optimization")
        filled = fill_template(tmpl, {"R_expr": "120x-0.5x^2", "C_expr": "3000+20x", "p": "120", "q": "1/2", "F": "3000", "c": "20", "x": "100", "max_profit": "2000"})
        self.assertIn("(100 : ℝ)", filled)
        self.assertIn("= 2000", filled)

    def test_classify_upward_parabola(self):
        p = r"Find the point on the parabola $y = x^2$ that is closest to the point $(0, \frac{3}{2})$."
        self.assertEqual(classify_problem(p), "upward_parabola_closest_point_optimization")
        tmpl = get_template("upward_parabola_closest_point_optimization")
        filled = fill_template(tmpl, {"c": "3/2", "x": "1", "y": "1", "x_sq": "1", "dist_sq": "5/4", "min_dist": "sqrt(5)/2"})
        self.assertIn("(1 : ℝ) = (1 : ℝ)^2", filled)
        self.assertIn("= 5/4", filled)

    def test_classify_trig_interval_extrema(self):
        p = r"Find the absolute maximum and minimum values of $f(x) = \sin x + \cos x$ on the interval $[0, 2\pi]$."
        self.assertEqual(classify_problem(p), "absolute_extrema_interval")

    def test_classify_open_box_min_surface_area(self):
        p = r"An open-top rectangular box with a square base must have a fixed volume of $32\text{ cm}^3$. Find the base side length $x$ that minimizes the total surface area."
        self.assertEqual(classify_problem(p), "open_box_min_surface_area_optimization")
        tmpl = get_template("open_box_min_surface_area_optimization")
        filled = fill_template(tmpl, {"V": "32", "unit": "cm", "x": "4", "h": "2", "min_S": "48"})
        self.assertIn("(4 : ℝ)^2 * 2 = 32", filled)
        self.assertIn("= 48", filled)

    def test_classify_sphere_inscribed_cone(self):
        p = r"A right circular cone is inscribed in a sphere of fixed radius $R = 9\text{ cm}$. What is the maximum possible volume of this cone?"
        self.assertEqual(classify_problem(p), "sphere_inscribed_cone_optimization")
        tmpl = get_template("sphere_inscribed_cone_optimization")
        filled = fill_template(tmpl, {"R": "9", "unit": "cm", "h": "12", "r_sq": "72", "r_disp": "6*sqrt(2)", "V_pi": "288", "V_disp": "288π"})
        self.assertIn("(72 : ℝ) = 2 * 9 * 12 - (12)^2", filled)
        self.assertIn("3 * (288 : ℝ) = 72 * 12", filled)

    def test_classify_line_closest_point(self):
        p = r"Find the point on the line $y = 2x + 1$ that is closest to the point $(4, 1)$."
        self.assertEqual(classify_problem(p), "line_closest_point_optimization")
        tmpl = get_template("line_closest_point_optimization")
        filled = fill_template(tmpl, {"m": "2", "b": "1", "x0": "4", "y0": "1", "x": "4/5", "y": "13/5", "x_disp": "4/5", "y_disp": "13/5", "dist_sq": "64/5", "dist_disp": "8*sqrt(5)/5"})
        self.assertIn("(13/5 : ℝ) = 2 * 4/5 + 1", filled)
        self.assertIn("(4/5 - 4)^2 + (13/5 - 1)^2 = 64/5", filled)

    def test_classify_average_cost(self):
        p = r"A manufacturing company has a total cost function $C(x) = x^2 + 36$, where $x$ is the number of units produced. Find the production level $x$ that minimizes the average cost per unit, $AC(x) = \frac{C(x)}{x}$."
        self.assertEqual(classify_problem(p), "average_cost_minimization")
        tmpl = get_template("average_cost_minimization")
        filled = fill_template(tmpl, {"C_expr": "x^2 + 36", "F": "36", "a": "1", "x": "6", "AC_min": "12", "AC_disp": "$12", "C_val": "72"})
        self.assertIn("(72 : ℝ) = 1 * (6)^2 + 36", filled)
        self.assertIn("(12 : ℝ) * 6 = 72", filled)

    def test_classify_moving_objects_closest_approach(self):
        p = r"At noon (t = 0), Ship A is 10 km due west of Ship B. Ship A sails east at 4 km/h, while Ship B sails north at 3 km/h. At what time t are the two ships closest to each other, and what is that minimum distance?"
        self.assertEqual(classify_problem(p), "moving_objects_closest_approach_optimization")
        tmpl = get_template("moving_objects_closest_approach_optimization")
        filled = fill_template(tmpl, {
            "d0": "10", "v1": "4", "v2": "3", "t_min": "8/5", "d_min": "6",
            "t_min_disp": "1.6", "d_min_disp": "6",
            "unit_dist": "km", "unit_speed": "km/h", "unit_time": "hours"
        })
        self.assertIn("2 * (4^2 + 3^2 : ℝ) * (8/5) - 2 * 10 * 4 = 0", filled)
        self.assertIn("(10 - 4 * (8/5) : ℝ)^2 + (3 * (8/5))^2 = (6)^2", filled)

    def test_classify_disk_cone_volume(self):
        p = r"A paper cup in the shape of a right circular cone is made by cutting a sector from a flat circular disk of radius R = 6 cm and joining the cut edges. What height h of the cone maximizes its volume?"
        self.assertEqual(classify_problem(p), "disk_cone_volume_optimization")
        tmpl = get_template("disk_cone_volume_optimization")
        filled = fill_template(tmpl, {
            "R": "6", "h": "2*Real.sqrt 3", "h_disp": "2*sqrt(3)", "h_sq": "12",
            "r_disp": "2*sqrt(6)", "V_max_disp": "16*pi*sqrt(3)", "unit": "cm"
        })
    def test_classify_beam_strength_cylindrical_log(self):
        p = "The strength S of a rectangular wooden beam is proportional to its width w times the square of its depth d (S = kwd^2). Find the dimensions of the strongest beam that can be cut from a cylindrical log of diameter 12 cm."
        self.assertEqual(classify_problem(p), "beam_strength_cylindrical_log_optimization")
        tmpl = get_template("beam_strength_cylindrical_log_optimization")
        filled = fill_template(tmpl, {
            "D": "12", "w_disp": "4*sqrt(3)", "d_disp": "4*sqrt(6)",
            "w_sq": "48", "d_sq": "96", "unit": "cm",
        })
        self.assertIn("3 * (48 : ℝ) = 12^2", filled)
        self.assertIn("(96 : ℝ) = 12^2 - 48", filled)

    def test_classify_cubic_extrema_parameters(self):
        p = "The cubic function f(x) = x^3 + ax^2 + bx + 5 has a local minimum value of 1 at x = 2. Find the constants a and b, and then find the local maximum value of the function."
        self.assertEqual(classify_problem(p), "cubic_extrema_parameters_optimization")
        tmpl = get_template("cubic_extrema_parameters_optimization")
        filled = fill_template(tmpl, {
            "c0": "5", "a": "-3", "b": "0", "x_min": "2", "y_min": "1",
            "x_max": "0", "y_max": "5",
        })
        self.assertIn("(2 : ℝ)^3 + (-3) * (2)^2 + (0) * (2) + 5 = 1", filled)
        self.assertIn("3 * (2 : ℝ)^2 + 2 * (-3) * (2) + (0) = 0", filled)

    def test_classify_sum_power_product(self):
        p = "Find two positive numbers x and y whose sum is 36 such that the product P = x^2 * y is maximized."
        self.assertEqual(classify_problem(p), "sum_power_product_optimization")
        tmpl = get_template("sum_power_product_optimization")
        filled = fill_template(tmpl, {"S": "36", "x": "24", "y": "12", "P_max": "6912"})
        self.assertIn("(24 : ℝ) + 12 = 36", filled)
        self.assertIn("27 * (6912 : ℝ) = 4 * (36)^3", filled)

    def test_classify_right_triangle_inscribed_rectangle(self):
        p = "A right triangle has legs of length 6 cm and 8 cm along the positive x- and y-axes. Find the dimensions of the largest rectangle that can be inscribed in the triangle if two of its sides lie along the legs."
        self.assertEqual(classify_problem(p), "right_triangle_inscribed_rectangle_optimization")
        tmpl = get_template("right_triangle_inscribed_rectangle_optimization")
        filled = fill_template(tmpl, {"a": "6", "b": "8", "w": "3", "h": "4", "w_disp": "3", "h_disp": "4", "A_max": "12", "unit": "cm"})
        self.assertIn("(3 : ℝ) = 6 / 2", filled)
        self.assertIn("(3 : ℝ) * 4 = 12", filled)

    def test_classify_line_triangle_min_area(self):
        p = "line with negative slope passes through the point (2, 3) and forms a right triangle with the positive x- and y-axes. What is the minimum possible area of this triangle?"
        self.assertEqual(classify_problem(p), "line_triangle_min_area_optimization")
        tmpl = get_template("line_triangle_min_area_optimization")
        filled = fill_template(tmpl, {"x0": "2", "y0": "3", "a": "4", "b": "6", "A_min": "12"})
        self.assertIn("(4 : ℝ) = 2 * 2", filled)
        self.assertIn("(1/2 : ℝ) * 4 * 6 = 12", filled)

    def test_classify_rental_unit_revenue(self):
        p = "A hotel has 100 rooms. When the nightly rate is $80, all 100 rooms are occupied. For every $2 increase in the nightly rate, 1 room becomes vacant. What nightly rate maximizes total revenue, and what is that maximum revenue?"
        self.assertEqual(classify_problem(p), "rental_unit_revenue_optimization")
        tmpl = get_template("rental_unit_revenue_optimization")
        filled = fill_template(tmpl, {
            "base_units": "100", "base_rate": "80", "rate_step": "2", "unit_step": "1",
            "n_steps": "30", "optimal_rate": "140", "occupied_units": "70", "R_max": "9800"
        })
        self.assertIn("(140 : ℝ) = 80 + 2 * 30", filled)
        self.assertIn("(140 : ℝ) * 70 = 9800", filled)

    def test_classify_transport_trip_cost(self):
        p = "The fuel cost per hour for running a cargo train at speed v km/h is v^2/25 dollars/hour. In addition, fixed crew and operational costs are $100 per hour. What steady speed v minimizes the total cost of a 500 km trip?"
        self.assertEqual(classify_problem(p), "transport_trip_cost_optimization")
        tmpl = get_template("transport_trip_cost_optimization")
        filled = fill_template(tmpl, {
            "distance": "500", "k_denom": "25", "fixed_cost": "100",
            "v_min": "50", "C_min": "2000", "unit_dist": "km", "unit_speed": "km/h"
        })
        self.assertIn("(50 : ℝ)^2 = 25 * 100", filled)
        self.assertIn("= 2000", filled)

    def test_classify_closed_box_cost(self):
        p = "A closed rectangular box with a square base is to be built with a volume of 48 m^3. The material for the top and bottom costs $3/m^2, while the material for the four vertical sides costs $2/m^2. Find the dimensions that minimize the total cost of the box."
        self.assertEqual(classify_problem(p), "closed_box_cost_optimization")
        tmpl = get_template("closed_box_cost_optimization")
        filled = fill_template(tmpl, {
            "V": "48", "c_tb": "3", "c_side": "2", "x_cubed": "32", "x_cubed_val": "32",
            "h_cubed": "108", "h_cubed_val": "108", "x_disp": "2*4^(1/3)", "h_disp": "3*4^(1/3)",
            "C_min_disp": "144*2^(1/3)", "unit": "m"
        })
        self.assertIn("(32 : ℝ) = 32", filled)
        self.assertIn("4 * (3 : ℝ) * 32 - 4 * (2) * 48 = 0", filled)

    def test_classify_cubic_two_parameter_extremum(self):
        p = "Find the constants a and b in the function f(x) = ax^3 + bx^2 such that the graph has a local maximum at the point (-1, 2)."
        self.assertEqual(classify_problem(p), "cubic_two_parameter_extremum_optimization")
        tmpl = get_template("cubic_two_parameter_extremum_optimization")
        filled = fill_template(tmpl, {
            "x0": "-1", "y0": "2", "a": "4", "b": "6", "extremum_type": "local maximum"
        })
        self.assertIn("(4 : ℝ) * (-1)^3 + (6) * (-1)^2 = 2", filled)
        self.assertIn("3 * (4 : ℝ) * (-1)^2 + 2 * (6) * (-1) = 0", filled)

    def test_classify_can_material_cost_ratio(self):
        p = "A metal can is to hold a volume of 250*pi cm^3. The circular top and bottom are stamped out of sheets that are twice as thick as the sheet used for the curved side (so the ends cost twice as much per cm^2 as the side). What radius r and height h minimize the material cost?"
        self.assertEqual(classify_problem(p), "can_material_cost_ratio_optimization")
        tmpl = get_template("can_material_cost_ratio_optimization")
        filled = fill_template(tmpl, {
            "V_pi": "250*pi", "k": "2", "r_cubed": "125/2", "h_cubed": "500", "h_cubed_val": "500",
            "V_num": "250", "r_disp": "5*4^(1/3)/2", "h_disp": "10*4^(1/3)", "unit": "cm"
        })
        self.assertIn("4 * (2 : ℝ) * 125/2 = 2 * 250", filled)
        self.assertIn("(500 : ℝ) = 500", filled)

    def test_classify_curve_tangent_triangle_min_area(self):
        p = "A tangent line is drawn to the curve y = 9 - x^2 at a point (x_0, y_0) in the first quadrant (x_0 > 0). Find the value of x_0 that minimizes the area of the right triangle formed by this tangent line and the positive x- and y-axes."
        self.assertEqual(classify_problem(p), "curve_tangent_triangle_min_area_optimization")
        tmpl = get_template("curve_tangent_triangle_min_area_optimization")
        filled = fill_template(tmpl, {
            "c": "9", "x0_sq": "3", "x0_disp": "3^(1/2)", "y0": "6", "b": "12", "A_min_disp": "12*3^(1/2)"
        })
        self.assertIn("3 * (3 : ℝ) - 9 = 0", filled)
        self.assertIn("(12 : ℝ) = 9 + 3", filled)

    def test_classify_semicircle_inscribed_trapezoid(self):
        p = "A trapezoid is inscribed in a semicircle of radius R = 4 cm such that its lower base is the diameter of the semicircle (8 cm) and its upper base is parallel to the diameter. What height h of the trapezoid maximizes its area?"
        self.assertEqual(classify_problem(p), "semicircle_inscribed_trapezoid_optimization")
        tmpl = get_template("semicircle_inscribed_trapezoid_optimization")
        filled = fill_template(tmpl, {
            "R": "4", "diam": "8", "h_sq": "12", "h_sq_val": "12", "h_disp": "2*3^(1/2)",
            "A_max_disp": "12*3^(1/2)", "unit": "cm"
        })
        self.assertIn("4 * (12 : ℝ) = 3 * (4)^2", filled)
        self.assertIn("4 * (12 : ℝ)^2 - 3 * (4)^2 * 12 = 0", filled)

    def test_classify_sqrt_curve_closest_point(self):
        p = "Find the point on the curve $y = \\sqrt{2x}$ that is closest to the point $(5, 0)$."
        self.assertEqual(classify_problem(p), "sqrt_curve_closest_point_optimization")
        tmpl = get_template("sqrt_curve_closest_point_optimization")
        filled = fill_template(tmpl, {
            "k": "2", "k_half": "1", "x1": "5", "y1": "0", "x_val": "4", "y_sq": "8", "d_sq": "9",
            "x_disp": "4", "y_disp": "2*sqrt(2)", "d_disp": "3"
        })
        self.assertIn("(4 : ℝ) - 5 = -1", filled)
        self.assertIn("2 * (4 : ℝ) - 2 * 5 + 2 = 0", filled)

    def test_classify_conical_tent_min_lateral_area(self):
        p = "A conical tent must hold a fixed volume of $V = 18\\pi\\sqrt{2}\\text{ m}^3$. What base radius $r$ and height $h$ minimize the lateral canvas area $S = \\pi r \\sqrt{r^2 + h^2}$?"
        self.assertEqual(classify_problem(p), "conical_tent_min_lateral_area_optimization")
        tmpl = get_template("conical_tent_min_lateral_area_optimization")
        filled = fill_template(tmpl, {
            "V_coeff": "18", "r_cubed": "54", "two_third_r_cubed": "36", "four_r_sixth": "11664",
            "V_str": "18*pi*sqrt(2) m^3", "r_disp": "3*2^(1/3)", "h_disp": "3*2^(5/6)", "unit": "m"
        })
        self.assertIn("(1/3 : ℝ) * 54 * 2 = 36", filled)
        self.assertIn("(54 : ℝ) = 3 * 18", filled)

    def test_classify_curve_secant_max_vertical_distance(self):
        p = "On the interval $[1, 4]$, find the $x$-coordinate where the curve $f(x) = \\sqrt{x}$ has the greatest vertical distance above the secant line connecting $(1, 1)$ and $(4, 2)$."
        self.assertEqual(classify_problem(p), "curve_secant_max_vertical_distance_optimization")
        tmpl = get_template("curve_secant_max_vertical_distance_optimization")
        filled = fill_template(tmpl, {
            "x1": "1", "x2": "4", "y1": "1", "y2": "2", "m_str": "1/3", "sqrt_x": "3/2",
            "x_opt": "9/4", "x_opt_disp": "9/4", "d_disp": "1/12"
        })
        self.assertIn("(2 - 1 : ℝ) / (4 - 1) = 1/3", filled)
        self.assertIn("(9/4 : ℝ) = (3/2)^2", filled)

    def test_classify_group_ticket_revenue(self):
        p = "A tour company charges $60 per person for a group of 30 passengers. For every additional passenger above 30, the ticket price for everyone in the group is reduced by $1.50. What group size maximizes the tour company's total revenue?"
        self.assertEqual(classify_problem(p), "group_ticket_revenue_optimization")
        tmpl = get_template("group_ticket_revenue_optimization")
        filled = fill_template(tmpl, {
            "N0": "30", "P0": "60", "d": "1.50", "d_frac": "3/2", "x_opt": "5",
            "N_opt": "35", "P_opt": "52.50", "P_opt_frac": "105/2", "R_max": "1837.50"
        })
        self.assertIn("(35 : ℝ) = 30 + 5", filled)
        self.assertIn("(1837.50 : ℝ) = 35 * 105/2", filled)

    def test_classify_sphere_cube_volume_sum_min_ratio(self):
        p = "The combined surface area of a sphere of radius $r$ and a cube of side $x$ is fixed at $24\\pi\\text{ cm}^2$. Find the ratio of the cube's side $x$ to the sphere's radius $r$ when the sum of their volumes is minimized."
        self.assertEqual(classify_problem(p), "sphere_cube_volume_sum_min_ratio_optimization")
        tmpl = get_template("sphere_cube_volume_sum_min_ratio_optimization")
        filled = fill_template(tmpl, {"C_str": "24*pi cm^2", "ratio": "2"})
        self.assertIn("(2 : ℝ) * 1 = 2", filled)

    def test_classify_inscribed_isosceles_triangle_circle(self):
        p = "Find the height $h$ and maximum area of an isosceles triangle inscribed in a circle of radius $R = 6\\text{ cm}$."
        self.assertEqual(classify_problem(p), "inscribed_isosceles_triangle_circle_optimization")
        tmpl = get_template("inscribed_isosceles_triangle_circle_optimization")
        filled = fill_template(tmpl, {
            "R": "6", "h": "9", "A_coeff": "27", "b_half_sq": "27",
            "b_half_disp": "3*sqrt(3)", "b_disp": "6*sqrt(3)", "A_max_disp": "27*sqrt(3)", "unit": "cm"
        })
        self.assertIn("2 * (9 : ℝ) = 3 * 6", filled)

    def test_classify_cylindrical_silo_hemispherical_roof(self):
        p = "A cylindrical silo with a flat circular floor and a hemispherical roof must hold a fixed total volume of $V = 72\\pi\\text{ m}^3$. The hemispherical roof costs twice as much per square meter as the cylindrical walls (and the floor is free). What radius $r$ and cylinder height $h$ minimize the construction cost?"
        self.assertEqual(classify_problem(p), "cylindrical_silo_hemispherical_roof_cost_optimization")
        tmpl = get_template("cylindrical_silo_hemispherical_roof_cost_optimization")
        filled = fill_template(tmpl, {
            "V_str": "72*pi m^3", "V_num": "72", "r": "3", "h": "6",
            "r_cubed": "27", "r_cubed_val": "27", "h_val": "6", "cost_ratio": "twice", "unit": "m"
        })
        self.assertIn("8 * (27 : ℝ) = 3 * 72", filled)

    def test_classify_rectangle_between_parabolas(self):
        p = "Find the maximum area of a rectangle (with sides parallel to the coordinate axes) that can be inscribed in the region bounded above by $y = 18 - x^2$ and below by $y = 2x^2$."
        self.assertEqual(classify_problem(p), "rectangle_between_parabolas_max_area_optimization")
        tmpl = get_template("rectangle_between_parabolas_max_area_optimization")
        filled = fill_template(tmpl, {
            "a": "18", "b": "1", "c": "2", "b_plus_c": "3", "x_sq": "2",
            "W_disp": "2*sqrt(2)", "H_disp": "12", "A_max_disp": "24*sqrt(2)", "A_max_sq": "1152"
        })
        self.assertIn("3 * (3 : ℝ) * 2 = 18", filled)

    def test_classify_hyperbola_closest_point(self):
        p = "Find the points in the first quadrant on the hyperbola $x^2 - y^2 = 4$ that are closest to the point $(0, 2)$, and find that minimum distance."
        self.assertEqual(classify_problem(p), "hyperbola_closest_point_optimization")
        tmpl = get_template("hyperbola_closest_point_optimization")
        filled = fill_template(tmpl, {
            "a_sq": "4", "x0": "0", "y0": "2", "x_sq": "5", "x_disp": "sqrt(5)",
            "y_disp": "1", "d_sq": "6", "d_disp": "sqrt(6)"
        })
        self.assertIn("4 * (1 : ℝ) - 2 * 2 = 0", filled)

    def test_classify_origin_ray_max_slope_cubic(self):
        p = "A ray from the origin $(0, 0)$ touches a point $(x, y)$ on the curve $y = -x^3 + 6x^2 - 9x + 10$ for $x > 0$. Wait–let's use $y = 6x^2 - x^3$ for $x > 0$. Find the point $(x, y)$ where the slope of the ray from the origin ($\\frac{y}{x}$) is maximized."
        self.assertEqual(classify_problem(p), "origin_ray_max_slope_cubic_optimization")
        tmpl = get_template("origin_ray_max_slope_cubic_optimization")
        filled = fill_template(tmpl, {
            "a": "6", "b": "1", "x_val": "3", "y_val": "27", "m_max": "9"
        })
        self.assertIn("2 * (1 : ℝ) * 3 = 6", filled)

    def test_classify_corridor_perpendicular_hypotenuse(self):
        p = "A corridor of width $1\\text{ m}$ meets a perpendicular corridor of width $8\\text{ m}$ (or equivalently, a line in the first quadrant passes through the point $(1, 8)$). What is the minimum length $L$ of the hypotenuse segment intercepted between the positive $x$- and $y$-axes?"
        self.assertEqual(classify_problem(p), "corridor_perpendicular_hypotenuse_length_optimization")
        tmpl = get_template("corridor_perpendicular_hypotenuse_length_optimization")
        filled = fill_template(tmpl, {
            "w1": "1", "w2": "8", "a": "5", "b": "10", "L_disp": "5*sqrt(5)", "L_sq": "125", "unit": "m"
        })
        self.assertIn("(1 : ℝ) / 5 + 8 / 10 = 1", filled)

    def test_classify_farmer_harvest_revenue(self):
        p = "A potato farmer can harvest immediately and get $100\\text{ bushels}$, which sell for $\\$6\\text{ per bushel}$. For every week ($t$) the farmer waits, the crop grows by $20\\text{ bushels}$, but the market price drops by $\\$0.50\\text{ per bushel}$ per week. How many weeks should the farmer wait to maximize total revenue?"
        self.assertEqual(classify_problem(p), "farmer_harvest_revenue_optimization")
        tmpl = get_template("farmer_harvest_revenue_optimization")
        filled = fill_template(tmpl, {
            "Q0": "100", "P0": "6", "dQ": "20", "dP": "1/2", "t_opt": "7/2", "t_disp": "3.5", "R_max": "1445/2", "R_disp": "$722.50"
        })
        self.assertIn("(6 : ℝ) * 20 - 100 * 1/2", filled)

    def test_classify_cone_circumscribed_sphere(self):
        p = "A right circular cone is circumscribed around a sphere of radius $R = 3\\text{ cm}$ (meaning the sphere sits inside the cone, tangent to its base and slanted sides). What height $h$ of the cone minimizes the cone's volume?"
        self.assertEqual(classify_problem(p), "cone_circumscribed_sphere_volume_optimization")
        tmpl = get_template("cone_circumscribed_sphere_volume_optimization")
        filled = fill_template(tmpl, {
            "R": "3", "h_opt": "12", "r_sq": "18", "r_disp": "3*sqrt(2)", "V_factor": "72", "unit": "cm"
        })
        self.assertIn("(12 : ℝ) = 4 * 3", filled)

    def test_classify_two_light_sources_illumination(self):
        p = "Two light sources are placed $10\\text{ meters}$ apart. Light source $A$ is $8$ times as bright as light source $B$. Since illumination varies directly with brightness and inversely with the square of the distance ($I = \\frac{k}{d^2}$), how far from light source $A$ on the line segment between them is the total illumination at a minimum?"
        self.assertEqual(classify_problem(p), "two_light_sources_illumination_optimization")
        tmpl = get_template("two_light_sources_illumination_optimization")
        filled = fill_template(tmpl, {
            "D": "10", "S": "8", "x_opt": "20/3", "x_disp": "20/3", "d2_opt": "10/3", "d2_disp": "10/3", "unit": "m"
        })
        self.assertIn("(20/3 : ℝ) + (10/3) = 10", filled)

    def test_classify_triangle_included_angle_max_area(self):
        p = "Two sides of a triangle have fixed lengths $a = 6\\text{ cm}$ and $b = 10\\text{ cm}$, with an included angle $\\theta$ between them. What angle $\\theta$ maximizes the area of the triangle, and what is that maximum area?"
        self.assertEqual(classify_problem(p), "triangle_included_angle_max_area_optimization")
        tmpl = get_template("triangle_included_angle_max_area_optimization")
        filled = fill_template(tmpl, {
            "a": "6", "b": "10", "theta": "pi/2", "theta_deg": "90", "A_max": "30", "unit": "cm"
        })
        self.assertIn("2 * (30 : ℝ) = (6 : ℝ) * (10 : ℝ)", filled)

    def test_classify_open_box_length_twice_width(self):
        p = "An open-top rectangular box must hold a fixed volume of $72\\text{ cm}^3$, and the length of its base must be twice its width ($L = 2W$). Find the dimensions of the box that minimize the total surface area of material used."
        self.assertEqual(classify_problem(p), "open_box_length_twice_width_min_surface_area_optimization")
        tmpl = get_template("open_box_length_twice_width_min_surface_area_optimization")
        filled = fill_template(tmpl, {
            "V": "72", "unit": "cm", "W_cubed": "54", "W_exact": "3*2^(1/3)", "W_val": "3.7798",
            "L_cubed": "432", "L_exact": "6*2^(1/3)", "L_val": "7.5595",
            "H_cubed": "16", "H_exact": "2*2^(1/3)", "H_val": "2.5198",
            "S_exact": "54*4^(1/3)", "S_val": "85.7196"
        })
        self.assertIn("4 * (54 : ℝ) = 3 * 72", filled)

    def test_classify_projectile_range_angle(self):
        p = "The horizontal range of a projectile launched at speed $v_0 = 20\\text{ m/s}$ at an angle $\\theta$ above flat ground (with $g = 10\\text{ m/s}^2$) is $R(\\theta) = \\frac{v_0^2}{g}\\sin\\theta\\cos\\theta = 40\\sin\\theta\\cos\\theta$. Use calculus to find the launch angle $\\theta$ that maximizes the range."
        self.assertEqual(classify_problem(p), "projectile_range_angle_optimization")
        tmpl = get_template("projectile_range_angle_optimization")
        filled = fill_template(tmpl, {
            "v0": "20", "g": "10", "k": "40", "theta": "pi/4", "theta_deg": "45", "R_max": "20", "v_unit": "m/s", "len_unit": "m"
        })
        self.assertIn("2 * (20 : ℝ) = 40", filled)

    def test_classify_horizontal_parabola_inscribed_rectangle(self):
        p = "Find the dimensions and maximum area of a rectangle inscribed in the region bounded by the horizontal parabola $x = 9 - y^2$ and the $y$-axis ($x = 0$)."
        self.assertEqual(classify_problem(p), "horizontal_parabola_inscribed_rectangle_optimization")
        tmpl = get_template("horizontal_parabola_inscribed_rectangle_optimization")
        filled = fill_template(tmpl, {
            "a": "9", "y_sq": "3", "y_exact": "sqrt(3)", "y_val": "1.7321", "W": "6",
            "H_exact": "2*sqrt(3)", "H_val": "3.4641", "A_max_exact": "12*sqrt(3)", "A_max_val": "20.7846", "A_max_sq": "432"
        })
        self.assertIn("3 * (3 : ℝ) = 9", filled)

    def test_classify_cubic_tangent_min_slope(self):
        p = "Find the point $(x, y)$ on the cubic curve $y = x^3 - 6x^2 + 15x - 2$ where the tangent line has the smallest (least) slope, and state what that minimum slope is."
        self.assertEqual(classify_problem(p), "cubic_tangent_min_slope_optimization")
        tmpl = get_template("cubic_tangent_min_slope_optimization")
        filled = fill_template(tmpl, {
            "b": "-6", "c": "15", "d": "-2", "x": "2", "y": "12", "m_min": "3"
        })
        self.assertIn("6 * (2 : ℝ) + 2 * (-6) = 0", filled)

    def test_classify_fish_swimming_upstream_energy(self):
        p = "A fish swims upstream a distance D against a river current of speed u = 4 km/h. The total energy E expended by the fish swimming at speed v > 4 relative to the water is proportional to its water speed cubed times the travel time t: E(v) = k v^3 t. Since ground speed is v - 4, travel time is t = D / (v - 4). What swimming speed v minimizes the total energy used?"
        self.assertEqual(classify_problem(p), "fish_swimming_upstream_energy_optimization")
        tmpl = get_template("fish_swimming_upstream_energy_optimization")
        filled = fill_template(tmpl, {"u": "4", "v": "6", "unit": "km/h"})
        self.assertIn("2 * (6 : ℝ) = 3 * 4", filled)

    def test_classify_right_triangle_fixed_area_min_leg_sum(self):
        p = "Among all right triangles with a fixed area of A = 18 cm^2, find the legs x and y that minimize the sum of the lengths of the two legs (x + y), and state the resulting hypotenuse."
        self.assertEqual(classify_problem(p), "right_triangle_fixed_area_min_leg_sum_optimization")
        tmpl = get_template("right_triangle_fixed_area_min_leg_sum_optimization")
        filled = fill_template(tmpl, {
            "A": "18", "x": "6", "y": "6", "h_sq": "72", "h_disp": "6*sqrt(2)", "h_val": "8.4853", "unit": "cm"
        })
        self.assertIn("(6 : ℝ)^2 = 2 * 18", filled)

    def test_classify_light_ray_reflection_fermat_path(self):
        p = "Point A is at (0, 2) and point B is at (6, 4). A light ray travels from A, reflects off a flat mirror along the x-axis at point P(x, 0), and reaches B. Use calculus to find the coordinate x that minimizes the total path length L(x) = AP + PB."
        self.assertEqual(classify_problem(p), "light_ray_reflection_fermat_path_optimization")
        tmpl = get_template("light_ray_reflection_fermat_path_optimization")
        filled = fill_template(tmpl, {
            "a": "2", "b": "4", "d": "6", "x_opt": "2", "L_sq": "72", "L_disp": "6*sqrt(2)", "L_val": "8.4853"
        })
        self.assertIn("(2 + 4 : ℝ) * 2 = 2 * 6", filled)

    def test_classify_sphere_inscribed_cylinder_lateral_area(self):
        p = "A right circular cylinder is inscribed in a sphere of fixed radius R = 5 cm. Instead of maximizing volume, find the cylinder radius r and height H that maximize the curved (lateral) surface area S = 2pi r H of the cylinder."
        self.assertEqual(classify_problem(p), "sphere_inscribed_cylinder_lateral_area_optimization")
        tmpl = get_template("sphere_inscribed_cylinder_lateral_area_optimization")
        filled = fill_template(tmpl, {
            "R": "5", "unit": "cm", "r_sq": "25/2", "r_disp": "5*sqrt(2)/2", "r_val": "3.5355",
            "H_sq": "50", "H_disp": "5*sqrt(2)", "H_val": "7.0711", "S_pi": "50", "S_disp": "50*pi", "S_val": "157.0796"
        })
        self.assertIn("2 * (25/2 : ℝ) = 5^2", filled)

    def test_classify_chemical_tank_hemispherical_ends_cost(self):
        p = "An industrial chemical tank is shaped like a right circular cylinder of radius $r$ and length $h$ capped at both ends by hemispheres of radius $r$. The tank must hold a fixed total volume of $V = \\frac{1000\\pi}{3}\\text{ m}^3$. The hemispherical ends cost twice as much per square meter to manufacture as the cylindrical side wall. What radius $r$ and cylinder length $h$ minimize the total construction cost?"
        self.assertEqual(classify_problem(p), "chemical_tank_hemispherical_ends_cost_optimization")
        tmpl = get_template("chemical_tank_hemispherical_ends_cost_optimization")
        filled = fill_template(tmpl, {
            "r_cubed": "125/2", "V_factor": "1000", "h_cubed": "4000", "h_cubed_val": "4000",
            "r_exact": "5 / 2^(1/3)", "r_val": "3.9685", "h_exact": "10 * 2^(2/3)", "h_val": "15.8740",
            "unit": "m", "V_disp": "1000*pi/3"
        })
        self.assertIn("16 * (125/2 : ℝ) = 1000", filled)
        from backend.pipeline.lean_runner import _verify_with_sympy
        self.assertTrue(_verify_with_sympy(filled))

    def test_classify_damped_oscillator_interval_extrema(self):
        p = "A damped harmonic oscillator has a displacement function $f(t) = e^{-t}\\sin t$ for $t \\in [0, 2\\pi]$. Find the exact times $t$ where the absolute maximum and absolute minimum displacements occur, and state those values."
        self.assertEqual(classify_problem(p), "damped_oscillator_interval_extrema_optimization")
        tmpl = get_template("damped_oscillator_interval_extrema_optimization")
        filled = fill_template(tmpl, {
            "t_max": "Real.pi / 4", "t_min": "5 * Real.pi / 4", "t_max_disp": "pi/4", "t_min_disp": "5*pi/4",
            "val_max_exact": "Real.sqrt 2 / 2 * Real.exp (-Real.pi / 4)",
            "val_min_exact": "-Real.sqrt 2 / 2 * Real.exp (-5 * Real.pi / 4)",
            "val_max_disp": "sqrt(2)/2 * exp(-pi/4)", "val_min_disp": "-sqrt(2)/2 * exp(-5*pi/4)",
            "val_max_approx": "0.3224", "val_min_approx": "-0.0139", "interval_disp": "[0, 2pi]"
        })
        self.assertIn("4 * (Real.pi / 4 : ℝ) = Real.pi", filled)
        from backend.pipeline.lean_runner import _verify_with_sympy
        self.assertTrue(_verify_with_sympy(filled))

    def test_classify_paper_folding_crease(self):
        p = "The bottom-right corner of a long rectangular strip of paper of width $W = 12\\text{ cm}$ is folded over so that the corner just touches the left edge of the page. Let $x$ be the length of the bottom edge that is folded up. Find the value of $x$ that minimizes the length $L$ of the diagonal crease."
        self.assertEqual(classify_problem(p), "paper_folding_crease_optimization")
        tmpl = get_template("paper_folding_crease_optimization")
        filled = fill_template(tmpl, {
            "W": "12", "x": "9", "x_disp": "9", "L_sq": "243", "L_disp": "9*sqrt(3)", "L_val": "15.5885", "unit": "cm"
        })
        self.assertIn("4 * (9 : ℝ) = 3 * 12", filled)
        from backend.pipeline.lean_runner import _verify_with_sympy
        self.assertTrue(_verify_with_sympy(filled))

    def test_classify_cubic_cost_average_cost(self):
        p = "A factory has a cubic total cost function $C(x) = x^3 - 12x^2 + 60x$ for $x > 0$ units. Find the output level $x$ that minimizes the average cost $AC(x) = \\frac{C(x)}{x}$, and verify that at this exact output level, Marginal Cost $C'(x)$ equals Average Cost $AC(x)$."
        self.assertEqual(classify_problem(p), "cubic_cost_average_cost_optimization")
        tmpl = get_template("cubic_cost_average_cost_optimization")
        filled = fill_template(tmpl, {
            "b": "-12", "c": "60", "C_expr": "x^3 - 12x^2 + 60x", "x": "6",
            "AC_val": "24", "MC_val": "24", "AC_expr": "x^2 - 12x + 60", "MC_expr": "3x^2 - 24x + 60"
        })
        self.assertIn("2 * (6 : ℝ) + (-12) = 0", filled)
        from backend.pipeline.lean_runner import _verify_with_sympy
        self.assertTrue(_verify_with_sympy(filled))

    def test_classify_demoivre_roots_integral(self):
        p = "Evaluate the integral of 1/(x^5 + 1) dx using De Moivre's theorem for partial fractions"
        self.assertEqual(classify_problem(p), "demoivre_roots_integral")

    def test_classify_feynman_technique_integral(self):
        p = "Evaluate the definite integral of (x^2 - 1)/ln(x) from 0 to 1 using Feynman's technique of differentiation under the integral sign"
        self.assertEqual(classify_problem(p), "feynman_technique_integral")

    def test_classify_series_expansion_definite_integral(self):
        p = "Evaluate the definite integral of (1 - cos(x))/x^2 from 0 to 1 using MacLaurin series expansion"
        self.assertEqual(classify_problem(p), "series_expansion_definite_integral")

    def test_classify_dilogarithm_integral(self):
        p = "Evaluate the definite integral of ln(1 - exp(-x)) from 0 to oo using the dilogarithm function"
        self.assertEqual(classify_problem(p), "dilogarithm_integral")

    def test_classify_power_rule_derivative(self):
        p = "Find the derivative of x^6 - 5*x^2 + 1 using the power rule"
        self.assertEqual(classify_problem(p), "power_rule_derivative")

    def test_classify_product_rule_derivative(self):
        p = "Find the derivative of x^2 * sin(x) using the product rule"
        self.assertEqual(classify_problem(p), "product_rule_derivative")

    def test_classify_quotient_rule_derivative(self):
        p = "Find the derivative of sin(x)/x using the quotient rule"
        self.assertEqual(classify_problem(p), "quotient_rule_derivative")

    def test_classify_chain_rule_derivative(self):
        p = "Find the derivative of sin(x^3) using the chain rule"
        self.assertEqual(classify_problem(p), "chain_rule_derivative")

    def test_classify_trig_derivative(self):
        p = "Find the derivative of sec(x) + tan(x) using trigonometric derivative rules"
        self.assertEqual(classify_problem(p), "trig_derivative")

    def test_classify_log_exp_derivative(self):
        p = "Find the derivative of exp(3*x) + ln(x) using logarithmic derivative rules"
        self.assertEqual(classify_problem(p), "log_exp_derivative")

    def test_classify_tangent_slope_derivative(self):
        p = "Find the slope of the tangent line to y = -6*sin(x) + 4*exp(x) at the point x = 0"
        self.assertEqual(classify_problem(p), "tangent_slope_derivative")

    def test_classify_derivative_limit_definition(self):
        p = "Evaluate the limit: lim_{h->0} [sqrt(x+h)*exp(x+h) - sqrt(x)*exp(x)] / h"
        self.assertEqual(classify_problem(p), "derivative_limit_definition")

    def test_classify_particle_velocity_derivative(self):
        p = "Find the velocity function of the particle at time t for s(t) = -(t^3 + 1)*exp(t)"
        self.assertEqual(classify_problem(p), "particle_velocity_derivative")

    def test_classify_tabular_derivative(self):
        p = "Let h(x) = f(x)*g(x). Use the table to find h'(2)"
        self.assertEqual(classify_problem(p), "tabular_derivative")

    def test_classify_symbolic_linear_rational_derivative(self):
        p = "Find dy/dx for y = (Ax + B)/(Cx + D) where A, B, C, D in Real"
        self.assertEqual(classify_problem(p), "symbolic_linear_rational_derivative")

    def test_classify_higher_order_derivative(self):
        p1 = "Find the second derivative of y = x^5 - 3*x^2 + 7"
        self.assertEqual(classify_problem(p1), "higher_order_derivative")
        p2 = "Find f''(x) for f(x) = sin(2x)"
        self.assertEqual(classify_problem(p2), "higher_order_derivative")

    def test_classify_inverse_trig_derivative(self):
        p1 = "Find dy/dx for y = arctan(3*x)"
        self.assertEqual(classify_problem(p1), "inverse_trig_derivative")
        p2 = "Find the derivative of y = arcsin(x^2)"
        self.assertEqual(classify_problem(p2), "inverse_trig_derivative")

    def test_classify_logarithmic_differentiation(self):
        p = "Find dy/dx using logarithmic differentiation for y = x^x"
        self.assertEqual(classify_problem(p), "logarithmic_differentiation")

    def test_classify_composition_derivative(self):
        p = "Given f(x) = x^3 and g(x) = 2x + 1, find (f o g)'(x)"
        self.assertEqual(classify_problem(p), "composition_derivative")

    def test_classify_normal_line(self):
        p = "Find the equation of the normal line to y = x^2 at (1, 1)"
        self.assertEqual(classify_problem(p), "normal_line")

    def test_classify_implicit_derivative(self):
        p1 = "Find dy/dx for x - y + x^2 = 6"
        self.assertEqual(classify_problem(p1), "implicit_derivative")
        p2 = "Find the slope of the tangent line for each function: x^2*y - y^3 + x*y = 4"
        self.assertEqual(classify_problem(p2), "implicit_derivative")

    def test_classify_implicit_derivative_at_point(self):
        p = "Find the dy/dx at the given point (a, b): cos(xy) + x^2 = y at (0, 1)"
        self.assertEqual(classify_problem(p), "implicit_derivative_at_point")

    def test_classify_implicit_tangent_line(self):
        p = "Find the equation of the tangent line for f(x) At the point (a, b): x^2 + y^2 = 16 at (1, sqrt(15))"
        self.assertEqual(classify_problem(p), "implicit_tangent_line")

    def test_classify_implicit_horizontal_tangents(self):
        p = "Find where dy/dx = 0: x^2 + y^2 - 2x - 4y = -1"
        self.assertEqual(classify_problem(p), "implicit_horizontal_tangents")

    def test_classify_implicit_vertical_tangents(self):
        p = "Find where the function has a vertical tangent: -2y^2 + x - 20y - 49 = 0"
        self.assertEqual(classify_problem(p), "implicit_vertical_tangents")

if __name__ == "__main__":
    unittest.main()


