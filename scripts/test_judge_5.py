from backend.templates.registry import Template, TEMPLATES
from backend.pipeline.statement_judge import judge
from backend.pipeline.formalizer import FormalizerResult

mock_templates = [
    Template(
        id="triangle_included_angle_max_area_optimization",
        display_name="Triangle Included Angle Area Maximization",
        keywords=[],
        lean_template="example : 2 * ({A_max} : ℝ) = ({a} : ℝ) * ({b} : ℝ) := by norm_num",
        tactic="norm_num",
        prompt_hint="",
        slots=["a", "b", "theta", "theta_deg", "A_max", "unit"],
        back_translation_template="Two sides of a triangle have fixed lengths a = {a} {unit} and b = {b} {unit}, with an included angle theta between them. The angle that maximizes the area is theta = {theta} ({theta_deg} degrees) and that maximum area is {A_max} {unit}^2.",
        example_problem="",
        example_slots={}
    ),
    Template(
        id="open_box_length_twice_width_min_surface_area_optimization",
        display_name="Open-Top Box Length Twice Width Surface Area Minimization",
        keywords=[],
        lean_template="example : 4 * ({W_cubed} : ℝ) = 3 * {V} ∧ ({L_cubed} : ℝ) = 8 * {W_cubed} ∧ 27 * ({H_cubed} : ℝ) = 8 * {W_cubed} := by norm_num",
        tactic="norm_num",
        prompt_hint="",
        slots=["V", "unit", "W_cubed", "W_exact", "W_val", "L_cubed", "L_exact", "L_val", "H_cubed", "H_exact", "H_val", "S_exact", "S_val"],
        back_translation_template="An open-top rectangular box must hold volume {V} {unit}^3, with base length twice its width (L = 2W). The dimensions minimizing total surface area are width W = {W_exact} {unit} (~{W_val} {unit}), length L = {L_exact} {unit} (~{L_val} {unit}), and height H = {H_exact} {unit} (~{H_val} {unit}), with minimum surface area {S_exact} {unit}^2 (~{S_val} {unit}^2).",
        example_problem="",
        example_slots={}
    ),
    Template(
        id="projectile_range_angle_optimization",
        display_name="Projectile Launch Angle Range Maximization",
        keywords=[],
        lean_template="example : 2 * ({R_max} : ℝ) = {k} ∧ 4 * ({R_max} : ℝ) * {g} = 2 * ({v0})^2 := by norm_num",
        tactic="norm_num",
        prompt_hint="",
        slots=["v0", "g", "k", "theta", "theta_deg", "R_max", "v_unit", "len_unit"],
        back_translation_template="The horizontal range of a projectile launched at speed v_0 = {v0} {v_unit} with g = {g} is R(theta) = {k}*sin(theta)*cos(theta). The launch angle that maximizes the range is theta = {theta} ({theta_deg} degrees) and that maximum range is {R_max} {len_unit}.",
        example_problem="",
        example_slots={}
    ),
    Template(
        id="horizontal_parabola_inscribed_rectangle_optimization",
        display_name="Horizontal Parabola Inscribed Rectangle Area Maximization",
        keywords=[],
        lean_template="example : 3 * ({y_sq} : ℝ) = {a} ∧ ({W} : ℝ) = {a} - {y_sq} ∧ ({A_max_sq} : ℝ) = 4 * ({W})^2 * {y_sq} := by norm_num",
        tactic="norm_num",
        prompt_hint="",
        slots=["a", "y_sq", "y_exact", "y_val", "W", "H_exact", "H_val", "A_max_exact", "A_max_val", "A_max_sq"],
        back_translation_template="For a rectangle inscribed in the region bounded by the horizontal parabola x = {a} - y^2 and the y-axis (x = 0), the dimensions that maximize area are width W = {W} and height H = {H_exact} (~{H_val}), and that maximum area is {A_max_exact} (~{A_max_val}).",
        example_problem="",
        example_slots={}
    ),
    Template(
        id="cubic_tangent_min_slope_optimization",
        display_name="Cubic Tangent Line Minimum Slope Optimization",
        keywords=[],
        lean_template="example : 6 * ({x} : ℝ) + 2 * ({b}) = 0 ∧ ({y} : ℝ) = ({x})^3 + ({b})*({x})^2 + ({c})*({x}) + ({d}) ∧ ({m_min} : ℝ) = 3*({x})^2 + 2*({b})*({x}) + ({c}) := by norm_num",
        tactic="norm_num",
        prompt_hint="",
        slots=["b", "c", "d", "x", "y", "m_min"],
        back_translation_template="On the cubic curve y = x^3 + ({b})*x^2 + ({c})*x + ({d}), the tangent line has the smallest (least) slope at the point ({x}, {y}) and that minimum slope is {m_min}.",
        example_problem="",
        example_slots={}
    )
]

for t in mock_templates:
    TEMPLATES[t.id] = t

tests = [
    (
        "triangle_included_angle_max_area_optimization",
        r"Two sides of a triangle have fixed lengths $a = 6\text{ cm}$ and $b = 10\text{ cm}$, with an included angle $\theta$ between them. What angle $\theta$ maximizes the area of the triangle, and what is that maximum area?",
        {"a": "6", "b": "10", "theta": "pi/2", "theta_deg": "90", "A_max": "30", "unit": "cm"},
        "example : 2 * (30 : ℝ) = (6 : ℝ) * (10 : ℝ) := by norm_num"
    ),
    (
        "open_box_length_twice_width_min_surface_area_optimization",
        r"An open-top rectangular box must hold a fixed volume of $72\text{ cm}^3$, and the length of its base must be twice its width ($L = 2W$). Find the dimensions of the box that minimize the total surface area of material used.",
        {"V": "72", "unit": "cm", "W_cubed": "54", "W_exact": "3*2^(1/3)", "W_val": "3.7798", "L_cubed": "432", "L_exact": "6*2^(1/3)", "L_val": "7.5595", "H_cubed": "16", "H_exact": "2*2^(1/3)", "H_val": "2.5198", "S_exact": "54*4^(1/3)", "S_val": "85.7196"},
        "example : 4 * (54 : ℝ) = 3 * 72 ∧ (432 : ℝ) = 8 * 54 ∧ 27 * (16 : ℝ) = 8 * 54 := by norm_num"
    ),
    (
        "projectile_range_angle_optimization",
        r"The horizontal range of a projectile launched at speed $v_0 = 20\text{ m/s}$ at an angle $\theta$ above flat ground (with $g = 10\text{ m/s}^2$) is $R(\theta) = \frac{v_0^2}{g}\sin\theta\cos\theta = 40\sin\theta\cos\theta$. Use calculus to find the launch angle $\theta$ that maximizes the range.",
        {"v0": "20", "g": "10", "k": "40", "theta": "pi/4", "theta_deg": "45", "R_max": "20", "v_unit": "m/s", "len_unit": "m"},
        "example : 2 * (20 : ℝ) = 40 ∧ 4 * (20 : ℝ) * 10 = 2 * (20)^2 := by norm_num"
    ),
    (
        "horizontal_parabola_inscribed_rectangle_optimization",
        r"Find the dimensions and maximum area of a rectangle inscribed in the region bounded by the horizontal parabola $x = 9 - y^2$ and the $y$-axis ($x = 0$).",
        {"a": "9", "y_sq": "3", "y_exact": "sqrt(3)", "y_val": "1.7321", "W": "6", "H_exact": "2*sqrt(3)", "H_val": "3.4641", "A_max_exact": "12*sqrt(3)", "A_max_val": "20.7846", "A_max_sq": "432"},
        "example : 3 * (3 : ℝ) = 9 ∧ (6 : ℝ) = 9 - 3 ∧ (432 : ℝ) = 4 * (6)^2 * 3 := by norm_num"
    ),
    (
        "cubic_tangent_min_slope_optimization",
        r"Find the point $(x, y)$ on the cubic curve $y = x^3 - 6x^2 + 15x - 2$ where the tangent line has the smallest (least) slope, and state what that minimum slope is.",
        {"b": "-6", "c": "15", "d": "-2", "x": "2", "y": "12", "m_min": "3"},
        "example : 6 * (2 : ℝ) + 2 * (-6) = 0 ∧ (12 : ℝ) = (2)^3 + (-6)*(2)^2 + 15*(2) + (-2) ∧ (3 : ℝ) = 3*(2)^2 + 2*(-6)*(2) + 15 := by norm_num"
    )
]

for i, (tid, prob, slots, lean) in enumerate(tests, 1):
    fr = FormalizerResult(
        lean_statement=lean,
        template_id=tid,
        slot_values=slots,
        elapsed_ms=10,
        attempts=1
    )
    jr = judge(prob, fr)
    print(f"P{i}: verdict={jr.verdict}, score={jr.similarity_score:.3f}, reason={jr.reason}")
