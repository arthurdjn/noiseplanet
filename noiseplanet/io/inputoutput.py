# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 14:31:28 2020

@author: arthurd
"""

import os
import json
import noiseplanet.utils as utils


def generate_hex(Q, R, origin, side_length, out_dirpath="."):
    
    # Project the coordinates in the webmercator system
    proj_init="epsg:4326"
    proj_out="epsg:3857"
                
    Xcenter, Ycenter = utils.hexs_to_cartesians(Q, R, side_length=side_length, origin=origin, 
                        proj_init=proj_out, proj_out=proj_init)              
    hexagons = utils.hexagons_coordinates(Xcenter, Ycenter, side_length=side_length, 
                                    proj_init=proj_init, proj_out=proj_out)
    
    # Test if the out directory exists
    directory = out_dirpath + '/hexagons'
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    for i, hexagon in enumerate(hexagons): 
        id = str(int(Q[i])) + 'x' + str(int(R[i]))
        properties = {'id': id}
        gj = utils.poly_to_geojson(hexagons, properties)

        # write the geojson
        outname = directory + '/' + 'hex_' + id + '.geojson'
        with open(outname, 'w') as f:
            json.dump(gj, f)
    

