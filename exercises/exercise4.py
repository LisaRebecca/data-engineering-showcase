import urllib.request
import zipfile
import pandas as pd
import sqlite3
import os

def download_and_unzip(url, zip_path, folder):
    urllib.request.urlretrieve(url, zip_path)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(folder)
    return os.path.join(folder, 'data.csv')

def reshape_data(csv_file_path):
    df =  pd.read_csv(csv_file_path, sep=";", index_col=False, usecols=["Geraet", "Hersteller", "Model", "Monat", "Temperatur in °C (DWD)", "Batterietemperatur in °C", "Geraet aktiv"])
    df.rename(columns={'Temperatur in °C (DWD)': 'Temperatur', 'Batterietemperatur in °C': 'Batterietemperatur'}, inplace=True)
    return df

def transform_data(df):
    df['Temperatur'] = df['Temperatur'].apply(lambda x: float(str(x).replace(",",".")))
    df['Temperatur'] = df['Temperatur'] * 9/5 + 32
    df['Batterietemperatur'] = df['Batterietemperatur'].apply(lambda x: float(str(x).replace(",",".")))
    df['Batterietemperatur'] = df['Batterietemperatur'] * 9/5 + 32
    return df

def validate_data(df):
    return df[df['Geraet'] > 0]

def save_to_sqlite(df, db_path, table_name):
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()

url = "https://www.mowesta.com/data/measure/mowesta-dataset-20221107.zip"
zip_path = 'mowesta-dataset-20221107.zip'
data_path = 'mowesta_dataset'

csv_file_path = download_and_unzip(url, zip_path, data_path)
df = reshape_data(csv_file_path)
df = transform_data(df)
df = validate_data(df)
save_to_sqlite(df, 'temperatures.sqlite', 'temperatures')
