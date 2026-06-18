import sqlite3
import pandas as pd

conn = sqlite3.connect("database/logistics.db")

query = """
SELECT
    Country,
    COUNT(*) AS Total_Orders
FROM logistics_data
GROUP BY Country
ORDER BY Total_Orders DESC
LIMIT 10;
"""

result = pd.read_sql_query(query, conn)

print(result)

conn.close()