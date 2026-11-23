"""
Tests verifying Raspberry Pi deployment readiness:
  - Systemd / restricted PATH resolution for Lean 4 & Lake binaries
  - Relative LEAN_PROJECT_PATH resolution from repo root
  - /health hardware/architecture/Lean telemetry fields
  - Valid bash syntax and systemd unit configuration for Raspberry Pi
"""

from __future__ import annotations

import os
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.main import app
from backend.pipeline import lean_runner


REPO_ROOT = Path(__file__).resolve().parents[2]


class TestPiDeploymentConfig(unittest.TestCase):
    def test_resolve_lean_and_lake_with_restricted_systemd_path(self):
        elan_lean = Path.home() / ".elan" / "bin" / "lean"
        if not elan_lean.exists():
            self.skipTest("~/.elan/bin/lean not present in this environment")

        # 1. Strict Pi / systemd mode: resolves ~/.elan/bin even when excluded from PATH
        with patch.dict(
            os.environ,
            {
                "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
                "LEAN_BINARY_PATH": "",
                "LAKE_BINARY_PATH": "",
                "VERIMATH_STRICT_LEAN": "true",
                "LEAN_PROJECT_PATH": "./lean/VeriMath",
            },
            clear=False,
        ):
            lean_bin, lake_bin, proj_path = lean_runner.resolve_lean_and_lake_binaries()
            self.assertTrue(os.path.exists(lean_bin), f"Expected lean at {lean_bin}")
            self.assertTrue(os.path.exists(lake_bin), f"Expected lake at {lake_bin}")
            self.assertTrue(os.path.isdir(proj_path), f"Expected Lean project at {proj_path}")
            self.assertTrue(lean_runner.is_lean_available())

        # 2. Dev mode with PATH excluding ~/.elan/bin and strict mode off: preserves SymPy fallback
        with patch.dict(
            os.environ,
            {
                "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
                "LEAN_BINARY_PATH": "",
                "LAKE_BINARY_PATH": "",
                "VERIMATH_STRICT_LEAN": "false",
                "LEAN_PROJECT_PATH": "./lean/VeriMath",
            },
            clear=False,
        ):
            self.assertFalse(lean_runner.is_lean_available())

    def test_health_reports_pi_runtime_fields(self):
        client = TestClient(app)
        res = client.get("/health")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "ok")
        self.assertIn("lean_installed", data)
        self.assertIn("strict_lean_mode", data)
        self.assertIn("arch", data)
        self.assertIn("connectors", data)

    def test_deployment_scripts_and_systemd_units_valid(self):
        scripts = [
            REPO_ROOT / "deployment" / "install_pi.sh",
            REPO_ROOT / "deployment" / "run_pi.sh",
            REPO_ROOT / "deployment" / "check_pi.sh",
        ]
        for script in scripts:
            self.assertTrue(script.exists(), f"Missing {script}")
            proc = subprocess.run(["bash", "-n", str(script)], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, f"Syntax error in {script}: {proc.stderr}")

        backend_unit = (REPO_ROOT / "deployment" / "systemd" / "verimath-backend.service").read_text()
        self.assertIn(".elan/bin", backend_unit)
        self.assertIn("SupplementaryGroups=video", backend_unit)

        frontend_unit = (REPO_ROOT / "deployment" / "systemd" / "verimath-frontend.service").read_text()
        self.assertIn("serve -s build -l 3000", frontend_unit)


if __name__ == "__main__":
    unittest.main()
