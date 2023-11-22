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
import pandas as pd
import sqlite3
import pyoxigraph as graph
from pyoxigraph import Store
import itertools
from urllib.request import urlretrieve
import bz2

# DATA SOURCE 1:

url = ("https://mobilithek.info/mdp-api/files/aux/573356838940979200/moin-2022-05-02.1-20220502.131229-1.ttl.bz2")
filename = "city_connections.ttl.bz2"
urlretrieve(url, filename)

zipfile = bz2.BZ2File(filename)
data = zipfile.read()
newfilepath = filename[:-4]
open(newfilepath, 'wb').write(data)

l = list(graph.parse(newfilepath, "text/turtle", base_iri="http://example.com/"))
store = Store()
store.load(newfilepath, mime_type="text/turtle")

connected_to = graph.NamedNode("http://moin-project.org/ontology/connectedTo")
has_trip = graph.NamedNode("http://moin-project.org/ontology/hasTrip")

connections = {}
for triple in l:
    try:
        subject, predicate, object = triple.subject, triple.predicate, triple.object
        if predicate == has_trip: #subject.predicate == connected_to and 
            trip_from = subject.subject
            trip_to = subject.object
            trip_id = triple.object
            connections[trip_id.value] = {
                "iri_start": str(trip_from.value),
                "iri_end": str(trip_to.value),
            }
    except AttributeError:
        print("Error with triple: ", triple)

duration = graph.NamedNode("http://moin-project.org/ontology/duration")
transport_type = graph.NamedNode("http://moin-project.org/ontology/transportType")
route = graph.NamedNode("http://moin-project.org/ontology/route")

for triple in l:
    try:
        subject, predicate, object = triple.subject, triple.predicate, triple.object
        pred_name = None
        pred_value = None
        if predicate in [duration, transport_type, route]:
            trip_id = triple.subject.value
            pred_name = triple.predicate.value
            pred_value = triple.object.value
            connections[trip_id][str(pred_name)] = str(pred_value)
    except AttributeError:
        print("Error with triple: ", triple)

df_connections = pd.DataFrame(connections).T
print(df_connections.head())

PREDICATE_LABEL = "http://www.w3.org/2000/01/rdf-schema#label"
IRI2Label = {}
result = store.query("SELECT ?subject ?object WHERE { ?subject <"+PREDICATE_LABEL+"> ?object}")

for r in result:
    IRI2Label[str(r["subject"].value)] = r["object"].value

def replace_with_label(iri):
    if iri in list(IRI2Label.keys()):
        return IRI2Label[iri]
    
def replace_transport_iri_with_label(transport_type_iri):
    if transport_type_iri == "http://moin-project.org/ontology/train":
        return "train"
    if transport_type_iri == "http://moin-project.org/ontology/car":
        return "car"
    if transport_type_iri == "http://moin-project.org/ontology/flight":
        return "flight"

df_connections["iri_start"] = df_connections["iri_start"].apply(replace_with_label)
print(df_connections.head())
df_connections["iri_end"] = df_connections["iri_end"].apply(replace_with_label)
df_connections["http://moin-project.org/ontology/transportType"] = df_connections["http://moin-project.org/ontology/transportType"].apply(replace_transport_iri_with_label)

df_connections = df_connections.rename(columns={
    "http://moin-project.org/ontology/route": "route",
    "http://moin-project.org/ontology/duration": "duration",
    "http://moin-project.org/ontology/transportType" : "transport_type",
    })

engine = sqlite3.connect('./data/connections.sqlite')
print(df_connections.head())
df_connections.to_sql('connections', con=engine, index=True, if_exists='replace')


# DATA SOURCE 2:

DATA_URL = "https://data.bundesnetzagentur.de/Bundesnetzagentur/SharedDocs/Downloads/DE/Sachgebiete/Energie/Unternehmen_Institutionen/E_Mobilitaet/ladesaeulenregister.csv"

df_charging_points = pd.read_csv(DATA_URL, encoding='latin-1', sep=";", skiprows=10)

engine = sqlite3.connect('./data/ev_chargin_points_germany.sqlite')

df_charging_points.to_sql('ev_chargin_points_germany', con=engine, index=False, if_exists='replace')


# DATA SOURCE 3:
URL = "https://www.bundesnetzagentur.de/SharedDocs/Downloads/DE/Sachgebiete/Energie/Unternehmen_Institutionen/E_Mobilitaet/Ladesaeuleninfrastruktur.xlsx?__blob=publicationFile&v=28"

measuring_dates = ["01-Jan-", "01-Apr-", "01-Jul-", "01-Oct-"]
dates = [ date+str(year) for year in range(2017, 2024) for date in measuring_dates ]
station_types = ["normal", "fast", "total"]

dates_and_types = ['-'.join(tuple) for tuple in list(itertools.product(dates, station_types))]
dates_and_types = dates_and_types[:-3]

columns = ["location", "state"] + dates_and_types

df_districts = pd.read_excel(URL, sheet_name="4.3 Ladepunkte je Kreis", skiprows=7, usecols="E:CI")
df_districts.columns = columns
df_districts = df_districts.drop(index=(len(df_districts)-1)) # drop last row
engine = sqlite3.connect('./data/ev_chargin_points_per_district.sqlite')
df_districts.to_sql('ev_chargin_points_per_district', con=engine, index=False, if_exists='replace')