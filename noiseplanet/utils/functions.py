# -*- coding: utf-8 -*-

# Created on Wed Dec 18 16:34:04 2019

# @author: Utilisateur

"""
Functions Module.

This module convert geojson to pandas DataFrame.
"""


import pandas as pd


def geojson_to_df(geojson, normalize_header=False):
    """
    Convert a GeoJson dictionary to a pandas DataFrame.

    Parameters
    ----------
    geojson : Dict
        GeoJson dictionary.
    normalize_header : Boolean, optional
        If True, normalize the header by spliting the path name and only keeping 
        the attribute name. The default is False.
        
    Returns
    -------
    df : pandas DataFrame
        Converted GeoJson in a DataFrame format.
        
    Example
    -------
        >>> from noiseplanet.utils.functions import geojson_to_df
        >>> df = geojson_to_df(geojson, normalize_header=False)
        >>> df.head
            type      geometry.type   geometry.coordinates    properties.id ...
            Feature   Point           [4.52, 45.58, 201.15]   0
            ...
            
        >>> df = geojson_to_df(geojson, normalize_header=True)
        >>> df.head
            type            coordinates             id ...
            Point           [4.52, 45.58, 201.15]   0
            ...
    """
    
    df = pd.io.json.json_normalize(geojson["features"])
    if normalize_header:
        del df[df.columns[0]]
        columns = [key.lower().split('.')[-1] for key in df.columns.values]
        df.columns = columns
        
    return df    


def df_to_geojson(df, geometry, coordinates, properties):
    """
    Convert a pandas DataFrame to a GeoJson dictionary.

    Parameters
    ----------
    df : pandas DataFrame
        DataFrame containing the geojson's informations.
    geometry : String
        The type of the geometry (Point, Polygon, etc.).
    coordinates : String
        The DataFrame column's name of the coordinates.
    properties : list of String eelements.
        The DataFrame column's names of the properties attributes.

    Returns
    -------
    geojson : Dict
        GeoJson dictionary with the geometry, coordinates, and properties elements.
    """
    
    geojson = {'type': 'FeatureCollection', 'features': []}
    for _, row in df.iterrows():
        feature = {'type':'Feature',
                    'properties':{},
                    'geometry': {'type': geometry,
                                'coordinates': coordinates}}

        for prop in properties:
            normalize_prop = prop.lower().split('.')[-1]
            feature['properties'][normalize_prop] = row[prop]
        geojson['features'].append(feature)
    
    return geojson

    
        