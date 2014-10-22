# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 09:24:16 2014

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
plt.close('all')


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

## custom modules
from misc_time import * 
from misc_numpy import *
from misc_matplotlib import * 

print 'opening MASTER_DATA excel file...'+dt.datetime.now().strftime('%H:%M:%S')
if 'XL' not in locals():
    XL = pd.ExcelFile(datadir+'MASTER_DATA_FAGAALU.xlsx')
print 'MASTER_DATA opened: '+dt.datetime.now().strftime('%H:%M:%S')

#### BAROMETERS
#### Import WX STATION Data
from load_from_MASTER_XL import WeatherStation

FPa = WeatherStation(XL,'FP-30min')
Bar15Min=FPa['Bar'].resample('15Min',fill_method='pad',limit=2) ## fill the 30min Barometric intervals to 15minute, but not Precip!
FPa = FPa.resample('15Min')
FPa['Bar']=Bar15Min
FPb = WeatherStation(XL,'FP-15min')
FP = FPa.append(FPb)

#### Import BAROMETRIC Data: NDBC,TULA,TAFUNA
def Tula(datapath=datadir+'BARO/TulaStation/TulaMetData/'):
    #### Barometric Pressure from NOAA Weather Station Tula
    print 'loading TULAbaro....'
    ylist = ['2012']
    TulaPressureList = []
    #print 'month'+'\t'+'day'+'\t'+'year'+'\t'+'mm precip'
    for y in ylist:
        path = datapath+y
        files = os.listdir(path)
        for f in files: ## each f is a new DAY
            data = open(path+'/'+f,'r')
            daysplit = f.replace('.','-').split('-')
            #dayfile = open(daysplit[1]+'-'+daysplit[2]+'-'+daysplit[0]+'.csv','w')
            year, month, day = daysplit[0],daysplit[1],daysplit[2]
            #print 'year: '+year+' month '+month+' day: '+day
            dailyprecip, precipprev, precip15, pressure = 0.0,0.0,0.0,0.0
            presscount = 0
            try:
                for d in data: ## each d is a new MINUTE
                    split = d.split(',')
                    try:
                        num =float(split[1]) #will be True if split[1] is a number and the line is data
                    except:
                        num = False
                        pass
                    if num != False: ## Make sure the line is data #
                        #print split[1]+','+split[2]+','+split[3]+','+split[4]+','+split[5]+','+split[13]+','+split[18]
                        hour,minute = split[4], split[5]
                        press = split[13] #the pressure value for the Minute, need to be agg'ed to 15min.
                        precip = split[18] ## subtract the previous Minute's precip value
                        presscount+=1
                        try: ## Running total for 15 min. aggregate
                            if float(press) == False:
                                pressure = 'NaN'
                            if float(press) != 9999:
                                pressure = pressure + float(press) ## running total of pressure?
                            if float(press) == 9999:
                                pressure = pressure + 1000
                        except:
                                pressure = 'NaN'
                                pass
                                
                        try: ## Subtract previous minute's precip from current minute to get correct value
                            if float(precip) == False:
                                precip = 'NaN'
                            if precip != 9999:
                                #print str(precip)+' - '+str(precipprev)
                                precip = float(precip)-precipprev ## subtract previous minute's precip (precipprev) from current precip (precip)
                                #print precip ## this should be the correct precip value
                                precip15=precip15+float(precip) ## Running total for 15 minute aggregated rainfall
                                precipprev = split[18]
                        except:
                                precip = 'NaN'
                                pass
                        if minute == '':
                            minute = 'NaN'
                            pass
                        ## at 15 minute intervals average pressure and tally up precip
                        if float(minute) == 0 or float(minute)==15 or float(minute)==30 or float(minute)==45: ## Adjust time offset???
                                pressure15 = float(pressure)/presscount ## Get 15 minute average pressure 
                                dailyprecip = dailyprecip+float(precip) ## Aggregate daily rainfall
                                #print month+'/'+day+'/'+year+'\t'+hour+':'+str(minute)+'\t'+str(pressure15)+'\t'+str(precip15) 
                                #print month+'/'+day+'/'+year+'\t'+hour+':'+str(minute)+'\t'+str(pressure15) ## tab-separated output
                                Time = datetime.datetime(int(year),int(month),int(day),int(hour),int(minute)) ## -10 so it lines up with other times
                                #print Time
                                timedelta =-datetime.timedelta(hours=11)
                                Time = Time + timedelta ## time offset to get it to match Faga'alu
                                #print Time
                                TulaPressureList.append((Time,float(pressure15))) ## make list of 15 minute averaged atmospheric pressure
                                precipprev = split[18] ## reassign precip to precipprev for next loop
                                precip15,pressure,presscount = 0.0,0.0,0 ## reset variables for next loop
            except:
                    raise
            #print month+'\t'+day+'\t'+year+'\t'+str(dailyprecip)
    datadict = dict(TulaPressureList) ## Make dictionary of (Time,Pressure) tuples, RAW data
    baro = pd.Series(datadict,name='TULAbaro')
    baro_offset = (baro/10.0)+.92
    return baro_offset


##load data from Tafuna Intl ## To get more data from the Airport run wundergrabber_NSTU.py in the 'Maindir+Data/NSTU/' folder
airport = pd.DataFrame.from_csv(datadir+'BARO/NSTU/NSTU-current.csv') ## download new data using wundergrabber
airport['Wind Speed m/s']=airport['Wind SpeedMPH'] * 0.44704
#TAFUNAbaro= pd.DataFrame({'TAFUNAbaro':airport['Sea Level PressureIn'] * 3.3863881579}).resample('15Min',fill_method='ffill',limit=2)## inches to kPa
TAFUNAbaro= pd.DataFrame({'TAFUNAbaro':airport['Sea Level PressureIn'] *.1}).resample('15Min')## inches to kPa
TAFUNAbaro = TAFUNAbaro.reindex(pd.date_range(min(TAFUNAbaro.index),max(TAFUNAbaro.index),freq='15Min'))
##load data from NDBC NSTP6 station at DMWR, Pago Harbor
## To get more NSTP6 data either go to their website and copy and paste the historical data
## or use wundergrabber_NSTP6-REALTIME.py and copy and paste frome the .csv
def ndbc(datafile = datadir+'BARO/NSTP6/NSTP6-2012-14.xlsx'):
    ndbcXL = pd.ExcelFile(datafile)
    ndbc_parse = lambda yr,mo,dy,hr,mn: datetime.datetime(yr,mo,dy,hr,mn)
    ndbc_data = ndbcXL.parse('NSTP6-2012-14',header=0,skiprows=1,parse_dates=[['#yr','mo','dy','hr','mn']],index_col=0,date_parser=ndbc_parse,
                             na_values=['9999','999','99','99.0'])
    #local = pytz.timezone('US/Samoa')
    #ndbc_data.index = ndbc_data.index.tz_localize(pytz.utc).tz_convert(local)
    return ndbc_data

NDBCbaro = ndbc(datafile = datadir+'BARO/NSTP6/NSTP6-2012-14.xlsx')
NDBCbaro = NDBCbaro['hPa'].resample('15Min')
NDBCbaro = NDBCbaro.interpolate(method='linear',limit=4)
NDBCbaro.columns=['NDBCbaro']
NDBCbaro=NDBCbaro.shift(-44) ## UTC to Samoa local  =11 hours =44x15min

##load data from NOAA Climate Observatory at Tula, East Tutuila
TULAbaro= pd.DataFrame(Tula(datadir+'BARO/TulaStation/TulaMetData/'),columns=['TULAbaro']) ## add TULA barometer data

## Build data frame of barometric data: Make column 'baropress' with best available data
allbaro = pd.DataFrame(TAFUNAbaro['TAFUNAbaro'])
allbaro['FPbaro']=FP['Bar']/10
allbaro['NDBCbaro']=NDBCbaro/10
allbaro['TULAbaro']=TULAbaro['TULAbaro']

## Fill priority = FP,NDBC,TAFUNA,TULA
allbaro['Baropress']=allbaro['FPbaro'].where(allbaro['FPbaro']>0,allbaro['NDBCbaro']) ## create a new column and fill with FP or NDBC
allbaro['Baropress']=allbaro['Baropress'].where(allbaro['Baropress']>0,allbaro['TAFUNAbaro'])
allbaro['Baropress']=allbaro['Baropress'].where(allbaro['Baropress']>0,allbaro['TULAbaro']) 


#### PRECIPITATION
#### Import PRECIP Data
from precip_data import raingauge, AddTimu1, AddTimu1Hourly, AddTimu1Daily, AddTimu1Monthly

print 'opening MASTER_DATA excel file...'+dt.datetime.now().strftime('%H:%M:%S')
if 'XL' not in locals():
    XL = pd.ExcelFile(datadir+'MASTER_DATA_FAGAALU.xlsx')
print 'MASTER_DATA opened: '+dt.datetime.now().strftime('%H:%M:%S')

## Timu-Fagaalu 1 (by the Quarry)
Precip = raingauge(XL,'Timu-Fagaalu1-2013',180) ## (path,sheet,shift) no header needed
Precip = Precip.append(raingauge(XL,'Timu-Fagaalu1-2014',0)) ## (path,sheet,shift) no header needed
Precip.columns=['Timu1']
Precip['Timu1-15']=Precip['Timu1'].resample('15Min',how='sum')
Precip['Timu1-30']=Precip['Timu1'].resample('30Min',how='sum')

Precip['Timu1hourly']= Precip['Timu1'].resample('H',how='sum')
Precip['Timu1hourly'].dropna().to_csv(datadir+'OUTPUT/Timu1hourly.csv',header=['Timu1hourly'])

Precip['Timu1daily'] = Precip['Timu1'].resample('D',how='sum')
Precip['Timu1daily'].dropna().to_csv(datadir+'OUTPUT/Timu1daily.csv',header=['Timu1daily'])

Precip['Timu1monthly'] = Precip['Timu1'].resample('MS',how='sum') ## Monthly Precip
Precip['Timu1monthly'].dropna().to_csv(datadir+'OUTPUT/Timu1monthly.csv',header=['Timu1monthly'])

## Timu-Fagaalu2 (up on Blunt's Point Ridge; only deployed for 2 months in 2012)
Precip['Timu2-30']=raingauge(XL,'Timu-Fagaalu2',180).resample('30Min',how='sum')

Precip['Timu2hourly']= Precip['Timu2-30'].resample('H',how='sum')
Precip['Timu2hourly'].dropna().to_csv(datadir+'OUTPUT/Timu2hourly.csv',header=['Timu2hourly'])

Precip['Timu2daily'] = Precip['Timu2-30'].resample('D',how='sum')
Precip['Timu2daily'].dropna().to_csv(datadir+'OUTPUT/Timu2daily.csv',header=['Timu2daily'])

Precip['Timu2monthly'] = Precip['Timu2-30'].resample('MS',how='sum') ## Monthly Precip
Precip['Timu2monthly'].dropna().to_csv(datadir+'OUTPUT/Timu2monthly.csv',header=['Timu2monthly'])

Precip['FPrain']=FP['Rain'] ## mm?
Precip['FPrain-30']=Precip['FPrain'].resample('30Min',how=sum)
Precip['FPhourly'] = Precip['FPrain'].resample('H',how='sum') ## label=left?? 
Precip['FPdaily'] = Precip['FPrain'].resample('D',how='sum')
Precip['FPmonthly'] = Precip['FPrain'].resample('MS',how='sum')

Precip['FPhourly'].dropna().to_csv(datadir+'OUTPUT/FPhourly.csv',header=['FPhourly'])
Precip['FPdaily'].dropna().to_csv(datadir+'OUTPUT/FPdaily.csv',header=['FPdaily'])
Precip['FPmonthly'].dropna().to_csv(datadir+'OUTPUT/FPmonthly.csv',header=['FPmonthly'])

## Filled Precipitation record, priority = Timu1, fill with FPrain
PrecipFilled=pd.DataFrame(pd.concat([Precip['Timu1-15'][dt.datetime(2012,1,7):dt.datetime(2013,2,8)],Precip['FPrain'][dt.datetime(2013,2,8,0,15):dt.datetime(2013,3,12)],Precip['Timu1-15'][dt.datetime(2013,3,12,0,15):dt.datetime(2013,3,24)],Precip['FPrain'][dt.datetime(2013,3,24,0,15):dt.datetime(2013,5,1)],Precip['Timu1-15'][dt.datetime(2013,5,1,0,15):dt.datetime(2014,8,5)]]),columns=['Precip']).dropna()



#### STAGE
#### Import PT Data
# ex. PT_Levelogger(allbaro,PTname,datapath,tshift=0,zshift=0): 
from load_from_MASTER_XL import PT_Hobo,PT_Levelogger

PT1a = PT_Hobo(allbaro,'PT1 LBJ bridge',XL,'PT-Fagaalu1a',12) #12 x 15min = 3hours
PT1b = PT_Hobo(allbaro,'PT1 LBJ bridge',XL,'PT-Fagaalu1b',3)
PT1c = PT_Hobo(allbaro,'PT1 LBJ bridge',XL,'PT-Fagaalu1c',0)
PT1 = pd.concat([PT1a,PT1b,PT1c])

PT2 = PT_Levelogger(allbaro,'PT2 Drive Thru',XL,'PT-Fagaalu2',0,-22)
# tshift in 15Min(or whatever the timestep is), zshift in cm
PT3a = PT_Hobo(allbaro,'PT3a Dam',XL,'PT-Fagaalu3a',12,-3)
PT3b = PT_Levelogger(allbaro,'PT3b Dam',XL,'PT-Fagaalu3b',0,-23)
PT3c = PT_Levelogger(allbaro,'PT3c Dam',XL,'PT-Fagaalu3c',0,-18.5)
PT3d = PT_Levelogger(allbaro,'PT3d Dam',XL,'PT-Fagaalu3d',0,-16)
PT3e = PT_Levelogger(allbaro,'PT3e Dam',XL,'PT-Fagaalu3e',0,-17.4)
PT3f = PT_Levelogger(allbaro,'PT3f Dam',XL,'PT-Fagaalu3f',0,-17)
PT3g = PT_Levelogger(allbaro-1.5,'PT3g Dam',XL,'PT-Fagaalu3g',0,-10.5)
PT3 = pd.concat([PT3a,PT3b,PT3c,PT3d,PT3e,PT3f,PT3g])
PT3 = PT3[PT3>0]

## STAGE DATA FOR PT's
Fagaalu_stage_data = DataFrame({'LBJ':PT1['stage'],'DT':PT2['stage'],'DAM':PT3['stage']})

## Year Interval Times
start2012, stop2012 = datetime.datetime(2012,1,7,0,0), datetime.datetime(2012,12,31,11,59)    
start2013, stop2013 = datetime.datetime(2013,1,1,0,0), datetime.datetime(2013,12,31,11,59)
start2014, stop2014 = datetime.datetime(2014,1,1,0,0), datetime.datetime(2014,12,31,11,59)   
PT1 = PT1.reindex(pd.date_range(start2012,stop2014,freq='15Min'))
PT3 = PT3.reindex(pd.date_range(start2012,stop2014,freq='15Min'))
Fagaalu_stage_data = Fagaalu_stage_data.reindex(pd.date_range(start2012,stop2014,freq='15Min'))

#### Import T and SSC Data
from load_from_MASTER_XL import TS3000,YSI,OBS,loadTSS
## Turbidimeter Data DAM
DAM_TS3K = TS3000(XL,'DAM-TS3K')
DAM_YSI = YSI(XL,'DAM-YSI')

## Turbidimeter Data LBJ
LBJ_YSI = YSI(XL,'LBJ-YSI')
LBJ_OBSa = OBS(XL,'LBJ-OBSa').truncate(after=dt.datetime(2013,4,1))
LBJ_OBSb = OBS(XL,'LBJ-OBSb')
LBJ_OBSa=LBJ_OBSa.rename(columns={'Turb_SS_Avg':'NTU'})
LBJ_OBSb=LBJ_OBSb.rename(columns={'Turb_SS_Mean':'NTU'})
LBJ_OBS=LBJ_OBSa.append(LBJ_OBSb)

## TSS Data, equivalent to SSC but I don't want to change all the code and file names
TSSXL = pd.ExcelFile(datadir+'SSC/TSS_grab_samples.xlsx')
TSS = loadTSS(TSSXL,'ALL_MASTER')
TSS= TSS[TSS['TSS (mg/L)']>0]


#### Import NUTRIENT Data
from load_from_MASTER_XL import loadNUTES1,loadNUTES2and3
##NUTRIENTS1 (first field season)
NUTESXL = pd.ExcelFile(datadir+'NUTRIENTS/NUTRIENTS1.xlsx')
NUTES1 = loadNUTES1(NUTESXL,'Data')
##NUTRIENTS2and3 (second and third field season)
NUTES2XL = pd.ExcelFile(datadir+'NUTRIENTS/NUTRIENTS from Lisa 5_5_14.xlsx')
NUTES2infoXL = pd.ExcelFile(datadir+'NUTRIENTS/NUTRIENTS to Lisa 3_17_14.xlsx')
NUTES2and3 = loadNUTES2and3(NUTES2XL,NUTES2infoXL)

#NUTES2and3.to_excel(datadir+'samoa/WATERSHED_ANALYSIS/NUTRIENTS/NUTES2and3.xlsx')
NUTES = NUTES1.append(NUTES2and3)
#NUTES.to_excel(datadir+'samoa/WATERSHED_ANALYSIS/NUTRIENTS/NUTES_ALL.xlsx')



## Plots
def PRECIP(show=False):
    print 'plotting Precip...'
    fig= plt.figure()
    Precip['Timu1daily'].dropna().plot(ls='steps-post',marker='None',c='r',label='Quarry')
    Precip['Timu2daily'].dropna().plot(ls='steps-post',marker='None',c='g',label='Ridge')
    Precip['FPdaily'].dropna().plot(ls='steps-post',marker='None',c='y',label='Wx Station')
    
    plt.draw()
    if show==True:
        plt.show()
    return
PRECIP(True)

def BARO(show=False):
    print 'Plotting Baro...'
    fig= plt.figure()
    
    plt.plot_date(allbaro['NDBCbaro'].index,allbaro['NDBCbaro'],ls='-',marker='None',c='r',label='NDBC at DMWR')
    plt.plot_date(allbaro['FPbaro'].index,allbaro['FPbaro'],ls='-',marker='None',c='g',label='Fagaalu Wx')
    plt.plot_date(allbaro['TAFUNAbaro'].index,allbaro['TAFUNAbaro'],ls='-',marker='None',c='y',label='Tafuna Airport')
    
    plt.ylim(100,102)    
    
    plt.draw()
    if show==True:
        plt.show()
    return
BARO(True)

def STAGE(show=False):
    print 'Plotting Stage...'
    fig= plt.figure()
    
    plt.plot_date(Fagaalu_stage_data['DAM'].index,Fagaalu_stage_data['DAM'],ls='-',marker='None',c='g',label='Forest')
    plt.plot_date(Fagaalu_stage_data['DT'].index,Fagaalu_stage_data['DT'],ls='-',marker='None',c='y',label='Quarry')
    plt.plot_date(Fagaalu_stage_data['LBJ'].index,Fagaalu_stage_data['LBJ'],ls='-',marker='None',c='r',label='Village')
    Precip['Timu1daily'].dropna().plot(ls='steps-post',marker='None',c='b',label='Quarry',alpha=0.5)
    
    plt.ylim(0,200)
    
    plt.draw()
    if show==True:
        plt.show()
    return
STAGE(True)
    
def PBS(show=False):
    print 'plotting PBS...'
    fig, (precip, baro, stage) = plt.subplots(3,1,sharex=True)
    
    precip.plot_date(Precip['Timu1daily'].index,Precip['Timu1daily'],ls='steps-post',marker='None',c='r',label='Quarry')
    precip.plot_date(Precip['Timu2daily'].index,Precip['Timu2daily'],ls='steps-post',marker='None',c='g',label='Ridge')
    precip.plot_date(Precip['FPdaily'].index,Precip['FPdaily'],ls='steps-post',marker='None',c='y',label='Wx Station')
    precip.set_title('Precipitation')
    precip.set_ylabel('mm/day')
    precip.legend()
    
    baro.plot_date(allbaro['NDBCbaro'].index,allbaro['NDBCbaro'],ls='-',marker='None',c='r',label='NDBC at DMWR')
    baro.plot_date(allbaro['FPbaro'].index,allbaro['FPbaro'],ls='-',marker='None',c='g',label='Fagaalu Wx')
    baro.plot_date(allbaro['TAFUNAbaro'].index,allbaro['TAFUNAbaro'],ls='-',marker='None',c='y',label='Tafuna Airport')
    baro.set_title('Barometric Pressure')
    baro.set_ylabel('Sea Level Pressure (hPa)')
    baro.legend()
    
    stage.plot_date(Fagaalu_stage_data['DAM'].index,Fagaalu_stage_data['DAM'],ls='-',marker='None',c='g',label='Forest')
    stage.plot_date(Fagaalu_stage_data['DT'].index,Fagaalu_stage_data['DT'],ls='-',marker='None',c='y',label='Quarry')
    stage.plot_date(Fagaalu_stage_data['LBJ'].index,Fagaalu_stage_data['LBJ'],ls='-',marker='None',c='r',label='Village')
    stage.set_title('Stage')
    stage.set_ylabel('cm')
    stage.set_ylim(0,100)
    stage.legend()
    
    plt.draw()
    if show==True:
        plt.show()
    return
PBS(True)

def TSN(show=False):
    print 'plotting TSN...'
    fig, (ntu, ssc, nut) = plt.subplots(3,1,sharex=True)
    
    ntu.plot_date(DAM_TS3K['NTU'].index,DAM_TS3K['NTU'],ls='-',marker='None',c='g',label='TS3K-Forest')
    ntu.plot_date(DAM_YSI['NTU'].index,DAM_YSI['NTU'],ls='-',marker='None',c='y',label='YSI-Forest')
    ntu.plot_date(LBJ_YSI['NTU'].index,LBJ_YSI['NTU'],ls='-',marker='None',c='y',label='YSI-Village')
    ntu.plot_date(LBJ_OBS['NTU'].index,LBJ_OBS['NTU'],ls='-',marker='None',c='r',label='OBS-Village')
    ntu.set_title('Turbidity')
    ntu.set_ylabel('NTU')
    ntu.set_ylim(0,2000)
    precip = ntu.twinx()
    precip.plot_date(Precip['Timu1daily'].index,Precip['Timu1daily'],ls='steps-post',marker='None',c='b',label='Precip (Quarry)')
    precip.set_ylabel('mm')

    ssc.plot_date(TSS['TSS (mg/L)'].index,TSS['TSS (mg/L)'],c='r')
    ssc.set_ylabel('mg/L')
    ssc.set_title('Suspended Sediment Concentration (SSC)')
    ssc.set_ylim(0,10000)
    
    nut.plot_date(NUTES['TDNmg/L'].index,NUTES['TDNmg/L'],c='g')
    nut.plot_date(NUTES['TDPmg/L'].index,NUTES['TDPmg/L'],c='r')
    
    nut.set_title('Nutrients')
    nut.set_ylabel('mg/L')
    
    plt.draw()
    if show==True:
        plt.show()
    return
TSN(True)

def Bars(show=False):
    print 'plotting Bars...'
    fig=plt.figure()
    
    ## Precipitation    
    Precip['FP']=Precip['FPdaily'].notnull()*1.0
    plt.plot_date(Precip['FP'].index,Precip['FP'],c='g')
    
    Precip['T1']=Precip['Timu1daily'].notnull()*1.3
    plt.plot_date(Precip['T1'].index,Precip['T1'],c='y')
    
    Precip['T2']=Precip['Timu2daily'].notnull()*1.6
    plt.plot_date(Precip['T2'].index,Precip['T2'],c='r')
    
    ## Barometric
    allbaro['FP']=allbaro['FPbaro'].resample('D',how='mean').notnull()*2.0 ## take daily mean, calculate boolean column and multiply by whatever. It will give you zeros and whatever. Plot the whatevers
    plt.plot_date(allbaro['FP'].index,allbaro['FP'],c='g')
    
    allbaro['TAF']=allbaro['TAFUNAbaro'].resample('D',how='mean').notnull()*2.3
    plt.plot_date(allbaro['TAF'].index,allbaro['TAF'],c='y')
    
    allbaro['NDBC']=allbaro['NDBCbaro'].resample('D',how='mean').notnull()*2.6
    plt.plot_date(allbaro['NDBC'].index,allbaro['NDBC'],c='r')
    
    ## Stage
    Fagaalu_stage_data['1']=Fagaalu_stage_data['LBJ'].resample('D',how='mean').notnull()*3.0
    plt.plot_date(Fagaalu_stage_data['1'].index,Fagaalu_stage_data['1'],c='r')

    Fagaalu_stage_data['2']=Fagaalu_stage_data['DT'].resample('D',how='mean').notnull()*3.3
    plt.plot_date(Fagaalu_stage_data['2'].index,Fagaalu_stage_data['2'],c='y')
    
    
    Fagaalu_stage_data['3']=Fagaalu_stage_data['DAM'].resample('D',how='mean').notnull()*3.6
    plt.plot_date(Fagaalu_stage_data['3'].index,Fagaalu_stage_data['3'],c='g')
    
    ## Turbidity
    plt.plot_date(LBJ_YSI['NTU'].resample('D',how='mean').index,LBJ_YSI['NTU'].resample('D',how='mean').notnull()*4.0,c='r',label='YSI-Village')    
    plt.plot_date(LBJ_OBS['NTU'].resample('D',how='mean').index,LBJ_OBS['NTU'].resample('D',how='mean').notnull()*4.3,c='y',label='OBS-Village')
    plt.plot_date(DAM_TS3K['NTU'].resample('D',how='mean').index,DAM_TS3K['NTU'].resample('D',how='mean').notnull()*4.6,c='g',label='TS3K-Forest')
    plt.plot_date(DAM_YSI['NTU'].resample('D',how='mean').index,DAM_YSI['NTU'].resample('D',how='mean').notnull()*4.6,c='g',label='YSI-Forest')

    ## SSC
    plt.plot_date(TSS['TSS (mg/L)'].index,TSS['TSS (mg/L)'].notnull()*5.0,c='r')
    ## Nutrients
    plt.plot_date(NUTES['TDNmg/L'].index,NUTES['TDNmg/L'].notnull()*5.3,c='g')
    plt.plot_date(NUTES['TDPmg/L'].index,NUTES['TDPmg/L'].notnull()*5.6,c='r')
    
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

    
    if show==True:
        plt.show()
    return
Bars(True)