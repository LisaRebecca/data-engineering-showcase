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
from graph_predicates import connected_to, has_trip, duration, transport_type, route, column_names, transport_types

import pandas as pd
import sqlite3
import pyoxigraph as graph
from pyoxigraph import Store
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
                    "iri_start": str(trip_from),
                    "iri_end": str(trip_to),
                }
            
            # triple represents properties of a specific trip
            if triple.predicate in [duration, transport_type, route]: 
                
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
df_connections = replace_from_dict(df_connections, "iri_start", IRI2Label)
df_connections = replace_from_dict(df_connections, "iri_end", IRI2Label)
df_connections = replace_from_dict(df_connections, "transport_type", transport_types)

df_connections.to_pickle("data/connections.pkl")

load_df_to_sqlite(df_connections, './data/connections.sqlite', 'connections')


# DATA SOURCE 2:

DATA_URL = "https://data.bundesnetzagentur.de/Bundesnetzagentur/SharedDocs/Downloads/DE/Sachgebiete/Energie/Unternehmen_Institutionen/E_Mobilitaet/ladesaeulenregister.csv"

df_charging_points = pd.read_csv(DATA_URL, encoding='latin-1', sep=";", skiprows=10)

df_charging_points.reset_index(drop=True)

df_charging_points.to_pickle("data/charging_points.pkl")

load_df_to_sqlite(df_charging_points, './data/ev_chargin_points_germany.sqlite', 'ev_chargin_points_germany')


# DATA SOURCE 3:

URL = "https://www.bundesnetzagentur.de/SharedDocs/Downloads/DE/Sachgebiete/Energie/Unternehmen_Institutionen/E_Mobilitaet/Ladesaeuleninfrastruktur.xlsx?__blob=publicationFile&v=28"

df_districts = pd.read_excel(URL, sheet_name="4.3 Ladepunkte je Kreis", skiprows=7, usecols="E:CI")

timestamps = create_timestamps(["1"],["Jan", "Apr", "Jul", "Oct"], ["2017", "2018", "2019", "2020", "2021", "2022", "2023"])
station_types = ["normal", "fast", "total"]

measurements = multiply_stringlists(timestamps, station_types)
measurements = measurements[:-3]

df_districts.columns = ["location", "state"] + measurements

df_districts = df_districts.drop(index=(len(df_districts)-1)) # drop last row, it only contains the sums

df_districts.to_pickle("data/districts.pkl")

load_df_to_sqlite(df_districts, './data/ev_chargin_points_per_district.sqlite', 'ev_chargin_points_per_district')
