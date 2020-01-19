# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 23:06:01 2020

@author: arthurd
"""


import numpy as np
import noiseplanet.db as db
import noiseplanet.io as io


conn = db.connect("../../nc_data/test/database/database_hmm.db")
query = "SELECT DISTINCT hex_id FROM point"
df = db.select_to_df(conn, query)


