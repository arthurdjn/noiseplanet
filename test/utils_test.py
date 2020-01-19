# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 17:33:44 2020

@author: arthurd
"""


import json
import numpy as np


from noiseplanet import utils

print('1/ Read a geojson and convert it in dataframe\n')
trackname = 'track_1'
filename = 'data/track/' + trackname + '.geojson'
with open(filename) as f:
    geojson = json.load(f)
    
df = utils.geojson_to_df(geojson, extract_coordinates=True)
print(df.head())
    
print('\n2/ Write a dataframe in a geojson format')
print("2.1/ Let's add one extra column, stats for example :\n")
stats = np.random.randint(20, 40, size=len(df))
df['stats'] = stats

print(df.head())
print('2.2/ Write the new geojson')
properties  =  ['location_utc',
                'bearing', 
                'speed',
                'accuracy', 
                'leq_id',
                'leq_utc',
                'leq_mean',
                'leq_100', 
                'marker-color',
                'stats']
gj = utils.df_to_geojson(df, properties, geometry_type='type', 
              lat='latitude', lon='longitude', z='elevation')

with open('data/test_write.geojson', 'w') as f:
    json.dump(gj, f)
print('file wrinten in data/test_write.geojson')

print("\n2.3/ Let's see the new file :\n")
with open('data/test_write.geojson') as f:
    geojson_new = json.load(f)
    
df_new = utils.geojson_to_df(geojson_new, extract_coordinates=True)
print(df_new.head())

trackname = 'meta_1'
filename = 'data/track/' + trackname + '.properties'
props = utils.properties_to_df(filename)

