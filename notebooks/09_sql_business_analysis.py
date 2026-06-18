import sqlite3
import pandas as pd

conn = sqlite3.connect("database/logistics.db")

queries = {

    "Top Countries By Orders": """
    SELECT Country,
           COUNT(*) AS Total_Orders
    FROM logistics_data
    GROUP BY Country
    ORDER BY Total_Orders DESC
    LIMIT 10;
    """,

    "Top Vendors": """
    SELECT Vendor,
           COUNT(*) AS Total_Orders
    FROM logistics_data
    GROUP BY Vendor
    ORDER BY Total_Orders DESC
    LIMIT 10;
    """,

    "Shipment Mode Distribution": """
    SELECT [Shipment Mode],
           COUNT(*) AS Total_Shipments
    FROM logistics_data
    GROUP BY [Shipment Mode];
    """,

    "Product Group Distribution": """
    SELECT [Product Group],
           COUNT(*) AS Total_Orders
    FROM logistics_data
    GROUP BY [Product Group]
    ORDER BY Total_Orders DESC;
    """,

    "Delayed Orders": """
    SELECT Delayed,
           COUNT(*) AS Total
    FROM logistics_data
    GROUP BY Delayed;
    """,

    "Top Countries By Revenue": """
    SELECT Country,
           ROUND(SUM([Line Item Value]),2) AS Revenue
    FROM logistics_data
    GROUP BY Country
    ORDER BY Revenue DESC
    LIMIT 10;
    """
}

for title, query in queries.items():

    print("\n" + "=" * 60)
    print(title.upper())
    print("=" * 60)

    result = pd.read_sql_query(query, conn)

    print(result)

conn.close()