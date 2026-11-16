with open("verimath/backend/pipeline/step_generator.py", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace(
    'rf"Factor the denominator polynomial Q(x) = {sp.latex(den)}',
    'rf"Apply Partial Fraction decomposition: factor the denominator polynomial Q(x) = {sp.latex(den)}'
)
text = text.replace(
    'rf"Examine the degrees of the numerator polynomial P(x) = {num_latex}',
    'rf"Apply Polynomial Long Division: examine the degrees of the numerator polynomial P(x) = {num_latex}'
)

with open("verimath/backend/pipeline/step_generator.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Updated pfd and long division in step_generator.py successfully.")
