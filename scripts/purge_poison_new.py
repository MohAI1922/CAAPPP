import sqlite3

conn = sqlite3.connect("demo_cache.db")
c = conn.cursor()

c.execute("DELETE FROM demo_cache WHERE problem_text LIKE ?", ("%three equal sides%",))
print("Deleted trapezoid:", c.rowcount)

c.execute("DELETE FROM demo_cache WHERE problem_text LIKE ?", ("%cone is inscribed inside a hemisphere%",))
print("Deleted hemisphere cone:", c.rowcount)

conn.commit()
conn.close()
