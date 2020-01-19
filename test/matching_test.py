# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 23:19:54 2020

@author: arthurd
"""

import noiseplanet as npt




# =============================================================================
#     1/ Read all the Geojson files
# =============================================================================
print("1/ Reading the files")
files = npt.utils.open_files("data/track", ext="geojson")
print(files)

files_properties = npt.utils.open_files("data/track", ext="properties")
print(files_properties)


# =============================================================================
#     2/ Map matching
# =============================================================================
print("2/ Map Matching")
npt.main(files, files_properties=None, out_dirname='data', method='hmm', db_file='database/database_hmm.db', log=True)





