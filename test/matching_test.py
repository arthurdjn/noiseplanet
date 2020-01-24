# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 23:19:54 2020

@author: arthurd
"""
import numpy as np
import osmnx as ox
import time

from noiseplanet import matching

def test_match():
    print('\nTest match(graph, track, method)')
    center_point = (45.75793143,  4.83549635)
    graph = ox.graph_from_point(center_point, distance=100)
    track = np.array( [[45.75793143,  4.83549635],
                       [45.75793143,  4.83549635],
                       [45.75791593,  4.83548718],
                       [45.75788795,  4.83546475],
                       [45.75788795,  4.83546475],
                       [45.75786658,  4.83547026],
                       [45.75783632,  4.83546862],
                       [45.75783632,  4.83546862],
                       [45.75782964,  4.83547046],
                       [45.75780487,  4.83546808],
                       [45.7577991 ,  4.83545974],
                       [45.7577991 ,  4.83545974],
                       [45.75778494,  4.83544537],
                       [45.75778018,  4.83542394],
                       [45.75778018,  4.83542394],
                       [45.75777708,  4.83542095],
                       [45.75778355,  4.83537921],
                       [45.75778355,  4.83537921],
                       [45.75779486,  4.8353652 ],
                       [45.75778985,  4.83535578],
                       [45.75779875,  4.83534073],
                       [45.75779875,  4.83534073],
                       [45.75778759,  4.83534048],
                       [45.75777132,  4.83530956],
                       [45.75777132,  4.83530956],
                       [45.75777826,  4.83529123],
                       [45.75772724,  4.83526193],
                       [45.75772724,  4.83526193],
                       [45.75770642,  4.8352539 ],
                       [45.75765273,  4.83523469],
                       [45.75765273,  4.83523469],
                       [45.75763036,  4.8352032 ],
                       [45.75760354,  4.83521685],
                       [45.75760031,  4.83517866],
                       [45.75760031,  4.83517866],
                       [45.75760174,  4.83514537],
                       [45.75755343,  4.83511274],
                       [45.75757394,  4.8350941 ],
                       [45.75757394,  4.8350941 ],
                       [45.75762054,  4.83503878],
                       [45.75769855,  4.83501164],
                       [45.75769951,  4.83498337],
                       [45.75772904,  4.83492365]])
    method = 'nearest'
    start = time.time()
    track_corr, route_corr, edgeid, stats = matching.match(graph, track, method)
    print('Map Matching nearest in {0}s'.format(round(time.time() - start, 5)))
    # print('track_corr {0}\nroute_corr {1}\nedgeid {2}\nstats {3}'.format(track_corr, route_corr, edgeid, stats))

    method = 'hmm'
    start = time.time()
    track_corr, route_corr, edgeid, stats = matching.match(graph, track, method)
    print('Map Matching hmm in {0}s'.format(round(time.time() - start, 5))) 
    # print('track_corr {0}\nroute_corr {1}\nedgeid {2}\nstats {3}'.format(track_corr, route_corr, edgeid, stats))

def test_match_from_geojson(dirname, out_dirname=".", method="nearest", log=True):
    matching.match_from_geojsons(dirname, out_dirname=out_dirname, method=method, log=log)


def test_match_from_geojsons(dirname, out_dirname=".", method="nearest", log=True):
    print('\nTest match_from_geojsons(dirname, out_dirname=".", method="nearest", log=True)')
    matching.match_from_geojsons(dirname, out_dirname=out_dirname, method=method, log=log)



if __name__ == "__main__":
    
    # Test the match function
    test_match()
    
    # Test the match_from_geojson function
    dirname = "../../nc_data/test/data/track"
    out_dirname = '.'
    test_match_from_geojsons(dirname, out_dirname=out_dirname, method="nearest", log=True)
    test_match_from_geojsons(dirname, out_dirname=out_dirname, method="hmm", log=True)


