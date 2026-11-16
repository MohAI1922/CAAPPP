import urllib.request
import json

problems = [
    ('Exponential Extrema', r'Find the maximum value of the function $f(x) = x e^{-x}$ for $x \ge 0$.'),
    ('Rational Function Local Extrema', r'Find the local minimum value of the rational function $f(x) = \frac{x^2 + 4}{x}$ for $x > 0$'),
    ('Economic Profit Optimization', r"A company's total revenue is $R(x) = 120x - 0.5x^2$ and total cost is $C(x) = 3000 + 20x$, where $x$ is units produced. What production level $x$ maximizes profit, and what is that maximum profit?"),
    ('Parabola Closest Point', r'Find the point on the parabola $y = x^2$ that is closest to the point $(0, \frac{3}{2})$.'),
    ('Trigonometric Interval Extrema', r'Find the absolute maximum and minimum values of $f(x) = \sin x + \cos x$ on the interval $[0, 2\pi]$.')
]

for name, p in problems:
    req = urllib.request.Request(
        'http://localhost:8000/solve',
        data=json.dumps({'problem': p}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(f'=== {name} ===')
            print(f"Status: {data.get('status')} | Template: {data.get('template_id')}")
            print(f"Answer: {data.get('verified_answer')}")
            print(f"LaTeX: {data.get('latex_answer')}")
            if data.get('rejection_reason'):
                print(f"Rejection: {data.get('rejection_reason')}")
            print()
    except Exception as e:
        print(f'=== {name} === HTTP Error: {e}\n')
