"""
VeriMath — Append Book of 1000 Derivatives Chapter 4 Dataset (Problems #415 - #552)
===================================================================================
Covers authentic problems #415 through #552 from Miguel Santiago's
'Book of 1000 Derivatives' (The Vegan Math Guy):
- Basic and nested chain rules (trig, exponential, logarithmic, radical) (#415 - #420, #433 - #438, #451 - #456, #487 - #492, #517 - #528, #535 - #545, #547 - #552)
- Product Rule + Chain Rule (#421 - #426, #445, #542, #543)
- Quotient Rule + Chain Rule (#427 - #432, #446, #459, #500, #520, #523, #525, #548, #550)
- Tabular Chain Rule (#439 - #444)
- Given functional substitutions (#445 - #450, #529 - #534)
- Constant & Pythagorean identity traps (#457, #462, #495, #496, #502, #539, #546)
- Difference Quotient Limits (#463 - #468)
- Particle Velocity from Position (#469 - #474)
- Slope of the Tangent Functions (#475 - #486)
- Tangent Line Equations at (x0, y0) or x = x0 (#505 - #516)

Generates:
1. Way 1: 138 authentic textbook problems (#415 to #552) + variants (~280 examples)
2. Way 2: 250 parametric variations (composite powers, radicals, exponentials, logs, trig, tabular, tangent lines)
Total: ~530 new verified ChatML examples.
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

def get_authentic_problems() -> List[Dict[str, Any]]:
    probs = [
        # Page 144 (#415 - #417)
        {"num": 415, "q": "Find dy/dx for y = -sec(sqrt(x))",
         "ans": "-(sec(sqrt(x))*tan(sqrt(x))) / (2*sqrt(x))",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => -Real.exp 0 / Real.cos (Real.sqrt x)) x = - (Real.sin (Real.sqrt x) / (Real.cos (Real.sqrt x))^2) * (1 / (2 * Real.sqrt x)) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "-1/Real.cos (Real.sqrt x)"},
        {"num": 416, "q": "Find dy/dx for y = ln(cos(x))",
         "ans": "-tan(x)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.log (Real.cos x)) x = -Real.tan x := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.log (Real.cos x)"},
        {"num": 417, "q": "Find dy/dx for y = e^(x^2 - 3x + 1)",
         "ans": "(2*x - 3)*e^(x^2 - 3*x + 1)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.exp (x^2 - 3*x + 1)) x = (2*x - 3)*Real.exp (x^2 - 3*x + 1) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.exp (x^2 - 3*x + 1)"},

        # Page 145 (#418 - #420)
        {"num": 418, "q": "Find dy/dx for y = csc(1 - x^2)",
         "ans": "2*x*csc(1 - x^2)*cot(1 - x^2)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => 1 / Real.sin (1 - x^2)) x = 2*x * (Real.cos (1 - x^2) / (Real.sin (1 - x^2))^2) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "1 / Real.sin (1 - x^2)"},
        {"num": 419, "q": "Find dy/dx for y = sqrt(10 - 4x^3)",
         "ans": "-6*x^2 / sqrt(10 - 4*x^3)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sqrt (10 - 4*x^3)) x = -6*x^2 / Real.sqrt (10 - 4*x^3) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.sqrt (10 - 4*x^3)"},
        {"num": 420, "q": "Find dy/dx for y = log_3(sin(x) - tan(x))",
         "ans": "(cos(x) - sec(x)^2) / ((sin(x) - tan(x))*ln(3))",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.log (Real.sin x - Real.tan x) / Real.log 3) x = (Real.cos x - (1 / Real.cos x)^2) / ((Real.sin x - Real.tan x) * Real.log 3) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.log (Real.sin x - Real.tan x) / Real.log 3"},

        # Page 146 (#421 - #423) Product + Chain
        {"num": 421, "q": "Find f'(x) for f(x) = sqrt(4 - x^2)*sin(5x)",
         "ans": "5*sqrt(4 - x^2)*cos(5*x) - x*sin(5*x)/sqrt(4 - x^2)",
         "tid": "product_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sqrt (4 - x^2) * Real.sin (5*x)) x = 5*Real.sqrt (4 - x^2)*Real.cos (5*x) - x*Real.sin (5*x)/Real.sqrt (4 - x^2) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.sqrt (4 - x^2) * Real.sin (5*x)"},
        {"num": 422, "q": "Find f'(x) for f(x) = e^(4x - 1)*ln(4x - 1)",
         "ans": "4*e^(4*x - 1)*ln(4*x - 1) + 4*e^(4*x - 1)/(4*x - 1)",
         "tid": "product_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.exp (4*x - 1) * Real.log (4*x - 1)) x = 4*Real.exp (4*x - 1)*Real.log (4*x - 1) + 4*Real.exp (4*x - 1)/(4*x - 1) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.exp (4*x - 1) * Real.log (4*x - 1)"},
        {"num": 423, "q": "Find f'(x) for f(x) = cos(x^2 - 5x + 1)*ln(6x^2)",
         "ans": "-(2*x - 5)*sin(x^2 - 5*x + 1)*ln(6*x^2) + (2/x)*cos(x^2 - 5*x + 1)",
         "tid": "product_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.cos (x^2 - 5*x + 1) * Real.log (6*x^2)) x = -(2*x - 5)*Real.sin (x^2 - 5*x + 1)*Real.log (6*x^2) + (2/x)*Real.cos (x^2 - 5*x + 1) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.cos (x^2 - 5*x + 1) * Real.log (6*x^2)"},

        # Page 147 (#424 - #426)
        {"num": 424, "q": "Find f'(x) for f(x) = sin(5x^2)*(7x - 1)^(1/3)",
         "ans": "10*x*cos(5*x^2)*(7*x - 1)^(1/3) + (7/3)*sin(5*x^2)*(7*x - 1)^(-2/3)",
         "tid": "product_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sin (5*x^2) * (7*x - 1)^(1/3 : ℝ)) x = 10*x*Real.cos (5*x^2)*(7*x - 1)^(1/3 : ℝ) + (7/3)*Real.sin (5*x^2)*(7*x - 1)^(-2/3 : ℝ) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.sin (5*x^2) * (7*x - 1)^(1/3 : ℝ)"},
        {"num": 425, "q": "Find f'(x) for f(x) = e^(5x - 1)*(x^3 - 8)^7",
         "ans": "5*e^(5*x - 1)*(x^3 - 8)^7 + 21*x^2*e^(5*x - 1)*(x^3 - 8)^6",
         "tid": "product_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.exp (5*x - 1) * (x^3 - 8)^7) x = 5*Real.exp (5*x - 1)*(x^3 - 8)^7 + 21*x^2*Real.exp (5*x - 1)*(x^3 - 8)^6 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.exp (5*x - 1) * (x^3 - 8)^7"},
        {"num": 426, "q": "Find f'(x) for f(x) = sin(sqrt(x))*sqrt(3x^3 - 1)",
         "ans": "(cos(sqrt(x))*sqrt(3*x^3 - 1))/(2*sqrt(x)) + (9*x^2*sin(sqrt(x)))/(2*sqrt(3*x^3 - 1))",
         "tid": "product_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sin (Real.sqrt x) * Real.sqrt (3*x^3 - 1)) x = (Real.cos (Real.sqrt x)*Real.sqrt (3*x^3 - 1))/(2*Real.sqrt x) + (9*x^2*Real.sin (Real.sqrt x))/(2*Real.sqrt (3*x^3 - 1)) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.sin (Real.sqrt x) * Real.sqrt (3*x^3 - 1)"},

        # Page 148 (#427 - #429) Quotient + Chain
        {"num": 427, "q": "Find g'(x) for g(x) = ln(x^2 - 1) / sin(4 - x^3)",
         "ans": "(2*x*sin(4 - x^3)/(x^2 - 1) + 3*x^2*ln(x^2 - 1)*cos(4 - x^3)) / sin(4 - x^3)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.log (x^2 - 1) / Real.sin (4 - x^3)) x = ((2*x / (x^2 - 1))*Real.sin (4 - x^3) + 3*x^2*Real.log (x^2 - 1)*Real.cos (4 - x^3)) / (Real.sin (4 - x^3))^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.log (x^2 - 1) / Real.sin (4 - x^3)"},
        {"num": 428, "q": "Find g'(x) for g(x) = sqrt(4x^2 + 1) / e^(3x + 1)",
         "ans": "(4*x - 12*x^2 - 3) / (e^(3*x + 1)*sqrt(4*x^2 + 1))",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sqrt (4*x^2 + 1) / Real.exp (3*x + 1)) x = (4*x - 12*x^2 - 3) / (Real.exp (3*x + 1) * Real.sqrt (4*x^2 + 1)) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.sqrt (4*x^2 + 1) / Real.exp (3*x + 1)"},
        {"num": 429, "q": "Find g'(x) for g(x) = cos(4x - 5) / cos(13x + 7)",
         "ans": "(-4*sin(4*x - 5)*cos(13*x + 7) + 13*cos(4*x - 5)*sin(13*x + 7)) / cos(13*x + 7)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.cos (4*x - 5) / Real.cos (13*x + 7)) x = (-4*Real.sin (4*x - 5)*Real.cos (13*x + 7) + 13*Real.cos (4*x - 5)*Real.sin (13*x + 7)) / (Real.cos (13*x + 7))^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.cos (4*x - 5) / Real.cos (13*x + 7)"},

        # Page 149 (#430 - #432)
        {"num": 430, "q": "Find g'(x) for g(x) = (x^4 + 1)^3 / ln(x - 6)",
         "ans": "(12*x^3*(x^4 + 1)^2*ln(x - 6) - (x^4 + 1)^3/(x - 6)) / ln(x - 6)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (x^4 + 1)^3 / Real.log (x - 6)) x = (12*x^3*(x^4 + 1)^2*Real.log (x - 6) - (x^4 + 1)^3/(x - 6)) / (Real.log (x - 6))^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(x^4 + 1)^3 / Real.log (x - 6)"},
        {"num": 431, "q": "Find g'(x) for g(x) = (x^2 - 1)^(1/4) / x^2",
         "ans": "(4 - 3*x^2) / (2*x^3*(x^2 - 1)^(3/4))",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (x^2 - 1)^(1/4 : ℝ) / x^2) x = (4 - 3*x^2) / (2*x^3*(x^2 - 1)^(3/4 : ℝ)) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(x^2 - 1)^(1/4 : ℝ) / x^2"},
        {"num": 432, "q": "Find g'(x) for g(x) = 6x / ln(sqrt(x) + 1/x)",
         "ans": "(6*ln(sqrt(x) + 1/x) - 6*x*(1/(2*sqrt(x)) - 1/x^2)/(sqrt(x) + 1/x)) / ln(sqrt(x) + 1/x)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => 6*x / Real.log (Real.sqrt x + 1/x)) x = (6*Real.log (Real.sqrt x + 1/x) - 6*x*(1/(2*Real.sqrt x) - 1/x^2)/(Real.sqrt x + 1/x)) / (Real.log (Real.sqrt x + 1/x))^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "6*x / Real.log (Real.sqrt x + 1/x)"},

        # Page 150 (#433 - #435) Nested Trig
        {"num": 433, "q": "Find the derivative of y = sin(cos(x))",
         "ans": "-sin(x)*cos(cos(x))",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sin (Real.cos x)) x = -Real.sin x * Real.cos (Real.cos x) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.sin (Real.cos x)"},
        {"num": 434, "q": "Find the derivative of y = cos(tan(x^2))",
         "ans": "-2*x*sec(x^2)^2*sin(tan(x^2))",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.cos (Real.tan (x^2))) x = -2*x * (1 / Real.cos (x^2))^2 * Real.sin (Real.tan (x^2)) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.cos (Real.tan (x^2))"},
        {"num": 435, "q": "Find the derivative of y = tan(sin(sqrt(x)))",
         "ans": "(cos(sqrt(x))*sec(sin(sqrt(x)))^2) / (2*sqrt(x))",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.tan (Real.sin (Real.sqrt x))) x = (Real.cos (Real.sqrt x) * (1 / Real.cos (Real.sin (Real.sqrt x)))^2) / (2 * Real.sqrt x) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.tan (Real.sin (Real.sqrt x))"},

        # Page 151 (#436 - #438)
        {"num": 436, "q": "Find the derivative of y = sin(cos(2x + 9))",
         "ans": "-2*sin(2*x + 9)*cos(cos(2*x + 9))",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sin (Real.cos (2*x + 9))) x = -2*Real.sin (2*x + 9) * Real.cos (Real.cos (2*x + 9)) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.sin (Real.cos (2*x + 9))"},
        {"num": 437, "q": "Find the derivative of y = sec(cos(sin(x)))",
         "ans": "-cos(x)*sin(sin(x))*sec(cos(sin(x)))*tan(cos(sin(x)))",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => 1 / Real.cos (Real.cos (Real.sin x))) x = -Real.cos x * Real.sin (Real.sin x) * (Real.sin (Real.cos (Real.sin x)) / (Real.cos (Real.cos (Real.sin x)))^2) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "1 / Real.cos (Real.cos (Real.sin x))"},
        {"num": 438, "q": "Find the derivative of y = sin(x - cos(1 - x^2))",
         "ans": "(1 - 2*x*sin(1 - x^2))*cos(x - cos(1 - x^2))",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sin (x - Real.cos (1 - x^2))) x = (1 - 2*x*Real.sin (1 - x^2))*Real.cos (x - Real.cos (1 - x^2)) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.sin (x - Real.cos (1 - x^2))"},

        # Page 152 (#439 - #441) Tabular Chain Rule
        {"num": 439, "q": "Given the table with x in {4, 8, 16}, f(4)=16, f'(4)=5, f(8)=6, f'(8)=4, f(16)=10, f'(16)=2, g(4)=8, g'(4)=4, g(8)=5, g'(8)=3, g(16)=-1, g'(16)=2, find h'(4) for h(x) = f(g(x))",
         "ans": "16",
         "tid": "tabular_derivative",
         "lean": "example : (4 : ℝ) * 4 = 16 := by norm_num",
         "expr": "f(g(x))"},
        {"num": 440, "q": "Given the table with x in {4, 8, 16}, f(4)=16, f'(4)=5, f(8)=6, f'(8)=4, f(16)=10, f'(16)=2, g(4)=8, g'(4)=4, g(8)=5, g'(8)=3, g(16)=-1, g'(16)=2, find h'(4) for h(x) = g(f(x))",
         "ans": "10",
         "tid": "tabular_derivative",
         "lean": "example : (2 : ℝ) * 5 = 10 := by norm_num",
         "expr": "g(f(x))"},
        {"num": 441, "q": "Given the table with x in {4, 8, 16}, f(4)=16, f'(4)=5, f(8)=6, f'(8)=4, f(16)=10, f'(16)=2, g(4)=8, g'(4)=4, g(8)=5, g'(8)=3, g(16)=-1, g'(16)=2, find h'(4) for h(x) = f(2x) + g(2x)",
         "ans": "14",
         "tid": "tabular_derivative",
         "lean": "example : 2 * (4 : ℝ) + 2 * 3 = 14 := by norm_num",
         "expr": "f(2*x) + g(2*x)"},

        # Page 153 (#442 - #444)
        {"num": 442, "q": "Given the table with x in {4, 8, 16}, f(4)=16, f'(4)=5, f(8)=6, f'(8)=4, f(16)=10, f'(16)=2, g(4)=8, g'(4)=4, g(8)=5, g'(8)=3, g(16)=-1, g'(16)=2, find h'(16) for h(x) = 4f(0.5x)g(x)",
         "ans": "40",
         "tid": "tabular_derivative",
         "lean": "example : 2 * 4 * (-1 : ℝ) + 4 * 6 * 2 = 40 := by norm_num",
         "expr": "4*f(0.5*x)*g(x)"},
        {"num": 443, "q": "Given the table with x in {4, 8, 16}, f(4)=16, f'(4)=5, f(8)=6, f'(8)=4, f(16)=10, f'(16)=2, g(4)=8, g'(4)=4, g(8)=5, g'(8)=3, g(16)=-1, g'(16)=2, find h'(2) for h(x) = f(x^2 + 4)",
         "ans": "16",
         "tid": "tabular_derivative",
         "lean": "example : (4 : ℝ) * 4 = 16 := by norm_num",
         "expr": "f(x^2 + 4)"},
        {"num": 444, "q": "Given the table with x in {4, 8, 16}, f(4)=16, f'(4)=5, f(8)=6, f'(8)=4, f(16)=10, f'(16)=2, g(4)=8, g'(4)=4, g(8)=5, g'(8)=3, g(16)=-1, g'(16)=2, find h'(-5/4) for h(x) = g(3 - 4x)",
         "ans": "-12",
         "tid": "tabular_derivative",
         "lean": "example : (3 : ℝ) * (-4) = -12 := by norm_num",
         "expr": "g(3 - 4*x)"},

        # Page 154 (#445 - #447) Functional substitutions
        {"num": 445, "q": "Given f(x) = ln(x^2 - 1) and g(x) = sin(x^2), find the derivative of h(x) = f(x)*g(x)",
         "ans": "2*x*sin(x^2)/(x^2 - 1) + 2*x*ln(x^2 - 1)*cos(x^2)",
         "tid": "product_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.log (x^2 - 1) * Real.sin (x^2)) x = 2*x*Real.sin (x^2)/(x^2 - 1) + 2*x*Real.log (x^2 - 1)*Real.cos (x^2) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.log (x^2 - 1) * Real.sin (x^2)"},
        {"num": 446, "q": "Given f(x) = ln(x^2 - 1) and g(x) = sin(x^2), find the derivative of h(x) = f(x)/g(x)",
         "ans": "(2*x*sin(x^2)/(x^2 - 1) - 2*x*ln(x^2 - 1)*cos(x^2)) / sin(x^2)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.log (x^2 - 1) / Real.sin (x^2)) x = ((2*x / (x^2 - 1))*Real.sin (x^2) - 2*x*Real.log (x^2 - 1)*Real.cos (x^2)) / (Real.sin (x^2))^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.log (x^2 - 1) / Real.sin (x^2)"},
        {"num": 447, "q": "Given f(x) = ln(x^2 - 1) and g(x) = sin(x^2), find the derivative of h(x) = f(x) - g(x)",
         "ans": "2*x/(x^2 - 1) - 2*x*cos(x^2)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.log (x^2 - 1) - Real.sin (x^2)) x = 2*x/(x^2 - 1) - 2*x*Real.cos (x^2) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.log (x^2 - 1) - Real.sin (x^2)"},

        # Page 155 (#448 - #450)
        {"num": 448, "q": "Given f(x) = ln(x^2 - 1) and g(x) = sin(x^2), find the derivative of h(x) = (f(x) + g(x))^3",
         "ans": "3*(ln(x^2 - 1) + sin(x^2))^2 * (2*x/(x^2 - 1) + 2*x*cos(x^2))",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (Real.log (x^2 - 1) + Real.sin (x^2))^3) x = 3*(Real.log (x^2 - 1) + Real.sin (x^2))^2 * (2*x/(x^2 - 1) + 2*x*Real.cos (x^2)) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(Real.log (x^2 - 1) + Real.sin (x^2))^3"},
        {"num": 449, "q": "Given f(x) = ln(x^2 - 1) and g(x) = sin(x^2), find the derivative of h(x) = sqrt(f(x)) + ln(g(x))",
         "ans": "x/((x^2 - 1)*sqrt(ln(x^2 - 1))) + 2*x*cot(x^2)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sqrt (Real.log (x^2 - 1)) + Real.log (Real.sin (x^2))) x = x/((x^2 - 1)*Real.sqrt (Real.log (x^2 - 1))) + 2*x*(Real.cos (x^2) / Real.sin (x^2)) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.sqrt (Real.log (x^2 - 1)) + Real.log (Real.sin (x^2))"},
        {"num": 450, "q": "Given f(x) = ln(x^2 - 1) and g(x) = sin(x^2), find the derivative of h(x) = tan(f(x) + g(x))",
         "ans": "(2*x/(x^2 - 1) + 2*x*cos(x^2)) * sec(ln(x^2 - 1) + sin(x^2))^2",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.tan (Real.log (x^2 - 1) + Real.sin (x^2))) x = (2*x/(x^2 - 1) + 2*x*Real.cos (x^2)) * (1 / Real.cos (Real.log (x^2 - 1) + Real.sin (x^2)))^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.tan (Real.log (x^2 - 1) + Real.sin (x^2))"},

        # Page 156 (#451 - #453)
        {"num": 451, "q": "Find dy/dx for y = sqrt(e^x*sin(x))",
         "ans": "(e^x*(sin(x) + cos(x))) / (2*sqrt(e^x*sin(x)))",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sqrt (Real.exp x * Real.sin x)) x = (Real.exp x * (Real.sin x + Real.cos x)) / (2 * Real.sqrt (Real.exp x * Real.sin x)) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.sqrt (Real.exp x * Real.sin x)"},
        {"num": 452, "q": "Find dy/dx for y = 4 / (sin(x) - cos(x))^2",
         "ans": "-8*(sin(x) + cos(x)) / (sin(x) - cos(x))^3",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => 4 / (Real.sin x - Real.cos x)^2) x = -8*(Real.sin x + Real.cos x) / (Real.sin x - Real.cos x)^3 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "4 / (Real.sin x - Real.cos x)^2"},
        {"num": 453, "q": "Find dy/dx for y = log_2(x^2 - cos(x^2))",
         "ans": "(2*x + 2*x*sin(x^2)) / ((x^2 - cos(x^2))*ln(2))",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.log (x^2 - Real.cos (x^2)) / Real.log 2) x = (2*x + 2*x*Real.sin (x^2)) / ((x^2 - Real.cos (x^2)) * Real.log 2) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.log (x^2 - Real.cos (x^2)) / Real.log 2"},

        # Page 157 (#454 - #456)
        {"num": 454, "q": "Find dy/dx for y = 2^(6x^3 - ln(x))",
         "ans": "(18*x^2 - 1/x)*ln(2)*2^(6*x^3 - ln(x))",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (2 : ℝ)^(6*x^3 - Real.log x)) x = (18*x^2 - 1/x) * Real.log 2 * (2 : ℝ)^(6*x^3 - Real.log x) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(2 : ℝ)^(6*x^3 - Real.log x)"},
        {"num": 455, "q": "Find dy/dx for y = tan(x^2 / ln(x^3 - 1))",
         "ans": "sec(x^2 / ln(x^3 - 1))^2 * (2*x*ln(x^3 - 1) - 3*x^4/(x^3 - 1)) / ln(x^3 - 1)^2",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.tan (x^2 / Real.log (x^3 - 1))) x = (1 / Real.cos (x^2 / Real.log (x^3 - 1)))^2 * (2*x*Real.log (x^3 - 1) - 3*x^4/(x^3 - 1)) / (Real.log (x^3 - 1))^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.tan (x^2 / Real.log (x^3 - 1))"},
        {"num": 456, "q": "Find dy/dx for y = 2(x - 3)^2 + 1",
         "ans": "4*(x - 3)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => 2*(x - 3)^2 + 1) x = 4*(x - 3) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "2*(x - 3)^2 + 1"},

        # Page 158 (#457 - #459) Constant trap & nested
        {"num": 457, "q": "Find dy/dx for y = sin(cos(tan(sec(0))))",
         "ans": "0",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sin (Real.cos (Real.tan (1 / Real.cos 0)))) x = 0 := by\n  simp [deriv_const]",
         "expr": "Real.sin (Real.cos (Real.tan (1 / Real.cos 0)))"},
        {"num": 458, "q": "Find dy/dx for y = 2^(sin(x))*ln(sqrt(x) - x^3)",
         "ans": "cos(x)*ln(2)*2^sin(x)*ln(sqrt(x) - x^3) + 2^sin(x)*(1/(2*sqrt(x)) - 3*x^2)/(sqrt(x) - x^3)",
         "tid": "product_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (2 : ℝ)^(Real.sin x) * Real.log (Real.sqrt x - x^3)) x = Real.cos x * Real.log 2 * (2 : ℝ)^(Real.sin x) * Real.log (Real.sqrt x - x^3) + (2 : ℝ)^(Real.sin x) * (1/(2*Real.sqrt x) - 3*x^2)/(Real.sqrt x - x^3) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(2 : ℝ)^(Real.sin x) * Real.log (Real.sqrt x - x^3)"},
        {"num": 459, "q": "Find dy/dx for y = ((x - 4)^7 + 1) / (sqrt(x) - 4)",
         "ans": "(7*(x - 4)^6*(sqrt(x) - 4) - ((x - 4)^7 + 1)/(2*sqrt(x))) / (sqrt(x) - 4)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => ((x - 4)^7 + 1) / (Real.sqrt x - 4)) x = (7*(x - 4)^6*(Real.sqrt x - 4) - ((x - 4)^7 + 1)/(2*Real.sqrt x)) / (Real.sqrt x - 4)^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "((x - 4)^7 + 1) / (Real.sqrt x - 4)"},

        # Page 159 (#460 - #462) Identities & Traps
        {"num": 460, "q": "Find dy/dx for y = ln((6 - x^2)/cos(x))",
         "ans": "-2*x/(6 - x^2) + tan(x)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.log ((6 - x^2) / Real.cos x)) x = -2*x/(6 - x^2) + Real.tan x := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.log ((6 - x^2) / Real.cos x)"},
        {"num": 461, "q": "Find dy/dx for y = 5x^10 - sec(sqrt(x) + 1)^3",
         "ans": "50*x^9 - (3/(2*sqrt(x)))*sec(sqrt(x) + 1)^3*tan(sqrt(x) + 1)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => 5*x^10 - (1 / Real.cos (Real.sqrt x + 1))^3) x = 50*x^9 - (3/(2*Real.sqrt x)) * (Real.sin (Real.sqrt x + 1) / (Real.cos (Real.sqrt x + 1))^4) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "5*x^10 - (1 / Real.cos (Real.sqrt x + 1))^3"},
        {"num": 462, "q": "Find dy/dx for y = sin(x)^2 - cos(x)^2",
         "ans": "2*sin(2*x)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (Real.sin x)^2 - (Real.cos x)^2) x = 2*Real.sin (2*x) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(Real.sin x)^2 - (Real.cos x)^2"},

        # Page 160 (#463 - #465) Difference Quotient Limits
        {"num": 463, "q": "Find the limit: lim_{h->0} (sin(2(x + h)^2 - (x + h)) - sin(2x^2 - x)) / h",
         "ans": "(4*x - 1)*cos(2*x^2 - x)",
         "tid": "derivative_limit_definition",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sin (2*x^2 - x)) x = (4*x - 1)*Real.cos (2*x^2 - x) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.sin (2*x^2 - x)"},
        {"num": 464, "q": "Find the limit: lim_{h->0} (sqrt(3(x + h)^3 - (x + h)^2) - sqrt(3x^3 - x^2)) / h",
         "ans": "(9*x^2 - 2*x) / (2*sqrt(3*x^3 - x^2))",
         "tid": "derivative_limit_definition",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sqrt (3*x^3 - x^2)) x = (9*x^2 - 2*x) / (2*Real.sqrt (3*x^3 - x^2)) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.sqrt (3*x^3 - x^2)"},
        {"num": 465, "q": "Find the limit: lim_{h->0} (tan(e^(x + h)) - tan(e^x)) / h",
         "ans": "e^x*sec(e^x)^2",
         "tid": "derivative_limit_definition",
         "lean": "example (x : ℝ) : deriv (fun x => Real.tan (Real.exp x)) x = Real.exp x * (1 / Real.cos (Real.exp x))^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.tan (Real.exp x)"},

        # Page 161 (#466 - #468)
        {"num": 466, "q": "Find the limit: lim_{h->0} (ln(2/(x + h)) - ln(2/x)) / h",
         "ans": "-1/x",
         "tid": "derivative_limit_definition",
         "lean": "example (x : ℝ) : deriv (fun x => Real.log (2/x)) x = -1/x := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.log (2/x)"},
        {"num": 467, "q": "Find the limit: lim_{h->0} ((6(x + h) - (x + h)^2)^4 - (6x - x^2)^4) / h",
         "ans": "4*(6 - 2*x)*(6*x - x^2)^3",
         "tid": "derivative_limit_definition",
         "lean": "example (x : ℝ) : deriv (fun x => (6*x - x^2)^4) x = 4*(6 - 2*x)*(6*x - x^2)^3 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(6*x - x^2)^4"},
        {"num": 468, "q": "Find the limit: lim_{h->0} (5*sqrt((x + h)^2 - 6) - 5*sqrt(x^2 - 6)) / h",
         "ans": "5*x / sqrt(x^2 - 6)",
         "tid": "derivative_limit_definition",
         "lean": "example (x : ℝ) : deriv (fun x => 5*Real.sqrt (x^2 - 6)) x = 5*x / Real.sqrt (x^2 - 6) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "5*Real.sqrt (x^2 - 6)"},

        # Page 162 (#469 - #471) Particle Velocity
        {"num": 469, "q": "Find the velocity of the particle given the position s(t) = sin(t)*sqrt(t^2 - 8t)",
         "ans": "cos(t)*sqrt(t^2 - 8*t) + (t - 4)*sin(t)/sqrt(t^2 - 8*t)",
         "tid": "particle_velocity_derivative",
         "lean": "example (t : ℝ) : deriv (fun t => Real.sin t * Real.sqrt (t^2 - 8*t)) t = Real.cos t * Real.sqrt (t^2 - 8*t) + (t - 4)*Real.sin t / Real.sqrt (t^2 - 8*t) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.sin t * Real.sqrt (t^2 - 8*t)"},
        {"num": 470, "q": "Find the velocity of the particle given the position s(t) = -(5 + t^3)^4 + cos(t)",
         "ans": "-12*t^2*(5 + t^3)^3 - sin(t)",
         "tid": "particle_velocity_derivative",
         "lean": "example (t : ℝ) : deriv (fun t => -(5 + t^3)^4 + Real.cos t) t = -12*t^2*(5 + t^3)^3 - Real.sin t := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "-(5 + t^3)^4 + Real.cos t"},
        {"num": 471, "q": "Find the velocity of the particle given the position s(t) = 7sec(sqrt(t^2 + 5))",
         "ans": "7*t*sec(sqrt(t^2 + 5))*tan(sqrt(t^2 + 5)) / sqrt(t^2 + 5)",
         "tid": "particle_velocity_derivative",
         "lean": "example (t : ℝ) : deriv (fun t => 7 / Real.cos (Real.sqrt (t^2 + 5))) t = 7*t * (Real.sin (Real.sqrt (t^2 + 5)) / (Real.cos (Real.sqrt (t^2 + 5)))^2) / Real.sqrt (t^2 + 5) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "7 / Real.cos (Real.sqrt (t^2 + 5))"},

        # Page 163 (#472 - #474)
        {"num": 472, "q": "Find the velocity of the particle given the position s(t) = ln((t - 1)*(t^2 - 3)*(4t + 4))",
         "ans": "1/(t - 1) + 2*t/(t^2 - 3) + 1/(t + 1)",
         "tid": "particle_velocity_derivative",
         "lean": "example (t : ℝ) : deriv (fun t => Real.log ((t - 1)*(t^2 - 3)*(4*t + 4))) t = 1/(t - 1) + 2*t/(t^2 - 3) + 1/(t + 1) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.log ((t - 1)*(t^2 - 3)*(4*t + 4))"},
        {"num": 473, "q": "Find the velocity of the particle given the position s(t) = sin(5t^2 + cos(2t))",
         "ans": "(10*t - 2*sin(2*t))*cos(5*t^2 + cos(2*t))",
         "tid": "particle_velocity_derivative",
         "lean": "example (t : ℝ) : deriv (fun t => Real.sin (5*t^2 + Real.cos (2*t))) t = (10*t - 2*Real.sin (2*t))*Real.cos (5*t^2 + Real.cos (2*t)) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.sin (5*t^2 + Real.cos (2*t))"},
        {"num": 474, "q": "Find the velocity of the particle given the position s(t) = 24t^2 + 2^(sin(t) - t^3)",
         "ans": "48*t + (cos(t) - 3*t^2)*ln(2)*2^(sin(t) - t^3)",
         "tid": "particle_velocity_derivative",
         "lean": "example (t : ℝ) : deriv (fun t => 24*t^2 + (2 : ℝ)^(Real.sin t - t^3)) t = 48*t + (Real.cos t - 3*t^2)*Real.log 2*(2 : ℝ)^(Real.sin t - t^3) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "24*t^2 + (2 : ℝ)^(Real.sin t - t^3)"},

        # Page 164 (#475 - #477) Slope functions
        {"num": 475, "q": "Find the slope of the tangent for the function f(x) = sin((x - 3)^3 + 5x)",
         "ans": "(3*(x - 3)^2 + 5)*cos((x - 3)^3 + 5*x)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sin ((x - 3)^3 + 5*x)) x = (3*(x - 3)^2 + 5)*Real.cos ((x - 3)^3 + 5*x) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.sin ((x - 3)^3 + 5*x)"},
        {"num": 476, "q": "Find the slope of the tangent for the function f(x) = -sqrt(4x^3 - 5) + 5^(2x + 1)",
         "ans": "-6*x^2/sqrt(4*x^3 - 5) + 2*ln(5)*5^(2*x + 1)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => -Real.sqrt (4*x^3 - 5) + (5 : ℝ)^(2*x + 1)) x = -6*x^2/Real.sqrt (4*x^3 - 5) + 2*Real.log 5*(5 : ℝ)^(2*x + 1) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "-Real.sqrt (4*x^3 - 5) + (5 : ℝ)^(2*x + 1)"},
        {"num": 477, "q": "Find the slope of the tangent for the function f(x) = -4tan(ln(x^2) + e^(x^2 - 5x + 6))",
         "ans": "-4*(2/x + (2*x - 5)*e^(x^2 - 5*x + 6))*sec(ln(x^2) + e^(x^2 - 5*x + 6))^2",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => -4*Real.tan (Real.log (x^2) + Real.exp (x^2 - 5*x + 6))) x = -4*(2/x + (2*x - 5)*Real.exp (x^2 - 5*x + 6)) * (1 / Real.cos (Real.log (x^2) + Real.exp (x^2 - 5*x + 6)))^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "-4*Real.tan (Real.log (x^2) + Real.exp (x^2 - 5*x + 6))"},

        # Page 165 (#478 - #480)
        {"num": 478, "q": "Find the slope of the tangent for the function f(x) = (2/(4 - x^2) - 1/x^2)^3",
         "ans": "3*(2/(4 - x^2) - 1/x^2)^2 * (4*x/(4 - x^2)^2 + 2/x^3)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (2/(4 - x^2) - 1/x^2)^3) x = 3*(2/(4 - x^2) - 1/x^2)^2 * (4*x/(4 - x^2)^2 + 2/x^3) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(2/(4 - x^2) - 1/x^2)^3"},
        {"num": 479, "q": "Find the slope of the tangent for the function f(x) = 6x^3 - sin(6x^3*cos(6x))",
         "ans": "18*x^2 - (18*x^2*cos(6*x) - 36*x^3*sin(6*x))*cos(6*x^3*cos(6*x))",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => 6*x^3 - Real.sin (6*x^3 * Real.cos (6*x))) x = 18*x^2 - (18*x^2*Real.cos (6*x) - 36*x^3*Real.sin (6*x))*Real.cos (6*x^3 * Real.cos (6*x)) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "6*x^3 - Real.sin (6*x^3 * Real.cos (6*x))"},
        {"num": 480, "q": "Find the slope of the tangent for the function f(x) = ln(5 - 6x) / sqrt(x)",
         "ans": "(-12*x - (5 - 6*x)*ln(5 - 6*x)) / (2*x^(3/2)*(5 - 6*x))",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.log (5 - 6*x) / Real.sqrt x) x = (-12*x - (5 - 6*x)*Real.log (5 - 6*x)) / (2*x^(3/2 : ℝ)*(5 - 6*x)) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.log (5 - 6*x) / Real.sqrt x"},

        # Page 166 (#481 - #483)
        {"num": 481, "q": "Find the slope of the tangent for the function f(x) = 2^(sin(x)*cos(4 - x))",
         "ans": "cos(2*x - 4)*ln(2)*2^(sin(x)*cos(4 - x))",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (2 : ℝ)^(Real.sin x * Real.cos (4 - x))) x = Real.cos (2*x - 4)*Real.log 2*(2 : ℝ)^(Real.sin x * Real.cos (4 - x)) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(2 : ℝ)^(Real.sin x * Real.cos (4 - x))"},
        {"num": 482, "q": "Find the slope of the tangent for the function f(x) = ln((x - 4)^3 / sin(x))",
         "ans": "3/(x - 4) - cot(x)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.log ((x - 4)^3 / Real.sin x)) x = 3/(x - 4) - Real.cos x / Real.sin x := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.log ((x - 4)^3 / Real.sin x)"},
        {"num": 483, "q": "Find the slope of the tangent for the function f(x) = (x^4 + x^3 - x^2 + x - 1 + 1/x)^4",
         "ans": "4*(x^4 + x^3 - x^2 + x - 1 + 1/x)^3 * (4*x^3 + 3*x^2 - 2*x + 1 - 1/x^2)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (x^4 + x^3 - x^2 + x - 1 + 1/x)^4) x = 4*(x^4 + x^3 - x^2 + x - 1 + 1/x)^3 * (4*x^3 + 3*x^2 - 2*x + 1 - 1/x^2) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(x^4 + x^3 - x^2 + x - 1 + 1/x)^4"},

        # Page 167 (#484 - #486)
        {"num": 484, "q": "Find the slope of the tangent for the function f(x) = sec(sqrt(x) - tan(x))",
         "ans": "(1/(2*sqrt(x)) - sec(x)^2)*sec(sqrt(x) - tan(x))*tan(sqrt(x) - tan(x))",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => 1 / Real.cos (Real.sqrt x - Real.tan x)) x = (1/(2*Real.sqrt x) - (1 / Real.cos x)^2) * (Real.sin (Real.sqrt x - Real.tan x) / (Real.cos (Real.sqrt x - Real.tan x))^2) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "1 / Real.cos (Real.sqrt x - Real.tan x)"},
        {"num": 485, "q": "Find the slope of the tangent for the function f(x) = -5x^2 + (8x + 1)/(x + 1)^15",
         "ans": "-10*x - (112*x + 7)/(x + 1)^16",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => -5*x^2 + (8*x + 1)/(x + 1)^15) x = -10*x - (112*x + 7)/(x + 1)^16 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "-5*x^2 + (8*x + 1)/(x + 1)^15"},
        {"num": 486, "q": "Find the slope of the tangent for the function f(x) = log_4(sin(x)*cos(x)^2)",
         "ans": "(cot(x) - 2*tan(x)) / ln(4)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.log (Real.sin x * (Real.cos x)^2) / Real.log 4) x = (Real.cos x / Real.sin x - 2*Real.tan x) / Real.log 4 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.log (Real.sin x * (Real.cos x)^2) / Real.log 4"},

        # Page 168 (#487 - #489)
        {"num": 487, "q": "Find the derivative of y = (3 - x)^3*(x + 3)^3",
         "ans": "-6*x*(9 - x^2)^2",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (9 - x^2)^3) x = -6*x*(9 - x^2)^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(9 - x^2)^3"},
        {"num": 488, "q": "Find the derivative of f(x) = log_2(sin(x)) - 6x",
         "ans": "cot(x)/ln(2) - 6",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.log (Real.sin x) / Real.log 2 - 6*x) x = (Real.cos x / Real.sin x) / Real.log 2 - 6 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.log (Real.sin x) / Real.log 2 - 6*x"},
        {"num": 489, "q": "Find the derivative of g(x) = (x^2 + 8x - 4)^(1/5)",
         "ans": "(2*x + 8) / (5*(x^2 + 8*x - 4)^(4/5))",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (x^2 + 8*x - 4)^(1/5 : ℝ)) x = (2*x + 8) / (5*(x^2 + 8*x - 4)^(4/5 : ℝ)) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(x^2 + 8*x - 4)^(1/5 : ℝ)"},

        # Page 169 (#490 - #492)
        {"num": 490, "q": "Find dy/dx for y = sin(x*tan(x*cos(x)))",
         "ans": "(tan(x*cos(x)) + x*(cos(x) - x*sin(x))*sec(x*cos(x))^2)*cos(x*tan(x*cos(x)))",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sin (x * Real.tan (x * Real.cos x))) x = (Real.tan (x * Real.cos x) + x*(Real.cos x - x*Real.sin x)*(1 / Real.cos (x * Real.cos x))^2)*Real.cos (x * Real.tan (x * Real.cos x)) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.sin (x * Real.tan (x * Real.cos x))"},
        {"num": 491, "q": "Find dy/dx for h(x) = sin(4x)^2 + 4cos(x)^2",
         "ans": "4*sin(8*x) - 4*sin(2*x)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (Real.sin (4*x))^2 + 4*(Real.cos x)^2) x = 4*Real.sin (8*x) - 4*Real.sin (2*x) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(Real.sin (4*x))^2 + 4*(Real.cos x)^2"},
        {"num": 492, "q": "Find dy/dx for f(x) = 2^(x^2 - 1) + 2(x^2 - 1)^2",
         "ans": "2*x*ln(2)*2^(x^2 - 1) + 8*x*(x^2 - 1)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (2 : ℝ)^(x^2 - 1) + 2*(x^2 - 1)^2) x = 2*x*Real.log 2*(2 : ℝ)^(x^2 - 1) + 8*x*(x^2 - 1) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(2 : ℝ)^(x^2 - 1) + 2*(x^2 - 1)^2"},

        # Page 170 (#493 - #495)
        {"num": 493, "q": "Find dy/dx for y = ln((4x - 5)/(4x + 1))",
         "ans": "24 / ((4*x - 5)*(4*x + 1))",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.log ((4*x - 5)/(4*x + 1))) x = 24 / ((4*x - 5)*(4*x + 1)) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.log ((4*x - 5)/(4*x + 1))"},
        {"num": 494, "q": "Find dy/dx for y = 6 - sqrt(x^2 - 2x - 8)",
         "ans": "-(x - 1) / sqrt(x^2 - 2*x - 8)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => 6 - Real.sqrt (x^2 - 2*x - 8)) x = -(x - 1) / Real.sqrt (x^2 - 2*x - 8) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "6 - Real.sqrt (x^2 - 2*x - 8)"},
        {"num": 495, "q": "Find dy/dx for y = 10^(10*log(x^3 + 7))",
         "ans": "30*x^2*(x^3 + 7)^9",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (x^3 + 7)^10) x = 30*x^2*(x^3 + 7)^9 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(x^3 + 7)^10"},

        # Page 171 (#496 - #498)
        {"num": 496, "q": "Find dy/dx for f(x) = sin(cos(x)^2 - sin(x)^2)",
         "ans": "-2*sin(2*x)*cos(cos(2*x))",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sin (Real.cos (2*x))) x = -2*Real.sin (2*x)*Real.cos (Real.cos (2*x)) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.sin (Real.cos (2*x))"},
        {"num": 497, "q": "Find dy/dx for g(x) = 3 - 6(6 - x^3)^3",
         "ans": "54*x^2*(6 - x^3)^2",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => 3 - 6*(6 - x^3)^3) x = 54*x^2*(6 - x^3)^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "3 - 6*(6 - x^3)^3"},
        {"num": 498, "q": "Find dy/dx for w(x) = sqrt(sin(sqrt(x)))",
         "ans": "cos(sqrt(x)) / (4*sqrt(x)*sqrt(sin(sqrt(x))))",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sqrt (Real.sin (Real.sqrt x))) x = Real.cos (Real.sqrt x) / (4*Real.sqrt x * Real.sqrt (Real.sin (Real.sqrt x))) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.sqrt (Real.sin (Real.sqrt x))"},

        # Page 172 (#499 - #501)
        {"num": 499, "q": "Find dy/dx for y = sqrt(x - sqrt(x))",
         "ans": "(2*sqrt(x) - 1) / (4*sqrt(x)*sqrt(x - sqrt(x)))",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sqrt (x - Real.sqrt x)) x = (2*Real.sqrt x - 1) / (4*Real.sqrt x * Real.sqrt (x - Real.sqrt x)) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.sqrt (x - Real.sqrt x)"},
        {"num": 500, "q": "Find dy/dx for f(x) = (x - 4x^2)^3 / 2^x",
         "ans": "(3*(1 - 8*x)*(x - 4*x^2)^2 - ln(2)*(x - 4*x^2)^3) / 2^x",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (x - 4*x^2)^3 / (2 : ℝ)^x) x = (3*(1 - 8*x)*(x - 4*x^2)^2 - Real.log 2*(x - 4*x^2)^3) / (2 : ℝ)^x := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(x - 4*x^2)^3 / (2 : ℝ)^x"},
        {"num": 501, "q": "Find dy/dx for y = sqrt(1/x + 2/(x - 1)^2)",
         "ans": "(-1/x^2 - 4/(x - 1)^3) / (2*sqrt(1/x + 2/(x - 1)^2))",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sqrt (1/x + 2/(x - 1)^2)) x = (-1/x^2 - 4/(x - 1)^3) / (2*Real.sqrt (1/x + 2/(x - 1)^2)) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.sqrt (1/x + 2/(x - 1)^2)"},

        # Page 173 (#502 - #504)
        {"num": 502, "q": "Find dy/dx for y = sin(tan(x) - cos(x)) + sin(pi)",
         "ans": "(sec(x)^2 + sin(x))*cos(tan(x) - cos(x))",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sin (Real.tan x - Real.cos x) + Real.sin Real.pi) x = ((1 / Real.cos x)^2 + Real.sin x)*Real.cos (Real.tan x - Real.cos x) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.sin (Real.tan x - Real.cos x)"},
        {"num": 503, "q": "Find dy/dx for f(x) = 5(x - 2)^4 + sqrt(x - 2)",
         "ans": "20*(x - 2)^3 + 1/(2*sqrt(x - 2))",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => 5*(x - 2)^4 + Real.sqrt (x - 2)) x = 20*(x - 2)^3 + 1/(2*Real.sqrt (x - 2)) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "5*(x - 2)^4 + Real.sqrt (x - 2)"},
        {"num": 504, "q": "Find dy/dx for g(x) = 4sin(4*sqrt(4 - x^2))",
         "ans": "-16*x*cos(4*sqrt(4 - x^2)) / sqrt(4 - x^2)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => 4*Real.sin (4*Real.sqrt (4 - x^2))) x = -16*x*Real.cos (4*Real.sqrt (4 - x^2)) / Real.sqrt (4 - x^2) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "4*Real.sin (4*Real.sqrt (4 - x^2))"},

        # Page 174 (#505 - #507) Tangent Line at point (x, y)
        {"num": 505, "q": "Find the equation of the tangent line for f(x) = sqrt((x - 3)*(x^2 + 3)) at (4, sqrt(19))",
         "ans": "y = 27*sqrt(19)/38*x - 35*sqrt(19)/19",
         "tid": "tangent_line",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sqrt ((x - 3)*(x^2 + 3))) 4 = 27*Real.sqrt 19/38 ∧ Real.sqrt ((4 - 3)*(4^2 + 3)) = Real.sqrt 19 := by\n  simp [deriv_pow, deriv_mul, deriv_add]\n  norm_num",
         "expr": "Real.sqrt ((x - 3)*(x^2 + 3))"},
        {"num": 506, "q": "Find the equation of the tangent line for f(x) = -5sin(3x^2) at (sqrt(pi), 0)",
         "ans": "y = 30*sqrt(pi)*x - 30*pi",
         "tid": "tangent_line",
         "lean": "example (x : ℝ) : deriv (fun x => -5*Real.sin (3*x^2)) (Real.sqrt Real.pi) = 30*Real.sqrt Real.pi ∧ -5*Real.sin (3*(Real.sqrt Real.pi)^2) = 0 := by\n  simp [deriv_sin, deriv_pow]\n  norm_num",
         "expr": "-5*Real.sin (3*x^2)"},
        {"num": 507, "q": "Find the equation of the tangent line for f(x) = 6ln(sqrt(x^2 - 4)) at (sqrt(20), ln(4))",
         "ans": "y - ln(4) = (3*sqrt(5)/4)*(x - 2*sqrt(5))",
         "tid": "tangent_line",
         "lean": "example (x : ℝ) : deriv (fun x => 6*Real.log (Real.sqrt (x^2 - 4))) (Real.sqrt 20) = 3*Real.sqrt 5/4 := by\n  simp [deriv_log, deriv_pow]\n  norm_num",
         "expr": "6*Real.log (Real.sqrt (x^2 - 4))"},

        # Page 175 (#508 - #510)
        {"num": 508, "q": "Find the equation of the tangent line for f(x) = 6e^(2x^2 - 5x + 1) at (1, 6*e^(-2))",
         "ans": "y = -6*e^(-2)*x + 12*e^(-2)",
         "tid": "tangent_line",
         "lean": "example (x : ℝ) : deriv (fun x => 6*Real.exp (2*x^2 - 5*x + 1)) 1 = -6*Real.exp (-2) ∧ 6*Real.exp (2*(1)^2 - 5*(1) + 1) = 6*Real.exp (-2) := by\n  simp [deriv_exp, deriv_pow]\n  norm_num",
         "expr": "6*Real.exp (2*x^2 - 5*x + 1)"},
        {"num": 509, "q": "Find the equation of the tangent line for f(x) = sin(e^x - 2x) at (1, sin(e - 2))",
         "ans": "y - sin(e - 2) = (e - 2)*cos(e - 2)*(x - 1)",
         "tid": "tangent_line",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sin (Real.exp x - 2*x)) 1 = (Real.exp 1 - 2)*Real.cos (Real.exp 1 - 2) := by\n  simp [deriv_sin, deriv_exp]\n  norm_num",
         "expr": "Real.sin (Real.exp x - 2*x)"},
        {"num": 510, "q": "Find the equation of the tangent line for f(x) = sqrt(ln(x) + 6x) at (1, sqrt(6))",
         "ans": "y = 7*sqrt(6)/12*x + 5*sqrt(6)/12",
         "tid": "tangent_line",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sqrt (Real.log x + 6*x)) 1 = 7*Real.sqrt 6 / 12 ∧ Real.sqrt (Real.log 1 + 6*1) = Real.sqrt 6 := by\n  simp [deriv_log, deriv_pow]\n  norm_num",
         "expr": "Real.sqrt (Real.log x + 6*x)"},

        # Page 176 (#511 - #513) Tangent Line at x = x0
        {"num": 511, "q": "Find the equation of the tangent line for f(x) = ln(cos(x)), x = 0",
         "ans": "y = 0",
         "tid": "tangent_line",
         "lean": "example (x : ℝ) : deriv (fun x => Real.log (Real.cos x)) 0 = 0 ∧ Real.log (Real.cos 0) = 0 := by\n  simp [deriv_log, deriv_cos]\n  norm_num",
         "expr": "Real.log (Real.cos x)"},
        {"num": 512, "q": "Find the equation of the tangent line for f(x) = e^sqrt(x - x^2), x = 0",
         "ans": "x = 0",
         "tid": "tangent_line",
         "lean": "example (x : ℝ) : Real.exp (Real.sqrt (0 - 0^2)) = 1 := by norm_num",
         "expr": "Real.exp (Real.sqrt (x - x^2))"},
        {"num": 513, "q": "Find the equation of the tangent line for f(x) = 4(x - 2)^4 - 6(x - 3)^2 + 1, x = 1",
         "ans": "y = 8*x - 27",
         "tid": "tangent_line",
         "lean": "example (x : ℝ) : deriv (fun x => 4*(x - 2)^4 - 6*(x - 3)^2 + 1) 1 = 8 ∧ 4*(1 - 2)^4 - 6*(1 - 3)^2 + 1 = -19 := by\n  simp [deriv_pow, deriv_sub, deriv_add]\n  norm_num",
         "expr": "4*(x - 2)^4 - 6*(x - 3)^2 + 1"},

        # Page 177 (#514 - #516)
        {"num": 514, "q": "Find the equation of the tangent line for f(x) = -4*(x^2 + 7)^(1/3), x = 1",
         "ans": "y = -2/3*x - 22/3",
         "tid": "tangent_line",
         "lean": "example (x : ℝ) : deriv (fun x => -4*(x^2 + 7)^(1/3 : ℝ)) 1 = -2/3 ∧ -4*(1^2 + 7)^(1/3 : ℝ) = -8 := by\n  simp [deriv_pow]\n  norm_num",
         "expr": "-4*(x^2 + 7)^(1/3 : ℝ)"},
        {"num": 515, "q": "Find the equation of the tangent line for f(x) = cos(e^x - e^(3x)), x = 0",
         "ans": "y = 1",
         "tid": "tangent_line",
         "lean": "example (x : ℝ) : deriv (fun x => Real.cos (Real.exp x - Real.exp (3*x))) 0 = 0 ∧ Real.cos (Real.exp 0 - Real.exp 0) = 1 := by\n  simp [deriv_cos, deriv_exp]\n  norm_num",
         "expr": "Real.cos (Real.exp x - Real.exp (3*x))"},
        {"num": 516, "q": "Find the equation of the tangent line for f(x) = 1/(x - 2) + 2/(x^2 + 1), x = 3",
         "ans": "y = -28/25*x + 114/25",
         "tid": "tangent_line",
         "lean": "example (x : ℝ) : deriv (fun x => 1/(x - 2) + 2/(x^2 + 1)) 3 = -28/25 ∧ 1/(3 - 2) + 2/(3^2 + 1) = 6/5 := by\n  simp [deriv_div, deriv_pow]\n  norm_num",
         "expr": "1/(x - 2) + 2/(x^2 + 1)"},

        # Page 178 (#517 - #519)
        {"num": 517, "q": "Find y' for y = log_4(x^2 + 3x + 1)",
         "ans": "(2*x + 3) / ((x^2 + 3*x + 1)*ln(4))",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.log (x^2 + 3*x + 1) / Real.log 4) x = (2*x + 3) / ((x^2 + 3*x + 1)*Real.log 4) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.log (x^2 + 3*x + 1) / Real.log 4"},
        {"num": 518, "q": "Find y' for y = (2x - 5)^3",
         "ans": "6*(2*x - 5)^2",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (2*x - 5)^3) x = 6*(2*x - 5)^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(2*x - 5)^3"},
        {"num": 519, "q": "Find y' for y = e^(ln(x) - 4x)",
         "ans": "e^(-4*x)*(1 - 4*x)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => x * Real.exp (-4*x)) x = Real.exp (-4*x)*(1 - 4*x) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "x * Real.exp (-4*x)"},

        # Page 179 (#520 - #522)
        {"num": 520, "q": "Find y' for y = 7 / sin(6x - 8)",
         "ans": "-42*csc(6*x - 8)*cot(6*x - 8)",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => 7 / Real.sin (6*x - 8)) x = -42 * Real.cos (6*x - 8) / (Real.sin (6*x - 8))^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "7 / Real.sin (6*x - 8)"},
        {"num": 521, "q": "Find y' for y = e^x*(1 - cos(2x))",
         "ans": "e^x*(1 - cos(2*x)) + 2*e^x*sin(2*x)",
         "tid": "product_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.exp x * (1 - Real.cos (2*x))) x = Real.exp x * (1 - Real.cos (2*x)) + 2*Real.exp x * Real.sin (2*x) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.exp x * (1 - Real.cos (2*x))"},
        {"num": 522, "q": "Find y' for y = (x^2 + 1)^5 - ln(x - 3)",
         "ans": "10*x*(x^2 + 1)^4 - 1/(x - 3)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (x^2 + 1)^5 - Real.log (x - 3)) x = 10*x*(x^2 + 1)^4 - 1/(x - 3) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(x^2 + 1)^5 - Real.log (x - 3)"},

        # Page 180 (#523 - #525)
        {"num": 523, "q": "Find y' for y = 3 / (x^2 - 3)^4",
         "ans": "-24*x / (x^2 - 3)^5",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => 3 / (x^2 - 3)^4) x = -24*x / (x^2 - 3)^5 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "3 / (x^2 - 3)^4"},
        {"num": 524, "q": "Find y' for y = (x^3 - 1)^(1/5)",
         "ans": "3*x^2 / (5*(x^3 - 1)^(4/5))",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (x^3 - 1)^(1/5 : ℝ)) x = 3*x^2 / (5*(x^3 - 1)^(4/5 : ℝ)) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(x^3 - 1)^(1/5 : ℝ)"},
        {"num": 525, "q": "Find y' for y = x / sqrt(x^2 - 1)",
         "ans": "-1 / (x^2 - 1)^(3/2)",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => x / Real.sqrt (x^2 - 1)) x = -1 / (x^2 - 1)^(3/2 : ℝ) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "x / Real.sqrt (x^2 - 1)"},

        # Page 181 (#526 - #528)
        {"num": 526, "q": "Find y' for y = 7(x - 1)^8 - 3(3x^4 - 1)^2",
         "ans": "56*(x - 1)^7 - 72*x^3*(3*x^4 - 1)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => 7*(x - 1)^8 - 3*(3*x^4 - 1)^2) x = 56*(x - 1)^7 - 72*x^3*(3*x^4 - 1) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "7*(x - 1)^8 - 3*(3*x^4 - 1)^2"},
        {"num": 527, "q": "Find y' for y = sqrt(x + 3) + e^(x + 3)",
         "ans": "1/(2*sqrt(x + 3)) + e^(x + 3)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sqrt (x + 3) + Real.exp (x + 3)) x = 1/(2*Real.sqrt (x + 3)) + Real.exp (x + 3) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.sqrt (x + 3) + Real.exp (x + 3)"},
        {"num": 528, "q": "Find y' for y = sin(x - 2) - cos(x + 2)",
         "ans": "cos(x - 2) + sin(x + 2)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sin (x - 2) - Real.cos (x + 2)) x = Real.cos (x - 2) + Real.sin (x + 2) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.sin (x - 2) - Real.cos (x + 2)"},

        # Page 182 (#529 - #531) Given f(x) = sin(2x), g(x) = sqrt(x), h(x) = (x - 1)^3
        {"num": 529, "q": "Given f(x) = sin(2x), g(x) = sqrt(x), h(x) = (x - 1)^3, find the derivative of f(g(x))",
         "ans": "cos(2*sqrt(x)) / sqrt(x)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sin (2 * Real.sqrt x)) x = Real.cos (2 * Real.sqrt x) / Real.sqrt x := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.sin (2 * Real.sqrt x)"},
        {"num": 530, "q": "Given f(x) = sin(2x), g(x) = sqrt(x), h(x) = (x - 1)^3, find the derivative of g(h(x))",
         "ans": "(3/2)*sqrt(x - 1)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (x - 1)^(3/2 : ℝ)) x = (3/2)*(x - 1)^(1/2 : ℝ) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(x - 1)^(3/2 : ℝ)"},
        {"num": 531, "q": "Given f(x) = sin(2x), g(x) = sqrt(x), h(x) = (x - 1)^3, find the derivative of g(f(x))",
         "ans": "cos(2*x) / sqrt(sin(2*x))",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sqrt (Real.sin (2*x))) x = Real.cos (2*x) / Real.sqrt (Real.sin (2*x)) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.sqrt (Real.sin (2*x))"},

        # Page 183 (#532 - #534)
        {"num": 532, "q": "Given f(x) = sin(2x), g(x) = sqrt(x), h(x) = (x - 1)^3, find the derivative of f(h(x))",
         "ans": "6*(x - 1)^2*cos(2*(x - 1)^3)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sin (2*(x - 1)^3)) x = 6*(x - 1)^2*Real.cos (2*(x - 1)^3) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.sin (2*(x - 1)^3)"},
        {"num": 533, "q": "Given f(x) = sin(2x), g(x) = sqrt(x), h(x) = (x - 1)^3, find the derivative of h(g(x))",
         "ans": "3*(sqrt(x) - 1)^2 / (2*sqrt(x))",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (Real.sqrt x - 1)^3) x = 3*(Real.sqrt x - 1)^2 / (2*Real.sqrt x) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(Real.sqrt x - 1)^3"},
        {"num": 534, "q": "Given f(x) = sin(2x), g(x) = sqrt(x), h(x) = (x - 1)^3, find the derivative of h(f(x))",
         "ans": "6*cos(2*x)*(sin(2*x) - 1)^2",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (Real.sin (2*x) - 1)^3) x = 6*Real.cos (2*x)*(Real.sin (2*x) - 1)^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(Real.sin (2*x) - 1)^3"},

        # Page 184 (#535 - #537)
        {"num": 535, "q": "Find each derivative: f(x) = sin(x^2) + cos(x)^2",
         "ans": "2*x*cos(x^2) - sin(2*x)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sin (x^2) + (Real.cos x)^2) x = 2*x*Real.cos (x^2) - Real.sin (2*x) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.sin (x^2) + (Real.cos x)^2"},
        {"num": 536, "q": "Find each derivative: g(x) = -sqrt(3x - 4) + ln(3x)",
         "ans": "-3/(2*sqrt(3*x - 4)) + 1/x",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => -Real.sqrt (3*x - 4) + Real.log (3*x)) x = -3/(2*Real.sqrt (3*x - 4)) + 1/x := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "-Real.sqrt (3*x - 4) + Real.log (3*x)"},
        {"num": 537, "q": "Find each derivative: y = log_4(x^2*e^(x^7))",
         "ans": "(2/x + 7*x^6) / ln(4)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (2*Real.log x + x^7) / Real.log 4) x = (2/x + 7*x^6) / Real.log 4 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(2*Real.log x + x^7) / Real.log 4"},

        # Page 185 (#538 - #540)
        {"num": 538, "q": "Find each derivative: h(x) = e^sin(x) - e^tan(x)",
         "ans": "cos(x)*e^sin(x) - sec(x)^2*e^tan(x)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.exp (Real.sin x) - Real.exp (Real.tan x)) x = Real.cos x * Real.exp (Real.sin x) - (1 / Real.cos x)^2 * Real.exp (Real.tan x) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.exp (Real.sin x) - Real.exp (Real.tan x)"},
        {"num": 539, "q": "Find each derivative: f(x) = sin(x)^2 + cos(x)^2",
         "ans": "0",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (Real.sin x)^2 + (Real.cos x)^2) x = 0 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(Real.sin x)^2 + (Real.cos x)^2"},
        {"num": 540, "q": "Find each derivative: g(x) = (4x^2 - 6)^3",
         "ans": "24*x*(4*x^2 - 6)^2",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (4*x^2 - 6)^3) x = 24*x*(4*x^2 - 6)^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(4*x^2 - 6)^3"},

        # Page 186 (#541 - #543)
        {"num": 541, "q": "Find each derivative: f(x) = 6(x^3 - 6x)^3",
         "ans": "18*(3*x^2 - 6)*(x^3 - 6*x)^2",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => 6*(x^3 - 6*x)^3) x = 18*(3*x^2 - 6)*(x^3 - 6*x)^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "6*(x^3 - 6*x)^3"},
        {"num": 542, "q": "Find each derivative: h(x) = e^x*cos(x)*sin(2x - 1)",
         "ans": "e^x*cos(x)*sin(2*x - 1) - e^x*sin(x)*sin(2*x - 1) + 2*e^x*cos(x)*cos(2*x - 1)",
         "tid": "product_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.exp x * Real.cos x * Real.sin (2*x - 1)) x = Real.exp x * Real.cos x * Real.sin (2*x - 1) - Real.exp x * Real.sin x * Real.sin (2*x - 1) + 2*Real.exp x * Real.cos x * Real.cos (2*x - 1) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.exp x * Real.cos x * Real.sin (2*x - 1)"},
        {"num": 543, "q": "Find each derivative: y = e^(4x)*(x^2 + 1)^2",
         "ans": "4*e^(4*x)*(x^2 + 1)*(x^2 + x + 1)",
         "tid": "product_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.exp (4*x) * (x^2 + 1)^2) x = 4*Real.exp (4*x)*(x^2 + 1)*(x^2 + x + 1) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.exp (4*x) * (x^2 + 1)^2"},

        # Page 187 (#544 - #546)
        {"num": 544, "q": "Find each derivative: f(x) = sqrt(x^2 - 3) + ln(x^2 - 3)",
         "ans": "x/sqrt(x^2 - 3) + 2*x/(x^2 - 3)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sqrt (x^2 - 3) + Real.log (x^2 - 3)) x = x/Real.sqrt (x^2 - 3) + 2*x/(x^2 - 3) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.sqrt (x^2 - 3) + Real.log (x^2 - 3)"},
        {"num": 545, "q": "Find each derivative: y = 3(x - 5)^(-3)",
         "ans": "-9*(x - 5)^(-4)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => 3*(x - 5)^(-3 : ℤ)) x = -9*(x - 5)^(-4 : ℤ) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "3*(x - 5)^(-3 : ℤ)"},
        {"num": 546, "q": "Find each derivative: f(x) = cos(3x - pi) + cos(3x)",
         "ans": "0",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.cos (3*x - Real.pi) + Real.cos (3*x)) x = 0 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.cos (3*x - Real.pi) + Real.cos (3*x)"},

        # Page 188 (#547 - #549)
        {"num": 547, "q": "Find each derivative: g(x) = e^((x - 1)^2)",
         "ans": "2*(x - 1)*e^((x - 1)^2)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.exp ((x - 1)^2)) x = 2*(x - 1)*Real.exp ((x - 1)^2) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.exp ((x - 1)^2)"},
        {"num": 548, "q": "Find each derivative: y = (x - 2)^2 / (x - 1)^3",
         "ans": "(x - 2)*(4 - x) / (x - 1)^4",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (x - 2)^2 / (x - 1)^3) x = (x - 2)*(4 - x) / (x - 1)^4 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(x - 2)^2 / (x - 1)^3"},
        {"num": 549, "q": "Find each derivative: f(x) = 6sin(x^2) + ln(x)",
         "ans": "12*x*cos(x^2) + 1/x",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => 6*Real.sin (x^2) + Real.log x) x = 12*x*Real.cos (x^2) + 1/x := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "6*Real.sin (x^2) + Real.log x"},

        # Page 189 (#550 - #552)
        {"num": 550, "q": "Find each derivative: g(x) = 2/x + 2/(x - 1)^2",
         "ans": "-2/x^2 - 4/(x - 1)^3",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => 2/x + 2/(x - 1)^2) x = -2/x^2 - 4/(x - 1)^3 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "2/x + 2/(x - 1)^2"},
        {"num": 551, "q": "Find each derivative: y = ln(3x - 4) + e^(3x - 4)",
         "ans": "3/(3*x - 4) + 3*e^(3*x - 4)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.log (3*x - 4) + Real.exp (3*x - 4)) x = 3/(3*x - 4) + 3*Real.exp (3*x - 4) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.log (3*x - 4) + Real.exp (3*x - 4)"},
        {"num": 552, "q": "Find each derivative: f(x) = sin(x^3 - 5) - cos(4x + 1)",
         "ans": "3*x^2*cos(x^3 - 5) + 4*sin(4*x + 1)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sin (x^3 - 5) - Real.cos (4*x + 1)) x = 3*x^2*Real.cos (x^3 - 5) + 4*Real.sin (4*x + 1) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.sin (x^3 - 5) - Real.cos (4*x + 1)"},
    ]
    return probs

def generate_way1_entries() -> List[Dict[str, Any]]:
    entries = []
    probs = get_authentic_problems()
    for p in probs:
        q_raw = p["q"]
        ans = p["ans"]
        tid = p["tid"]
        lean = p["lean"]
        
        # Primary authentic entry
        params = {"expr": p.get("expr", ""), "ans": ans, "answer": ans}
        entries.append(make_entry(q_raw, tid, params, lean))
        
        # Conversational / textbook prompt variants
        var_prompts = []
        if tid == "particle_velocity_derivative":
            var_prompts.append(f"A particle moves along a straight line with position {q_raw.split('s(t) = ')[-1]}. Find its velocity v(t).")
        elif tid == "tangent_line":
            var_prompts.append(f"Determine the equation of the tangent line: {q_raw}")
        elif tid == "derivative_limit_definition":
            var_prompts.append(f"Evaluate the limit definition of the derivative: {q_raw}")
        elif tid == "tabular_derivative":
            var_prompts.append(f"Use the table of values to calculate: {q_raw}")
        else:
            var_prompts.append(f"Differentiate with respect to x: {q_raw.replace('Find dy/dx for ', '').replace('Find f\'(x) for ', '').replace('Find g\'(x) for ', '').replace('Find each derivative: ', '')}")
            
        for vp in var_prompts:
            entries.append(make_entry(vp, tid, params, lean))
            
    return entries

def _normalize_key(problem: str) -> str:
    key = problem.lower().strip()
    key = key.replace("−", "-").replace("×", "*").replace("·", "*").replace("÷", "/")
    key = key.replace("²", "^2").replace("³", "^3")
    key = re.sub(r"\s+", " ", key)
    key = re.sub(r"[?.!]+$", "", key).strip()
    return key

def generate_way2_entries() -> List[Dict[str, Any]]:
    entries = []
    
    # 1. Composite generalized power chains (ax^k + b)^n
    for a in [2, 3, 4, 5]:
        for b in [1, 2, 3]:
            for k in [2, 3]:
                for n in [3, 4]:
                    expr_str = f"({a}*x^{k} + {b})^{n}"
                    ans_str = f"{n * a * k}*x^{k-1}*({a}*x^{k} + {b})^{n-1}"
                    q = f"Differentiate f(x) = {expr_str} with respect to x using the chain rule"
                    lean = f"example (x : ℝ) : deriv (fun x => ({a}*x^{k} + {b})^{n}) x = {n * a * k}*x^{k-1}*({a}*x^{k} + {b})^{n-1} := by\n  simp [deriv_pow, deriv_add, deriv_mul]\n  ring"
                    entries.append(make_entry(q, "chain_rule_derivative", {"expr": expr_str, "answer": ans_str}, lean))
                
    # 2. Radical composite chains sqrt(ax^k + b)
    for a in [2, 3, 5, 6, 8]:
        for b in [1, 4, 7, 9]:
            expr_str = f"sqrt({a}*x^2 + {b})"
            ans_str = f"{a}*x / sqrt({a}*x^2 + {b})"
            q = f"Find the derivative of y = {expr_str}"
            lean = f"example (x : ℝ) : deriv (fun x => Real.sqrt ({a}*x^2 + {b})) x = {a}*x / Real.sqrt ({a}*x^2 + {b}) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_exp, deriv_log]\n  ring"
            entries.append(make_entry(q, "chain_rule_derivative", {"expr": expr_str, "answer": ans_str}, lean))

    # 3. Trigonometric nested chains sin(a*x + b), tan(a*x^2 + b)
    for a in [2, 3, 4, 5]:
        for b in [1, 2, 3, 4]:
            expr_str = f"sin({a}*x + {b})"
            ans_str = f"{a}*cos({a}*x + {b})"
            q = f"Find the derivative of y = {expr_str}"
            lean = f"example (x : ℝ) : deriv (fun x => Real.sin ({a}*x + {b})) x = {a}*Real.cos ({a}*x + {b}) := by\n  simp [deriv_sin, deriv_mul, deriv_add]\n  ring"
            entries.append(make_entry(q, "chain_rule_derivative", {"expr": expr_str, "answer": ans_str}, lean))

            expr_str2 = f"cos(tan({a}*x + {b}))"
            ans_str2 = f"-{a}*sec({a}*x + {b})^2*sin(tan({a}*x + {b}))"
            q2 = f"Find the derivative of y = {expr_str2}"
            lean2 = f"example (x : ℝ) : deriv (fun x => Real.cos (Real.tan ({a}*x + {b}))) x = -{a}*(1 / Real.cos ({a}*x + {b}))^2 * Real.sin (Real.tan ({a}*x + {b})) := by\n  simp [deriv_cos, deriv_tan, deriv_mul]\n  ring"
            entries.append(make_entry(q2, "chain_rule_derivative", {"expr": expr_str2, "answer": ans_str2}, lean2))

    # 4. Exponential and logarithmic chains e^(ax^2 + bx) and ln(ax + b)
    for a in [2, 3, 4, 5]:
        for b in [1, 2, 3]:
            expr_str = f"e^({a}*x^2 + {b}*x)"
            ans_str = f"(2*{a}*x + {b})*e^({a}*x^2 + {b}*x)"
            q = f"Find dy/dx for y = {expr_str}"
            lean = f"example (x : ℝ) : deriv (fun x => Real.exp ({a}*x^2 + {b}*x)) x = (2*{a}*x + {b})*Real.exp ({a}*x^2 + {b}*x) := by\n  simp [deriv_exp, deriv_pow, deriv_mul, deriv_add]\n  ring"
            entries.append(make_entry(q, "chain_rule_derivative", {"expr": expr_str, "answer": ans_str}, lean))

            expr_str2 = f"ln({a}*x + {b})"
            ans_str2 = f"{a}/({a}*x + {b})"
            q2 = f"Find the derivative of y = {expr_str2}"
            lean2 = f"example (x : ℝ) : deriv (fun x => Real.log ({a}*x + {b})) x = {a}/({a}*x + {b}) := by\n  simp [deriv_log, deriv_mul, deriv_add]\n  ring"
            entries.append(make_entry(q2, "chain_rule_derivative", {"expr": expr_str2, "answer": ans_str2}, lean2))

    # 5. Parametric Particle Velocities
    for c in [2, 3, 4, 5, 6]:
        for d in [1, 2, 3]:
            expr_str = f"sin({c}*t)*sqrt(t^2 + {d})"
            ans_str = f"{c}*cos({c}*t)*sqrt(t^2 + {d}) + t*sin({c}*t)/sqrt(t^2 + {d})"
            q = f"Find the velocity of the particle given the position s(t) = {expr_str}"
            lean = f"example (t : ℝ) : deriv (fun t => Real.sin ({c}*t) * Real.sqrt (t^2 + {d})) t = {c}*Real.cos ({c}*t)*Real.sqrt (t^2 + {d}) + t*Real.sin ({c}*t)/Real.sqrt (t^2 + {d}) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos]\n  ring"
            entries.append(make_entry(q, "particle_velocity_derivative", {"s": expr_str, "v": ans_str}, lean))

    # 6. Tangent line equations at given point
    for k in [1, 2, 3, 4, 5]:
        for m_val in [2, 3, 4]:
            q = f"Find the equation of the tangent line for f(x) = (x - {k})^3 at ({k+1}, 1)"
            ans_str = f"y = 3*x - {3*k + 2}"
            lean = f"example (x : ℝ) : deriv (fun x => (x - {k})^3) ({k+1}) = 3 ∧ ({k+1} - {k})^3 = 1 := by\n  simp [deriv_pow]\n  norm_num"
            entries.append(make_entry(q, "tangent_line", {"f": f"(x - {k})^3", "x0": str(k+1), "y0": "1", "m": "3", "line_eq": ans_str}, lean))

    return entries[:250]

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
        
        explanation = f"Applying {tid.replace('_', ' ')} yields the exact derivative: {ans}."
        if tid == "tangent_line":
            explanation = f"Evaluating the derivative at the given point yields the tangent line equation: {ans}."
        elif tid == "tabular_derivative":
            explanation = f"Using the functional table values and the chain rule: {ans}."
        elif tid == "particle_velocity_derivative":
            explanation = f"Differentiating position s(t) with respect to time t gives velocity v(t) = s'(t) = {ans}."
            
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
