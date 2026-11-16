"""
Integration test for the 5 user-reported problems.
Verifies end-to-end pipeline execution: classification, solving, formalization,
statement judge faithfulness, Lean 4 / SymPy CAS verification, LaTeX output.
"""

import unittest
import asyncio
from backend.main import solve_endpoint, SolveRequest

class TestUserReported5Problems(unittest.TestCase):
    def test_problem_1_streetlamp_tip_of_shadow(self):
        """
        Problem 1: Street light tip of shadow
        Question: A street light is mounted 15 feet above the ground. A 6-foot-tall person walks away from the light straight down the street at a speed of 4 ft/s. At what rate is the tip of the person's shadow moving when they are 10 feet from the base of the light?
        Expected: 20/3 ft/s, VERIFIED, template: streetlamp_shadow_tip_rates
        """
        p = (
            "A street light is mounted 15 feet above the ground. A 6-foot-tall person walks away "
            "from the light straight down the street at a speed of 4 ft/s. "
            "At what rate is the tip of the person's shadow moving when they are 10 feet from the base of the light?"
        )
        req = SolveRequest(problem=p)
        resp = asyncio.run(solve_endpoint(req))
        self.assertEqual(resp.status, "VERIFIED")
        self.assertEqual(resp.template_id, "streetlamp_shadow_tip_rates")
        self.assertIn("20/3", resp.verified_answer)
        self.assertIn("ft/s", resp.verified_answer)
        self.assertIsNotNone(resp.latex_answer)

    def test_problem_2_pulley_boat(self):
        """
        Problem 2: Boat pulled to dock via pulley
        Question: A boat is pulled toward a dock by a rope attached to the bow through a pulley on the dock 12 feet above the bow. If the rope is hauled in at a rate of 4 ft/s, how fast is the boat approaching the dock when the length of the rope from bow to pulley is 20 feet?
        Expected: 5 ft/s, VERIFIED, template: pulley_boat_rates
        """
        p = (
            "A boat is pulled toward a dock by a rope attached to the bow through a pulley on the dock 12 feet above the bow. "
            "If the rope is hauled in at a rate of 4 ft/s, how fast is the boat approaching the dock "
            "when the length of the rope from bow to pulley is 20 feet?"
        )
        req = SolveRequest(problem=p)
        resp = asyncio.run(solve_endpoint(req))
        self.assertEqual(resp.status, "VERIFIED")
        self.assertEqual(resp.template_id, "pulley_boat_rates")
        self.assertIn("5", resp.verified_answer)
        self.assertIn("ft/s", resp.verified_answer)
        self.assertIsNotNone(resp.latex_answer)

    def test_problem_3_cube_expansion(self):
        """
        Problem 3: Cube edge volume expansion
        Question: The edge length of a cube is increasing at a constant rate of 2 cm/min. At what rate is the volume of the cube increasing when the edge length is 5 cm?
        Expected: 150 cm^3/min, VERIFIED, template: cube_expansion_rates
        """
        p = (
            "The edge length of a cube is increasing at a constant rate of 2 cm/min. "
            "At what rate is the volume of the cube increasing when the edge length is 5 cm?"
        )
        req = SolveRequest(problem=p)
        resp = asyncio.run(solve_endpoint(req))
        self.assertEqual(resp.status, "VERIFIED")
        self.assertEqual(resp.template_id, "cube_expansion_rates")
        self.assertIn("150", resp.verified_answer)
        self.assertIn("cm^3/min", resp.verified_answer)
        self.assertIsNotNone(resp.latex_answer)

    def test_problem_4_spherical_snowball_surface_melting(self):
        """
        Problem 4: Spherical snowball surface area decrease (Fixing formula and sign error!)
        Question: A spherical snowball melts so that its surface area decreases at a rate of 4 cm^2/min. Find the rate at which the radius is changing when the radius is 3 cm.
        Expected: -1/(6*pi) cm/min, VERIFIED, template: spherical_surface_rates
        """
        p = (
            "A spherical snowball melts so that its surface area decreases at a rate of 4 cm^2/min. "
            "Find the rate at which the radius is changing when the radius is 3 cm."
        )
        req = SolveRequest(problem=p)
        resp = asyncio.run(solve_endpoint(req))
        self.assertEqual(resp.status, "VERIFIED")
        self.assertEqual(resp.template_id, "spherical_surface_rates")
        self.assertIn("-1/(6*pi)", resp.verified_answer)
        self.assertIn("cm/min", resp.verified_answer)
        self.assertIn("decreasing", resp.verified_answer)
        self.assertIsNotNone(resp.latex_answer)

    def test_problem_5_orthogonal_bicycles_clock_time(self):
        """
        Problem 5: Bicycles orthogonal motion with 2:00 PM and noon
        Question: Two bicycles start from the same intersection at noon. Bicycle A travels north at 12 km/h and Bicycle B travels east at 9 km/h. How fast is the distance between them changing at 2:00 PM?
        Expected: 15 km/h, VERIFIED, template: orthogonal_motion_rates
        """
        p = (
            "Two bicycles start from the same intersection at noon. "
            "Bicycle A travels north at 12 km/h and Bicycle B travels east at 9 km/h. "
            "How fast is the distance between them changing at 2:00 PM?"
        )
        req = SolveRequest(problem=p)
        resp = asyncio.run(solve_endpoint(req))
        self.assertEqual(resp.status, "VERIFIED")
        self.assertEqual(resp.template_id, "orthogonal_motion_rates")
        self.assertIn("15", resp.verified_answer)
        self.assertIn("km/h", resp.verified_answer)
        self.assertIsNotNone(resp.latex_answer)

    def test_euler_substitution_integral(self):
        """
        Euler Substitution 1: Integrate 1 / [ x + sqrt(x^2 + x + 1) ] dx
        """
        p = "Integrate 1 / [ x + sqrt(x^2 + x + 1) ] dx"
        req = SolveRequest(problem=p)
        resp = asyncio.run(solve_endpoint(req))
        self.assertEqual(resp.status, "VERIFIED")
        self.assertEqual(resp.template_id, "indefinite_integral")
        self.assertIsNotNone(resp.verified_answer)
        self.assertIn("ln", resp.verified_answer)
        self.assertIsNotNone(resp.latex_answer)

    def test_involution_integral(self):
        """
        Algebraic Involution: Integrate (x^2 - 1) / [ (x^2 + 1) * sqrt(x^4 + 1) ] dx
        """
        p = "Integrate (x^2 - 1) / [ (x^2 + 1) * sqrt(x^4 + 1) ] dx"
        req = SolveRequest(problem=p)
        resp = asyncio.run(solve_endpoint(req))
        self.assertEqual(resp.status, "VERIFIED")
        self.assertEqual(resp.template_id, "indefinite_integral")
        self.assertIsNotNone(resp.verified_answer)
        self.assertIn("arccos", resp.verified_answer)
        self.assertIsNotNone(resp.latex_answer)

    def test_nested_transcendental_derivative(self):
        """
        Nested transcendental derivative: Find the derivative of arctan(x^(x^2)) * sec(e^(sin(x))) with respect to x
        """
        p = "Find the derivative of arctan(x^(x^2)) * sec(e^(sin(x))) with respect to x"
        req = SolveRequest(problem=p)
        resp = asyncio.run(solve_endpoint(req))
        self.assertEqual(resp.status, "VERIFIED")
        self.assertEqual(resp.template_id, "derivative")
        self.assertIsNotNone(resp.verified_answer)
        self.assertIn("arctan", resp.verified_answer)
        self.assertIsNotNone(resp.latex_answer)

if __name__ == "__main__":
    unittest.main()


