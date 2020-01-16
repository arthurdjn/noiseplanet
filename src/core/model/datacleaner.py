# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 15:33:13 2019

@author: Utilisateur
"""


"""
UNUSED
"""

import pyjson
import pyproj
import numpy as np

def clean_speed(df, threshold=5, time_acquisition=1):
    """
    """
    
    try:
        speeds = df['speed']
        coordinates = df['coordinates']
    except:
        print(">>> Warning\n",
              "Make sure that the dataframe input have a 'speed' and 'coordinates'",
              "columns.")
        return 0
    
    geod = pyproj.Geod(ellps='WGS84')
    
    for i in range(len(coordinates) - 1):
        point0 = list(coordinates[i])
        point1 = list(coordinates[i+1])
        speed = speeds[i]
        if not np.isnan(speed) and  len(point0) > 2 and len(point1) > 2:
            lon0, lat0 = point0[0], point0[1]
            lon1, lat1 = point1[0], point1[1]
            _, _, dist = geod.inv(lon0, lat0, lon1, lat1)
            diff_norm = abs(dist - speed)/abs(dist + speed)
            print(dist, speed)
    
if __name__ == "__main__":
    print("\n\t-----------------------\n",
            "\t     Correction\n\n")
    
    
# =============================================================================
#     1/ Read the dataframe
# =============================================================================
    file_name = '..\\test\\track_test\\track.geojson'
    df = pyjson.geojson_to_dataframe(file_name)
    print(df.head())

# =============================================================================
#     2/ Correct from errors
# =============================================================================
    clean_speed(df)




