# -*- coding: utf-8 -*-
"""Spectral Rec.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fcYfQZliNlVZAuyF-7OF40ywMBs_Hspf
"""

from google.colab import drive
drive.mount('/content/gdrive')

from __future__ import division

import numpy as np 
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd 

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sn
import numpy as np
import pickle

#spectral clustering recommendation

model = pickle.load(open('/content/gdrive/My Drive/8th_Sem_Project PES_293_323_355/spactralClusteringDict.pkl','rb'))
user_per_cluster_dict = pickle.load(open('/content/gdrive/My Drive/8th_Sem_Project PES_293_323_355/spactralClusteringDictWithCount.pkl','rb'))
embeddings = pickle.load(open('/content/gdrive/My Drive/8th_Sem_Project PES_293_323_355/spectralDict.pkl', 'rb'))

f = pickle.load(open('/content/gdrive/My Drive/8th_Sem_Project PES_293_323_355/user_high_low_info.pickle','rb'))
top_users = pickle.load(open('/content/gdrive/My Drive/8th_Sem_Project PES_293_323_355/top_users.pickle','rb'))
top_users = list(top_users.keys())
count = 0
accuracy = 0
error = 0

final_df = pd.DataFrame(columns = ["User", "Recommended set length", "Actual recommended set length", "Common recommendations", "Common recommendation length" ,"Coverage", "Overall Coverage", "Hit Rate"])
for user in top_users:
  if(len(f[user]['high']) > 20):
    count += 1
    sample_user = user
    embedding_sample_user = embeddings[sample_user]
    cluster_sample_user = model[sample_user]
    cluster_entries = user_per_cluster_dict[cluster_sample_user]

    cluster_entries_embeddings = []
    for i in range(0, len(cluster_entries)):
      cluster_entries_embeddings.append(embeddings[cluster_entries[i]])

    distance_from_sample_user = {}
    for cluster_user in cluster_entries_embeddings:
      dist = np.linalg.norm(np.array(embeddings[sample_user])-np.array(cluster_user))
      distance_from_sample_user[list(embeddings.keys())[list(embeddings.values()).index(cluster_user)]] = dist

    distance_from_sample_user_sorted = [(k, distance_from_sample_user[k]) for k in sorted(distance_from_sample_user, key=distance_from_sample_user.get, reverse=False)]
    distance_from_sample_user_sorted = distance_from_sample_user_sorted[1:11]

    recommended_set = set()
    
    for i in range (0,10):
      influential_user = distance_from_sample_user_sorted[i][0]
      recommended_set |= f[influential_user]['high']
      row = {}
    try:
      row["User"] = sample_user
    except:
      continue
    try:
      row["Recommended set length"] = len(list(recommended_set))
    except:
      row["Recommended set length"] = 0
    try:
      row["Actual recommended set length"] = len(f[sample_user]['high'])
    except:
      row["Actual recommended set length"] = 0
    try:
      row["Common recommendations"] = recommended_set & f[sample_user]['high']
    except:
      row["Common recommendations"] = 0
    try:
      row["Common recommendation length"] = len(list(recommended_set & f[sample_user]['high']))
    except:
      row["Common recommendation length"] = 0
    try:
      row["Coverage"] = len(list(recommended_set & f[sample_user]['high']))/len(f[sample_user]['high'])
    except:
      row["Coverage"] = 0
    try:
      accuracy += len(list(recommended_set & f[sample_user]['high']))/len(f[sample_user]['high'])
      row["Overall Coverage"] = accuracy/count
    except:
      row["Overall Coverage"] = 0
    try:
      error += len(list(recommended_set & f[sample_user]['high']))/len(list(recommended_set))
      row["Hit Rate"] = error
    except:
      row["Hit Rate"] = 0
    df1 = pd.DataFrame()
    df1 = df1.append(row, ignore_index=True)
    final_df = final_df.append(df1)

final_df

pickle.dump(final_df, open("/content/gdrive/My Drive/8th_Sem_Project PES_293_323_355/spectral_output.pickle","wb"))