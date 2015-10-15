# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 06:55:40 2015

@author: Alex
"""


## THIS IS TO LOAD AND USE BAROMETRIC DATA FROM THE AIRPORT AT TAFUNA
## IT WASN'T NEEDED AFTER ADEQUATE DATA WAS FOUND FROM THE NDBC NSTP6 STATION


## Load data from Tafuna Intl Airport
## To get more data run wundergrabber_NSTU.py in the 'Maindir+Data/NSTU/' folder
airport = pd.DataFrame.from_csv(datadir+'BARO/NSTU/NSTU-current.csv') 
airport['Wind Speed m/s']=airport['Wind SpeedMPH'] * 0.44704
TAFUNAbaro= pd.DataFrame({'TAFUNAbaro':airport['Sea Level PressureIn'] * 3.3863881579}).resample('15Min',fill_method='ffill',limit=2)## inches to kPa

## THESE LINES GO WHERE THE allbaro df is created
allbaro['TAFUNAbaro']=TAFUNAbaro['TAFUNAbaro']

allbaro['Baropress']=allbaro['Baropress'].where(allbaro['Baropress']>0,allbaro['TAFUNAbaro'])











