import pandas as pd
import sqlite3
from pandas.testing import assert_frame_equal

cnx = sqlite3.connect('/Users/lisaschmidt/Documents/GitHub/data-engineering-showcase/data/connections.sqlite')
df = pd.read_sql_query("SELECT * FROM connections", cnx)

assert len(df) == 40515

reference = pd.read_pickle("data/connections_reference.pkl").reset_index(drop=True)
new = pd.read_pickle("data/connections.pkl").reset_index(drop=True)

assert_frame_equal(reference, new)


cnx = sqlite3.connect('data/ev_chargin_points_germany.sqlite')
df = pd.read_sql_query("SELECT * FROM ev_chargin_points_germany", cnx)

assert len(df) == 51472

cnx = sqlite3.connect('data/ev_chargin_points_per_district.sqlite')
df = pd.read_sql_query("SELECT * FROM ev_chargin_points_per_district", cnx)

assert len(df) == 401

