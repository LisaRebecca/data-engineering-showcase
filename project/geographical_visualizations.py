import geopandas as gpd
import matplotlib.pyplot as plt
import os
import urllib
import zipfile

if not os.path.exists('./GER_shape/'):
    urllib.request.urlretrieve('https://biogeo.ucdavis.edu/data/diva/adm/DEU_adm.zip', 'GER_shape.zip')
    with zipfile.ZipFile('GER_shape.zip', 'r') as zip_ref:
        zip_ref.extractall('GER_shape')
    os.remove('GER_shape.zip')

def plot_routes_on_germany_map(data, routes_column="route", color='red'):

    EPSG_GERMANY = 4326
    
    gdf_germany = gpd.read_file('./GER_shape/DEU_adm1.shp')
    gdf_germany = gdf_germany.to_crs(epsg=EPSG_GERMANY)
    
    plot_routes(data, EPSG_GERMANY, gdf_germany, routes_column=routes_column, color=color)


def plot_routes(data, crs, basemap, routes_column="route", color="red"):
    gdf_routes = gpd.GeoDataFrame(data, geometry=gpd.GeoSeries.from_wkt(data[routes_column]))
    gdf_routes.set_crs(epsg=crs, inplace=True)

    _, ax = plt.subplots(figsize=(20, 6))
    basemap.plot(ax=ax, edgecolor='black', color='grey', kind='geo')
    gdf_routes.plot(ax=ax, linewidth=1, color=color)
    plt.show()
