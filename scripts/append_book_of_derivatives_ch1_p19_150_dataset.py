"""
VeriMath — Reference 2: Book of 1000 Derivatives (Chapter 1, Problems #19–#150) Dataset Generator
================================================================================================
Grounds the training dataset in Miguel Santiago's "Book of 1000 Derivatives":
  - Completes Chapter 1 (Power Rule + Sum/Difference + Basic Derivatives, #19 through #150).
  - Integrates new mathematical concepts:
      * Arbitrary base logarithms: log_a(x) -> 1/(x*ln(a))
      * Arbitrary base exponentials: a^x -> a^x * ln(a)
      * Constant trigonometric terms: sin(pi), cos(pi), tan(0), sin(pi/2) -> 0
      * Tangent line slope at point x0: f'(x0) (#85–#87 at x=0, #121–#123 at x=pi)
      * Instantaneous rate of change at point x: f'(x) (#49–#51)
      * Transition to Chapter 2: Product Rule (#150 completed)

Pathway 1: Authentic textbook problem formulations (#19 to #150).
Pathway 2: Parametric / randomized generalization variations.
"""

import json
import os
import random
import sys
import sympy
from sympy import symbols, diff, sympify, pi, E

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.templates.registry import TEMPLATES, classify_problem

x = symbols('x')

SYSTEM_PROMPT = (
    "You are VeriMath Precision Autoformalization Extractor. Your task is to analyze "
    "mathematical word problems, classify them into the correct template, extract all "
    "parameter values into a structured JSON object, and verify whether all necessary "
    "information is present to solve the problem. If any required variable is missing, "
    "set is_complete to false and identify the missing field. Output valid JSON only."
)

def make_entry(user_text: str, template: str, params: dict, target: str, is_complete: bool = True, missing: list = None):
    assistant_data = {
        "template": template,
        "is_complete": is_complete,
        "parameters": params,
        "target": target,
        "missing_parameters": missing or []
    }
    return {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text.strip()},
            {"role": "assistant", "content": json.dumps(assistant_data, indent=2)}
        ]
    }

def generate_way1():
    entries = []

    # Authentic problems (#19 to #150)
    # Each entry: (prob_num, expr_str, deriv_str, template_id, target, phrasings)
    # For tangent slope: (prob_num, expr_str, x0_str, m_str, template_id, target, phrasings)
    
    problems_data = [
        # Page 9 (#19 - #21)
        (19, "4/x^30 - 1/sqrt(x)", "-120/x^31 + 1/(2*x^(3/2))", "power_rule_derivative", "derivative",
         ["Find the derivative of y = 4/x^30 - 1/sqrt(x)", "Differentiate y = 4/x^30 - 1/sqrt(x) using the power rule"]),
        (20, "14*x - 2500", "14", "power_rule_derivative", "derivative",
         ["Find the derivative of y = 14*x - 2500", "Calculate dy/dx for y = 14x - 2500"]),
        (21, "15*x^2 + sin(pi)", "30*x", "derivative", "derivative",
         ["Find the derivative of y = 15*x^2 + sin(pi)", "Differentiate y = 15x^2 + sin(pi) with respect to x"]),

        # Page 10 (#22 - #24)
        (22, "sin(x) + x", "cos(x) + 1", "trig_derivative", "derivative",
         ["Find the derivative of y = sin(x) + x", "Differentiate y = sin(x) + x with respect to x"]),
        (23, "cos(x) + x^2", "-sin(x) + 2*x", "trig_derivative", "derivative",
         ["Find the derivative of y = cos(x) + x^2", "Calculate dy/dx for y = cos(x) + x^2"]),
        (24, "4*tan(x)", "4*sec(x)^2", "trig_derivative", "derivative",
         ["Find the derivative of y = 4*tan(x)", "Differentiate y = 4tan(x) with respect to x"]),

        # Page 11 (#25 - #27)
        (25, "10*sin(x) + cos(x) - x^2", "10*cos(x) - sin(x) - 2*x", "trig_derivative", "derivative",
         ["Find the derivative of y = 10*sin(x) + cos(x) - x^2", "Calculate dy/dx for y = 10sin(x) + cos(x) - x^2"]),
        (26, "5*cot(x)", "-5*csc(x)^2", "trig_derivative", "derivative",
         ["Find the derivative of y = 5*cot(x)", "Differentiate y = 5cot(x) with respect to x"]),
        (27, "16*x^2 - tan(x)", "32*x - sec(x)^2", "trig_derivative", "derivative",
         ["Find the derivative of y = 16*x^2 - tan(x)", "Calculate dy/dx for y = 16x^2 - tan(x)"]),

        # Page 12 (#28 - #30)
        (28, "6*sqrt(x) + 1", "3/sqrt(x)", "power_rule_derivative", "derivative",
         ["Find the derivative of y = 6*sqrt(x) + 1", "Differentiate y = 6sqrt(x) + 1 using the power rule"]),
        (29, "3*csc(x)", "-3*csc(x)*cot(x)", "trig_derivative", "derivative",
         ["Find the derivative of y = 3*csc(x)", "Calculate dy/dx for y = 3csc(x)"]),
        (30, "4*x^5 - exp(x)", "20*x^4 - exp(x)", "log_exp_derivative", "derivative",
         ["Find the derivative of y = 4*x^5 - e^x", "Differentiate y = 4x^5 - e^x with respect to x"]),

        # Page 13 (#31 - #33)
        (31, "ln(x) + 5*exp(x)", "1/x + 5*exp(x)", "log_exp_derivative", "derivative",
         ["Find the derivative of y = ln(x) + 5*e^x", "Calculate dy/dx for y = ln(x) + 5e^x"]),
        (32, "4/x^2 - cos(x)", "-8/x^3 + sin(x)", "derivative", "derivative",
         ["Find the derivative of y = 4/x^2 - cos(x)", "Differentiate y = 4/x^2 - cos(x) with respect to x"]),
        (33, "100*sec(x) + x^7", "100*sec(x)*tan(x) + 7*x^6", "trig_derivative", "derivative",
         ["Find the derivative of y = 100*sec(x) + x^7", "Calculate dy/dx for y = 100sec(x) + x^7"]),

        # Page 14 (#34 - #36)
        (34, "6*x^5 - 10*x", "30*x^4 - 10", "power_rule_derivative", "derivative",
         ["Find the derivative of y = 6*x^5 - 10*x", "Differentiate y = 6x^5 - 10x using the power rule"]),
        (35, "6*tan(x) - sin(x)", "6*sec(x)^2 - cos(x)", "trig_derivative", "derivative",
         ["Find the derivative of y = 6*tan(x) - sin(x)", "Calculate dy/dx for y = 6tan(x) - sin(x)"]),
        (36, "4/x + x^(1/4)", "-4/x^2 + 1/(4*x^(3/4))", "power_rule_derivative", "derivative",
         ["Find the derivative of y = 4/x + root(4, x)", "Differentiate y = 4/x + x^(1/4) with respect to x"]),

        # Page 15 (#37 - #39)
        (37, "7*sqrt(x) + 1/x^4", "7/(2*sqrt(x)) - 4/x^5", "power_rule_derivative", "derivative",
         ["Find the derivative of y = 7*sqrt(x) + 1/x^4", "Calculate dy/dx for y = 7sqrt(x) + 1/x^4"]),
        (38, "6*sin(x) - csc(x) + 7", "6*cos(x) + csc(x)*cot(x)", "trig_derivative", "derivative",
         ["Find the derivative of y = 6*sin(x) - csc(x) + 7", "Differentiate y = 6sin(x) - csc(x) + 7"]),
        (39, "4*ln(x) - 4*exp(x) - 4*x^2", "4/x - 4*exp(x) - 8*x", "log_exp_derivative", "derivative",
         ["Find the derivative of y = 4*ln(x) - 4*e^x - 4*x^2", "Calculate dy/dx for y = 4ln(x) - 4e^x - 4x^2"]),

        # Page 16 (#40 - #42)
        (40, "6*sec(x) - ln(x)", "6*sec(x)*tan(x) - 1/x", "derivative", "derivative",
         ["Find the derivative of y = 6*sec(x) - ln(x)", "Differentiate y = 6sec(x) - ln(x)"]),
        (41, "6*x^5 + 4*x^3 - exp(x)", "30*x^4 + 12*x^2 - exp(x)", "log_exp_derivative", "derivative",
         ["Find the derivative of y = 6*x^5 + 4*x^3 - e^x", "Calculate dy/dx for y = 6x^5 + 4x^3 - e^x"]),
        (42, "cot(x) + tan(x)", "-csc(x)^2 + sec(x)^2", "trig_derivative", "derivative",
         ["Find the derivative of y = cot(x) + tan(x)", "Differentiate y = cot(x) + tan(x)"]),

        # Page 17 (#43 - #45)
        (43, "sqrt(x) + x^(1/5) + 4", "1/(2*sqrt(x)) + 1/(5*x^(4/5))", "power_rule_derivative", "derivative",
         ["Find the derivative of y = sqrt(x) + x^(1/5) + 4", "Calculate dy/dx for y = sqrt(x) + root(5, x) + 4"]),
        (44, "15*x^2 + 6*x + 3/x", "30*x + 6 - 3/x^2", "power_rule_derivative", "derivative",
         ["Find the derivative of y = 15*x^2 + 6*x + 3/x", "Differentiate y = 15x^2 + 6x + 3/x"]),
        (45, "cos(x) + exp(x)", "-sin(x) + exp(x)", "derivative", "derivative",
         ["Find the derivative of y = cos(x) + e^x", "Calculate dy/dx for y = cos(x) + e^x"]),

        # Page 18 (#46 - #48)
        (46, "ln(x) + 4*x", "1/x + 4", "log_exp_derivative", "derivative",
         ["Find the derivative of y = ln(x) + 4*x", "Differentiate y = ln(x) + 4x"]),
        (47, "14*x^2 - 6*x + sin(x)", "28*x - 6 + cos(x)", "derivative", "derivative",
         ["Find the derivative of y = 14*x^2 - 6*x + sin(x)", "Calculate dy/dx for y = 14x^2 - 6x + sin(x)"]),
        (48, "sqrt(x) + tan(x)", "1/(2*sqrt(x)) + sec(x)^2", "derivative", "derivative",
         ["Find the derivative of y = sqrt(x) + tan(x)", "Differentiate y = sqrt(x) + tan(x)"]),

        # Page 19 (#49 - #51) "FIND THE INSTANTANEOUS RATE OF CHANGE AT THE POINT X"
        (49, "1/sqrt(x) + ln(x)", "-1/(2*x^(3/2)) + 1/x", "log_exp_derivative", "derivative",
         ["Find the instantaneous rate of change of y = 1/sqrt(x) + ln(x) at the point x",
          "Find the derivative of y = 1/sqrt(x) + ln(x)"]),
        (50, "exp(x) + sec(x)", "exp(x) + sec(x)*tan(x)", "derivative", "derivative",
         ["Find the instantaneous rate of change of y = e^x + sec(x) at the point x",
          "Differentiate y = e^x + sec(x) with respect to x"]),
        (51, "ln(x) + 6*x^2 + 5", "1/x + 12*x", "log_exp_derivative", "derivative",
         ["Find the instantaneous rate of change of y = ln(x) + 6*x^2 + 5 at the point x",
          "Calculate dy/dx for y = ln(x) + 6x^2 + 5"]),

        # Page 20 (#52 - #54)
        (52, "4*x^2 - 8*sin(x)", "8*x - 8*cos(x)", "derivative", "derivative",
         ["Find the derivative of y = 4*x^2 - 8*sin(x)", "Calculate dy/dx for y = 4x^2 - 8sin(x)"]),
        (53, "3*x^3 + 4*x^2 + 6*x - 1", "9*x^2 + 8*x + 6", "power_rule_derivative", "derivative",
         ["Find the derivative of y = 3*x^3 + 4*x^2 + 6*x - 1", "Differentiate y = 3x^3 + 4x^2 + 6x - 1"]),
        (54, "40*x^2 + 6/x^2", "80*x - 12/x^3", "power_rule_derivative", "derivative",
         ["Find the derivative of y = 40*x^2 + 6/x^2", "Calculate dy/dx for y = 40x^2 + 6/x^2"]),

        # Page 21 (#55 - #57)
        (55, "10*csc(x) - 8*ln(x)", "-10*csc(x)*cot(x) - 8/x", "derivative", "derivative",
         ["Find the derivative of y = 10*csc(x) - 8*ln(x)", "Differentiate y = 10csc(x) - 8ln(x)"]),
        (56, "exp(x) + 4*x^3 - 4", "exp(x) + 12*x^2", "log_exp_derivative", "derivative",
         ["Find the derivative of y = e^x + 4*x^3 - 4", "Calculate dy/dx for y = e^x + 4x^3 - 4"]),
        (57, "10*x^2 + 4*x - 6", "20*x + 4", "power_rule_derivative", "derivative",
         ["Find the derivative of y = 10*x^2 + 4*x - 6", "Differentiate y = 10x^2 + 4x - 6"]),

        # Page 22 (#58 - #60) Base a exponentials
        (58, "5*sin(x) + 4^x", "5*cos(x) + 4^x*ln(4)", "log_exp_derivative", "derivative",
         ["Find the derivative of y = 5*sin(x) + 4^x", "Calculate dy/dx for y = 5sin(x) + 4^x"]),
        (59, "sec(x) + 3^x", "sec(x)*tan(x) + 3^x*ln(3)", "log_exp_derivative", "derivative",
         ["Find the derivative of y = sec(x) + 3^x", "Differentiate y = sec(x) + 3^x"]),
        (60, "2^x + ln(x) - 4*x", "2^x*ln(2) + 1/x - 4", "log_exp_derivative", "derivative",
         ["Find the derivative of y = 2^x + ln(x) - 4*x", "Calculate dy/dx for y = 2^x + ln(x) - 4x"]),

        # Page 23 (#61 - #63)
        (61, "6*tan(x) + 2*x^2", "6*sec(x)^2 + 4*x", "trig_derivative", "derivative",
         ["Find the derivative of y = 6*tan(x) + 2*x^2", "Differentiate y = 6tan(x) + 2x^2"]),
        (62, "-3*sin(x) + 6^x", "-3*cos(x) + 6^x*ln(6)", "log_exp_derivative", "derivative",
         ["Find the derivative of y = -3*sin(x) + 6^x", "Calculate dy/dx for y = -3sin(x) + 6^x"]),
        (63, "cos(x) + 3*sqrt(x) - 1", "-sin(x) + 3/(2*sqrt(x))", "derivative", "derivative",
         ["Find the derivative of y = cos(x) + 3*sqrt(x) - 1", "Differentiate y = cos(x) + 3sqrt(x) - 1"]),

        # Page 24/25 (#64 - #66)
        (64, "-5^x + sec(x)", "-5^x*ln(5) + sec(x)*tan(x)", "log_exp_derivative", "derivative",
         ["Find the derivative of y = -5^x + sec(x)", "Calculate dy/dx for y = -5^x + sec(x)"]),
        (65, "4*sqrt(x) + 3*x^2", "2/sqrt(x) + 6*x", "power_rule_derivative", "derivative",
         ["Find the derivative of y = 4*sqrt(x) + 3*x^2", "Differentiate y = 4sqrt(x) + 3x^2"]),
        (66, "x^3 + 3^x + 3*x", "3*x^2 + 3^x*ln(3) + 3", "log_exp_derivative", "derivative",
         ["Find the derivative of y = x^3 + 3^x + 3*x", "Calculate dy/dx for y = x^3 + 3^x + 3x"]),

        # Page 25 (#67 - #69)
        (67, "5*sqrt(x) + 5/x", "5/(2*sqrt(x)) - 5/x^2", "power_rule_derivative", "derivative",
         ["Find the derivative of y = 5*sqrt(x) + 5/x", "Differentiate y = 5sqrt(x) + 5/x"]),
        (68, "tan(x) - sin(x)", "sec(x)^2 - cos(x)", "trig_derivative", "derivative",
         ["Find the derivative of y = tan(x) - sin(x)", "Calculate dy/dx for y = tan(x) - sin(x)"]),
        (69, "sqrt(x) - 4*sec(x)", "1/(2*sqrt(x)) - 4*sec(x)*tan(x)", "derivative", "derivative",
         ["Find the derivative of y = sqrt(x) - 4*sec(x)", "Differentiate y = sqrt(x) - 4sec(x)"]),

        # Page 26 (#70 - #72)
        (70, "exp(x) + 3^x", "exp(x) + 3^x*ln(3)", "log_exp_derivative", "derivative",
         ["Find the derivative of y = e^x + 3^x", "Calculate dy/dx for y = e^x + 3^x"]),
        (71, "4*x^2 + 2/x^4", "8*x - 8/x^5", "power_rule_derivative", "derivative",
         ["Find the derivative of y = 4*x^2 + 2/x^4", "Differentiate y = 4x^2 + 2/x^4"]),
        (72, "x^4 + x^3 + 2*x^2 + sqrt(x)", "4*x^3 + 3*x^2 + 4*x + 1/(2*sqrt(x))", "power_rule_derivative", "derivative",
         ["Find the derivative of y = x^4 + x^3 + 2*x^2 + sqrt(x)", "Calculate dy/dx for y = x^4 + x^3 + 2x^2 + sqrt(x)"]),

        # Page 27 (#73 - #75)
        (73, "6^x - cos(x)", "6^x*ln(6) + sin(x)", "log_exp_derivative", "derivative",
         ["Find the derivative of y = 6^x - cos(x)", "Differentiate y = 6^x - cos(x)"]),
        (74, "4/x^3 + 2/x^2", "-12/x^4 - 4/x^3", "power_rule_derivative", "derivative",
         ["Find the derivative of y = 4/x^3 + 2/x^2", "Calculate dy/dx for y = 4/x^3 + 2/x^2"]),
        (75, "10*sin(x) + 10^x", "10*cos(x) + 10^x*ln(10)", "log_exp_derivative", "derivative",
         ["Find the derivative of y = 10*sin(x) + 10^x", "Differentiate y = 10sin(x) + 10^x"]),

        # Page 28 (#76 - #78) Base a logarithms
        (76, "log_3(x)", "1/(x*ln(3))", "log_exp_derivative", "derivative",
         ["Find the derivative of y = log_3(x)", "Calculate dy/dx for y = log3(x)"]),
        (77, "6*sqrt(x) - 6/x + log_6(x)", "3/sqrt(x) + 6/x^2 + 1/(x*ln(6))", "log_exp_derivative", "derivative",
         ["Find the derivative of y = 6*sqrt(x) - 6/x + log_6(x)", "Differentiate y = 6sqrt(x) - 6/x + log6(x)"]),
        (78, "2*sin(x) + exp(x)", "2*cos(x) + exp(x)", "derivative", "derivative",
         ["Find the derivative of y = 2*sin(x) + e^x", "Calculate dy/dx for y = 2sin(x) + e^x"]),

        # Page 29 (#79 - #81)
        (79, "x^4 + 3*x^2 - 1", "4*x^3 + 6*x", "power_rule_derivative", "derivative",
         ["Find the derivative of y = x^4 + 3*x^2 - 1", "Differentiate y = x^4 + 3x^2 - 1"]),
        (80, "16*x^2 + log_10(x)", "32*x + 1/(x*ln(10))", "log_exp_derivative", "derivative",
         ["Find the derivative of y = 16*x^2 + log(x)", "Calculate dy/dx for y = 16x^2 + log10(x)"]),
        (81, "3*x^2 - 4*x + 6", "6*x - 4", "power_rule_derivative", "derivative",
         ["Find the derivative of y = 3*x^2 - 4*x + 6", "Differentiate y = 3x^2 - 4x + 6"]),

        # Page 30 (#82 - #84)
        (82, "2*tan(x) + ln(x)", "2*sec(x)^2 + 1/x", "derivative", "derivative",
         ["Find the derivative of y = 2*tan(x) + ln(x)", "Calculate dy/dx for y = 2tan(x) + ln(x)"]),
        (83, "16*sin(x) + sqrt(x)", "16*cos(x) + 1/(2*sqrt(x))", "derivative", "derivative",
         ["Find the derivative of y = 16*sin(x) + sqrt(x)", "Differentiate y = 16sin(x) + sqrt(x)"]),
        (84, "14*x^2 - ln(x) - 4^x", "28*x - 1/x - 4^x*ln(4)", "log_exp_derivative", "derivative",
         ["Find the derivative of y = 14*x^2 - ln(x) - 4^x", "Calculate dy/dx for y = 14x^2 - ln(x) - 4^x"]),

        # Page 32 (#88 - #93)
        (88, "6*log_3(x) + 100", "6/(x*ln(3))", "log_exp_derivative", "derivative",
         ["Find the derivative of y = 6*log_3(x) + 100", "Calculate dy/dx for y = 6log3(x) + 100"]),
        (89, "csc(x) + 2*x", "-csc(x)*cot(x) + 2", "trig_derivative", "derivative",
         ["Find the derivative of y = csc(x) + 2*x", "Differentiate y = csc(x) + 2x"]),
        (90, "4*sin(x) + 4*cos(x)", "4*cos(x) - 4*sin(x)", "trig_derivative", "derivative",
         ["Find the derivative of y = 4*sin(x) + 4*cos(x)", "Calculate dy/dx for y = 4sin(x) + 4cos(x)"]),
        (91, "3*x^3 - x^2 + 4*x + 10", "9*x^2 - 2*x + 4", "power_rule_derivative", "derivative",
         ["Find the derivative of y = 3*x^3 - x^2 + 4*x + 10", "Differentiate y = 3x^3 - x^2 + 4x + 10"]),
        (92, "1/x^2 + ln(x)", "-2/x^3 + 1/x", "log_exp_derivative", "derivative",
         ["Find the derivative of y = 1/x^2 + ln(x)", "Calculate dy/dx for y = 1/x^2 + ln(x)"]),
        (93, "4^x + 5^x - 6", "4^x*ln(4) + 5^x*ln(5)", "log_exp_derivative", "derivative",
         ["Find the derivative of y = 4^x + 5^x - 6", "Differentiate y = 4^x + 5^x - 6"]),

        # Page 34 (#94 - #96)
        (94, "6*x^3 - 10*x + 7*sin(x)", "18*x^2 - 10 + 7*cos(x)", "derivative", "derivative",
         ["Find the derivative of y = 6*x^3 - 10*x + 7*sin(x)", "Differentiate y = 6x^3 - 10x + 7sin(x)"]),
        (95, "1/sqrt(x) - 2*x^3", "-1/(2*x^(3/2)) - 6*x^2", "power_rule_derivative", "derivative",
         ["Find the derivative of y = 1/sqrt(x) - 2*x^3", "Calculate dy/dx for y = 1/sqrt(x) - 2x^3"]),
        (96, "48*x^2 + 1/x", "96*x - 1/x^2", "power_rule_derivative", "derivative",
         ["Find the derivative of y = 48*x^2 + 1/x", "Differentiate y = 48x^2 + 1/x"]),

        # Page 35 (#97 - #99)
        (97, "cot(x) - sin(x)", "-csc(x)^2 - cos(x)", "trig_derivative", "derivative",
         ["Find the derivative of y = cot(x) - sin(x)", "Calculate dy/dx for y = cot(x) - sin(x)"]),
        (98, "100*sin(x)", "100*cos(x)", "trig_derivative", "derivative",
         ["Find the derivative of y = 100*sin(x)", "Differentiate y = 100sin(x)"]),
        (99, "tan(pi) - cos(pi)", "0", "derivative", "derivative",
         ["Find the derivative of y = tan(pi) - cos(pi)", "Calculate dy/dx for y = tan(pi) - cos(pi)"]),

        # Page 36 (#100 - #102)
        (100, "x^(1/5) - x^(1/3)", "1/(5*x^(4/5)) - 1/(3*x^(2/3))", "power_rule_derivative", "derivative",
         ["Find the derivative of y = root(5, x) - root(3, x)", "Differentiate y = x^(1/5) - x^(1/3)"]),
        (101, "ln(x) + exp(x) + log_10(x)", "1/x + exp(x) + 1/(x*ln(10))", "log_exp_derivative", "derivative",
         ["Find the derivative of y = ln(x) + e^x + log(x)", "Calculate dy/dx for y = ln(x) + e^x + log(x)"]),
        (102, "x^2 + 5*x - 6", "2*x + 5", "power_rule_derivative", "derivative",
         ["Find the derivative of y = x^2 + 5*x - 6", "Differentiate y = x^2 + 5x - 6"]),

        # Page 37 (#103 - #105)
        (103, "3*sqrt(x) - 2*x", "3/(2*sqrt(x)) - 2", "power_rule_derivative", "derivative",
         ["Find the derivative of y = 3*sqrt(x) - 2*x", "Calculate dy/dx for y = 3sqrt(x) - 2x"]),
        (104, "4*x^3 - x + 10", "12*x^2 - 1", "power_rule_derivative", "derivative",
         ["Find the derivative of y = 4*x^3 - x + 10", "Differentiate y = 4x^3 - x + 10"]),
        (105, "log_7(x) - sin(x)", "1/(x*ln(7)) - cos(x)", "log_exp_derivative", "derivative",
         ["Find the derivative of y = log_7(x) - sin(x)", "Calculate dy/dx for y = log7(x) - sin(x)"]),

        # Page 38 (#106 - #108)
        (106, "tan(x) - 2*x^2", "sec(x)^2 - 4*x", "trig_derivative", "derivative",
         ["Find the derivative of y = tan(x) - 2*x^2", "Differentiate y = tan(x) - 2x^2"]),
        (107, "6*x^2 - 7*x + 8", "12*x - 7", "power_rule_derivative", "derivative",
         ["Find the derivative of y = 6*x^2 - 7*x + 8", "Calculate dy/dx for y = 6x^2 - 7x + 8"]),
        (108, "-8*sin(x) + 10*exp(x)", "-8*cos(x) + 10*exp(x)", "derivative", "derivative",
         ["Find the derivative of y = -8*sin(x) + 10*e^x", "Differentiate y = -8sin(x) + 10e^x"]),

        # Page 39 (#109 - #111)
        (109, "16 + tan(0) - sin(pi/2)", "0", "derivative", "derivative",
         ["Find the derivative of y = 16 + tan(0) - sin(pi/2)", "Calculate dy/dx for y = 16 + tan(0) - sin(pi/2)"]),
        (110, "sqrt(x) + 1/x^2", "1/(2*sqrt(x)) - 2/x^3", "power_rule_derivative", "derivative",
         ["Find the derivative of y = sqrt(x) + 1/x^2", "Differentiate y = sqrt(x) + 1/x^2"]),
        (111, "2*x^5 - 6*x^4 + x^3 - 7*x^2 - 10", "10*x^4 - 24*x^3 + 3*x^2 - 14*x", "power_rule_derivative", "derivative",
         ["Find the derivative of y = 2*x^5 - 6*x^4 + x^3 - 7*x^2 - 10", "Calculate dy/dx for y = 2x^5 - 6x^4 + x^3 - 7x^2 - 10"]),

        # Page 40 (#112 - #114)
        (112, "cos(x) + 15*x^3", "-sin(x) + 45*x^2", "trig_derivative", "derivative",
         ["Find the derivative of y = cos(x) + 15*x^3", "Differentiate y = cos(x) + 15x^3"]),
        (113, "-4*x^2 + tan(x)", "-8*x + sec(x)^2", "trig_derivative", "derivative",
         ["Find the derivative of y = -4*x^2 + tan(x)", "Calculate dy/dx for y = -4x^2 + tan(x)"]),
        (114, "-6^x - 15", "-6^x*ln(6)", "log_exp_derivative", "derivative",
         ["Find the derivative of y = -6^x - 15", "Differentiate y = -6^x - 15"]),

        # Page 41 (#115 - #117)
        (115, "1/x^70 + sqrt(x)", "-70/x^71 + 1/(2*sqrt(x))", "power_rule_derivative", "derivative",
         ["Find the derivative of y = 1/x^70 + sqrt(x)", "Calculate dy/dx for y = 1/x^70 + sqrt(x)"]),
        (116, "tan(x) - sec(x)", "sec(x)^2 - sec(x)*tan(x)", "trig_derivative", "derivative",
         ["Find the derivative of y = tan(x) - sec(x)", "Differentiate y = tan(x) - sec(x)"]),
        (117, "4*x^4 + 3*x^3 - 5*x^2 + 1", "16*x^3 + 9*x^2 - 10*x", "power_rule_derivative", "derivative",
         ["Find the derivative of 4*x^4 + 3*x^3 - 5*x^2 + 1", "Calculate dy/dx for y = 4x^4 + 3x^3 - 5x^2 + 1"]),

        # Page 42 (#118 - #120)
        (118, "sin(x) + 4", "cos(x)", "trig_derivative", "derivative",
         ["Find the derivative of y = sin(x) + 4", "Differentiate y = sin(x) + 4"]),
        (119, "14/x - 6/x^2", "-14/x^2 + 12/x^3", "power_rule_derivative", "derivative",
         ["Find the derivative of y = 14/x - 6/x^2", "Calculate dy/dx for y = 14/x - 6/x^2"]),
        (120, "7*sqrt(x) + sec(x)", "7/(2*sqrt(x)) + sec(x)*tan(x)", "derivative", "derivative",
         ["Find the derivative of y = 7*sqrt(x) + sec(x)", "Differentiate y = 7sqrt(x) + sec(x)"]),

        # Page 44 (#124 - #126)
        (124, "6*x^2 + 1/x", "12*x - 1/x^2", "power_rule_derivative", "derivative",
         ["Find the derivative of y = 6*x^2 + 1/x", "Differentiate y = 6x^2 + 1/x"]),
        (125, "x^3 + x^2 - 6*x + 6/x", "3*x^2 + 2*x - 6 - 6/x^2", "power_rule_derivative", "derivative",
         ["Find the derivative of y = x^3 + x^2 - 6*x + 6/x", "Calculate dy/dx for y = x^3 + x^2 - 6x + 6/x"]),
        (126, "x^(1/4) + cot(x)", "1/(4*x^(3/4)) - csc(x)^2", "derivative", "derivative",
         ["Find the derivative of y = root(4, x) + cot(x)", "Differentiate y = x^(1/4) + cot(x)"]),

        # Page 45 (#127 - #129)
        (127, "10*x^2 + 10^x", "20*x + 10^x*ln(10)", "log_exp_derivative", "derivative",
         ["Find the derivative of y = 10*x^2 + 10^x", "Calculate dy/dx for y = 10x^2 + 10^x"]),
        (128, "4*x + log_7(x)", "4 + 1/(x*ln(7))", "log_exp_derivative", "derivative",
         ["Find the derivative of y = 4*x + log_7(x)", "Differentiate y = 4x + log7(x)"]),
        (129, "sin(x) + cos(x) - tan(x)", "cos(x) - sin(x) - sec(x)^2", "trig_derivative", "derivative",
         ["Find the derivative of y = sin(x) + cos(x) - tan(x)", "Calculate dy/dx for y = sin(x) + cos(x) - tan(x)"]),

        # Page 46 (#130 - #132)
        (130, "5*x^3 + 3*x^2 - 40*x + 1", "15*x^2 + 6*x - 40", "power_rule_derivative", "derivative",
         ["Find the derivative of y = 5*x^3 + 3*x^2 - 40*x + 1", "Differentiate y = 5x^3 + 3x^2 - 40x + 1"]),
        (131, "40*x^2 - sqrt(x) + (1/3)*x^(1/3)", "80*x - 1/(2*sqrt(x)) + 1/(9*x^(2/3))", "power_rule_derivative", "derivative",
         ["Find the derivative of y = 40*x^2 - sqrt(x) + (1/3)*root(3, x)", "Calculate dy/dx for y = 40x^2 - sqrt(x) + (1/3)*x^(1/3)"]),
        (132, "7*sin(x) - csc(x)", "7*cos(x) + csc(x)*cot(x)", "trig_derivative", "derivative",
         ["Find the derivative of y = 7*sin(x) - csc(x)", "Differentiate y = 7sin(x) - csc(x)"]),

        # Page 47 (#133 - #135)
        (133, "tan(x) - sin(x)", "sec(x)^2 - cos(x)", "trig_derivative", "derivative",
         ["Find the derivative of y = tan(x) - sin(x)", "Calculate dy/dx for y = tan(x) - sin(x)"]),
        (134, "40*x^3 - 6*x^2", "120*x^2 - 12*x", "power_rule_derivative", "derivative",
         ["Find the derivative of y = 40*x^3 - 6*x^2", "Differentiate y = 40x^3 - 6x^2"]),
        (135, "log_2(x) + 7^x", "1/(x*ln(2)) + 7^x*ln(7)", "log_exp_derivative", "derivative",
         ["Find the derivative of y = log_2(x) + 7^x", "Calculate dy/dx for y = log2(x) + 7^x"]),

        # Page 48 (#136 - #138)
        (136, "36 - 40*ln(x)", "-40/x", "log_exp_derivative", "derivative",
         ["Find the derivative of y = 36 - 40*ln(x)", "Differentiate y = 36 - 40ln(x)"]),
        (137, "ln(x) + x^(1/3)", "1/x + 1/(3*x^(2/3))", "log_exp_derivative", "derivative",
         ["Find the derivative of y = ln(x) + root(3, x)", "Calculate dy/dx for y = ln(x) + x^(1/3)"]),
        (138, "sec(x) + 6*cos(x)", "sec(x)*tan(x) - 6*sin(x)", "trig_derivative", "derivative",
         ["Find the derivative of y = sec(x) + 6*cos(x)", "Differentiate y = sec(x) + 6cos(x)"]),

        # Page 49 (#139 - #141)
        (139, "3*x^4 + 6*x^3 - 4^x", "12*x^3 + 18*x^2 - 4^x*ln(4)", "log_exp_derivative", "derivative",
         ["Find the derivative of y = 3*x^4 + 6*x^3 - 4^x", "Calculate dy/dx for y = 3x^4 + 6x^3 - 4^x"]),
        (140, "cot(x) + csc(x)", "-csc(x)^2 - csc(x)*cot(x)", "trig_derivative", "derivative",
         ["Find the derivative of y = cot(x) + csc(x)", "Differentiate y = cot(x) + csc(x)"]),
        (141, "40*x^2 - log_4(x)", "80*x - 1/(x*ln(4))", "log_exp_derivative", "derivative",
         ["Find the derivative of y = 40*x^2 - log_4(x)", "Calculate dy/dx for y = 40x^2 - log4(x)"]),

        # Page 50 (#142 - #144)
        (142, "sin(x) - 7*cos(x) + 10*x", "cos(x) + 7*sin(x) + 10", "trig_derivative", "derivative",
         ["Find the derivative of y = sin(x) - 7*cos(x) + 10*x", "Differentiate y = sin(x) - 7cos(x) + 10x"]),
        (143, "-6*x^4 + 3*x^2 + 1/x", "-24*x^3 + 6*x - 1/x^2", "power_rule_derivative", "derivative",
         ["Find the derivative of y = -6*x^4 + 3*x^2 + 1/x", "Calculate dy/dx for y = -6x^4 + 3x^2 + 1/x"]),
        (144, "sqrt(x) - 1/x^2", "1/(2*sqrt(x)) + 2/x^3", "power_rule_derivative", "derivative",
         ["Find the derivative of y = sqrt(x) - 1/x^2", "Differentiate y = sqrt(x) - 1/x^2"]),

        # Page 51 (#145 - #147)
        (145, "sin(3*pi) - cos(pi)", "0", "derivative", "derivative",
         ["Find the derivative of y = sin(3*pi) - cos(pi)", "Calculate dy/dx for y = sin(3*pi) - cos(pi)"]),
        (146, "tan(x) - sin(pi/2)", "sec(x)^2", "trig_derivative", "derivative",
         ["Find the derivative of y = tan(x) - sin(pi/2)", "Differentiate y = tan(x) - sin(pi/2)"]),
        (147, "5^x + ln(x)", "5^x*ln(5) + 1/x", "log_exp_derivative", "derivative",
         ["Find the derivative of y = 5^x + ln(x)", "Calculate dy/dx for y = 5^x + ln(x)"]),

        # Page 52 (#148 - #150)
        (148, "sqrt(x) + x^(1/4)", "1/(2*sqrt(x)) + 1/(4*x^(3/4))", "power_rule_derivative", "derivative",
         ["Find the derivative of y = sqrt(x) + root(4, x)", "Differentiate y = sqrt(x) + x^(1/4)"]),
        (149, "1/x^2 + 2*x", "-2/x^3 + 2", "power_rule_derivative", "derivative",
         ["Find the derivative of y = 1/x^2 + 2*x", "Calculate dy/dx for y = 1/x^2 + 2x"]),
        (150, "x^(1/3) - 1/x", "1/(3*x^(2/3)) + 1/x^2", "power_rule_derivative", "derivative",
         ["Find the derivative of y = root(3, x) - 1/x", "Differentiate y = x^(1/3) - 1/x"]),
    ]

    for item in problems_data:
        p_num, expr, ans, tpl, tgt, phrasings = item
        for q in phrasings:
            entries.append(make_entry(q, tpl, {"expr": expr, "answer": ans}, tgt))

    # Tangent line slope problems (#85–#87 and #121–#123)
    tangent_slope_data = [
        # Page 31 (#85 - #87 at x = 0)
        ("-6*sin(x) + 4*exp(x)", "0", "-2", [
            "Find the slope of the tangent line at the point x=0 for y = -6*sin(x) + 4*e^x",
            "Find the slope of the tangent line to y = -6*sin(x) + 4*exp(x) at x = 0",
            "What is the slope of the tangent line to y = -6sin(x) + 4e^x at x = 0?",
        ]),
        ("3^x - 4*x^2", "0", "ln(3)", [
            "Find the slope of the tangent line at the point x=0 for y = 3^x - 4*x^2",
            "Find the slope of the tangent line to y = 3^x - 4*x^2 at x = 0",
            "Calculate the slope of the tangent line for y = 3^x - 4x^2 at x = 0",
        ]),
        ("-4*x + 5*tan(x)", "0", "1", [
            "Find the slope of the tangent line at the point x=0 for y = -4*x + 5*tan(x)",
            "Find the slope of the tangent line to y = -4*x + 5*tan(x) at x = 0",
            "What is the slope of the tangent line for y = -4x + 5tan(x) at x = 0?",
        ]),

        # Page 43 (#121 - #123 at x = pi)
        ("exp(x) - 2*sin(x)", "pi", "2 + exp(pi)", [
            "Find the slope of the tangent line for the function at x = pi: y = e^x - 2*sin(x)",
            "Find the slope of the tangent line to y = exp(x) - 2*sin(x) at x = pi",
            "Calculate the slope of the tangent line for y = e^x - 2sin(x) at x = pi",
        ]),
        ("exp(x) - 3*cos(x)", "pi", "exp(pi)", [
            "Find the slope of the tangent line for the function at x = pi: y = e^x - 3*cos(x)",
            "Find the slope of the tangent line to y = exp(x) - 3*cos(x) at x = pi",
            "Calculate the slope of the tangent line for y = e^x - 3cos(x) at x = pi",
        ]),
        ("4^x + tan(x)", "pi", "1 + 4^pi*ln(4)", [
            "Find the slope of the tangent line for the function at x = pi: y = 4^x + tan(x)",
            "Find the slope of the tangent line to y = 4^x + tan(x) at x = pi",
            "Calculate the slope of the tangent line for y = 4^x + tan(x) at x = pi",
        ]),
    ]

    for f_expr, x0_val, m_val, phrasings in tangent_slope_data:
        for q in phrasings:
            entries.append(make_entry(
                q, "tangent_slope_derivative",
                {"f": f_expr, "x0": x0_val, "m": m_val},
                "tangent_slope"
            ))

    # Incomplete slot checks for robustness
    entries.append(make_entry(
        "Find the slope of the tangent line at the point x=0",
        "tangent_slope_derivative",
        {"f": None, "x0": "0", "m": None},
        "tangent_slope",
        False, ["f"]
    ))
    entries.append(make_entry(
        "Find the slope of the tangent line to y = 3^x - 4*x^2",
        "tangent_slope_derivative",
        {"f": "3^x - 4*x^2", "x0": None, "m": None},
        "tangent_slope",
        False, ["x0"]
    ))

    return entries

def generate_way2():
    """
    Parametric generator creating 350+ mathematically verified derivative variations:
      - Arbitrary base logarithms log_a(x) for a in [2..12]
      - Arbitrary base exponentials a^x for a in [2..12]
      - Tangent slopes at x0 in {0, 1, 2, -1, pi, pi/2}
      - Constant trig traps
      - Linear combinations of polynomials, roots, reciprocals, trig, and exp/log
    """
    entries = []
    random.seed(100)

    # 1. Arbitrary Base Logarithms log_a(x)
    for _ in range(60):
        a = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 12])
        c = random.randint(1, 10) * random.choice([1, -1])
        c2 = random.randint(1, 10) * random.choice([1, -1])
        deg = random.choice([1, 2, 3])

        expr_sym = c * (sympy.log(x) / sympy.log(a)) + c2 * x**deg
        d_sym = diff(expr_sym, x)

        expr_str = f"{c}*log_{a}(x) + {c2}*x^{deg}" if c2 > 0 else f"{c}*log_{a}(x) - {abs(c2)}*x^{deg}"
        ans_str = str(d_sym).replace("**", "^").replace("log(", "ln(")

        q = random.choice([
            f"Find the derivative of y = {expr_str}",
            f"Calculate dy/dx for y = {expr_str}",
            f"Differentiate {expr_str} with respect to x",
        ])
        entries.append(make_entry(q, "log_exp_derivative", {"expr": expr_str, "answer": ans_str}, "derivative"))

    # 2. Arbitrary Base Exponentials a^x
    for _ in range(60):
        a = random.choice([2, 3, 4, 5, 6, 7, 8, 10])
        c = random.randint(1, 8) * random.choice([1, -1])
        trig_or_poly = random.choice([sympy.sin(x), sympy.cos(x), x**2, x**3])

        expr_sym = c * a**x + trig_or_poly
        d_sym = diff(expr_sym, x)

        expr_str = str(expr_sym).replace("**", "^")
        ans_str = str(d_sym).replace("**", "^").replace("log(", "ln(")

        q = random.choice([
            f"Find the derivative of y = {expr_str}",
            f"Calculate dy/dx for y = {expr_str}",
            f"Differentiate y = {expr_str} with respect to x",
        ])
        entries.append(make_entry(q, "log_exp_derivative", {"expr": expr_str, "answer": ans_str}, "derivative"))

    # 3. Tangent Slope at a Point x0
    for _ in range(70):
        x0_choice = random.choice([0, 1, 2, -1, "pi"])
        x0_val = sympy.pi if x0_choice == "pi" else sympy.Integer(x0_choice)
        x0_str = "pi" if x0_choice == "pi" else str(x0_choice)

        c1 = random.randint(1, 6) * random.choice([1, -1])
        c2 = random.randint(1, 6) * random.choice([1, -1])
        fn1 = random.choice([sympy.exp(x), sympy.sin(x), sympy.cos(x), x**2, x**3])
        fn2 = random.choice([sympy.tan(x), sympy.exp(x), x**2, 2**x, 3**x])

        f_sym = c1 * fn1 + c2 * fn2
        df_sym = diff(f_sym, x)
        m_eval = sympy.simplify(df_sym.subs(x, x0_val))

        f_str = str(f_sym).replace("**", "^")
        m_str = str(m_eval).replace("**", "^").replace("log(", "ln(")

        q = random.choice([
            f"Find the slope of the tangent line to y = {f_str} at x = {x0_str}",
            f"Find the slope of the tangent line at the point x={x0_str} for y = {f_str}",
            f"Calculate the slope of the tangent line for y = {f_str} at x = {x0_str}",
        ])
        entries.append(make_entry(q, "tangent_slope_derivative", {"f": f_str, "x0": x0_str, "m": m_str}, "tangent_slope"))

    # 4. Constant Trigonometric and Transcendental Traps
    const_traps = [
        "sin(pi)", "cos(pi)", "tan(0)", "sin(pi/2)", "cos(pi/2)", "sin(2*pi)",
        "tan(pi)", "cos(2*pi)", "sin(3*pi)", "cos(3*pi)", "exp(0)", "ln(1)"
    ]
    for _ in range(40):
        c_trap = random.choice(const_traps)
        deg = random.randint(2, 5)
        c_poly = random.randint(2, 20)

        expr_str = f"{c_poly}*x^{deg} + {c_trap}"
        ans_str = f"{c_poly * deg}*x^{deg - 1}"

        q = random.choice([
            f"Find the derivative of y = {expr_str}",
            f"Calculate dy/dx for y = {expr_str}",
            f"Differentiate y = {expr_str} with respect to x",
        ])
        entries.append(make_entry(q, "derivative", {"expr": expr_str, "answer": ans_str}, "derivative"))

    # 5. Mixed Polynomials, Radicals, and Laurent Negative Powers
    for _ in range(120):
        k = random.randint(1, 25)
        m = random.choice([2, 3, 4, 5])
        c1 = random.randint(1, 10) * random.choice([1, -1])
        c2 = random.randint(1, 10) * random.choice([1, -1])

        expr_sym = c1 / x**k + c2 * x**(sympy.Rational(1, m))
        d_sym = diff(expr_sym, x)

        expr_str = str(expr_sym).replace("**", "^")
        ans_str = str(d_sym).replace("**", "^")

        q = random.choice([
            f"Find the derivative of y = {expr_str} using the power rule",
            f"Calculate dy/dx for y = {expr_str}",
            f"Differentiate y = {expr_str} with respect to x",
        ])
        entries.append(make_entry(q, "power_rule_derivative", {"expr": expr_str, "answer": ans_str}, "derivative"))

    return entries

def main():
    dataset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "verimath_finetune_dataset.jsonl"))
    print(f"Loading existing dataset from: {dataset_path}")
    
    existing_entries = []
    if os.path.exists(dataset_path):
        with open(dataset_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    existing_entries.append(json.loads(line))
    print(f"Existing entries: {len(existing_entries)}")

    way1 = generate_way1()
    print(f"Generated Way 1 (Authentic #19–#150 & Tangent Slopes): {len(way1)} examples")

    way2 = generate_way2()
    print(f"Generated Way 2 (Parametric Generalization): {len(way2)} examples")

    new_entries = way1 + way2
    print(f"Total new entries to append: {len(new_entries)}")

    # Check templates exist in registry
    for e in new_entries:
        asst = json.loads(e["messages"][2]["content"])
        tpl_id = asst["template"]
        assert tpl_id in TEMPLATES, f"Template {tpl_id} not in registry!"

    # Append to dataset
    with open(dataset_path, "a", encoding="utf-8") as f:
        for item in new_entries:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"Successfully appended {len(new_entries)} entries.")
    total = len(existing_entries) + len(new_entries)
    print(f"New total dataset size: {total} examples")

if __name__ == "__main__":
    main()
