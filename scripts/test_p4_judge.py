import sys
sys.path.insert(0, '.')
from backend.pipeline.statement_judge import judge
from backend.pipeline.formalizer import FormalizerResult
from backend.templates.registry import get_template, fill_template

prob = r'Find the point on the parabola $y = x^2$ that is closest to the point $(0, \frac{3}{2})$.'

# Let's inspect parabola_closest_point_optimization
tmpl = get_template('parabola_closest_point_optimization')
print('Template slots:', tmpl.slots)
print('Lean template:', tmpl.lean_template)
print('Back translation template:', tmpl.back_translation_template)
