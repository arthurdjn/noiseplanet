# -*- coding: utf-8 -*-
'''
Created on Wed Dec 18 16:34:04 2019

@author: Utilisateur
'''

import numpy as np
import pandas as pd
import json

from os import listdir
from os.path import join



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



def open_files(dir_name, ext="geojson"):
    """
        *** Get the path of all files in a directory ***
    
    :param dir_name: Name or path to the directory where the files you want to
            open are saved.
    type dir_name: String
    :param ext: The files extension you want to open.
    type ext: String
    
    return: A list of the path of all files saved in the directory, with the extension
            geojson by default.
    rtype: array like
    
    -----------------------------------------------------------------------
    Example :
        >>> dir_name = "path/to/your/directory"
        >>> files = open_files(dir_name, ext="geojson")
        >>> files
            ['../test/track_test/track.geojson',
             '../test/track_test/track(1).geojson',
             '../test/track_test/track(2).geojson',
             ...
             '../test/track_test/track(100).geojson']
    -----------------------------------------------------------------------
    """
    try :
        ls=listdir(dir_name)
    except FileNotFoundError :
        print("\nWarning: \nThe directory was not found.")
        raise FileNotFoundError
    files_list = []
    for f in ls :
        if f.endswith(ext):
            filename = join(dir_name, f)
            files_list.append(filename)
    return np.array(files_list)





if __name__ == "__main__":
    print('\n\t-----------------------\n',
            '\t     Input Output\n\n')
    
# =============================================================================
#     1/ Read a geojson and convert it in dataframe
# =============================================================================
    print('1/ Read a geojson and convert it in dataframe\n')
    trackname = 'track(1)'
    filename = '../../data/track/' + trackname + '.geojson'
    with open(filename) as f:
        geojson = json.load(f)
        
    df = geojson_to_df(geojson, extract_coordinates=True)
    print(df.head())
        
# =============================================================================
#     2/ Write a dataframe in a geojson format
# =============================================================================
    print('\n2/ Write a dataframe in a geojson format')
    print("\t2.1/ Let's add one extra column, stats for example :\n")
    stats = np.random.randint(20, 40, size=len(df))
    df['stats'] = stats

    print(df.head())
    print('\t2.2/ Write the new geojson')
    properties  =  ['location_utc',
                    'bearing', 
                    'speed',
                    'accuracy', 
                    'leq_id',
                    'leq_utc',
                    'leq_mean',
                    'leq_100', 
                    'leq_125', 
                    'leq_160', 
                    'leq_200', 
                    'leq_250', 
                    'leq_315', 
                    'leq_400', 
                    'leq_500', 
                    'leq_630', 
                    'leq_800', 
                    'leq_1000', 
                    'leq_1250', 
                    'leq_1600', 
                    'leq_2000', 
                    'leq_2500', 
                    'leq_3150', 
                    'leq_4000', 
                    'leq_5000', 
                    'leq_6300', 
                    'leq_8000', 
                    'leq_10000', 
                    'leq_12500', 
                    'leq_16000',
                    'marker-color',
                    'stats']
    gj = df_to_geojson(df, properties, geometry_type='type', 
                  lat='latitude', lon='longitude', z='elevation')

    with open('test_write.geojson', 'w') as f:
        json.dump(gj, f)
    
    print("\n\t2.3/ Let's see the new file :\n")
    with open('test_write.geojson') as f:
        geojson_new = json.load(f)
        
    df_new = geojson_to_df(geojson_new, extract_coordinates=True)
    print(df_new.head())
    
    trackname = 'meta(1)'
    filename = '../../data/track/' + trackname + '.properties'
    props = properties_to_df(filename)
    
    
# =============================================================================
#     3/ Read all geojson files in a directory
# =============================================================================
    print("\n3/ Read all geojson files in a directory")
    files = open_files("../../data/track")

    print(files)    
    
    
    
    
    
        