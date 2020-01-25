# -*- coding: utf-8 -*-

# Created on Sun Jan 19 14:31:28 2020

# @author: arthurd

"""
InputOutput Module.

This module save and open files/directory.
"""


import os
import json
import numpy as np


def open_geojson(file_path):
    """
    Open a GeoJson file in a dictionary format.

    Parameters
    ----------
    file_path : String
        Path / Name of the Geojson file. Should contains the extension.

    Returns
    -------
    geojson : Dict
        Dictionary of the GeoJson.
    """
    with open(file_path) as f:
        geojson = json.load(f)
    return geojson


def save_geojson(geojson, out_path):
    """
    Save a GeoJson dictionary.

    Parameters
    ----------
    geojson : Dict
        Dictionary of the GeoJson.
    out_path : String
        Output path / name of the Geojson file. Should contains the extension.

    Returns
    -------
    None.
    """
    with open(out_path, 'w') as f:
        json.dump(geojson, f)


def open_files(dir_path, ext="geojson"):
    """
    Get the path of all files in a directory

    Parameters
    ----------
    dir_path : string
        Name or path to the directory where the files you want to
        open are saved..
    ext : string, optional
        The files extension you want to open. The default is "geojson".

    Raises
    ------
    FileNotFoundError
        If the directory is not found, it raises this issue.

    Returns
    -------
    array like
        A list of the path of all files saved in the directory, with the extension
        geojson by default.
   

    Example
    -------
        >>> dir_name = "path/to/your/directory"
        >>> files = open_files(dir_name, ext="geojson")
        >>> files
            ['../test/track_test/track.geojson',
             '../test/track_test/track(1).geojson',
             '../test/track_test/track(2).geojson',
             ...
             '../test/track_test/track(100).geojson']
    """
    try :
        ls = os.listdir(dir_path)
    except FileNotFoundError :
        print("\nWarning: \nThe directory was not found.")
        raise FileNotFoundError
    files_list = []
    for f in ls :
        if f.endswith(ext):
            filename = os.path.join(dir_path, f)
            files_list.append(filename)
    return np.array(files_list)


def open_properties(file_path, sep='=', comment_char='#'):
    """
    Open properties file.

    Parameters
    ----------
    file_path : String
        Path / Name of the properties file.
    sep : String, optional
        Separator of attributes / elements. 
        The default is '='.
    comment_char : String, optional
        Comment symbol. 
        The default is '#'.

    Returns
    -------
    properties : Dict
        Dictionary of the properties.
    """

    properties = {}
    with open(file_path, "rt") as f:
        for line in f:
            l = line.strip()
            if l and not l.startswith(comment_char):
                key_value = l.split(sep)
                key = key_value[0].strip()
                value = sep.join(key_value[1:]).strip().strip('"') 
                properties[key] = value 
    return properties

