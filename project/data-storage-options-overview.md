# Overview: Data Storage Options

## Datasets

- Dataset 1: Graph data, ttl-serialization
- Dataset 2: Tabular data, CSV
- Dataset 3: Tabular Data, XLSX

## Different Data Formats for the Datasets

### Dataset 1
1. Store it as a graph but provide interface functions which allow for easy extraction of data which is needed so that you don't have to write graph db requests.
2. Transform it into a relational format.

Advice by the teaching staff:
> Graph databases have a place when you need to traverse over the graph data frequently. If you don't need to do that, then I'd rather transform the data into a better suiting format (e.g. tabular).

<mark>Decision: Dataset 1 will be transformed into a tabular format.</mark>


### Dataset 2
<mark>Decision: Dataset 2 is already in a relational format and should stay the same.</mark>

### Dataset 3
<mark>Decision: Dataset 3 is already in a relational format and should stay the same.</mark>

## Different Storage Formats for the Datasets

Common relational Formats:
- dataframe serialization: .pkl, .parquet
- database serialization: .sqlite, duck-db

Advice by the teaching staff:
> [A database is] better [than a dataframe] for querying the data without loading it into RAM completely
> Using a database is also more portable in the sense that you could also write code in other languages more easily,

<mark>The datasets will be stored as a .sqlite database.</mark>
