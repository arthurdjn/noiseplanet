# -*- coding: utf-8 -*-

# Created on Thu Dec 5 16:49:20 2019

# @author: arthurd

"""
FoHex Module.

Generate HTML hexagonal maps.
"""


import folium
import numpy as np
import webbrowser

from noiseplanet.utils import hexgrid


def hexgrid_folium(folium_map, bbox, side_length=50000):
    """
    Add a grid of hexagons to a folium map.

    Parameters
    ----------
    folium_map : Folium Map
        Map on which the hexagonal grid will be added.
    bbox : Tuple
        Box of the area to generate the hexagons.
        Format : Lower X, Lower Y, Upper X, Upper Y.
    side_length : Float, optional
        Side length of the hexagons. The default is 50000.

    Returns
    -------
    folium_map : Folium Map
        Map with the added hexagons.
    """

    # Compute the hexbin grid in the webmercator system to have visually equal hexbin ...
    proj_init="epsg:4326"
    proj_out="epsg:3857"
    grid = hexgrid.hexbin_grid(bbox, side_length=side_length, proj_init=proj_init, proj_out=proj_out)

    print("size grid :", len(grid))

    # ... and reproject each hexagonal in the geographic system
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
        folium_geojson = folium.GeoJson(geojson,
                            style_function=lambda feature,
                            color=color: {
                                          'fillColor': color,
                                          'color':"black",
                                          'weight': 2,
                                          'dashArray': '5, 5',
                                          'fillOpacity': 0.55,
                                         })

        folium_map.add_child(folium_geojson)
  
    return folium_map


def add_polygon_folium(foloium_map, *polygon):
    """
    Add polygon to a folium map from their coordinates.

    Parameters
    ----------
    foloium_map : Folium Map
        Map where poygons are added.
    *polygon : List
        Polygons to add to the map.
        A polygon is a list of points, each points composed by lat, lon coordinates.

    Returns
    -------
    foloium_map : Folium Map
        Map with the polygons.
    """
    
    for poly in polygon:
        geojson = {"type": "FeatureCollection",
                    "properties":{
                            "lower_left": 0,
                            "upper_right": 0
                            },
                    "features": [{
                            "type":"Feature",
                            "geometry":{
                                    "type":"Polygon",
                                    "coordinates": [poly]
                                    }
                            }]
                    }

        color = 'skyblue'
        folium_geojson = folium.GeoJson(geojson,
                            style_function=lambda feature,
                            color=color: {
                                          'fillColor': color,
                                          'color':"black",
                                          'weight': 2,
                                          'dashArray': '5, 5',
                                          'fillOpacity': 0.55,
                                         })

        foloium_map.add_child(folium_geojson)
    
    return foloium_map




if __name__ == "__main__":
    # 1/ Create a grid
    foloium_map = folium.Map(zoom_start = 5, location=[55, 0])

    lower_left = [45.743860, 4.821815]
    upper_right = [45.763263, 4.858980]
    bbox = (lower_left[1], lower_left[0], upper_right[1], upper_right[0])
    foloium_map = hexgrid_folium(foloium_map, bbox, side_length=15)


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


    foloium_map = add_polygon_folium(foloium_map, *hexagons)


    foloium_map.save("my_hexbin_map2.html")
    webbrowser.open("my_hexbin_map2.html", new=2)  # open in new tab





