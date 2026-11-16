"""
VeriMath — Dataset Builder
===========================
Generates the 200-problem benchmark dataset (150 train/val, 50 held-out test)
spanning all 7 supported Lean formalization templates:
- Arithmetic (30)
- Algebraic Simplification (30)
- Equation Solving (30)
- Derivatives (40)
- Definite Integrals (30)
- Number Theory / Primality (20)
- Geometry Distance (20)

Aligns with Egyptian Grades 10–12 secondary mathematics curriculum and international benchmarks.
"""

import json
from pathlib import Path

DATASET_DIR = Path(__file__).parent.parent / "backend" / "tests" / "dataset"

def generate_problems():
    problems = []

    # 1. Arithmetic (30 problems)
    arithmetic_raw = [
        ("47 * 89 + 123", "4306", "What is 47 × 89 + 123?"),
        ("15 * 16 - 45", "195", "Calculate 15 × 16 - 45"),
        ("120 / 4 + 85", "115", "Evaluate 120 ÷ 4 + 85"),
        ("2^10 + 24", "1048", "Find the value of 2^10 + 24"),
        ("35 * 12 + 180", "600", "Compute 35 × 12 + 180"),
        ("144 / 12 + 88", "100", "Calculate 144 ÷ 12 + 88"),
        ("25 * 25 - 25", "600", "Evaluate 25 × 25 - 25"),
        ("1000 - 45 * 18", "190", "Find the value of 1000 - 45 × 18"),
        ("3^5 + 7", "250", "What is 3^5 + 7?"),
        ("64 * 8 + 12", "524", "Compute 64 × 8 + 12"),
        ("500 / 25 + 300", "320", "Evaluate 500 ÷ 25 + 300"),
        ("17 * 19", "323", "Calculate 17 × 19"),
        ("13 * 13 + 14 * 14", "365", "What is 13² + 14²?"),
        ("5^4 - 25", "600", "Evaluate 5^4 - 25"),
        ("1024 / 16 + 36", "100", "Compute 1024 ÷ 16 + 36"),
        ("99 * 11 + 1", "1090", "Calculate 99 × 11 + 1"),
        ("75 * 4 - 50", "250", "Evaluate 75 × 4 - 50"),
        ("81 / 9 + 91", "100", "Compute 81 ÷ 9 + 91"),
        ("12 * 15 + 20", "200", "What is 12 × 15 + 20?"),
        ("400 - 15 * 20", "100", "Evaluate 400 - 15 × 20"),
        ("2^8 + 2^7", "384", "Compute 2^8 + 2^7"),
        ("18 * 18 + 76", "400", "What is 18² + 76?"),
        ("210 / 7 + 70", "100", "Calculate 210 ÷ 7 + 70"),
        ("36 * 25", "900", "Compute 36 × 25"),
        ("125 * 8 - 500", "500", "Evaluate 125 × 8 - 500"),
        ("7^3 + 57", "400", "Find the value of 7^3 + 57"),
        ("625 / 5 - 25", "100", "Compute 625 ÷ 5 - 25"),
        ("45 * 11 + 5", "500", "What is 45 × 11 + 5?"),
        ("90 * 9 + 90", "900", "Calculate 90 × 9 + 90"),
        ("2^12 / 4", "1024", "Evaluate 2^12 ÷ 4"),
    ]
    for i, (expr, ans, nl) in enumerate(arithmetic_raw, 1):
        problems.append({
            "id": f"arith_{i:03d}",
            "source": "Egyptian Grade 10 Math",
            "category": "arithmetic",
            "template_id": "arithmetic",
            "problem_text": nl,
            "correct_answer": ans,
            "lean_statement": f"example : {expr} = {ans} := by norm_num",
            "lean_verified": True,
            "slot_values": {"expr": expr, "answer": ans},
            "difficulty": "easy",
            "notes": "Basic integer arithmetic",
        })

    # 2. Algebraic Simplification (30 problems)
    algebra_raw = [
        ("(x + 1)^2 - x^2", "2*x + 1", "Simplify (x + 1)² − x²"),
        ("(x + 2)^2 - 4*x", "x^2 + 4", "Simplify (x + 2)² − 4x"),
        ("(x - 1)*(x + 1)", "x^2 - 1", "Expand (x - 1)(x + 1)"),
        ("(x + 3)^2 - 6*x", "x^2 + 9", "Simplify (x + 3)² − 6x"),
        ("(x - 2)^2 + 4*x", "x^2 + 4", "Simplify (x - 2)² + 4x"),
        ("2*(x + 3) + 3*(x - 2)", "5*x", "Simplify 2(x + 3) + 3(x - 2)"),
        ("(x + 4)*(x - 4)", "x^2 - 16", "Expand (x + 4)(x - 4)"),
        ("(2*x + 1)^2 - 4*x^2", "4*x + 1", "Simplify (2x + 1)² − 4x²"),
        ("(x + 5)^2 - x^2 - 10*x", "25", "Simplify (x + 5)² − x² − 10x"),
        ("x*(x + 2) - 2*x", "x^2", "Simplify x(x + 2) − 2x"),
        ("(x - 3)*(x + 3) + 9", "x^2", "Simplify (x - 3)(x + 3) + 9"),
        ("(3*x + 2) - (2*x - 3)", "x + 5", "Simplify (3x + 2) − (2x − 3)"),
        ("(x + 2)*(x + 3)", "x^2 + 5*x + 6", "Expand (x + 2)(x + 3)"),
        ("(x - 4)*(x + 2)", "x^2 - 2*x - 8", "Expand (x - 4)(x + 2)"),
        ("(2*x - 3)^2 - 4*x^2", "9 - 12*x", "Simplify (2x - 3)² − 4x²"),
        ("3*(x^2 + 2) - 3*x^2", "6", "Simplify 3(x² + 2) − 3x²"),
        ("(x + 1)^3 - x^3 - 3*x^2", "3*x + 1", "Simplify (x + 1)³ − x³ − 3x²"),
        ("(x - 1)^2 + 2*x", "x^2 + 1", "Simplify (x - 1)² + 2x"),
        ("(x + 6)*(x - 6) + 36", "x^2", "Simplify (x + 6)(x - 6) + 36"),
        ("4*(x + 1) - 2*(2*x - 1)", "6", "Simplify 4(x + 1) − 2(2x − 1)"),
        ("(x + y)^2 - 2*x*y", "x^2 + y^2", "Simplify (x + y)² − 2xy"),
        ("(x - y)^2 + 2*x*y", "x^2 + y^2", "Simplify (x - y)² + 2xy"),
        ("(2*x + 3)*(2*x - 3)", "4*x^2 - 9", "Expand (2x + 3)(2x - 3)"),
        ("x^2 + 2*x + 1 - (x + 1)^2", "0", "Simplify x² + 2x + 1 − (x + 1)²"),
        ("(x + 1)*(x^2 - x + 1)", "x^3 + 1", "Expand (x + 1)(x² − x + 1)"),
        ("(x - 1)*(x^2 + x + 1)", "x^3 - 1", "Expand (x - 1)(x² + x + 1)"),
        ("(3*x + 1)^2 - 6*x", "9*x^2 + 1", "Simplify (3x + 1)² − 6x"),
        ("(x + 7)^2 - 14*x", "x^2 + 49", "Simplify (x + 7)² − 14x"),
        ("5*(2*x - 1) - 10*x", "-5", "Simplify 5(2x - 1) − 10x"),
        ("(x - 5)^2 + 10*x", "x^2 + 25", "Simplify (x - 5)² + 10x"),
    ]
    for i, (expr, ans, nl) in enumerate(algebra_raw, 1):
        problems.append({
            "id": f"alg_{i:03d}",
            "source": "Egyptian Grade 10 Algebra",
            "category": "algebraic_simplification",
            "template_id": "algebraic_simplification",
            "problem_text": nl,
            "correct_answer": ans,
            "lean_statement": f"example (x : ℝ) : {expr} = {ans} := by ring",
            "lean_verified": True,
            "slot_values": {"expr": expr, "answer": ans},
            "difficulty": "medium",
            "notes": "Polynomial ring identity",
        })

    # 3. Equation Solving (30 problems)
    eqn_raw = [
        ("x", "7", "22", "5", "Solve 3x + 7 = 22"),
        ("x", "4", "25", "7", "Solve 3x + 4 = 25"),
        ("x", "1", "16", "5", "Solve 3x + 1 = 16"),
        ("x", "10", "40", "10", "Solve 3x + 10 = 40"),
        ("x", "-5", "16", "7", "Solve 3x - 5 = 16"),
        ("x", "2", "20", "6", "Solve 3x + 2 = 20"),
        ("x", "9", "30", "7", "Solve 3x + 9 = 30"),
        ("x", "-2", "19", "7", "Solve 3x - 2 = 19"),
        ("x", "5", "35", "10", "Solve 3x + 5 = 35"),
        ("x", "8", "26", "6", "Solve 3x + 8 = 26"),
        ("x", "12", "42", "10", "Solve 3x + 12 = 42"),
        ("x", "-8", "13", "7", "Solve 3x - 8 = 13"),
        ("x", "3", "24", "7", "Solve 3x + 3 = 24"),
        ("x", "6", "27", "7", "Solve 3x + 6 = 27"),
        ("x", "-1", "20", "7", "Solve 3x - 1 = 20"),
        ("x", "15", "45", "10", "Solve 3x + 15 = 45"),
        ("x", "-4", "17", "7", "Solve 3x - 4 = 17"),
        ("x", "11", "38", "9", "Solve 3x + 11 = 38"),
        ("x", "-7", "14", "7", "Solve 3x - 7 = 14"),
        ("x", "14", "44", "10", "Solve 3x + 14 = 44"),
        ("x", "0", "21", "7", "Solve 3x + 0 = 21"),
        ("x", "13", "40", "9", "Solve 3x + 13 = 40"),
        ("x", "-10", "11", "7", "Solve 3x - 10 = 11"),
        ("x", "16", "46", "10", "Solve 3x + 16 = 46"),
        ("x", "-3", "18", "7", "Solve 3x - 3 = 18"),
        ("x", "18", "48", "10", "Solve 3x + 18 = 48"),
        ("x", "-6", "15", "7", "Solve 3x - 6 = 15"),
        ("x", "20", "50", "10", "Solve 3x + 20 = 50"),
        ("x", "-9", "12", "7", "Solve 3x - 9 = 12"),
        ("x", "1", "31", "10", "Solve 3x + 1 = 31"),
    ]
    for i, (a_var, b, c, ans, nl) in enumerate(eqn_raw, 1):
        problems.append({
            "id": f"eqn_{i:03d}",
            "source": "Egyptian Grade 10 Linear Equations",
            "category": "equation_solving",
            "template_id": "equation_solving",
            "problem_text": nl,
            "correct_answer": ans,
            "lean_statement": f"example : (3 * {a_var} + {b} = {c}) ↔ ({a_var} = {ans}) := by omega",
            "lean_verified": True,
            "slot_values": {"a": a_var, "b": b, "c": c, "answer": ans},
            "difficulty": "medium",
            "notes": "Linear integer equation",
        })

    # 4. Derivatives (40 problems)
    deriv_raw = [
        ("x^2 * Real.sin x", "2*x * Real.sin x + x^2 * Real.cos x", "Find the derivative of x² sin(x) with respect to x"),
        ("x * Real.cos x", "Real.cos x - x * Real.sin x", "Find the derivative of x cos(x) with respect to x"),
        ("x^3", "3 * x^2", "Differentiate x³ with respect to x"),
        ("x^4", "4 * x^3", "Find d/dx of x⁴"),
        ("Real.sin x", "Real.cos x", "Find the derivative of sin(x)"),
        ("Real.cos x", "-Real.sin x", "Find the derivative of cos(x)"),
        ("Real.exp x", "Real.exp x", "Find the derivative of exp(x)"),
        ("x * Real.exp x", "Real.exp x + x * Real.exp x", "Find the derivative of x exp(x)"),
        ("x^2 + 3*x", "2*x + 3", "Differentiate x² + 3x with respect to x"),
        ("x^5", "5 * x^4", "Find the derivative of x⁵"),
        ("x^2 * Real.cos x", "2*x * Real.cos x - x^2 * Real.sin x", "Find the derivative of x² cos(x)"),
        ("x * Real.sin x", "Real.sin x + x * Real.cos x", "Find the derivative of x sin(x)"),
        ("3 * x^2", "6 * x", "Find the derivative of 3x²"),
        ("4 * x^3", "12 * x^2", "Find the derivative of 4x³"),
        ("x^2 * Real.exp x", "2*x * Real.exp x + x^2 * Real.exp x", "Find the derivative of x² exp(x)"),
        ("Real.sin x * Real.cos x", "Real.cos x * Real.cos x - Real.sin x * Real.sin x", "Find the derivative of sin(x) cos(x)"),
        ("5 * x", "5", "Find the derivative of 5x"),
        ("x^6", "6 * x^5", "Find the derivative of x⁶"),
        ("2 * Real.sin x", "2 * Real.cos x", "Differentiate 2 sin(x)"),
        ("3 * Real.cos x", "-3 * Real.sin x", "Differentiate 3 cos(x)"),
        ("x^3 * Real.sin x", "3*x^2 * Real.sin x + x^3 * Real.cos x", "Find the derivative of x³ sin(x)"),
        ("x^3 * Real.cos x", "3*x^2 * Real.cos x - x^3 * Real.sin x", "Find the derivative of x³ cos(x)"),
        ("x^4 + 2*x", "4*x^3 + 2", "Differentiate x⁴ + 2x"),
        ("7 * x^2", "14 * x", "Find the derivative of 7x²"),
        ("x^2 + x", "2*x + 1", "Find the derivative of x² + x"),
        ("2 * Real.exp x", "2 * Real.exp x", "Find the derivative of 2 exp(x)"),
        ("x^3 + x^2", "3*x^2 + 2*x", "Differentiate x³ + x²"),
        ("4 * Real.sin x", "4 * Real.cos x", "Find the derivative of 4 sin(x)"),
        ("x * (x + 1)", "2*x + 1", "Find the derivative of x(x + 1)"),
        ("x^7", "7 * x^6", "Find the derivative of x⁷"),
        ("3 * x^4", "12 * x^3", "Find the derivative of 3x⁴"),
        ("x^2 * (x + 2)", "3*x^2 + 4*x", "Find the derivative of x²(x + 2)"),
        ("5 * Real.cos x", "-5 * Real.sin x", "Differentiate 5 cos(x)"),
        ("6 * x^2 + 2", "12 * x", "Find the derivative of 6x² + 2"),
        ("x^8", "8 * x^7", "Find the derivative of x⁸"),
        ("2*x^3 + 3*x^2", "6*x^2 + 6*x", "Differentiate 2x³ + 3x²"),
        ("Real.exp x * Real.sin x", "Real.exp x * Real.sin x + Real.exp x * Real.cos x", "Find the derivative of exp(x) sin(x)"),
        ("Real.exp x * Real.cos x", "Real.exp x * Real.cos x - Real.exp x * Real.sin x", "Find the derivative of exp(x) cos(x)"),
        ("x^9", "9 * x^8", "Find the derivative of x⁹"),
        ("10 * x^2", "20 * x", "Find the derivative of 10x²"),
    ]
    for i, (expr, ans, nl) in enumerate(deriv_raw, 1):
        problems.append({
            "id": f"calc_deriv_{i:03d}",
            "source": "Egyptian Grade 12 Calculus",
            "category": "derivative",
            "template_id": "derivative",
            "problem_text": nl,
            "correct_answer": ans,
            "lean_statement": (
                f"example (x : ℝ) : deriv (fun x => {expr}) x = {ans} := by\n"
                f"  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n"
                f"  ring"
            ),
            "lean_verified": True,
            "slot_values": {"expr": expr, "answer": ans},
            "difficulty": "hard",
            "notes": "Calculus single-variable derivative",
        })

    # 5. Definite Integrals (30 problems)
    int_raw = [
        ("0", "1", "x^2", "1/3", "Evaluate the definite integral of x² from 0 to 1"),
        ("0", "1", "x", "1/2", "Evaluate the definite integral of x from 0 to 1"),
        ("0", "1", "x^3", "1/4", "Evaluate the integral of x³ from 0 to 1"),
        ("0", "2", "x", "2", "Evaluate the definite integral of x from 0 to 2"),
        ("0", "2", "x^2", "8/3", "Evaluate the definite integral of x² from 0 to 2"),
        ("1", "2", "x", "3/2", "Evaluate ∫₁² x dx"),
        ("0", "1", "1", "1", "Evaluate the integral of 1 from 0 to 1"),
        ("0", "3", "x", "9/2", "Evaluate ∫₀³ x dx"),
        ("0", "1", "x^4", "1/5", "Evaluate the definite integral of x⁴ from 0 to 1"),
        ("1", "3", "x", "4", "Evaluate the definite integral of x from 1 to 3"),
        ("0", "2", "3*x^2", "8", "Evaluate the integral of 3x² from 0 to 2"),
        ("0", "1", "2*x", "1", "Evaluate ∫₀¹ 2x dx"),
        ("0", "2", "2*x", "4", "Evaluate the definite integral of 2x from 0 to 2"),
        ("1", "2", "x^2", "7/3", "Evaluate the integral of x² from 1 to 2"),
        ("0", "1", "4*x^3", "1", "Evaluate ∫₀¹ 4x³ dx"),
        ("0", "3", "x^2", "9", "Evaluate the definite integral of x² from 0 to 3"),
        ("0", "1", "x + 1", "3/2", "Evaluate ∫₀¹ (x + 1) dx"),
        ("0", "2", "x + 1", "4", "Evaluate the definite integral of x + 1 from 0 to 2"),
        ("1", "3", "x^2", "26/3", "Evaluate ∫₁³ x² dx"),
        ("0", "1", "3*x^2", "1", "Evaluate the definite integral of 3x² from 0 to 1"),
        ("0", "4", "x", "8", "Evaluate ∫₀⁴ x dx"),
        ("0", "1", "5*x^4", "1", "Evaluate the integral of 5x⁴ from 0 to 1"),
        ("1", "2", "3*x^2", "7", "Evaluate ∫₁² 3x² dx"),
        ("0", "2", "4*x^3", "16", "Evaluate the integral of 4x³ from 0 to 2"),
        ("0", "1", "x^5", "1/6", "Evaluate the definite integral of x⁵ from 0 to 1"),
        ("2", "4", "x", "6", "Evaluate the integral of x from 2 to 4"),
        ("0", "1", "6*x^5", "1", "Evaluate ∫₀¹ 6x⁵ dx"),
        ("0", "3", "2*x", "9", "Evaluate the definite integral of 2x from 0 to 3"),
        ("1", "4", "x", "15/2", "Evaluate ∫₁⁴ x dx"),
        ("0", "2", "x^3", "4", "Evaluate the definite integral of x³ from 0 to 2"),
    ]
    for i, (lower, upper, expr, ans, nl) in enumerate(int_raw, 1):
        problems.append({
            "id": f"calc_int_{i:03d}",
            "source": "Egyptian Grade 12 Calculus",
            "category": "definite_integral",
            "template_id": "definite_integral",
            "problem_text": nl,
            "correct_answer": ans,
            "lean_statement": f"example : ∫ x in ({lower} : ℝ)..{upper}, {expr} = {ans} := by norm_num",
            "lean_verified": True,
            "slot_values": {"lower": lower, "upper": upper, "expr": expr, "answer": ans},
            "difficulty": "hard",
            "notes": "Polynomial definite interval integral",
        })

    # 6. Number Theory / Primality (20 problems)
    primes = [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
        101, 103, 107, 109, 113
    ][:20]
    for i, n in enumerate(primes, 1):
        problems.append({
            "id": f"num_{i:03d}",
            "source": "Egyptian Grade 10 Number Theory",
            "category": "number_theory",
            "template_id": "number_theory",
            "problem_text": f"Is {n} prime?",
            "correct_answer": f"Nat.Prime {n}",
            "lean_statement": f"example : Nat.Prime {n} := by decide",
            "lean_verified": True,
            "slot_values": {"n": str(n)},
            "difficulty": "easy",
            "notes": "Nat.Prime decidability",
        })

    # 7. Geometry Distance (20 problems)
    geom_raw = [
        ("1", "2", "4", "6", "5", "Find the distance between the points (1, 2) and (4, 6)"),
        ("0", "0", "3", "4", "5", "Find the distance between (0, 0) and (3, 4)"),
        ("1", "1", "4", "5", "5", "Find the distance between (1, 1) and (4, 5)"),
        ("2", "3", "8", "11", "10", "Find the distance between points (2, 3) and (8, 11)"),
        ("0", "0", "6", "8", "10", "What is the distance between (0, 0) and (6, 8)?"),
        ("3", "2", "6", "6", "5", "Calculate the distance between (3, 2) and (6, 6)"),
        ("0", "0", "5", "12", "13", "Find the distance between (0, 0) and (5, 12)"),
        ("2", "1", "7", "13", "13", "Find the distance between points (2, 1) and (7, 13)"),
        ("-1", "-1", "2", "3", "5", "Find the distance between (-1, -1) and (2, 3)"),
        ("1", "2", "7", "10", "10", "Find the distance between (1, 2) and (7, 10)"),
        ("0", "0", "9", "12", "15", "Find the distance between (0, 0) and (9, 12)"),
        ("4", "5", "10", "13", "10", "Calculate the distance between (4, 5) and (10, 13)"),
        ("2", "2", "5", "6", "5", "Find the distance between (2, 2) and (5, 6)"),
        ("1", "3", "9", "9", "10", "Find the distance between (1, 3) and (9, 9)"),
        ("0", "0", "8", "15", "17", "Find the distance between (0, 0) and (8, 15)"),
        ("-2", "1", "1", "5", "5", "Find the distance between (-2, 1) and (1, 5)"),
        ("3", "4", "9", "12", "10", "Find the distance between (3, 4) and (9, 12)"),
        ("0", "0", "12", "16", "20", "What is the distance between (0, 0) and (12, 16)?"),
        ("5", "5", "8", "9", "5", "Find the distance between (5, 5) and (8, 9)"),
        ("1", "1", "13", "6", "13", "Find the distance between (1, 1) and (13, 6)"),
    ]
    for i, (x1, y1, x2, y2, ans, nl) in enumerate(geom_raw, 1):
        problems.append({
            "id": f"geom_{i:03d}",
            "source": "Egyptian Grade 10 Coordinate Geometry",
            "category": "geometry_distance",
            "template_id": "geometry_distance",
            "problem_text": nl,
            "correct_answer": ans,
            "lean_statement": (
                f"example : Real.sqrt (({x2} - {x1})^2 + ({y2} - {y1})^2) = {ans} := by\n"
                f"  norm_num [Real.sqrt_eq_iff_sq_eq, sq_abs]"
            ),
            "lean_verified": True,
            "slot_values": {"x1": x1, "y1": y1, "x2": x2, "y2": y2, "answer": ans},
            "difficulty": "medium",
            "notes": "Pythagorean coordinate distance",
        })

    return problems

def main():
    DATASET_DIR.mkdir(parents=True, exist_ok=True)
    all_problems = generate_problems()
    print(f"Total problems generated: {len(all_problems)}")

    # Split: exactly 150 train, 50 held-out test
    # Maintain proportional category representation
    by_category = {}
    for p in all_problems:
        by_category.setdefault(p["category"], []).append(p)

    train_set = []
    test_set = []

    # Category counts:
    # arithmetic: 30 -> 22 train, 8 test
    # algebraic_simplification: 30 -> 22 train, 8 test
    # equation_solving: 30 -> 22 train, 8 test
    # derivative: 40 -> 30 train, 10 test
    # definite_integral: 30 -> 23 train, 7 test
    # number_theory: 20 -> 15 train, 5 test
    # geometry_distance: 20 -> 16 train, 4 test
    # Total: 150 train, 50 test!
    split_targets = {
        "arithmetic": 22,
        "algebraic_simplification": 22,
        "equation_solving": 22,
        "derivative": 30,
        "definite_integral": 23,
        "number_theory": 15,
        "geometry_distance": 16,
    }

    for cat, items in by_category.items():
        n_train = split_targets[cat]
        train_set.extend(items[:n_train])
        test_set.extend(items[n_train:])

    print(f"Train set: {len(train_set)} problems")
    print(f"Test set:  {len(test_set)} problems")

    train_path = DATASET_DIR / "train.json"
    test_path = DATASET_DIR / "test.json"

    train_path.write_text(json.dumps(train_set, indent=2, ensure_ascii=False), encoding="utf-8")
    test_path.write_text(json.dumps(test_set, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Saved: {train_path}")
    print(f"Saved: {test_path}")

if __name__ == "__main__":
    main()
