
import urllib.request, json

problems = [
    ('Problem 1 (Image 1)', 'Find the local maximum or minimum value of the function x 2 - 6x + 11'),
    ('Problem 2 (Image 2)', 'Find both the local maximum and local minimum values of (x) = x^3 - 3x^2 - 9x + 5$.'),
    ('Problem 3 (Image 3)', 'Find the absolute maximum and absolute minimum values of (x) = x^3 - 12x$ on the closed interval $[0, 3]$.'),
    ('Problem 4 (Image 4)', 'Find two positive numbers whose sum is $ and whose product is as large as possible.')
]

for name, p in problems:
    req = urllib.request.Request('http://localhost:8000/solve', data=json.dumps({'problem': p}).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as resp:
            d = json.loads(resp.read().decode('utf-8'))
            st = d.get('status')
            tid = d.get('template_id')
            ans = d.get('verified_answer')
            lat = d.get('latex_answer')
            ms = d.get('elapsed_ms')
            err = d.get('rejection_reason')
            print(f'=== {name} ===')
            print(f'Status: {st} | Template: {tid} | Elapsed: {ms}ms')
            print(f'Answer: {ans}')
            print(f'LaTeX: {lat}')
            if err:
                print(f'Error: {err}')
            print()
    except Exception as e:
        print(f'=== {name} ===')
        print(f'HTTP Exception: {e}')
        print()
