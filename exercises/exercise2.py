import pandas as pd
from sqlalchemy import create_engine, BIGINT, FLOAT, TEXT

DATA_URL = "https://download-data.deutschebahn.com/static/datasets/haltestellen/D_Bahnhof_2020_alle.CSV"
DB_FILENAME = "data/trainstops.sqlite"
DB_TABLENAME = "trainstops"


def load_data(url: str) -> pd.DataFrame:
    return pd.read_csv(DATA_URL, sep=";", decimal=",")

def clean_data(data: pd.DataFrame) -> pd.DataFrame:

    # First, drop the "Status" column
    data = data.drop(columns=["Status"])  

    # Valid "Verkehr" values are "FV", "RV", "nur DPN"
    valid_verkehr = ["FV", "RV", "nur DPN"]
    data = data[data['Verkehr'].isin(valid_verkehr)]

    # Valid "Laenge", "Breite" values are geographic coordinate system values between and including -90 and 90
    data = data[data['Laenge'].between(-90, 90, inclusive='both')]
    data = data[data['Breite'].between(-90, 90, inclusive='both')]

    # Empty cells are considered invalid
    data = data[data.notnull().all(axis=1)]

    # Valid "IFOPT" values follow this pattern:
    # <exactly two characters>:<any amount of numbers>:<any amount of numbers><optionally another colon followed by any amount of numbers>
    data = data[data['IFOPT'].str.match(r'^[a-zA-Z]{2}:\d+:\d+(\:\d+)?$')]
    
    return data

def persist_data(data: pd.DataFrame, location: str, tablename: str) -> None:
    # Use fitting SQLite types (e.g., BIGINT, TEXT or FLOAT) for all columns
    types = {
            "EVA_NR": BIGINT,
            "DS100": TEXT,
            "IFOPT": TEXT,
            "NAME": TEXT,
            "Verkehr": TEXT,
            "Laenge": FLOAT,
            "Breite": FLOAT,
            "Betreiber_Name": TEXT,
            "Betreiber_Nr": BIGINT
        }

    engine = create_engine("sqlite:///"+location)
    data.to_sql(tablename, engine, if_exists="replace", index=False, dtype=types)
    engine.dispose()

df_trainstops = load_data(DATA_URL)
df_trainstops = clean_data(df_trainstops)
persist_data(df_trainstops, DB_FILENAME, DB_TABLENAME)
