# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 12:07:09 2019

@author: Utilisateur
"""


# =============================================================================
#     Extraction and decomposition of dictionaries
# =============================================================================

def decompose_dict(d, new_dict):
    """
        *** Extract all elements and elements of sub dictionary of a dictionary ***
                      
        :param d: the main dictionary to extract all its elements
        type d: dict
        :param new_dict: the new dictionary containning all values
        type d: dict
        
        return: None

        -----------------------------------------------------------------------
        Example :
                >>> d = {'a':3, 'b':4, 'c':5, 'd': {'e':6}}
                >>> new_dict = {}
                >>> decompose_dict(d, new_dict)
                >>> new_dict
                    {'a':3, 'b':4, 'c':5, 'e':6}
                    
                Note that the key 'd' and the element 6 are skipped.
        -----------------------------------------------------------------------
    """
    for key in d:
        if type(d[key]) == dict:
            decompose_dict(d[key], new_dict)
        else:
            new_dict[key] = d[key]
        
    
def extract_dict(d, new_dict):
    """
        *** Extract all values of a dictionary and its sub dictionary
            and place them into the single dictionary new_dict ***
                    
        :param d: the main dictionary
        type d: dict
        :param new_dict: auxiliary dictionary to keep track 
                of all elements from d
        type new_dict: dict
        
        return: None
        
        -----------------------------------------------------------------------
        Example :
                >>> d = {'a':3, 'b':4, 'c':5, 'd': {'e':6}}
                >>> new_dict = {'a':None, 'b': None, 'e': None}
                >>> extract_dict(d, new_dict)
                >>> new_dict
                    {'a':3, 'b':4, 'e':6}
        -----------------------------------------------------------------------
    """
    
    for key in d:
        if type(d[key]) == dict:
            extract_dict(d[key], new_dict)
        elif key in new_dict:
            new_dict[key] = d[key]
    
    
def extract_from_labels(d, labels):
    """
        *** Extract all values of a dictionary regarding to their labels ***
                    
        :param d: the main dictionary
        type d: dict
        :param labels: The labels, or key index, that you want from the main dict
        type labels: list
        
        return: A decomposed dictionary containing the values of the main dict
                for each label/key.
        rtype: dict
        
        -----------------------------------------------------------------------
        Example :
                >>> d = {'a':3, 'b':4, 'c':5, 'd': {'e':6}}
                >>> labels = ['a', 'b', 'e']
                >>> extract_from_labels(d, labels)
                    {'a':3, 'b':4, 'e':6}
        -----------------------------------------------------------------------
    """

    new_dict = {}
    for label in labels:
        new_dict[label] = None
                
    extract_dict(d, new_dict)
    
    return new_dict
        




if __name__ == "__main__":
    print("\n\t-----------------------\n",
            "\t       Utils\n\n")
    
# =============================================================================
#     1/ Decomposition
# =============================================================================
    print("1/ Decomposition of a dict")
    d = {"a": 20, "b": 24, "c":10, "d":{"e": 10, "f":3.14, "g":{"h":10148}}, "i":0, "j":{"k":999}}
    new_dict = {}
    decompose_dict(d, new_dict)
    print("Main dict :", d)
    print("Decomposition :", new_dict)
    
    
# =============================================================================
#     2/ Extraction
# =============================================================================
    print("2/ Extraction of a dict from its keys")
    labels = ['a', 'f', 'g', 'h', 'k']
    ext_dict = extract_from_labels(d, labels)
    print("Extracting the labels :", labels)
    print("Extracted dict :", ext_dict)
    
    
    
    
    
    
    
    
    