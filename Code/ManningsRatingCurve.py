# -*- coding: utf-8 -*-
"""
Created on Sat Oct 25 15:39:23 2014

@author: Alex
"""

#### Import modules
## Data Processing
import numpy as np
import pandas as pd
import math
import datetime as dt
import pytz
## Set Pandas display options
pd.set_option('display.large_repr', 'truncate')
pd.set_option('display.max_rows', 15)

#### DIRECTORIES
git=True
if git==True: ## Git repository
    maindir = 'C:/Users/Alex/Documents/GitHub/Fagaalu-Sediment-Flux/' 
    datadir=maindir+'Data/'
    dataoutputdir = datadir+'Output/'
    GISdir = maindir+'Data/GIS/'
    figdir = maindir+'Figures/'
    dirs={'main':maindir,'data':datadir,'GIS':GISdir,'fig':figdir}
elif git!=True: ## Local folders
    maindir = 'C:/Users/Alex/Desktop/'### samoa/
    csvoutputdir = datadir+'samoa/WATERSHED_ANALYSIS/FAGAALU/MasterDataFiles/csv_output/'
    savedir = datadir+'samoa/WATERSHED_ANALYSIS/GoodFigures/'
    figdir = datadir+'samoa/WATERSHED_ANALYSIS/GoodFigures/rawfigoutput/'
    
    
XL = pd.ExcelFile(datadir+'Q/LBJ_cross_section.xlsx') 

df = XL.parse('LBJ_m',header=4,parse_cols='F:H')
df = df.dropna()

S = 0.01
n=0.05
areas, wp, v, q, = [],[],[],[]
stages = np.arange(.01,2,.1) #m
#stages = np.array([.1])
for stage in stages:
    df['y1'] = df['depth']+df['Rod Reading'].max()
    df['y2'] = stage
    df['z'] = df['y2']-df['y1']
    df['z'] = df['z'][df['z']>=0]
    
    x = df['Dist'].values
    y1 = df['y1'].values
    y2 = df['y2'].values
    
    z = y2-y1
    z= np.where(z>=0,z,0)
    Area = trapz(z,x)
    
    
    
    ## Wetted Perimeter
    df['dx'] =df['Dist'].sub(df['Dist'].shift(1),fill_value=0)
    df['dy'] = df['z'].sub(df['z'].shift(1),fill_value=0)
    df['wp'] = (df['dx']**2 + df['dy']**2)**0.5
    WP = df['wp'].sum()
    R = (Area/WP) ## m2/m = m
    ## Mannings = (1R^2/3 * S^1/2)/n
    ManningV = (1*(R**(2.0/3.0))*(S**0.5))/n
    ManningQ = ManningV * Area * 1000 ## L/Sec
            

    fig, ax1 = plt.subplots(1)
    ax1.plot(df['Dist'],df['y1'],'-o',c='k')
    ax1.fill_between(df['Dist'], df['y1'], stage,where = df['y1']<=stage,alpha=.5, interpolate=True)
    ax1.annotate('stage: '+str(stage)+'m',xy=(df['Dist'].mean(),stage+.03))
    ax1.annotate('Area: '+'%.3f'%Area+'m2',xy=(df['Dist'].min(),stage+.03))
    ax1.annotate('WP: '+'%.2f'%WP+'m',xy=(df['Dist'].min(),stage+.25))
    ax1.annotate('Manning V: '+'%.2f'%ManningV+'m/s ',xy=(df['Dist'].mean(),stage+.25))
    ax1.annotate('Manning Q: '+'%.3f'%ManningQ+'L/s',xy=(df['Dist'].mean(),stage+.45))
    plt.axes().set_aspect('equal')
    plt.xlim(-1,df['Dist'].max()+1),plt.ylim(-1,stage + 1.)


    areas.append(Area)
    wp.append(WP)
    v.append(ManningV)
    q.append(ManningQ)
    