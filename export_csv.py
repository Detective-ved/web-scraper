# ---------- EXPORT CSV ----------
import sqlite3
import pandas as pd
from tkinter import messagebox
def export_csv():
    conn = sqlite3.connect("data.db")
    df = pd.read_sql("SELECT * FROM scraped_data", conn)
    df.to_csv("scraped_data.csv", index=False)
    conn.close()
    messagebox.showinfo("Success", "CSV Exported Successfully!")
