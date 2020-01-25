# -*- coding: utf-8 -*-

# Created on Sun Jan 19 14:31:28 2020

# @author: arthurd

"""
InputOutput Module.

This module save and open files/directory.
"""


import requests
import os
import json
import numpy as np
import zipfile



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


def unzip_file(*file, out_dir):
    """
    Unzip files in a directory.

    Parameters
    ----------
    out_dir : String
        Path to the output location.
    *file : String
        Path of files to unzip.

    Returns
    -------
    None.
    """
    
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    filelist = ['track.geojson', 'meta.properties']
    
    for zip_file in file:  # loop through items in dir
        name = zip_file.split(os.sep)[-1].split('.')[0].split('_')[1]
        try:
            with zipfile.ZipFile(zip_file) as zf:  # open the zip file
                for target_file in filelist:  # loop through the list of files to extract
                    if target_file in zf.namelist():  # check if the file exists in the archive
                        # generate the desired output name:
                        target_name = target_file.split('.')[0] + "_" + name + "." + target_file.split('.')[1]
                        target_path = os.path.join(out_dir, target_name)  # output path
                        with open(target_path, "wb") as f:  # open the output path for writing
                            f.write(zf.read(target_file))  # save the contents of the file in it
        except zipfile.BadZipFile:
            print('Zip File Error : {0} has not been unziped.'.format(zip_file))
    


def unzip_dir(in_dir, out_dir):
    """
    Unzip files in a directory.

    Parameters
    ----------
    out_dir : String
        Path to the output location.
    *file : String
        Path of files to unzip.

    Returns
    -------
    None.
    """
    
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    files = open_files(in_dir, ext='zip')
    filelist = ['track.geojson', 'meta.properties']
    
    for file in files:  # loop through items in dir
        name = file.split(os.sep)[-1].split('.')[0].split('_')[1]
        try:
            with zipfile.ZipFile(file) as zf:  # open the zip file
                for target_file in filelist:  # loop through the list of files to extract
                    if target_file in zf.namelist():  # check if the file exists in the archive
                        # generate the desired output name:
                        target_name = target_file.split('.')[0] + "_" + name + "." + target_file.split('.')[1]
                        target_path = os.path.join(out_dir, target_name)  # output path
                        with open(target_path, "wb") as f:  # open the output path for writing
                            f.write(zf.read(target_file))  # save the contents of the file in it
        except zipfile.BadZipFile:
            print('Zip File Error : {0} has not been unziped.'.format(file))


def extract_track(query_csv, out_dir='data'):
    """
    Extract GeoJson tracks from a CSV.
    
    See https://dashboard.noise-planet.org/public/question/52ee2bde-2d28-4377-bcbb-061d7cbfa343
    
    Parameters
    ----------
    query_csv : String
        CSV file of the tracks.

    Returns
    -------
    None.
    """
    
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        
    lines = open(query_csv, "r").readlines()
    for line in lines[1:]:
        url = line.split(",")[1][:-1]
        filename = out_dir + os.sep + url[url.rfind("/") + 1:]
        open(filename,"wb").write(requests.get(url).content)








