"""
Unit & Integration Tests for VeriMath Generalized Out-of-Domain Autoformalizer & Prover
======================================================================================
Verifies:
1. Triggers ONLY when problem is outside the 244 trained templates (`generalized_mode=True`).
2. Proposes and formally verifies unseen out-of-domain problems (identities, inequalities,
   divisibility, GCD, partial derivatives, determinants, finite sums).
3. Strictly REJECTS false out-of-domain claims (`status == "REJECTED"`).
4. Keeps in-domain problems on the standard template pipeline (`generalized_mode=False`).
5. Rejects non-mathematical prompts as `UNSUPPORTED`.
"""

import unittest
from fastapi.testclient import TestClient

from backend.main import app


class TestGeneralizedOutOfDomainProver(unittest.TestCase):
    def test_in_domain_does_not_use_generalized_mode(self):
        with TestClient(app) as client:
            r = client.post("/solve", json={"problem": "Integrate: x^2 * sqrt(x^3 + 4) dx"})
            self.assertEqual(r.status_code, 200)
            data = r.json()
            self.assertEqual(data["status"], "VERIFIED")
            self.assertFalse(data["generalized_mode"])

    def test_generalized_true_out_of_domain_problems(self):
        cases = [
            ("Prove that (a + b)^3 = a^3 + 3*a^2*b + 3*a*b^2 + b^3", "generalized_identity"),
            ("Prove that 2^10 > 1000", "generalized_inequality"),
            ("Does 7 divide 1001?", "generalized_number_theory"),
            ("Find gcd(84, 126)", "generalized_number_theory"),
            ("Find the partial derivative of x^2*y + y^3 with respect to x", "generalized_partial_derivative"),
            ("Find the determinant of [[3, 4], [2, 5]]", "generalized_linear_algebra"),
            ("Find the sum of the first 10 positive integers", "generalized_series_combinatorics"),
        ]
        with TestClient(app) as client:
            for prob, expected_kind in cases:
                r = client.post("/solve", json={"problem": prob})
                self.assertEqual(r.status_code, 200, f"HTTP failure for: {prob}")
                data = r.json()
                self.assertEqual(data["status"], "VERIFIED", f"Expected VERIFIED for '{prob}', got {data}")
                self.assertTrue(data["generalized_mode"])
                self.assertEqual(data["template_id"], expected_kind)
                self.assertTrue(data["explanation"])
                self.assertTrue(data["mental_model"])
                self.assertTrue(data["pitfall_tip"])

    def test_generalized_strictly_rejects_false_claims(self):
        false_claims = [
            "Prove that (a + b)^2 = a^2 + b^2",
            "Prove that 2^10 < 1000",
            "Prove that 7 divides 100",
        ]
        with TestClient(app) as client:
            for claim in false_claims:
                r = client.post("/solve", json={"problem": claim})
                self.assertEqual(r.status_code, 200)
                data = r.json()
                self.assertEqual(data["status"], "REJECTED", f"False claim '{claim}' was not REJECTED: {data}")
                self.assertTrue(data["generalized_mode"])
                self.assertIsNone(data["verified_answer"])

    def test_non_math_prompt_returns_unsupported(self):
        with TestClient(app) as client:
            r = client.post("/solve", json={"problem": "What is the capital of France?"})
            self.assertEqual(r.status_code, 200)
            data = r.json()
            self.assertEqual(data["status"], "UNSUPPORTED")
            self.assertFalse(data["generalized_mode"])


if __name__ == "__main__":
    unittest.main()
