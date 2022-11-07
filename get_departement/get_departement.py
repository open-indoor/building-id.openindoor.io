#!/usr/bin/env python3
# import requests
import json
# import argparse
# import sys
import os
# import osm2geojson
import re
# import subprocess
# import geojson

import geopandas as gpd
import pandas as pd
# from pathlib import Path
import glob
from flask import Flask
from shapely.geometry import Point, Polygon, shape

# hapely.geometry.shape()

# assign directory
 
# iterate over files in
# that directory
# files = Path(directory).glob('*.geojson')
# for file in files:
#     print(file)


    # clip stuff with gdf

    # save the clip result

app = Flask("get_departement") # Needs defining at file global scope for thread-local sharing
gdf = None
def setup_app(app):
    global gdf
    # directory = 'data/region'
    # gdf_list = []
    gdf = gpd.read_file("data/departements-20180101.shp")
    # for geofile in glob.iglob('data/region/*.geojson'):
    #     print('geofile:', geofile)
    #     my_gdf = gpd.read_file(geofile)
    #     my_region = os.path.splitext(os.path.basename(geofile))[0]
    #     print(my_region)
    #     my_gdf['region'] = my_region
    #     gdf_list.append(my_gdf)
    # gdf = pd.concat(gdf_list)

setup_app(app)

@app.route("/europe/france/departement/<float(signed=True):latitude>/<float(signed=True):longitude>")
def get_departement(latitude, longitude):
    point = Point(longitude,latitude)
    # indoors.intersects(shap).any()
    # print('gdf:', gdf)
    for index,row in gdf.iterrows(): # Looping over all points
        # polygon = Polygon(row["geometry"])
        my_shape = shape(row["geometry"])
        # return "my_shape:" + str(my_shape)

        # print('')
        region = "None"
        if (point.intersects(my_shape)):
            region = re.sub('\D', '', row["code_insee"])
            break
    response = app.response_class(
        response=json.dumps({"region": region}),
        status=200,
        mimetype='application/json'
    )
    return response


# print('departement:', get_departement(48.8590, 2.3486))




if __name__ == '__main__':
    app.run(host="0.0.0.0")