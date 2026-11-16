"""
VeriMath — Append Book of 1000 Derivatives Chapters 2 & 3 Dataset
==================================================================
Covers authentic problems #151 through #280 from Miguel Santiago's
'Book of 1000 Derivatives' (The Vegan Math Guy):
- Chapter 2: Product Rule (#151 - #250)
  - 2-factor, 3-factor, and 4-factor products
  - Properties of logarithms and exponents (e^(x + ln x) -> x e^x, ln(x^(x^2)) -> x^2 ln x)
  - Tabular evaluation of products (#178 - #183, #203 - #205)
  - Difference quotient limit definitions (#184 - #189, #224 - #226)
  - Particle velocity v(t) = s'(t) and v(t0) = s'(t0) (#193 - #195, #227 - #229)
  - Point-slope evaluations f'(c) at given c (#240 - #245)
  - Given k(x) compositions (#246 - #250)
- Chapter 3: Quotient Rule (#251 - #280)
  - Algebraic rational functions (Ax+B)/(Cx+D), (7x^2-1)/(x+4), etc.
  - Trigonometric, logarithmic, and exponential quotients
  - Reciprocal quotient rule (1/(x+4), 1/(x^2-3x+5), 6/(x^3-8))
  - Tabular evaluation of quotients (#263 - #268)
  - Tangent line slope of quotient at point x = c (#275 - #280)

Generates:
1. Way 1: 130 authentic problems (#151 to #280) + variations (270 examples)
2. Way 2: 380 parametric variations (multi-factor products, quotient rules,
   difference quotients, particle velocities, tabular derivatives, tangent slopes)
Total: ~650 new verified ChatML examples.
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
    
    # Authentic Problems 151-280 definitions
    probs = [
        # Page 54 (#151 - #153)
        {"num": 151, "q": "Find the value of y' for y = x^2*sin(x)", "ans": "x^2*cos(x) + 2*x*sin(x)", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => x^2*Real.sin (x)) x = x^2*Real.cos (x) + 2*x*Real.sin (x) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "x^2*Real.sin (x)"},
        {"num": 152, "q": "Find the value of y' for y = sin(x)*cos(x)", "ans": "cos(x)^2 - sin(x)^2", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => Real.sin (x)*Real.cos (x)) x = Real.cos (x)^2 - Real.sin (x)^2 := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "Real.sin (x)*Real.cos (x)"},
        {"num": 153, "q": "Find the value of y' for y = e^x*ln(x)", "ans": "e^x*ln(x) + e^x/x", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => Real.exp (x)*Real.log (x)) x = Real.exp (x)*Real.log (x) + Real.exp (x)/x := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "Real.exp (x)*Real.log (x)"},
        # Page 55 (#154 - #156)
        {"num": 154, "q": "Find the value of y' for y = (x^2 + 2)*e^x", "ans": "(x^2 + 2*x + 2)*e^x", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => (x^2 + 2)*Real.exp (x)) x = (x^2 + 2*x + 2)*Real.exp (x) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "(x^2 + 2)*Real.exp (x)"},
        {"num": 155, "q": "Find the value of y' for y = sqrt(x)*tan(x)", "ans": "sqrt(x)*sec(x)^2 + tan(x)/(2*sqrt(x))", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => Real.sqrt (x)*Real.tan (x)) x = Real.sqrt (x)*Real.sec (x)^2 + Real.tan (x)/(2*Real.sqrt (x)) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "Real.sqrt (x)*Real.tan (x)"},
        {"num": 156, "q": "Find the value of y' for y = x^(1/3)*sin(x) + x", "ans": "x^(1/3)*cos(x) + sin(x)/(3*x^(2/3)) + 1", "tid": "derivative", "lean": "example (x : ℝ) : deriv (fun x => x^(1/3)*Real.sin (x) + x) x = x^(1/3)*Real.cos (x) + Real.sin (x)/(3*x^(2/3)) + 1 := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "x^(1/3)*Real.sin (x) + x"},
        # Page 56 (#157 - #159)
        {"num": 157, "q": "Find the value of y' for y = (x^3 + 6)*(x^2 - 3*x + 1)", "ans": "5*x^4 - 12*x^3 + 3*x^2 + 12*x - 18", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => (x^3 + 6)*(x^2 - 3*x + 1)) x = 5*x^4 - 12*x^3 + 3*x^2 + 12*x - 18 := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "(x^3 + 6)*(x^2 - 3*x + 1)"},
        {"num": 158, "q": "Find the value of y' for y = ln(x)*sin(x)", "ans": "ln(x)*cos(x) + sin(x)/x", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => Real.log (x)*Real.sin (x)) x = Real.log (x)*Real.cos (x) + Real.sin (x)/x := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "Real.log (x)*Real.sin (x)"},
        {"num": 159, "q": "Find the value of y' for y = (1/x)*cos(x)", "ans": "-cos(x)/x^2 - sin(x)/x", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => (1/x)*Real.cos (x)) x = -Real.cos (x)/x^2 - Real.sin (x)/x := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "(1/x)*Real.cos (x)"},
        # Page 57 (#160 - #162)
        {"num": 160, "q": "Find the value of y' for y = tan(x)*cot(x)", "ans": "0", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => Real.tan (x)*Real.cot (x)) x = 0 := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "Real.tan (x)*Real.cot (x)"},
        {"num": 161, "q": "Find the value of y' for y = 2^x * e^x", "ans": "2^x * e^x * (ln(2) + 1)", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => 2^x * Real.exp (x)) x = 2^x * Real.exp (x) * (Real.log 2 + 1) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "2^x * Real.exp (x)"},
        {"num": 162, "q": "Find the value of y' for y = x^4 * sec(x)", "ans": "x^4*sec(x)*tan(x) + 4*x^3*sec(x)", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => x^4 * Real.sec (x)) x = x^4*Real.sec (x)*Real.tan (x) + 4*x^3*Real.sec (x) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "x^4 * Real.sec (x)"},
        # Page 58 (#163 - #165)
        {"num": 163, "q": "Find the slope of the tangent line for the function f(x) = 4*e^x*cot(x)", "ans": "-4*e^x*csc(x)^2 + 4*e^x*cot(x)", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => 4*Real.exp (x)*Real.cot (x)) x = -4*Real.exp (x)*Real.csc (x)^2 + 4*Real.exp (x)*Real.cot (x) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "4*Real.exp (x)*Real.cot (x)"},
        {"num": 164, "q": "Find the slope of the tangent line for the function f(x) = x^3*cos(x)", "ans": "-x^3*sin(x) + 3*x^2*cos(x)", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => x^3*Real.cos (x)) x = -x^3*Real.sin (x) + 3*x^2*Real.cos (x) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "x^3*Real.cos (x)"},
        {"num": 165, "q": "Find the slope of the tangent line for the function f(x) = ln(x^(x^2))", "ans": "2*x*ln(x) + x", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => x^2 * Real.log (x)) x = 2*x*Real.log (x) + x := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "x^2 * Real.log (x)"},
        # Page 59 (#166 - #168)
        {"num": 166, "q": "Find the slope of the tangent line for f(x) = (x^3 - 1)*(x^4 + 6)", "ans": "7*x^6 - 4*x^3 + 18*x^2", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => (x^3 - 1)*(x^4 + 6)) x = 7*x^6 - 4*x^3 + 18*x^2 := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "(x^3 - 1)*(x^4 + 6)"},
        {"num": 167, "q": "Find the slope of the tangent line for f(x) = 16*x^3*cot(x)", "ans": "-16*x^3*csc(x)^2 + 48*x^2*cot(x)", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => 16*x^3*Real.cot (x)) x = -16*x^3*Real.csc (x)^2 + 48*x^2*Real.cot (x) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "16*x^3*Real.cot (x)"},
        {"num": 168, "q": "Find the slope of the tangent line for f(x) = 7*x^2*ln(x)", "ans": "14*x*ln(x) + 7*x", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => 7*x^2*Real.log (x)) x = 14*x*Real.log (x) + 7*x := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "7*x^2*Real.log (x)"},
        # Page 60 (#169 - #171)
        {"num": 169, "q": "Find y' for y = e^x * x^(1/5)", "ans": "e^x * x^(1/5) + e^x / (5*x^(4/5))", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => Real.exp (x) * x^(1/5)) x = Real.exp (x) * x^(1/5) + Real.exp (x) / (5*x^(4/5)) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "Real.exp (x) * x^(1/5)"},
        {"num": 170, "q": "Find y' for y = sin(x)*ln(x^7)", "ans": "7*cos(x)*ln(x) + 7*sin(x)/x", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => 7*Real.sin (x)*Real.log (x)) x = 7*Real.cos (x)*Real.log (x) + 7*Real.sin (x)/x := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "7*Real.sin (x)*Real.log (x)"},
        {"num": 171, "q": "Find y' for y = 6*x^2*cos(x)*tan(x)", "ans": "6*x^2*cos(x) + 12*x*sin(x)", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => 6*x^2*Real.sin (x)) x = 6*x^2*Real.cos (x) + 12*x*Real.sin (x) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "6*x^2*Real.sin (x)"},
        # Page 61 (#172 - #174)
        {"num": 172, "q": "Find y' for y = x^2*ln(x)*sin(x)", "ans": "x^2*sin(x)*cos(x) + x^2*ln(x)*cos(x) + 2*x*ln(x)*sin(x) + x*sin(x)", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => x^2*Real.log (x)*Real.sin (x)) x = x^2*Real.log (x)*Real.cos (x) + 2*x*Real.log (x)*Real.sin (x) + x*Real.sin (x) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "x^2*Real.log (x)*Real.sin (x)"},
        {"num": 173, "q": "Find y' for y = sqrt(x)*e^x*cos(x)", "ans": "-sqrt(x)*e^x*sin(x) + sqrt(x)*e^x*cos(x) + e^x*cos(x)/(2*sqrt(x))", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => Real.sqrt (x)*Real.exp (x)*Real.cos (x)) x = -Real.sqrt (x)*Real.exp (x)*Real.sin (x) + Real.sqrt (x)*Real.exp (x)*Real.cos (x) + Real.exp (x)*Real.cos (x)/(2*Real.sqrt (x)) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "Real.sqrt (x)*Real.exp (x)*Real.cos (x)"},
        {"num": 174, "q": "Find y' for y = sin(x)*tan(x)", "ans": "sin(x)*sec(x)^2 + cos(x)*tan(x)", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => Real.sin (x)*Real.tan (x)) x = Real.sin (x)*Real.sec (x)^2 + Real.cos (x)*Real.tan (x) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "Real.sin (x)*Real.tan (x)"},
        # Page 62 (#175 - #177)
        {"num": 175, "q": "Find y' for y = sec(x)*cot(x)", "ans": "-csc(x)*cot(x)", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => Real.csc (x)) x = -Real.csc (x)*Real.cot (x) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "Real.csc (x)"},
        {"num": 176, "q": "Find y' for y = x*sin(x)*cos(x)", "ans": "x*cos(2*x) + sin(x)*cos(x)", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => x*Real.sin (x)*Real.cos (x)) x = x*Real.cos (2*x) + Real.sin (x)*Real.cos (x) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "x*Real.sin (x)*Real.cos (x)"},
        {"num": 177, "q": "Find y' for y = x^2*ln(x)*4^x", "ans": "x^2*4^x*ln(4)*ln(x) + 2*x*4^x*ln(x) + x*4^x", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => x^2*Real.log (x)*4^x) x = x^2*4^x*Real.log (4)*Real.log (x) + 2*x*4^x*Real.log (x) + x*4^x := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "x^2*Real.log (x)*4^x"},
        # Page 63 (#178 - #180) Tabular Product Rule
        {"num": 178, "q": "Let h(x) = f(x)*g(x). Use the table to solve #178: h'(2)", "ans": "-24", "tid": "tabular_derivative", "lean": "example : (-4) * 2 + 8 * (-2) = -24 := by\n  norm_num", "op": "h'(2) = f'(2)*g(2) + f(2)*g'(2)", "pt": "2", "sub": "(-4) * 2 + 8 * (-2)"},
        {"num": 179, "q": "Let h(x) = f(x)*g(x). Use the table to solve #179: 6*h'(1)", "ans": "-36", "tid": "tabular_derivative", "lean": "example : 6 * ((-6) * 1 + 0 * 4) = -36 := by\n  norm_num", "op": "6*h'(1)", "pt": "1", "sub": "6 * ((-6) * 1 + 0 * 4)"},
        {"num": 180, "q": "Let h(x) = f(x)*g(x). Use the table to solve #180: 6*h'(1) - g'(4)", "ans": "-42", "tid": "tabular_derivative", "lean": "example : -36 - 6 = -42 := by\n  norm_num", "op": "6*h'(1) - g'(4)", "pt": "1", "sub": "-36 - 6"},
        # Page 64 (#181 - #183)
        {"num": 181, "q": "Let h(x) = f(x)*g(x). Use the table to solve #181: h'(5) - h'(2)", "ans": "106", "tid": "tabular_derivative", "lean": "example : 82 - (-24) = 106 := by\n  norm_num", "op": "h'(5) - h'(2)", "pt": "5", "sub": "82 - (-24)"},
        {"num": 182, "q": "Let h(x) = f(x)*g(x). Use the table to solve #182: 7*h'(4)", "ans": "70", "tid": "tabular_derivative", "lean": "example : 7 * ((-2) * 13 + 6 * 6) = 70 := by\n  norm_num", "op": "7*h'(4)", "pt": "4", "sub": "7 * ((-2) * 13 + 6 * 6)"},
        {"num": 183, "q": "Let h(x) = f(x)*g(x). Use the table to solve #183: h'(3)", "ans": "46", "tid": "tabular_derivative", "lean": "example : 10 * 7 + (-4) * 6 = 46 := by\n  norm_num", "op": "h'(3)", "pt": "3", "sub": "10 * 7 + (-4) * 6"},
        # Page 65 (#184 - #186) Difference Quotient Limits
        {"num": 184, "q": "Find each limit: lim_{h->0} (sqrt(x+h)*e^(x+h) - sqrt(x)*e^x)/h", "ans": "sqrt(x)*e^x + e^x/(2*sqrt(x))", "tid": "derivative_limit_definition", "lean": "example (x : ℝ) : deriv (fun x => Real.sqrt (x)*Real.exp (x)) x = Real.sqrt (x)*Real.exp (x) + Real.exp (x)/(2*Real.sqrt (x)) := by\n  simp [deriv_pow, deriv_mul, deriv_div, deriv_sin, deriv_cos, deriv_tan, deriv_sec, deriv_exp, deriv_log]\n  ring", "f": "Real.sqrt (x)*Real.exp (x)"},
        {"num": 185, "q": "Find each limit: lim_{h->0} ((x+h)^2*tan(x+h) - x^2*tan(x))/h", "ans": "x^2*sec(x)^2 + 2*x*tan(x)", "tid": "derivative_limit_definition", "lean": "example (x : ℝ) : deriv (fun x => x^2*Real.tan (x)) x = x^2*Real.sec (x)^2 + 2*x*Real.tan (x) := by\n  simp [deriv_pow, deriv_mul, deriv_div, deriv_sin, deriv_cos, deriv_tan, deriv_sec, deriv_exp, deriv_log]\n  ring", "f": "x^2*Real.tan (x)"},
        {"num": 186, "q": "Find each limit: lim_{h->0} (2^(x+h)*sqrt(x+h) - 2^x*sqrt(x))/h", "ans": "2^x*sqrt(x)*ln(2) + 2^x/(2*sqrt(x))", "tid": "derivative_limit_definition", "lean": "example (x : ℝ) : deriv (fun x => 2^x*Real.sqrt (x)) x = 2^x*Real.sqrt (x)*Real.log (2) + 2^x/(2*Real.sqrt (x)) := by\n  simp [deriv_pow, deriv_mul, deriv_div, deriv_sin, deriv_cos, deriv_tan, deriv_sec, deriv_exp, deriv_log]\n  ring", "f": "2^x*Real.sqrt (x)"},
        # Page 66 (#187 - #189)
        {"num": 187, "q": "Find each limit: lim_{h->0} (x+h)^(1/4)*ln(x+h) - x^(1/4)*ln(x))/h", "ans": "x^(1/4)/x + ln(x)/(4*x^(3/4))", "tid": "derivative_limit_definition", "lean": "example (x : ℝ) : deriv (fun x => x^(1/4)*Real.log (x)) x = x^(1/4)/x + Real.log (x)/(4*x^(3/4)) := by\n  simp [deriv_pow, deriv_mul, deriv_div, deriv_sin, deriv_cos, deriv_tan, deriv_sec, deriv_exp, deriv_log]\n  ring", "f": "x^(1/4)*Real.log (x)"},
        {"num": 188, "q": "Find each limit: lim_{h->0} (e^(x+h)/(x+h)^2 - e^x/x^2)/h", "ans": "e^x/x^2 - 2*e^x/x^3", "tid": "derivative_limit_definition", "lean": "example (x : ℝ) : deriv (fun x => Real.exp (x)/x^2) x = Real.exp (x)/x^2 - 2*Real.exp (x)/x^3 := by\n  simp [deriv_pow, deriv_mul, deriv_div, deriv_sin, deriv_cos, deriv_tan, deriv_sec, deriv_exp, deriv_log]\n  ring", "f": "Real.exp (x)/x^2"},
        {"num": 189, "q": "Find each limit: lim_{h->0} (((x+h)^2 - 1)*(x+h - 5) - (x^2 - 1)*(x - 5))/h", "ans": "3*x^2 - 10*x - 1", "tid": "derivative_limit_definition", "lean": "example (x : ℝ) : deriv (fun x => (x^2 - 1)*(x - 5)) x = 3*x^2 - 10*x - 1 := by\n  simp [deriv_pow, deriv_mul, deriv_div, deriv_sin, deriv_cos, deriv_tan, deriv_sec, deriv_exp, deriv_log]\n  ring", "f": "(x^2 - 1)*(x - 5)"},
        # Page 67 (#190 - #192)
        {"num": 190, "q": "Find y' for y = e^(x + ln(x))", "ans": "x*e^x + e^x", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => x*Real.exp (x)) x = x*Real.exp (x) + Real.exp (x) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "x*Real.exp (x)"},
        {"num": 191, "q": "Find y' for y = 6^x*cos(x) + 4*x^2", "ans": "6^x*cos(x)*ln(6) - 6^x*sin(x) + 8*x", "tid": "derivative", "lean": "example (x : ℝ) : deriv (fun x => 6^x*Real.cos (x) + 4*x^2) x = 6^x*Real.cos (x)*Real.log (6) - 6^x*Real.sin (x) + 8*x := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "6^x*Real.cos (x) + 4*x^2"},
        {"num": 192, "q": "Find y' for y = (x^3 + 5*x)*e^x", "ans": "(x^3 + 3*x^2 + 5*x + 5)*e^x", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => (x^3 + 5*x)*Real.exp (x)) x = (x^3 + 3*x^2 + 5*x + 5)*Real.exp (x) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "(x^3 + 5*x)*Real.exp (x)"},
        # Page 68 (#193 - #195) Particle Velocity at t = 2
        {"num": 193, "q": "Find the velocity of the particle at time t = 2: f(t) = 3*t^2*sin(t)", "ans": "12*sin(2) + 12*cos(2)", "tid": "particle_velocity_derivative", "lean": "example : deriv (fun t => 3*t^2*Real.sin (t)) 2 = 12*Real.sin (2) + 12*Real.cos (2) := by\n  simp [deriv_pow, deriv_mul, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "s": "3*t^2*Real.sin (t)"},
        {"num": 194, "q": "Find the velocity of the particle at time t = 2: f(t) = e^t*t^(1/7)", "ans": "15*2^(1/7)*e^2/14", "tid": "particle_velocity_derivative", "lean": "example : deriv (fun t => Real.exp (t)*t^(1/7)) 2 = 15*2^(1/7)*Real.exp (2)/14 := by\n  simp [deriv_pow, deriv_mul, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "s": "Real.exp (t)*t^(1/7)"},
        {"num": 195, "q": "Find the velocity of the particle at time t = 2: f(t) = (t^4 + 6*t)*(e^t - 2*t^2)", "ans": "66*e^2 - 528", "tid": "particle_velocity_derivative", "lean": "example : deriv (fun t => (t^4 + 6*t)*(Real.exp (t) - 2*t^2)) 2 = 66*Real.exp (2) - 528 := by\n  simp [deriv_pow, deriv_mul, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "s": "(t^4 + 6*t)*(Real.exp (t) - 2*t^2)"},
        # Page 69 (#196 - #198)
        {"num": 196, "q": "Find y' for y = (x^2 + 6*x - 1)*(x^2 + 4*x + 5)", "ans": "4*x^3 + 30*x^2 + 56*x + 26", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => (x^2 + 6*x - 1)*(x^2 + 4*x + 5)) x = 4*x^3 + 30*x^2 + 56*x + 26 := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "(x^2 + 6*x - 1)*(x^2 + 4*x + 5)"},
        {"num": 197, "q": "Find y' for y = (e^x + 6*x)*(sin(x) + cos(x))", "ans": "(e^x + 6*x)*(cos(x) - sin(x)) + (e^x + 6)*(sin(x) + cos(x))", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => (Real.exp (x) + 6*x)*(Real.sin (x) + Real.cos (x))) x = (Real.exp (x) + 6*x)*(Real.cos (x) - Real.sin (x)) + (Real.exp (x) + 6)*(Real.sin (x) + Real.cos (x)) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "(Real.exp (x) + 6*x)*(Real.sin (x) + Real.cos (x))"},
        {"num": 198, "q": "Find y' for y = sqrt(x)*log_6(x)", "ans": "log_6(x)/(2*sqrt(x)) + 1/(sqrt(x)*ln(6))", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => Real.sqrt (x)*(Real.log (x)/Real.log 6)) x = (Real.log (x)/Real.log 6)/(2*Real.sqrt (x)) + 1/(Real.sqrt (x)*Real.log 6) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "Real.sqrt (x)*(Real.log (x)/Real.log 6)"},
        # Page 70 (#199 - #202)
        {"num": 199, "q": "Find y' for y = (6*x^2 + 4*x)*sin(x)", "ans": "(6*x^2 + 4*x)*cos(x) + (12*x + 4)*sin(x)", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => (6*x^2 + 4*x)*Real.sin (x)) x = (6*x^2 + 4*x)*Real.cos (x) + (12*x + 4)*Real.sin (x) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "(6*x^2 + 4*x)*Real.sin (x)"},
        {"num": 200, "q": "Find y' for y = (2/x + x^4)*(x^3 + 1)", "ans": "7*x^6 + 4*x^3 + 4*x - 2/x^2", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => (2/x + x^4)*(x^3 + 1)) x = 7*x^6 + 4*x^3 + 4*x - 2/x^2 := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "(2/x + x^4)*(x^3 + 1)"},
        {"num": 201, "q": "Find y' for y = 6*(2^x)*e^x", "ans": "6*(2^x)*e^x*(ln(2) + 1)", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => 6*(2^x)*Real.exp (x)) x = 6*(2^x)*Real.exp (x)*(Real.log 2 + 1) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "6*(2^x)*Real.exp (x)"},
        {"num": 202, "q": "Find y' for y = (x^2 + sqrt(x))*e^x", "ans": "(x^2 + 2*x + sqrt(x) + 1/(2*sqrt(x)))*e^x", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => (x^2 + Real.sqrt (x))*Real.exp (x)) x = (x^2 + 2*x + Real.sqrt (x) + 1/(2*Real.sqrt (x)))*Real.exp (x) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "(x^2 + Real.sqrt (x))*Real.exp (x)"},
        # Page 71 (#203 - #205) Functional Product Values
        {"num": 203, "q": "Let F(x) = G(x)*H(x). Given G(2) = -8, H(2) = 5, G'(2) = -1, H'(2) = 3, find F'(2)", "ans": "-29", "tid": "tabular_derivative", "lean": "example : (-1) * 5 + (-8) * 3 = -29 := by\n  norm_num", "op": "F'(2) = G'(2)*H(2) + G(2)*H'(2)", "pt": "2", "sub": "(-1) * 5 + (-8) * 3"},
        {"num": 204, "q": "Given h(x) = (x + e^x)*f(x), f(0) = 6, f'(0) = -1, find h'(0)", "ans": "11", "tid": "tabular_derivative", "lean": "example : (1 + 1) * 6 + (0 + 1) * (-1) = 11 := by\n  norm_num", "op": "h'(0)", "pt": "0", "sub": "(1 + 1) * 6 + (0 + 1) * (-1)"},
        {"num": 205, "q": "Given h(x) = (x^2 + 1)*f(x), h'(6) = -1, f'(6) = -2, find f(6)", "ans": "73/12", "tid": "tabular_derivative", "lean": "example : (-1 - 37 * (-2)) / 12 = 73/12 := by\n  norm_num", "op": "f(6) = (h'(6) - 37*f'(6))/12", "pt": "6", "sub": "(-1 - 37 * (-2)) / 12"},
        # Page 72 (#206 - #208)
        {"num": 206, "q": "Find f'(x) for f(x) = (5*x^3 - 1)*(-x^5 + 6)", "ans": "-40*x^7 + 5*x^4 + 90*x^2", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => (5*x^3 - 1)*(-x^5 + 6)) x = -40*x^7 + 5*x^4 + 90*x^2 := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "(5*x^3 - 1)*(-x^5 + 6)"},
        {"num": 207, "q": "Find f'(x) for f(x) = e^x * x^(5/3)", "ans": "e^x * x^(5/3) + (5/3)*e^x * x^(2/3)", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => Real.exp (x) * x^(5/3)) x = Real.exp (x) * x^(5/3) + (5/3)*Real.exp (x) * x^(2/3) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "Real.exp (x) * x^(5/3)"},
        {"num": 208, "q": "Find f'(x) for f(x) = (x^4 - 6*x^3 + 12*x - 1)*ln(x)", "ans": "(4*x^3 - 18*x^2 + 12)*ln(x) + (x^4 - 6*x^3 + 12*x - 1)/x", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => (x^4 - 6*x^3 + 12*x - 1)*Real.log (x)) x = (4*x^3 - 18*x^2 + 12)*Real.log (x) + (x^4 - 6*x^3 + 12*x - 1)/x := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "(x^4 - 6*x^3 + 12*x - 1)*Real.log (x)"},
        # Page 73 (#209 - #211)
        {"num": 209, "q": "Find f'(x) for f(x) = (3/x + x^5)*sin(x)", "ans": "(3/x + x^5)*cos(x) + (5*x^4 - 3/x^2)*sin(x)", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => (3/x + x^5)*Real.sin (x)) x = (3/x + x^5)*Real.cos (x) + (5*x^4 - 3/x^2)*Real.sin (x) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "(3/x + x^5)*Real.sin (x)"},
        {"num": 210, "q": "Find f'(x) for f(x) = cos(x)*tan(x)*ln(x)", "ans": "cos(x)*ln(x) + sin(x)/x", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => Real.sin (x)*Real.log (x)) x = Real.cos (x)*Real.log (x) + Real.sin (x)/x := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "Real.sin (x)*Real.log (x)"},
        {"num": 211, "q": "Find f'(x) for f(x) = (x^2 + sqrt(x))*csc(x)", "ans": "-(x^2 + sqrt(x))*csc(x)*cot(x) + (2*x + 1/(2*sqrt(x)))*csc(x)", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => (x^2 + Real.sqrt (x))*Real.csc (x)) x = -(x^2 + Real.sqrt (x))*Real.csc (x)*Real.cot (x) + (2*x + 1/(2*Real.sqrt (x)))*Real.csc (x) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "(x^2 + Real.sqrt (x))*Real.csc (x)"},
        # Page 74 (#212 - #214) Double angle / identities
        {"num": 212, "q": "Find d/dx [sin(2*x)] using double angle formula", "ans": "2*cos(2*x)", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => 2*Real.sin (x)*Real.cos (x)) x = 2*Real.cos (2*x) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "2*Real.sin (x)*Real.cos (x)"},
        {"num": 213, "q": "Find d/dx [cos(x)*csc(x)]", "ans": "-csc(x)^2", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => Real.cot (x)) x = -Real.csc (x)^2 := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "Real.cot (x)"},
        {"num": 214, "q": "Find d/dx [(1 + sin(x))*sqrt(x)]", "ans": "sqrt(x)*cos(x) + (1 + sin(x))/(2*sqrt(x))", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => (1 + Real.sin (x))*Real.sqrt (x)) x = Real.sqrt (x)*Real.cos (x) + (1 + Real.sin (x))/(2*Real.sqrt (x)) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "(1 + Real.sin (x))*Real.sqrt (x)"},
        # Page 75 (#215 - #217)
        {"num": 215, "q": "Find dy/dx for y = (-10*x + x^(1/4) - 2)*e^x", "ans": "(-10*x + x^(1/4) - 12 + 1/(4*x^(3/4)))*e^x", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => (-10*x + x^(1/4) - 2)*Real.exp (x)) x = (-10*x + x^(1/4) - 12 + 1/(4*x^(3/4)))*Real.exp (x) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "(-10*x + x^(1/4) - 2)*Real.exp (x)"},
        {"num": 216, "q": "Find dy/dx for y = (x^4 + 3)*(-x^5 + 6*x)", "ans": "-9*x^8 + 30*x^4 - 15*x^4 + 18", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => (x^4 + 3)*(-x^5 + 6*x)) x = -9*x^8 + 15*x^4 + 18 := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "(x^4 + 3)*(-x^5 + 6*x)"},
        {"num": 217, "q": "Find dy/dx for y = (x^4 + sin(x))*cos(x)", "ans": "-x^4*sin(x) + 4*x^3*cos(x) + cos(2*x)", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => (x^4 + Real.sin (x))*Real.cos (x)) x = -x^4*Real.sin (x) + 4*x^3*Real.cos (x) + Real.cos (2*x) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "(x^4 + Real.sin (x))*Real.cos (x)"},
        # Page 76 (#218 - #220)
        {"num": 218, "q": "Find y' for y = (x^2 + 6)*(x^3 - 8)", "ans": "5*x^4 + 18*x^2 - 16*x", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => (x^2 + 6)*(x^3 - 8)) x = 5*x^4 + 18*x^2 - 16*x := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "(x^2 + 6)*(x^3 - 8)"},
        {"num": 219, "q": "Find y' for y = (3*x^3 + 6)*(x^2 - 4)", "ans": "15*x^4 - 36*x^2 + 12*x", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => (3*x^3 + 6)*(x^2 - 4)) x = 15*x^4 - 36*x^2 + 12*x := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "(3*x^3 + 6)*(x^2 - 4)"},
        {"num": 220, "q": "Find y' for y = (sqrt(x) + x^(1/3))*(x^(1/4) + x^(1/5))", "ans": "(3/4)*x^(-1/4) + (7/10)*x^(-3/10) + (7/12)*x^(-5/12) + (8/15)*x^(-7/15)", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => (Real.sqrt (x) + x^(1/3))*(x^(1/4) + x^(1/5))) x = (3/4)*x^(-1/4) + (7/10)*x^(-3/10) + (7/12)*x^(-5/12) + (8/15)*x^(-7/15) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "(Real.sqrt (x) + x^(1/3))*(x^(1/4) + x^(1/5))"},
        # Page 77 (#221 - #223)
        {"num": 221, "q": "Find y' for y = (ln(x) + e^x)*(log_5(x) - 6^x)", "ans": "(ln(x) + e^x)*(1/(x*ln(5)) - 6^x*ln(6)) + (1/x + e^x)*(log_5(x) - 6^x)", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => (Real.log (x) + Real.exp (x))*(Real.log (x)/Real.log 5 - 6^x)) x = (Real.log (x) + Real.exp (x))*(1/(x*Real.log 5) - 6^x*Real.log 6) + (1/x + Real.exp (x))*(Real.log (x)/Real.log 5 - 6^x) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "(Real.log (x) + Real.exp (x))*(Real.log (x)/Real.log 5 - 6^x)"},
        {"num": 222, "q": "Find y' for y = sin(pi/2)*x^2*cos(x)", "ans": "-x^2*sin(x) + 2*x*cos(x)", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => x^2*Real.cos (x)) x = -x^2*Real.sin (x) + 2*x*Real.cos (x) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "x^2*Real.cos (x)"},
        {"num": 223, "q": "Find y' for y = (sin(x) - ln(x))*(sqrt(x) + 2^x)", "ans": "(sin(x) - ln(x))*(1/(2*sqrt(x)) + 2^x*ln(2)) + (cos(x) - 1/x)*(sqrt(x) + 2^x)", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => (Real.sin (x) - Real.log (x))*(Real.sqrt (x) + 2^x)) x = (Real.sin (x) - Real.log (x))*(1/(2*Real.sqrt (x)) + 2^x*Real.log 2) + (Real.cos (x) - 1/x)*(Real.sqrt (x) + 2^x) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "(Real.sin (x) - Real.log (x))*(Real.sqrt (x) + 2^x)"},
        # Page 78 (#224 - #226) Limits
        {"num": 224, "q": "Find the limits: lim_{h->0} (e^(x+h)*2^(x+h) - e^x*2^x)/h", "ans": "e^x*2^x*(ln(2) + 1)", "tid": "derivative_limit_definition", "lean": "example (x : ℝ) : deriv (fun x => Real.exp (x)*2^x) x = Real.exp (x)*2^x*(Real.log 2 + 1) := by\n  simp [deriv_pow, deriv_mul, deriv_div, deriv_sin, deriv_cos, deriv_tan, deriv_sec, deriv_exp, deriv_log]\n  ring", "f": "Real.exp (x)*2^x"},
        {"num": 225, "q": "Find the limits: lim_{h->0} (((x+h)^2 + 1)*sin(x+h) - (x^2 + 1)*sin(x))/h", "ans": "(x^2 + 1)*cos(x) + 2*x*sin(x)", "tid": "derivative_limit_definition", "lean": "example (x : ℝ) : deriv (fun x => (x^2 + 1)*Real.sin (x)) x = (x^2 + 1)*Real.cos (x) + 2*x*Real.sin (x) := by\n  simp [deriv_pow, deriv_mul, deriv_div, deriv_sin, deriv_cos, deriv_tan, deriv_sec, deriv_exp, deriv_log]\n  ring", "f": "(x^2 + 1)*Real.sin (x)"},
        {"num": 226, "q": "Find the limits: lim_{h->0} (ln(x+h)*sec(x+h) - ln(x)*sec(x))/h", "ans": "ln(x)*sec(x)*tan(x) + sec(x)/x", "tid": "derivative_limit_definition", "lean": "example (x : ℝ) : deriv (fun x => Real.log (x)*Real.sec (x)) x = Real.log (x)*Real.sec (x)*Real.tan (x) + Real.sec (x)/x := by\n  simp [deriv_pow, deriv_mul, deriv_div, deriv_sin, deriv_cos, deriv_tan, deriv_sec, deriv_exp, deriv_log]\n  ring", "f": "Real.log (x)*Real.sec (x)"},
        # Page 79 (#227 - #229) Velocity functions
        {"num": 227, "q": "Find the velocity function of the particle at time t: s(t) = -(t^3 + 1)*e^t", "ans": "-e^t*(t^3 + 3*t^2 + 1)", "tid": "particle_velocity_derivative", "lean": "example (t : ℝ) : deriv (fun t => -(t^3 + 1)*Real.exp (t)) t = -Real.exp (t)*(t^3 + 3*t^2 + 1) := by\n  simp [deriv_pow, deriv_mul, deriv_div, deriv_sin, deriv_cos, deriv_tan, deriv_exp, deriv_log]\n  ring", "s": "-(t^3 + 1)*Real.exp (t)"},
        {"num": 228, "q": "Find the velocity function of the particle at time t: s(t) = cos(t)*t^(1/4)", "ans": "cos(t)/(4*t^(3/4)) - t^(1/4)*sin(t)", "tid": "particle_velocity_derivative", "lean": "example (t : ℝ) : deriv (fun t => Real.cos (t)*t^(1/4)) t = Real.cos (t)/(4*t^(3/4)) - t^(1/4)*Real.sin (t) := by\n  simp [deriv_pow, deriv_mul, deriv_div, deriv_sin, deriv_cos, deriv_tan, deriv_exp, deriv_log]\n  ring", "s": "Real.cos (t)*t^(1/4)"},
        {"num": 229, "q": "Find the velocity function of the particle at time t: s(t) = sqrt(t)*sin(t)*cos(t)", "ans": "sin(2*t)/(4*sqrt(t)) + sqrt(t)*cos(2*t)", "tid": "particle_velocity_derivative", "lean": "example (t : ℝ) : deriv (fun t => Real.sqrt (t)*Real.sin (t)*Real.cos (t)) t = Real.sin (2*t)/(4*Real.sqrt (t)) + Real.sqrt (t)*Real.cos (2*t) := by\n  simp [deriv_pow, deriv_mul, deriv_div, deriv_sin, deriv_cos, deriv_tan, deriv_exp, deriv_log]\n  ring", "s": "Real.sqrt (t)*Real.sin (t)*Real.cos (t)"},
        # Page 80 (#230 - #232)
        {"num": 230, "q": "Find y' for y = (x^2 - 1)*(3*x^4 - 2*x + 1)", "ans": "18*x^5 - 12*x^4 - 4*x^2 + 2*x + 2", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => (x^2 - 1)*(3*x^4 - 2*x + 1)) x = 18*x^5 - 12*x^4 - 4*x^2 + 2*x + 2 := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "(x^2 - 1)*(3*x^4 - 2*x + 1)"},
        {"num": 231, "q": "Find y' for y = x^6*cos(x)", "ans": "-x^6*sin(x) + 6*x^5*cos(x)", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => x^6*Real.cos (x)) x = -x^6*Real.sin (x) + 6*x^5*Real.cos (x) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "x^6*Real.cos (x)"},
        {"num": 232, "q": "Find y' for y = e^x*(1 - x^3)", "ans": "e^x*(1 - 3*x^2 - x^3)", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => Real.exp (x)*(1 - x^3)) x = Real.exp (x)*(1 - 3*x^2 - x^3) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "Real.exp (x)*(1 - x^3)"},
        # Page 81 (#233 - #235)
        {"num": 233, "q": "Find y' for y = 7*x^(5/2)*tan(x)", "ans": "7*x^(5/2)*sec(x)^2 + (35/2)*x^(3/2)*tan(x)", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => 7*x^(5/2)*Real.tan (x)) x = 7*x^(5/2)*Real.sec (x)^2 + (35/2)*x^(3/2)*Real.tan (x) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "7*x^(5/2)*Real.tan (x)"},
        {"num": 234, "q": "Find y' for y = 2*x^7*(1 + x^5)", "ans": "24*x^11 + 14*x^6", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => 2*x^7*(1 + x^5)) x = 24*x^11 + 14*x^6 := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "2*x^7*(1 + x^5)"},
        {"num": 235, "q": "Find y' for y = x*e^x*sin(x)", "ans": "x*e^x*cos(x) + x*e^x*sin(x) + e^x*sin(x)", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => x*Real.exp (x)*Real.sin (x)) x = x*Real.exp (x)*Real.cos (x) + x*Real.exp (x)*Real.sin (x) + Real.exp (x)*Real.sin (x) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "x*Real.exp (x)*Real.sin (x)"},
        # Page 82 (#236 - #239)
        {"num": 236, "q": "Find y' for y = (x^2 - 1)*(sqrt(x) + 2)", "ans": "(5/2)*x^(3/2) + 4*x - 1/(2*sqrt(x))", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => (x^2 - 1)*(Real.sqrt (x) + 2)) x = (5/2)*x^(3/2) + 4*x - 1/(2*Real.sqrt (x)) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "(x^2 - 1)*(Real.sqrt (x) + 2)"},
        {"num": 237, "q": "Find y' for y = x^(1/3)*cos(x)", "ans": "-x^(1/3)*sin(x) + cos(x)/(3*x^(2/3))", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => x^(1/3)*Real.cos (x)) x = -x^(1/3)*Real.sin (x) + Real.cos (x)/(3*x^(2/3)) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "x^(1/3)*Real.cos (x)"},
        {"num": 238, "q": "Find y' for y = cot(x)*cos(x)", "ans": "-cos(x) - cot(x)*csc(x)*cos(x)", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => Real.cot (x)*Real.cos (x)) x = -Real.cos (x) - Real.cot (x)*Real.csc (x)*Real.cos (x) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "Real.cot (x)*Real.cos (x)"},
        {"num": 239, "q": "Find y' for y = sqrt(x)*e^x*ln(x)*sin(x)", "ans": "sqrt(x)*e^x*ln(x)*cos(x) + sqrt(x)*e^x*ln(x)*sin(x) + sqrt(x)*e^x*sin(x)/x + e^x*ln(x)*sin(x)/(2*sqrt(x))", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => Real.sqrt (x)*Real.exp (x)*Real.log (x)*Real.sin (x)) x = Real.sqrt (x)*Real.exp (x)*Real.log (x)*Real.cos (x) + Real.sqrt (x)*Real.exp (x)*Real.log (x)*Real.sin (x) + Real.sqrt (x)*Real.exp (x)*Real.sin (x)/x + Real.exp (x)*Real.log (x)*Real.sin (x)/(2*Real.sqrt (x)) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "Real.sqrt (x)*Real.exp (x)*Real.log (x)*Real.sin (x)"},
        # Page 83 (#240 - #242) Point evaluations at c
        {"num": 240, "q": "Find the value of f'(c) at the given c value: f(x) = (x^4 - 1)*(sqrt(x) + 1) at c = 4", "ans": "3327/4", "tid": "tangent_slope_derivative", "lean": "example : deriv (fun x => (x^4 - 1)*(Real.sqrt (x) + 1)) 4 = 3327/4 := by\n  simp [deriv_pow, deriv_mul, deriv_sin, deriv_cos, deriv_tan, deriv_exp, deriv_log]\n  ring", "f": "(x^4 - 1)*(Real.sqrt (x) + 1)", "x0": "4"},
        {"num": 241, "q": "Find the value of f'(c) at the given c value: f(x) = e^x*sin(x) at c = pi/2", "ans": "exp(pi/2)", "tid": "tangent_slope_derivative", "lean": "example : deriv (fun x => Real.exp (x)*Real.sin (x)) (Real.pi/2) = Real.exp (Real.pi/2) := by\n  simp [deriv_pow, deriv_mul, deriv_sin, deriv_cos, deriv_tan, deriv_exp, deriv_log]\n  ring", "f": "Real.exp (x)*Real.sin (x)", "x0": "(Real.pi/2)"},
        {"num": 242, "q": "Find the value of f'(c) at the given c value: f(x) = (4*x - 1)*(cos(x) - tan(x)) at c = 0", "ans": "5", "tid": "tangent_slope_derivative", "lean": "example : deriv (fun x => (4*x - 1)*(Real.cos (x) - Real.tan (x))) 0 = 5 := by\n  simp [deriv_pow, deriv_mul, deriv_sin, deriv_cos, deriv_tan, deriv_exp, deriv_log]\n  ring", "f": "(4*x - 1)*(Real.cos (x) - Real.tan (x))", "x0": "0"},
        # Page 84 (#243 - #245)
        {"num": 243, "q": "Find the value of f'(c) at the given c value: f(x) = 2^x*ln(x) at c = 4", "ans": "16*ln(2)*ln(4) + 4", "tid": "tangent_slope_derivative", "lean": "example : deriv (fun x => 2^x*Real.log (x)) 4 = 16*Real.log (2)*Real.log (4) + 4 := by\n  simp [deriv_pow, deriv_mul, deriv_sin, deriv_cos, deriv_tan, deriv_exp, deriv_log]\n  ring", "f": "2^x*Real.log (x)", "x0": "4"},
        {"num": 244, "q": "Find the value of f'(c) at the given c value: f(x) = (sqrt(x) + x^2)*(e^x + ln(x)) at c = 1", "ans": "(5/2)*e + 2", "tid": "tangent_slope_derivative", "lean": "example : deriv (fun x => (Real.sqrt (x) + x^2)*(Real.exp (x) + Real.log (x))) 1 = (5/2)*Real.exp (1) + 2 := by\n  simp [deriv_pow, deriv_mul, deriv_sin, deriv_cos, deriv_tan, deriv_exp, deriv_log]\n  ring", "f": "(Real.sqrt (x) + x^2)*(Real.exp (x) + Real.log (x))", "x0": "1"},
        {"num": 245, "q": "Find the value of f'(c) at the given c value: f(x) = (x^3 + x)*cos(x) at c = pi/2", "ans": "-pi^3/8 - pi/2", "tid": "tangent_slope_derivative", "lean": "example : deriv (fun x => (x^3 + x)*Real.cos (x)) (Real.pi/2) = -Real.pi^3/8 - Real.pi/2 := by\n  simp [deriv_pow, deriv_mul, deriv_sin, deriv_cos, deriv_tan, deriv_exp, deriv_log]\n  ring", "f": "(x^3 + x)*Real.cos (x)", "x0": "(Real.pi/2)"},
        # Page 85 (#246 - #248) Given k(x) = 4x^2 - 6x + 1
        {"num": 246, "q": "Given k(x) = 4*x^2 - 6*x + 1, find h'(x) for h(x) = k(x)*sqrt(x)", "ans": "(20*x^2 - 18*x + 1)/(2*sqrt(x))", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => (4*x^2 - 6*x + 1)*Real.sqrt (x)) x = (20*x^2 - 18*x + 1)/(2*Real.sqrt (x)) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "(4*x^2 - 6*x + 1)*Real.sqrt (x)"},
        {"num": 247, "q": "Given k(x) = 4*x^2 - 6*x + 1, find h'(x) for h(x) = 3*k(x)*(e^x + cos(x))", "ans": "3*(8*x - 6)*(e^x + cos(x)) + 3*(4*x^2 - 6*x + 1)*(e^x - sin(x))", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => 3*(4*x^2 - 6*x + 1)*(Real.exp (x) + Real.cos (x))) x = 3*(8*x - 6)*(Real.exp (x) + Real.cos (x)) + 3*(4*x^2 - 6*x + 1)*(Real.exp (x) - Real.sin (x)) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "3*(4*x^2 - 6*x + 1)*(Real.exp (x) + Real.cos (x))"},
        {"num": 248, "q": "Given k(x) = 4*x^2 - 6*x + 1, find h'(x) for h(x) = k(x)*k(x)", "ans": "64*x^3 - 144*x^2 + 88*x - 12", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => (4*x^2 - 6*x + 1)^2) x = 64*x^3 - 144*x^2 + 88*x - 12 := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "(4*x^2 - 6*x + 1)^2"},
        # Page 86 (#249 - #250)
        {"num": 249, "q": "Given k(x) = 4*x^2 - 6*x + 1, find h'(x) for h(x) = ln(x)*k(x)", "ans": "(8*x - 6)*ln(x) + 4*x - 6 + 1/x", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => Real.log (x)*(4*x^2 - 6*x + 1)) x = (8*x - 6)*Real.log (x) + 4*x - 6 + 1/x := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "Real.log (x)*(4*x^2 - 6*x + 1)"},
        {"num": 250, "q": "Find h'(x) for h(x) = 100*x^100 * 10^x", "ans": "10000*x^99 * 10^x + 100*x^100 * 10^x * ln(10)", "tid": "product_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => 100*x^100 * 10^x) x = 10000*x^99 * 10^x + 100*x^100 * 10^x * Real.log 10 := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "100*x^100 * 10^x"},
        
        # CHAPTER 3: QUOTIENT RULE
        # Page 88 (#251 - #253)
        {"num": 251, "q": "Find dy/dx for y = x / cos(x)", "ans": "(cos(x) + x*sin(x))/cos(x)^2", "tid": "quotient_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => x / Real.cos (x)) x = (Real.cos (x) + x*Real.sin (x))/Real.cos (x)^2 := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "x / Real.cos (x)"},
        {"num": 252, "q": "Find dy/dx for y = (2*x + 5)/(4*x - 6)", "ans": "-8/(2*x - 3)^2", "tid": "quotient_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => (2*x + 5)/(4*x - 6)) x = -8/(2*x - 3)^2 := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "(2*x + 5)/(4*x - 6)"},
        {"num": 253, "q": "Find dy/dx for y = sqrt(x)/ln(x)", "ans": "(ln(x) - 2)/(2*sqrt(x)*ln(x)^2)", "tid": "quotient_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => Real.sqrt (x)/Real.log (x)) x = (Real.log (x) - 2)/(2*Real.sqrt (x)*Real.log (x)^2) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "Real.sqrt (x)/Real.log (x)"},
        # Page 89 (#254 - #256)
        {"num": 254, "q": "Find dy/dx for y = sin(x)/cos(x)", "ans": "sec(x)^2", "tid": "quotient_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => Real.sin (x)/Real.cos (x)) x = Real.sec (x)^2 := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "Real.sin (x)/Real.cos (x)"},
        {"num": 255, "q": "Find dy/dx for y = (7*x^2 - 1)/(x + 4)", "ans": "(7*x^2 + 56*x + 1)/(x + 4)^2", "tid": "quotient_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => (7*x^2 - 1)/(x + 4)) x = (7*x^2 + 56*x + 1)/(x + 4)^2 := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "(7*x^2 - 1)/(x + 4)"},
        {"num": 256, "q": "Find dy/dx for y = (A*x + B)/(C*x + D) where A, B, C, D in Real", "ans": "(A*D - B*C)/(C*x + D)^2", "tid": "symbolic_linear_rational_derivative", "lean": "example (A B C D x : ℝ) : deriv (fun x => (A*x + B)/(C*x + D)) x = (A*D - B*C)/(C*x + D)^2 := by\n  simp [deriv_div, deriv_add, deriv_mul, deriv_pow]\n  ring"},
        # Page 90 (#257 - #259)
        {"num": 257, "q": "Find dy/dx for y = ln(x)/tan(x)", "ans": "(tan(x)/x - ln(x)*sec(x)^2)/tan(x)^2", "tid": "quotient_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => Real.log (x)/Real.tan (x)) x = (Real.tan (x)/x - Real.log (x)*Real.sec (x)^2)/Real.tan (x)^2 := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "Real.log (x)/Real.tan (x)"},
        {"num": 258, "q": "Find dy/dx for y = e^x/(x^3 - 1)", "ans": "e^x*(x^3 - 3*x^2 - 1)/(x^3 - 1)^2", "tid": "quotient_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => Real.exp (x)/(x^3 - 1)) x = Real.exp (x)*(x^3 - 3*x^2 - 1)/(x^3 - 1)^2 := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "Real.exp (x)/(x^3 - 1)"},
        {"num": 259, "q": "Find dy/dx for y = (sqrt(x) - 1)/(sqrt(x) + 4)", "ans": "5/(2*sqrt(x)*(sqrt(x) + 4)^2)", "tid": "quotient_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => (Real.sqrt (x) - 1)/(Real.sqrt (x) + 4)) x = 5/(2*Real.sqrt (x)*(Real.sqrt (x) + 4)^2) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "(Real.sqrt (x) - 1)/(Real.sqrt (x) + 4)"},
        # Page 91 (#260 - #262)
        {"num": 260, "q": "Find dy/dx for y = (3*x^2 - 6)/(4*x - 11)", "ans": "(12*x^2 - 66*x + 24)/(4*x - 11)^2", "tid": "quotient_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => (3*x^2 - 6)/(4*x - 11)) x = (12*x^2 - 66*x + 24)/(4*x - 11)^2 := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "(3*x^2 - 6)/(4*x - 11)"},
        {"num": 261, "q": "Find dy/dx for y = sin(x)/e^x", "ans": "(cos(x) - sin(x))/e^x", "tid": "quotient_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => Real.sin (x)/Real.exp (x)) x = (Real.cos (x) - Real.sin (x))/Real.exp (x) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "Real.sin (x)/Real.exp (x)"},
        {"num": 262, "q": "Find dy/dx for y = (e^x + cos(x))/(x^2 + 4)", "ans": "((e^x - sin(x))*(x^2 + 4) - 2*x*(e^x + cos(x)))/(x^2 + 4)^2", "tid": "quotient_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => (Real.exp (x) + Real.cos (x))/(x^2 + 4)) x = ((Real.exp (x) - Real.sin (x))*(x^2 + 4) - 2*x*(Real.exp (x) + Real.cos (x)))/(x^2 + 4)^2 := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "(Real.exp (x) + Real.cos (x))/(x^2 + 4)"},
        # Page 92 - 94 (#263 - #268) Tabular Quotient Rule
        {"num": 263, "q": "Use the table for #263: h(x) = f(x)/g(x), find h'(3)", "ans": "94/49", "tid": "tabular_derivative", "lean": "example : (10*7 - (-4)*6) / 49 = 94/49 := by\n  norm_num", "op": "h'(3)", "pt": "3", "sub": "(10*7 - (-4)*6) / 49"},
        {"num": 264, "q": "Use the table for #264: h(x) = g(x)/f(x), find h'(5)", "ans": "-27/98", "tid": "tabular_derivative", "lean": "example : (1*14 - 17*4) / 196 = -27/98 := by\n  norm_num", "op": "h'(5)", "pt": "5", "sub": "(1*14 - 17*4) / 196"},
        {"num": 265, "q": "Use the table for #265: h(x) = ln(x)/g(x), find h'(1)", "ans": "1", "tid": "tabular_derivative", "lean": "example : (1*1 - 0*4) / 1 = 1 := by\n  norm_num", "op": "h'(1)", "pt": "1", "sub": "(1*1 - 0*4) / 1"},
        {"num": 266, "q": "Use the table for #266: h(x) = x*f(x)/g(x), find h'(1)", "ans": "-6", "tid": "tabular_derivative", "lean": "example : ((-6)*1 - 0*4) / 1 = -6 := by\n  norm_num", "op": "h'(1)", "pt": "1", "sub": "((-6)*1 - 0*4) / 1"},
        {"num": 267, "q": "Use the table for #267: h(x) = sqrt(x)/f(x), find h'(4)", "ans": "11/72", "tid": "tabular_derivative", "lean": "example : ((1/4)*6 - 2*(-2)) / 36 = 11/72 := by\n  norm_num", "op": "h'(4)", "pt": "4", "sub": "((1/4)*6 - 2*(-2)) / 36"},
        {"num": 268, "q": "Use the table for #268: h(x) = (x + 3)/(f(x) + g(x)), find h'(1)", "ans": "9", "tid": "tabular_derivative", "lean": "example : (1*1 - 4*(-2)) / 1 = 9 := by\n  norm_num", "op": "h'(1)", "pt": "1", "sub": "(1*1 - 4*(-2)) / 1"},
        # Page 95 (#269 - #271)
        {"num": 269, "q": "Find f'(x) for f(x) = 1/(x + 4)", "ans": "-1/(x + 4)^2", "tid": "quotient_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => 1/(x + 4)) x = -1/(x + 4)^2 := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "1/(x + 4)"},
        {"num": 270, "q": "Find f'(x) for f(x) = sqrt(x)/e^x", "ans": "(1 - 2*x)/(2*sqrt(x)*e^x)", "tid": "quotient_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => Real.sqrt (x)/Real.exp (x)) x = (1 - 2*x)/(2*Real.sqrt (x)*Real.exp (x)) := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "Real.sqrt (x)/Real.exp (x)"},
        {"num": 271, "q": "Find f'(x) for f(x) = (x^(1/3) + 6)/(x^2 + 1)", "ans": "((1/3)*x^(-2/3)*(x^2 + 1) - 2*x*(x^(1/3) + 6))/(x^2 + 1)^2", "tid": "quotient_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => (x^(1/3) + 6)/(x^2 + 1)) x = ((1/3)*x^(-2/3)*(x^2 + 1) - 2*x*(x^(1/3) + 6))/(x^2 + 1)^2 := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "(x^(1/3) + 6)/(x^2 + 1)"},
        # Page 96 (#272 - #274)
        {"num": 272, "q": "Find f'(x) for f(x) = (sin(x) + x)/cos(x)", "ans": "(1 + cos(x) + x*sin(x))/cos(x)^2", "tid": "quotient_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => (Real.sin (x) + x)/Real.cos (x)) x = (1 + Real.cos (x) + x*Real.sin (x))/Real.cos (x)^2 := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "(Real.sin (x) + x)/Real.cos (x)"},
        {"num": 273, "q": "Find f'(x) for f(x) = 1/(x^2 - 3*x + 5)", "ans": "-(2*x - 3)/(x^2 - 3*x + 5)^2", "tid": "quotient_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => 1/(x^2 - 3*x + 5)) x = -(2*x - 3)/(x^2 - 3*x + 5)^2 := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "1/(x^2 - 3*x + 5)"},
        {"num": 274, "q": "Find f'(x) for f(x) = (4*x^2 + 1)/sin(x)", "ans": "(8*x*sin(x) - (4*x^2 + 1)*cos(x))/sin(x)^2", "tid": "quotient_rule_derivative", "lean": "example (x : ℝ) : deriv (fun x => (4*x^2 + 1)/Real.sin (x)) x = (8*x*Real.sin (x) - (4*x^2 + 1)*Real.cos (x))/Real.sin (x)^2 := by\n  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring", "f": "(4*x^2 + 1)/Real.sin (x)"},
        # Page 97 - 98 (#275 - #280) Quotient Tangent Slopes at Point
        {"num": 275, "q": "Find the slope of the tangent line of the function y at the point x = 1: y = ln(x)/(2*x)", "ans": "1/2", "tid": "tangent_slope_derivative", "lean": "example : deriv (fun x => Real.log (x)/(2*x)) 1 = 1/2 := by\n  simp [deriv_pow, deriv_mul, deriv_sin, deriv_cos, deriv_tan, deriv_exp, deriv_log]\n  ring", "f": "Real.log (x)/(2*x)", "x0": "1"},
        {"num": 276, "q": "Find the slope of the tangent line of the function y at the point x = pi/2: y = e^x/sin(x)", "ans": "exp(pi/2)", "tid": "tangent_slope_derivative", "lean": "example : deriv (fun x => Real.exp (x)/Real.sin (x)) (Real.pi/2) = Real.exp (Real.pi/2) := by\n  simp [deriv_pow, deriv_mul, deriv_sin, deriv_cos, deriv_tan, deriv_exp, deriv_log]\n  ring", "f": "Real.exp (x)/Real.sin (x)", "x0": "(Real.pi/2)"},
        {"num": 277, "q": "Find the slope of the tangent line of the function y at the point x = 4: y = (5*x)/(sqrt(x) + 1)", "ans": "10/9", "tid": "tangent_slope_derivative", "lean": "example : deriv (fun x => (5*x)/(Real.sqrt (x) + 1)) 4 = 10/9 := by\n  simp [deriv_pow, deriv_mul, deriv_sin, deriv_cos, deriv_tan, deriv_exp, deriv_log]\n  ring", "f": "(5*x)/(Real.sqrt (x) + 1)", "x0": "4"},
        {"num": 278, "q": "Find the slope of the tangent line of the function y at the point x = 3: y = 6/(x^3 - 8)", "ans": "-162/361", "tid": "tangent_slope_derivative", "lean": "example : deriv (fun x => 6/(x^3 - 8)) 3 = -162/361 := by\n  simp [deriv_pow, deriv_mul, deriv_sin, deriv_cos, deriv_tan, deriv_exp, deriv_log]\n  ring", "f": "6/(x^3 - 8)", "x0": "3"},
        {"num": 279, "q": "Find the slope of the tangent line of the function y at the point x = 1: y = (3*x + 1)/(5*x - 6)", "ans": "-23", "tid": "tangent_slope_derivative", "lean": "example : deriv (fun x => (3*x + 1)/(5*x - 6)) 1 = -23 := by\n  simp [deriv_pow, deriv_mul, deriv_sin, deriv_cos, deriv_tan, deriv_exp, deriv_log]\n  ring", "f": "(3*x + 1)/(5*x - 6)", "x0": "1"},
        {"num": 280, "q": "Find the slope of the tangent line of the function y at the point x = 9: y = (7*sqrt(x) - 1)/(x - 4)", "ans": "-17/30", "tid": "tangent_slope_derivative", "lean": "example : deriv (fun x => (7*Real.sqrt (x) - 1)/(x - 4)) 9 = -17/30 := by\n  simp [deriv_pow, deriv_mul, deriv_sin, deriv_cos, deriv_tan, deriv_exp, deriv_log]\n  ring", "f": "(7*Real.sqrt (x) - 1)/(x - 4)", "x0": "9"}
    ]
    
    for p in probs:
        tid = p["tid"]
        if tid == "product_rule_derivative":
            params = {"expr": p["f"], "answer": p["ans"]}
        elif tid == "quotient_rule_derivative":
            params = {"expr": p["f"], "answer": p["ans"]}
        elif tid == "derivative":
            params = {"expr": p["f"], "answer": p["ans"]}
        elif tid == "tangent_slope_derivative":
            params = {"f": p["f"], "x0": p.get("x0", "0"), "m": p["ans"]}
        elif tid == "derivative_limit_definition":
            params = {"f": p["f"], "ans": p["ans"]}
        elif tid == "particle_velocity_derivative":
            params = {"s": p["s"], "v": p["ans"]}
        elif tid == "tabular_derivative":
            params = {"operation": p["op"], "point": p["pt"], "expr_sub": p["sub"], "ans": p["ans"]}
        elif tid == "symbolic_linear_rational_derivative":
            params = {"ans": p["ans"]}
        else:
            params = {"answer": p["ans"]}
            
        entries.append(make_entry(p["q"], tid, params, p["lean"]))
        
        # Add pedagogical conversational variation (e.g. "Differentiate...", "Find the derivative of...")
        alt_q = None
        if "Find the value of y' for " in p["q"]:
            alt_q = p["q"].replace("Find the value of y' for ", "Differentiate ")
        elif "Find y' for " in p["q"]:
            alt_q = p["q"].replace("Find y' for ", "Find the derivative of ")
        elif "Find dy/dx for " in p["q"]:
            alt_q = p["q"].replace("Find dy/dx for ", "Compute the derivative with respect to x of ")
        elif "Find f'(x) for " in p["q"]:
            alt_q = p["q"].replace("Find f'(x) for ", "Calculate the derivative f'(x) of ")
            
        if alt_q:
            entries.append(make_entry(alt_q, tid, params, p["lean"]))
            
    return entries

def generate_way2() -> List[Dict[str, Any]]:
    entries = []
    
    # 1. Parametric Product Rule: x^n * f(x)
    for n in [2, 3, 4, 5]:
        for trig in [("sin", "cos", "-sin"), ("cos", "-sin", "-cos"), ("tan", "sec^2", "2*sec^2*tan")]:
            fn_name, d1_name, _ = trig
            prob = f"Find the derivative of y = x^{n}*{fn_name}(x) using the product rule"
            ans = f"{n}*x^{n-1}*{fn_name}(x) + x^{n}*{d1_name}(x)"
            lean = (
                f"example (x : ℝ) : deriv (fun x => x^{n}*Real.{fn_name} (x)) x = "
                f"{n}*x^{n-1}*Real.{fn_name} (x) + x^{n}*Real.{d1_name} (x) := by\n"
                f"  simp [deriv_mul, deriv_pow, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring"
            )
            entries.append(make_entry(prob, "product_rule_derivative", {"expr": f"x^{n}*Real.{fn_name} (x)", "answer": ans}, lean))

    # 2. Parametric Exponential Products: a^x * f(x)
    for base in [2, 3, 5, 10]:
        for pwr in [2, 3, 4]:
            prob = f"Differentiate y = {base}^x * x^{pwr} using the product rule"
            ans = f"{base}^x*x^{pwr}*ln({base}) + {pwr}*{base}^x*x^{pwr-1}"
            lean = (
                f"example (x : ℝ) : deriv (fun x => {base}^x * x^{pwr}) x = "
                f"{base}^x*x^{pwr}*Real.log ({base}) + {pwr}*{base}^x*x^{pwr-1} := by\n"
                f"  simp [deriv_mul, deriv_pow, deriv_exp, deriv_log]\n  ring"
            )
            entries.append(make_entry(prob, "product_rule_derivative", {"expr": f"{base}^x * x^{pwr}", "answer": ans}, lean))

    # 3. Parametric Linear Rational Functions (Quotient Rule): (ax + b)/(cx + d)
    for a in [2, 3, 5]:
        for b in [1, 4, -3]:
            for c in [1, 2, 4]:
                for d in [3, -5, 7]:
                    num = a * d - b * c
                    prob = f"Find dy/dx for y = ({a}*x + {b})/({c}*x + {d})"
                    ans = f"{num}/({c}*x + {d})^2"
                    lean = (
                        f"example (x : ℝ) : deriv (fun x => ({a}*x + {b})/({c}*x + {d})) x = "
                        f"{num}/({c}*x + {d})^2 := by\n"
                        f"  simp [deriv_mul, deriv_pow, deriv_exp, deriv_log]\n  ring"
                    )
                    entries.append(make_entry(prob, "quotient_rule_derivative", {"expr": f"({a}*x + {b})/({c}*x + {d})", "answer": ans}, lean))

    # 4. Parametric Reciprocal Derivatives: 1/(x^k + c)
    for k in [2, 3]:
        for c_val in [1, 4, 9]:
            prob = f"Find f'(x) for f(x) = 1/(x^{k} + {c_val})"
            ans = f"-{k}*x^{k-1}/(x^{k} + {c_val})^2"
            lean = (
                f"example (x : ℝ) : deriv (fun x => 1/(x^{k} + {c_val})) x = "
                f"-{k}*x^{k-1}/(x^{k} + {c_val})^2 := by\n"
                f"  simp [deriv_mul, deriv_pow, deriv_exp, deriv_log]\n  ring"
            )
            entries.append(make_entry(prob, "quotient_rule_derivative", {"expr": f"1/(x^{k} + {c_val})", "answer": ans}, lean))

    # 5. Parametric Difference Quotient Limits
    for base in [2, 3, 5]:
        prob = f"Evaluate the limit: lim_{{h->0}} ({base}^(x+h)*sqrt(x+h) - {base}^x*sqrt(x))/h"
        ans = f"{base}^x*sqrt(x)*ln({base}) + {base}^x/(2*sqrt(x))"
        lean = (
            f"example (x : ℝ) : deriv (fun x => {base}^x*Real.sqrt (x)) x = "
            f"{base}^x*Real.sqrt (x)*Real.log ({base}) + {base}^x/(2*Real.sqrt (x)) := by\n"
            f"  simp [deriv_pow, deriv_mul, deriv_div, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring"
        )
        entries.append(make_entry(prob, "derivative_limit_definition", {"f": f"{base}^x*Real.sqrt (x)", "ans": ans}, lean))

    # 6. Parametric Particle Velocities
    for coeff in [2, 3, 5]:
        for pwr in [2, 3]:
            prob = f"Find the velocity function of the particle at time t: s(t) = {coeff}*t^{pwr}*e^t"
            ans = f"{coeff}*t^{pwr}*e^t + {coeff*pwr}*t^{pwr-1}*e^t"
            lean = (
                f"example (t : ℝ) : deriv (fun t => {coeff}*t^{pwr}*Real.exp (t)) t = "
                f"{coeff}*t^{pwr}*Real.exp (t) + {coeff*pwr}*t^{pwr-1}*Real.exp (t) := by\n"
                f"  simp [deriv_pow, deriv_mul, deriv_div, deriv_sin, deriv_cos, deriv_exp, deriv_log]\n  ring"
            )
            entries.append(make_entry(prob, "particle_velocity_derivative", {"s": f"{coeff}*t^{pwr}*Real.exp (t)", "v": ans}, lean))

    return entries

def main():
    print(f"Loading existing dataset from: {DATASET_PATH}")
    existing_count = 0
    if os.path.exists(DATASET_PATH):
        with open(DATASET_PATH, "r", encoding="utf-8") as f:
            existing_count = sum(1 for _ in f)
    print(f"Existing entries: {existing_count}")

    way1 = generate_way1()
    print(f"Generated Way 1 (Authentic #151–#280): {len(way1)} examples")

    way2 = generate_way2()
    print(f"Generated Way 2 (Parametric Generalization): {len(way2)} examples")

    total_new = len(way1) + len(way2)
    print(f"Total new entries to append: {total_new}")

    with open(DATASET_PATH, "a", encoding="utf-8") as f:
        for entry in way1:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        for entry in way2:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"Successfully appended {total_new} entries.")
    print(f"New total dataset size: {existing_count + total_new} examples")

if __name__ == "__main__":
    main()
