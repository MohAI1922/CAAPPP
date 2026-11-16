import re

p = r"A closed right circular cylinder must have a fixed volume of $54\pi\text{ cm}^3$. What radius $r$ minimizes the total surface area?"

t = p.strip()
t = t.replace("$", " ")
t = re.sub(r"\b([a-zA-Z])\s+(\d+)\b", r"\1^\2", t)
t = re.sub(r"\\(?:quad|qquad)\b", " ", t)
t = t.replace(r"\,", " ").replace(r"\;", " ").replace(r"\!", " ")
t = re.sub(r"\\(?:left|right)\b", "", t)
t = re.sub(r"\\(?:limits|nolimits)\b", "", t)
t = t.replace(r"\text", " text").replace("\text", " text")
t = re.sub(r"\\?(?:text|mathrm|mathbf|operatorname)\{([^}]*)\}", r" \1 ", t)
t = t.replace(r"\(", " ").replace(r"\)", " ")
t = t.replace(r"\[", " ").replace(r"\]", " ")
t = re.sub(r"\\(?:geq|ge)\b", ">=", t)
t = re.sub(r"\\(?:leq|le)\b", "<=", t)
t = re.sub(r"\\cdot\b", "*", t)
t = re.sub(r"\\times\b", "*", t)
t = re.sub(r"\\theta\b", "theta", t)
t = re.sub(r"\\pi\b", "pi", t)
t = re.sub(r"\\alpha\b", "alpha", t)
t = re.sub(r"\\beta\b", "beta", t)
t = re.sub(r"\\(sin|cos|tan|sec|csc|cot|arcsin|arccos|arctan|asec|acsc|acot|ln|log|exp|sqrt)\b", r"\1", t)
print("t after initial:", repr(t))

m_V = re.search(r"(\d+(?:\.\d+)?)\s*(?:\\pi|pi)", t, re.I)
print("m_V:", m_V.group(1) if m_V else "None")
