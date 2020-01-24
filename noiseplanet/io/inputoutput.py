# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 14:31:28 2020

@author: arthurd
"""

import os
import json
import numpy as np

import noiseplanet.utils as utils


def open_geojson(file_name):
    with open(file_name) as f:
        geojson = json.load(f)
    return geojson


def save_geojson(geojson, file_name):
    with open(file_name, 'w') as f:
        json.dump(geojson, f)


def open_files(dir_path, ext="geojson"):
    """
    Get the path of all files in a directory

    Parameters
    ----------
    dir_path : string
        Name or path to the directory where the files you want to
        open are saved..
    ext : string, optional
        The files extension you want to open. The default is "geojson".

    Raises
    ------
    FileNotFoundError
        If the directory is not found, it raises this issue.

    Returns
    -------
    array like
        A list of the path of all files saved in the directory, with the extension
        geojson by default.
   
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
        ls = os.listdir(dir_path)
    except FileNotFoundError :
        print("\nWarning: \nThe directory was not found.")
        raise FileNotFoundError
    files_list = []
    for f in ls :
        if f.endswith(ext):
            filename = os.path.join(dir_path, f)
            files_list.append(filename)
    return np.array(files_list)




def open_properties(filepath, sep='=', comment_char='#'):
    """
    Read the file passed as parameter as a properties file.
    """
    properties = {}
    with open(filepath, "rt") as f:
        for line in f:
            l = line.strip()
            if l and not l.startswith(comment_char):
                key_value = l.split(sep)
                key = key_value[0].strip()
                value = sep.join(key_value[1:]).strip().strip('"') 
                properties[key] = value 
    return properties
    # return pd.DataFrame(data=props, index=[0])



















def generate_hex(Q, R, origin, side_length, df_properties=None, out_dirpath="."):
    
    # Project the coordinates in the webmercator system
    proj_init="epsg:4326"
    proj_out="epsg:3857"
                
    Xcenter, Ycenter = utils.hexs_to_cartesians(Q, R, side_length=side_length, origin=origin, 
                        proj_init=proj_out, proj_out=proj_init)              
    hexagons = utils.hexagons_coordinates(Xcenter, Ycenter, side_length=side_length, 
                                    proj_init=proj_init, proj_out=proj_out)
    
    # Test if the out directory exists
    directory = out_dirpath + '/hexagons'
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    for i, hexagon in enumerate(hexagons): 
        # Create a unique id for each hexagons
        id = str(int(Q[i])) + 'x' + str(int(R[i]))
        
        # Update properties
        properties = {'id': id}
        for key in df_properties:
            properties[key] = df_properties[key][i]
            
        # Convert the hexagon in a geojson format
        gj = utils.poly_to_geojson(hexagon, properties)
        # Write the geojson
        outname = directory + '/' + 'hex_' + id + '.geojson'
        with open(outname, 'w') as f:
            json.dump(gj, f)
    





# Create Geojson
def generate_hexs(Q, R, origin, side_length, df_props=None, out_dirpath="."):
    
    # Project the coordinates in the webmercator system
    proj_init="epsg:4326"
    proj_out="epsg:3857"
                
    Xcenter, Ycenter = utils.hexs_to_cartesians(Q, R, side_length=side_length, origin=origin, 
                        proj_init=proj_out, proj_out=proj_init)              
    hexagons = utils.hexagons_coordinates(Xcenter, Ycenter, side_length=side_length, 
                                    proj_init=proj_init, proj_out=proj_out)
    
    # Test if the out directory exists
    directory = out_dirpath + '/hexagons'
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    feature = []
    
    for i, hexagon in enumerate(hexagons):  
        # Create a unique id for each hexagons
        id = str(int(Q[i])) + 'x' + str(int(R[i]))
        
        # Update properties
        properties = {'id': id}
        
        hex_feature = {
            "type":"Feature",
            "geometry":{
                    "type":"Polygon",
                    "properties": properties,
                    "coordinates": [hexagon]
                    }
            }
        feature.append(hex_feature)

    gj = {"type": "FeatureCollection",
            "features": feature
    }
    # Write the geojson
    outname = directory + '/' + 'hex_' + '.geojson'
    with open(outname, 'w') as f:
        json.dump(gj, f)
