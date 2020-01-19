# -*- coding: utf-8 -*-
'''
Created on Wed Dec 18 16:34:04 2019

@author: Utilisateur
'''

import numpy as np
import pandas as pd

"""

DEPRECATED !!!

"""
    


def geojson_to_df(geojson, extract_coordinates=True):

    
    data = {'type': []}
    if extract_coordinates:
        data['longitude'] = []
        data['latitude'] = []
        data['elevation'] = []
    else:
        data['coordinates'] = []
    properties = []
    count_prop = 0
    for feature in geojson['features']:
        if feature['geometry'] is not None:        
            # geometry
            data['type'].append(feature['geometry']['type'])
            if extract_coordinates:
                data['longitude'].append(feature['geometry']['coordinates'][0])
                data['latitude'].append(feature['geometry']['coordinates'][1])
                data['elevation'].append(feature['geometry']['coordinates'][2])
            else:
                data['coordinates'].append(feature['geometry']['coordinates'])
        else:
            # geometry
            data['type'].append(None)
            if extract_coordinates:
                data['longitude'].append(np.nan)
                data['latitude'].append(np.nan)
                data['elevation'].append(np.nan)
            else:
                data['coordinates'].append(np.nan)
            
        # properties
        for prop in feature['properties']:
            if prop in properties:
                data[prop].append(feature['properties'][prop])
            else:
                data[prop] = [np.nan] * count_prop + [feature['properties'][prop]]
                properties.append(prop)
        for key in np.setdiff1d(properties, feature['properties'], assume_unique=True):
            if key not in feature['properties']:
                data[key].append(np.nan)
                
        count_prop += 1
    df = pd.DataFrame(data)
    return df
   


def df_to_geojson(df, properties, geometry_type='type', 
                  lat='latitude', lon='longitude', z='elevation'):
    gj = {'type':'FeatureCollection', 'features':[]}
    for _, row in df.iterrows():
        feature = {'type':'Feature',
                   'properties':{},
                   'geometry':{'type': row[geometry_type],
                               'coordinates':[]}}
        feature['geometry']['coordinates'] = [row[lon], row[lat], row[z]]
        for prop in properties:
            feature['properties'][prop] = row[prop]
        gj['features'].append(feature)
    return gj


def properties_to_df(filepath, sep='=', comment_char='#'):
    """
    Read the file passed as parameter as a properties file.
    """
    props = {}
    with open(filepath, "rt") as f:
        for line in f:
            l = line.strip()
            if l and not l.startswith(comment_char):
                key_value = l.split(sep)
                key = key_value[0].strip()
                value = sep.join(key_value[1:]).strip().strip('"') 
                props[key] = value 
    return pd.DataFrame(data=props, index=[0])


def poly_to_geojson(polygon, properties={'id':'0'}):
    gj = {"type": "FeatureCollection",
                    "properties": properties,
                    "features": [{
                            "type":"Feature",
                            "geometry":{
                                    "type":"Polygon",
                                    "coordinates": [polygon]
                                    }
                            }]
            }
    return gj




    
    
    
    
        