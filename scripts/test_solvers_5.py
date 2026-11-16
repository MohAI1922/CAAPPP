import re
import sympy
from sympy import symbols, Poly, simplify, cbrt, sqrt, Rational

x = symbols('x')

# Test P1
prob1 = r"Two sides of a triangle have fixed lengths $a = 6\text{ cm}$ and $b = 10\text{ cm}$, with an included angle $\theta$ between them. What angle $\theta$ maximizes the area of the triangle, and what is that maximum area?"
m_a = re.search(r"a\s*=\s*(\d+(?:\.\d+)?)", prob1, re.I)
m_b = re.search(r"b\s*=\s*(\d+(?:\.\d+)?)", prob1, re.I)
a_val = Rational(m_a.group(1)) if m_a else Rational(6)
b_val = Rational(m_b.group(1)) if m_b else Rational(10)
A_max = Rational(1, 2) * a_val * b_val
print(f"P1: a={a_val}, b={b_val}, A_max={A_max}")

# Test P2
prob2 = r"An open-top rectangular box must hold a fixed volume of $72\text{ cm}^3$, and the length of its base must be twice its width ($L = 2W$). Find the dimensions of the box that minimize the total surface area of material used."
m_v = re.search(r"(\d+(?:\.\d+)?)\s*(?:\\text\{)?\s*(?:cm|m|in|ft)\^?3", prob2, re.I)
V_val = Rational(m_v.group(1)) if m_v else Rational(72)
W_cubed = Rational(3, 4) * V_val
W_sym = simplify(cbrt(W_cubed))
L_sym = simplify(2 * W_sym)
H_sym = simplify(W_sym * Rational(2, 3))
S_sym = simplify(2 * W_sym**2 + 6 * W_sym * H_sym)
L_cubed = 8 * W_cubed
H_cubed = Rational(8, 27) * W_cubed
print(f"P2: V={V_val}, W^3={W_cubed}, W={W_sym}, L={L_sym}, H={H_sym}, S={S_sym}")

# Test P3
prob3 = r"The horizontal range of a projectile launched at speed $v_0 = 20\text{ m/s}$ at an angle $\theta$ above flat ground (with $g = 10\text{ m/s}^2$) is $R(\theta) = \frac{v_0^2}{g}\sin\theta\cos\theta = 40\sin\theta\cos\theta$. Use calculus to find the launch angle $\theta$ that maximizes the range."
m_v0 = re.search(r"v_?0\s*=\s*(\d+(?:\.\d+)?)", prob3, re.I)
m_g = re.search(r"g\s*=\s*(\d+(?:\.\d+)?)", prob3, re.I)
m_k = re.search(r"=\s*(\d+(?:\.\d+)?)\s*(?:\\sin|\bsin)", prob3, re.I)
v0_val = Rational(m_v0.group(1)) if m_v0 else Rational(20)
g_val = Rational(m_g.group(1)) if m_g else Rational(10)
k_val = Rational(m_k.group(1)) if m_k else Rational(v0_val**2, g_val)
R_max = Rational(k_val, 2)
print(f"P3: v0={v0_val}, g={g_val}, k={k_val}, R_max={R_max}")

# Test P4
prob4 = r"Find the dimensions and maximum area of a rectangle inscribed in the region bounded by the horizontal parabola $x = 9 - y^2$ and the $y$-axis ($x = 0$)."
m_parab = re.search(r"x\s*=\s*(\d+(?:\.\d+)?)\s*-\s*y", prob4, re.I)
a_val = Rational(m_parab.group(1)) if m_parab else Rational(9)
y_sq = Rational(a_val, 3)
y_sym = simplify(sqrt(y_sq))
W_p4 = a_val - y_sq
H_p4 = simplify(2 * y_sym)
A_max_p4 = simplify(W_p4 * H_p4)
A_max_sq_p4 = A_max_p4**2
print(f"P4: a={a_val}, y_sq={y_sq}, y={y_sym}, W={W_p4}, H={H_p4}, A_max={A_max_p4}, A_max_sq={A_max_sq_p4}")

# Test P5
prob5 = r"Find the point $(x, y)$ on the cubic curve $y = x^3 - 6x^2 + 15x - 2$ where the tangent line has the smallest (least) slope, and state what that minimum slope is."
def prep(s):
    s = s.replace("^", "**").replace("–", "-").strip()
    s = re.sub(r"(\d)\s*([a-zA-Z\(])", r"\1*\2", s)
    return s

m_poly = re.search(r"y\s*=\s*([^,$]+)", prob5)
if m_poly:
    p_str = prep(m_poly.group(1))
    poly = Poly(sympy.sympify(p_str), x)
    coeffs = poly.all_coeffs()
    b_val = coeffs[1]
    c_val = coeffs[2]
    d_val = coeffs[3]
    x_opt = Rational(-b_val, 3)
    y_opt = poly.eval(x_opt)
    m_min = 3 * x_opt**2 + 2 * b_val * x_opt + c_val
    print(f"P5: b={b_val}, c={c_val}, d={d_val}, x={x_opt}, y={y_opt}, m_min={m_min}")
