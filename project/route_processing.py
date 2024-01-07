import pandas as pd


def aggregate_travel_modes(df_connections):
    df_car = df_connections[df_connections['transport_type'] == 'car']
    df_train = df_connections[df_connections['transport_type'] == 'train']

    fastest_car = df_car.loc[df_car.groupby(['start', 'end'])['duration'].idxmin()]
    fastest_train = df_train.groupby(['start', 'end'])['duration'].min().reset_index()

    df_connectivity = pd.merge(fastest_car, fastest_train, on=['start', 'end'], suffixes=('_car', '_train'))
    return df_connectivity

def calculate_absolute_deviation(row, column1='duration_car', column2='duration_train'):
    a = row[column1]
    b = row[column2]
    return b - a

def calculate_relative_deviation(row, column1='duration_car', column2='duration_train'):
    a = row[column1]
    b = row[column2]
    absolute_deviation = b - a
    return absolute_deviation / a * 100

def calculate_density(route, chargers_gdf, buffer_distance=5000):

    buffer = route.geometry.buffer(buffer_distance)
    chargers_in_buffer = chargers_gdf.within(buffer)
    count_chargers = chargers_in_buffer.sum()
    route_length_meters = route.geometry.length
    density = count_chargers / route_length_meters if route_length_meters else 0
    return density

from shapely.ops import nearest_points
import numpy as np
def calculate_nearest_distances(route, chargers_gdf, num_points_per_km=0.1):
    num_points = 10#int(route.geometry.length * 1000 * num_points_per_km)

    points = [route.geometry.interpolate(i/num_points, normalized=True) for i in range(num_points + 1)]
    
    distances = []
    for point in points:
        nearest_charger = nearest_points(point, chargers_gdf.unary_union)[1]
        distance = point.distance(nearest_charger)
        distances.append(distance)
    
    return np.mean(distances)

def calculate_coverage_ratio(route, chargers_gdf, max_distance):

    chargers_buffer = chargers_gdf.buffer(max_distance)

    covered_length = 0

    for charger in chargers_buffer:
        if charger.intersects(route.geometry):
            intersection = charger.intersection(route.geometry)
            covered_length += intersection.length

    total_route_length = route.geometry.length
    coverage_ratio = covered_length / total_route_length if total_route_length else 0

    return coverage_ratio

def process_route(route, chargers_gdf):
    density = calculate_density(route, chargers_gdf)
    avg_dist = calculate_nearest_distances(route, chargers_gdf)
    #coverage = calculate_coverage_ratio(route, chargers_gdf, max_distance=500)
    return density, avg_dist#, coverage

def project_to_meters(geodataframe, to=32632):
    return geodataframe.set_crs(epsg=4326).to_crs(epsg=to)

def compute_connectivity_metrics(df_chargers, df_connectivity):
    import geopandas as gpd
    from shapely.geometry import Point
    from shapely.wkt import loads

    # Convert to GeoDataFrames
    df_chargers['geometry'] = df_chargers.apply(lambda row: Point(float(row.longitude), float(row.latitude)), axis=1)
    gdf_chargers = gpd.GeoDataFrame(df_chargers, geometry='geometry')
    df_connectivity['geometry'] = df_connectivity['route'].apply(lambda x: loads(x))
    gdf_connectivity = gpd.GeoDataFrame(df_connectivity, geometry='geometry')

    # project to a coordinate system that uses meters 
    gdf_chargers = project_to_meters(gdf_chargers)
    gdf_connectivity = project_to_meters(gdf_connectivity)

    from joblib import Parallel, delayed
    from multiprocessing import cpu_count
    from tqdm import tqdm

    routes_list = [route for _, route in gdf_connectivity.iterrows()]
    results = Parallel(n_jobs=cpu_count())(delayed(process_route)(route, gdf_chargers) for route in tqdm(routes_list))

    densities, distances = zip(*results)

    df_connectivity['charger_density'] = densities
    df_connectivity['avg_dist_charger'] = distances
    df_connectivity[:5]

    return densities, distances