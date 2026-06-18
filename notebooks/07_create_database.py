import pandas as pd
import sqlite3

# Load Featured Dataset
df = pd.read_csv("data/processed/logistics_featured.csv")

# Create SQLite Database
conn = sqlite3.connect("database/logistics.db")

# Save Dataset as Table
df.to_sql(
    "logistics_data",
    conn,
    if_exists="replace",
    index=False
)

print("Database Created Successfully!")
print(" Table Name: logistics_data")

conn.close()