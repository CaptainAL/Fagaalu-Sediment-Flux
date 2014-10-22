# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 09:24:16 2014

@author: Alex
"""
import matplotlib.pyplot as plt
import matplotlib as mpl
import pylab
import numpy as np
import pandas as pd
from pandas import DataFrame    
from AnnoteFinder import AnnoteFinder
import datetime as dt
import pandas.stats.moments as m
import math
plt.close('all')
plt.ion()

#### DIRECTORIES
datadir = 'C:/Users/Alex/Desktop/'### samoa/
csvoutputdir = datadir+'samoa/WATERSHED_ANALYSIS/FAGAALU/MasterDataFiles/csv_output/'

## custom modules
from misc_time import * 
from misc_numpy import *
from misc_matplotlib import * 

#### BAROMETERS
from load_csv_data import WeatherStation
## Wx at Faga'alu
FPa = WeatherStation(datadir+'samoa/WATERSHED_ANALYSIS/FAGAALU/MasterDataFiles/FP-Master-a.csv')
Bar15Min=FPa['Bar'].resample('15Min',fill_method='pad',limit=2) ## fill the 30min Barometric intervals to 15minute, but not Precip!
FPa = FPa.resample('15Min')
FPa['Bar']=Bar15Min
FPb = WeatherStation(datadir+'samoa/WATERSHED_ANALYSIS/FAGAALU/MasterDataFiles/FP-Master-b.csv')
FP = FPa.append(FPb)

from load_data import ndbc
allbaro = DataFrame(ndbc(datadir+'samoa/WATERSHED_ANALYSIS/BarometricData/NSTP6/'))
allbaro['FPbaro']=FP['Bar']/10
airport = DataFrame.from_csv('C:/Users/Alex/Desktop/samoa/WATERSHED_ANALYSIS/BarometricData/NSTU/NSTU-all.csv').resample('15Min')
airport['Sea Level PressureIn Int'] = airport['Sea Level PressureIn'].interpolate(method='linear')
TAFUNAbaro= DataFrame(airport['Sea Level PressureIn Int'] * 3.3863881579,columns=['Baropress']) ## inches to kPa
allbaro['TAFUNAbaro']=TAFUNAbaro['Baropress'] ## Use just the airport data: no shift needed, it seems to match up perfectly(??)
allbaro['Baropress']=TAFUNAbaro['Baropress']

#### PRECIPITATION
from precip_data import raingauge
## Faga'alu
Timu1 = raingauge(datadir+'samoa/WATERSHED_ANALYSIS/FAGAALU/MasterDataFiles/Timu1-Master.csv',180)
Timu2 = raingauge(datadir+'samoa/WATERSHED_ANALYSIS/FAGAALU/Timu2/Timu2-3_28_13-1minute.csv',180)

#Timu1
Timu1mm = DataFrame(Timu1['Events']*.254,columns=['Timu1'],index=date_range(datetime.datetime(2012,1,6,17,45,0),datetime.datetime(2013,6,26,0,0,0),freq='1Min')) ## hundredths to mm
Precip= DataFrame(Timu1mm['Timu1'].resample('D',how='sum'),columns=['Timu1-daily'])
#Timu2
Precip['Timu2-daily']=Timu2['Events'].resample('D',how='sum')*.254
##TimuWx
Precip['FPrain-daily']=FP['Rain'].resample('D',how=sum)



#### STAGE
from load_csv_data import PT_Hobo,PT_Levelogger
PT1a = PT_Hobo(allbaro,'PT1 LBJ bridge',datadir+'samoa/WATERSHED_ANALYSIS/FAGAALU/MasterDataFiles/Fagaalu1a-Master-to 10_10_12.csv',12) #12 x 15min = 3hours
PT1b = PT_Hobo(allbaro,'PT1 LBJ bridge',datadir+'/samoa/WATERSHED_ANALYSIS/FAGAALU/MasterDataFiles/Fagaalu1b-Master-to 6_25_13.csv',4)
PT1 = PT1a.append(PT1b)

PT2 = PT_Levelogger(allbaro,'PT2 Drive Thru',datadir+'samoa/WATERSHED_ANALYSIS/FAGAALU/MasterDataFiles/Fagaalu2-Master-to 3_19_12.csv')
PT2['stage'] = PT2['stage'] - 22
# tshift in 15Min(or whatever the timestep is), zshift in cm
PT3a = PT_Hobo(allbaro,'PT3a Dam',datadir+'samoa/WATERSHED_ANALYSIS/FAGAALU/MasterDataFiles/Fagaalu3a-Master-to 8_16_12.csv',12,-2)
PT3b = PT_Levelogger(allbaro,'PT3b Dam',datadir+'samoa/WATERSHED_ANALYSIS/FAGAALU/MasterDataFiles/Fagaalu3b-Master-to 3_8_13.csv',0,-22)
PT3c = PT_Levelogger(allbaro,'PT3c Dam',datadir+'samoa/WATERSHED_ANALYSIS/FAGAALU/MasterDataFiles/Fagaalu3c-Master-to 3_28_13.csv',0,-18.5)
PT3d = PT_Levelogger(allbaro,'PT3d Dam',datadir+'samoa/WATERSHED_ANALYSIS/FAGAALU/MasterDataFiles/Fagaalu3d-Master-to 4_15_13.csv',0,-16)
PT3e = PT_Levelogger(allbaro,'PT3e Dam',datadir+'samoa/WATERSHED_ANALYSIS/FAGAALU/MasterDataFiles/Fagaalu3e-Master-to 6_4_13.csv',0,-17.5)
PT3f = PT_Levelogger(allbaro,'PT3f Dam',datadir+'samoa/WATERSHED_ANALYSIS/FAGAALU/MasterDataFiles/Fagaalu3f-Master-to 6_26_13.csv',0,-17)
PT3g = PT_Levelogger(allbaro,'PT3g Dam',datadir+'samoa/WATERSHED_ANALYSIS/FAGAALU/MasterDataFiles/Fagaalu3g-Master-to 7_15_13.csv',0,2)
PT3 = pd.concat([PT3a,PT3b,PT3c,PT3d,PT3e,PT3f,PT3g])

## STAGE DATA FOR PT's
stage_data = DataFrame({'LBJ':PT1['stage'],'DT':PT2['stage'],'DAM':PT3['stage']})

#### TURBIDITY
from load_data import YSI,OBS
from load_csv_data import TS3000
TS3K = TS3000(datadir+'samoa/WATERSHED_ANALYSIS/FAGAALU/MasterDataFiles/TS3000-Master-to 7_18_12.csv')
YSI = YSI(datadir+'samoa/WATERSHED_ANALYSIS/FAGAALU/MasterDataFiles/YSI_LBJ_MASTER-to 5_23_12.txt')
OBS = OBS(datadir+'samoa/WATERSHED_ANALYSIS/FAGAALU/OBS500-LBJ/LBJ_Table1.dat')#.truncate(after=datetime.datetime(2013,4,1))

## GRABs
from load_csv_data import loadTSS,loadNUTES
TSS = loadTSS(datadir+'samoa/WATERSHED_ANALYSIS/TSS/TSS_grab_samples.xls','ALL_MASTER')
TSS['TSS (mg/L)'] = TSS['TSS (mg/L)'].where(TSS['TSS (mg/L)']>0)
NUTES = loadNUTES(datadir+'samoa/WATERSHED_ANALYSIS/FAGAALU/NUTRIENTS/Nutrients1.xls','by_Location')

## Plots


def PRECIP(show=False):
    fig= plt.figure()
    plt.plot_date(Precip['Timu1-daily'].index,Precip['Timu1-daily'],ls='steps-post',marker='None',c='r',label='Quarry')
    plt.plot_date(Precip['Timu2-daily'].index,Precip['Timu2-daily'],ls='steps-post',marker='None',c='g',label='Ridge')
    plt.plot_date(Precip['FPrain-daily'].index,Precip['FPrain-daily'],ls='steps-post',marker='None',c='y',label='Wx Station')
    
    plt.draw()
    if show==True:
        plt.show()
    return
#PRECIP(True)

def BARO(show=False):
    fig= plt.figure()
    
    plt.plot_date(allbaro['NDBCbaro'].index,allbaro['NDBCbaro'],ls='-',marker='None',c='r',label='NDBC at DMWR')
    plt.plot_date(allbaro['FPbaro'].index,allbaro['FPbaro'],ls='-',marker='None',c='g',label='Fagaalu Wx')
    plt.plot_date(allbaro['TAFUNAbaro'].index,allbaro['TAFUNAbaro'],ls='-',marker='None',c='y',label='Tafuna Airport')
    
    plt.draw()
    if show==True:
        plt.show()
    return
#BARO(True)

def STAGE(show=False):
    fig= plt.figure()
    
    plt.plot_date(stage_data['DAM'].index,stage_data['DAM'],ls='-',marker='None',c='g',label='Forest')
    plt.plot_date(stage_data['DT'].index,stage_data['DT'],ls='-',marker='None',c='y',label='Quarry')
    plt.plot_date(stage_data['LBJ'].index,stage_data['LBJ'],ls='-',marker='None',c='r',label='Village')
    
    plt.draw()
    if show==True:
        plt.show()
    return
#STAGE(True)
    
def PBS(show=False):
    fig, (precip, baro, stage) = plt.subplots(3,1,sharex=True)
    
    precip.plot_date(Precip['Timu1-daily'].index,Precip['Timu1-daily'],ls='steps-post',marker='None',c='r',label='Quarry')
    precip.plot_date(Precip['Timu2-daily'].index,Precip['Timu2-daily'],ls='steps-post',marker='None',c='g',label='Ridge')
    precip.plot_date(Precip['FPrain-daily'].index,Precip['FPrain-daily'],ls='steps-post',marker='None',c='y',label='Wx Station')
    precip.set_title('Precipitation')
    precip.set_ylabel('mm/day')
    precip.legend()
    
    baro.plot_date(allbaro['NDBCbaro'].index,allbaro['NDBCbaro'],ls='-',marker='None',c='r',label='NDBC at DMWR')
    baro.plot_date(allbaro['FPbaro'].index,allbaro['FPbaro'],ls='-',marker='None',c='g',label='Fagaalu Wx')
    baro.plot_date(allbaro['TAFUNAbaro'].index,allbaro['TAFUNAbaro'],ls='-',marker='None',c='y',label='Tafuna Airport')
    baro.set_title('Barometric Pressure')
    baro.set_ylabel('Sea Level Pressure (hPa)')
    baro.legend()
    
    stage.plot_date(stage_data['DAM'].index,stage_data['DAM'],ls='-',marker='None',c='g',label='Forest')
    stage.plot_date(stage_data['DT'].index,stage_data['DT'],ls='-',marker='None',c='y',label='Quarry')
    stage.plot_date(stage_data['LBJ'].index,stage_data['LBJ'],ls='-',marker='None',c='r',label='Village')
    stage.set_title('Stage')
    stage.set_ylabel('cm')
    stage.set_ylim(0,100)
    stage.legend()
    
    plt.draw()
    if show==True:
        plt.show()
    return
#PBS(True)

def TSN(show=False):
    fig, (ntu, ssc, nut) = plt.subplots(3,1,sharex=True)
    
    ntu.plot_date(TS3K['NTU'].index,TS3K['NTU'],ls='-',marker='None',c='g',label='Forest')
    ntu.plot_date(YSI['NTU'].index,YSI['NTU'],ls='-',marker='None',c='y',label='YSI-Village')
    ntu.plot_date(OBS['NTU'].index,OBS['NTU'],ls='-',marker='None',c='r',label='OBS-Village')
    ntu.set_title('Turbidity')
    ntu.set_ylabel('NTU')
    ntu.set_ylim(0,2000)
    precip = ntu.twinx()
    precip.plot_date(Precip['Timu1-daily'].index,Precip['Timu1-daily'],ls='steps-post',marker='None',c='b',label='Precip (Quarry)')
    precip.set_ylabel('mm')

    ssc.plot_date(TSS['TSS (mg/L)'].index,TSS['TSS (mg/L)'],c='r')
    ssc.set_ylabel('mg/L')
    ssc.set_title('Suspended Sediment Concentration (SSC)')
    ssc.set_ylim(0,10000)
    
    nut.plot_date(NUTES['TDN mg/L'].index,NUTES['TDN mg/L'],c='g')
    nut.plot_date(NUTES['TDP mg/L'].index,NUTES['TDP mg/L'],c='r')
    
    nut.set_title('Nutrients')
    nut.set_ylabel('mg/L')
    
    plt.draw()
    if show==True:
        plt.show()
    return
#TSN(True)

def Bars(show=False):
    fig=plt.figure()
    
    ## Precipitation    
    Precip['FP']=Precip['FPrain-daily'].notnull()*1.0
    plt.plot_date(Precip['FP'].index,Precip['FP'],c='g')
    
    Precip['T1']=Precip['Timu1-daily'].notnull()*1.3
    plt.plot_date(Precip['T1'].index,Precip['T1'],c='y')
    
    Precip['T2']=Precip['Timu2-daily'].notnull()*1.6
    plt.plot_date(Precip['T2'].index,Precip['T2'],c='r')
    
    ## Barometric
    allbaro['FP']=allbaro['FPbaro'].resample('D',how='mean').notnull()*2.0 ## take daily mean, calculate boolean column and multiply by whatever. It will give you zeros and whatever. Plot the whatevers
    plt.plot_date(allbaro['FP'].index,allbaro['FP'],c='g')
    
    allbaro['TAF']=allbaro['TAFUNAbaro'].resample('D',how='mean').notnull()*2.3
    plt.plot_date(allbaro['TAF'].index,allbaro['TAF'],c='y')
    
    allbaro['NDBC']=allbaro['NDBCbaro'].resample('D',how='mean').notnull()*2.6
    plt.plot_date(allbaro['NDBC'].index,allbaro['NDBC'],c='r')
    
    ## Stage
    stage_data['1']=stage_data['LBJ'].resample('D',how='mean').notnull()*3.0
    plt.plot_date(stage_data['1'].index,stage_data['1'],c='r')

    stage_data['2']=stage_data['DT'].resample('D',how='mean').notnull()*3.3
    plt.plot_date(stage_data['2'].index,stage_data['2'],c='y')
    
    
    stage_data['3']=stage_data['DAM'].resample('D',how='mean').notnull()*3.6
    plt.plot_date(stage_data['3'].index,stage_data['3'],c='g')
    
    ## Turbidity
    plt.plot_date(YSI['NTU'].resample('D',how='mean').index,YSI['NTU'].resample('D',how='mean').notnull()*4.0,c='r',label='YSI-Village')    
    plt.plot_date(OBS['NTU'].resample('D',how='mean').index,OBS['NTU'].resample('D',how='mean').notnull()*4.3,c='y',label='OBS-Village')
    plt.plot_date(TS3K['NTU'].resample('D',how='mean').index,TS3K['NTU'].resample('D',how='mean').notnull()*4.6,c='g',label='Forest')
    
    
    ## SSC
    plt.plot_date(TSS['TSS (mg/L)'].index,TSS['TSS (mg/L)'].notnull()*5.0,c='r')
    ## Nutrients
    plt.plot_date(NUTES['TDN mg/L'].index,NUTES['TDN mg/L'].notnull()*5.3,c='g')
    plt.plot_date(NUTES['TDP mg/L'].index,NUTES['TDP mg/L'].notnull()*5.6,c='r')
    
    ## Labels
    plt.text(Precip['T1'].index[0],1.1,'Rain Gage at Weather Station (mm-15min int.)')
    plt.text(Precip['T1'].index[0],1.4,'Rain Gage at Quarry (mm-1min int.)')
    plt.text(Precip['T1'].index[0],1.7,'Rain Gage at Ridge (mm-1min int.)')    
    
    plt.text(Precip['T1'].index[0],2.1,'Weather Station-bar.press.(kPa)')
    plt.text(Precip['T1'].index[0],2.4,'Tafuna Airport-bar.press.(kPa)')
    plt.text(Precip['T1'].index[0],2.7,'DMWR-bar.press.(kPa)')
    
    plt.text(Precip['T1'].index[0],3.1,'PT at LBJ-Stage(cm)')
    plt.text(Precip['T1'].index[0],3.4,'PT at Quarry-Stage(cm)')
    plt.text(Precip['T1'].index[0],3.7,'PT at Dam-Stage(cm)')
    
    plt.text(Precip['T1'].index[0],4.1,'YSI Turbidimeter at LBJ(NTU)')    
    plt.text(Precip['T1'].index[0],4.4,'OBS500 Turbidimeter at LBJ(NTU)')
    plt.text(Precip['T1'].index[0],4.7,'TS3000 Turbidimeter at Dam(NTU)')
    
    plt.text(Precip['T1'].index[0],5.1,'SSC (mg/L)')
    plt.text(Precip['T1'].index[0],5.4,'TDN (mg/L)')
    plt.text(Precip['T1'].index[0],5.7,'TDP (mg/L)')
    
    plt.ylim(0.9,6.1)

    
    
    plt.draw()
    if show==True:
        plt.show()
    return
Bars(True)