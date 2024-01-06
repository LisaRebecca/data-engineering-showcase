""" 
Write a script (for example in Python or Jayvee) that 
    - pulls the data sets you chose from the internet, 
    - transforms it,
    - fixes errors, 
    - finally stores your data in the /data directory
Place the script in the /project directory (any file name is fine)
The output of the script should be: 
    - datasets in your /data directory (e.g., as SQLite databases) 

"""
from graph_predicates import connected_to, has_trip, duration, drivingDistance, transport_type, route, column_names, transport_types

import pandas as pd
import sqlite3
import pyoxigraph as graph
from pyoxigraph import Store
import isodate
import itertools
from urllib.request import urlretrieve
import bz2


def download_file(URL: str, output_file: str) -> None:
    urlretrieve(URL, output_file)
    return output_file

def unpack_bz2_archive(input_file) -> str :
    zipfile = bz2.BZ2File(input_file)
    data = zipfile.read()
    output_file = filename[:-4]
    open(output_file, 'wb').write(data)
    return output_file

def get_triple_list(graph_file_path: str) -> list:
    return list(graph.parse(graph_file_path, "text/turtle", base_iri="http://example.com/"))

def extract_trips_from_graph(triples: list)-> pd.DataFrame:
    connections = {}
    for triple in triples:
        try:
            # triple represents a trip between two cities
            if triple.predicate == has_trip: 
                
                trip_from = triple.subject.subject.value
                trip_to = triple.subject.object.value
                trip_id = triple.object.value
                
                connections[trip_id] = {
                    "start": str(trip_from),
                    "end": str(trip_to),
                }
            
            # triple represents properties of a specific trip
            if triple.predicate in [duration, transport_type, route, drivingDistance]: 
                
                trip_id = triple.subject.value
                pred_name = triple.predicate.value
                pred_value = triple.object.value
                
                connections[trip_id][str(pred_name)] = str(pred_value)

        except AttributeError:
            print("Error with triple: ", triple)

    return pd.DataFrame(connections).T.reset_index(drop=True)

def extract_labels_from_graph(graph_path: str, label_iri="http://www.w3.org/2000/01/rdf-schema#label") -> dict:
    store = Store()
    store.load(graph_path, mime_type="text/turtle")
    
    result = store.query("SELECT ?subject ?object WHERE { ?subject <"+label_iri+"> ?object}")
    IRI2Label = {}
    for r in result:
        IRI2Label[str(r["subject"].value)] = r["object"].value
    return IRI2Label

def convert_duration_to_minutes(duration_str):
    duration = isodate.parse_duration(duration_str)
    return int(duration.total_seconds()/60)

def replace_from_dict(data: pd.DataFrame, column_name: str, map: dict) -> pd.DataFrame:
    def f(key):
        if key in list(map.keys()):
            return map[key]
        
    data[column_name] = data[column_name].apply(f)
    return data

def create_timestamps(days: list, months: list, years: list) -> list:
    timestamps = ['-'.join(tuple) for tuple in list(itertools.product(years, months))]
    timestamps = ['-'.join(tuple) for tuple in list(itertools.product(timestamps, days))]
    return timestamps

def multiply_stringlists(first: list, second: list) -> list:
    return ['-'.join(tuple) for tuple in list(itertools.product(first, second))]

def load_df_to_sqlite(df: pd.DataFrame, db_location: str, table_name: str):
    engine = sqlite3.connect(db_location)
    df.to_sql(table_name, con=engine, index=False, if_exists='replace')


# DATA SOURCE 1:

DATA_URL = ("https://mobilithek.info/mdp-api/files/aux/573356838940979200/moin-2022-05-02.1-20220502.131229-1.ttl.bz2")
filename = "city_connections.ttl.bz2"

archive_file_path = download_file(DATA_URL, filename)

graph_file_path = unpack_bz2_archive(archive_file_path)

triples = get_triple_list(graph_file_path)
df_connections = extract_trips_from_graph(triples)

df_connections = df_connections.rename(columns=column_names)

IRI2Label = extract_labels_from_graph(graph_file_path)
df_connections = replace_from_dict(df_connections, "start", IRI2Label)
df_connections = replace_from_dict(df_connections, "end", IRI2Label)
df_connections = replace_from_dict(df_connections, "transport_type", transport_types)

df_connections["duration"] = df_connections["duration"].apply(convert_duration_to_minutes)
df_connections["driving_distance"] = df_connections["driving_distance"].apply(lambda x: float(x) / 1000)

df_connections.to_pickle("data/connections.pkl")

load_df_to_sqlite(df_connections, './data/connections.sqlite', 'connections')


# DATA SOURCE 2:

DATA_URL = "https://data.bundesnetzagentur.de/Bundesnetzagentur/SharedDocs/Downloads/DE/Sachgebiete/Energie/Unternehmen_Institutionen/E_Mobilitaet/ladesaeulenregister.csv"

df_charging_points = pd.read_csv(DATA_URL, encoding='latin-1', sep=";", skiprows=10)

df_charging_points.reset_index(drop=True)

column_names = {
    "Betreiber":"operator",
    "Ort":"city",
    "Bundesland":"state",
    "Kreis/kreisfreie Stadt":"district",
    "Längengrad":"longitude",
    "Breitengrad":"latitude",
    "Nennleistung Ladeeinrichtung [kW]":"rated_capacity",
}

df_charging_points = df_charging_points.rename(columns=column_names)

df_charging_points = df_charging_points[df_charging_points.columns.intersection(set(column_names.values()))]

df_charging_points["longitude"] = df_charging_points["longitude"].apply(lambda x: float(str(x).replace(",",".")))
df_charging_points["latitude"] = df_charging_points["latitude"].apply(lambda x: float(str(x).replace(",",".")))
df_charging_points["rated_capacity"] = df_charging_points["rated_capacity"].apply(lambda x: float(str(x).replace(",",".")))

df_charging_points = df_charging_points.dropna(how="all")

df_charging_points.to_pickle("data/chargers.pkl")

load_df_to_sqlite(df_charging_points, './data/charging_points_germany.sqlite', 'chargers')


# DATA SOURCE 3:

URL = "https://www.bundesnetzagentur.de/SharedDocs/Downloads/DE/Sachgebiete/Energie/Unternehmen_Institutionen/E_Mobilitaet/Ladesaeuleninfrastruktur.xlsx?__blob=publicationFile&v=28"

df_districts = pd.read_excel(URL, sheet_name="4.3 Ladepunkte je Kreis", skiprows=7, usecols="E:CI")
df_districts = df_districts.drop(index=(len(df_districts)-1)) # drop last row, it only contains the sums

df_districts['Unnamed: 4'] = df_districts['Unnamed: 4'].apply(lambda x: x.replace("Landkreis ", "").replace("-Kreis", "").replace("kreis", "").replace("Kreisfreie Stadt ", "").replace("Stadt ", "").replace("Kreis ", "").replace(" Kreis", ""))

districts = df_districts["Unnamed: 4"]
states = df_districts["Unnamed: 5"]

cols_total = df_districts.columns.str.contains('gesamt')
cols_january = [ (i%4==0) for i in range(27)]

df_districts = df_districts.loc[:, cols_total]
df_districts = df_districts.loc[:, cols_january]
df_districts = pd.concat([districts, states, df_districts], axis=1)

df_districts.columns = ["location", "state"] + [str(t) for t in range(2017, 2024)]

df_districts.to_pickle("data/districts.pkl")

load_df_to_sqlite(df_districts, './data/charging_points_development.sqlite', 'districts')
