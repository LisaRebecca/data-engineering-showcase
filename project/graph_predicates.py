import pyoxigraph as graph

connected_to = graph.NamedNode("http://moin-project.org/ontology/connectedTo")
has_trip = graph.NamedNode("http://moin-project.org/ontology/hasTrip")
duration = graph.NamedNode("http://moin-project.org/ontology/duration")
transport_type = graph.NamedNode("http://moin-project.org/ontology/transportType")
route = graph.NamedNode("http://moin-project.org/ontology/route")

column_names = {
    "http://moin-project.org/ontology/route": "route",
    "http://moin-project.org/ontology/duration": "duration",
    "http://moin-project.org/ontology/transportType" : "transport_type",
    }

transport_types = {
    "http://moin-project.org/ontology/train": "train",
    "http://moin-project.org/ontology/car": "car",
    "http://moin-project.org/ontology/flight": "flight",
}