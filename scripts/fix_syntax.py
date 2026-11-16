import re

with open("verimath/backend/pipeline/step_generator.py", "rb") as f:
    content = f.read()

idx1 = content.find(b"    # Step 3: Transform the integral into terms of u")
idx2 = content.find(b"    return steps", idx1)

replacement = """    # Step 3: Transform the integral into terms of u
    u_int_latex = sp.latex(u_integrand)
    if ratio != 1:
        u_transformed_latex = rf"{ratio_latex} \\int {u_int_latex}\\,du"
    else:
        u_transformed_latex = rf"\\int {u_int_latex}\\,du"

    steps.append(SolutionStep(
        step_number=3,
        title="Transform the Integral to the Variable u",
        explanation=(
            "Substitute u and du into the original integrand to eliminate x completely and obtain an elementary power integral in u:"
        ),
        math=rf"\\int \\left({expr_latex}\\right) dx = {u_transformed_latex}"
    ))

    # Step 4: Evaluate the antiderivative in u
    u_antideriv_latex = sp.latex(u_antideriv)
    if power == -1:
        rule_desc = r"Apply the logarithmic integration rule \\int \\frac{1}{u} du = \\ln|u|:"
    else:
        rule_desc = r"Apply the power rule of integration \\int u^n du = \\frac{u^{n+1}}{n+1}:"

    steps.append(SolutionStep(
        step_number=4,
        title="Evaluate the Integral in Terms of u",
        explanation=rule_desc,
        math=rf"{u_transformed_latex} = {u_antideriv_latex}"
    ))

    # Step 5: Back-substitute and add C
    steps.append(SolutionStep(
        step_number=5,
        title="Back-Substitute Original Variable and Add Constant C",
        explanation=(
            rf"Substitute back u = {base_latex} to express the antiderivative in terms of x, and attach the arbitrary constant of integration C:"
        ),
        math=rf"\\int \\left({expr_latex}\\right) dx = {ans_latex} + C"
    ))

""".encode("utf-8")

new_content = content[:idx1] + replacement + content[idx2:]
with open("verimath/backend/pipeline/step_generator.py", "wb") as f:
    f.write(new_content)

print("Updated step_generator.py successfully.")
