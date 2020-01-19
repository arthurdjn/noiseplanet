# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 15:09:25 2020

@author: arthurd
"""



import numpy as np
import noiseplanet.db as db
import noiseplanet.io as io


conn = db.connect("database/database_hmm.db")

query = "SELECT DISTINCT hex_id FROM point"
df = db.select_to_df(conn, query)

hex_id = np.array([*df['hex_id']])
Q = hex_id[:,0]
R = hex_id[:,1]
origin = (0, 0)
side_length = 15

io.generate_hexs(Q, R, origin, side_length, out_dirpath="data")



