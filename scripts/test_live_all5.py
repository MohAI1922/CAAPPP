import urllib.request
import json

PROBLEMS = [
    (
        "P1 - Inscribed Isosceles Triangle in Circle",
        "Find the height h and maximum area of an isosceles triangle inscribed in a circle of radius R = 6 cm."
    ),
    (
        "P2 - Cylindrical Silo with Hemispherical Roof",
        "A cylindrical silo with a flat circular floor and a hemispherical roof must hold a fixed total volume of V = 72*pi m^3. The hemispherical roof costs twice as much per square meter as the cylindrical walls (and the floor is free). What radius r and cylinder height h minimize the construction cost?"
    ),
    (
        "P3 - Rectangle Inscribed Between Parabolas",
        "Find the maximum area of a rectangle (with sides parallel to the coordinate axes) that can be inscribed in the region bounded above by y = 18 - x^2 and below by y = 2x^2."
    ),
    (
        "P4 - Hyperbola Closest Point",
        "Find the points in the first quadrant on the hyperbola x^2 - y^2 = 4 that are closest to the point (0, 2), and find that minimum distance."
    ),
    (
        "P5 - Origin Ray Max Slope to Cubic",
        "A ray from the origin (0, 0) touches a point (x, y) on the curve y = -x^3 + 6x^2 - 9x + 10 for x > 0. Wait–let's use y = 6x^2 - x^3 for x > 0. Find the point (x, y) where the slope of the ray from the origin (y/x) is maximized."
    ),
    (
        "Refusal Message Check",
        "Explain the history of the French Revolution in 1789."
    )
]

for label, p_text in PROBLEMS:
    req = urllib.request.Request(
        "http://127.0.0.1:8001/solve",
        data=json.dumps({"problem": p_text}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        print(f"=== {label} ===")
        print(f"Status: {data.get('status')}")
        print(f"Template ID: {data.get('template_id')}")
        print(f"Verified Answer: {data.get('verified_answer')}")
        print(f"LaTeX Answer: {data.get('latex_answer')}")
        stmt = data.get('lean_statement')
        if stmt:
            stmt = stmt.encode('ascii', 'backslashreplace').decode('ascii')
        print(f"Lean Statement: {stmt}")
        print(f"Rejection Reason: {data.get('rejection_reason')}")
        print()
