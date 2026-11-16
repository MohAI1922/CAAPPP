"""
VeriMath — Book of Integrals Answer Key (#217–#438) Two-Way Dataset Generator
============================================================================
Processes Book of Integrals Official Answer Key Pages 202–221:
  - Wallis Definite Integrals (#217–#219, #295)
  - Product-to-Sum Trig Integrals (#220–#223, #294)
  - Weierstrass Substitution Integrals (#224–#235, #341, #371, #382)
  - Radical Species & Euler Substitution (#236–#244, #277, #290, #292, #293, #302, #303, #312, #316, #321, #323, #332, #353, #361, #362, #363, #384, #385, #418)
  - FTC Definite Integrals (#245–#251, #330, #342)
  - Absolute Value Definite Integrals (#252–#257, #336)
  - King's Rule Contest Integrals (#258–#265, #325, #398, #404, #414, #424)
  - S.E-One Symmetry Method (#266–#269, #329, #409)
  - P.U.N. Integrals (#270, #365, #370)
  - Root Manipulation Integrals (#280, #288, #350, #351, #357)
  - Trig Substitution Integrals (#271, #281, #284, #340, #346, #391, #402, #413)
  - Trig Power Reduction Integrals (#272, #291, #314, #386, #392, #410, #422)
  - Integration by Parts & Ghost Functions (#276, #282, #305, #309, #318, #322, #348, #356, #359, #360, #376, #379, #396, #399, #411, #412)
  - Partial Fractions (#278, #279, #285, #289, #298, #300, #301, #315, #317, #335, #358, #367, #375, #390, #403, #406, #407, #415, #416, #419)
  - PFD Linear Power Ratio Trick (#310, #311, #347)
  - Euler's Formula Integration (#372, #373)
  - Conjugate Radical Rationalizing (#381, #395)
  - Infinite Nested Radicals (#397)
  - Exponential Derivative Sum Rule (#393)
  - Feynman's Technique (#417, #423, #425, #426)
  - Series Expansion Definite Integrals (#427–#432)
  - Euler Dilogarithm Function (#433–#438)

Pathway 1: Authentic textbook problem formulations.
Pathway 2: Parametric / randomized generalization variations.
"""

import json
import os
import random
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.templates.registry import TEMPLATES, classify_problem

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

    # 1. Wallis Integrals (#217, #218, #219, #295)
    wallis_data = [
        ("2*cos(x)^3", "0", "pi/2", "4/3", "Evaluate the definite integral of 2*cos(x)^3 from 0 to pi/2 using Wallis formula"),
        ("4*sin(x)^2", "0", "pi/2", "pi", "Calculate the definite integral of 4*sin(x)^2 from 0 to pi/2 using Wallis formula"),
        ("cos(x)^7", "0", "pi/2", "16/35", "Evaluate the definite integral of cos(x)^7 from 0 to pi/2 using Wallis property"),
        ("sin(x)^4*cos(x)^2", "0", "pi/2", "pi/32", "Find the definite integral of sin(x)^4*cos(x)^2 from 0 to pi/2 using Wallis formula"),
        ("sin(x)^6", "0", "pi/2", "5*pi/32", "Evaluate \\int_0^{pi/2} sin(x)^6 dx using Wallis formula"),
        ("cos(x)^5", "0", "pi/2", "8/15", "Calculate the definite integral of cos(x)^5 from 0 to pi/2 using Wallis formula"),
        ("sin(x)^8", "0", "pi/2", "35*pi/256", "Evaluate the definite integral of sin(x)^8 from 0 to pi/2 using Wallis formula"),
    ]
    for expr, low, up, ans, q in wallis_data:
        entries.append(make_entry(q, "wallis_integral", {"expr": expr, "lower": low, "upper": up, "answer": ans}, "definite_integral"))
    entries.append(make_entry("Evaluate the trig power on [0, pi/2] using Wallis formula", "wallis_integral", {"expr": None, "lower": "0", "upper": "pi/2", "answer": None}, "definite_integral", False, ["expr"]))

    # 2. Product-to-Sum Trig (#220, #221, #222, #223, #294)
    p2s_data = [
        ("sin(2*x)*sin(3*x)", "-cos(5*x)/10 + cos(x)/2", "Integrate sin(2*x)*sin(3*x) dx using product to sum formulas"),
        ("cos(3*x)*sin(4*x)", "-cos(7*x)/14 - cos(x)/2", "Find \\int cos(3*x)*sin(4*x) dx using product to sum trig formulas"),
        ("sin(x)*cos(3*x)", "-cos(4*x)/8 + cos(2*x)/4", "Evaluate \\int sin(x)*cos(3*x) dx by product-to-sum identities"),
        ("sin(3*x)*sin(4*x)", "-sin(7*x)/14 + sin(x)/2", "Integrate sin(3*x)*sin(4*x) dx using product to sum formulas"),
        ("sin(x)*sin(2*x)*sin(3*x)", "(12*x + 3*sin(2*x) - 3*sin(4*x) - sin(6*x))/192", "Evaluate \\int sin(x)*sin(2*x)*sin(3*x) dx using product to sum"),
        ("cos(2*x)*cos(5*x)", "sin(7*x)/14 + sin(3*x)/6", "Find the integral of cos(2*x)*cos(5*x) dx using product to sum formulas"),
    ]
    for expr, ant, q in p2s_data:
        entries.append(make_entry(q, "product_to_sum_trig_integral", {"expr": expr, "antideriv": ant}, "antiderivative"))

    # 3. Weierstrass Substitution (#224-#235, #341, #371, #382)
    weier_data = [
        ("1/(1 + sin(x))", "-2/(tan(x/2) + 1)", "Evaluate \\int 1/(1 + sin(x)) dx using Weierstrass substitution"),
        ("1/(2 + cos(x))", "(2*sqrt(3)/3)*arctan(tan(x/2)/sqrt(3))", "Integrate 1/(2 + cos(x)) dx using Weierstrass substitution t = tan(x/2)"),
        ("1/(5 - 4*cos(x))", "(2/3)*arctan(3*tan(x/2))", "Find \\int 1/(5 - 4*cos(x)) dx using Weierstrass substitution"),
        ("1/(3*sin(x) + 2*cos(x) + 1)", "(12/sqrt(5))*arctan((3*tan(x/2)-2)/sqrt(5))", "Evaluate \\int 1/(3*sin(x) + 2*cos(x) + 1) dx by Weierstrass substitution"),
        ("1/(1 + cos(2*x))", "tan(x)/2", "Integrate 1/(1 + cos(2*x)) dx using Weierstrass substitution"),
        ("(1 - cos(x))/(1 + cos(x))", "2*tan(x/2) - x", "Find \\int (1 - cos(x))/(1 + cos(x)) dx using Weierstrass substitution"),
        ("1/(sin(x) + cos(x) + sqrt(2))", "-sqrt(2)/(tan(x/2) + 1 - sqrt(2))", "Evaluate \\int 1/(sin(x) + cos(x) + sqrt(2)) dx using Weierstrass substitution"),
        ("1/(1 + sin(x) + cos(x))", "ln|tan(x/2) + 1|", "Integrate 1/(1 + sin(x) + cos(x)) dx using Weierstrass substitution"),
        ("1/(2 + sin(x) - cos(x))", "sqrt(2)*arctan((sqrt(3)*tan(x/2)+1)/sqrt(2))", "Evaluate \\int 1/(2 + sin(x) - cos(x)) dx using Weierstrass substitution"),
        ("1/(11*sin(x)^2 + 5*cos(x)^2)", "-(4/sqrt(55))*arctan(sqrt(5/11)*cot(x))", "Evaluate \\int 1/(11*sin(x)^2 + 5*cos(x)^2) dx using Weierstrass substitution"),
    ]
    for expr, ant, q in weier_data:
        entries.append(make_entry(q, "weierstrass_substitution_integral", {"expr": expr, "antideriv": ant}, "antiderivative"))

    # 4. Radical Species & Euler Substitution (#236-#244, #277, #290, #292, #293, #302, #303, #312, #316, #321, #323, #332, #353, #361, #362, #363, #384, #385, #418)
    rad_data = [
        ("1/((x+1)*sqrt(2*x+1))", "sqrt(2)*arctan(sqrt(2*x+1))", "Evaluate \\int 1/((x+1)*sqrt(2*x+1)) dx using radical species substitution"),
        ("1/((x-3)*sqrt(x^2-3))", "(1/sqrt(2))*arctan((x-3)/(sqrt(2)*sqrt(x^2-3)))", "Integrate 1/((x-3)*sqrt(x^2-3)) dx using radical species method"),
        ("1/((x+1)^2*sqrt((x+1)^2+1))", "-sqrt((x+1)^2+1)/(x+1)", "Find \\int 1/((x+1)^2*sqrt((x+1)^2+1)) dx using radical species substitution"),
        ("1/((2*x+1)*sqrt(x^2-x+3))", "-tanh^(-1)((7*x+2)/(2*sqrt(15)*sqrt(x^2-x+3)))/sqrt(15)", "Integrate 1/((2*x+1)*sqrt(x^2-x+3)) dx using radical species method"),
        ("x/((x^2+1)*sqrt(x^2+5))", "(1/2)*arctan(2*x/sqrt(x^2+5))", "Find \\int x/((x^2+1)*sqrt(x^2+5)) dx using radical species substitution"),
        ("1/((x-2)*sqrt(x^2-2*x+5))", "tanh^(-1)(2*(x-2)/(sqrt(5)*sqrt(x^2-2*x+5)))/(2*sqrt(5))", "Integrate 1/((x-2)*sqrt(x^2-2*x+5)) dx using radical species substitution"),
        ("(x+3)/sqrt(x^2+6*x+1)", "(1/2)*(x+3)*sqrt(x^2+6*x+1) - 4*ln|sqrt(x^2+6*x+1)+x+3|", "Integrate (x+3)/sqrt(x^2+6*x+1) dx using radical species method"),
        ("sqrt(x^2+6*x+18)", "(1/2)*(sqrt(x^2+6*x+18)*(x+3) + 9*asinh((x+3)/3))", "Find \\int sqrt(x^2+6*x+18) dx using radical species substitution"),
        ("(3*x+2)/sqrt(3*x^2+4*x+5)", "(1/6)*sqrt(3*x^2+4*x+5)*(3*x+2) + (11/(6*sqrt(3)))*asinh((3*x+2)/sqrt(11))", "Evaluate \\int (3*x+2)/sqrt(3*x^2+4*x+5) dx using radical species method"),
        ("sqrt(4*x-x^2)", "-5*(sqrt(4*x-x^2) + 4*asin(sqrt(1-x/4)))", "Find \\int sqrt(4*x-x^2) dx using radical species substitution"),
        ("1/sqrt(x^2+6*x+19)", "(1/sqrt(10))*ln|x+3 + sqrt(x^2+6*x+19)|", "Evaluate \\int 1/sqrt(x^2+6*x+19) dx using radical species method"),
    ]
    for expr, ant, q in rad_data:
        entries.append(make_entry(q, "radical_species_integral", {"expr": expr, "antideriv": ant}, "antiderivative"))

    # 5. Absolute Value Definite Integrals (#252-#257, #336)
    abs_data = [
        ("|x^2 - 4*x - 5|", "0", "10", "1106/3", "Evaluate the definite integral of |x^2 - 4*x - 5| from 0 to 10 using absolute value partition"),
        ("|x^3 - 3*x|", "-2", "3", "(56 + 13*sqrt(13))/3", "Evaluate the definite integral of |x^3 - 3*x| from -2 to 3 using absolute value partition"),
        ("|e^x - 2|", "-2", "3", "1/e^2 + e^3 + 2*(ln(256)-6)", "Find the definite integral of |e^x - 2| from -2 to 3 using absolute value partition"),
        ("|x^2 - 3*x + 2|", "0", "4", "40/3", "Evaluate the definite integral of |x^2 - 3*x + 2| from 0 to 4 using absolute value partition"),
        ("|sin(x) - 1/2|", "0", "2*pi", "26/3 + 32*sqrt(3)", "Find the definite integral of |sin(x) - 1/2| from 0 to 2*pi using absolute value partition"),
        ("|x^3 - 25*x|", "-5", "5", "240", "Evaluate the definite integral of |x^3 - 25*x| from -5 to 5 using absolute value partition"),
        ("|x^2 - 9|", "-6", "6", "765/2", "Evaluate the definite integral of |x^2 - 9| from -6 to 6 using absolute value partition"),
    ]
    for expr, low, up, ans, q in abs_data:
        entries.append(make_entry(q, "absolute_value_definite_integral", {"expr": expr, "lower": low, "upper": up, "answer": ans}, "definite_integral"))

    # 6. King's Rule Contest Integrals (#258-#265, #325, #398, #404, #414, #424)
    kings_data = [
        ("ln(1 + tan(x))", "0", "pi/4", "pi*ln(2)/8", "Evaluate the definite integral of ln(1 + tan(x)) from 0 to pi/4 using King's rule"),
        ("sin(x)/(sin(x) + cos(x))", "0", "pi/2", "pi/4", "Evaluate the definite integral of sin(x)/(sin(x) + cos(x)) from 0 to pi/2 using King's rule"),
        ("x^2/(x^2 + (1-x)^2)", "0", "1", "1/2", "Evaluate the definite integral of x^2/(x^2 + (1-x)^2) from 0 to 1 using King's property"),
        ("1/(1 + tan(x)^sqrt(2))", "0", "pi/2", "pi/4", "Evaluate the definite integral of 1/(1 + tan(x)^sqrt(2)) from 0 to pi/2 using King's rule"),
        ("x*sin(x)/(1 + cos(x)^2)", "0", "pi", "pi^2/4", "Evaluate the definite integral of x*sin(x)/(1 + cos(x)^2) from 0 to pi using King's rule"),
        ("x*ln(sin(x))", "0", "pi", "-pi^2*ln(2)/2", "Evaluate the definite integral of x*ln(sin(x)) from 0 to pi using King's rule"),
        ("ln(tan(x))", "0", "pi/2", "0", "Evaluate the definite integral of ln(tan(x)) from 0 to pi/2 using King's rule"),
        ("x/(1 + sin(x))", "0", "pi", "pi", "Evaluate the definite integral of x/(1 + sin(x)) from 0 to pi using King's rule"),
        ("cos(x)^2/(cos(x)^2 + 4*sin(x)^2)", "0", "pi/2", "pi/6", "Evaluate the definite integral of cos(x)^2/(cos(x)^2 + 4*sin(x)^2) from 0 to pi/2 using King's rule"),
        ("ln(x)/(1 + x^2)", "0", "oo", "0", "Evaluate the definite integral of ln(x)/(1 + x^2) from 0 to oo using King's involution"),
    ]
    for expr, low, up, ans, q in kings_data:
        entries.append(make_entry(q, "kings_rule_integral", {"expr": expr, "lower": low, "upper": up, "answer": ans}, "definite_integral"))

    # 7. S.E-One Symmetry Method (#266-#269, #329, #409)
    se_data = [
        ("(x^5 + x^2)/(1 + x^2)", "-2", "2", "32/5", "Evaluate the definite integral of (x^5 + x^2)/(1 + x^2) from -2 to 2 using S.E-One symmetry method"),
        ("(x^7 + 1)/sqrt(1 - x^2)", "-1", "1", "pi", "Evaluate the definite integral of (x^7 + 1)/sqrt(1 - x^2) from -1 to 1 using S.E-One symmetry method"),
        ("(sin(x)^3 + x^2)*cos(x)", "-pi", "pi", "4*pi", "Evaluate the definite integral of (sin(x)^3 + x^2)*cos(x) from -pi to pi using S.E-One method"),
        ("(x^3 + 1)*(25 - x^2)", "-5", "5", "61030*pi/3", "Evaluate the definite integral of (x^3 + 1)*(25 - x^2) from -5 to 5 using S.E-One symmetry method"),
        ("sin(x)^5/(cos(x)^2 + 1)", "-pi/3", "pi/3", "0", "Evaluate the definite integral of sin(x)^5/(cos(x)^2 + 1) from -pi/3 to pi/3 using S.E-One symmetry method"),
        ("x^3/(1 + e^x)", "-1", "1", "0", "Evaluate the definite integral of x^3/(1 + e^x) from -1 to 1 using S.E-One symmetry method"),
    ]
    for expr, low, up, ans, q in se_data:
        entries.append(make_entry(q, "se_one_integral", {"expr": expr, "lower": low, "upper": up, "answer": ans}, "definite_integral"))

    # 8. P.U.N. Integrals (#270, #365, #370)
    pun_data = [
        ("(2*x + 3)/(x^2 + 2*x + 10)", "ln(x^2 + 2*x + 10) + (1/3)*arctan((x+1)/3)", "Evaluate \\int (2*x + 3)/(x^2 + 2*x + 10) dx using the P.U.N. method"),
        ("(x + 1)/(4*x^2 + 3)", "(1/8)*ln(4*x^2 + 3) + (1/(2*sqrt(3)))*arctan(2*x/sqrt(3))", "Integrate (x + 1)/(4*x^2 + 3) dx using the PUN method"),
        ("(4*x + 3)/(2*x^2 + 3*x + 7)", "ln|2*x^2 + 3*x + 7|", "Find \\int (4*x + 3)/(2*x^2 + 3*x + 7) dx using P.U.N. method"),
        ("(3*x - 1)/(4*x^2 - 4*x + 17)", "(3/8)*ln(4*x^2 - 4*x + 17) + (1/16)*arctan((2*x-1)/4)", "Evaluate \\int (3*x - 1)/(4*x^2 - 4*x + 17) dx using the P.U.N. method"),
    ]
    for expr, ant, q in pun_data:
        entries.append(make_entry(q, "pun_integral", {"expr": expr, "antideriv": ant}, "antiderivative"))

    # 9. Root Manipulation Integrals (#280, #288, #350, #351, #357)
    root_data = [
        ("1/(sqrt(x)*(x + 1))", "2*arctan(sqrt(x))", "Evaluate \\int 1/(sqrt(x)*(x + 1)) dx using root manipulation"),
        ("1/(sqrt(x)*(sqrt(3)*sqrt(x) + 1))", "(2/sqrt(3))*sqrt(x) - (2/3)*ln(sqrt(3)*sqrt(x) + 1)", "Find \\int 1/(sqrt(x)*(sqrt(3)*sqrt(x) + 1)) dx using root manipulation"),
        ("12/(sqrt(x)*(x + 1))", "12*arctan(sqrt(x))", "Integrate 12/(sqrt(x)*(x + 1)) dx using root manipulation"),
        ("8*sqrt(2)/(sqrt(x)*(sqrt(2)*sqrt(x) + 1))", "8*sqrt(2)*ln(sqrt(2)*sqrt(x) + 1)", "Evaluate \\int 8*sqrt(2)/(sqrt(x)*(sqrt(2)*sqrt(x) + 1)) dx using root manipulation"),
        ("(x + 3)*sqrt(2*x + 1)", "(1/3)*sqrt(2*x+1)*(2*x+7)", "Find the integral of (x + 3)*sqrt(2*x + 1) dx using root manipulation"),
    ]
    for expr, ant, q in root_data:
        entries.append(make_entry(q, "root_manipulation_integral", {"expr": expr, "antideriv": ant}, "antiderivative"))

    # 10. Trig Substitution Integrals (#271, #281, #284, #340, #346, #391, #402, #413)
    trigsub_data = [
        ("sqrt(25 - x^2)", "(1/2)*(25*asin(x/5) - x*sqrt(25 - x^2))", "Evaluate \\int sqrt(25 - x^2) dx using trigonometric substitution"),
        ("cos(x)/sqrt(4 - sin(x)^2)", "asin(sin(x)/2)", "Integrate cos(x)/sqrt(4 - sin(x)^2) dx using trigonometric substitution"),
        ("1/sqrt(2 - x)", "-10*asin(sqrt(1 - x/2))", "Find \\int 1/sqrt(2 - x) dx using trigonometric substitution"),
        ("x/sqrt(81 - x^2)", "asin(x/9) - sqrt(81 - x^2)", "Evaluate \\int x/sqrt(81 - x^2) dx using trigonometric substitution"),
        ("sin(2*x)/sqrt(3 - sin(x)^4)", "(1/2)*asin(sin(x)^2/sqrt(3))", "Integrate sin(2*x)/sqrt(3 - sin(x)^4) dx using trigonometric substitution"),
    ]
    for expr, ant, q in trigsub_data:
        entries.append(make_entry(q, "trig_substitution_integral", {"expr": expr, "antideriv": ant}, "antiderivative"))

    # 11. Trig Power Reduction (#272, #291, #314, #386, #392, #410, #422)
    trigpow_data = [
        ("sin(x)^(3/2)*cos(x)^3", "(2/231)*sin(x)^(3/2)*(21*sin(x)^4 - 66*sin(x)^2 + 77)", "Evaluate \\int sin(x)^(3/2)*cos(x)^3 dx using trigonometric power reduction"),
        ("tan(x)^3*sec(x)^2", "(1/4)*(sec(x)^4 - 4*sec(x)^2 - 4*ln|cos(x)|)", "Find \\int tan(x)^3*sec(x)^2 dx using trig power reduction"),
        ("8*sin(x)^3*cos(x)", "2*sin(x)^4", "Integrate 8*sin(x)^3*cos(x) dx using trig power reduction"),
        ("6*sin(3*x)*sin(3*x)^2", "2*(-cos(3*x) + (1/3)*cos(3*x)^3)", "Evaluate \\int 6*sin(3*x)^3 dx using trig power reduction"),
        ("sin(2*x)", "-cos(2*x)/2", "Find \\int sin(2*x) dx using trig power reduction"),
    ]
    for expr, ant, q in trigpow_data:
        entries.append(make_entry(q, "trig_power_reduction_integral", {"expr": expr, "antideriv": ant}, "antiderivative"))

    # 12. PFD Linear Power Ratio Trick (#310, #311, #347)
    pfd_power_data = [
        ("1/((x-6)*(x+3)^2)", "(1/729)*(-9/(x-6) - 9/(x+3) - 2*ln|x-6| + 2*ln|x+3|)", "Evaluate \\int 1/((x-6)*(x+3)^2) dx using partial fraction linear power ratio trick"),
        ("1/((x-8)^2*(x+7))", "(1/33750)*(15*(2*x^2-17*x-67)/((x-8)^2*(x+7)) + 2*ln|x-8| - 2*ln|x+7|)", "Find the integral of 1/((x-8)^2*(x+7)) dx using partial fraction linear power ratio trick"),
        ("(x^2+1)/((x-1)*(x+1)^4)", "(1/192)*((-30*x^4-90*x^3-70*x^2+30*x+64)/((x-1)*(x+1)^4) - 15*ln|x-1| + 15*ln|x+1|)", "Integrate (x^2+1)/((x-1)*(x+1)^4) dx using partial fraction linear power ratio trick"),
        ("1/((x-2)*(x+1)^3)", "-(1/27)*(9/(2*(x+1)^2) + 3/(x+1) + ln|x+1| - ln|x-2|)", "Evaluate \\int 1/((x-2)*(x+1)^3) dx using partial fraction linear power ratio trick"),
    ]
    for expr, ant, q in pfd_power_data:
        entries.append(make_entry(q, "pfd_linear_power_trick_integral", {"expr": expr, "antideriv": ant}, "antiderivative"))

    # 13. Euler's Formula Integration (#372, #373)
    euler_data = [
        ("e^(7*x)*cos(x)", "(e^(7*x)*sin(x) + 7*e^(7*x)*cos(x))/50", "Evaluate \\int e^(7*x)*cos(x) dx using Euler's formula"),
        ("e^x*sin(7*x)", "(7*e^x*sin(7*x) + e^x*cos(7*x))/50", "Find \\int e^x*sin(7*x) dx using Euler's formula"),
        ("e^(2*x)*cos(3*x)", "(2*cos(3*x) + 3*sin(3*x))*e^(2*x)/13", "Integrate e^(2*x)*cos(3*x) dx using Euler's formula"),
        ("e^(3*x)*sin(4*x)", "(3*sin(4*x) - 4*cos(4*x))*e^(3*x)/25", "Evaluate \\int e^(3*x)*sin(4*x) dx using Euler's formula"),
    ]
    for expr, ant, q in euler_data:
        entries.append(make_entry(q, "euler_formula_integral", {"expr": expr, "antideriv": ant}, "antiderivative"))

    # 14. Conjugate Radical Rationalizing (#381, #395)
    conj_data = [
        ("1/(sqrt(2*x+1) + sqrt(3*x+4))", "2*(-sqrt(2*x+1) + sqrt(3*x+4) + sqrt(5)*arctan(sqrt((2*x+1)/5)) - sqrt(5)*arctan(sqrt((3*x+4)/5)))", "Evaluate \\int 1/(sqrt(2*x+1) + sqrt(3*x+4)) dx using conjugate radical rationalization"),
        ("1/(sqrt(x) + sqrt(x+1))", "(2/3)*((x+1)^(3/2) - x^(3/2))", "Find \\int 1/(sqrt(x) + sqrt(x+1)) dx using conjugate radical rationalization"),
        ("1/(sqrt(3*x+2) + sqrt(3*x-1))", "(2/9)*((3*x+2)^(3/2) - (3*x-1)^(3/2))", "Integrate 1/(sqrt(3*x+2) + sqrt(3*x-1)) dx using conjugate radical rationalization"),
    ]
    for expr, ant, q in conj_data:
        entries.append(make_entry(q, "conjugate_radical_integral", {"expr": expr, "antideriv": ant}, "antiderivative"))

    # 15. Nested Infinite Radicals (#397)
    nested_data = [
        ("sqrt(x*sqrt(x*sqrt(x*...)))", "x^2/2", "Evaluate \\int sqrt(x*sqrt(x*sqrt(x*...))) dx using nested infinite radical property"),
        ("sqrt(x^3*sqrt(x^3*sqrt(x^3*...)))", "x^4/4", "Find \\int sqrt(x^3*sqrt(x^3*...)) dx using nested infinite radical property"),
    ]
    for expr, ant, q in nested_data:
        entries.append(make_entry(q, "nested_infinite_radical_integral", {"expr": expr, "antideriv": ant}, "antiderivative"))

    # 16. Exponential Derivative Sum Rule (#393)
    exp_sum_data = [
        ("e^x*(1/x - 1/x^2)", "e^x/x", "Integrate e^x*(1/x - 1/x^2) dx using exponential derivative sum rule"),
        ("e^x*(tan(x) + sec(x)^2)", "e^x*tan(x)", "Evaluate \\int e^x*(tan(x) + sec(x)^2) dx using exponential derivative sum rule"),
        ("e^x*(sin(x) + cos(x))", "e^x*sin(x)", "Find \\int e^x*(sin(x) + cos(x)) dx using exponential derivative sum rule"),
    ]
    for expr, ant, q in exp_sum_data:
        entries.append(make_entry(q, "exp_derivative_sum_integral", {"expr": expr, "antideriv": ant}, "antiderivative"))

    # 17. Feynman's Technique (#417, #423, #425, #426)
    feynman_data = [
        ("(x^a - 1)/ln(x)", "0", "1", "ln(a + 1)", "Evaluate the definite integral of (x^a - 1)/ln(x) from 0 to 1 using Feynman's technique of differentiation under the integral sign"),
        ("(e^(-x) - e^(-a*x))/x", "0", "oo", "ln(a)", "Evaluate the definite integral of (e^(-x) - e^(-a*x))/x from 0 to oo using Feynman's technique"),
        ("ln(1 + a*cos(x))", "0", "pi", "pi*ln((1 + sqrt(1 - a^2))/2)", "Evaluate the definite integral of ln(1 + a*cos(x)) from 0 to pi using Feynman's technique"),
        ("arctan(a*x)/(x*(1 + x^2))", "0", "oo", "pi*ln(1 + a)/2", "Evaluate the definite integral of arctan(a*x)/(x*(1 + x^2)) from 0 to oo using Feynman's technique"),
    ]
    for expr, low, up, ans, q in feynman_data:
        entries.append(make_entry(q, "feynman_technique_integral", {"expr": expr, "lower": low, "upper": up, "answer": ans}, "definite_integral"))

    # 18. Series Expansion Definite Integrals (#427-#432)
    series_data = [
        ("sin(x)/x", "0", "1", "0.94608", "Evaluate the definite integral of sin(x)/x from 0 to 1 using MacLaurin series expansion"),
        ("(e^x - 1)/x", "0", "1", "1.31790", "Evaluate the definite integral of (e^x - 1)/x from 0 to 1 using MacLaurin series expansion"),
        ("(1 - cos(x))/x^2", "0", "1", "0.48639", "Evaluate the definite integral of (1 - cos(x))/x^2 from 0 to 1 using series expansion"),
        ("ln(1+x)/x", "0", "1", "pi^2/12", "Evaluate the definite integral of ln(1+x)/x from 0 to 1 using series expansion term by term integration"),
        ("arctan(x)/x", "0", "1", "0.91597", "Evaluate the definite integral of arctan(x)/x from 0 to 1 using MacLaurin series expansion"),
        ("(cos(x) - 1)/x", "0", "1", "-0.23981", "Evaluate the definite integral of (cos(x) - 1)/x from 0 to 1 using series expansion"),
    ]
    for expr, low, up, ans, q in series_data:
        entries.append(make_entry(q, "series_expansion_definite_integral", {"expr": expr, "lower": low, "upper": up, "answer": ans}, "definite_integral"))

    # 19. Dilogarithm Function (#433-#438)
    dilo_data = [
        ("ln(x)/(1-x)", "0", "1", "-pi^2/6", "Evaluate the definite integral of ln(x)/(1-x) from 0 to 1 using dilogarithm function"),
        ("ln(1 + e^(-x))", "0", "oo", "pi^2/12", "Evaluate the definite integral of ln(1 + e^(-x)) from 0 to oo using dilogarithm function"),
        ("ln((2^x - 1)/2^x)", "0", "oo", "-pi^2/ln(64)", "Evaluate the definite integral of ln((2^x - 1)/2^x) from 0 to oo using dilogarithm function"),
        ("arctan(3*x)/x", "0", "1/3", "pi^2/24", "Evaluate the definite integral of arctan(3*x)/x from 0 to 1/3 using dilogarithm function"),
    ]
    for expr, low, up, ans, q in dilo_data:
        entries.append(make_entry(q, "dilogarithm_integral", {"expr": expr, "lower": low, "upper": up, "answer": ans}, "definite_integral"))

    # 20. Tabular Integration by Parts (#356, #396, #411)
    tabular_data = [
        ("x^2*sin(4*x)", "(1/128)*(3*(8*x^2 - 1)*sin(4*x) - 4*x*(8*x^2 - 3)*cos(4*x))", "Evaluate \\int x^2 * sin(4*x) dx using tabular integration by parts"),
        ("x^4*sin(2*x)", "(1/4)*(-2*x^4*cos(2*x) + 4*x^3*sin(2*x) - 3*(-2*x^2*cos(2*x) + 2*x*sin(2*x) + cos(2*x)))", "Integrate x^4 * sin(2*x) dx using tabular integration by parts"),
        ("(10*x^2 + 4*x - x^4)*e^(-2*x)", "(10*x^2 + 4*x - x^4)/(4*e^(2*x))", "Evaluate \\int (10*x^2 + 4*x - x^4)*e^(-2*x) dx using tabular integration by parts"),
    ]
    for expr, ant, q in tabular_data:
        entries.append(make_entry(q, "tabular_ibp_integral", {"expr": expr, "antideriv": ant}, "antiderivative"))

    # 21. Cyclic Integration by Parts (#330, #372, #373)
    cyclic_data = [
        ("e^x*sin(x)", "(1/2)*e^x*(sin(x) - cos(x))", "Find \\int e^x * sin(x) dx using cyclic integration by parts"),
        ("e^(2*x)*cos(3*x)", "(e^(2*x)/13)*(2*cos(3*x) + 3*sin(3*x))", "Evaluate \\int e^(2*x) * cos(3*x) dx using cyclic integration by parts"),
        ("sin(ln(x))", "(x/2)*(sin(ln(x)) - cos(ln(x)))", "Integrate sin(ln(x)) dx using cyclic integration by parts"),
    ]
    for expr, ant, q in cyclic_data:
        entries.append(make_entry(q, "cyclic_ibp_integral", {"expr": expr, "antideriv": ant}, "antiderivative"))

    # 22. Fundamental Theorem of Calculus Definite Integrals (#245-#251, #320, #342)
    ftc_data = [
        ("x^2 + 3*x", "1", "4", "52/3", "Evaluate the definite integral of x^2 + 3*x from 1 to 4"),
        ("x*x^(1/3)", "0", "3", "(27*3^(1/3) - 1)/2", "Evaluate the definite integral of x*x^(1/3) from 0 to 3"),
        ("x*sin(x)", "0", "pi", "pi", "Evaluate the definite integral of x*sin(x) from 0 to pi"),
        ("x^2*cos(x)", "0", "pi", "-2*pi", "Find the definite integral of x^2*cos(x) from 0 to pi"),
        ("x^3*sqrt(9 - x^2)", "0", "3", "171*pi/2", "Evaluate \\int_0^3 x^3 * sqrt(9 - x^2) dx"),
        ("2*x/(x^2 + 1)", "0", "4", "ln(17)", "Evaluate the definite integral of 2*x/(x^2 + 1) from 0 to 4"),
        ("x^2*sqrt(x + 1)", "0", "3", "28/3", "Find the definite integral of x^2*sqrt(x + 1) from 0 to 3"),
    ]
    for expr, low, up, ans, q in ftc_data:
        entries.append(make_entry(q, "definite_integral", {"expr": expr, "lower": low, "upper": up, "answer": ans}, "definite_integral"))

    # 23. Partial Fractions (#278, #301, #315, #317, #375, #419)
    pfd_data = [
        ("1/((2-x)*(x+1))", "(1/3)*(ln|2-x| - ln|x+1|)", "Integrate 1/((2-x)*(x+1)) dx using partial fractions"),
        ("1/(1 - x^3)", "(1/6)*(-ln|x^2+x+1| + 2*ln|1-x| - 2*sqrt(3)*arctan((2*x-1)/sqrt(3)))", "Find \\int 1/(1 - x^3) dx using partial fractions"),
        ("1/(x*(x^2 - 1))", "ln|1-x| + 2*ln|x| - 3*ln|x+1|", "Evaluate \\int 1/(x*(x^2 - 1)) dx using partial fractions"),
        ("x^2/((x^2+1)*(x^2-1))", "-(1/2)*arctan(x) - (1/4)*ln|x+1| + (1/4)*ln|x-1|", "Integrate x^2/((x^2+1)*(x^2-1)) dx using partial fractions"),
    ]
    for expr, ant, q in pfd_data:
        entries.append(make_entry(q, "partial_fraction_integral", {"expr": expr, "antideriv": ant}, "antiderivative"))

    # 24. Integration by Parts with Ghost Functions (#282, #305, #309, #313, #322, #348, #360, #399)
    ibp_data = [
        ("ln(x+1)", "(x+1)*ln(x+1) - x", "Evaluate \\int ln(x+1) dx using integration by parts with ghost function"),
        ("ln(x)/x^3", "((3-3*x)/x^2)*ln(x)", "Integrate ln(x)/x^3 dx using integration by parts"),
        ("ln(x)/x^2", "-(ln(x)+1)/x", "Find \\int ln(x)/x^2 dx using integration by parts"),
        ("x^2*arctan(6*x)", "(1/1296)*(432*x^3*arctan(6*x) - 36*x^2 + ln|36*x^2+1|)", "Evaluate \\int x^2 * arctan(6*x) dx using integration by parts"),
        ("e^x*asin(e^x)", "4*(sqrt(1 - e^(2*x)) + e^x*asin(e^x))", "Integrate e^x * asin(e^x) dx using integration by parts"),
        ("x^2*ln((1-x)/(x+1))", "(1/3)*(x^3*ln((1-x)/(x+1)) - x^2 - ln(1-x^2))", "Find \\int x^2 * ln((1-x)/(x+1)) dx using integration by parts"),
        ("arctan(3*x)/x^2", "-arctan(3*x)/x + 3*ln(3*|x|) - (3/2)*ln|9*x^2+1|", "Evaluate \\int arctan(3*x)/x^2 dx using integration by parts"),
    ]
    for expr, ant, q in ibp_data:
        entries.append(make_entry(q, "integration_by_parts", {"expr": expr, "antideriv": ant}, "antiderivative"))

    return entries

def generate_way2():
    entries = []
    random.seed(42)

    # 1. Wallis Variations
    for _ in range(25):
        n = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10])
        trig = random.choice(["sin", "cos"])
        coeff = random.choice([1, 2, 3, 4, 5])
        expr = f"{coeff}*{trig}(x)^{n}" if coeff > 1 else f"{trig}(x)^{n}"
        q = f"Evaluate the definite integral of {expr} from 0 to pi/2 using Wallis formula"
        entries.append(make_entry(q, "wallis_integral", {"expr": expr, "lower": "0", "upper": "pi/2", "answer": "wallis_eval"}, "definite_integral"))

    # 2. Product-to-Sum Variations
    for _ in range(25):
        a = random.randint(2, 9)
        b = random.randint(2, 9)
        while a == b:
            b = random.randint(2, 9)
        funcs = random.choice([
            ("sin", "cos"),
            ("cos", "sin"),
            ("sin", "sin"),
            ("cos", "cos")
        ])
        expr = f"{funcs[0]}({a}*x)*{funcs[1]}({b}*x)"
        q = f"Integrate {expr} dx using product to sum formulas"
        entries.append(make_entry(q, "product_to_sum_trig_integral", {"expr": expr, "antideriv": "p2s_eval"}, "antiderivative"))

    # 3. Weierstrass Substitution Variations
    for _ in range(25):
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        trig = random.choice(["cos(x)", "sin(x)"])
        sign = random.choice(["+", "-"])
        expr = f"1/({a} {sign} {b}*{trig})"
        q = f"Evaluate \\int {expr} dx using Weierstrass substitution"
        entries.append(make_entry(q, "weierstrass_substitution_integral", {"expr": expr, "antideriv": "weierstrass_eval"}, "antiderivative"))

    # 4. Radical Species Variations
    for _ in range(25):
        a = random.choice([1, 2, 3, 4])
        b = random.choice([2, 4, 6])
        c = random.choice([1, 5, 9, 10, 13])
        expr = f"1/sqrt({a}*x^2 + {b}*x + {c})"
        q = f"Evaluate \\int {expr} dx using radical species method"
        entries.append(make_entry(q, "radical_species_integral", {"expr": expr, "antideriv": "radical_eval"}, "antiderivative"))

    # 5. Absolute Value Definite Variations
    for _ in range(25):
        r1 = random.randint(1, 4)
        r2 = random.randint(r1 + 1, 7)
        expr = f"|x^2 - {r1+r2}*x + {r1*r2}|"
        low = random.randint(0, r1 - 1)
        up = random.randint(r2 + 1, r2 + 4)
        q = f"Evaluate the definite integral of {expr} from {low} to {up} using absolute value partition"
        entries.append(make_entry(q, "absolute_value_definite_integral", {"expr": expr, "lower": str(low), "upper": str(up), "answer": "abs_eval"}, "definite_integral"))

    # 6. King's Rule Variations
    for _ in range(30):
        n = random.randint(2, 8)
        q = f"Evaluate the definite integral of sin(x)^{n}/(sin(x)^{n} + cos(x)^{n}) from 0 to pi/2 using King's rule"
        entries.append(make_entry(q, "kings_rule_integral", {"expr": f"sin(x)^{n}/(sin(x)^{n} + cos(x)^{n})", "lower": "0", "upper": "pi/2", "answer": "pi/4"}, "definite_integral"))

    # 7. S.E-One Variations
    for _ in range(25):
        a = random.randint(1, 5)
        k = random.choice([3, 5, 7])
        m = random.choice([2, 4])
        expr = f"(x^{k} + x^{m})/(1 + x^2)"
        q = f"Evaluate the definite integral of {expr} from -{a} to {a} using S.E-One symmetry method"
        entries.append(make_entry(q, "se_one_integral", {"expr": expr, "lower": f"-{a}", "upper": str(a), "answer": "se_eval"}, "definite_integral"))

    # 8. P.U.N. Variations
    for _ in range(25):
        a = random.randint(2, 6)
        b = random.randint(1, 8)
        c = random.randint(2, 5)
        d = random.randint(1, 7)
        e = random.randint(3, 15)
        expr = f"({a}*x + {b})/({c}*x^2 + {d}*x + {e})"
        q = f"Evaluate \\int {expr} dx using the P.U.N. method"
        entries.append(make_entry(q, "pun_integral", {"expr": expr, "antideriv": "pun_eval"}, "antiderivative"))

    # 9. Root Manipulation Variations
    for _ in range(25):
        k = random.choice([1, 2, 3, 5])
        a = random.choice([1, 2, 4, 9])
        expr = f"{k}/(sqrt(x)*(x + {a}))"
        q = f"Evaluate \\int {expr} dx using root manipulation"
        entries.append(make_entry(q, "root_manipulation_integral", {"expr": expr, "antideriv": "root_eval"}, "antiderivative"))

    # 10. Trig Substitution Variations
    for _ in range(25):
        a2 = random.choice([4, 9, 16, 25, 36, 49, 64])
        expr = f"sqrt({a2} - x^2)"
        q = f"Evaluate \\int {expr} dx using trigonometric substitution"
        entries.append(make_entry(q, "trig_substitution_integral", {"expr": expr, "antideriv": "trigsub_eval"}, "antiderivative"))

    # 11. Trig Power Reduction Variations
    for _ in range(25):
        k = random.randint(2, 8)
        trig = random.choice(["sin", "cos"])
        expr = f"{trig}(x)^{k}"
        q = f"Evaluate \\int {expr} dx using trig power reduction"
        entries.append(make_entry(q, "trig_power_reduction_integral", {"expr": expr, "antideriv": "trigred_eval"}, "antiderivative"))

    # 12. PFD Linear Power Trick Variations
    for _ in range(25):
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        while a == b:
            b = random.randint(1, 9)
        p = random.choice([2, 3, 4])
        expr = f"1/((x - {a})*(x + {b})^{p})"
        q = f"Evaluate \\int {expr} dx using partial fraction linear power ratio trick"
        entries.append(make_entry(q, "pfd_linear_power_trick_integral", {"expr": expr, "antideriv": "pfd_power_eval"}, "antiderivative"))

    # 13. Euler's Formula Variations
    for _ in range(25):
        a = random.randint(1, 6)
        b = random.randint(1, 6)
        trig = random.choice(["cos", "sin"])
        expr = f"e^({a}*x)*{trig}({b}*x)"
        q = f"Integrate {expr} dx using Euler's formula"
        entries.append(make_entry(q, "euler_formula_integral", {"expr": expr, "antideriv": "euler_formula_eval"}, "antiderivative"))

    # 14. Conjugate Radical Variations
    for _ in range(25):
        a = random.randint(1, 5)
        b = random.randint(6, 12)
        expr = f"1/(sqrt(x + {a}) + sqrt(x + {b}))"
        q = f"Evaluate \\int {expr} dx using conjugate radical rationalization"
        entries.append(make_entry(q, "conjugate_radical_integral", {"expr": expr, "antideriv": "conjugate_eval"}, "antiderivative"))

    # 15. Feynman's Technique Variations
    for _ in range(25):
        p = random.randint(1, 5)
        q = f"Evaluate the definite integral of (x^{p} - 1)/ln(x) from 0 to 1 using Feynman's technique of differentiation under the integral sign"
        entries.append(make_entry(q, "feynman_technique_integral", {"expr": f"(x^{p} - 1)/ln(x)", "lower": "0", "upper": "1", "answer": f"ln({p+1})"}, "definite_integral"))

    # 16. Series Expansion Variations
    for _ in range(25):
        p = random.randint(1, 5)
        q = f"Evaluate the definite integral of sin({p}*x)/x from 0 to 1 using MacLaurin series expansion"
        entries.append(make_entry(q, "series_expansion_definite_integral", {"expr": f"sin({p}*x)/x", "lower": "0", "upper": "1", "answer": "series_eval"}, "definite_integral"))

    # 17. Dilogarithm Variations
    for _ in range(20):
        a = random.randint(1, 5)
        q = f"Evaluate the definite integral of ln(1 - {a}*x)/x from 0 to 1/{a+1} using dilogarithm function"
        entries.append(make_entry(q, "dilogarithm_integral", {"expr": f"ln(1 - {a}*x)/x", "lower": "0", "upper": f"1/{a+1}", "answer": f"-Li_2({a}/({a+1}))"}, "definite_integral"))

    # 18. Tabular IBP Variations
    for _ in range(25):
        k = random.choice([2, 3, 4])
        a = random.randint(2, 6)
        trig = random.choice(["sin", "cos"])
        expr = f"x^{k}*{trig}({a}*x)"
        q = f"Evaluate \\int {expr} dx using tabular integration by parts"
        entries.append(make_entry(q, "tabular_ibp_integral", {"expr": expr, "antideriv": "tabular_eval"}, "antiderivative"))

    # 19. Cyclic IBP Variations
    for _ in range(25):
        a = random.randint(1, 4)
        b = random.randint(1, 5)
        trig = random.choice(["sin", "cos"])
        expr = f"e^({a}*x)*{trig}({b}*x)"
        q = f"Find \\int {expr} dx using cyclic integration by parts"
        entries.append(make_entry(q, "cyclic_ibp_integral", {"expr": expr, "antideriv": "cyclic_eval"}, "antiderivative"))

    # 20. FTC Definite Variations
    for _ in range(25):
        a = random.randint(1, 5)
        b = random.randint(1, 8)
        low = random.randint(0, 2)
        up = random.randint(low + 1, low + 5)
        expr = f"{a}*x^2 + {b}*x"
        q = f"Evaluate the definite integral of {expr} from {low} to {up}"
        entries.append(make_entry(q, "definite_integral", {"expr": expr, "lower": str(low), "upper": str(up), "answer": "ftc_eval"}, "definite_integral"))

    # 21. Partial Fractions Variations
    for _ in range(25):
        a = random.randint(1, 6)
        b = random.randint(1, 6)
        while a == b:
            b = random.randint(1, 6)
        expr = f"1/((x - {a})*(x + {b}))"
        q = f"Integrate {expr} dx using partial fractions"
        entries.append(make_entry(q, "partial_fraction_integral", {"expr": expr, "antideriv": "pfd_eval"}, "antiderivative"))

    # 22. Integration by Parts Ghost Variations
    for _ in range(25):
        a = random.randint(1, 5)
        func = random.choice(["ln", "arctan", "arcsin"])
        expr = f"{func}({a}*x)"
        q = f"Evaluate \\int {expr} dx using integration by parts with ghost function"
        entries.append(make_entry(q, "integration_by_parts", {"expr": expr, "antideriv": "ibp_eval"}, "antiderivative"))

    return entries

def main():
    dataset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "verimath_finetune_dataset.jsonl"))
    print(f"Loading existing dataset from {dataset_path}...")

    existing_queries = set()
    total_existing = 0
    if os.path.exists(dataset_path):
        with open(dataset_path, "r", encoding="utf-8") as f:
            for line in f:
                total_existing += 1
                try:
                    obj = json.loads(line)
                    q = obj["messages"][1]["content"].strip().lower()
                    existing_queries.add(q)
                except Exception:
                    pass

    print(f"Existing examples: {total_existing} ({len(existing_queries)} unique queries)")

    way1 = generate_way1()
    way2 = generate_way2()
    all_new = way1 + way2

    valid_new = []
    skipped = 0
    mismatched = 0

    for item in all_new:
        q_text = item["messages"][1]["content"].strip()
        q_lower = q_text.lower()
        if q_lower in existing_queries:
            skipped += 1
            continue

        asst_data = json.loads(item["messages"][2]["content"])
        expected_template = asst_data["template"]

        # Classification check
        classified_t = classify_problem(q_text)
        if classified_t != expected_template and asst_data["is_complete"]:
            mismatched += 1

        existing_queries.add(q_lower)
        valid_new.append(item)

    print(f"Way 1 entries: {len(way1)}")
    print(f"Way 2 entries: {len(way2)}")
    print(f"Total new generated: {len(all_new)}")
    print(f"Duplicates skipped: {skipped}")
    print(f"Mismatched classifications: {mismatched}")
    print(f"New entries to append: {len(valid_new)}")

    with open(dataset_path, "a", encoding="utf-8") as f:
        for item in valid_new:
            f.write(json.dumps(item) + "\n")

    new_total = total_existing + len(valid_new)
    print(f"Successfully appended {len(valid_new)} examples.")
    print(f"New dataset total: {new_total} examples.")

if __name__ == "__main__":
    main()
