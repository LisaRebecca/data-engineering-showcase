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
    assert (connection_df.columns == pd.Index(['iri_start', 'iri_end', 'transport_type', 'route', 'duration'])).all()

# DATA SOURCE 2:

@pytest.fixture
def chargers_df():
    cnx = sqlite3.connect('data/ev_chargin_points_germany.sqlite')
    df = pd.read_sql_query("SELECT * FROM ev_chargin_points_germany", cnx)
    cnx.close()
    return df

def test_chargers_size(chargers_df):
    assert len(chargers_df) == 54225

def test_chargers_index(chargers_df):
    idx = ['Betreiber', 'Straße', 'Hausnummer', 'Adresszusatz', 'Postleitzahl',
        'Ort', 'Bundesland', 'Kreis/kreisfreie Stadt', 'Breitengrad',
        'Längengrad', 'Inbetriebnahmedatum',
        'Nennleistung Ladeeinrichtung [kW]', 'Art der Ladeeinrichung',
        'Anzahl Ladepunkte', 'Steckertypen1', 'P1 [kW]', 'Public Key1',
        'Steckertypen2', 'P2 [kW]', 'Public Key2', 'Steckertypen3', 'P3 [kW]',
        'Public Key3', 'Steckertypen4', 'P4 [kW]', 'Public Key4']
    assert (chargers_df.columns == pd.Index(idx)).all()


# DATA SOURCE 3:
@pytest.fixture
def districts_df():
    cnx = sqlite3.connect('data/ev_chargin_points_per_district.sqlite')
    df = pd.read_sql_query("SELECT * FROM ev_chargin_points_per_district", cnx)
    cnx.close()
    return df

def test_distrits_size(districts_df):
    assert len(districts_df) == 401

def test_districts_index(districts_df):
    idx = ['location', 'state', '2017-Jan-1-normal', '2017-Jan-1-fast',
        '2017-Jan-1-total', '2017-Apr-1-normal', '2017-Apr-1-fast',
        '2017-Apr-1-total', '2017-Jul-1-normal', '2017-Jul-1-fast',
        '2017-Jul-1-total', '2017-Oct-1-normal', '2017-Oct-1-fast',
        '2017-Oct-1-total', '2018-Jan-1-normal', '2018-Jan-1-fast',
        '2018-Jan-1-total', '2018-Apr-1-normal', '2018-Apr-1-fast',
        '2018-Apr-1-total', '2018-Jul-1-normal', '2018-Jul-1-fast',
        '2018-Jul-1-total', '2018-Oct-1-normal', '2018-Oct-1-fast',
        '2018-Oct-1-total', '2019-Jan-1-normal', '2019-Jan-1-fast',
        '2019-Jan-1-total', '2019-Apr-1-normal', '2019-Apr-1-fast',
        '2019-Apr-1-total', '2019-Jul-1-normal', '2019-Jul-1-fast',
        '2019-Jul-1-total', '2019-Oct-1-normal', '2019-Oct-1-fast',
        '2019-Oct-1-total', '2020-Jan-1-normal', '2020-Jan-1-fast',
        '2020-Jan-1-total', '2020-Apr-1-normal', '2020-Apr-1-fast',
        '2020-Apr-1-total', '2020-Jul-1-normal', '2020-Jul-1-fast',
        '2020-Jul-1-total', '2020-Oct-1-normal', '2020-Oct-1-fast',
        '2020-Oct-1-total', '2021-Jan-1-normal', '2021-Jan-1-fast',
        '2021-Jan-1-total', '2021-Apr-1-normal', '2021-Apr-1-fast',
        '2021-Apr-1-total', '2021-Jul-1-normal', '2021-Jul-1-fast',
        '2021-Jul-1-total', '2021-Oct-1-normal', '2021-Oct-1-fast',
        '2021-Oct-1-total', '2022-Jan-1-normal', '2022-Jan-1-fast',
        '2022-Jan-1-total', '2022-Apr-1-normal', '2022-Apr-1-fast',
        '2022-Apr-1-total', '2022-Jul-1-normal', '2022-Jul-1-fast',
        '2022-Jul-1-total', '2022-Oct-1-normal', '2022-Oct-1-fast',
        '2022-Oct-1-total', '2023-Jan-1-normal', '2023-Jan-1-fast',
        '2023-Jan-1-total', '2023-Apr-1-normal', '2023-Apr-1-fast',
        '2023-Apr-1-total', '2023-Jul-1-normal', '2023-Jul-1-fast',
        '2023-Jul-1-total']

    assert (districts_df.columns == pd.Index(idx)).all()