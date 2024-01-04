import pandas as pd
import sqlite3

# DATA SOURCE 1:

import pytest

@pytest.fixture
def connection_df():
    cnx = sqlite3.connect('data/connections.sqlite')
    df = pd.read_sql_query("SELECT * FROM connections", cnx)
    cnx.close()
    return df

def test_connections_size(connection_df):
    assert len(connection_df) == 40515

def test_connections_index(connection_df):
    assert (connection_df.columns == pd.Index(['start', 'end', 'transport_type', 'route', 'duration', 'driving_distance'])).all()

# DATA SOURCE 2:

@pytest.fixture
def chargers_df():
    cnx = sqlite3.connect('data/charging_points_germany.sqlite')
    df = pd.read_sql_query("SELECT * FROM chargers", cnx)
    cnx.close()
    return df

def test_chargers_size(chargers_df):
    assert len(chargers_df) == 54225

def test_chargers_index(chargers_df):
    print("DATAFRAME:",chargers_df.columns)
    idx = ["operator", "city", "state", "district", "latitude", "longitude", "rated_capacity"]
    assert (chargers_df.columns == pd.Index(idx)).all()


# DATA SOURCE 3:
@pytest.fixture
def districts_df():
    cnx = sqlite3.connect('data/charging_points_development.sqlite')
    df = pd.read_sql_query("SELECT * FROM districts", cnx)
    cnx.close()
    return df

def test_distrits_size(districts_df):
    assert len(districts_df) == 401

def test_districts_index(districts_df):
    idx = ['location', 'state', '2017', '2018', '2019', '2020', '2021', '2022', '2023']

    assert (districts_df.columns == pd.Index(idx)).all()