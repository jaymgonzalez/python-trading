import sqlite3
import pandas as pd

# Connect to the SQLite database
con = sqlite3.connect("tick_btcusdt.db")

# Read a table from the database into a pandas dataframe
df = pd.read_sql_query("SELECT * FROM btcusdt", con)

# Close the database connection
con.close()

# Display the dataframe
print(df.head())
