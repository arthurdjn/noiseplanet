# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 23:19:54 2020

@author: arthurd
"""

import noiseplanet as npt



if __name__ == "__main__":
    print("1/ Reading the files")
    files = npt.io.open_files("data/track", ext="geojson")
    print(files)
    
    files_properties = npt.io.open_files("data/track", ext="properties")
    print(files_properties)
    
    print("2/ Map Matching")
    npt.main(files, files_properties=files_properties, out_dirname='data', method='hmm', db_file='database/database_hmm.db', log=True)
    




