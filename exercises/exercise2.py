import pandas as pd
from sqlalchemy import create_engine

DATA_URL = "https://download-data.deutschebahn.com/static/datasets/haltestellen/D_Bahnhof_2020_alle.CSV"
DB_FILENAME = "trainstops.sqlite"
DB_TABLENAME = "trainstops"

df_trainstops = pd.read_csv(DATA_URL, sep=";", decimal=",")
print(df_trainstops.columns)

# First, drop the "Status" column
df_trainstops = df_trainstops.drop(columns=["Status"])

print(df_trainstops.columns)
print(len(df_trainstops))

# Valid "Verkehr" values are "FV", "RV", "nur DPN"
valid_verkehr = ["FV", "RV", "nur DPN"]
df_trainstops = df_trainstops[df_trainstops['Verkehr'].isin(valid_verkehr)]

# Valid "Laenge", "Breite" values are geographic coordinate system values between and including -90 and 90
df_trainstops = df_trainstops[df_trainstops['Laenge'].between(-90, 90, inclusive='both')]
df_trainstops = df_trainstops[df_trainstops['Breite'].between(-90, 90, inclusive='both')]

# Empty cells are considered invalid
df_trainstops = df_trainstops[df_trainstops.notnull().all(axis=1)]

# Valid "IFOPT" values follow this pattern:
# <exactly two characters>:<any amount of numbers>:<any amount of numbers><optionally another colon followed by any amount of numbers>
df_trainstops = df_trainstops[df_trainstops['IFOPT'].str.match(r'^[a-zA-Z]{2}:\d+:\d+(\:\d+)?$')]
print(len(df_trainstops))

# Use fitting SQLite types (e.g., BIGINT, TEXT or FLOAT) for all columns

engine = create_engine("sqlite:///"+DB_FILENAME)
df_trainstops.to_sql(DB_TABLENAME, engine, if_exists="replace", index=True)
engine.dispose()

