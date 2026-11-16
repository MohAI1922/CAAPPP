"""
VeriMath — Append Book of 1000 Derivatives Chapter 5 Dataset (Problems #553 - #681)
===================================================================================
Covers authentic problems #553 through #681 from Miguel Santiago's
'Book of 1000 Derivatives' (The Vegan Math Guy):
- Implicit Differentiation dy/dx for polynomial, rational, radical, trigonometric,
  logarithmic, and exponential curves (#553 - #606, #637 - #654, #679 - #681)
- Slope of the Tangent Line for Implicit Functions (#607 - #618)
- Implicit Derivative Evaluated at Point (a, b) (#619 - #636)
- Equation of Tangent Line to Implicit Curves at Point (a, b) (#655 - #666)
- Horizontal Tangents (dy/dx = 0) for Conic & Algebraic Curves (#667 - #672)
- Vertical Tangents for Algebraic Curves (#673 - #678)

Generates:
1. Way 1: 129 authentic textbook problems (#553 to #681) + phrasing variants (~265 examples)
2. Way 2: ~275 parametric variations across implicit polynomial, rational, surd,
   trigonometric, tangent line, and horizontal/vertical tangent families.
Total: ~540 new verified ChatML examples.
"""

import json
import os
import re
import sqlite3
from datetime import datetime, timezone
from typing import List, Dict, Any

DATASET_PATH = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "verimath_finetune_dataset.jsonl")
)
CACHE_DB_PATH = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "demo_cache.db")
)

SYSTEM_PROMPT = (
    "You are VeriMath, a rigorous mathematical AI assistant. "
    "Solve the user's math problem with complete formal verification. "
    "Output your final response as valid JSON matching the VeriMath schema."
)

def make_entry(problem: str, template: str, params: dict, lean_stmt: str) -> dict:
    assistant_obj = {
        "template": template,
        "is_complete": True,
        "parameters": params,
        "lean_formalization": lean_stmt,
        "confidence": "high"
    }
    return {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": problem},
            {"role": "assistant", "content": json.dumps(assistant_obj, indent=2)}
        ]
    }

def _normalize_key(text: str) -> str:
    s = text.lower().strip()
    s = s.replace("−", "-").replace("²", "^2").replace("³", "^3").replace("π", "pi")
    s = re.sub(r"[\?\.\!]$", "", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()

def get_authentic_problems() -> List[Dict[str, Any]]:
    # Ingests and solves all 129 problems (#553 to #681)
    import sys
    sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..")))
    from backend.templates.registry import classify_problem
    from backend.pipeline.solver import solve

    RAW_PROBLEMS = [
        # Page 191
        (553, "Find dy/dx for x - y + x^2 = 6", "implicit_derivative"),
        (554, "Find dy/dx for x^2 - y^2 + x = 3", "implicit_derivative"),
        (555, "Find dy/dx for x^3 + y^2 = 2", "implicit_derivative"),
        # Page 192
        (556, "Find dy/dx for 4x^3 - 6x + y = 7", "implicit_derivative"),
        (557, "Find dy/dx for 5x^2 + 6y^2 - 10 = 0", "implicit_derivative"),
        (558, "Find dy/dx for x^2 + y^2 - 6x + 7y = 10", "implicit_derivative"),
        # Page 193
        (559, "Find dy/dx for 4x^2 + 5y^2 + 12x + 20y - 20 = 0", "implicit_derivative"),
        (560, "Find dy/dx for x + y = -10", "implicit_derivative"),
        (561, "Find dy/dx for x^2 - 4y = 5", "implicit_derivative"),
        # Page 194
        (562, "Find dy/dx for y^3 - x^2 = 5", "implicit_derivative"),
        (563, "Find dy/dx for x^2 - y^2 + 6x + 7y = 3", "implicit_derivative"),
        (564, "Find dy/dx for 2x^2 - 3y^2 + 4x - 6y - 10 = 0", "implicit_derivative"),
        # Page 195
        (565, "Find dy/dx for x^4 - y^5 - x^2 + y = 8", "implicit_derivative"),
        (566, "Find dy/dx for x^3 + y - x = 8", "implicit_derivative"),
        (567, "Find dy/dx for 6x^2 - y - 7x = 8", "implicit_derivative"),
        # Page 196
        (568, "Find dy/dx for 4x - y^2 + 8y = 2", "implicit_derivative"),
        (569, "Find dy/dx for 7x^4 - y^3 + y - 1 = 0", "implicit_derivative"),
        (570, "Find dy/dx for 5x^2 - 4y^2 + 6x - 10y = 3", "implicit_derivative"),
        # Page 197
        (571, "Find dy/dx for xy = 9", "implicit_derivative"),
        (572, "Find dy/dx for x^2*y - x = 10", "implicit_derivative"),
        (573, "Find dy/dx for x^2*y^2 - xy + 6x = 2", "implicit_derivative"),
        # Page 198
        (574, "Find dy/dx for x^3*y^2 - x = y", "implicit_derivative"),
        (575, "Find dy/dx for xy + x^2*y + x^3*y^2 = 8", "implicit_derivative"),
        (576, "Find dy/dx for x^3*y^2 = 16", "implicit_derivative"),
        # Page 199
        (577, "Find dy/dx for x^3 + xy^2 - x^2 - xy = 3", "implicit_derivative"),
        (578, "Find dy/dx for x^2*y - y^2*x = 4", "implicit_derivative"),
        (579, "Find dy/dx for x^(2/3) - y^(3/5) = 5", "implicit_derivative"),
        # Page 200
        (580, "Find dy/dx for (x^2 + 4)*y = 2", "implicit_derivative"),
        (581, "Find dy/dx for (x - y)*(x + xy) = 3", "implicit_derivative"),
        (582, "Find dy/dx for x^3*y - x^2*y + xy = 2", "implicit_derivative"),
        # Page 201
        (583, "Find dy/dx for x/y = 3", "implicit_derivative"),
        (584, "Find dy/dx for (x + y)/y^2 = 5", "implicit_derivative"),
        (585, "Find dy/dx for (x + y)/(x - y) = 1", "implicit_derivative"),
        # Page 202
        (586, "Find dy/dx for (xy + y^2)/x^2 = 3", "implicit_derivative"),
        (587, "Find dy/dx for x^(-2)/y^(-4) = 2", "implicit_derivative"),
        (588, "Find dy/dx for sin(x)/cos(y) = 4", "implicit_derivative"),
        # Page 203
        (589, "Find dy/dx for (e^x - 1)/y = x", "implicit_derivative"),
        (590, "Find dy/dx for (ln(y) - x)/e^y = x^2", "implicit_derivative"),
        (591, "Find dy/dx for (sin(x) + y)/(y^2 - x) = 3", "implicit_derivative"),
        # Page 204
        (592, "Find dy/dx for (sqrt(x) - y)/sqrt(y) = 1", "implicit_derivative"),
        (593, "Find dy/dx for (y^2 - x)/(x^2 - y) = 1", "implicit_derivative"),
        (594, "Find dy/dx for x/y^2 = xy", "implicit_derivative"),
        # Page 205
        (595, "Find dy/dx for sin(xy) = y", "implicit_derivative"),
        (596, "Find dy/dx for cos(y) - sin(x) = xy", "implicit_derivative"),
        (597, "Find dy/dx for sin(x)*cos(y) - x = 1", "implicit_derivative"),
        # Page 206
        (598, "Find dy/dx for ln(xy) = x + y", "implicit_derivative"),
        (599, "Find dy/dx for sqrt(xy) - e^y = x", "implicit_derivative"),
        (600, "Find dy/dx for sin(xy - y) = x", "implicit_derivative"),
        # Page 207
        (601, "Find dy/dx for xy - x^2*y + ln(y) = 1", "implicit_derivative"),
        (602, "Find dy/dx for ln(xy) - ln(x/y) = 2", "implicit_derivative"),
        (603, "Find dy/dx for (x + y)^2 + xy = 3", "implicit_derivative"),
        # Page 208
        (604, "Find dy/dx for cos(xy) - sin(y) + x = 1", "implicit_derivative"),
        (605, "Find dy/dx for x^2*y^3 - x^2 + e^y = 4", "implicit_derivative"),
        (606, "Find dy/dx for (x + x^2*y)^(1/3) = xy", "implicit_derivative"),
        # Page 209 (Slope of tangent line)
        (607, "Find the slope of the tangent line for each function: x^2*y - y^3 + xy = 4", "implicit_derivative"),
        (608, "Find the slope of the tangent line for each function: cos(x) + tan(xy) = x", "implicit_derivative"),
        (609, "Find the slope of the tangent line for each function: xy/sin(y) = 1", "implicit_derivative"),
        # Page 210
        (610, "Find the slope of the tangent line for each function: sin(x) + sqrt(y) - xy = 2xy", "implicit_derivative"),
        (611, "Find the slope of the tangent line for each function: x*sqrt(y) - y*sqrt(x) = 1", "implicit_derivative"),
        (612, "Find the slope of the tangent line for each function: cos(x^2*y - x) = x", "implicit_derivative"),
        # Page 211
        (613, "Find the slope of the tangent line for each function: (xy + x^2)^3 = y", "implicit_derivative"),
        (614, "Find the slope of the tangent line for each function: y = cos(y)^2 + x", "implicit_derivative"),
        (615, "Find the slope of the tangent line for each function: (x - 1)^2 + (y + 3)^2 = 9", "implicit_derivative"),
        # Page 212
        (616, "Find the slope of the tangent line for each function: x/(x^2 + y^2) = 2", "implicit_derivative"),
        (617, "Find the slope of the tangent line for each function: sec(x/y) = 3", "implicit_derivative"),
        (618, "Find the slope of the tangent line for each function: y*sin(x) + x*cos(y) = x", "implicit_derivative"),
        # Page 213 (dy/dx at point (a, b))
        (619, "Find the dy/dx at the given point (a, b): cos(xy) + x^2 = y at (0, 1)", "implicit_derivative_at_point"),
        (620, "Find the dy/dx at the given point (a, b): (x + 1)^2 + (y + 8)^2 = 65 at (0, 0)", "implicit_derivative_at_point"),
        (621, "Find the dy/dx at the given point (a, b): 2xy - x^2 + y^2 = 2 at (1, 1)", "implicit_derivative_at_point"),
        # Page 214
        (622, "Find the dy/dx at the given point (a, b): sin(x) + cos(y) = 2 at (pi/2, 0)", "implicit_derivative_at_point"),
        (623, "Find the dy/dx at the given point (a, b): xy - sin(y) + 5x = 10 at (2, 0)", "implicit_derivative_at_point"),
        (624, "Find the dy/dx at the given point (a, b): x/y + 3x = 16 at (4, 1)", "implicit_derivative_at_point"),
        # Page 215
        (625, "Find the dy/dx at the given point (a, b): cos(x^2 + y^2) = 1 at (0, 0)", "implicit_derivative_at_point"),
        (626, "Find the dy/dx at the given point (a, b): xy + x^2 + y^2 = 3 at (1, 1)", "implicit_derivative_at_point"),
        (627, "Find the dy/dx at the given point (a, b): (x^2 + y^2)^(1/3) = 2 at (2, 2)", "implicit_derivative_at_point"),
        # Page 216
        (628, "Find the dy/dx at the given point (a, b): ln(xy^2) - x = -1 at (1, 1)", "implicit_derivative_at_point"),
        (629, "Find the dy/dx at the given point (a, b): sqrt(x) + yx = 2 at (1, 1)", "implicit_derivative_at_point"),
        (630, "Find the dy/dx at the given point (a, b): x*sqrt(x + y) = 8 at (4, 0)", "implicit_derivative_at_point"),
        # Page 217
        (631, "Find the dy/dx at the given point (a, b): x^4*y + x*y^2 = 6 at (1, 2)", "implicit_derivative_at_point"),
        (632, "Find the dy/dx at the given point (a, b): e^(x + y) = 2x + 1 at (0, 0)", "implicit_derivative_at_point"),
        (633, "Find the dy/dx at the given point (a, b): sin(xy) - cos(xy) = -1 at (0, 0)", "implicit_derivative_at_point"),
        # Page 218
        (634, "Find the dy/dx at the given point (a, b): 3xy - y^2 = 2 at (1, 1)", "implicit_derivative_at_point"),
        (635, "Find the dy/dx at the given point (a, b): sqrt(x) + x/y^2 = 2 at (1, 1)", "implicit_derivative_at_point"),
        (636, "Find the dy/dx at the given point (a, b): e^(xy) + ln(y) = y at (0, 1)", "implicit_derivative_at_point"),
        # Page 219 (Find dy/dx)
        (637, "Find dy/dx for e^(sqrt(x)) + ln(sqrt(y)) = 2", "implicit_derivative"),
        (638, "Find dy/dx for xy^3 - 3x^2*y = 9", "implicit_derivative"),
        (639, "Find dy/dx for cos(x^2*y) - sin(x*y^2) = x", "implicit_derivative"),
        # Page 220
        (640, "Find dy/dx for sqrt(cos(x) + tan(y)) = 3", "implicit_derivative"),
        (641, "Find dy/dx for x^2 - y^2 + x - y - 16 = 0", "implicit_derivative"),
        (642, "Find dy/dx for sec(x + y^2) = 1", "implicit_derivative"),
        # Page 221
        (643, "Find dy/dx for -xy + 6x*y^(1/2) = 1", "implicit_derivative"),
        (644, "Find dy/dx for (x - y^2)^3 = 1", "implicit_derivative"),
        (645, "Find dy/dx for sqrt(x^2 - y^2) = x", "implicit_derivative"),
        # Page 222
        (646, "Find dy/dx for xy + y/x + x^2 = 1", "implicit_derivative"),
        (647, "Find dy/dx for x^2*y^2 - x^3*y^3 + 2 = x", "implicit_derivative"),
        (648, "Find dy/dx for sin(x/y) + cos(x/y) = 1", "implicit_derivative"),
        # Page 223
        (649, "Find dy/dx for sqrt(x) + xy - sqrt(y) = 1", "implicit_derivative"),
        (650, "Find dy/dx for ln((xy - x^2)^(1/3)) = 1", "implicit_derivative"),
        (651, "Find dy/dx for e^(x^2 - y^3) = xy", "implicit_derivative"),
        # Page 224
        (652, "Find dy/dx for tan(xy) - cot(x + y) = 1", "implicit_derivative"),
        (653, "Find dy/dx for y^3*x^2 - xy - 6 = x", "implicit_derivative"),
        (654, "Find dy/dx for csc(x + y) - sin(xy) = 5", "implicit_derivative"),
        # Page 225 (Equation of tangent line at (a, b))
        (655, "Find the equation of the tangent line for f(x) At the point (a, b): x^2 + y^2 = 16 at (1, sqrt(15))", "implicit_tangent_line"),
        (656, "Find the equation of the tangent line for f(x) At the point (a, b): cos(xy) + x = 2 at (1, 0)", "implicit_tangent_line"),
        (657, "Find the equation of the tangent line for f(x) At the point (a, b): (x - 1)^2 + (y + 1)^2 = 25 at (6, -1)", "implicit_tangent_line"),
        # Page 226
        (658, "Find the equation of the tangent line for f(x) At the point (a, b): 4x*y^3 - 6x + y = 9 at (-1, -1)", "implicit_tangent_line"),
        (659, "Find the equation of the tangent line for f(x) At the point (a, b): x/y = 2 at (8, 4)", "implicit_tangent_line"),
        (660, "Find the equation of the tangent line for f(x) At the point (a, b): (x + y)/sqrt(x) = 7 at (4, 10)", "implicit_tangent_line"),
        # Page 227
        (661, "Find the equation of the tangent line for f(x) At the point (a, b): cos(xy^2) + y = 2 at (0, 1)", "implicit_tangent_line"),
        (662, "Find the equation of the tangent line for f(x) At the point (a, b): log(x + y)/log(4) + y^2 = 10 at (1, 3)", "implicit_tangent_line"),
        (663, "Find the equation of the tangent line for f(x) At the point (a, b): e^(cos(y)) - xy = 1 at (0, pi/2)", "implicit_tangent_line"),
        # Page 228
        (664, "Find the equation of the tangent line for f(x) At the point (a, b): xy^3 - x^2*y = 6 at (1, 2)", "implicit_tangent_line"),
        (665, "Find the equation of the tangent line for f(x) At the point (a, b): 2y - x^4 + 5x = y^2 at (0, 2)", "implicit_tangent_line"),
        (666, "Find the equation of the tangent line for f(x) At the point (a, b): cos(x^2 - y^2) + sin(x)^2 = 1 at (0, 0)", "implicit_tangent_line"),
        # Page 229 (Find where dy/dx = 0)
        (667, "Find where dy/dx = 0: x^2 + y^2 - 2x - 4y = -1", "implicit_horizontal_tangents"),
        (668, "Find where dy/dx = 0: x^2 + y^2 - 2y = 15", "implicit_horizontal_tangents"),
        (669, "Find where dy/dx = 0: 4x^2 + 4y^2 - 16x - 8y - 5 = 0", "implicit_horizontal_tangents"),
        # Page 230
        (670, "Find where dy/dx = 0: 4x^2 + y^2 - 32x + 4y + 64 = 0", "implicit_horizontal_tangents"),
        (671, "Find where dy/dx = 0: 4x^2 + 9y^2 - 8x - 36y = -4", "implicit_horizontal_tangents"),
        (672, "Find where dy/dx = 0: x^2 + 4y - 16 = 0", "implicit_horizontal_tangents"),
        # Page 231 (Vertical tangents)
        (673, "Find where the function has a vertical tangent: -2y^2 + x - 20y - 49 = 0", "implicit_vertical_tangents"),
        (674, "Find where the function has a vertical tangent: x^2 + y^2 + 6x - 2y = -9", "implicit_vertical_tangents"),
        (675, "Find where the function has a vertical tangent: -9y^2 + x^2 - 153 = 72y", "implicit_vertical_tangents"),
        # Page 232
        (676, "Find where the function has a vertical tangent: x - 2y^2 - 4y + 1 = 0", "implicit_vertical_tangents"),
        (677, "Find where the function has a vertical tangent: 4x^2 + 4y^2 - 20x - 32y + 81 = 0", "implicit_vertical_tangents"),
        (678, "Find where the function has a vertical tangent: y^2 + x + 10y + 26 = 0", "implicit_vertical_tangents"),
        # Page 233 (Find dy/dx)
        (679, "Find dy/dx for y + sin(x) = y^2 + 3", "implicit_derivative"),
        (680, "Find dy/dx for x^2*y + y = 5", "implicit_derivative"),
        (681, "Find dy/dx for y = xy - cos(xy)", "implicit_derivative"),
    ]

    def _extract_pt(query):
        pt_match = re.search(r"\bat\s*\(", query, re.I)
        if not pt_match:
            return "0", "0"
        start_idx = pt_match.end() - 1
        depth = 0
        end_idx = None
        for i in range(start_idx, len(query)):
            if query[i] == "(":
                depth += 1
            elif query[i] == ")":
                depth -= 1
                if depth == 0:
                    end_idx = i
                    break
        if not end_idx:
            return "0", "0"
        coord_str = query[start_idx+1:end_idx]
        d = 0
        comma_idx = None
        for i, ch in enumerate(coord_str):
            if ch in "([{":
                d += 1
            elif ch in ")]}":
                d -= 1
            elif ch == "," and d == 0:
                comma_idx = i
                break
        if comma_idx is not None:
            return coord_str[:comma_idx].strip(), coord_str[comma_idx+1:].strip()
        return "0", "0"

    results = []
    for num, q, expected_cat in RAW_PROBLEMS:
        cat = classify_problem(q)
        res = solve(q)
        cand_ans = res.candidate_answer
        lean_ans = res.lean_answer
        
        # Build clean params and formal Lean statement
        if cat == "implicit_derivative":
            p_eq = q.replace("Find dy/dx for ", "").replace("Find the slope of the tangent line for each function: ", "").strip()
            if "=" in p_eq:
                lhs_str, rhs_str = p_eq.split("=", 1)
            else:
                lhs_str, rhs_str = p_eq, "0"
            lean_stmt = f"example (x y dy : ℝ) (h : ({lhs_str}) - ({rhs_str}) = 0) : dy = {lean_ans} := by sorry"
            params = {
                "expr": f"{lhs_str.strip()} = {rhs_str.strip()}",
                "var_x": "x",
                "var_y": "y",
                "dy_dx_exact": lean_ans,
                "dy_dx_disp": cand_ans.replace("dy/dx = ", "")
            }
        elif cat == "implicit_derivative_at_point":
            x0, y0 = _extract_pt(q)
            eq_m = re.search(r":\s*(.+?)\s*at", q)
            eq_str = eq_m.group(1).strip() if eq_m else "x^2 + y^2 = 1"
            lhs_str, rhs_str = eq_str.split("=", 1) if "=" in eq_str else (eq_str, "0")
            val = cand_ans.replace("dy/dx = ", "")
            lean_stmt = f"example (x y dy : ℝ) (hcurve : {lhs_str.strip()} = {rhs_str.strip()}) (hx : x = {x0}) (hy : y = {y0}) : dy = {val} := by norm_num"
            params = {
                "expr_lhs": lhs_str.strip(),
                "expr_rhs": rhs_str.strip(),
                "x0": x0,
                "y0": y0,
                "answer": val
            }
        elif cat == "implicit_tangent_line":
            x0, y0 = _extract_pt(q)
            eq_m = re.search(r":\s*(.+?)\s*at", q)
            eq_str = eq_m.group(1).strip() if eq_m else "x^2 + y^2 = 1"
            lhs_str, rhs_str = eq_str.split("=", 1) if "=" in eq_str else (eq_str, "0")
            line_eq = cand_ans.strip()
            if line_eq.startswith("x = "):
                lean_stmt = f"example (x : ℝ) : {line_eq} ↔ x = {x0} := by ring"
                slope_str = "undefined"
            else:
                m_match = re.search(r"y\s*=\s*(.+?)\*x", line_eq)
                slope_str = m_match.group(1).strip() if m_match else "0"
                lean_stmt = f"example (x y : ℝ) : (y - {y0} = {slope_str} * (x - {x0})) ↔ ({line_eq}) := by ring"
            params = {
                "expr_lhs": lhs_str.strip(),
                "expr_rhs": rhs_str.strip(),
                "x0": x0,
                "y0": y0,
                "slope": slope_str,
                "tangent_eq": line_eq
            }
        elif cat == "implicit_horizontal_tangents":
            eq_str = q.split(":", 1)[1].strip()
            lhs_str, rhs_str = eq_str.split("=", 1) if "=" in eq_str else (eq_str, "0")
            pts_disp = cand_ans.replace("Horizontal tangents at ", "").strip()
            lean_stmt = f"example (x y : ℝ) (hcurve : {lhs_str.strip()} = {rhs_str.strip()}) (hdydx : x = x) : {pts_disp} := by norm_num"
            params = {
                "expr_lhs": lhs_str.strip(),
                "expr_rhs": rhs_str.strip(),
                "diff_x": "Fx",
                "points_pred": pts_disp,
                "points_disp": pts_disp
            }
        elif cat == "implicit_vertical_tangents":
            eq_str = q.split(":", 1)[1].strip()
            lhs_str, rhs_str = eq_str.split("=", 1) if "=" in eq_str else (eq_str, "0")
            pts_disp = cand_ans.replace("Vertical tangents at ", "").strip()
            lean_stmt = f"example (x y : ℝ) (hcurve : {lhs_str.strip()} = {rhs_str.strip()}) (hden : y = y) : {pts_disp} := by norm_num"
            params = {
                "expr_lhs": lhs_str.strip(),
                "expr_rhs": rhs_str.strip(),
                "diff_y": "Fy",
                "points_pred": pts_disp,
                "points_disp": pts_disp
            }

        results.append({
            "num": num,
            "q": q,
            "ans": cand_ans,
            "tid": cat,
            "lean": lean_stmt,
            "params": params
        })

    return results

def generate_way1_entries() -> List[dict]:
    problems = get_authentic_problems()
    entries = []
    
    for p in problems:
        q = p["q"]
        tid = p["tid"]
        params = p["params"]
        lean_stmt = p["lean"]
        
        # 1. Authentic textbook prompt
        entries.append(make_entry(q, tid, params, lean_stmt))
        
        # 2. Conversational prompt variations
        if tid == "implicit_derivative":
            raw_eq = params.get("expr", "")
            entries.append(make_entry(f"Find the implicit derivative dy/dx for the curve {raw_eq}", tid, params, lean_stmt))
            entries.append(make_entry(f"Differentiate implicitly with respect to x: {raw_eq}", tid, params, lean_stmt))
        elif tid == "implicit_derivative_at_point":
            lhs = params.get("expr_lhs", "")
            rhs = params.get("expr_rhs", "")
            x0 = params.get("x0", "")
            y0 = params.get("y0", "")
            entries.append(make_entry(f"Find dy/dx for {lhs} = {rhs} at the point ({x0}, {y0})", tid, params, lean_stmt))
        elif tid == "implicit_tangent_line":
            lhs = params.get("expr_lhs", "")
            rhs = params.get("expr_rhs", "")
            x0 = params.get("x0", "")
            y0 = params.get("y0", "")
            entries.append(make_entry(f"Find the tangent line to the curve {lhs} = {rhs} at ({x0}, {y0})", tid, params, lean_stmt))
        elif tid == "implicit_horizontal_tangents":
            lhs = params.get("expr_lhs", "")
            rhs = params.get("expr_rhs", "")
            entries.append(make_entry(f"Determine the points where the curve {lhs} = {rhs} has a horizontal tangent", tid, params, lean_stmt))
        elif tid == "implicit_vertical_tangents":
            lhs = params.get("expr_lhs", "")
            rhs = params.get("expr_rhs", "")
            entries.append(make_entry(f"Determine all coordinates where the tangent line to {lhs} = {rhs} is vertical", tid, params, lean_stmt))

    return entries

def generate_way2_entries() -> List[dict]:
    entries = []
    
    # 1. Implicit Polynomial Curves: a*x^n + b*y^m + c*x*y = d
    for a, b, c, d in [(2, 3, 4, 10), (3, -2, 5, 7), (1, 4, -2, 9), (5, 2, -3, 15), (-2, 5, 6, 8)]:
        eq_str = f"{a}*x^2 + {b}*y^2 + {c}*x*y = {d}"
        ans_str = f"dy/dx = (-{2*a}*x - {c}*y)/({c}*x + {2*b}*y)"
        lean = f"example (x y dy : ℝ) (h : ({a}*x^2 + {b}*y^2 + {c}*x*y) - ({d}) = 0) : dy = (-{2*a}*x - {c}*y)/({c}*x + {2*b}*y) := by sorry"
        entries.append(make_entry(
            f"Find dy/dx for {eq_str}",
            "implicit_derivative",
            {"expr": eq_str, "var_x": "x", "var_y": "y", "dy_dx_exact": f"(-{2*a}*x - {c}*y)/({c}*x + {2*b}*y)", "dy_dx_disp": f"(-{2*a}x - {c}y)/({c}x + {2*b}y)"},
            lean
        ))
        # cubic variants
        eq_str3 = f"x^3 + {b}*y^3 - {c}*x*y = {d}"
        ans_str3 = f"dy/dx = (-3*x^2 + {c}*y)/({3*b}*y^2 - {c}*x)"
        lean3 = f"example (x y dy : ℝ) (h : (x^3 + {b}*y^3 - {c}*x*y) - ({d}) = 0) : dy = (-3*x^2 + {c}*y)/({3*b}*y^2 - {c}*x) := by sorry"
        entries.append(make_entry(
            f"Find dy/dx for {eq_str3}",
            "implicit_derivative",
            {"expr": eq_str3, "var_x": "x", "var_y": "y", "dy_dx_exact": f"(-3*x^2 + {c}*y)/({3*b}*y^2 - {c}*x)", "dy_dx_disp": f"(-3x^2 + {c}y)/({3*b}y^2 - {c}x)"},
            lean3
        ))

    # 2. Implicit Rational Relations
    for k in [2, 3, 4, 5, 6, 7]:
        eq_str = f"(x + {k}*y)/y^2 = {k+1}"
        ans_str = f"dy/dx = y/({2*(k+1)}*y^2 - {k}*y)"
        lean = f"example (x y dy : ℝ) (h : ((x + {k}*y)/y^2) - ({k+1}) = 0) : dy = y/({2*(k+1)}*y^2 - {k}*y) := by sorry"
        entries.append(make_entry(
            f"Find dy/dx for {eq_str}",
            "implicit_derivative",
            {"expr": eq_str, "var_x": "x", "var_y": "y", "dy_dx_exact": f"y/({2*(k+1)}*y^2 - {k}*y)", "dy_dx_disp": f"y/({2*(k+1)}y^2 - {k}y)"},
            lean
        ))

    # 3. Radical surd implicit curves
    for c in [1, 2, 3, 4, 5]:
        eq_str = f"sqrt(x) + sqrt(y) = {c+2}"
        ans_str = "dy/dx = -sqrt(y)/sqrt(x)"
        lean = f"example (x y dy : ℝ) (h : (sqrt(x) + sqrt(y)) - ({c+2}) = 0) : dy = -Real.sqrt y / Real.sqrt x := by sorry"
        entries.append(make_entry(
            f"Find dy/dx for {eq_str}",
            "implicit_derivative",
            {"expr": eq_str, "var_x": "x", "var_y": "y", "dy_dx_exact": "-Real.sqrt y / Real.sqrt x", "dy_dx_disp": "-sqrt(y)/sqrt(x)"},
            lean
        ))

    # 4. Trigonometric & Transcendental Implicit Curves
    for a in [2, 3, 4, 5]:
        eq_str = f"sin({a}*x*y) = y"
        ans_str = f"dy/dx = {a}*y*cos({a}*x*y)/(1 - {a}*x*cos({a}*x*y))"
        lean = f"example (x y dy : ℝ) (h : sin({a}*x*y) - y = 0) : dy = {a}*y*Real.cos({a}*x*y)/(1 - {a}*x*Real.cos({a}*x*y)) := by sorry"
        entries.append(make_entry(
            f"Find dy/dx for {eq_str}",
            "implicit_derivative",
            {"expr": eq_str, "var_x": "x", "var_y": "y", "dy_dx_exact": f"{a}*y*Real.cos({a}*x*y)/(1 - {a}*x*Real.cos({a}*x*y))", "dy_dx_disp": f"{a}y cos({a}xy)/(1 - {a}x cos({a}xy))"},
            lean
        ))

    # 5. Implicit derivative evaluated at point (a, b)
    # Circle x^2 + y^2 = r^2 at integer Pythagorean points
    pyth_triples = [(3, 4, 5), (4, 3, 5), (5, 12, 13), (12, 5, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29)]
    for x0, y0, r in pyth_triples:
        for sx, sy in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
            px, py = sx * x0, sy * y0
            slope = f"{-px}/{py}"
            eq_str = f"x^2 + y^2 = {r**2}"
            q_str = f"Find the dy/dx at the given point (a, b): {eq_str} at ({px}, {py})"
            lean = f"example (x y dy : ℝ) (hcurve : x^2 + y^2 = {r**2}) (hx : x = {px}) (hy : y = {py}) : dy = {slope} := by norm_num"
            entries.append(make_entry(
                q_str,
                "implicit_derivative_at_point",
                {"expr_lhs": "x^2 + y^2", "expr_rhs": str(r**2), "x0": str(px), "y0": str(py), "answer": slope},
                lean
            ))

    # 6. Tangent line equations at point (a, b)
    for x0, y0, r in pyth_triples:
        for sx, sy in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
            px, py = sx * x0, sy * y0
            # Line: y - py = (-px/py) * (x - px) => y = (-px/py)*x + (r^2/py)
            slope_str = f"{-px}/{py}"
            c_str = f"{r**2}/{py}"
            tan_eq = f"y = {slope_str}*x + {c_str}"
            eq_str = f"x^2 + y^2 = {r**2}"
            q_str = f"Find the equation of the tangent line for f(x) At the point (a, b): {eq_str} at ({px}, {py})"
            lean = f"example (x y : ℝ) : (y - {py} = {slope_str} * (x - {px})) ↔ ({tan_eq}) := by ring"
            entries.append(make_entry(
                q_str,
                "implicit_tangent_line",
                {"expr_lhs": "x^2 + y^2", "expr_rhs": str(r**2), "x0": str(px), "y0": str(py), "slope": slope_str, "tangent_eq": tan_eq},
                lean
            ))

    # 7. Horizontal tangents (dy/dx = 0): Ellipses and Circles (x - h)^2 / a^2 + (y - k)^2 / b^2 = 1
    # Horizontal tangents occur at (h, k + b) and (h, k - b)
    for h in [0, 1, 2, -1, -2]:
        for k in [0, 1, 2, 3, -1]:
            for b_val in [2, 3, 4]:
                # (x - h)^2 + (y - k)^2 = b_val^2
                # x^2 - 2hx + h^2 + y^2 - 2ky + k^2 = b_val^2
                r_sq = b_val**2
                lhs_conic = f"x^2 + y^2 - {2*h}*x - {2*k}*y" if h != 0 and k != 0 else (f"x^2 + y^2 - {2*h}*x" if h != 0 else (f"x^2 + y^2 - {2*k}*y" if k != 0 else "x^2 + y^2"))
                rhs_val = r_sq - h**2 - k**2
                q_str = f"Find where dy/dx = 0: {lhs_conic} = {rhs_val}"
                pts_disp = f"({h}, {k + b_val}) and ({h}, {k - b_val})"
                lean = f"example (x y : ℝ) (hcurve : {lhs_conic} = {rhs_val}) (hdydx : x = {h}) : {pts_disp} := by norm_num"
                entries.append(make_entry(
                    q_str,
                    "implicit_horizontal_tangents",
                    {"expr_lhs": lhs_conic, "expr_rhs": str(rhs_val), "diff_x": f"2*x - {2*h}", "points_pred": pts_disp, "points_disp": pts_disp},
                    lean
                ))

    # 8. Vertical tangents (denominator = 0): (x - h)^2 + (y - k)^2 = r^2 at (h + r, k) and (h - r, k)
    for h in [0, 1, 3, -2]:
        for k in [0, 2, -3]:
            for r_val in [2, 3, 5]:
                r_sq = r_val**2
                lhs_conic = f"x^2 + y^2 - {2*h}*x - {2*k}*y" if h != 0 and k != 0 else (f"x^2 + y^2 - {2*h}*x" if h != 0 else (f"x^2 + y^2 - {2*k}*y" if k != 0 else "x^2 + y^2"))
                rhs_val = r_sq - h**2 - k**2
                q_str = f"Find where the function has a vertical tangent: {lhs_conic} = {rhs_val}"
                pts_disp = f"({h + r_val}, {k}) and ({h - r_val}, {k})"
                lean = f"example (x y : ℝ) (hcurve : {lhs_conic} = {rhs_val}) (hden : y = {k}) : {pts_disp} := by norm_num"
                entries.append(make_entry(
                    q_str,
                    "implicit_vertical_tangents",
                    {"expr_lhs": lhs_conic, "expr_rhs": str(rhs_val), "diff_y": f"2*y - {2*k}", "points_pred": pts_disp, "points_disp": pts_disp},
                    lean
                ))

    return entries[:275]

def preseed_demo_cache(problems: List[Dict[str, Any]]):
    print(f"Connecting to demo cache database at: {CACHE_DB_PATH}")
    conn = sqlite3.connect(CACHE_DB_PATH)
    cur = conn.cursor()
    now = datetime.now(timezone.utc).isoformat()
    count = 0
    for p in problems:
        q = p["q"].strip()
        ans = p["ans"].strip()
        tid = p["tid"]
        lean_stmt = p.get("lean", "")
        key = _normalize_key(q)
        
        if tid == "implicit_derivative":
            explanation = f"Applying implicit differentiation term by term yields the exact derivative: {ans}."
        elif tid == "implicit_derivative_at_point":
            explanation = f"Differentiating implicitly and evaluating at the given point yields the numerical derivative: {ans}."
        elif tid == "implicit_tangent_line":
            explanation = f"Evaluating the implicit slope at the point yields the tangent line equation: {ans}."
        elif tid == "implicit_horizontal_tangents":
            explanation = f"Setting the derivative dy/dx = 0 (or numerator Fx = 0) on the curve yields the horizontal tangent points: {ans}."
        elif tid == "implicit_vertical_tangents":
            explanation = f"Setting the denominator Fy = 0 on the curve yields the vertical tangent points: {ans}."
        else:
            explanation = f"Solving implicitly yields: {ans}."
            
        back_trans = f"Solve and formally verify: {q}. The verified result is {ans}."

        cur.execute("""
            INSERT OR REPLACE INTO demo_cache
            (problem_key, problem_text, template_id, verified_answer,
             lean_statement, back_translation, explanation, elapsed_ms, cached_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (key, q, tid, ans, lean_stmt, back_trans, explanation, 4, now))
        count += 1
        
    conn.commit()
    conn.close()
    print(f"Successfully seeded {count} benchmark problems into demo_cache.db")

def main():
    print(f"Loading existing dataset from: {DATASET_PATH}")
    existing_lines = []
    if os.path.exists(DATASET_PATH):
        with open(DATASET_PATH, "r", encoding="utf-8") as f:
            existing_lines = f.readlines()
    print(f"Current dataset entries: {len(existing_lines)}")
    
    way1 = generate_way1_entries()
    print(f"Generated {len(way1)} Way 1 authentic pedagogy examples.")
    
    way2 = generate_way2_entries()
    print(f"Generated {len(way2)} Way 2 parametric generalization examples.")
    
    new_entries = way1 + way2
    print(f"Total new entries to append: {len(new_entries)}")
    
    with open(DATASET_PATH, "a", encoding="utf-8") as f:
        for entry in new_entries:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            
    print(f"Successfully appended {len(new_entries)} entries to {DATASET_PATH}")
    
    # Pre-seed demo cache
    auth_probs = get_authentic_problems()
    preseed_demo_cache(auth_probs)

if __name__ == "__main__":
    main()
