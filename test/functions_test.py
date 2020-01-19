# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 21:05:06 2020

@author: arthurd
"""

import json
from pandas.io.json import json_normalize
import pandas as pd
import numpy as np

from noiseplanet import utils

# data = json.loads(elevations)

file = "data/track/track_1.geojson"
with open(file) as f:
    geojson = json.load(f)

df = json_normalize(geojson["features"])




df2 = pd.read_json(file)


df3 = utils.geojson_to_df(geojson)

df.to_json("data/test.geojson")

df4 = json_normalize(geojson["features"])
df5 = utils.geojson_to_df(geojson)


np.array([*df['geometry.coordinates']])