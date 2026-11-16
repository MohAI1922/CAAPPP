"""
Test suite covering all 14 diagnostic problems across 3 sections:
- Section 1: 2D & 3D Geometric Solids (Sphere, Ladder Area, Inverted Cone, Cube Space Diagonal, Trapezoidal Trough)
- Section 2: Trigonometry & Angular Rates (Rocket Launch, Searchlight, Clock Hands, Dynamic Triangle, Painting Angle)
- Section 3: Relative Motion, Shadows & 3D Distance (Streetlight Shadow Dual Rates, 3D Skew Car/Helicopter, Boat & Winch, Non-Orthogonal Roads)

Tests run end-to-end through solve_endpoint to verify:
1. Classification to proper template
2. Exact mathematical calculation
3. Formalization without missing number/function errors
4. Statement judge faithfulness acceptance
5. Lean 4 / SymPy CAS mathematical verification
6. Clean LaTeX presentation
"""

import unittest
from backend.main import solve_endpoint, SolveRequest


class Test14DiagnosticProblems(unittest.IsolatedAsyncioTestCase):

    async def test_q1_sphere_volume_surface_rates(self):
        problem = "The volume of a sphere is increasing at a constant rate of $100\\pi\\text{ cm}^3/\\text{s}$. At what rate is its surface area increasing when the radius is $5\\text{ cm}$?"
        res = await solve_endpoint(SolveRequest(problem=problem))
        self.assertEqual(res.status, "VERIFIED", f"Failed with reason: {res.rejection_reason}")
        self.assertIn("40*pi", res.verified_answer)
        self.assertIsNotNone(res.latex_answer)
        self.assertIn("40", res.latex_answer)

    async def test_q2_ladder_area_rates(self):
        problem = "A $13\\text{ m}$ ladder leans against a vertical wall. The bottom of the ladder slides away from the wall at $2\\text{ m/s}$. How fast is the area of the right triangle formed by the ladder, the wall, and the ground changing at the instant the base is $5\\text{ m}$ from the wall?"
        res = await solve_endpoint(SolveRequest(problem=problem))
        self.assertEqual(res.status, "VERIFIED", f"Failed with reason: {res.rejection_reason}")
        self.assertIn("119/12", res.verified_answer)
        self.assertIsNotNone(res.latex_answer)

    async def test_q3_inverted_cone_pump_and_leak(self):
        problem = "An inverted conical tank has a height of $10\\text{ m}$ and a top radius of $4\\text{ m}$. Water leaks from the bottom at $2\\text{ m}^3/\\text{min}$ while simultaneously being pumped in at the top at $5\\text{ m}^3/\\text{min}$. How fast is the water level rising when the water is $5\\text{ m}$ deep?"
        res = await solve_endpoint(SolveRequest(problem=problem))
        self.assertEqual(res.status, "VERIFIED", f"Failed with reason: {res.rejection_reason}")
        self.assertIn("3/(4*pi)", res.verified_answer)
        self.assertIsNotNone(res.latex_answer)

    async def test_q4_cube_space_diagonal(self):
        problem = "The space diagonal (corner-to-opposite-corner) of a cube is increasing at a rate of $3\\sqrt{3}\\text{ cm/s}$. At what rate is the volume of the cube increasing when the edge length is $4\\text{ cm}$?"
        res = await solve_endpoint(SolveRequest(problem=problem))
        self.assertEqual(res.status, "VERIFIED", f"Failed with reason: {res.rejection_reason}")
        self.assertIn("144", res.verified_answer)
        self.assertIsNotNone(res.latex_answer)

    async def test_q5_trapezoidal_trough(self):
        problem = "A water trough is $10\\text{ m}$ long and its vertical cross-section is an isosceles trapezoid with a bottom width of $2\\text{ m}$, a top width of $6\\text{ m}$, and a height of $2\\text{ m}$. If water is pumped in at $4\\text{ m}^3/\\text{min}$, how fast is the water level rising when the water is $1\\text{ m}$ deep?"
        res = await solve_endpoint(SolveRequest(problem=problem))
        self.assertEqual(res.status, "VERIFIED", f"Failed with reason: {res.rejection_reason}")
        self.assertTrue("1/10" in res.verified_answer or "0.1" in res.verified_answer)
        self.assertIsNotNone(res.latex_answer)

    async def test_q6_rocket_elevation(self):
        problem = "A rocket launches vertically upward at $50\\text{ m/s}$. A tracking camera is fixed on the ground $200\\text{ m}$ from the launchpad. How fast is the camera's angle of elevation changing (in $\\text{rad/s}$) when the rocket is $200\\text{ m}$ above the ground?"
        res = await solve_endpoint(SolveRequest(problem=problem))
        self.assertEqual(res.status, "VERIFIED", f"Failed with reason: {res.rejection_reason}")
        self.assertIn("1/8", res.verified_answer)
        self.assertIsNotNone(res.latex_answer)

    async def test_q7_searchlight_rotation(self):
        problem = "A lighthouse sits $3\\text{ km}$ offshore from a straight coastline and its light rotates at $2\\text{ revolutions per minute}$. How fast is the beam of light moving along the shore when it passes a point $4\\text{ km}$ from the spot on shore closest to the lighthouse?"
        res = await solve_endpoint(SolveRequest(problem=problem))
        self.assertEqual(res.status, "VERIFIED", f"Failed with reason: {res.rejection_reason}")
        self.assertIn("100*pi/3", res.verified_answer)
        self.assertIsNotNone(res.latex_answer)

    async def test_q8_clock_hands_distance(self):
        problem = "The minute hand of a clock is $8\\text{ cm}$ long and the hour hand is $5\\text{ cm}$ long. How fast is the distance between the tips of the hands changing at exactly 4:00?"
        res = await solve_endpoint(SolveRequest(problem=problem))
        self.assertEqual(res.status, "VERIFIED", f"Failed with reason: {res.rejection_reason}")
        self.assertIn("110*pi/(3*sqrt(43))", res.verified_answer)
        self.assertIsNotNone(res.latex_answer)

    async def test_q9_triangle_angle_area(self):
        problem = "Two sides of a triangle have fixed lengths of $10\\text{ cm}$ and $15\\text{ cm}$. The angle $\\theta$ between them is increasing at a constant rate of $0.1\\text{ rad/s}$. Find the rate at which the area of the triangle is increasing when $\\theta = \\frac{\\pi}{3}$."
        res = await solve_endpoint(SolveRequest(problem=problem))
        self.assertEqual(res.status, "VERIFIED", f"Failed with reason: {res.rejection_reason}")
        self.assertTrue("15/4" in res.verified_answer or "3.75" in res.verified_answer)
        self.assertIsNotNone(res.latex_answer)

    async def test_q10_painting_viewing_angle(self):
        problem = "A $6\\text{ m}$ tall painting hangs on a wall with its bottom edge $2\\text{ m}$ above an observer's eye level. The observer walks directly toward the wall at $1.5\\text{ m/s}$. How fast is the viewing angle $\\theta$ subtended by the painting changing when the observer is $4\\text{ m}$ from the wall?"
        res = await solve_endpoint(SolveRequest(problem=problem))
        self.assertEqual(res.status, "VERIFIED", f"Failed with reason: {res.rejection_reason}")
        self.assertIn("0", res.verified_answer)
        self.assertIsNotNone(res.latex_answer)

    async def test_q11_streetlight_shadow_dual(self):
        problem = "A $2\\text{ m}$ tall person walks away from a $6\\text{ m}$ tall streetlight at $1.2\\text{ m/s}$. Find (a) the rate at which the length of the shadow is increasing, and (b) the rate at which the tip of the shadow is moving away from the streetlight."
        res = await solve_endpoint(SolveRequest(problem=problem))
        self.assertEqual(res.status, "VERIFIED", f"Failed with reason: {res.rejection_reason}")
        self.assertIn("0.6", res.verified_answer)
        self.assertIn("1.8", res.verified_answer)
        self.assertIsNotNone(res.latex_answer)

    async def test_q12_skew_3d_motion(self):
        problem = "A car travels east along a straight road at $20\\text{ m/s}$. A helicopter flies north at a constant altitude of $120\\text{ m}$ at $15\\text{ m/s}$. At $t = 0$, the helicopter is directly above the road at a point $90\\text{ m}$ east of the car. How fast is the direct 3D distance between them changing at $t = 2\\text{ s}$?"
        res = await solve_endpoint(SolveRequest(problem=problem))
        self.assertEqual(res.status, "VERIFIED", f"Failed with reason: {res.rejection_reason}")
        self.assertIn("55/sqrt(178)", res.verified_answer)
        self.assertIsNotNone(res.latex_answer)

    async def test_q13_boat_winch_pulley(self):
        problem = "A winch sits on a dock $3\\text{ m}$ above the bow of a boat and pulls a rope attached to the bow at $1\\text{ m/s}$. How fast is the boat approaching the dock horizontally when $5\\text{ m}$ of rope is out?"
        res = await solve_endpoint(SolveRequest(problem=problem))
        self.assertEqual(res.status, "VERIFIED", f"Failed with reason: {res.rejection_reason}")
        self.assertTrue("5/4" in res.verified_answer or "1.25" in res.verified_answer)
        self.assertIsNotNone(res.latex_answer)

    async def test_q14_non_orthogonal_roads(self):
        problem = "Two straight roads intersect at a $60^\\circ$ angle. Car A is $4\\text{ km}$ from the intersection and moving toward it at $60\\text{ km/h}$. Car B is $3\\text{ km}$ from the intersection and moving away from it at $80\\text{ km/h}$. How fast is the distance between the two cars changing at that instant?"
        res = await solve_endpoint(SolveRequest(problem=problem))
        self.assertEqual(res.status, "VERIFIED", f"Failed with reason: {res.rejection_reason}")
        self.assertIn("70/sqrt(13)", res.verified_answer)
        self.assertIsNotNone(res.latex_answer)


if __name__ == "__main__":
    unittest.main()
