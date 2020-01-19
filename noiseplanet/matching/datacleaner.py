# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 15:33:13 2019

@author: Utilisateur
"""

            
def clean_data(df):
    # Fill None values by interpolation
    try:
        df = df.interpolate(method='quadratic', axis=0)
    except ValueError as e:
        print("{0} The interpolation failed for {1}".format(e))
    # Delete rows where there are no positions
    df = df[df['type'].notnull()]
    return df
    




