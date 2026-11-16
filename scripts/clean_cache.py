import sqlite3

conn = sqlite3.connect("demo_cache.db")
c = conn.cursor()
rows = c.execute("SELECT problem_key, problem_text, template_id, verified_answer FROM demo_cache").fetchall()
to_delete = []
for r in rows:
    p = r[1].lower()
    if any(k in p for k in ["closed interval", "lifeguard", "illumination", "rain gutter", "first quadrant", "snell", "lightbulb", "ship", "closest", "paper cup", "concentration", "e^{2x}", "e^2x", "4t/(t^2", "c(t)"]):
        to_delete.append(r[0])
        print(f"Deleting cached entry: {r[1][:60]} -> {r[3]}")

if to_delete:
    c.executemany("DELETE FROM demo_cache WHERE problem_key = ?", [(k,) for k in to_delete])
    conn.commit()
    print(f"Successfully deleted {len(to_delete)} stale cache entries.")
else:
    print("No stale cache entries found.")
conn.close()
