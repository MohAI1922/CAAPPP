import urllib.request
import json

def test_prob(prob):
    print("=" * 60)
    print("PROBLEM:", prob)
    req = urllib.request.Request(
        "http://127.0.0.1:8000/solve",
        data=json.dumps({"problem": prob}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        print("Status:", data.get("status"))
        print("Verified Answer:", data.get("verified_answer"))
        print("LaTeX Answer:", data.get("latex_answer"))
        print("Num Steps:", len(data.get("steps", [])))
        for s in data.get("steps", []):
            print(f"  Step {s['step_number']}: {s['title']}")
            print(f"    Explanation: {s['explanation']}")
            print(f"    Math: {s['math']}")

try:
    test_prob("Integrate: x^2 * sqrt(x^3 + 4) dx")
    test_prob("Find the indefinite integral of (x^3 + 2*x + 1)/(x^2 + 1) with respect to x")
except Exception as e:
    print("Error:", e)
