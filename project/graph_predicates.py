import pyoxigraph as graph

connected_to = graph.NamedNode("http://moin-project.org/ontology/connectedTo")
has_trip = graph.NamedNode("http://moin-project.org/ontology/hasTrip")
duration = graph.NamedNode("http://moin-project.org/ontology/duration")
transport_type = graph.NamedNode("http://moin-project.org/ontology/transportType")
route = graph.NamedNode("http://moin-project.org/ontology/route")
drivingDistance = graph.NamedNode("http://moin-project.org/ontology/drivingDistance")

column_names = {
    "http://moin-project.org/ontology/route": "route",
    "http://moin-project.org/ontology/duration": "duration",
    "http://moin-project.org/ontology/transportType" : "transport_type",
    "http://moin-project.org/ontology/drivingDistance" : "driving_distance",
    }

transport_types = {
    "http://moin-project.org/ontology/train": "train",
    "http://moin-project.org/ontology/car": "car",
    "http://moin-project.org/ontology/flight": "flight",
}