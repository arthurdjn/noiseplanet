# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 15:09:25 2020

@author: arthurd
"""



import numpy as np
import noiseplanet as npt
import noiseplanet.io.inputoutput as io


conn = npt.db.connect("../database/database_hmm2.db")

query = "SELECT hex_id FROM point"
df = npt.db.select_to_df(conn, query)

hex_id = np.array([*df['hex_id']])
Q = hex_id[:,0]
R = hex_id[:,1]
origin = (0, 0)
side_length = 15



io.generate_hex(Q, R, origin, side_length, out_dirpath="data")


