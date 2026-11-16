import sympy
from sympy import Rational, simplify, sqrt, cbrt, sin, cos, pi, symbols

# P1: Triangle included angle
a = 6
b = 10
# A = (1/2)*a*b*sin(theta) => max at theta = pi/2
A_max = Rational(1, 2) * a * b
print(f"P1: theta = pi/2 (90 deg), A_max = {A_max}")

# P2: Open-top box L = 2W, V = 72
# V = 2*W^2*H = 72 => W^2*H = 36 => H = 36/W^2
# S(W) = 2*W^2 + 6*W*H = 2*W^2 + 216/W
# S'(W) = 4*W - 216/W^2 = 0 => 4*W^3 = 216 => W^3 = 54 => W = 3*2^(1/3)
V = Rational(72)
W_cubed = Rational(3, 4) * V  # 54
W = simplify(cbrt(W_cubed))   # 3*2^(1/3)
L = 2 * W                     # 6*2^(1/3)
H = V / (2 * W**2)            # 2*2^(1/3)
S_min = 2 * W**2 + 6 * W * H  # 54*2^(2/3)
print(f"P2: W = {W} (~{float(W):.4f}), L = {L} (~{float(L):.4f}), H = {H} (~{float(H):.4f}), S_min = {S_min} (~{float(S_min):.4f})")

# P3: Projectile range R(theta) = 40*sin(theta)*cos(theta)
# R'(theta) = 40*cos(2*theta) = 0 => theta = pi/4
k = 40
R_max = Rational(k, 2)
print(f"P3: theta = pi/4 (45 deg), R_max = {R_max}")

# P4: Horizontal parabola x = 9 - y^2
# A(y) = 2*y*(9 - y^2) = 18*y - 2*y^3
# A'(y) = 18 - 6*y^2 = 0 => y^2 = 3 => y = sqrt(3)
# W = 9 - 3 = 6, H = 2*sqrt(3), A_max = 12*sqrt(3)
a_p4 = 9
y_sq = Rational(a_p4, 3) # 3
y_val = sqrt(y_sq)       # sqrt(3)
W_p4 = a_p4 - y_sq       # 6
H_p4 = 2 * y_val         # 2*sqrt(3)
A_max_p4 = W_p4 * H_p4   # 12*sqrt(3)
A_max_sq_p4 = A_max_p4**2 # 432
print(f"P4: W = {W_p4}, H = {H_p4}, A_max = {A_max_p4}, A_max_sq = {A_max_sq_p4}")

# P5: Cubic tangent min slope y = x^3 - 6x^2 + 15x - 2
# y' = 3x^2 - 12x + 15
# y'' = 6x - 12 = 0 => x = 2
x_p5 = 2
y_p5 = x_p5**3 - 6*x_p5**2 + 15*x_p5 - 2 # 12
m_min_p5 = 3*x_p5**2 - 12*x_p5 + 15      # 3
print(f"P5: point = ({x_p5}, {y_p5}), m_min = {m_min_p5}")
