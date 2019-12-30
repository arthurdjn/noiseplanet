# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 15:32:28 2019

@author: Utilisateur
"""

import pandas as pd
import numpy as np
 
    
def global_stats(dfstats):
    stats = []    
    
    for key in dfstats:
        astats = []
        mean = np.mean(dfstats[key].values)
        s = np.sum(dfstats[key].values)
        var = np.var(dfstats[key].values)
        std = np.std(dfstats[key].values)
        mini = np.min(dfstats[key].values)
        maxi = np.max(dfstats[key].values)
        # adding the stats for key
        astats.append(s)
        astats.append(mini)
        astats.append(maxi)
        astats.append(mean)
        astats.append(var)
        astats.append(std)
        # updating the global matrix of stats
        stats.append(astats)
    
    dfglobalstats = pd.DataFrame(stats, columns=['sum', 'min', 'max', 'mean', 'var', 'std'],
                                        index=[key for key in dfstats])
    
    return dfglobalstats


if __name__ == "__main__":
    print("\n\t-----------------------\n",
            "\t       Statistics      \n\n")
        
# =============================================================================
#     1/ Print the stats
# =============================================================================
    print("1/ Print the stats")
    array = np.random.randint(20, size=50)
    statistics = {"random": array}
    stats = pd.DataFrame(statistics)
    dfstats = global_stats(stats)
    print(dfstats.head())

    
# =============================================================================
#     2/ Plot graph
# =============================================================================
    
    