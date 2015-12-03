# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 01:13:30 2015

@author: shaynarose
"""



#Purpose: To determine a relationship between crime and distance from green spaces.

#Ideas, all as a function of proximity to park:
#Type of crime
#Crime at certain time of day or year
#Predict this with decision trees?

#read in Baltimore City open source data and filter for only 2014.
#Drop any rows without locations.
import csv
import pandas as pd
import numpy as np

crime_file = '/Users/shaynarose/General_Assembly_DAT9/Project/2014.csv'
crime_file = '2014.csv'
data = pd.read_csv(crime_file)

#2014 values are (38272, 84224)
data14 = data[38272:]
data14 = data14.dropna()
#went from 45,952 rows to 14,603 rows

#create new columns for latitude and longitude
data14['lat'], data14['lon'] = zip(*data14['Location 1'].str.strip('()').str.split(',', 1).tolist())
data14.lat = data14.lat.astype(float)
data14.lon = data14.lon.astype(float)
data14 = data14.reset_index()
crime_len = len(data14)
crime_col_len = len(data14.columns)


#read in parks locations.  Using Baltimore's 18 official parks.
#is there way of getting all coordinates of parks/green spaces?
#used perimeter of parks every 500-1000 ft, a few center points
#excluded golf courses
parks_file = '/Users/shaynarose/General_Assembly_DAT9/Project/baltparks.xlsx'
parks_file = 'baltparks.xlsx'
baltparks = pd.read_excel(parks_file)

#Define function that converts coordinates to distance.
def distance(row):
    results = []
    print(row[0:10])
    for n in range(crime_col_len, crime_col_len + 290):
      park = row[n]
      phi_1 = row.lat*np.pi/180
      phi_2 = park[0]*np.pi/180
      delta_phi = phi_2 - phi_1
      Delta_lambda = (park[1] - row.lon)*np.pi/180
      a = np.sin(delta_phi/2)**2 + np.cos(phi_1)*np.cos(phi_2)*np.sin(Delta_lambda/2)**2
      results.append(6371000 * 2*np.arctan2(np.sqrt(a), np.sqrt(1-a)))
    results = np.asarray(results)

    return np.min(results)
    return np.argmin(results)
    
#iterate down baltparks for each crime in data14 to find minimum distance from any park
#return distance in new column
baltparks['latlon'] = zip(baltparks.lat, baltparks.lon)
parks_row = baltparks[['latlon']].transpose()
parks_row = parks_row.append([parks_row]*crime_len, ignore_index=True)
combined = pd.concat([data14, parks_row], axis = 1)
combined['closest'] = combined.apply(distance, axis=1)

#examine typical values
data14 = combined[['CrimeDate', 'CrimeCode', 'Description', 'Weapon', 'District', 'closest']]
data14.groupby('Description').closest.agg(['count', 'mean', 'min', 'max'])
data14.groupby('Weapon').closest.agg(['count', 'mean', 'min', 'max'])


import matplotlib.pyplot as plt


#box plot
data14.boxplot(column='closest', by='Description', vert=False)

#histograms
data14.closest.plot(kind='hist', bins=20, title='Crime Distance')
plt.xlabel('Distance (m)')
plt.ylabel('Frequency')

data14.groupby('Description').closest.plot(kind='hist', bins=20, title='Crime Distance')
plt.xlabel('Distance (m)')
plt.ylabel('Frequency')

data14.closest.plot(kind='hist', bins=20, title='Crime Distance', xlim = (0, 1000))
plt.xlabel('Distance (m)')
plt.ylabel('Frequency')

data14.groupby('Description').closest.plot(kind='hist', bins=20, title='Crime Distance', xlim = (0, 1000))
plt.xlabel('Distance (m)')
plt.ylabel('Frequency')

data14.groupby('Description').get_group('COMMON ASSAULT').closest.plot(kind='hist', bins=20, title='Common Assault', xlim = (0, 1000))
plt.xlabel('Distance (m)')
plt.ylabel('Frequency')

data14.groupby('Description').get_group('AGG. ASSAULT').closest.plot(kind='hist', bins=20, title='Aggressive Assault', xlim = (0, 1000))
plt.xlabel('Distance (m)')
plt.ylabel('Frequency')

#density plot
data14.closest.plot(kind='density', title='Crime Distance', xlim = (0, 1000))
plt.xlabel('Distance (m)')
plt.ylabel('Frequency')

data14.closest.plot(kind='density', title='Crime Distance', xlim = (0, 8000))
plt.xlabel('Distance (m)')
plt.ylabel('Frequency')

#density plot by crime type
data14.groupby('Description').closest.plot(kind='density', title='Crime Distance', xlim = (0, 1000))
plt.xlabel('Distance (m)')
plt.ylabel('Frequency')

data14.groupby('Description').closest.plot(kind='density', title='Crime Distance', xlim = (0, 8000))
plt.xlabel('Distance (m)')
plt.ylabel('Frequency')

data14.groupby('Description').closest.plot(kind='density', title='Crime Distance', xlim = (0, 2000))
plt.xlabel('Distance (m)')
plt.ylabel('Frequency')


from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn import metrics
feature_cols = ['Description', 'closest']

