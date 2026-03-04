import sqlite3

def init_db():
    conn= sqlite3.connect("database.db")
    cursor=conn.cursor()

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        category TEXT NOT NULL,
                        amount REAL NOT NULL,
                        date TEXT NOT NULL
                   )
""")
    conn.commit()
    conn.close()

init_db()