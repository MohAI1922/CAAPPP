"""
VeriMath — Comprehensive Colab Fine-Tuning Dataset Generator
============================================================
Generates 2,500 instruction-tuning pairs spanning all major calculus,
algebra, and related rates problem families.

Covers:
 1. Conical Tanks (Inverted cones, pumping/leaking, complete & incomplete)
 2. Sliding Ladders (Pythagorean rates, complete & incomplete)
 3. Spherical Solids & Balloons (Volume, surface area, radius, pi handling)
 4. Orthogonal Motion (Cars, ships, planes from intersections)
 5. Streetlight & Shadows (Shadow growth vs. tip velocity)
 6. Pulleys & Boats (Winch on dock hauling boat)
 7. Cubes & Expanding Solids (Edge, volume, surface area)
 8. Trapezoidal Troughs & Canals (Cross-sectional water flow)
 9. Triangle Law of Cosines (Two sides and angle, 3rd side rate)
10. Pure Calculus & Algebra (Derivatives, definite integrals, linear/quadratic equations)

Includes BOTH:
 - Complete Problems: standard textbook questions with diverse phrasing.
 - Incomplete Problems (Guardrails): missing crucial variables (depth, time, length)
   training the model to output `is_complete: false` and NEVER hallucinate numbers!
"""

import json
import random
from pathlib import Path

OUTPUT_FILE = Path(__file__).parent.parent / "verimath_finetune_dataset.jsonl"

SYSTEM_PROMPT = (
    "You are VeriMath Precision Autoformalization Extractor. "
    "Your task is to analyze mathematical word problems, classify them into the correct template, "
    "extract all parameter values into a structured JSON object, and verify whether all necessary "
    "information is present to solve the problem. If any required variable is missing, set is_complete to false "
    "and identify the missing field. Output valid JSON only."
)

def build_dataset():
    dataset = []

    # -------------------------------------------------------------
    # 1. Inverted Conical Tanks (300 problems)
    # -------------------------------------------------------------
    cone_heights = [8, 10, 12, 14, 15, 16, 20]
    cone_radii = [2, 3, 4, 5, 6, 8]
    flow_rates = [2, 3, 4, 5, 6, 8, 9, 10, 12]
    depths = [2, 3, 4, 5, 6, 7, 8, 9, 10]

    for _ in range(300):
        H = random.choice(cone_heights)
        R = random.choice([r for r in cone_radii if r < H])
        dV = random.choice(flow_rates)
        is_complete = random.random() > 0.3
        base_prompt = f"A water tank has the shape of an inverted right circular cone with a height of {H} m and a base radius of {R} m. Water is being pumped into the tank at a constant rate of {dV} m^3/min."
        if is_complete:
            h = random.choice([d for d in depths if d < H])
            q = random.choice([
                f" How fast is the water level rising when the water is {h} m deep?",
                f" Find the rate at which the water depth is increasing when the water reaches {h} meters.",
                f" At what speed is the water level rising at the exact instant the depth is {h} meters?"
            ])
            full_prompt = base_prompt + q
            ans = {
                "template": "conical_tank_rates",
                "is_complete": True,
                "parameters": {"H": str(H), "R": str(R), "dV": str(dV), "h": str(h)},
                "target": "dh_dt",
                "missing_parameters": []
            }
        else:
            full_prompt = base_prompt
            ans = {
                "template": "conical_tank_rates",
                "is_complete": False,
                "parameters": {"H": str(H), "R": str(R), "dV": str(dV), "h": None},
                "target": "dh_dt",
                "missing_parameters": ["h"],
                "rejection_reason": "Incomplete problem: Missing water depth (h). The rising rate depends on the instantaneous depth."
            }
        dataset.append({"messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": full_prompt}, {"role": "assistant", "content": json.dumps(ans, indent=2)}]})

    # -------------------------------------------------------------
    # 2. Sliding Ladders (300 problems)
    # -------------------------------------------------------------
    for _ in range(300):
        L = random.choice([10, 13, 15, 17, 20, 25, 26])
        dx = random.choice([1, 2, 3, 4, 5])
        is_complete = random.random() > 0.25
        base_prompt = f"A {L}-foot ladder leans against a vertical wall. The bottom of the ladder slides away from the wall at {dx} ft/s."
        if is_complete:
            x = random.choice(range(3, L - 2))
            full_prompt = base_prompt + f" How fast is the top of the ladder sliding down when the base is {x} feet from the wall?"
            ans = {
                "template": "related_rates",
                "is_complete": True,
                "parameters": {"L": str(L), "dx": str(dx), "x": str(x)},
                "target": "dy_dt",
                "missing_parameters": []
            }
        else:
            full_prompt = base_prompt
            ans = {
                "template": "related_rates",
                "is_complete": False,
                "parameters": {"L": str(L), "dx": str(dx), "x": None},
                "target": "dy_dt",
                "missing_parameters": ["x"],
                "rejection_reason": "Incomplete problem: Missing base distance (x). Specify how far the ladder base is from the wall."
            }
        dataset.append({"messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": full_prompt}, {"role": "assistant", "content": json.dumps(ans, indent=2)}]})

    # -------------------------------------------------------------
    # 3. Spheres & Balloons (250 problems)
    # -------------------------------------------------------------
    for _ in range(250):
        dV = random.choice([20, 50, 100, 200, 400])
        r = random.choice([2, 3, 4, 5, 8, 10])
        has_pi = random.choice([True, False])
        dV_str = f"{dV}*pi" if has_pi else str(dV)
        dV_prompt = f"{dV}π" if has_pi else str(dV)
        is_complete = random.random() > 0.25
        base = f"Air is being pumped into a spherical balloon at a rate of {dV_prompt} cm³/s."
        if is_complete:
            full_prompt = base + f" Determine the rate at which the radius is increasing when the radius is {r} cm."
            ans = {
                "template": "spherical_expansion_rates",
                "is_complete": True,
                "parameters": {"dV": dV_str, "r": str(r)},
                "target": "dr_dt",
                "missing_parameters": []
            }
        else:
            full_prompt = base
            ans = {
                "template": "spherical_expansion_rates",
                "is_complete": False,
                "parameters": {"dV": dV_str, "r": None},
                "target": "dr_dt",
                "missing_parameters": ["r"],
                "rejection_reason": "Incomplete problem: Missing radius (r)."
            }
        dataset.append({"messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": full_prompt}, {"role": "assistant", "content": json.dumps(ans, indent=2)}]})

    # -------------------------------------------------------------
    # 4. Orthogonal Motion (250 problems)
    # -------------------------------------------------------------
    for _ in range(250):
        va = random.choice([15, 20, 25, 30, 40, 50])
        vb = random.choice([16, 20, 24, 30, 45, 60])
        t = random.choice([1, 2, 3, 4])
        is_complete = random.random() > 0.25
        base = f"Car A leaves an intersection traveling North at {va} mph, and Car B leaves at the same time traveling East at {vb} mph."
        if is_complete:
            full_prompt = base + f" How fast is the distance between them increasing {t} hours later?"
            ans = {
                "template": "orthogonal_motion_rates",
                "is_complete": True,
                "parameters": {"va": str(va), "vb": str(vb), "t": str(t)},
                "target": "dz_dt",
                "missing_parameters": []
            }
        else:
            full_prompt = base
            ans = {
                "template": "orthogonal_motion_rates",
                "is_complete": False,
                "parameters": {"va": str(va), "vb": str(vb), "t": None},
                "target": "dz_dt",
                "missing_parameters": ["t"],
                "rejection_reason": "Incomplete problem: Missing elapsed time (t)."
            }
        dataset.append({"messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": full_prompt}, {"role": "assistant", "content": json.dumps(ans, indent=2)}]})

    # -------------------------------------------------------------
    # 5. Streetlamp & Shadow Problems (250 problems)
    # -------------------------------------------------------------
    for _ in range(250):
        hl = random.choice([12, 15, 18, 20])
        hp = random.choice([5, 6])
        v = random.choice([3, 4, 5])
        is_tip = random.choice([True, False])
        target_name = "tip_speed" if is_tip else "shadow_rate"
        template_id = "streetlamp_shadow_tip_rates" if is_tip else "streetlamp_shadow_rates"
        question_text = "How fast is the tip of his shadow moving?" if is_tip else "At what rate is the length of his shadow increasing?"
        prompt = f"A streetlight is mounted at the top of a {hl}-foot pole. A {hp}-ft-tall person walks away from the pole at {v} ft/s. {question_text}"
        ans = {
            "template": template_id,
            "is_complete": True,
            "parameters": {"h_pole": str(hl), "h_person": str(hp), "v_person": str(v)},
            "target": target_name,
            "missing_parameters": []
        }
        dataset.append({"messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}, {"role": "assistant", "content": json.dumps(ans, indent=2)}]})

    # -------------------------------------------------------------
    # 6. Pulleys & Boats (200 problems)
    # -------------------------------------------------------------
    for _ in range(200):
        h_dock = random.choice([6, 8, 10, 12])
        rope_rate = random.choice([2, 3, 4, 5])
        rope_len = random.choice([15, 20, 25])
        is_complete = random.random() > 0.2
        base = f"A boat is pulled toward a dock by a rope attached to the bow and passing through a pulley on the dock {h_dock} ft above the bow. The rope is hauled in at {rope_rate} ft/s."
        if is_complete:
            full_prompt = base + f" How fast is the boat approaching the dock when {rope_len} ft of rope is out?"
            ans = {
                "template": "pulley_boat_rates",
                "is_complete": True,
                "parameters": {"h": str(h_dock), "dz": str(-rope_rate), "z": str(rope_len)},
                "target": "dx_dt",
                "missing_parameters": []
            }
        else:
            full_prompt = base
            ans = {
                "template": "pulley_boat_rates",
                "is_complete": False,
                "parameters": {"h": str(h_dock), "dz": str(-rope_rate), "z": None},
                "target": "dx_dt",
                "missing_parameters": ["z"],
                "rejection_reason": "Incomplete problem: Missing rope length (z)."
            }
        dataset.append({"messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": full_prompt}, {"role": "assistant", "content": json.dumps(ans, indent=2)}]})

    # -------------------------------------------------------------
    # 7. Cubes & Rectangular Solids (200 problems)
    # -------------------------------------------------------------
    for _ in range(200):
        s = random.choice([3, 4, 5, 6, 8, 10])
        ds = random.choice([1, 2, 3])
        prompt = f"The edge length of a cube is expanding at a rate of {ds} cm/s. How fast is the volume of the cube increasing when the edge length is {s} cm?"
        ans = {
            "template": "cube_expansion_rates",
            "is_complete": True,
            "parameters": {"s": str(s), "ds": str(ds)},
            "target": "dV_dt",
            "missing_parameters": []
        }
        dataset.append({"messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}, {"role": "assistant", "content": json.dumps(ans, indent=2)}]})

    # -------------------------------------------------------------
    # 8. Trapezoidal Troughs / Canals (200 problems)
    # -------------------------------------------------------------
    for _ in range(200):
        L = random.choice([10, 12, 15, 20])
        b_bottom = random.choice([2, 3, 4])
        b_top = random.choice([6, 8, 10])
        H = random.choice([3, 4, 5])
        dV = random.choice([4, 6, 8, 10])
        h_water = random.choice([1, 2])
        prompt = f"A water trough is {L} m long with cross-section an isosceles trapezoid of bottom width {b_bottom} m, top width {b_top} m, and height {H} m. Water flows in at {dV} m³/min. How fast is the water level rising when water is {h_water} m deep?"
        ans = {
            "template": "trapezoidal_trough_rates",
            "is_complete": True,
            "parameters": {"L": str(L), "b_bottom": str(b_bottom), "b_top": str(b_top), "H": str(H), "dV": str(dV), "h": str(h_water)},
            "target": "dh_dt",
            "missing_parameters": []
        }
        dataset.append({"messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}, {"role": "assistant", "content": json.dumps(ans, indent=2)}]})

    # -------------------------------------------------------------
    # 9. Triangle Law of Cosines (150 problems)
    # -------------------------------------------------------------
    for _ in range(150):
        a = random.choice([10, 12, 15])
        b = random.choice([8, 10, 14])
        da = random.choice([1, 2])
        prompt = f"Two sides of a triangle are {a} m and {b} m with an included angle of pi/3 radians. If side a increases at {da} m/s while side b and the angle remain constant, how fast is the third side changing?"
        ans = {
            "template": "triangle_angle_third_side_rates",
            "is_complete": True,
            "parameters": {"a": str(a), "b": str(b), "da": str(da), "theta": "pi/3"},
            "target": "dc_dt",
            "missing_parameters": []
        }
        dataset.append({"messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}, {"role": "assistant", "content": json.dumps(ans, indent=2)}]})

    # -------------------------------------------------------------
    # -------------------------------------------------------------
    # 10. Multi-Rule Derivatives (Product, Quotient, Chain, Trig Identities)
    # -------------------------------------------------------------
    deriv_multi_rules = [
        # Product Rule
        ("x^2 * sin(x)", "Find the derivative of f(x) = x^2 * sin(x)"),
        ("exp(x) * cos(x)", "Differentiate f(x) = e^x * cos(x) using the product rule"),
        ("x^3 * ln(x)", "Find dy/dx for y = x^3 * ln(x)"),
        ("tan(x) * sec(x)", "Differentiate f(x) = tan(x) * sec(x)"),
        ("(2*x + 3) * (x^2 - 1)", "Find the derivative of (2x + 3)(x^2 - 1)"),
        # Quotient Rule
        ("sin(x) / (x^2 + 1)", "Find the derivative of f(x) = sin(x) / (x^2 + 1) using the quotient rule"),
        ("(x + 1) / (x - 1)", "Differentiate y = (x + 1) / (x - 1)"),
        ("ln(x) / x", "Find dy/dx for y = ln(x) / x"),
        ("cos(x) / (sin(x) + 1)", "Find the derivative of cos(x) / (sin(x) + 1)"),
        ("exp(x) / (x^2 + 1)", "Differentiate f(x) = e^x / (x^2 + 1)"),
        # Chain Rule & Trig Identities
        ("sin(3*x^2)", "Differentiate f(x) = sin(3x^2) using the chain rule"),
        ("cos(x)^2", "Find the derivative of y = cos^2(x)"),
        ("tan(2*x)", "Find dy/dx for y = tan(2x)"),
        ("sec(x)^2", "Differentiate f(x) = sec^2(x)"),
        ("csc(x)", "Find the derivative of csc(x) with respect to x"),
        ("cot(x)", "Differentiate f(x) = cot(x)"),
        ("sqrt(x^2 + 4)", "Find the derivative of f(x) = sqrt(x^2 + 4)"),
        ("ln(sec(x) + tan(x))", "Differentiate y = ln(sec(x) + tan(x))"),
    ]
    for expr, prompt in deriv_multi_rules:
        for _ in range(15):
            dataset.append({
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": json.dumps({
                        "template": "derivative",
                        "is_complete": True,
                        "parameters": {"expr": expr},
                        "target": "derivative",
                        "missing_parameters": []
                    }, indent=2)}
                ]
            })

    # -------------------------------------------------------------
    # 11. Advanced Integration (King's Rule & U-Substitution)
    # -------------------------------------------------------------
    # King's Rule Definite Integrals
    kings_integrals = [
        ("sin(x)/(sin(x) + cos(x))", "0", "pi/2", "Evaluate the integral of sin(x)/(sin(x) + cos(x)) from 0 to pi/2 using King's rule"),
        ("cos(x)/(sin(x) + cos(x))", "0", "pi/2", "Evaluate the definite integral of cos(x)/(sin(x) + cos(x)) from 0 to pi/2 using King's property"),
        ("1/(1 + tan(x)^3)", "0", "pi/2", "Compute the integral of 1/(1 + tan(x)^3) from 0 to pi/2 by King's rule"),
        ("x * sin(x) / (1 + cos(x)^2)", "0", "pi", "Evaluate the integral of x*sin(x)/(1 + cos(x)^2) from 0 to pi using King's rule"),
        ("sqrt(sin(x))/(sqrt(sin(x)) + sqrt(cos(x)))", "0", "pi/2", "Evaluate the integral of sqrt(sin(x))/(sqrt(sin(x)) + sqrt(cos(x))) from 0 to pi/2 using King's rule"),
        ("1 / ((1 + x^sqrt(3)) * (1 + x^2))", "0", "inf", "Evaluate the definite integral of 1 / ((1 + x^sqrt(3)) * (1 + x^2)) from 0 to inf"),
        ("1 / ((1 + x^e) * (1 + x^2))", "0", "inf", "Evaluate the definite integral of 1 / ((1 + x^e) * (1 + x^2)) from 0 to inf using King's property"),
        ("1 / ((1 + x^2024) * (1 + x^2))", "0", "inf", "Find the integral of 1 / ((1 + x^2024) * (1 + x^2)) from 0 to inf"),
        ("ln(1 + x) / (1 + x^2)", "0", "1", "Evaluate the integral of ln(1 + x) / (1 + x^2) from 0 to 1 using King's rule"),
    ]
    for expr, a, b, prompt in kings_integrals:
        for _ in range(20):
            dataset.append({
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": json.dumps({
                        "template": "kings_rule_integral",
                        "is_complete": True,
                        "parameters": {"expr": expr, "lower": a, "upper": b},
                        "target": "integral_value",
                        "missing_parameters": []
                    }, indent=2)}
                ]
            })

    # U-Substitution Indefinite Integrals
    u_sub_integrals = [
        ("2*x * exp(x^2)", "Evaluate the indefinite integral of 2x * e^(x^2) dx using u-substitution"),
        ("sin(x) * cos(x)", "Find the integral of sin(x) * cos(x) dx"),
        ("2*x * (x^2 + 1)^3", "Evaluate the indefinite integral of 2x(x^2 + 1)^3 dx"),
        ("tan(x) * sec(x)^2", "Find the antiderivative of tan(x) * sec^2(x) dx"),
        ("sin(x) / cos(x)^2", "Integrate sin(x) / cos^2(x) dx"),
        ("2*x / (x^2 + 1)", "Evaluate the integral of 2x / (x^2 + 1) dx"),
        ("x * sqrt(x^2 + 4)", "Find the indefinite integral of x * sqrt(x^2 + 4) dx"),
        ("cos(x) * exp(sin(x))", "Integrate e^(sin(x)) * cos(x) dx"),
        ("3*x^2 * (x^3 + 5)^4", "Evaluate the indefinite integral of 3x^2(x^3 + 5)^4 dx"),
        ("sec(x)^2 / tan(x)", "Find the antiderivative of sec^2(x) / tan(x) dx"),
        ("3*x^2 + 2*x", "Evaluate the indefinite integral of 3x² + 2x"),
        ("4*x^3 - 6*x", "Find the indefinite integral of 4x³ − 6x"),
        ("exp(2*x)", "Evaluate the indefinite integral of e^(2x) dx"),
        ("1/x", "Find the indefinite integral of 1/x dx"),
    ]
    for expr, prompt in u_sub_integrals:
        for _ in range(15):
            dataset.append({
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": json.dumps({
                        "template": "indefinite_integral",
                        "is_complete": True,
                        "parameters": {"expr": expr},
                        "target": "antiderivative",
                        "missing_parameters": []
                    }, indent=2)}
                ]
            })

    # -------------------------------------------------------------
    # 12. Tangent & Normal Lines (Complete & Incomplete Guardrails)
    # -------------------------------------------------------------
    tangent_problems = [
        ("x^2 - 3*x", "2", "Find the equation of the tangent line to f(x) = x^2 - 3x at x = 2", False),
        ("x^3 - 3*x", "1", "Find the normal line to y = x^3 - 3x at x = 1", True),
        ("sin(x)", "0", "What is the equation of the tangent line to f(x) = sin(x) at x = 0?", False),
        ("x^2", "1", "Find the normal line to curve f(x) = x^2 at x = 1", True),
        ("2*x^3 - 4*x + 1", "2", "Find the tangent line to y = 2x^3 - 4x + 1 at x = 2", False),
        ("sqrt(x)", "4", "Find the tangent line to f(x) = sqrt(x) at x = 4", False),
        ("1/x", "1", "Find the normal line to y = 1/x at x = 1", True),
        ("exp(x)", "0", "Find the equation of the tangent line to f(x) = e^x at x = 0", False)
    ]
    for f_expr, x0, prompt, is_norm in tangent_problems:
        for _ in range(15):
            dataset.append({
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": json.dumps({
                        "template": "tangent_line",
                        "is_complete": True,
                        "parameters": {"f": f_expr, "x0": x0, "type": "normal" if is_norm else "tangent"},
                        "target": "line_equation",
                        "missing_parameters": []
                    }, indent=2)}
                ]
            })

    # Incomplete Tangent Line Guardrails (missing x0 point)
    incomp_tangents = [
        ("x^2 - 3*x", "Find the equation of the tangent line to f(x) = x^2 - 3x"),
        ("x^3 - 3*x", "Find the normal line to y = x^3 - 3x"),
        ("sin(x)", "What is the equation of the tangent line to curve f(x) = sin(x)?"),
    ]
    for f_expr, prompt in incomp_tangents:
        for _ in range(10):
            dataset.append({
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": json.dumps({
                        "template": "tangent_line",
                        "is_complete": False,
                        "parameters": {"f": f_expr, "x0": None},
                        "target": "line_equation",
                        "missing_parameters": ["x0"],
                        "rejection_reason": "Incomplete problem: Missing point of tangency (x0). A line cannot be determined without a specific point."
                    }, indent=2)}
                ]
            })

    # -------------------------------------------------------------
    # 13. Critical Points
    # -------------------------------------------------------------
    critical_problems = [
        ("x^3 - 3*x^2", "Find the critical points of f(x) = x^3 - 3*x^2"),
        ("2*x^3 - 3*x^2 - 12*x + 5", "Find all critical points of f(x) = 2x^3 - 3x^2 - 12x + 5"),
        ("x^4 - 4*x^2", "Find the stationary points of y = x^4 - 4x^2"),
        ("x^3 - 3*x", "Find the critical points of f(x) = x^3 - 3x"),
        ("x^4 - 2*x^2 + 3", "Find all critical points of f(x) = x^4 - 2x^2 + 3")
    ]
    for f_expr, prompt in critical_problems:
        for _ in range(15):
            dataset.append({
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": json.dumps({
                        "template": "critical_points",
                        "is_complete": True,
                        "parameters": {"f": f_expr},
                        "target": "critical_points",
                        "missing_parameters": []
                    }, indent=2)}
                ]
            })

    # -------------------------------------------------------------
    # 14. Extrema Points (Local Maximum & Minimum)
    # -------------------------------------------------------------
    extrema_problems = [
        ("x^3 - 3*x", "Find the local maximum and minimum of f(x) = x^3 - 3*x"),
        ("2*x^3 - 9*x^2 + 12*x", "Find the local extrema of f(x) = 2x^3 - 9x^2 + 12x"),
        ("x^4 - 2*x^2 + 3", "Find the local maximum and minimum values of f(x) = x^4 - 2x^2 + 3"),
        ("x^3 - 12*x", "Find the relative maximum and relative minimum of y = x^3 - 12x"),
        ("-x^3 + 3*x^2 + 9*x - 4", "Find the local extrema of f(x) = -x^3 + 3x^2 + 9x - 4")
    ]
    for f_expr, prompt in extrema_problems:
        for _ in range(15):
            dataset.append({
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": json.dumps({
                        "template": "extrema_points",
                        "is_complete": True,
                        "parameters": {"f": f_expr},
                        "target": "extrema_points",
                        "missing_parameters": []
                    }, indent=2)}
                ]
            })

    # -------------------------------------------------------------
    # 15. Inflection Points & Concavity
    # -------------------------------------------------------------
    inflection_problems = [
        ("x^3 - 3*x^2", "Find the inflection points of f(x) = x^3 - 3*x^2"),
        ("x^3 - 6*x^2 + 9*x", "Find the point of inflection of y = x^3 - 6x^2 + 9x"),
        ("3*x^5 - 5*x^4", "Find the inflection points of f(x) = 3x^5 - 5x^4"),
        ("x^4 - 6*x^2", "Find the points of inflection and concavity of f(x) = x^4 - 6x^2"),
        ("x^3 - 12*x", "Find the inflection point of f(x) = x^3 - 12x")
    ]
    for f_expr, prompt in inflection_problems:
        for _ in range(15):
            dataset.append({
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": json.dumps({
                        "template": "inflection_points",
                        "is_complete": True,
                        "parameters": {"f": f_expr},
                        "target": "inflection_points",
                        "missing_parameters": []
                    }, indent=2)}
                ]
            })

    # -------------------------------------------------------------
    # 16. Algebra & Quadratic Equations
    # -------------------------------------------------------------
    eqs = [
        ("3*x + 7 = 22", "Solve 3x + 7 = 22"),
        ("5*x - 15 = 0", "Find the value of x if 5x - 15 = 0"),
        ("x^2 - 5*x + 6 = 0", "Find the roots of x² - 5x + 6 = 0"),
        ("2*x^2 - 8 = 0", "Solve the quadratic equation 2x² - 8 = 0")
    ]
    for eq, prompt in eqs:
        for _ in range(20):
            tmpl = "quadratic_equation" if "^2" in eq or "²" in eq else "equation_solving"
            dataset.append({"messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}, {"role": "assistant", "content": json.dumps({"template": tmpl, "is_complete": True, "parameters": {"equation": eq}, "target": "roots", "missing_parameters": []}, indent=2)}]})

    # Definite Integrals
    integrals = [
        ("x^2", "0", "3", "Evaluate the definite integral of x² from 0 to 3"),
        ("2*x + 1", "1", "4", "Find the area under 2x + 1 from x=1 to x=4"),
        ("sin(x)", "0", "pi", "Compute the integral of sin(x) from 0 to π")
    ]
    for expr, a, b, prompt in integrals:
        for _ in range(20):
            dataset.append({"messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}, {"role": "assistant", "content": json.dumps({"template": "definite_integral", "is_complete": True, "parameters": {"expr": expr, "lower": a, "upper": b}, "target": "integral_value", "missing_parameters": []}, indent=2)}]})

    # Shuffle
    random.shuffle(dataset)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for entry in dataset:
            f.write(json.dumps(entry) + "\n")

    print(f"Generated {len(dataset)} comprehensive instruction pairs in {OUTPUT_FILE}")

if __name__ == "__main__":
    build_dataset()

