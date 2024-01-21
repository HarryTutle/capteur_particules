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

pollution=pd.read_csv('/home/harry/pollution/data_pollution_21_01_24.csv', sep=';')
pollution.columns=['année', 'mois', 'jour', 'heure', 'humidité', 'température', 'pm10', 'pm25']
pollution['date']=pollution.apply(lambda row: str(int(row['année']))+'/'+str(int(row['mois']))+'/' +str(int(row['jour']))+' '+str(int(row['heure']))+':'+str(int(0))+':'+str(int(0)), axis=1)
pollution['date']=pd.to_datetime(pollution['date'])
pollution=pollution.set_index('date')
pollution=pollution.drop(['année', 'mois', 'jour', 'heure'], axis=1)
pollution=pollution.loc['2023-10-24 07:00:00':,] # on commence aux données valables.
pollution['pm25']=pollution['pm25'].apply(lambda x: float(x))
pollution=pollution.groupby(pollution.index).mean()
pollution['jour_semaine']=pollution.index.day_name()
pollution['heure']=pollution.index.hour

""" pollution par jours"""

plt.figure(figsize=(20, 20))
plt.subplot(2, 2, 1)
plt.title('évolution température par jours')
plt.plot(pollution['température'].groupby(pd.Grouper(freq='D')).mean(), color='blue')
plt.xticks(rotation=90)
plt.ylabel('degrés celsius')
plt.subplot(2, 2, 2)
plt.title('évolution humidité par jours')
plt.plot(pollution['humidité'].groupby(pd.Grouper(freq='D')).mean(), color='yellow')
plt.xticks(rotation=90)
plt.ylabel('% humidité')
plt.subplot(2, 2, 3)
plt.title('évolution pm10 par jours')
plt.plot(pollution['pm10'].groupby(pd.Grouper(freq='D')).mean(), color='red')
plt.xticks(rotation=90)
plt.subplot(2, 2, 4)
plt.title('évolution pm25 par jours')
plt.plot(pollution['pm25'].groupby(pd.Grouper(freq='D')).mean(), color='orange')
plt.xticks(rotation=90)
plt.show()


""" selection données un jour """

def data_journée(date):
    
    """
    rentrer la date en string et au format datetime(ex: 2023-11-15 pour le 15 novembre).
    """

    
    
    data=pollution.loc[date+" 00:00:00": date+" 23:00:00" , :]
    
    plt.figure(figsize=(20, 20))
    plt.subplot(2, 2, 1)
    plt.title(f'évolution température: {date}')
    plt.plot(data.index, data['température'], color='blue')
    plt.xticks(rotation=90)
    plt.ylabel('degrés celsius')
    
    plt.subplot(2, 2, 2)
    plt.title(f'évolution humidité: {date}')
    plt.plot(data.index, data['humidité'], color='yellow')
    plt.xticks(rotation=90)
    plt.ylabel('% humidité')
    
    plt.subplot(2, 2, 3)
    plt.title(f'évolution pm10: {date}')
    plt.plot(data.index, data['pm10'], color='red')
    plt.xticks(rotation=90)
    
    plt.subplot(2, 2, 4)
    plt.title(f'évolution pm25: {date}')
    plt.plot(data.index, data['pm25'], color='orange')
    plt.xticks(rotation=90)
    
    plt.show()
    
    return data
    
debug=data_journée("2024-01-19")

''' distribution de la pollution selon le jour de la semaine en moyenne'''

plt.figure(figsize=(20, 20))
plt.subplot(2, 2, 1)
plt.title('distribution moyenne température')
plt.violinplot([pollution.loc[pollution['jour_semaine']==i, "température"] for i in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]])
plt.xticks([i for i in range(1, 8)], ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], rotation=45)
plt.subplot(2, 2, 2)
plt.title('distribution moyenne humidité')
plt.violinplot([pollution.loc[pollution['jour_semaine']==i, 'humidité'] for i in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]])
plt.xticks([i for i in range(1, 8)], ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], rotation=45)
plt.subplot(2, 2, 3)
plt.title('distribution moyenne pm10')
plt.violinplot([pollution.loc[pollution['jour_semaine']==i, "pm10"] for i in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]])
plt.xticks([i for i in range(1, 8)], ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], rotation=45)
plt.subplot(2, 2, 4)
plt.title('distribution moyenne pm25')
plt.violinplot([pollution.loc[pollution['jour_semaine']==i, 'pm25'] for i in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]])
plt.xticks([i for i in range(1, 8)], ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], rotation=45)
plt.show()

''' distribution pollution selon les heures et le jour de la semaine'''

plt.figure(figsize=(30, 60))
try:
    count=1
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday",  "Friday", "Saturday", "Sunday"]:
        plt.subplot(7, 1, count)
        plt.title(f"moyenne pm10 par heure pour {day}")
        plt.plot(pollution.loc[pollution['jour_semaine']==day, ['pm10', 'heure']].groupby('heure').mean())
        plt.xticks([i for i in range(0, 24)])
        count+=1  
        
except:
    pass
plt.show()


plt.figure(figsize=(30, 60))
try:
    count=1
    for day in ["Monday", "Tuesday", "Wednesday","Thursday" ,"Friday", "Saturday", "Sunday"]:
        plt.subplot(7, 1, count)
        plt.title(f"moyenne pm25 par heure pour {day}")
        plt.plot(pollution.loc[pollution['jour_semaine']==day, ['pm25', 'heure']].groupby('heure').mean())
        plt.xticks([i for i in range(0, 24)])
        count+=1         
except:
    pass

plt.show()

