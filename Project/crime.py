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
import numpy as math
data = pd.read_csv('/Users/shaynarose/General_Assembly_DAT9/Project/2014.csv')
data14 = data[38272:]
data14c = data14.dropna()

#create latitude and Longitude columns as floats

latlon = pd.DataFrame(data14c['Location 1'].str.strip('()').str.split(',', 1).tolist())
data14b = pd.concat([data14c, latlon], axis = 1)


#38272:84224

#read in parks locations.  Using Baltimore's 18 official parks.
#is there way of getting all coordinates of parks/green spaces?
baltparks = pd.read_excel('/Users/shaynarose/General_Assembly_DAT9/Project/baltparks.xlsx')
baltparks

#Define function that converts coordinates to distance.
#Create dataframe with arbitrary coordinates for parks (using centers)
#(Might be better if use perimeter coordinates, defining quantity of coordinates per park by park size)
#Create new column that delivers crime's minimum distance to park in meters

# LatPark = baltbarks...
#LonParks = baltparks...
#for i in range(38272, 84224):
#   for j in range(1:18)
#       The_D[i,j] = distance(Lat[i], LatPark[j], Lon[i], LonPark[j])
#       Min_D = min(The_D across j) #WTF



def distance(Lat1, Lat2, Lon1, Lon2):
    phi_1 = Lat1*math.pi/180
    phi_2 = Lat2*math.pi/180
    Delta_phi = phi_2 - phi_1
    Delta_lambda = (Lon2 - Lon1)*math.pi/180
    a = math.sin(Delta_phi/2)**2 + math.cos(phi_1)*math.cos(phi_2)*math.sin(Delta_lambda/2)**2
    c = 2*math.arctan2(math.sqrt(a), math.sqrt(1-a))
    d = 6371000*c
    return d
    

    
    