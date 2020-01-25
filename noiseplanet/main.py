# -*- coding: utf-8 -*-

# Created on Thu Dec 5 16:49:20 2019

# @author: arthurd

"""
Main module.

Download GeoJson tracks from NoisePlanet server.
Match GeoJson tracks on the OSM network and Save them in a DataBase.
"""

import sys

from noiseplanet import db, io, matcher


if __name__ == "__main__":
    
    # extract the track from the csv
    io.extract_track(*sys.argv[1:])
    # Unzip the track
    io.unzip_dir(*sys.argv[1:])
    # Matching to OSM
    matcher.match_from_geojsons(*sys.argv[1:])
    # Save in a DataBase
    db.track_to_db(*sys.argv[1:])


