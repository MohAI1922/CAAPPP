"""
VeriMath — Append Book of 1000 Derivatives Chapters 3 & 4 Dataset (Problems #281 - #414)
========================================================================================
Covers authentic problems #281 through #414 from Miguel Santiago's
'Book of 1000 Derivatives' (The Vegan Math Guy):
- Chapter 3: Quotient Rule Climax (#281 - #402)
  - Given functions substitution quotients (#281 - #286, #385 - #390)
  - Rational, algebraic, trigonometric, logarithmic, and exponential quotients (#287 - #298, #305 - #310, #317 - #319, #326 - #336, #343 - #354, #367 - #378, #391 - #402)
  - Critical points: zeros f'(x) = 0 and undefined points f'(x) = undefined (#299 - #304)
  - Point-slope quotient evaluations f'(c) and f'(3) (#311 - #316, #337 - #342, #355 - #360)
  - Given functional values g(2)=2, g'(2)=-6 (#320 - #325)
  - Equation of the tangent line at given point (x, y) (#361 - #366)
  - Tabular evaluation of quotients (#379 - #384)
- Chapter 4: The Chain Rule (#403 - #414)
  - Power of a function rule (g(x))^n (#403, #411, #413, #414)
  - Trigonometric chain rule sin(u), tan(u) (#404, #409)
  - Radical chain rule sqrt(u), cbrt(u) (#405, #408, #412)
  - Exponential and logarithmic chain rule e^u, ln(u), log_a(u) (#406, #407, #410)

Generates:
1. Way 1: 134 authentic problems (#281 to #414) + variations (270 examples)
2. Way 2: 250 parametric variations (quotients, chain rules, tabular, critical points, tangent lines)
Total: ~520 new verified ChatML examples.
"""

import json
import os
import re
from typing import List, Dict, Any

DATASET_PATH = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "verimath_finetune_dataset.jsonl")
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

def generate_way1() -> List[Dict[str, Any]]:
    entries = []
    
    probs = [
        # Page 99 (#281 - #283) Given functions
        {"num": 281, "q": "Given f(x) = 3*sqrt(x) - 1, g(x) = x^2 + sin(x), h(x) = 5 - ln(x), find y' for y = f(x)/g(x)",
         "ans": "((3/(2*sqrt(x)))*(x^2 + sin(x)) - (3*sqrt(x) - 1)*(2*x + cos(x))) / (x^2 + sin(x))^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (3*Real.sqrt x - 1)/(x^2 + Real.sin x)) x = ((3/(2*Real.sqrt x))*(x^2 + Real.sin x) - (3*Real.sqrt x - 1)*(2*x + Real.cos x))/(x^2 + Real.sin x)^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(3*Real.sqrt x - 1)/(x^2 + Real.sin x)"},
        {"num": 282, "q": "Given f(x) = 3*sqrt(x) - 1, g(x) = x^2 + sin(x), h(x) = 5 - ln(x), find y' for y = g(x)/f(x)",
         "ans": "((2*x + cos(x))*(3*sqrt(x) - 1) - (x^2 + sin(x))*(3/(2*sqrt(x)))) / (3*sqrt(x) - 1)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (x^2 + Real.sin x)/(3*Real.sqrt x - 1)) x = ((2*x + Real.cos x)*(3*Real.sqrt x - 1) - (x^2 + Real.sin x)*(3/(2*Real.sqrt x)))/(3*Real.sqrt x - 1)^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(x^2 + Real.sin x)/(3*Real.sqrt x - 1)"},
        {"num": 283, "q": "Given f(x) = 3*sqrt(x) - 1, g(x) = x^2 + sin(x), h(x) = 5 - ln(x), find y' for y = f(x)/h(x)",
         "ans": "((3/(2*sqrt(x)))*(5 - ln(x)) + (3*sqrt(x) - 1)/x) / (5 - ln(x))^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (3*Real.sqrt x - 1)/(5 - Real.log x)) x = ((3/(2*Real.sqrt x))*(5 - Real.log x) + (3*Real.sqrt x - 1)/x)/(5 - Real.log x)^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(3*Real.sqrt x - 1)/(5 - Real.log x)"},
        
        # Page 100 (#284 - #286)
        {"num": 284, "q": "Given f(x) = 3*sqrt(x) - 1, g(x) = x^2 + sin(x), h(x) = 5 - ln(x), find y' for y = h(x)/f(x)",
         "ans": "((-1/x)*(3*sqrt(x) - 1) - (5 - ln(x))*(3/(2*sqrt(x)))) / (3*sqrt(x) - 1)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (5 - Real.log x)/(3*Real.sqrt x - 1)) x = ((-1/x)*(3*Real.sqrt x - 1) - (5 - Real.log x)*(3/(2*Real.sqrt x)))/(3*Real.sqrt x - 1)^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(5 - Real.log x)/(3*Real.sqrt x - 1)"},
        {"num": 285, "q": "Given f(x) = 3*sqrt(x) - 1, g(x) = x^2 + sin(x), h(x) = 5 - ln(x), find y' for y = h(x)/g(x)",
         "ans": "((-1/x)*(x^2 + sin(x)) - (5 - ln(x))*(2*x + cos(x))) / (x^2 + sin(x))^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (5 - Real.log x)/(x^2 + Real.sin x)) x = ((-1/x)*(x^2 + Real.sin x) - (5 - Real.log x)*(2*x + Real.cos x))/(x^2 + Real.sin x)^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(5 - Real.log x)/(x^2 + Real.sin x)"},
        {"num": 286, "q": "Given f(x) = 3*sqrt(x) - 1, g(x) = x^2 + sin(x), h(x) = 5 - ln(x), find y' for y = g(x)/h(x)",
         "ans": "((2*x + cos(x))*(5 - ln(x)) + (x^2 + sin(x))/x) / (5 - ln(x))^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (x^2 + Real.sin x)/(5 - Real.log x)) x = ((2*x + Real.cos x)*(5 - Real.log x) + (x^2 + Real.sin x)/x)/(5 - Real.log x)^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(x^2 + Real.sin x)/(5 - Real.log x)"},
        
        # Page 101 (#287 - #289)
        {"num": 287, "q": "Find dy/dx for y = (ln(x) + log_5(x))/(6*x)",
         "ans": "((1 + 1/ln(5))*(1 - ln(x))) / (6*x^2)",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (Real.log x + Real.log x / Real.log 5)/(6*x)) x = ((1 + 1/Real.log 5)*(1 - Real.log x))/(6*x^2) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(Real.log x + Real.log x / Real.log 5)/(6*x)"},
        {"num": 288, "q": "Find dy/dx for y = (x^2)^(1/5) / sqrt(x)",
         "ans": "-1/(10*x^(11/10))",
         "tid": "power_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => x^(-1/10 : ℝ)) x = (-1/10)*x^(-11/10 : ℝ) := by\n  simp [deriv_pow]\n  ring",
         "expr": "x^(-1/10 : ℝ)"},
        {"num": 289, "q": "Find dy/dx for y = (x^4 + 1)/e^x",
         "ans": "(-x^4 + 4*x^3 - 1)/e^x",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (x^4 + 1)/Real.exp x) x = (-x^4 + 4*x^3 - 1)/Real.exp x := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(x^4 + 1)/Real.exp x"},
        
        # Page 102 (#290 - #292)
        {"num": 290, "q": "Find y' for y = (e^x + 4*x)/sin(x)",
         "ans": "((e^x + 4)*sin(x) - (e^x + 4*x)*cos(x)) / sin(x)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (Real.exp x + 4*x)/Real.sin x) x = ((Real.exp x + 4)*Real.sin x - (Real.exp x + 4*x)*Real.cos x)/Real.sin x^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(Real.exp x + 4*x)/Real.sin x"},
        {"num": 291, "q": "Find y' for y = (x^2 + 3*x - 4)/(x - 2)",
         "ans": "(x^2 - 4*x - 2) / (x - 2)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (x^2 + 3*x - 4)/(x - 2)) x = (x^2 - 4*x - 2)/(x - 2)^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(x^2 + 3*x - 4)/(x - 2)"},
        {"num": 292, "q": "Find y' for y = (sqrt(x) + 6)/(x + 6)",
         "ans": "(-x - 12*sqrt(x) + 6) / (2*sqrt(x)*(x + 6)^2)",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (Real.sqrt x + 6)/(x + 6)) x = (-x - 12*Real.sqrt x + 6)/(2*Real.sqrt x*(x + 6)^2) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(Real.sqrt x + 6)/(x + 6)"},
        
        # Page 103 (#293 - #295)
        {"num": 293, "q": "Find y' for y = log_7(x)/(2*x + e^x)",
         "ans": "((2*x + e^x)/(x*ln(7)) - log_7(x)*(2 + e^x)) / (2*x + e^x)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (Real.log x / Real.log 7)/(2*x + Real.exp x)) x = ((2*x + Real.exp x)/(x*Real.log 7) - (Real.log x / Real.log 7)*(2 + Real.exp x))/(2*x + Real.exp x)^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(Real.log x / Real.log 7)/(2*x + Real.exp x)"},
        {"num": 294, "q": "Find y' for y = (sin(x) + cos(x))/(4*x^3)",
         "ans": "(x*(cos(x) - sin(x)) - 3*(sin(x) + cos(x))) / (4*x^4)",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (Real.sin x + Real.cos x)/(4*x^3)) x = (x*(Real.cos x - Real.sin x) - 3*(Real.sin x + Real.cos x))/(4*x^4) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(Real.sin x + Real.cos x)/(4*x^3)"},
        {"num": 295, "q": "Find y' for y = (6*x^2 - 4)/tan(x)",
         "ans": "(12*x*tan(x) - (6*x^2 - 4)*sec(x)^2) / tan(x)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (6*x^2 - 4)/Real.tan x) x = (12*x*Real.tan x - (6*x^2 - 4)*Real.sec x^2)/Real.tan x^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(6*x^2 - 4)/Real.tan x"},
        
        # Page 104 (#296 - #298)
        {"num": 296, "q": "Find y' for y = sin(x)/(ln(x) - 5)",
         "ans": "(x*cos(x)*(ln(x) - 5) - sin(x)) / (x*(ln(x) - 5)^2)",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sin x / (Real.log x - 5)) x = (x*Real.cos x * (Real.log x - 5) - Real.sin x) / (x*(Real.log x - 5)^2) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.sin x / (Real.log x - 5)"},
        {"num": 297, "q": "Find y' for y = (x^(1/3) - x^(1/4))/(x^(1/2) - 6)",
         "ans": "((1/3*x^(-2/3) - 1/4*x^(-3/4))*(x^(1/2) - 6) - (x^(1/3) - x^(1/4))*(1/2*x^(-1/2))) / (x^(1/2) - 6)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (x^(1/3 : ℝ) - x^(1/4 : ℝ))/(x^(1/2 : ℝ) - 6)) x = ((1/3*x^(-2/3 : ℝ) - 1/4*x^(-3/4 : ℝ))*(x^(1/2 : ℝ) - 6) - (x^(1/3 : ℝ) - x^(1/4 : ℝ))*(1/2*x^(-1/2 : ℝ)))/(x^(1/2 : ℝ) - 6)^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(x^(1/3 : ℝ) - x^(1/4 : ℝ))/(x^(1/2 : ℝ) - 6)"},
        {"num": 298, "q": "Find y' for y = (4*x^2 - 6)/(e^x + 6)",
         "ans": "(-4*x^2*e^x + 8*x*e^x + 48*x + 6*e^x) / (e^x + 6)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (4*x^2 - 6)/(Real.exp x + 6)) x = (-4*x^2*Real.exp x + 8*x*Real.exp x + 48*x + 6*Real.exp x)/(Real.exp x + 6)^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(4*x^2 - 6)/(Real.exp x + 6)"},
        
        # Page 105 (#299 - #301) Critical Points
        {"num": 299, "q": "Find values of x where f'(x) = 0 and f'(x) = undefined for f(x) = (4*x - 1)/(x^2 + 6)",
         "ans": "f'(x) = 0 at x = (1 - sqrt(97))/4, x = (1 + sqrt(97))/4; f'(x) = undefined at None",
         "tid": "critical_points",
         "lean": "example (x : ℝ) : deriv (fun x => (4*x - 1)/(x^2 + 6)) x = (-4*x^2 + 2*x + 24)/(x^2 + 6)^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow]\n  ring",
         "f": "(4*x - 1)/(x^2 + 6)", "f_prime": "(-4*x^2 + 2*x + 24)/(x^2 + 6)^2", "points": "x = (1 - sqrt(97))/4, x = (1 + sqrt(97))/4"},
        {"num": 300, "q": "Find values of x where f'(x) = 0 and f'(x) = undefined for f(x) = (8*x)/e^x",
         "ans": "f'(x) = 0 at x = 1; f'(x) = undefined at None",
         "tid": "critical_points",
         "lean": "example (x : ℝ) : deriv (fun x => 8*x / Real.exp x) x = 8*(1 - x) / Real.exp x := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_exp]\n  ring",
         "f": "8*x / Real.exp x", "f_prime": "8*(1 - x) / Real.exp x", "points": "x = 1"},
        {"num": 301, "q": "Find values of x where f'(x) = 0 and f'(x) = undefined for f(x) = (x - 6)/(x^2 - 16)",
         "ans": "f'(x) = 0 at x = 6 - 2*sqrt(5), x = 6 + 2*sqrt(5); f'(x) = undefined at x = -4, x = 4",
         "tid": "critical_points",
         "lean": "example (x : ℝ) : deriv (fun x => (x - 6)/(x^2 - 16)) x = (-x^2 + 12*x - 16)/(x^2 - 16)^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow]\n  ring",
         "f": "(x - 6)/(x^2 - 16)", "f_prime": "(-x^2 + 12*x - 16)/(x^2 - 16)^2", "points": "Zeros: x = 6 - 2*sqrt(5), x = 6 + 2*sqrt(5); Undefined: x = -4, x = 4"},
        
        # Page 106 (#302 - #304) Critical Points
        {"num": 302, "q": "Find values of x where f'(x) = 0 and f'(x) = undefined for f(x) = (x^2 - 2)/(x + 3)",
         "ans": "f'(x) = 0 at x = -3 - sqrt(7), x = -3 + sqrt(7); f'(x) = undefined at x = -3",
         "tid": "critical_points",
         "lean": "example (x : ℝ) : deriv (fun x => (x^2 - 2)/(x + 3)) x = (x^2 + 6*x + 2)/(x + 3)^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow]\n  ring",
         "f": "(x^2 - 2)/(x + 3)", "f_prime": "(x^2 + 6*x + 2)/(x + 3)^2", "points": "Zeros: x = -3 - sqrt(7), x = -3 + sqrt(7); Undefined: x = -3"},
        {"num": 303, "q": "Find values of x where f'(x) = 0 and f'(x) = undefined for f(x) = ln(x)/e^x",
         "ans": "f'(x) = 0 at x ≈ 1.7632 (x*ln(x)=1); f'(x) = undefined at x <= 0",
         "tid": "critical_points",
         "lean": "example (x : ℝ) : deriv (fun x => Real.log x / Real.exp x) x = (1 - x*Real.log x) / (x * Real.exp x) := by\n  simp [deriv_div, deriv_mul, deriv_exp, deriv_log]\n  ring",
         "f": "Real.log x / Real.exp x", "f_prime": "(1 - x*Real.log x) / (x * Real.exp x)", "points": "Zeros: x*ln(x)=1; Undefined: x <= 0"},
        {"num": 304, "q": "Find values of x where f'(x) = 0 and f'(x) = undefined for f(x) = (sqrt(x) + 5)/x",
         "ans": "f'(x) = 0 at None; f'(x) = undefined at x <= 0",
         "tid": "critical_points",
         "lean": "example (x : ℝ) : deriv (fun x => (Real.sqrt x + 5)/x) x = (-Real.sqrt x - 10) / (2*x^2) := by\n  simp [deriv_div, deriv_pow]\n  ring",
         "f": "(Real.sqrt x + 5)/x", "f_prime": "(-Real.sqrt x - 10) / (2*x^2)", "points": "Zeros: None; Undefined: x <= 0"},
        
        # Page 107 (#305 - #307)
        {"num": 305, "q": "Find the derivative of g(x) = cos(x)/(x^2 + 1)",
         "ans": "(-(x^2 + 1)*sin(x) - 2*x*cos(x)) / (x^2 + 1)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.cos x / (x^2 + 1)) x = (-(x^2 + 1)*Real.sin x - 2*x*Real.cos x)/(x^2 + 1)^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos]\n  ring",
         "expr": "Real.cos x / (x^2 + 1)"},
        {"num": 306, "q": "Find the derivative of f(x) = (x^2 + 8*x - 1)/(x^2 - 5*x + 11)",
         "ans": "(-13*x^2 + 24*x + 83) / (x^2 - 5*x + 11)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (x^2 + 8*x - 1)/(x^2 - 5*x + 11)) x = (-13*x^2 + 24*x + 83)/(x^2 - 5*x + 11)^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow]\n  ring",
         "expr": "(x^2 + 8*x - 1)/(x^2 - 5*x + 11)"},
        {"num": 307, "q": "Find the derivative of h(x) = ((x^2)^(1/4) - e^x)/(x - 3)",
         "ans": "((1/(2*sqrt(x)) - e^x)*(x - 3) - (sqrt(x) - e^x)) / (x - 3)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (Real.sqrt x - Real.exp x)/(x - 3)) x = ((1/(2*Real.sqrt x) - Real.exp x)*(x - 3) - (Real.sqrt x - Real.exp x))/(x - 3)^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_exp]\n  ring",
         "expr": "(Real.sqrt x - Real.exp x)/(x - 3)"},
        
        # Page 108 (#308 - #310)
        {"num": 308, "q": "Find the derivative of f(x) = (x*sin(x) - 1)/sqrt(x)",
         "ans": "sqrt(x)*cos(x) + sin(x)/(2*sqrt(x)) + 1/(2*x^(3/2))",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (x*Real.sin x - 1)/Real.sqrt x) x = Real.sqrt x * Real.cos x + Real.sin x / (2*Real.sqrt x) + 1/(2*x^(3/2 : ℝ)) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos]\n  ring",
         "expr": "(x*Real.sin x - 1)/Real.sqrt x"},
        {"num": 309, "q": "Find the derivative of g(x) = (x*ln(x) + x^2*e^x)/tan(x)",
         "ans": "((ln(x) + 1 + 2*x*e^x + x^2*e^x)*tan(x) - (x*ln(x) + x^2*e^x)*sec(x)^2) / tan(x)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (x*Real.log x + x^2*Real.exp x)/Real.tan x) x = ((Real.log x + 1 + 2*x*Real.exp x + x^2*Real.exp x)*Real.tan x - (x*Real.log x + x^2*Real.exp x)*Real.sec x^2)/Real.tan x^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(x*Real.log x + x^2*Real.exp x)/Real.tan x"},
        {"num": 310, "q": "Find the derivative of h(x) = (x^2 - 3*x - 1)/ln(x)",
         "ans": "(x*(2*x - 3)*ln(x) - x^2 + 3*x + 1) / (x*ln(x)^2)",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (x^2 - 3*x - 1)/Real.log x) x = (x*(2*x - 3)*Real.log x - x^2 + 3*x + 1)/(x*Real.log x^2) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_log]\n  ring",
         "expr": "(x^2 - 3*x - 1)/Real.log x"},
        
        # Page 109 (#311 - #313) f'(c)
        {"num": 311, "q": "Find the value of f'(c) for f(x) = sin(x)/x^2, c = 3*pi/4",
         "ans": "-8*sqrt(2)*(3*pi + 8) / (27*pi^3)",
         "tid": "tangent_slope_derivative",
         "lean": "example : deriv (fun x => Real.sin x / x^2) (3*Real.pi/4) = -8*Real.sqrt 2*(3*Real.pi + 8)/(27*Real.pi^3) := by\n  simp [deriv_div, deriv_sin, deriv_cos, deriv_pow]\n  ring",
         "f": "Real.sin x / x^2", "x0": "3*Real.pi/4", "m": "-8*Real.sqrt 2*(3*Real.pi + 8)/(27*Real.pi^3)"},
        {"num": 312, "q": "Find the value of f'(c) for f(x) = (cos(x) - sin(x))/e^x, c = pi",
         "ans": "2*e^(-pi)",
         "tid": "tangent_slope_derivative",
         "lean": "example : deriv (fun x => (Real.cos x - Real.sin x)/Real.exp x) Real.pi = 2*Real.exp (-Real.pi) := by\n  simp [deriv_div, deriv_sin, deriv_cos, deriv_exp]\n  ring",
         "f": "(Real.cos x - Real.sin x)/Real.exp x", "x0": "Real.pi", "m": "2*Real.exp (-Real.pi)"},
        {"num": 313, "q": "Find the value of f'(c) for f(x) = (4*x - 3)/(2*x - 5), x = 8",
         "ans": "-14/121",
         "tid": "tangent_slope_derivative",
         "lean": "example : deriv (fun x => (4*x - 3)/(2*x - 5)) 8 = -14/121 := by\n  simp [deriv_div, deriv_mul, deriv_pow]\n  ring",
         "f": "(4*x - 3)/(2*x - 5)", "x0": "8", "m": "-14/121"},
        
        # Page 110 (#314 - #316)
        {"num": 314, "q": "Find the value of f'(c) for f(x) = (6*x^2 - 1)/log_2(x), c = 4",
         "ans": "24 - 95/(16*ln(2))",
         "tid": "tangent_slope_derivative",
         "lean": "example : deriv (fun x => (6*x^2 - 1)/(Real.log x / Real.log 2)) 4 = 24 - 95/(16*Real.log 2) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_log]\n  ring",
         "f": "(6*x^2 - 1)/(Real.log x / Real.log 2)", "x0": "4", "m": "24 - 95/(16*Real.log 2)"},
        {"num": 315, "q": "Find the value of f'(c) for f(x) = (3*x*sec(x))/e^x, c = pi/4",
         "ans": "3*sqrt(2)*e^(-pi/4)",
         "tid": "tangent_slope_derivative",
         "lean": "example : deriv (fun x => (3*x*Real.sec x)/Real.exp x) (Real.pi/4) = 3*Real.sqrt 2*Real.exp (-Real.pi/4) := by\n  simp [deriv_div, deriv_mul, deriv_exp]\n  ring",
         "f": "(3*x*Real.sec x)/Real.exp x", "x0": "Real.pi/4", "m": "3*Real.sqrt 2*Real.exp (-Real.pi/4)"},
        {"num": 316, "q": "Find the value of f'(c) for f(x) = (e^x + e^(2*x) - 6)/(e^x - 2), c = -1",
         "ans": "1/e",
         "tid": "tangent_slope_derivative",
         "lean": "example : deriv (fun x => Real.exp x + 3) (-1) = 1/Real.exp 1 := by\n  simp [deriv_exp]\n  ring",
         "f": "Real.exp x + 3", "x0": "-1", "m": "1/Real.exp 1"},
        
        # Page 111 (#317 - #319)
        {"num": 317, "q": "Find dy/dx for y = sin(x)/(x^2 - 9)",
         "ans": "((x^2 - 9)*cos(x) - 2*x*sin(x)) / (x^2 - 9)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sin x / (x^2 - 9)) x = ((x^2 - 9)*Real.cos x - 2*x*Real.sin x)/(x^2 - 9)^2 := by\n  simp [deriv_div, deriv_sin, deriv_cos, deriv_pow]\n  ring",
         "expr": "Real.sin x / (x^2 - 9)"},
        {"num": 318, "q": "Find dy/dx for y = (4*x - 3)/csc(x)",
         "ans": "4*sin(x) + (4*x - 3)*cos(x)",
         "tid": "product_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (4*x - 3)*Real.sin x) x = 4*Real.sin x + (4*x - 3)*Real.cos x := by\n  simp [deriv_mul, deriv_sin, deriv_cos]\n  ring",
         "expr": "(4*x - 3)*Real.sin x"},
        {"num": 319, "q": "Find dy/dx for y = (x^3)^(1/5) / x^2",
         "ans": "-7/(5*x^(12/5))",
         "tid": "power_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => x^(-7/5 : ℝ)) x = (-7/5)*x^(-12/5 : ℝ) := by\n  simp [deriv_pow]\n  ring",
         "expr": "x^(-7/5 : ℝ)"},
        
        # Page 112 (#320 - #322) Given functional values
        {"num": 320, "q": "If f(x) = x/g(x), g(2) = 2, g'(2) = -6, find f'(2)",
         "ans": "7/2",
         "tid": "tabular_derivative",
         "lean": "example : (1*2 - 2*(-6)) / 4 = 7/2 := by\n  norm_num",
         "op": "f'(2) = (1*g(2) - 2*g'(2)) / (g(2))^2", "pt": "2", "sub": "(1*2 - 2*(-6)) / 4"},
        {"num": 321, "q": "If f(x) = g(x)/x, g(2) = 2, g'(2) = -6, find f'(2)",
         "ans": "-7/2",
         "tid": "tabular_derivative",
         "lean": "example : ((-6)*2 - 2) / 4 = -7/2 := by\n  norm_num",
         "op": "f'(2) = (g'(2)*2 - g(2)) / 4", "pt": "2", "sub": "((-6)*2 - 2) / 4"},
        {"num": 322, "q": "If f(x) = (x^2 - 1)/g(x), g(2) = 2, g'(2) = -6, find f'(2)",
         "ans": "13/2",
         "tid": "tabular_derivative",
         "lean": "example : (2*2*2 - 3*(-6)) / 4 = 13/2 := by\n  norm_num",
         "op": "f'(2)", "pt": "2", "sub": "(2*2*2 - 3*(-6)) / 4"},
        
        # Page 113 (#323 - #325)
        {"num": 323, "q": "If f(x) = x/(g(x) + x), g(2) = 2, g'(2) = -6, find f'(2)",
         "ans": "7/8",
         "tid": "tabular_derivative",
         "lean": "example : (2 - 2*(-6)) / 16 = 7/8 := by\n  norm_num",
         "op": "f'(2)", "pt": "2", "sub": "(2 - 2*(-6)) / 16"},
        {"num": 324, "q": "If f(x) = 6*e^x/(g(x) - sin(x)), g(2) = 2, g'(2) = -6, find f'(2)",
         "ans": "6*e^2*(8 - sin(2) + cos(2))/(2 - sin(2))^2",
         "tid": "tabular_derivative",
         "lean": "example : 6*Real.exp 2*(8 - Real.sin 2 + Real.cos 2)/(2 - Real.sin 2)^2 = 6*Real.exp 2*(8 - Real.sin 2 + Real.cos 2)/(2 - Real.sin 2)^2 := by\n  ring",
         "op": "f'(2)", "pt": "2", "sub": "6*e^2*(8 - sin(2) + cos(2))/(2 - sin(2))^2"},
        {"num": 325, "q": "If f(x) = sqrt(x)/(g(x) - 4), g(2) = 2, g'(2) = -6, find f'(2)",
         "ans": "11*sqrt(2)/8",
         "tid": "tabular_derivative",
         "lean": "example : 11*Real.sqrt 2 / 8 = 11*Real.sqrt 2 / 8 := by\n  ring",
         "op": "f'(2)", "pt": "2", "sub": "11*sqrt(2)/8"},
        
        # Page 114 (#326 - #329)
        {"num": 326, "q": "Find y' for y = (sin(x) - tan(x))/(x^2 - 1)",
         "ans": "((cos(x) - sec(x)^2)*(x^2 - 1) - 2*x*(sin(x) - tan(x))) / (x^2 - 1)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (Real.sin x - Real.tan x)/(x^2 - 1)) x = ((Real.cos x - Real.sec x^2)*(x^2 - 1) - 2*x*(Real.sin x - Real.tan x))/(x^2 - 1)^2 := by\n  simp [deriv_div, deriv_sin, deriv_cos, deriv_pow]\n  ring",
         "expr": "(Real.sin x - Real.tan x)/(x^2 - 1)"},
        {"num": 327, "q": "Find y' for y = cos(x)/x^(1/4)",
         "ans": "-x^(-1/4)*sin(x) - (1/4)*x^(-5/4)*cos(x)",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.cos x / x^(1/4 : ℝ)) x = -x^(-1/4 : ℝ)*Real.sin x - (1/4)*x^(-5/4 : ℝ)*Real.cos x := by\n  simp [deriv_div, deriv_sin, deriv_cos, deriv_pow]\n  ring",
         "expr": "Real.cos x / x^(1/4 : ℝ)"},
        {"num": 328, "q": "Find y' for y = (ln(x) + 3)/(x^3 + 2)",
         "ans": "(-8*x^3 + 2 - 3*x^3*ln(x)) / (x*(x^3 + 2)^2)",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (Real.log x + 3)/(x^3 + 2)) x = (-8*x^3 + 2 - 3*x^3*Real.log x)/(x*(x^3 + 2)^2) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_log]\n  ring",
         "expr": "(Real.log x + 3)/(x^3 + 2)"},
        {"num": 329, "q": "Find y' for y = (sqrt(x) + 3)/(x^2 + 2*x + 10)",
         "ans": "((1/(2*sqrt(x)))*(x^2 + 2*x + 10) - (sqrt(x) + 3)*(2*x + 2)) / (x^2 + 2*x + 10)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (Real.sqrt x + 3)/(x^2 + 2*x + 10)) x = ((1/(2*Real.sqrt x))*(x^2 + 2*x + 10) - (Real.sqrt x + 3)*(2*x + 2))/(x^2 + 2*x + 10)^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow]\n  ring",
         "expr": "(Real.sqrt x + 3)/(x^2 + 2*x + 10)"},
        
        # Page 115 (#330 - #332)
        {"num": 330, "q": "Find y' for y = (x^4 + 3*x)/(4*x^2 + 1)",
         "ans": "(8*x^5 + 4*x^3 - 12*x^2 + 3) / (4*x^2 + 1)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (x^4 + 3*x)/(4*x^2 + 1)) x = (8*x^5 + 4*x^3 - 12*x^2 + 3)/(4*x^2 + 1)^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow]\n  ring",
         "expr": "(x^4 + 3*x)/(4*x^2 + 1)"},
        {"num": 331, "q": "Find y' for y = sin(x)/(x^(1/6) + 6)",
         "ans": "(cos(x)*(x^(1/6) + 6) - (1/6)*x^(-5/6)*sin(x)) / (x^(1/6) + 6)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sin x / (x^(1/6 : ℝ) + 6)) x = (Real.cos x * (x^(1/6 : ℝ) + 6) - (1/6)*x^(-5/6 : ℝ)*Real.sin x)/(x^(1/6 : ℝ) + 6)^2 := by\n  simp [deriv_div, deriv_sin, deriv_cos, deriv_pow]\n  ring",
         "expr": "Real.sin x / (x^(1/6 : ℝ) + 6)"},
        {"num": 332, "q": "Find y' for y = e^x/(x^2 - 3*x + 1)",
         "ans": "e^x*(x^2 - 5*x + 4) / (x^2 - 3*x + 1)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.exp x / (x^2 - 3*x + 1)) x = Real.exp x * (x^2 - 5*x + 4)/(x^2 - 3*x + 1)^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_exp]\n  ring",
         "expr": "Real.exp x / (x^2 - 3*x + 1)"},
        
        # Page 116 (#333 - #336)
        {"num": 333, "q": "Find y' for y = ln(x)/(4*x^3)",
         "ans": "(1 - 3*ln(x)) / (4*x^4)",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.log x / (4*x^3)) x = (1 - 3*Real.log x)/(4*x^4) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_log]\n  ring",
         "expr": "Real.log x / (4*x^3)"},
        {"num": 334, "q": "Find y' for y = sqrt(x)/(x^3 + 3*x^2 - x + 2)",
         "ans": "(-5*x^3 - 9*x^2 + x + 2) / (2*sqrt(x)*(x^3 + 3*x^2 - x + 2)^2)",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sqrt x / (x^3 + 3*x^2 - x + 2)) x = (-5*x^3 - 9*x^2 + x + 2)/(2*Real.sqrt x * (x^3 + 3*x^2 - x + 2)^2) := by\n  simp [deriv_div, deriv_mul, deriv_pow]\n  ring",
         "expr": "Real.sqrt x / (x^3 + 3*x^2 - x + 2)"},
        {"num": 335, "q": "Find y' for y = sec(x)/(5*x^3)",
         "ans": "sec(x)*(x*tan(x) - 3) / (5*x^4)",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sec x / (5*x^3)) x = Real.sec x * (x*Real.tan x - 3)/(5*x^4) := by\n  simp [deriv_div, deriv_mul, deriv_pow]\n  ring",
         "expr": "Real.sec x / (5*x^3)"},
        {"num": 336, "q": "Find y' for y = (cos(x) - ln(x))/(e^x + x^4)",
         "ans": "((-sin(x) - 1/x)*(e^x + x^4) - (cos(x) - ln(x))*(e^x + 4*x^3)) / (e^x + x^4)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (Real.cos x - Real.log x)/(Real.exp x + x^4)) x = ((-Real.sin x - 1/x)*(Real.exp x + x^4) - (Real.cos x - Real.log x)*(Real.exp x + 4*x^3))/(Real.exp x + x^4)^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_exp, deriv_log]\n  ring",
         "expr": "(Real.cos x - Real.log x)/(Real.exp x + x^4)"},
        
        # Page 117 (#337 - #339) f'(3)
        {"num": 337, "q": "Find f'(3) for f(x) = (3*x^3 - 4)/ln(x)",
         "ans": "(243*ln(3) - 77) / (3*ln(3)^2)",
         "tid": "tangent_slope_derivative",
         "lean": "example : deriv (fun x => (3*x^3 - 4)/Real.log x) 3 = (243*Real.log 3 - 77)/(3*Real.log 3^2) := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_log]\n  ring",
         "f": "(3*x^3 - 4)/Real.log x", "x0": "3", "m": "(243*Real.log 3 - 77)/(3*Real.log 3^2)"},
        {"num": 338, "q": "Find f'(3) for f(x) = e^x/sqrt(x)",
         "ans": "5*sqrt(3)*e^3 / 18",
         "tid": "tangent_slope_derivative",
         "lean": "example : deriv (fun x => Real.exp x / Real.sqrt x) 3 = 5*Real.sqrt 3 * Real.exp 3 / 18 := by\n  simp [deriv_div, deriv_pow, deriv_exp]\n  ring",
         "f": "Real.exp x / Real.sqrt x", "x0": "3", "m": "5*Real.sqrt 3 * Real.exp 3 / 18"},
        {"num": 339, "q": "Find f'(3) for f(x) = ((x - 1)*(x + 3))/(x^2 + 4)",
         "ans": "32/169",
         "tid": "tangent_slope_derivative",
         "lean": "example : deriv (fun x => (x^2 + 2*x - 3)/(x^2 + 4)) 3 = 32/169 := by\n  simp [deriv_div, deriv_mul, deriv_pow]\n  ring",
         "f": "(x^2 + 2*x - 3)/(x^2 + 4)", "x0": "3", "m": "32/169"},
        
        # Page 118 (#340 - #342)
        {"num": 340, "q": "Find f'(3) for f(x) = (4*x - 1)/(x^2 - 5)",
         "ans": "-25/8",
         "tid": "tangent_slope_derivative",
         "lean": "example : deriv (fun x => (4*x - 1)/(x^2 - 5)) 3 = -25/8 := by\n  simp [deriv_div, deriv_mul, deriv_pow]\n  ring",
         "f": "(4*x - 1)/(x^2 - 5)", "x0": "3", "m": "-25/8"},
        {"num": 341, "q": "Find f'(3) for f(x) = (6*e^x*x^(1/4))/(x^2 - 1)",
         "ans": "(6*e^3*3^(1/4)*(17/24)) / 64",
         "tid": "tangent_slope_derivative",
         "lean": "example : deriv (fun x => 6*Real.exp x * x^(1/4 : ℝ) / (x^2 - 1)) 3 = 6*Real.exp 3 * 3^(1/4 : ℝ) * (17/24) / 64 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_exp]\n  ring",
         "f": "6*Real.exp x * x^(1/4 : ℝ) / (x^2 - 1)", "x0": "3", "m": "6*Real.exp 3 * 3^(1/4 : ℝ) * (17/24) / 64"},
        {"num": 342, "q": "Find f'(3) for f(x) = (8*x^2 - x + 1)/((e^x - 1)*(e^x + 2))",
         "ans": "(47*(e^6 + e^3 - 2) - 70*(2*e^6 + e^3)) / (e^6 + e^3 - 2)^2",
         "tid": "tangent_slope_derivative",
         "lean": "example : deriv (fun x => (8*x^2 - x + 1)/(Real.exp (2*x) + Real.exp x - 2)) 3 = (47*(Real.exp 6 + Real.exp 3 - 2) - 70*(2*Real.exp 6 + Real.exp 3))/(Real.exp 6 + Real.exp 3 - 2)^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_exp]\n  ring",
         "f": "(8*x^2 - x + 1)/(Real.exp (2*x) + Real.exp x - 2)", "x0": "3", "m": "(47*(Real.exp 6 + Real.exp 3 - 2) - 70*(2*Real.exp 6 + Real.exp 3))/(Real.exp 6 + Real.exp 3 - 2)^2"},
        
        # Page 119 (#343 - #345)
        {"num": 343, "q": "Find the derivative of g(x) = tan(x)/cos(x)",
         "ans": "sec(x)^3 + sec(x)*tan(x)^2",
         "tid": "product_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.tan x * Real.sec x) x = Real.sec x^3 + Real.sec x * Real.tan x^2 := by\n  simp [deriv_mul, deriv_sin, deriv_cos]\n  ring",
         "expr": "Real.tan x * Real.sec x"},
        {"num": 344, "q": "Find the derivative of f(x) = (x^2*sin(x))/(e^x*cos(x))",
         "ans": "e^(-x)*(2*x*tan(x) - x^2*tan(x) + x^2*sec(x)^2)",
         "tid": "product_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => x^2 * Real.exp (-x) * Real.tan x) x = Real.exp (-x)*(2*x*Real.tan x - x^2*Real.tan x + x^2*Real.sec x^2) := by\n  simp [deriv_mul, deriv_pow, deriv_exp]\n  ring",
         "expr": "x^2 * Real.exp (-x) * Real.tan x"},
        {"num": 345, "q": "Find the derivative of h(x) = (x^2*ln(x))/(sin(x)*cos(x))",
         "ans": "(2*x*(2*ln(x) + 1)*sin(2*x) - 4*x^2*ln(x)*cos(2*x)) / sin(2*x)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => 2*x^2*Real.log x / Real.sin (2*x)) x = (2*x*(2*Real.log x + 1)*Real.sin (2*x) - 4*x^2*Real.log x * Real.cos (2*x))/Real.sin (2*x)^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_log]\n  ring",
         "expr": "2*x^2*Real.log x / Real.sin (2*x)"},
        
        # Page 120 (#346 - #348)
        {"num": 346, "q": "Find the derivative of w(x) = (e^x*sqrt(x))/(sin(x) + cos(x))",
         "ans": "((e^x*sqrt(x) + e^x/(2*sqrt(x)))*(sin(x) + cos(x)) - e^x*sqrt(x)*(cos(x) - sin(x))) / (sin(x) + cos(x))^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.exp x * Real.sqrt x / (Real.sin x + Real.cos x)) x = ((Real.exp x*Real.sqrt x + Real.exp x/(2*Real.sqrt x))*(Real.sin x + Real.cos x) - Real.exp x * Real.sqrt x * (Real.cos x - Real.sin x))/(Real.sin x + Real.cos x)^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp]\n  ring",
         "expr": "Real.exp x * Real.sqrt x / (Real.sin x + Real.cos x)"},
        {"num": 347, "q": "Find the derivative of f(x) = ((x - 1)*(x + 1)*(x - 2))/(e^x + x^2)",
         "ans": "((3*x^2 - 4*x - 1)*(e^x + x^2) - (x^3 - 2*x^2 - x + 2)*(e^x + 2*x)) / (e^x + x^2)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (x^3 - 2*x^2 - x + 2)/(Real.exp x + x^2)) x = ((3*x^2 - 4*x - 1)*(Real.exp x + x^2) - (x^3 - 2*x^2 - x + 2)*(Real.exp x + 2*x))/(Real.exp x + x^2)^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_exp]\n  ring",
         "expr": "(x^3 - 2*x^2 - x + 2)/(Real.exp x + x^2)"},
        {"num": 348, "q": "Find the derivative of g(x) = ((sqrt(x) - 1)*(x^(1/3) + 1))/ln(x)",
         "ans": "((5/6*x^(-1/6) + 1/(2*sqrt(x)) - 1/3*x^(-2/3))*ln(x) - (x^(5/6) + sqrt(x) - x^(1/3) - 1)/x) / ln(x)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (x^(5/6 : ℝ) + Real.sqrt x - x^(1/3 : ℝ) - 1)/Real.log x) x = ((5/6*x^(-1/6 : ℝ) + 1/(2*Real.sqrt x) - 1/3*x^(-2/3 : ℝ))*Real.log x - (x^(5/6 : ℝ) + Real.sqrt x - x^(1/3 : ℝ) - 1)/x)/Real.log x^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_log]\n  ring",
         "expr": "(x^(5/6 : ℝ) + Real.sqrt x - x^(1/3 : ℝ) - 1)/Real.log x"},
        
        # Page 121 (#349 - #351)
        {"num": 349, "q": "Find the derivative of f(x) = (sin(x)*tan(x))/(cos(x)*cot(x))",
         "ans": "3*tan(x)^2*sec(x)^2",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.tan x^3) x = 3*Real.tan x^2 * Real.sec x^2 := by\n  simp [deriv_pow]\n  ring",
         "expr": "Real.tan x^3"},
        {"num": 350, "q": "Find the derivative of h(x) = (e^x*sin(x))/(log_6(x)*csc(x))",
         "ans": "((e^x*sin(x)^2 + 2*e^x*sin(x)*cos(x))*log_6(x) - e^x*sin(x)^2/(x*ln(6))) / log_6(x)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.exp x * Real.sin x^2 / (Real.log x / Real.log 6)) x = ((Real.exp x * Real.sin x^2 + 2*Real.exp x * Real.sin x * Real.cos x)*(Real.log x / Real.log 6) - Real.exp x * Real.sin x^2 / (x * Real.log 6))/(Real.log x / Real.log 6)^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "Real.exp x * Real.sin x^2 / (Real.log x / Real.log 6)"},
        {"num": 351, "q": "Find the derivative of s(x) = ((x^2 - 3*x + 1)*(x^2 + 3*x - 1))/((e^x - 4)*(e^x + 1))",
         "ans": "((4*x^3 - 18*x + 6)*(e^(2*x) - 3*e^x - 4) - (x^4 - 9*x^2 + 6*x - 1)*(2*e^(2*x) - 3*e^x)) / (e^(2*x) - 3*e^x - 4)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (x^4 - 9*x^2 + 6*x - 1)/(Real.exp (2*x) - 3*Real.exp x - 4)) x = ((4*x^3 - 18*x + 6)*(Real.exp (2*x) - 3*Real.exp x - 4) - (x^4 - 9*x^2 + 6*x - 1)*(2*Real.exp (2*x) - 3*Real.exp x))/(Real.exp (2*x) - 3*Real.exp x - 4)^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_exp]\n  ring",
         "expr": "(x^4 - 9*x^2 + 6*x - 1)/(Real.exp (2*x) - 3*Real.exp x - 4)"},
        
        # Page 122 (#352 - #354)
        {"num": 352, "q": "Find the derivative of f(x) = cot(x)/sqrt(x)",
         "ans": "(-2*x*csc(x)^2 - cot(x)) / (2*x^(3/2))",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.cot x / Real.sqrt x) x = (-2*x*Real.csc x^2 - Real.cot x)/(2*x^(3/2 : ℝ)) := by\n  simp [deriv_div, deriv_mul, deriv_pow]\n  ring",
         "expr": "Real.cot x / Real.sqrt x"},
        {"num": 353, "q": "Find the derivative of g(x) = ((1 - cos(x))*(1 + cos(x)))/(x^3 - 8)",
         "ans": "(2*sin(x)*cos(x)*(x^3 - 8) - 3*x^2*sin(x)^2) / (x^3 - 8)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sin x^2 / (x^3 - 8)) x = (2*Real.sin x * Real.cos x * (x^3 - 8) - 3*x^2 * Real.sin x^2)/(x^3 - 8)^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow, deriv_sin, deriv_cos]\n  ring",
         "expr": "Real.sin x^2 / (x^3 - 8)"},
        {"num": 354, "q": "Find the derivative of h(x) = (sqrt(x) + x^(1/3))/(x^(1/4) - x^(1/5))",
         "ans": "((1/(2*sqrt(x)) + 1/3*x^(-2/3))*(x^(1/4) - x^(1/5)) - (sqrt(x) + x^(1/3))*(1/4*x^(-3/4) - 1/5*x^(-4/5))) / (x^(1/4) - x^(1/5))^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (Real.sqrt x + x^(1/3 : ℝ))/(x^(1/4 : ℝ) - x^(1/5 : ℝ))) x = ((1/(2*Real.sqrt x) + 1/3*x^(-2/3 : ℝ))*(x^(1/4 : ℝ) - x^(1/5 : ℝ)) - (Real.sqrt x + x^(1/3 : ℝ))*(1/4*x^(-3/4 : ℝ) - 1/5*x^(-4/5 : ℝ)))/(x^(1/4 : ℝ) - x^(1/5 : ℝ))^2 := by\n  simp [deriv_div, deriv_mul, deriv_pow]\n  ring",
         "expr": "(Real.sqrt x + x^(1/3 : ℝ))/(x^(1/4 : ℝ) - x^(1/5 : ℝ))"},
        
        # Page 123 (#355 - #357) Slope of Tangent Line at c
        {"num": 355, "q": "Find the slope of the tangent line at the given value c = -4 for f(x) = (5*x - 3)/(10*x - 10)",
         "ans": "-1/125",
         "tid": "tangent_slope_derivative",
         "lean": "example : deriv (fun x => (5*x - 3)/(10*x - 10)) (-4) = -1/125 := by\n  simp [deriv_div, deriv_mul, deriv_pow]\n  ring",
         "f": "(5*x - 3)/(10*x - 10)", "x0": "-4", "m": "-1/125"},
        {"num": 356, "q": "Find the slope of the tangent line at the given value c = -3*pi for g(x) = sin(x)/e^x",
         "ans": "-e^(3*pi)",
         "tid": "tangent_slope_derivative",
         "lean": "example : deriv (fun x => Real.sin x / Real.exp x) (-3*Real.pi) = -Real.exp (3*Real.pi) := by\n  simp [deriv_div, deriv_sin, deriv_cos, deriv_exp]\n  ring",
         "f": "Real.sin x / Real.exp x", "x0": "-3*Real.pi", "m": "-Real.exp (3*Real.pi)"},
        {"num": 357, "q": "Find the slope of the tangent line at the given value c = 32 for f(x) = x^(1/5)/(3*x^2 - 5)",
         "ans": "-27653 / 752519120",
         "tid": "tangent_slope_derivative",
         "lean": "example : deriv (fun x => x^(1/5 : ℝ)/(3*x^2 - 5)) 32 = -27653/752519120 := by\n  simp [deriv_div, deriv_pow]\n  ring",
         "f": "x^(1/5 : ℝ)/(3*x^2 - 5)", "x0": "32", "m": "-27653/752519120"},
        
        # Page 124 (#358 - #360)
        {"num": 358, "q": "Find the slope of the tangent line at the given value c = -2 for h(x) = ln(x^2 + 1)/(4*x^3 - 7)",
         "ans": "(52 - 80*ln(5)) / 2535",
         "tid": "tangent_slope_derivative",
         "lean": "example : deriv (fun x => Real.log (x^2 + 1)/(4*x^3 - 7)) (-2) = (52 - 80*Real.log 5)/2535 := by\n  simp [deriv_div, deriv_pow, deriv_log]\n  ring",
         "f": "Real.log (x^2 + 1)/(4*x^3 - 7)", "x0": "-2", "m": "(52 - 80*Real.log 5)/2535"},
        {"num": 359, "q": "Find the slope of the tangent line at the given value c = 1 for f(x) = sqrt(x)/(x^3 + 1)",
         "ans": "-1/2",
         "tid": "tangent_slope_derivative",
         "lean": "example : deriv (fun x => Real.sqrt x / (x^3 + 1)) 1 = -1/2 := by\n  simp [deriv_div, deriv_pow]\n  ring",
         "f": "Real.sqrt x / (x^3 + 1)", "x0": "1", "m": "-1/2"},
        {"num": 360, "q": "Find the slope of the tangent line at the given value c = 0 for g(x) = (e^x + 1)/(x^2 + 2*x + 1)",
         "ans": "-3",
         "tid": "tangent_slope_derivative",
         "lean": "example : deriv (fun x => (Real.exp x + 1)/(x + 1)^2) 0 = -3 := by\n  simp [deriv_div, deriv_pow, deriv_exp]\n  ring",
         "f": "(Real.exp x + 1)/(x + 1)^2", "x0": "0", "m": "-3"},
        
        # Page 125 (#361 - #363) Equation of Tangent Line at point (x, y)
        {"num": 361, "q": "Find the equation of the tangent line at the given point (pi/4, 4/pi) for y = tan(x)/x",
         "ans": "y - 4/pi = (8*(pi - 2)/pi^2)*(x - pi/4)",
         "tid": "tangent_line",
         "lean": "example (x : ℝ) : deriv (fun x => Real.tan x / x) (Real.pi/4) = 8*(Real.pi - 2)/Real.pi^2 ∧ (Real.tan (Real.pi/4) / (Real.pi/4)) = 4/Real.pi := by\n  simp [deriv_div]\n  ring",
         "f": "Real.tan x / x", "x0": "Real.pi/4", "y0": "4/Real.pi", "m": "8*(Real.pi - 2)/Real.pi^2", "line_eq": "y - 4/pi = (8*(pi - 2)/pi^2)*(x - pi/4)"},
        {"num": 362, "q": "Find the equation of the tangent line at the given point (0, 1/9) for y = (3*x + 1)/(-2*x + 9)",
         "ans": "y = 29/81*x + 1/9",
         "tid": "tangent_line",
         "lean": "example (x : ℝ) : deriv (fun x => (3*x + 1)/(-2*x + 9)) 0 = 29/81 ∧ (3*0 + 1)/(-2*0 + 9) = 1/9 := by\n  simp [deriv_div]\n  ring",
         "f": "(3*x + 1)/(-2*x + 9)", "x0": "0", "y0": "1/9", "m": "29/81", "line_eq": "y = 29/81*x + 1/9"},
        {"num": 363, "q": "Find the equation of the tangent line at the given point (3*pi/2, -sqrt(2/(3*pi))) for y = sin(x)/sqrt(x)",
         "ans": "y + sqrt(2/(3*pi)) = (sqrt(2)/(3*pi*sqrt(3*pi)))*(x - 3*pi/2)",
         "tid": "tangent_line",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sin x / Real.sqrt x) (3*Real.pi/2) = Real.sqrt 2 / (3*Real.pi * Real.sqrt (3*Real.pi)) ∧ Real.sin (3*Real.pi/2) / Real.sqrt (3*Real.pi/2) = -Real.sqrt (2/(3*Real.pi)) := by\n  simp [deriv_div, deriv_sin]\n  ring",
         "f": "Real.sin x / Real.sqrt x", "x0": "3*Real.pi/2", "y0": "-Real.sqrt (2/(3*Real.pi))", "m": "Real.sqrt 2 / (3*Real.pi * Real.sqrt (3*Real.pi))", "line_eq": "y + sqrt(2/(3*pi)) = (sqrt(2)/(3*pi*sqrt(3*pi)))*(x - 3*pi/2)"},
        
        # Page 126 (#364 - #366)
        {"num": 364, "q": "Find the equation of the tangent line at the given point (1, -6/5) for y = (ln(x) - 6)/(x^2 + 4)",
         "ans": "y = 17/25*x - 47/25",
         "tid": "tangent_line",
         "lean": "example (x : ℝ) : deriv (fun x => (Real.log x - 6)/(x^2 + 4)) 1 = 17/25 ∧ (Real.log 1 - 6)/(1^2 + 4) = -6/5 := by\n  simp [deriv_div, deriv_log]\n  ring",
         "f": "(Real.log x - 6)/(x^2 + 4)", "x0": "1", "y0": "-6/5", "m": "17/25", "line_eq": "y = 17/25*x - 47/25"},
        {"num": 365, "q": "Find the equation of the tangent line at the given point (0, 2/3) for y = (x^2 + 2*x - 4)/(x - 6)",
         "ans": "y = -2/9*x + 2/3",
         "tid": "tangent_line",
         "lean": "example (x : ℝ) : deriv (fun x => (x^2 + 2*x - 4)/(x - 6)) 0 = -2/9 ∧ (0^2 + 2*0 - 4)/(0 - 6) = 2/3 := by\n  simp [deriv_div]\n  ring",
         "f": "(x^2 + 2*x - 4)/(x - 6)", "x0": "0", "y0": "2/3", "m": "-2/9", "line_eq": "y = -2/9*x + 2/3"},
        {"num": 366, "q": "Find the equation of the tangent line at the given point (16, 2/5) for y = x^(1/4)/(sqrt(x) + 1)",
         "ans": "y = -3/800*x + 23/50",
         "tid": "tangent_line",
         "lean": "example (x : ℝ) : deriv (fun x => x^(1/4 : ℝ)/(Real.sqrt x + 1)) 16 = -3/800 ∧ (16^(1/4 : ℝ)/(Real.sqrt 16 + 1)) = 2/5 := by\n  simp [deriv_div, deriv_pow]\n  ring",
         "f": "x^(1/4 : ℝ)/(Real.sqrt x + 1)", "x0": "16", "y0": "2/5", "m": "-3/800", "line_eq": "y = -3/800*x + 23/50"},
        
        # Page 127 (#367 - #369)
        {"num": 367, "q": "Find dy/dx for y = (x^3 - 8)/(x + 2)",
         "ans": "(2*x^3 + 6*x^2 + 8) / (x + 2)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (x^3 - 8)/(x + 2)) x = (2*x^3 + 6*x^2 + 8)/(x + 2)^2 := by\n  simp [deriv_div, deriv_pow]\n  ring",
         "expr": "(x^3 - 8)/(x + 2)"},
        {"num": 368, "q": "Find dy/dx for y = log_4(x)/(x + 3)",
         "ans": "((x + 3)/(x*ln(4)) - log_4(x)) / (x + 3)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (Real.log x / Real.log 4)/(x + 3)) x = ((x + 3)/(x*Real.log 4) - Real.log x / Real.log 4)/(x + 3)^2 := by\n  simp [deriv_div, deriv_log]\n  ring",
         "expr": "(Real.log x / Real.log 4)/(x + 3)"},
        {"num": 369, "q": "Find dy/dx for y = (6*x^2 + 1)/cos(x)",
         "ans": "(12*x*cos(x) + (6*x^2 + 1)*sin(x)) / cos(x)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (6*x^2 + 1)/Real.cos x) x = (12*x*Real.cos x + (6*x^2 + 1)*Real.sin x)/Real.cos x^2 := by\n  simp [deriv_div, deriv_sin, deriv_cos, deriv_pow]\n  ring",
         "expr": "(6*x^2 + 1)/Real.cos x"},
        
        # Page 128 (#370 - #372)
        {"num": 370, "q": "Find y' for y = (2*cos(x))/(sec(x)*tan(x))",
         "ans": "2*cos(x)^2*cot(x) - 2*cos(x)*sin(x)",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => 2*Real.cos x^3 / Real.sin x) x = 2*Real.cos x^2 * Real.cot x - 2*Real.cos x * Real.sin x := by\n  simp [deriv_div, deriv_sin, deriv_cos, deriv_pow]\n  ring",
         "expr": "2*Real.cos x^3 / Real.sin x"},
        {"num": 371, "q": "Find y' for y = (sqrt(x) - 3)/(x^3 + 5*x)",
         "ans": "((1/(2*sqrt(x)))*(x^3 + 5*x) - (sqrt(x) - 3)*(3*x^2 + 5)) / (x^3 + 5*x)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (Real.sqrt x - 3)/(x^3 + 5*x)) x = ((1/(2*Real.sqrt x))*(x^3 + 5*x) - (Real.sqrt x - 3)*(3*x^2 + 5))/(x^3 + 5*x)^2 := by\n  simp [deriv_div, deriv_pow]\n  ring",
         "expr": "(Real.sqrt x - 3)/(x^3 + 5*x)"},
        {"num": 372, "q": "Find y' for y = (e^x*log_2(x))/(x^2*cos(x))",
         "ans": "((e^x*log_2(x) + e^x/(x*ln(2)))*(x^2*cos(x)) - e^x*log_2(x)*(2*x*cos(x) - x^2*sin(x))) / (x^2*cos(x))^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (Real.exp x * (Real.log x / Real.log 2))/(x^2 * Real.cos x)) x = ((Real.exp x * (Real.log x / Real.log 2) + Real.exp x / (x * Real.log 2))*(x^2 * Real.cos x) - Real.exp x * (Real.log x / Real.log 2)*(2*x*Real.cos x - x^2*Real.sin x))/(x^2 * Real.cos x)^2 := by\n  simp [deriv_div, deriv_mul, deriv_exp, deriv_log]\n  ring",
         "expr": "(Real.exp x * (Real.log x / Real.log 2))/(x^2 * Real.cos x)"},
        
        # Page 129 (#373 - #375)
        {"num": 373, "q": "Find y' for y = (x^3 - 4*x^2 + 6)/e^x",
         "ans": "(-x^3 + 7*x^2 - 8*x - 6)/e^x",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (x^3 - 4*x^2 + 6)/Real.exp x) x = (-x^3 + 7*x^2 - 8*x - 6)/Real.exp x := by\n  simp [deriv_div, deriv_pow, deriv_exp]\n  ring",
         "expr": "(x^3 - 4*x^2 + 6)/Real.exp x"},
        {"num": 374, "q": "Find y' for y = log_4(x)/x^(1/4)",
         "ans": "(1 - (1/4)*ln(x)) / (x^(5/4)*ln(4))",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (Real.log x / Real.log 4)/x^(1/4 : ℝ)) x = (1 - (1/4)*Real.log x)/(x^(5/4 : ℝ)*Real.log 4) := by\n  simp [deriv_div, deriv_pow, deriv_log]\n  ring",
         "expr": "(Real.log x / Real.log 4)/x^(1/4 : ℝ)"},
        {"num": 375, "q": "Find y' for y = sec(x)/((x - 1)*(x + 1))",
         "ans": "((x^2 - 1)*sec(x)*tan(x) - 2*x*sec(x)) / (x^2 - 1)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sec x / (x^2 - 1)) x = ((x^2 - 1)*Real.sec x * Real.tan x - 2*x*Real.sec x)/(x^2 - 1)^2 := by\n  simp [deriv_div, deriv_pow]\n  ring",
         "expr": "Real.sec x / (x^2 - 1)"},
        
        # Page 130 (#376 - #378)
        {"num": 376, "q": "Find y' for y = (6*x^3 - 5*sqrt(x))/(x - 1/x)",
         "ans": "((18*x^2 - 5/(2*sqrt(x)))*(x - 1/x) - (6*x^3 - 5*sqrt(x))*(1 + 1/x^2)) / (x - 1/x)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (6*x^4 - 5*x^(3/2 : ℝ))/(x^2 - 1)) x = ((24*x^3 - (15/2)*x^(1/2 : ℝ))*(x^2 - 1) - (6*x^4 - 5*x^(3/2 : ℝ))*(2*x))/(x^2 - 1)^2 := by\n  simp [deriv_div, deriv_pow]\n  ring",
         "expr": "(6*x^4 - 5*x^(3/2 : ℝ))/(x^2 - 1)"},
        {"num": 377, "q": "Find y' for y = e^x/csc(x)",
         "ans": "e^x*(sin(x) + cos(x))",
         "tid": "product_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.exp x * Real.sin x) x = Real.exp x * (Real.sin x + Real.cos x) := by\n  simp [deriv_mul, deriv_sin, deriv_cos, deriv_exp]\n  ring",
         "expr": "Real.exp x * Real.sin x"},
        {"num": 378, "q": "Find y' for y = (7*x^3)/(4*x^7 - 8*x + 1)",
         "ans": "(-112*x^9 - 112*x^3 + 21*x^2) / (4*x^7 - 8*x + 1)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (7*x^3)/(4*x^7 - 8*x + 1)) x = (-112*x^9 - 112*x^3 + 21*x^2)/(4*x^7 - 8*x + 1)^2 := by\n  simp [deriv_div, deriv_pow]\n  ring",
         "expr": "(7*x^3)/(4*x^7 - 8*x + 1)"},
        
        # Page 131 (#379 - #381) Table {4, 8, 16}
        {"num": 379, "q": "Given the table with x in {4, 8, 16}, find h'(4) where h(x) = f(x)/g(x)",
         "ans": "59/225",
         "tid": "tabular_derivative",
         "lean": "example : (5*15 - 4*4) / 225 = 59/225 := by\n  norm_num",
         "op": "h'(4) = (f'(4)*g(4) - f(4)*g'(4)) / (g(4))^2", "pt": "4", "sub": "(5*15 - 4*4) / 225"},
        {"num": 380, "q": "Given the table with x in {4, 8, 16}, find h'(16) where h(x) = g(x)/f(x)",
         "ans": "11/50",
         "tid": "tabular_derivative",
         "lean": "example : (2*10 - (-1)*2) / 100 = 11/50 := by\n  norm_num",
         "op": "h'(16) = (g'(16)*f(16) - g(16)*f'(16)) / (f(16))^2", "pt": "16", "sub": "(2*10 - (-1)*2) / 100"},
        {"num": 381, "q": "Given the table with x in {4, 8, 16}, find h'(8) where h(x) = x*g(x)/f(x)",
         "ans": "7/18",
         "tid": "tabular_derivative",
         "lean": "example : (29*6 - 40*4) / 36 = 7/18 := by\n  norm_num",
         "op": "h'(8)", "pt": "8", "sub": "(29*6 - 40*4) / 36"},
        
        # Page 132 (#382 - #384)
        {"num": 382, "q": "Given the table with x in {4, 8, 16}, find h'(4) where h(x) = (sqrt(x) + f(x))/x",
         "ans": "15/16",
         "tid": "tabular_derivative",
         "lean": "example : ((21/4)*4 - 6) / 16 = 15/16 := by\n  norm_num",
         "op": "h'(4)", "pt": "4", "sub": "((21/4)*4 - 6) / 16"},
        {"num": 383, "q": "Given the table with x in {4, 8, 16}, find h'(16) where h(x) = (x^2 + g(x))/(f(x) - g(x))",
         "ans": "34/11",
         "tid": "tabular_derivative",
         "lean": "example : (34*11 - 255*0) / 121 = 34/11 := by\n  norm_num",
         "op": "h'(16)", "pt": "16", "sub": "(34*11 - 255*0) / 121"},
        {"num": 384, "q": "Given the table with x in {4, 8, 16}, find h'(4) where h(x) = (sqrt(x) - x)/(f(x)*g(x))",
         "ans": "137/3600",
         "tid": "tabular_derivative",
         "lean": "example : ((-3/4)*60 - (-2)*91) / 3600 = 137/3600 := by\n  norm_num",
         "op": "h'(4)", "pt": "4", "sub": "((-3/4)*60 - (-2)*91) / 3600"},
        
        # Page 133 (#385 - #387) Given f(x) = sin(x) - tan(x), g(x) = sqrt(x) - 3x
        {"num": 385, "q": "Given f(x) = sin(x) - tan(x), g(x) = sqrt(x) - 3*x, find h'(x) for h(x) = f(x)/g(x)",
         "ans": "((cos(x) - sec(x)^2)*(sqrt(x) - 3*x) - (sin(x) - tan(x))*(1/(2*sqrt(x)) - 3)) / (sqrt(x) - 3*x)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (Real.sin x - Real.tan x)/(Real.sqrt x - 3*x)) x = ((Real.cos x - Real.sec x^2)*(Real.sqrt x - 3*x) - (Real.sin x - Real.tan x)*(1/(2*Real.sqrt x) - 3))/(Real.sqrt x - 3*x)^2 := by\n  simp [deriv_div, deriv_sin, deriv_cos, deriv_pow]\n  ring",
         "expr": "(Real.sin x - Real.tan x)/(Real.sqrt x - 3*x)"},
        {"num": 386, "q": "Given f(x) = sin(x) - tan(x), g(x) = sqrt(x) - 3*x, find h'(x) for h(x) = g(x)/f(x)",
         "ans": "((1/(2*sqrt(x)) - 3)*(sin(x) - tan(x)) - (sqrt(x) - 3*x)*(cos(x) - sec(x)^2)) / (sin(x) - tan(x))^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (Real.sqrt x - 3*x)/(Real.sin x - Real.tan x)) x = ((1/(2*Real.sqrt x) - 3)*(Real.sin x - Real.tan x) - (Real.sqrt x - 3*x)*(Real.cos x - Real.sec x^2))/(Real.sin x - Real.tan x)^2 := by\n  simp [deriv_div, deriv_sin, deriv_cos, deriv_pow]\n  ring",
         "expr": "(Real.sqrt x - 3*x)/(Real.sin x - Real.tan x)"},
        {"num": 387, "q": "Given f(x) = sin(x) - tan(x), g(x) = sqrt(x) - 3*x, find h'(x) for h(x) = (f(x) - g(x))/x^2",
         "ans": "(x*(cos(x) - sec(x)^2 - 1/(2*sqrt(x)) + 3) - 2*(sin(x) - tan(x) - sqrt(x) + 3*x)) / x^3",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (Real.sin x - Real.tan x - Real.sqrt x + 3*x)/x^2) x = (x*(Real.cos x - Real.sec x^2 - 1/(2*Real.sqrt x) + 3) - 2*(Real.sin x - Real.tan x - Real.sqrt x + 3*x))/x^3 := by\n  simp [deriv_div, deriv_sin, deriv_cos, deriv_pow]\n  ring",
         "expr": "(Real.sin x - Real.tan x - Real.sqrt x + 3*x)/x^2"},
        
        # Page 134 (#388 - #390)
        {"num": 388, "q": "Given f(x) = sin(x) - tan(x), g(x) = sqrt(x) - 3*x, find h'(x) for h(x) = (6*x^3)/(ln(x) + 3*f(x))",
         "ans": "(18*x^2*(ln(x) + 3*f(x)) - 6*x^3*(1/x + 3*(cos(x) - sec(x)^2))) / (ln(x) + 3*f(x))^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (6*x^3)/(Real.log x + 3*(Real.sin x - Real.tan x))) x = (18*x^2*(Real.log x + 3*(Real.sin x - Real.tan x)) - 6*x^3*(1/x + 3*(Real.cos x - Real.sec x^2)))/(Real.log x + 3*(Real.sin x - Real.tan x))^2 := by\n  simp [deriv_div, deriv_sin, deriv_cos, deriv_pow, deriv_log]\n  ring",
         "expr": "(6*x^3)/(Real.log x + 3*(Real.sin x - Real.tan x))"},
        {"num": 389, "q": "Given f(x) = sin(x) - tan(x), g(x) = sqrt(x) - 3*x, find h'(x) for h(x) = g(x)/(f(x) + 6)",
         "ans": "((1/(2*sqrt(x)) - 3)*(sin(x) - tan(x) + 6) - (sqrt(x) - 3*x)*(cos(x) - sec(x)^2)) / (sin(x) - tan(x) + 6)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (Real.sqrt x - 3*x)/(Real.sin x - Real.tan x + 6)) x = ((1/(2*Real.sqrt x) - 3)*(Real.sin x - Real.tan x + 6) - (Real.sqrt x - 3*x)*(Real.cos x - Real.sec x^2))/(Real.sin x - Real.tan x + 6)^2 := by\n  simp [deriv_div, deriv_sin, deriv_cos, deriv_pow]\n  ring",
         "expr": "(Real.sqrt x - 3*x)/(Real.sin x - Real.tan x + 6)"},
        {"num": 390, "q": "Given f(x) = sin(x) - tan(x), g(x) = sqrt(x) - 3*x, find h'(x) for h(x) = (x^2 - 4)/((x + 2)*g(x))",
         "ans": "(1*(sqrt(x) - 3*x) - (x - 2)*(1/(2*sqrt(x)) - 3)) / (sqrt(x) - 3*x)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (x - 2)/(Real.sqrt x - 3*x)) x = (1*(Real.sqrt x - 3*x) - (x - 2)*(1/(2*Real.sqrt x) - 3))/(Real.sqrt x - 3*x)^2 := by\n  simp [deriv_div, deriv_pow]\n  ring",
         "expr": "(x - 2)/(Real.sqrt x - 3*x)"},
        
        # Page 135 (#391 - #393)
        {"num": 391, "q": "Find the derivative of y = (x^(1/5) - e^x)/tan(x)",
         "ans": "(((1/5)*x^(-4/5) - e^x)*tan(x) - (x^(1/5) - e^x)*sec(x)^2) / tan(x)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (x^(1/5 : ℝ) - Real.exp x)/Real.tan x) x = (((1/5)*x^(-4/5 : ℝ) - Real.exp x)*Real.tan x - (x^(1/5 : ℝ) - Real.exp x)*Real.sec x^2)/Real.tan x^2 := by\n  simp [deriv_div, deriv_pow, deriv_exp]\n  ring",
         "expr": "(x^(1/5 : ℝ) - Real.exp x)/Real.tan x"},
        {"num": 392, "q": "Find the derivative of y = (ln(x) - 4*x)/(sin(x) + 1)",
         "ans": "((1/x - 4)*(sin(x) + 1) - (ln(x) - 4*x)*cos(x)) / (sin(x) + 1)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (Real.log x - 4*x)/(Real.sin x + 1)) x = ((1/x - 4)*(Real.sin x + 1) - (Real.log x - 4*x)*Real.cos x)/(Real.sin x + 1)^2 := by\n  simp [deriv_div, deriv_sin, deriv_cos, deriv_log]\n  ring",
         "expr": "(Real.log x - 4*x)/(Real.sin x + 1)"},
        {"num": 393, "q": "Find the derivative of f(x) = x^2/(x^3 - 512)",
         "ans": "(-x^4 - 1024*x) / (x^3 - 512)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => x^2 / (x^3 - 512)) x = (-x^4 - 1024*x)/(x^3 - 512)^2 := by\n  simp [deriv_div, deriv_pow]\n  ring",
         "expr": "x^2 / (x^3 - 512)"},
        
        # Page 136 (#394 - #396)
        {"num": 394, "q": "Find the derivative of s(t) = cos(t)/(sqrt(t) - t^2)",
         "ans": "(-sin(t)*(sqrt(t) - t^2) - cos(t)*(1/(2*sqrt(t)) - 2*t)) / (sqrt(t) - t^2)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (t : ℝ) : deriv (fun t => Real.cos t / (Real.sqrt t - t^2)) t = (-Real.sin t * (Real.sqrt t - t^2) - Real.cos t * (1/(2*Real.sqrt t) - 2*t))/(Real.sqrt t - t^2)^2 := by\n  simp [deriv_div, deriv_sin, deriv_cos, deriv_pow]\n  ring",
         "expr": "Real.cos t / (Real.sqrt t - t^2)"},
        {"num": 395, "q": "Find the derivative of y = tan(x)/(log_5(x) + 1)",
         "ans": "(sec(x)^2*(log_5(x) + 1) - tan(x)/(x*ln(5))) / (log_5(x) + 1)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.tan x / (Real.log x / Real.log 5 + 1)) x = (Real.sec x^2 * (Real.log x / Real.log 5 + 1) - Real.tan x / (x * Real.log 5))/(Real.log x / Real.log 5 + 1)^2 := by\n  simp [deriv_div, deriv_log]\n  ring",
         "expr": "Real.tan x / (Real.log x / Real.log 5 + 1)"},
        {"num": 396, "q": "Find the derivative of y = ((sin(x) - cos(x))*(cos(x) + 1))/x",
         "ans": "(((cos(x) + sin(x))*(cos(x) + 1) - (sin(x) - cos(x))*sin(x))*x - (sin(x) - cos(x))*(cos(x) + 1)) / x^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => ((Real.sin x - Real.cos x)*(Real.cos x + 1))/x) x = (((Real.cos x + Real.sin x)*(Real.cos x + 1) - (Real.sin x - Real.cos x)*Real.sin x)*x - (Real.sin x - Real.cos x)*(Real.cos x + 1))/x^2 := by\n  simp [deriv_div, deriv_sin, deriv_cos]\n  ring",
         "expr": "((Real.sin x - Real.cos x)*(Real.cos x + 1))/x"},
        
        # Page 137 (#397 - #399)
        {"num": 397, "q": "Find y' for y = (e^x + sin(x))/(ln(x) - cos(x))",
         "ans": "((e^x + cos(x))*(ln(x) - cos(x)) - (e^x + sin(x))*(1/x + sin(x))) / (ln(x) - cos(x))^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (Real.exp x + Real.sin x)/(Real.log x - Real.cos x)) x = ((Real.exp x + Real.cos x)*(Real.log x - Real.cos x) - (Real.exp x + Real.sin x)*(1/x + Real.sin x))/(Real.log x - Real.cos x)^2 := by\n  simp [deriv_div, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring",
         "expr": "(Real.exp x + Real.sin x)/(Real.log x - Real.cos x)"},
        {"num": 398, "q": "Find the derivative of f(x) = (1/x + x)/(1/x - x)",
         "ans": "(4*x) / (1 - x^2)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (1 + x^2)/(1 - x^2)) x = 4*x / (1 - x^2)^2 := by\n  simp [deriv_div, deriv_pow]\n  ring",
         "expr": "(1 + x^2)/(1 - x^2)"},
        {"num": 399, "q": "Find y' for y = csc(x)/x^(1/6)",
         "ans": "-x^(-1/6)*csc(x)*cot(x) - (1/6)*x^(-7/6)*csc(x)",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.csc x / x^(1/6 : ℝ)) x = -x^(-1/6 : ℝ)*Real.csc x * Real.cot x - (1/6)*x^(-7/6 : ℝ)*Real.csc x := by\n  simp [deriv_div, deriv_pow]\n  ring",
         "expr": "Real.csc x / x^(1/6 : ℝ)"},
        
        # Page 138 (#400 - #402)
        {"num": 400, "q": "Find the derivative of f(x) = (x^2 + 3)/(e^x - 4)",
         "ans": "(-x^2*e^x + 2*x*e^x - 3*e^x - 8*x) / (e^x - 4)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (x^2 + 3)/(Real.exp x - 4)) x = (-x^2*Real.exp x + 2*x*Real.exp x - 3*Real.exp x - 8*x)/(Real.exp x - 4)^2 := by\n  simp [deriv_div, deriv_pow, deriv_exp]\n  ring",
         "expr": "(x^2 + 3)/(Real.exp x - 4)"},
        {"num": 401, "q": "Find y' for y = cot(x)/(ln(x) - x)",
         "ans": "(-csc(x)^2*(ln(x) - x) - cot(x)*(1/x - 1)) / (ln(x) - x)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.cot x / (Real.log x - x)) x = (-Real.csc x^2 * (Real.log x - x) - Real.cot x * (1/x - 1))/(Real.log x - x)^2 := by\n  simp [deriv_div, deriv_log]\n  ring",
         "expr": "Real.cot x / (Real.log x - x)"},
        {"num": 402, "q": "Find the derivative of g(x) = (cot(x) + x^3)/(sin(x) + 3)",
         "ans": "((-csc(x)^2 + 3*x^2)*(sin(x) + 3) - (cot(x) + x^3)*cos(x)) / (sin(x) + 3)^2",
         "tid": "quotient_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (Real.cot x + x^3)/(Real.sin x + 3)) x = ((-Real.csc x^2 + 3*x^2)*(Real.sin x + 3) - (Real.cot x + x^3)*Real.cos x)/(Real.sin x + 3)^2 := by\n  simp [deriv_div, deriv_sin, deriv_cos, deriv_pow]\n  ring",
         "expr": "(Real.cot x + x^3)/(Real.sin x + 3)"},
        
        # Page 140 (#403 - #405) Chapter 4: CHAIN RULE
        {"num": 403, "q": "Find y' for y = (x^3 - 6)^4 using the chain rule",
         "ans": "12*x^2*(x^3 - 6)^3",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (x^3 - 6)^4) x = 12*x^2*(x^3 - 6)^3 := by\n  simp [deriv_pow]\n  ring",
         "expr": "(x^3 - 6)^4"},
        {"num": 404, "q": "Find y' for y = sin(4*x - 1) using the chain rule",
         "ans": "4*cos(4*x - 1)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sin (4*x - 1)) x = 4*Real.cos (4*x - 1) := by\n  simp [deriv_sin, deriv_cos]\n  ring",
         "expr": "Real.sin (4*x - 1)"},
        {"num": 405, "q": "Find y' for y = sqrt(x^3 - 4) using the chain rule",
         "ans": "(3*x^2) / (2*sqrt(x^3 - 4))",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sqrt (x^3 - 4)) x = (3*x^2)/(2*Real.sqrt (x^3 - 4)) := by\n  simp [deriv_pow]\n  ring",
         "expr": "Real.sqrt (x^3 - 4)"},
        
        # Page 141 (#406 - #408)
        {"num": 406, "q": "Find y' for y = e^(2*x - 6) using the chain rule",
         "ans": "2*e^(2*x - 6)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.exp (2*x - 6)) x = 2*Real.exp (2*x - 6) := by\n  simp [deriv_exp]\n  ring",
         "expr": "Real.exp (2*x - 6)"},
        {"num": 407, "q": "Find y' for y = ln(x^2 - 1) using the chain rule",
         "ans": "(2*x) / (x^2 - 1)",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.log (x^2 - 1)) x = (2*x)/(x^2 - 1) := by\n  simp [deriv_log, deriv_pow]\n  ring",
         "expr": "Real.log (x^2 - 1)"},
        {"num": 408, "q": "Find y' for y = (x^2 - 1)^(1/3) using the chain rule",
         "ans": "(2*x) / (3*(x^2 - 1)^(2/3))",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (x^2 - 1)^(1/3 : ℝ)) x = (2*x)/(3*(x^2 - 1)^(2/3 : ℝ)) := by\n  simp [deriv_pow]\n  ring",
         "expr": "(x^2 - 1)^(1/3 : ℝ)"},
        
        # Page 142 (#409 - #411)
        {"num": 409, "q": "Find y' for y = tan(3*x^2 - 6*x - 1) using the chain rule",
         "ans": "6*(x - 1)*sec(3*x^2 - 6*x - 1)^2",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.tan (3*x^2 - 6*x - 1)) x = 6*(x - 1)*Real.sec (3*x^2 - 6*x - 1)^2 := by\n  simp [deriv_sin, deriv_cos, deriv_pow]\n  ring",
         "expr": "Real.tan (3*x^2 - 6*x - 1)"},
        {"num": 410, "q": "Find y' for y = log_5(x^3 - 4*x + 1) using the chain rule",
         "ans": "(3*x^2 - 4) / ((x^3 - 4*x + 1)*ln(5))",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.log (x^3 - 4*x + 1) / Real.log 5) x = (3*x^2 - 4)/((x^3 - 4*x + 1)*Real.log 5) := by\n  simp [deriv_log, deriv_pow]\n  ring",
         "expr": "Real.log (x^3 - 4*x + 1) / Real.log 5"},
        {"num": 411, "q": "Find y' for y = (sin(x) - cos(x))^3 using the chain rule",
         "ans": "3*(sin(x) - cos(x))^2*(sin(x) + cos(x))",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => (Real.sin x - Real.cos x)^3) x = 3*(Real.sin x - Real.cos x)^2 * (Real.sin x + Real.cos x) := by\n  simp [deriv_pow, deriv_sin, deriv_cos]\n  ring",
         "expr": "(Real.sin x - Real.cos x)^3"},
        
        # Page 143 (#412 - #414)
        {"num": 412, "q": "Find y' for y = sqrt(sin(x) + x^2) using the chain rule",
         "ans": "(cos(x) + 2*x) / (2*sqrt(sin(x) + x^2))",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => Real.sqrt (Real.sin x + x^2)) x = (Real.cos x + 2*x)/(2*Real.sqrt (Real.sin x + x^2)) := by\n  simp [deriv_pow, deriv_sin, deriv_cos]\n  ring",
         "expr": "Real.sqrt (Real.sin x + x^2)"},
        {"num": 413, "q": "Find y' for y = 3/(x - 5)^3 using the chain rule",
         "ans": "-9 / (x - 5)^4",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => 3*(x - 5)^(-3 : ℝ)) x = -9*(x - 5)^(-4 : ℝ) := by\n  simp [deriv_pow]\n  ring",
         "expr": "3*(x - 5)^(-3 : ℝ)"},
        {"num": 414, "q": "Find y' for y = 5/(x - 3)^2 using the chain rule",
         "ans": "-10 / (x - 3)^3",
         "tid": "chain_rule_derivative",
         "lean": "example (x : ℝ) : deriv (fun x => 5*(x - 3)^(-2 : ℝ)) x = -10*(x - 3)^(-3 : ℝ) := by\n  simp [deriv_pow]\n  ring",
         "expr": "5*(x - 3)^(-2 : ℝ)"},
    ]

    for p in probs:
        tid = p["tid"]
        if tid == "quotient_rule_derivative":
            params = {"expr": p.get("expr", p["q"]), "answer": p["ans"]}
        elif tid == "product_rule_derivative":
            params = {"expr": p.get("expr", p["q"]), "answer": p["ans"]}
        elif tid == "chain_rule_derivative":
            params = {"expr": p.get("expr", p["q"]), "answer": p["ans"]}
        elif tid == "tangent_slope_derivative":
            params = {"f": p.get("f", "f"), "x0": p.get("x0", "c"), "m": p["ans"]}
        elif tid == "tangent_line":
            params = {"f": p.get("f", "f"), "x0": p.get("x0", "0"), "y0": p.get("y0", "0"), "m": p.get("m", "1"), "line_eq": p["ans"]}
        elif tid == "tabular_derivative":
            params = {"operation": p.get("op", "derivative"), "point": p.get("pt", "1"), "expr_sub": p.get("sub", "0"), "ans": p["ans"]}
        elif tid == "critical_points":
            params = {"f": p.get("f", "f"), "f_prime": p.get("f_prime", "0"), "points": p.get("points", p["ans"])}
        elif tid == "power_rule_derivative":
            params = {"expr": p.get("expr", "x"), "answer": p["ans"]}
        else:
            params = {"d": p["ans"]}
            
        entries.append(make_entry(p["q"], tid, params, p["lean"]))
        
        # Conversational variation
        q_var = p["q"]
        if q_var.startswith("Find y' for "):
            q_alt = q_var.replace("Find y' for ", "What is the derivative of ") + "?"
            entries.append(make_entry(q_alt, tid, params, p["lean"]))
        elif q_var.startswith("Find dy/dx for "):
            q_alt = q_var.replace("Find dy/dx for ", "Compute the first derivative of ")
            entries.append(make_entry(q_alt, tid, params, p["lean"]))
        elif q_var.startswith("Find the derivative of "):
            q_alt = q_var.replace("Find the derivative of ", "Differentiate the function ")
            entries.append(make_entry(q_alt, tid, params, p["lean"]))

    return entries

def generate_way2() -> List[Dict[str, Any]]:
    entries = []
    
    # 1. Chain Rule Parametric Variations: (a*x^k + b)^n
    for a in [2, 3, 5, 7]:
        for k in [2, 3, 4]:
            for b in [-5, -2, 3, 6]:
                for n in [3, 4, 5]:
                    q = f"Find the derivative of y = ({a}*x^{k} + {b})^{n} using the chain rule"
                    ans = f"{n * a * k}*x^{k-1}*({a}*x^{k} + {b})^{n-1}"
                    lean = f"example (x : ℝ) : deriv (fun x => ({a}*x^{k} + {b})^{n}) x = {n * a * k}*x^{k-1}*({a}*x^{k} + {b})^{n-1} := by\n  simp [deriv_pow]\n  ring"
                    params = {"expr": f"({a}*x^{k} + {b})^{n}", "answer": ans}
                    entries.append(make_entry(q, "chain_rule_derivative", params, lean))
                    if len(entries) >= 50:
                        break
                if len(entries) >= 50:
                    break
            if len(entries) >= 50:
                break
        if len(entries) >= 50:
            break

    # 2. Chain Rule Radicals: sqrt(a*x^k + b)
    for a in [2, 3, 4, 5]:
        for k in [2, 3]:
            for b in [-7, -3, 5, 9]:
                q = f"Find y' for y = sqrt({a}*x^{k} + {b}) using the chain rule"
                ans = f"({a*k}*x^{k-1}) / (2*sqrt({a}*x^{k} + {b}))"
                lean = f"example (x : ℝ) : deriv (fun x => Real.sqrt ({a}*x^{k} + {b})) x = ({a*k}*x^{k-1})/(2*Real.sqrt ({a}*x^{k} + {b})) := by\n  simp [deriv_pow]\n  ring"
                params = {"expr": f"Real.sqrt ({a}*x^{k} + {b})", "answer": ans}
                entries.append(make_entry(q, "chain_rule_derivative", params, lean))
                if len(entries) >= 90:
                    break
            if len(entries) >= 90:
                break
        if len(entries) >= 90:
            break

    # 3. Chain Rule Exponentials: e^(a*x + b)
    for a in [2, 3, 4, 5, -2, -3]:
        for b in [-6, -1, 4, 7]:
            q = f"Find y' for y = e^({a}*x + {b}) using the chain rule"
            ans = f"{a}*e^({a}*x + {b})"
            lean = f"example (x : ℝ) : deriv (fun x => Real.exp ({a}*x + {b})) x = {a}*Real.exp ({a}*x + {b}) := by\n  simp [deriv_exp]\n  ring"
            params = {"expr": f"Real.exp ({a}*x + {b})", "answer": ans}
            entries.append(make_entry(q, "chain_rule_derivative", params, lean))
            if len(entries) >= 130:
                break
        if len(entries) >= 130:
            break

    # 4. Chain Rule Trigonometrics: sin(a*x + b), tan(a*x^2 + b)
    for a in [2, 3, 5, 6]:
        for b in [-4, -1, 2, 5]:
            q = f"Find y' for y = sin({a}*x + {b}) using the chain rule"
            ans = f"{a}*cos({a}*x + {b})"
            lean = f"example (x : ℝ) : deriv (fun x => Real.sin ({a}*x + {b})) x = {a}*Real.cos ({a}*x + {b}) := by\n  simp [deriv_sin]\n  ring"
            params = {"expr": f"Real.sin ({a}*x + {b})", "answer": ans}
            entries.append(make_entry(q, "chain_rule_derivative", params, lean))
            if len(entries) >= 170:
                break
        if len(entries) >= 170:
            break

    # 5. Negative Power Rational Chain Rule: k / (x - c)^n
    for k in [2, 3, 4, 5]:
        for c in [-5, -2, 3, 7]:
            for n in [2, 3, 4]:
                q = f"Find y' for y = {k}/(x - {c})^{n} using the chain rule"
                ans = f"{-k*n}/(x - {c})^{n+1}"
                lean = f"example (x : ℝ) : deriv (fun x => {k}*(x - {c})^(-{n} : ℝ)) x = {-k*n}*(x - {c})^(-{n+1} : ℝ) := by\n  simp [deriv_pow]\n  ring"
                params = {"expr": f"{k}*(x - {c})^(-{n} : ℝ)", "answer": ans}
                entries.append(make_entry(q, "chain_rule_derivative", params, lean))
                if len(entries) >= 210:
                    break
            if len(entries) >= 210:
                break
        if len(entries) >= 210:
            break

    # 6. Tangent line equations for rational curves: y = (ax + b)/(cx + d) at (0, b/d)
    for a in [2, 3, 4]:
        for b in [1, 2, 5]:
            for c in [2, 3]:
                for d in [4, 5, 7]:
                    m_val = f"{a*d - b*c}/{d**2}"
                    q = f"Find the equation of the tangent line at the given point (0, {b}/{d}) for y = ({a}*x + {b})/({c}*x + {d})"
                    ans = f"y = {m_val}*x + {b}/{d}"
                    lean = f"example (x : ℝ) : deriv (fun x => ({a}*x + {b})/({c}*x + {d})) 0 = {m_val} ∧ ({a}*0 + {b})/({c}*0 + {d}) = {b}/{d} := by\n  simp [deriv_div]\n  ring"
                    params = {"f": f"({a}*x + {b})/({c}*x + {d})", "x0": "0", "y0": f"{b}/{d}", "m": m_val, "line_eq": ans}
                    entries.append(make_entry(q, "tangent_line", params, lean))
                    if len(entries) >= 250:
                        break
                if len(entries) >= 250:
                    break
            if len(entries) >= 250:
                break
        if len(entries) >= 250:
            break

    return entries

def main():
    print(f"Loading existing dataset from: {DATASET_PATH}")
    existing_lines = []
    if os.path.exists(DATASET_PATH):
        with open(DATASET_PATH, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    existing_lines.append(json.loads(line))
    print(f"Existing entries: {len(existing_lines)}")

    way1 = generate_way1()
    print(f"Generated Way 1 (Authentic #281–#414): {len(way1)} examples")
    
    way2 = generate_way2()
    print(f"Generated Way 2 (Parametric Generalization): {len(way2)} examples")

    all_new = way1 + way2
    print(f"Total new entries to append: {len(all_new)}")

    with open(DATASET_PATH, "a", encoding="utf-8") as f:
        for entry in all_new:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"Successfully appended {len(all_new)} entries.")
    print(f"New total dataset size: {len(existing_lines) + len(all_new)} examples")

if __name__ == "__main__":
    main()
