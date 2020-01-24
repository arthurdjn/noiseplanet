# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 15:33:13 2019

@author: arthurd
"""

            
def clean_data(df):
    """
    Clean a DataFrame track. This function is under development.

    Parameters
    ----------
    df : pandas DataFrame
        DataFrame to clean. Currently, only missing points are deleted.

    Returns
    -------
    df : pandas DataFrame
        Cleaned DataFrame.

    """
    # Fill None values by interpolation
    # try:
    #     df = df.interpolate(method='quadratic', axis=1, subset=['speed'])
    # except ValueError as e:
    #     print("{0} The interpolation failed for {1}".format(e))
    # Delete rows where there are no positions
    df = df.dropna(how='any', axis=0, subset=['type']) 
    return df
    




