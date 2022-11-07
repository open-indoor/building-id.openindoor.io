#!/usr/bin/env python3
import requests
import json
import argparse
import sys
import os
import osm2geojson
import re
import subprocess
import geojson

# https://wiki.openstreetmap.org/wiki/Indoor_Navigation_App_Content_Discovery_API

# PATH_INFO="" ./get_building_data.py
# curl https://osm.api.openindoor.io/

# Le Louvre
# PATH_INFO="/osm/places/relation/3262297/related" ./get_building_data.py

# PATH_INFO="/osm/places/way/55503397/related" ./get_building_data.py
# curl http://localhost/osm/places/way/55503397/related
# curl http://localhost:8097/osm/places/way/55503397/related
# curl https://building-id.openindoor.io/osm/places/way/55503397/related
# curl https://osm.api.openindoor.io/osm/places/way/55503397/related
# curl
# curl \
#   --header "X-RapidAPI-Host: osm-indoor-building.p.rapidapi.com" \
#   --header "X-RapidAPI-Key: c9d5519010mshf559cd43bb1c93dp14f22ejsnb2d285cc46bb" \
#   https://osm-indoor-building.p.rapidapi.com/osm/places/way/55503397/related
# curl https://gateway.openindoor.io/osm/places/way/55503397/related

def json2geojson(data: json):
    # print('data:', data)
    result = subprocess.run(
        ["osmtogeojson"],
        text=True,
        input=json.dumps(data, indent=None, separators=(",",":")),
        capture_output=True
    )
    return geojson.loads(result.stdout)
    # print('result:', result.stdout)

path_info = os.environ.get('PATH_INFO')
path_info = re.sub('/+', '/', path_info)
# print('path_info:', path_info)
f = open("demofile2.txt", "w")
f.write(str(path_info))
# f.write(str(sys.argv))
# f.write(str(os.environ))
# f.write(os.environ.get('PATH_INFO'))
# f.write(res)
f.close()

# path_info = "/55503397"
folder = path_info.split('/')
# print('folder:', folder)
# print('len(folder):', len(folder))
if len(folder) < 3:
    print("Content-Type: text/html")
    print("")
    print("""<html>
  <head>
    <title>Welcome to OpenIndoor API</title>
    <script type="application/ld+json">
      {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "OpenIndoor",
        "applicationCategory": "Metaverse",
        "creator": {
           "@type": "Organization",
           "name": "OpenIndoor",
           "url": "https://www.openindoor.net/"
        }
      }
    </script>
  </head>
</html>""")
    print("")
else:
    my_id = folder[4]
    my_type = folder[3]
    req_str = ""
    if (my_type == "way"):
        req_str = """[out:json][timeout:5];
way(id:""" + str(my_id) + """);
map_to_area->.b;
nwr(area.b);
out;"""
    elif (my_type == "relation"):
        req_str = """[out:json][timeout:25];
relation(id:""" + str(my_id) + """);
map_to_area->.b;
nwr(area.b);
out;"""
    res = {}
    try:
        r = requests.post(
            "https://overpass-api-world.openindoor.io/api/interpreter" ,
            data = req_str
        )
        res = r.json()

        if (len(folder) > 6 and folder[6] == "json"):
            print("Content-type: application/json")
            print("")
            print(json.dumps(res))
        else:
            # my_geojson = osm2geojson.json2geojson(res)
            my_geojson = json2geojson(res)
            print("Content-type: application/geo+json")
            print("")
            print(geojson.dumps(my_geojson, indent=None, separators=(",",":")))

    except Exception as e:
        print("HTTP/1.1 500 Internal Server Error")
        print("Content-Type: application/octet-stream")
        print("")
        print("Request error")
