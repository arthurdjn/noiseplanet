# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 17:33:44 2020

@author: arthurd
"""


import json
import numpy as np
import pandas as pd

from noiseplanet import utils


def test_df_to_geojson():
    geojson = {
              "type": "FeatureCollection",
              "features": [
                
                {
                  "type": "Feature",
                  "geometry": {
                    "type": "Point",
                    "coordinates": [
                      4.914903366028505,
                      45.7852725976994,
                      308.5739246938037
                    ]
                  },
                  "properties": {
                    "leq_mean": 40.07053,
                    "marker-color": "#B8D6D1",
                    "accuracy": 96,
                    "location_utc": 1507071853948,
                    "leq_utc": 1507071853144,
                    "leq_id": 4,
                    "bearing": 215.15285,
                    "speed": 0.22279137,
                    "leq_100": 27.960316,
                    "leq_125": 27.812155,
                    "leq_160": 24.650198,
                    "leq_200": 25.09629,
                    "leq_250": 21.228565,
                    "leq_315": 21.56663,
                    "leq_400": 26.527437,
                    "leq_500": 29.834623,
                    "leq_630": 27.973343,
                    "leq_800": 28.65164,
                    "leq_1000": 29.625328,
                    "leq_1250": 27.457666,
                    "leq_1600": 24.705,
                    "leq_2000": 26.625557,
                    "leq_2500": 30.395763,
                    "leq_3150": 25.542177,
                    "leq_4000": 25.08086,
                    "leq_5000": 24.600506,
                    "leq_6300": 26.505657,
                    "leq_8000": 25.828566,
                    "leq_10000": 20.198694,
                    "leq_12500": 15.001841,
                    "leq_16000": 10.275352
                  }
                },
                {
                  "type": "Feature",
                  "geometry": {
                    "type": "Point",
                    "coordinates": [
                      4.9148443050763015,
                      45.78526148961034,
                      299.0012617091176
                    ]
                  },
                  "properties": {
                    "leq_mean": 41.105766,
                    "marker-color": "#B8D6D1",
                    "accuracy": 128,
                    "location_utc": 1507071854948,
                    "leq_utc": 1507071854216,
                    "leq_id": 5,
                    "bearing": 239.0649,
                    "speed": 0.14811344,
                    "leq_100": 9.679459,
                    "leq_125": 13.061665,
                    "leq_160": 14.144692,
                    "leq_200": 20.06505,
                    "leq_250": 18.503063,
                    "leq_315": 22.471695,
                    "leq_400": 27.914675,
                    "leq_500": 28.075678,
                    "leq_630": 29.18336,
                    "leq_800": 30.089338,
                    "leq_1000": 32.148552,
                    "leq_1250": 30.177233,
                    "leq_1600": 27.067488,
                    "leq_2000": 29.18854,
                    "leq_2500": 32.27753,
                    "leq_3150": 28.223087,
                    "leq_4000": 29.28262,
                    "leq_5000": 27.599894,
                    "leq_6300": 28.638742,
                    "leq_8000": 28.081095,
                    "leq_10000": 21.839924,
                    "leq_12500": 16.590805,
                    "leq_16000": 11.953764
                  }
                },
                {
                  "type": "Feature",
                  "geometry": {
                    "type": "Point",
                    "coordinates": [
                      4.914792221261604,
                      45.78528816803448,
                      292.51776728496185
                    ]
                  },
                  "properties": {
                    "leq_mean": 41.523438,
                    "marker-color": "#B8D6D1",
                    "accuracy": 128,
                    "location_utc": 1507071855948,
                    "leq_utc": 1507071855340,
                    "leq_id": 6,
                    "bearing": 300.32434,
                    "speed": 0.13124688,
                    "leq_100": 8.998961,
                    "leq_125": 12.450066,
                    "leq_160": 13.862192,
                    "leq_200": 20.57264,
                    "leq_250": 17.827635,
                    "leq_315": 22.80262,
                    "leq_400": 27.544498,
                    "leq_500": 27.598087,
                    "leq_630": 29.47041,
                    "leq_800": 30.46653,
                    "leq_1000": 32.52231,
                    "leq_1250": 30.676237,
                    "leq_1600": 27.500904,
                    "leq_2000": 30.069105,
                    "leq_2500": 32.984486,
                    "leq_3150": 28.696085,
                    "leq_4000": 29.280056,
                    "leq_5000": 28.045334,
                    "leq_6300": 29.626554,
                    "leq_8000": 28.745527,
                    "leq_10000": 22.237398,
                    "leq_12500": 16.701935,
                    "leq_16000": 11.957227
                  }
                }
              ]
            }
    df = utils.geojson_to_df(geojson, normalize_header=True)
    print(df)
    
def test_df_to_geojson():
    geojson = {
          "type": "FeatureCollection",
          "features": [
            
            {
              "type": "Feature",
              "geometry": {
                "type": "Point",
                "coordinates": [
                  4.914903366028505,
                  45.7852725976994,
                  308.5739246938037
                ]
              },
              "properties": {
                "leq_mean": 40.07053,
                "marker-color": "#B8D6D1",
                "accuracy": 96,
                "location_utc": 1507071853948,
                "leq_utc": 1507071853144,
                "leq_id": 4,
                "bearing": 215.15285,
                "speed": 0.22279137,
                "leq_100": 27.960316,
                "leq_125": 27.812155,
                "leq_160": 24.650198,
                "leq_200": 25.09629,
                "leq_250": 21.228565,
                "leq_315": 21.56663,
                "leq_400": 26.527437,
                "leq_500": 29.834623,
                "leq_630": 27.973343,
                "leq_800": 28.65164,
                "leq_1000": 29.625328,
                "leq_1250": 27.457666,
                "leq_1600": 24.705,
                "leq_2000": 26.625557,
                "leq_2500": 30.395763,
                "leq_3150": 25.542177,
                "leq_4000": 25.08086,
                "leq_5000": 24.600506,
                "leq_6300": 26.505657,
                "leq_8000": 25.828566,
                "leq_10000": 20.198694,
                "leq_12500": 15.001841,
                "leq_16000": 10.275352
              }
            },
            {
              "type": "Feature",
              "geometry": {
                "type": "Point",
                "coordinates": [
                  4.9148443050763015,
                  45.78526148961034,
                  299.0012617091176
                ]
              },
              "properties": {
                "leq_mean": 41.105766,
                "marker-color": "#B8D6D1",
                "accuracy": 128,
                "location_utc": 1507071854948,
                "leq_utc": 1507071854216,
                "leq_id": 5,
                "bearing": 239.0649,
                "speed": 0.14811344,
                "leq_100": 9.679459,
                "leq_125": 13.061665,
                "leq_160": 14.144692,
                "leq_200": 20.06505,
                "leq_250": 18.503063,
                "leq_315": 22.471695,
                "leq_400": 27.914675,
                "leq_500": 28.075678,
                "leq_630": 29.18336,
                "leq_800": 30.089338,
                "leq_1000": 32.148552,
                "leq_1250": 30.177233,
                "leq_1600": 27.067488,
                "leq_2000": 29.18854,
                "leq_2500": 32.27753,
                "leq_3150": 28.223087,
                "leq_4000": 29.28262,
                "leq_5000": 27.599894,
                "leq_6300": 28.638742,
                "leq_8000": 28.081095,
                "leq_10000": 21.839924,
                "leq_12500": 16.590805,
                "leq_16000": 11.953764
              }
            },
            {
              "type": "Feature",
              "geometry": {
                "type": "Point",
                "coordinates": [
                  4.914792221261604,
                  45.78528816803448,
                  292.51776728496185
                ]
              },
              "properties": {
                "leq_mean": 41.523438,
                "marker-color": "#B8D6D1",
                "accuracy": 128,
                "location_utc": 1507071855948,
                "leq_utc": 1507071855340,
                "leq_id": 6,
                "bearing": 300.32434,
                "speed": 0.13124688,
                "leq_100": 8.998961,
                "leq_125": 12.450066,
                "leq_160": 13.862192,
                "leq_200": 20.57264,
                "leq_250": 17.827635,
                "leq_315": 22.80262,
                "leq_400": 27.544498,
                "leq_500": 27.598087,
                "leq_630": 29.47041,
                "leq_800": 30.46653,
                "leq_1000": 32.52231,
                "leq_1250": 30.676237,
                "leq_1600": 27.500904,
                "leq_2000": 30.069105,
                "leq_2500": 32.984486,
                "leq_3150": 28.696085,
                "leq_4000": 29.280056,
                "leq_5000": 28.045334,
                "leq_6300": 29.626554,
                "leq_8000": 28.745527,
                "leq_10000": 22.237398,
                "leq_12500": 16.701935,
                "leq_16000": 11.957227
              }
            }
          ]
        }
    df = pd.DataFrame(geojson)
    df = utils.df_geojson(df)
    print(df)

    
if __name__ == "__main__":
    
    # DataFrame <-> GeoJSON
    test_df_to_geojson()
    
    
# print('1/ Read a geojson and convert it in dataframe\n')
# trackname = 'track_1'
# filename = 'data/track/' + trackname + '.geojson'
# with open(filename) as f:
#     geojson = json.load(f)
    
# df = utils.geojson_to_df(geojson, extract_coordinates=True)
# print(df.head())
    
# print('\n2/ Write a dataframe in a geojson format')
# print("2.1/ Let's add one extra column, stats for example :\n")
# stats = np.random.randint(20, 40, size=len(df))
# df['stats'] = stats

# print(df.head())
# print('2.2/ Write the new geojson')
# properties  =  ['location_utc',
#                 'bearing', 
#                 'speed',
#                 'accuracy', 
#                 'leq_id',
#                 'leq_utc',
#                 'leq_mean',
#                 'leq_100', 
#                 'marker-color',
#                 'stats']
# gj = utils.df_to_geojson(df, properties, geometry_type='type', 
#               lat='latitude', lon='longitude', z='elevation')

# with open('data/test_write.geojson', 'w') as f:
#     json.dump(gj, f)
# print('file wrinten in data/test_write.geojson')

# print("\n2.3/ Let's see the new file :\n")
# with open('data/test_write.geojson') as f:
#     geojson_new = json.load(f)
    
# df_new = utils.geojson_to_df(geojson_new, extract_coordinates=True)
# print(df_new.head())

# trackname = 'meta_1'
# filename = 'data/track/' + trackname + '.properties'
# props = utils.properties_to_df(filename)

