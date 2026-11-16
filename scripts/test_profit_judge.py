import sys
sys.path.insert(0, '.')
from backend.pipeline.statement_judge import _check_numbers_match, _check_math_functions_match, _check_key_entities_match, _normalize
import difflib

prob = "A company's total revenue is $R(x) = 120x - 0.5x^2$ and total cost is $C(x) = 3000 + 20x$, where $x$ is units produced. What production level $x$ maximizes profit, and what is that maximum profit?"
bt = "A company's total revenue is R(x) = 120x - 0.5x^2 and total cost is C(x) = 3000 + 20x, where x is units produced. The production level that maximizes profit is x = 100 units, and the maximum profit is $2000."

p_norm = _normalize(prob)
b_norm = _normalize(bt)
t1 = sorted(set(p_norm.split()))
t2 = sorted(set(b_norm.split()))
common = sorted(set(t1).intersection(set(t2)))
common_str = " ".join(common)
t1_str = " ".join(t1)
t2_str = " ".join(t2)
r1 = difflib.SequenceMatcher(None, common_str, t1_str).ratio()
r2 = difflib.SequenceMatcher(None, common_str, t2_str).ratio()
r3 = difflib.SequenceMatcher(None, t1_str, t2_str).ratio()
sim = max(r1, r2, r3)

print('SIMILARITY:', sim)
print('NUMERIC:', _check_numbers_match(prob, bt).passed)
print('FUNCTIONS:', _check_math_functions_match(prob, bt).passed)
print('ENTITIES:', _check_key_entities_match(prob, bt).passed)
