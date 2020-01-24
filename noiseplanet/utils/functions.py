# -*- coding: utf-8 -*-
'''
Created on Wed Dec 18 16:34:04 2019

@author: Utilisateur
'''

import pandas as pd



# =============================================================================
# DEPRECATED
# =============================================================================
# def geojson_to_df(geojson, extract_coordinates=True):   
#     data = {'type': []}
#     if extract_coordinates:
#         data['longitude'] = []
#         data['latitude'] = []
#         data['elevation'] = []
#     else:
#         data['coordinates'] = []
#     properties = []
#     count_prop = 0
#     for feature in geojson['features']:
#         if feature['geometry'] is not None:        
#             # geometry
#             data['type'].append(feature['geometry']['type'])
#             if extract_coordinates:
#                 data['longitude'].append(feature['geometry']['coordinates'][0])
#                 data['latitude'].append(feature['geometry']['coordinates'][1])
#                 data['elevation'].append(feature['geometry']['coordinates'][2])
#             else:
#                 data['coordinates'].append(feature['geometry']['coordinates'])
#         else:
#             # geometry
#             data['type'].append(None)
#             if extract_coordinates:
#                 data['longitude'].append(np.nan)
#                 data['latitude'].append(np.nan)
#                 data['elevation'].append(np.nan)
#             else:
#                 data['coordinates'].append(np.nan)
#
#         # properties
#         for prop in feature['properties']:
#             if prop in properties:
#                 data[prop].append(feature['properties'][prop])
#             else:
#                 data[prop] = [np.nan] * count_prop + [feature['properties'][prop]]
#                 properties.append(prop)
#         for key in np.setdiff1d(properties, feature['properties'], assume_unique=True):
#             if key not in feature['properties']:
#                 data[key].append(np.nan)
#          
#         count_prop += 1
#     df = pd.DataFrame(data)
#     return df
# =============================================================================


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
        Example :
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
    Returns
    -------
    df : pandas DataFrame
        Converted GeoJson in a DataFrame format.
    """
    
    df = pd.io.json.json_normalize(geojson["features"])
    if normalize_header:
        del df[df.columns[0]]
        columns = [key.lower().split('.')[-1] for key in df.columns.values]
        df.columns = columns
        
    return df    


# =============================================================================
# DEPRECATED
# =============================================================================
# def df_to_geojson(df, properties, geometry_type='type', 
#                   lat='latitude', lon='longitude', z='elevation'):
#     gj = {'type':'FeatureCollection', 'features': []}
#     for _, row in df.iterrows():
#         feature = {'type':'Feature',
#                    'properties':{},
#                    'geometry':{'type': row[geometry_type],
#                                'coordinates':[]}}
#         feature['geometry']['coordinates'] = [row[lon], row[lat], row[z]]
#         for prop in properties:
#             feature['properties'][prop] = row[prop]
#         gj['features'].append(feature)
#     return gj
# =============================================================================


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

    
        