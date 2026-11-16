with open("verimath/backend/pipeline/step_generator.py", "r", encoding="utf-8") as f:
    text = f.read()

replacements = [
    (
        '"Express the given expression as a product of two differentiable functions u(x) and v(x) "\n            "such that f(x) = u(x) \\\\cdot v(x) (El-Moasser Unit 3, Lesson 3)."',
        '"Express the given expression as a product of two differentiable functions u(x) and v(x) "\n            "such that f(x) = u(x) \\\\cdot v(x)."'
    ),
    (
        '"Apply the verbal rule from El-Moasser: \'The first \\\\times derivative of the second + the second \\\\times derivative of the first\': "\n            "\\\\frac{d}{dx}[u \\\\cdot v] = u(x) v\'(x) + v(x) u\'(x)."',
        '"Apply the product rule formula: \'The first \\\\times derivative of the second + the second \\\\times derivative of the first\': "\n            "\\\\frac{d}{dx}[u \\\\cdot v] = u(x) v\'(x) + v(x) u\'(x)."'
    ),
    (
        '"Write the expression in the rational form f(x) = \\\\frac{u(x)}{v(x)}, identifying numerator u(x) "\n            "and denominator v(x) with v(x) \\\\neq 0 (El-Moasser Unit 3, Lesson 3)."',
        '"Write the expression in the rational form f(x) = \\\\frac{u(x)}{v(x)}, identifying numerator u(x) "\n            "and denominator v(x) with v(x) \\\\neq 0."'
    ),
    (
        '"Apply the verbal rule from El-Moasser: \'Denominator \\\\times derivative of numerator minus "\n            "numerator \\\\times derivative of denominator, all divided by denominator squared\': "\n            "\\\\frac{d}{dx}\\\\left[\\\\frac{u}{v}\\\\right] = \\\\frac{v u\' - u v\'}{v^2}."',
        '"Apply the quotient rule formula: \'Denominator \\\\times derivative of numerator minus "\n            "numerator \\\\times derivative of denominator, all divided by denominator squared\': "\n            "\\\\frac{d}{dx}\\\\left[\\\\frac{u}{v}\\\\right] = \\\\frac{v u\' - u v\'}{v^2}."'
    ),
    (
        '"Apply the verbal rule from El-Moasser (Rule 1, p. 110): \'Increase the exponent by 1, then divide by the "\n            "new exponent\': \\\\int x^n dx = \\\\frac{x^{n+1}}{n+1} (for n \\\\neq -1). The integral of a constant is \\\\int a dx = a x."',
        '"Apply the power rule of integration: \'Increase the exponent by 1, then divide by the "\n            "new exponent\': \\\\int x^n dx = \\\\frac{x^{n+1}}{n+1} (for n \\\\neq -1). The integral of a constant is \\\\int a dx = a x."'
    ),
    (
        '"The set of all antiderivatives of a function defines the indefinite integral. Attach the arbitrary constant "\n            "of integration C (El-Moasser Definition, p. 109)."',
        '"The set of all antiderivatives of a function defines the indefinite integral. Attach the arbitrary constant "\n            "of integration C."'
    ),
    (
        '"According to El-Moasser (Unit 4, Lesson 2, pp. 171\u2013174), apply trigonometric identities "\n            "or direct antiderivative formulas to integrate."',
        '"Apply standard trigonometric identities or direct antiderivative formulas to integrate."'
    ),
    (
        'rf"According to curriculum standards (The Book of Integrals, p. 47: Partial Fraction Decomposition / Senior 3 Advanced Calculus), "\n            rf"factor the denominator polynomial Q(x) = {sp.latex(den)} completely into linear/quadratic factors: "\n            rf"Q(x) = {den_factored_latex}."',
        'rf"Factor the denominator polynomial Q(x) = {sp.latex(den)} completely into linear/quadratic irreducible factors: "\n            rf"Q(x) = {den_factored_latex}."'
    ),
    (
        'rf"According to curriculum standards (The Book of Integrals, p. 58: Polynomial Long Division / Senior 3 Advanced Calculus), "\n            rf"examine the degrees of the numerator polynomial P(x) = {num_latex} (\\deg(P) = {deg_num}) and "\n            rf"denominator polynomial Q(x) = {den_latex} (\\deg(Q) = {deg_den}). "\n            rf"Since \\deg(P) \\ge \\deg(Q), the rational function is improper and polynomial long division is required prior to integration."',
        'rf"Examine the degrees of the numerator polynomial P(x) = {num_latex} (\\deg(P) = {deg_num}) and "\n            rf"denominator polynomial Q(x) = {den_latex} (\\deg(Q) = {deg_den}). "\n            rf"Since \\deg(P) \\ge \\deg(Q), the rational function is improper and polynomial long division is required prior to integration."'
    )
]

replaced = 0
for old, new in replacements:
    if old in text:
        text = text.replace(old, new)
        replaced += 1
    else:
        print(f"Warning: pattern not found: {old[:50]}...")

with open("verimath/backend/pipeline/step_generator.py", "w", encoding="utf-8") as f:
    f.write(text)

print(f"Replaced {replaced}/{len(replacements)} citations in step_generator.py.")
