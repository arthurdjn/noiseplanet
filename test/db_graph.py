# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 23:06:01 2020

@author: arthurd
"""


import numpy as np
import noiseplanet.db as db
import noiseplanet.io as io

import matplotlib.pyplot as plt
import pandas as pd
from math import pi



conn = db.connect("../../nc_data/test/database/database.db")
# query = """
#         SELECT LOWER(hmm_meta.device_manufacturer), AVG(hmm_point.accuracy), AVG(hmm_point.proj_accuracy), AVG(hmm_point.proj_length), AVG(hmm_point.path_length),  AVG(hmm_point.unlinked)
#         FROM hmm_meta, hmm_point, nearest_meta
#         WHERE hmm_meta.track_id == hmm_point.track_id AND hmm_meta.track_id == nearest_meta.track_id
#         GROUP BY LOWER(hmm_meta.device_manufacturer)
#         """
# df_hmm = db.select_to_df(conn, query)


# query = """
#         SELECT LOWER(nearest_meta.device_manufacturer), AVG(nearest_point.accuracy), AVG(nearest_point.proj_accuracy), AVG(nearest_point.proj_length), AVG(nearest_point.path_length), AVG(nearest_point.unlinked)
#         FROM hmm_meta, nearest_point, nearest_meta
#         WHERE nearest_meta.track_id == nearest_point.track_id AND hmm_meta.track_id == nearest_meta.track_id
#         GROUP BY LOWER(nearest_meta.device_manufacturer)
#         """
# df_nearest = db.select_to_df(conn, query)
    

query = """
        SELECT LOWER(nearest_meta.device_manufacturer), AVG(nearest_point.accuracy), AVG(nearest_point.proj_accuracy), AVG(nearest_point.proj_length), AVG(nearest_point.path_length), AVG(nearest_point.unlinked)
        FROM hmm_meta, nearest_point, nearest_meta
        WHERE nearest_meta.track_id == nearest_point.track_id AND hmm_meta.track_id == nearest_meta.track_id
        """
huawei_nearest = db.select_to_df(conn, query)

query = """
        SELECT LOWER(hmm_meta.device_manufacturer), AVG(hmm_point.accuracy), AVG(hmm_point.proj_accuracy), AVG(hmm_point.proj_length), AVG(hmm_point.path_length), AVG(hmm_point.unlinked)
        FROM hmm_meta, hmm_point, nearest_meta
        WHERE hmm_meta.track_id == hmm_point.track_id AND hmm_meta.track_id == nearest_meta.track_id
        """
huawei_hmm = db.select_to_df(conn, query)


# huawei_hmm = df_hmm.loc[4]
# samsung_hmm = df_hmm.loc[10]
# sony_hmm = df_hmm.loc[11]
# xiaomi_hmm = df_hmm.loc[15]

# huawei_nearest = df_nearest.loc[4]
# samsung_nearest = df_nearest.loc[10]
# sony_nearest = df_nearest.loc[11]
# xiaomi_nearest = df_nearest.loc[15]




columns  = ['device_manufacturer', 'accuracy', 'proj_accruracy', 'proj_length', 'path_length', 'unlink']
index = ['nearest', 'hmm']
# df_radar_huawei = pd.DataFrame([huawei_nearest.values, huawei_hmm.values], columns=columns)
df_radar_huawei = pd.DataFrame(np.row_stack((huawei_nearest.values, huawei_hmm.values)), columns=columns)


for key in df_radar_huawei.columns[1:]:
    df_radar_huawei[key]= df_radar_huawei[key]/df_radar_huawei[key].sum()

df_radar_huawei['accuracy'] = [0.5, 0.5]
df_radar_huawei['unlink'] = [1, 0]

# Set data
df = df_radar_huawei
 
# ------- PART 1: Create background
# Style
plt.style.use('seaborn-darkgrid') 

# number of variable
categories=list(df)[1:]
N = len(categories)
 
# What will be the angle of each axis in the plot? (we divide the plot / number of variable)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]
 
# Initialise the spider plot
ax = plt.subplot(111, polar=True)
 
# If you want the first axis to be on top:
ax.set_theta_offset(pi / 2)
ax.set_theta_direction(-1)
 
# Draw one axe per variable + add labels labels yet
plt.xticks(angles[:-1], categories)
 
# Draw ylabels
ax.set_rlabel_position(0)
plt.yticks([0, 0.33, 0.66], ["0","0.33","0.66"], color="grey", size=7)
plt.ylim(0, 1)
 
 
# ------- PART 2: Add plots
 
# Plot each individual = each line of the data
 
# Ind1
values=df.loc[0].drop('device_manufacturer').values.flatten().tolist()
values += values[:1]
ax.plot(angles, values, linewidth=1, linestyle='solid', label=df['device_manufacturer'][0] + ' nearest')
ax.fill(angles, values, 'b', alpha=0.1)
 
# Ind2
values=df.loc[1].drop('device_manufacturer').values.flatten().tolist()
values += values[:1]
ax.plot(angles, values, linewidth=1, linestyle='solid', label=df['device_manufacturer'][1] + ' hmm')
ax.fill(angles, values, 'r', alpha=0.1)
 
# Add legend
plt.legend(loc='upper right', bbox_to_anchor=(1.25, 1.07), frameon=False)
plt.savefig('../img/graph_stats.png', dpi=600, transparent=True)


