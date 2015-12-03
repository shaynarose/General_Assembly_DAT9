# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 21:30:16 2015

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
data = pd.read_csv(crime_file)

#2014 values are (38272, 84224)
data14 = data[38272:]
data14 = data14.dropna()
#went from 45,952 rows to 14,603 rows
​
#create new columns for latitude and longitude
data14['lat'], data14['lon'] = zip(*data14['Location 1'].str.strip('()').str.split(',', 1).tolist())
data14.lat = data14.lat.astype(float)
data14.lon = data14.lon.astype(float)
data14 = data14.reset_index()
crime_len = len(data14)
crime_col_len = len(data14.columns)
​
​
#read in parks locations.  Using Baltimore's 18 official parks.
#is there way of getting all coordinates of parks/green spaces?
#used perimeter of parks every 500-1000 ft, a few center points
#excluded golf courses
parks_file = '/Users/shaynarose/General_Assembly_DAT9/Project/baltparks.xlsx'
baltparks = pd.read_excel(parks_file)
​
#Define function that converts coordinates to distance.
def distance(row):
    results = []
    print(row[0:10])
    for n in range(crime_col_len, crime_col_len + 290):
      # print(row[n])
    # return 77
      park = row[n]
      phi_1 = row.lat*np.pi/180
      phi_2 = park[0]*np.pi/180
      delta_phi = phi_2 - phi_1
      Delta_lambda = (park[1] - row.lon)*np.pi/180
      a = np.sin(delta_phi/2)**2 + np.cos(phi_1)*np.cos(phi_2)*np.sin(Delta_lambda/2)**2
      results.append(6371000 * 2*np.arctan2(np.sqrt(a), np.sqrt(1-a)))
      results = np.asarray(results)
​
    return np.argmin(results)
    
#baltparks will be Lat2, Lon2 and data14 will be Lat1, Lon1.
#iterate down baltparks for each crime in data14 to find minimum distance from any park
#return distance and park name in two new columns
​
# for i in range(0, 14602):
#   for j in range(0, 290):
#       big_D = pd.DataFrame()
#       big_D[i, j] = distance(data14.lat[i], baltparks.lat[j], data14.lon[i], baltparks.lon[j])
​
print(data14.size)
flatparks = pd.DataFrame(baltparks[['lat', 'lon']].stack())
# flatparks.columns = flatparks.columns.get_level_values(0) + flatparks.columns.get_level_values(1)
print(flatparks)
# print(baltparks[['lat', 'lon']].stack())
baltparks['latlon'] = zip(baltparks.lat, baltparks.lon)
parks_row = baltparks[['latlon']].transpose()
parks_row = parks_row.append([parks_row]*crime_len, ignore_index=True)
combined = pd.concat([data14, parks_row], axis = 1)
combined['closest'] = combined[0:100].apply(distance, axis=1)
print(combined.columns[0:20])
    

    
    