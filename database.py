# ---------- DATABASE ----------
import sqlite3
def create_db():
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS scraped_data(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            content TEXT
        )
    """)
    conn.commit()
    conn.close()
