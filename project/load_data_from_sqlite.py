"""
This script shows an example how to load the serialized datasets from their sqlite representation into a dataframe.
"""

import pandas as pd
import sqlite3

cnx = sqlite3.connect('/Users/lisaschmidt/Documents/GitHub/data-engineering-showcase/data/connections.sqlite')
df = pd.read_sql_query("SELECT * FROM connections", cnx)
print(df.head)