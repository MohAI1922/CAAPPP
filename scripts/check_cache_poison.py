import sqlite3

conn = sqlite3.connect("demo_cache.db")
cursor = conn.cursor()

keywords = ["trapezoid", "hemisphere", "microcontroller", "ellipse", "parabola"]
for kw in keywords:
    rows = cursor.execute("SELECT template_id, problem_text, verified_answer FROM demo_cache WHERE problem_text LIKE ?", (f"%{kw}%",)).fetchall()
    print(f"=== Keyword '{kw}' ({len(rows)} entries) ===")
    for r in rows:
        print(f"  Template: {r[0]}")
        print(f"  Text: {r[1][:80]}...")
        print(f"  Answer: {r[2]}")
