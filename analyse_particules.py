#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 14:39:54 2023

@author: harry
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pollution=pd.read_csv('/home/harry/pollution/data_pollution.csv', sep=';')
pollution.columns=['année', 'mois', 'jour', 'heure', 'humidité', 'température', 'pm10', 'pm25']
pollution['date']=pollution.apply(lambda row: str(int(row['année']))+'/'+str(int(row['mois']))+'/' +str(int(row['jour']))+' '+str(int(row['heure']))+':'+str(int(0))+':'+str(int(0)), axis=1)
pollution['date']=pd.to_datetime(pollution['date'])
pollution=pollution.set_index('date')
pollution=pollution.drop(['année', 'mois', 'jour', 'heure'], axis=1)
pollution=pollution.loc['2023-10-24 07:00:00':,] # on commence aux données valables.
pollution['pm25']=pollution['pm25'].apply(lambda x: float(x))
pollution=pollution.groupby(pollution.index).mean()


plt.figure(figsize=(20, 20))
plt.subplot(2, 2, 1)
plt.title('évolution température')
plt.plot(pollution.index, pollution['température'], color='blue')
plt.xticks(rotation=90)
plt.ylabel('degrés celsius')
plt.subplot(2, 2, 2)
plt.title('évolution humidité')
plt.plot(pollution.index, pollution['humidité'], color='yellow')
plt.xticks(rotation=90)
plt.ylabel('% humidité')
plt.subplot(2, 2, 3)
plt.title('évolution pm10')
plt.plot(pollution.index, pollution['pm10'], color='red')
plt.xticks(rotation=90)
plt.subplot(2, 2, 4)
plt.title('évolution pm25')
plt.plot(pollution.index, pollution['pm25'], color='orange')
plt.xticks(rotation=90)
plt.show()