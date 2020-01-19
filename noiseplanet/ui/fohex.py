# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 22:16:26 2019

@author: arthurd
"""


import folium
import numpy as np
import webbrowser

import json

from noiseplanet.utils import hexgrid


def hexgrid_folium(m, bbox, side_length=50000):

    # Compute the hexbin grid in the webmercator system to have visually equal hexbin ...
    proj_init="epsg:4326"
    proj_out="epsg:3857"
    grid = hexgrid.hexbin_grid(bbox, side_length=side_length, proj_init=proj_init, proj_out=proj_out)

    # ... and reproject each hexagonal in the geographic system
    # save in local the geojson
    features = []
    
    for hexagon in grid:
        feature = { "type":"Feature",
                    "geometry":{
                            "type":"Polygon",
                            "coordinates": [hexagon]
                            }
                    }
        features.append(feature)
        geojson = {"type": "FeatureCollection",
                    "properties":{
                            "lower_left": (bbox[0], bbox[1]),
                            "upper_right": (bbox[2], bbox[3])
                            },
                    "features": [feature]
                    }

        color = 'skyblue'
        gj = folium.GeoJson(geojson,
                            style_function=lambda feature,
                            color=color: {
                                          'fillColor': color,
                                          'color':"black",
                                          'weight': 2,
                                          'dashArray': '5, 5',
                                          'fillOpacity': 0.55,
                                         })

        m.add_child(gj)

    folium.CircleMarker(location=[bbox[0], bbox[1]],
                    radius=5,
                    weight=1,
                    color="red",
                    fill=True,
                    fill_opacity=1).add_to(m)

    folium.CircleMarker(location=[bbox[2], bbox[3]],
                    radius=5,
                    weight=1,
                    color="red",
                    fill=True,
                    fill_opacity=1).add_to(m)


    m.save("my_hexbin_map2.html")
    webbrowser.open("my_hexbin_map2.html", new=2)  # open in new tab

    geojsons = {"type": "FeatureCollection",
                "properties":{
                        "lower_left": (bbox[0], bbox[1]),
                        "upper_right": (bbox[2], bbox[3])
                        },
                "features": features 
                }

    # Write the geojson
    outname = 'hex2' + '.geojson'

    with open(outname, 'w') as f:
        json.dump(geojsons, f)



    return m


def add_hexagons_folium(m, hexagons):
    for hexagon in hexagons:
        geo_json = {"type": "FeatureCollection",
                    "properties":{
                            "lower_left": 0,
                            "upper_right": 0
                            },
                    "features": [{
                            "type":"Feature",
                            "geometry":{
                                    "type":"Polygon",
                                    "coordinates": [hexagon]
                                    }
                            }]
                    }

        color = 'skyblue'
        gj = folium.GeoJson(geo_json,
                            style_function=lambda feature,
                            color=color: {
                                          'fillColor': color,
                                          'color':"black",
                                          'weight': 2,
                                          'dashArray': '5, 5',
                                          'fillOpacity': 0.55,
                                         })

        m.add_child(gj)

    m.save("my_hexbin_map.html")
    webbrowser.open("my_hexbin_map.html", new=2)  # open in new tab








if __name__ == "__main__":
    # 1/ Create a grid
    m = folium.Map(zoom_start = 5, location=[55, 0])

    lower_left = [45.75, 4.85]
    upper_right = [45.76, 4.86]
    bbox = (lower_left[1], lower_left[0], upper_right[1], upper_right[0])
    hexgrid_folium(m, bbox, side_length=15)


    proj_init="epsg:4326"
    proj_out="epsg:3857"

    lon = np.random.rand(40)/2 + 3
    lat = np.random.rand(40) + 45
    # origin = (-179.99999999, -89.99999999)
    origin = (0, 0)
    side_length = 15000

    R = 0.5 * side_length * 1/(np.sin(np.deg2rad(30)))
    r = R * np.cos(np.deg2rad(30))


    Q, R = hexgrid.nearest_hexagons(lon, lat, side_length=side_length, origin=origin,
                        proj_init=proj_init, proj_out=proj_out)
    Xcenter, Ycenter = hexgrid.hexs_to_cartesians(Q, R, side_length=side_length, origin=origin,
                        proj_init=proj_out, proj_out=proj_init)
    hexagons = hexgrid.hexagons_coordinates(Xcenter, Ycenter, side_length=side_length,
                                    proj_init=proj_init, proj_out=proj_out)


    add_hexagons_folium(m, hexagons)








