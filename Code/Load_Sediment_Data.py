# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 11:36:17 2016

@author: Alex
"""

#timer
import datetime as dt
start_time = dt.datetime.now()
print 'Start time: '+start_time.strftime('%H:%M:%S')



#### Import modules
## Data Processing
import os
import numpy as np
import pandas as pd

## Statistical Analysis
from scipy import stats
import pandas.stats.moments as m
from scipy.stats import pearsonr as pearson_r
from scipy.stats import spearmanr as spearman_r

import statsmodels.formula.api as smf
import statsmodels.stats.api

## Call R modules
#from rpy2.robjects.packages import importr
import rpy2.robjects as ro
import pandas.rpy.common as com

## Make sure R is communicating
ro.r('x=c()')
ro.r('x[1]="lets talk to R"')
print(ro.r('x'))


#### Plotting Tools
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.gridspec as gridspec 
import pylab
from AnnoteFinder import AnnoteFinder
import seaborn as sns
plt.close('all')
plt.ion()

##custom modules
import misc_time
from misc_time import * 
from misc_numpy import *
from misc_matplotlib import * 

## Set Pandas display options
pd.set_option('display.large_repr', 'truncate')
pd.set_option('display.width', 180)
pd.set_option('display.max_rows', 30)
pd.set_option('display.max_columns', 13)

#### DIRECTORIES
git=True
if git==True: ## Git repository
    maindir = 'C:/Users/Alex/Documents/GitHub/Fagaalu-Sediment-Flux/'
    #maindir = 'C:/Users/Alex/Documents/GitHub/Fagaalu-Sedimentation/' 
    datadir=maindir+'Data/'
    watershed_datadir= 'C:/Users/Alex/Documents/GitHub/Fagaalu-Sediment-Flux/Data/' 
    dataoutputdir = datadir+'Output/'
    GISdir = maindir+'Data/GIS/'
    figdir = maindir+'Figures/'
    tabledir = maindir+'Tables/'
    dirs={'main':maindir,'data':datadir,'GIS':GISdir,'fig':figdir}
elif git!=True: ## Local folders
    maindir = 'C:/Users/Alex/Desktop/'### samoa/
    csvoutputdir = datadir+'samoa/WATERSHED_ANALYSIS/FAGAALU/MasterDataFiles/csv_output/'
    savedir = datadir+'samoa/WATERSHED_ANALYSIS/GoodFigures/'
    figdir = datadir+'samoa/WATERSHED_ANALYSIS/GoodFigures/rawfigoutput/'
    
## Figure formatting
#publishable =  plotsettings.Set('GlobEnvChange')    ## plotsettings.py
#publishable.set_figsize(n_columns = 2, n_rows = 2)
    
mpl.rc_file(maindir+'johrc.rc')
mpl.rcParams['savefig.directory']=maindir+'rawfig/'
mpl.rcParams
mpl.rc('legend',scatterpoints=1)  
## Ticks
my_locator = matplotlib.ticker.MaxNLocator(4)

def show_plot(show=False,fig=figure):
    if show==True:
        plt.show()
        

def letter_subplots(fig,x=0.1,y=0.95,vertical='top',horizontal='right',Color='k',font_size=10,font_weight='bold'):
    sub_plot_count = 0
    sub_plot_letters = {0:'(a)',1:'(b)',2:'(c)',3:'(d)',4:'(e)',5:'(f)',6:'(g)',7:'(h)',8:'(i)'}
    for ax in fig.axes:
        ax.text(x,y,sub_plot_letters[sub_plot_count],verticalalignment=vertical, horizontalalignment=horizontal,transform=ax.transAxes,color=Color,fontsize=font_size,fontweight=font_weight)
        sub_plot_count+=1
    return 

def logaxes(log=False,fig=figure):
    if log==True:
        print 'log axes'
        for ax in fig.axes:
            ax.set_yscale('log'), ax.set_xscale('log')
    return
def savefig(save=True,filename=''):
    if save==True:
        plt.savefig(filename+'.pdf') ## for publication
        plt.savefig(filename+'.png') ## for manuscript
    return

def labelindex_subplot(ax,i,x,y): 
    indexstrings = [str(ind) for ind in i]
    af = AnnoteFinder(x,y,indexstrings,axis=ax)
    connect('button_press_event', af)
    return

    
def power(x,a,b):
    y = a*(x**b)
    return y
    
def powerfunction(x,y,name='power rating',pvalue=0.01):
    ## put x and y in a dataframe so you can drop ones that don't match up  
    datadf = pd.DataFrame.from_dict({'x':x,'y':y}).dropna().apply(np.log10)   
    datadf = datadf[datadf>=-10] ##verify data is valid (not inf)
    regression = pd.ols(y=datadf['y'],x=datadf['x'])
    if pearson_r(datadf['x'],datadf['y'])[1] < pvalue:
        pearson = pearson_r(datadf['x'],datadf['y'])[0]
    else: 
        pearson = np.nan
    if  spearman_r(datadf['x'],datadf['y'])[1] < pvalue:
        spearman = spearman_r(datadf['x'],datadf['y'])[0]
    else:
        spearman = np.nan
    coeffdf = pd.DataFrame({'a':[10**regression.beta[1]],'b':[regression.beta[0]],
    'r2':[regression.r2],'rmse':[regression.rmse],'pearson':[pearson],'spearman':[spearman]},
index=[name])
    return coeffdf

def PowerFit(x,y,xspace = 'none',ax=plt,**kwargs):
    ## Develop power function for x and y
    powfunc = powerfunction(x,y) ## x and y should be Series
    a, b = powfunc['a'].values, powfunc['b'].values
    #print a,b
    if xspace == 'none':
        xvals = np.linspace(x.min()-10,x.max()*1.2)
        #print 'No xspace, calculating xvals: '+'%.0f'%x.min()+'-'+'%.0f'%x.max()+'*1.5= '+'%.0f'%(x.max()*1.5)
    else:
        xvals=xspace
    ypred = a*(xvals**b)
    ax.plot(xvals,ypred,**kwargs)
    return powfunc  

def Sum_Storms(Storm_list,Data,offset=0):
    eventlist = []
    print 'Summing storms...'
    for storm_index,storm in Storm_list.iterrows():
        start = storm['start']-dt.timedelta(minutes=offset) ##if Storms are defined by stream response you have to grab the preceding precip data
        end= storm['end']
        data = True ## Innocent until proven guilty
        try:
            #print str(start) +' '+str(end)
            event = Data.ix[start:end] ### slice list of Data for event
        except KeyError:
            raise
            start = start+dt.timedelta(minutes=15) ## if the start time falls between 2 30minute periods
            print 'change storm start to '+str(start)            
            try:
                event = Data.ix[start:end]
            except KeyError:
                end = end+dt.timedelta(minutes=15)
                print 'change storm end to '+str(end) 
                try:
                    event = Data.ix[start:end]
                except KeyError:
                    print 'no storm data available for storm '+str(start)
                    data = False
                    pass
        if data != False:
            eventcount,eventsum,eventmax=np.nan,np.nan,np.nan
            ## only take events with complete data
            if len(event.dropna()) == len(event):
                eventcount = event.count()
                eventsum = event.sum()
                eventmax = event.max()
                eventlist.append((storm['start'],[storm['start'],storm['end'],eventcount,eventsum,eventmax])) 
            else:
                eventlist.append((storm['start'],[storm['start'],storm['end'],eventcount,eventsum,eventmax])) 
        if data == False:
            eventcount,eventsum,eventmax=np.nan,np.nan,np.nan
            eventlist.append((storm['start'],[storm['start'],storm['end'],eventcount,eventsum,eventmax])) 
    Events=DataFrame.from_items(eventlist,orient='index',columns=['start','end','count','sum','max'])
    return Events
    
## Year Interval Times
start2012, stop2012 = dt.datetime(2012,1,1,0,0), dt.datetime(2012,12,31,11,59)    
start2013, stop2013 = dt.datetime(2013,1,1,0,0), dt.datetime(2013,12,31,11,59)
start2014, stop2014 = dt.datetime(2014,1,1,0,0), dt.datetime(2014,12,31,11,59)   
start2015, stop2015 = dt.datetime(2015,1,1,0,0), dt.datetime(2015,12,31,11,59)   
## Field Seasons
fieldstart2012, fieldstop2012 =  dt.datetime(2012,1,5,0,0), dt.datetime(2012,3,29,11,59)    
fieldstart2013, fieldstop2013 =  dt.datetime(2013,2,4,0,0), dt.datetime(2013,7,17,11,59)    
fieldstart2014a, fieldstop2014a =  dt.datetime(2014,1,10,0,0), dt.datetime(2014,3,7,11,59)
fieldstart2014b, fieldstop2014b =  dt.datetime(2014,9,29,0,0), dt.datetime(2015,1,12,11,59)     
## Mitigation
Mitigation = dt.datetime(2014,10,1,0,0)
## SedPods
study_start , study_end= dt.datetime(2014,3,1), dt.datetime(2015,4,30)


### LOAD FIELD DATA
if 'XL' not in locals():
    ## Sediment Budget (pre-mitigation)
    master_data_filename = datadir+'MASTER_DATA_FAGAALU.xlsx'
    ## Sediment Budget (with post-mitigation)
    #master_data_filename = datadir+'MASTER_DATA_FAGAALU_with new 2015 data.xlsx'
    ## Reef Sedimentation Analysis
    #master_data_filename =    datadir+'Fagaalu_Watershed/MASTER_DATA_FAGAALU_for sedimentation.xlsx'
    
    print 'opening MASTER_DATA excel file...'+dt.datetime.now().strftime('%H:%M:%S')
    XL = pd.ExcelFile(master_data_filename)

    
    
    #XL = pd.ExcelFile()
    
if 'XL' in locals():
    print 'MASTER_DATA opened: '+dt.datetime.now().strftime('%H:%M:%S')    
    
#### Import PRECIP Data
#from precip_data import raingauge#, AddTimu1, AddTimu1Hourly, AddTimu1Daily, AddTimu1Monthly
def raingauge(XL,sheet='',shift=0):
    print 'loading precip: '+sheet+'...'
    #my_parser= lambda x: dt.datetime.strptime(x,"%m/%d/%Y %H:%M")
    gauge = XL.parse(sheet,header=1,index_col=0,parse_cols='B,C',parse_dates=True)#,date_parser=my_parser)
    gauge= gauge.shift(shift)
    gauge = gauge*0.254 ##hundredths to mm
    gauge.columns=['Events']
    return gauge    

if 'Precip' not in locals():
    ## Timu-Fagaalu 1 (by the Quarry)
    ## 2012-2013 Data
    Precip = raingauge(XL,'Timu-Fagaalu1-2013',180) ## (path,sheet,shift) no header needed
    Precip = Precip.truncate(dt.datetime(2012,1,21,0,0)) ### The Timu1 rain gauge had a wire loose and didn't record data until after 1/20/2012 when I fixed it
    Precip= Precip.reindex(pd.date_range(dt.datetime(2012,1,6,17,51),dt.datetime(2013,12,31,23,59),freq='1Min'))
    ## 2014 Data
    Precip = Precip.append(raingauge(XL,'Timu-Fagaalu1-2014',0)) ## (path,sheet,shift) no header needed
    ## 2015 Data
    #Precip = Precip.append(raingauge(XL,'Timu-Fagaalu1-2015',0)) ## (path,sheet,shift) no header needed
    Precip.columns=['Timu1']
    Precip['Timu1-15']=Precip['Timu1'].resample('15Min',how='sum')
    Precip['Timu1-30']=Precip['Timu1'].resample('30Min',how='sum')
    # Hourly
    Precip['Timu1hourly']= Precip['Timu1'].resample('H',how='sum')
    #Precip['Timu1hourly'].dropna().to_csv(datadir+'OUTPUT/Timu1hourly.csv',header=['Timu1hourly'])
    # Daily
    Precip['Timu1daily'] = Precip['Timu1'].resample('D',how='sum')
    #Precip['Timu1daily'].dropna().to_csv(datadir+'OUTPUT/Timu1daily.csv',header=['Timu1daily'])
    # Monthly
    Precip['Timu1monthly'] = Precip['Timu1'].resample('MS',how='sum') ## Monthly Precip
    #Precip['Timu1monthly'].dropna().to_csv(datadir+'OUTPUT/Timu1monthly.csv',header=['Timu1monthly'])
    ## Timu-Fagaalu2 (up on Blunt's Point Ridge; only deployed for 2 months in 2012)
    Precip['Timu2-30']=raingauge(XL,'Timu-Fagaalu2',180).resample('30Min',how='sum')
    # Hourly
    Precip['Timu2hourly']= Precip['Timu2-30'].resample('H',how='sum')
    #Precip['Timu2hourly'].dropna().to_csv(datadir+'OUTPUT/Timu2hourly.csv',header=['Timu2hourly'])
    # Daily
    Precip['Timu2daily'] = Precip['Timu2-30'].resample('D',how='sum')
    #Precip['Timu2daily'].dropna().to_csv(datadir+'OUTPUT/Timu2daily.csv',header=['Timu2daily'])
    # Monthly
    Precip['Timu2monthly'] = Precip['Timu2-30'].resample('MS',how='sum') ## Monthly Precip
    #Precip['Timu2monthly'].dropna().to_csv(datadir+'OUTPUT/Timu2monthly.csv',header=['Timu2monthly'])


#### Import WX STATION Data
#from load_from_MASTER_XL import WeatherStation
def WeatherStation(XL,sheet=''):
    print 'loading Wx: '+sheet+'...'
    ## Fagaalu Weather Station
    #my_parser= lambda x,y: dt.datetime.strptime(x+y,"%m/%d/%Y%I:%M %p")
    Wx= XL.parse(sheet,skiprows=1,header=0,parse_cols='A:AD',parse_dates=[['Date','Time']],index_col=['Date_Time'],na_values=['---'])
    Wx.columns=['TempOut', 'HiTemp', 'LowTemp', 'OutHum', 'DewPt', 'WindSpeed', 'WindDir', 'WindRun', 'HiSpeed', 'HiDir', 'WindChill', 'HeatIndex', 'THWIndex', 'Bar', 'Rain', 'RainRate', 'HeatD-D', 'CoolD-D', 'InTemp', 'InHum', 'InDew', 'InHeat', 'InEMC', 'InAirDensity', 'WindSamp', 'WindTx', 'ISSRecept', 'Arc.Int.']
    return Wx
    
if 'FP' not in locals():
    print 'Opening Weather Station data...'
    FPa = WeatherStation(XL,'FP-30min')
    Bar15Min=FPa['Bar'].resample('15Min',fill_method='pad',limit=2) ## fill the 30min Barometric intervals to 15minute, but not Precip!
    FPa = FPa.resample('15Min')
    FPa['Bar']=Bar15Min
    FPb = WeatherStation(XL,'FP-15min')
    FP = FPa.append(FPb)

Precip['FPrain']=FP['Rain'] ## mm?
Precip['FPrain']
Precip['FPrain-30']=Precip['FPrain'].resample('30Min',how=sum)
Precip['FPhourly'] = Precip['FPrain'].resample('H',how='sum') ## label=left?? 
Precip['FPdaily'] = Precip['FPrain'].resample('D',how='sum')
Precip['FPmonthly'] = Precip['FPrain'].resample('MS',how='sum')

#Precip['FPhourly'].dropna().to_csv(datadir+'OUTPUT/FPhourly.csv',header=['FPhourly'])
#Precip['FPdaily'].dropna().to_csv(datadir+'OUTPUT/FPdaily.csv',header=['FPdaily'])
#Precip['FPmonthly'].dropna().to_csv(datadir+'OUTPUT/FPmonthly.csv',header=['FPmonthly'])

## Filled Precipitation record, priority = Timu1, fill with FPrain
PrecipFilled=pd.DataFrame(pd.concat([Precip['Timu1-15'][dt.datetime(2012,1,6,17,51):dt.datetime(2012,1,6,23,59)], Precip['FPrain'][dt.datetime(2012,1,7,0,0):dt.datetime(2012,1,20,23,59)], Precip['Timu1-15'][dt.datetime(2012,1,21,0,0):dt.datetime(2013,2,8,0,0)], Precip['FPrain'][dt.datetime(2013,2,8,0,15):dt.datetime(2013,3,12,0,0)], Precip['Timu1-15'][dt.datetime(2013,3,12,0,15):dt.datetime(2013,3,24,0,0)], Precip['FPrain'][dt.datetime(2013,3,24,0,15):dt.datetime(2013,5,1,0,0)],Precip['Timu1-15'][dt.datetime(2013,5,1,0,15):dt.datetime(2014,1,8,0,0)], Precip['Timu1-15'][dt.datetime(2014,1,14,0,0):dt.datetime(2014,12,31,23,59)] ]),columns=['Precip']).dropna()

#PrecipFilled = PrecipFilled.reindex(pd.date_range(dt.datetime(2012,1,7),dt.datetime(2014,12,31),freq='15Min'))


#### Import BAROMETRIC Data: NDBC

##load data from NDBC NSTP6 station at DMWR, Pago Harbor
## To get more NSTP6 data either go to their website and copy and paste the historical data
## or use wundergrabber_NSTP6-REALTIME.py and copy and paste frome the .csv
def ndbc(datafile = watershed_datadir+'BARO/NSTP6/NSTP6-2012-14.xlsx'):
    print 'Loading NDBC NSTP6 barometric data...'
    try:
        ndbc_data = pd.DataFrame.from_csv(watershed_datadir+'BARO/NSTP6/NDBC_Baro.csv')
    except:
        ndbcXL = pd.ExcelFile(datafile)
        ndbc_parse = lambda yr,mo,dy,hr,mn: dt.datetime(yr,mo,dy,hr,mn)
        ndbc_data = ndbcXL.parse('NSTP6-2012-14',header=0,skiprows=1,parse_dates=[['#yr','mo','dy','hr','mn']],index_col=0,date_parser=ndbc_parse,na_values=['9999','999','99','99.0'])
        #ndbc_data.to_csv(datadir+'BARO/NSTP6/NDBC_Baro.csv')
    #local = pytz.timezone('US/Samoa')
    #ndbc_data.index = ndbc_data.index.tz_localize(pytz.utc).tz_convert(local)
    print 'NDBC loaded'
    return ndbc_data

NDBCbaro = ndbc(datafile = watershed_datadir+'BARO/NSTP6/NSTP6-2012-14.xlsx')
NDBCbaro = NDBCbaro['hPa'].resample('15Min')
NDBCbaro = NDBCbaro.interpolate(method='linear',limit=4)
NDBCbaro.columns=['NDBCbaro']
NDBCbaro=NDBCbaro.shift(-44) ## UTC to Samoa local  =11 hours =44x15min
NDBCbaro = NDBCbaro-.022

## Barologger at  LBJ
def barologger(XL,sheet=''):
    print 'loading Wx: '+sheet+'...'
    ## Fagaalu Weather Station
    #my_parser= lambda x,y: dt.datetime.strptime(x+y,"%m/%d/%Y%I:%M %p")
    Baro=  XL.parse(sheet,header=11,parse_cols='A,B,D',parse_dates=[['Date','Time']],index_col=['Date_Time'])
    Baro.columns= ['LEVEL']
    Baro=Baro.resample('15Min',how='mean')
    return Baro
    
BaroLogger = barologger(XL,'Fagaalu1-Barologger')
 
## Build data frame of barometric data: Make column 'baropress' with best available data
 ## Fill priority = FP,NDBC,TAFUNA,TULA (TAFUNA and TULA have been deprecated, reside in other scripts)
allbaro = pd.DataFrame(NDBCbaro/10).reindex(pd.date_range(start2012,stop2015,freq='15Min'))
allbaro['FPbaro']=FP['Bar']/10
allbaro['NDBCbaro']=NDBCbaro/10
allbaro['BaroLogger']=BaroLogger

## create a new column and fill with FP or Barologger
allbaro['Baropress']=allbaro['FPbaro'].where(allbaro['FPbaro']>0,allbaro['BaroLogger']) 
## create a new column and fill with FP or NDBC
allbaro['Baropress']=allbaro['Baropress'].where(allbaro['Baropress']>0,allbaro['NDBCbaro']) 


#### Import PT Data
# ex. PT_Levelogger(allbaro,PTname,datapath,tshift=0,zshift=0): 
#from load_from_MASTER_XL import PT_Hobo,PT_Levelogger
def PT_Hobo(allbaro,PTname,XL,sheet='',tshift=0,zshift=0): # tshift in 15Min(or whatever the timestep is), zshift in cm
    print 'loading HOBO PT: '+sheet+'...'
    PT = XL.parse(sheet,header=1,index_col=0,parse_cols='B,C',parse_dates=True)
    PT.columns=['Pressure']
    PT=PT.resample('15Min',how='mean')
    PT=PT.shift(tshift) ## shift by 3 hours (12 x 15minutes)
    PT['barodata']=allbaro['Baropress']
    PT['stage(cm)']=(PT['Pressure']-PT['barodata'])*.102*100.0 ## hPa  to cm
    #PT['stage']=PT['stage'].where(PT['stage']>0,PT['barodata']) ## filter negative values
    PT['stage(cm)']=PT['stage(cm)'].round(1)  
    PT['stage(cm)']=PT['stage(cm)']+zshift
    PT['Uncorrected_stage']=PT['stage(cm)'].round(0)
    return PT

def PT_Levelogger(allbaro,PTname,XL,sheet,tshift=0,zshift=0): # tshift in hours, zshift in cm
    print 'loading Levelogger PT: '+sheet+'...'
    PT = XL.parse(sheet,header=11,parse_cols='A,B,D',parse_dates=[['Date','Time']],index_col=['Date_Time'])
    PT.columns= ['LEVEL']
    PT=PT.resample('15Min',how='mean')
    PT['barodata']=allbaro['Baropress']
    PT=PT.shift(tshift) ## shift by 3 hours (12 x 15minutes)
    PT['stage(cm)']=(PT['LEVEL']-PT['barodata'])*.102*100.0
    #PT['stage']=PT['stage'].where(PT['stage']>0,0) ## filter negative values
    PT['stage(cm)']=PT['stage(cm)'].round(1)  
    PT['stage(cm)']=PT['stage(cm)']+zshift
    PT['Uncorrected_stage']=PT['stage(cm)'].round(0)
    return PT
    
## PT1 LBJ
# tshift in 15Min(or whatever the timestep is), zshift in cm
PT1aa = PT_Hobo(allbaro,'PT1 LBJ bridge',XL,'PT-Fagaalu1aa',tshift=12) #12 x 15min = 3hours (It says it was at GMT-8 instead of GMT-11 but the logger time was set to local anyway)
PT1ab = PT_Hobo(allbaro,'PT1 LBJ bridge',XL,'PT-Fagaalu1ab',tshift=12) #12 x 15min = 3hours (It says it was at GMT-8 instead of GMT-11 but the logger time was set to local anyway)
PT1ba = PT_Hobo(allbaro,'PT1 LBJ bridge',XL,'PT-Fagaalu1ba',tshift=4)
PT1bb = PT_Hobo(allbaro,'PT1 LBJ bridge',XL,'PT-Fagaalu1bb',tshift=4)
PT1bc = PT_Hobo(allbaro,'PT1 LBJ bridge',XL,'PT-Fagaalu1bc',tshift=4)
PT1ca = PT_Hobo(allbaro,'PT1 LBJ bridge',XL,'PT-Fagaalu1ca').truncate(after= dt.datetime(2014,9,23))
PT1cb = PT_Hobo(allbaro,'PT1 LBJ bridge',XL,'PT-Fagaalu1cb')
PT1cc = PT_Hobo(allbaro,'PT1 LBJ bridge',XL,'PT-Fagaalu1cc')

PT1 = pd.concat([PT1aa,PT1ab,PT1ba,PT1bb,PT1bc,PT1ca,PT1cb,PT1cc])

#rawPT1XL = pd.ExcelFile(datadir+'PT-Fagaalu1-raw.xlsx') 
#rawPT1=pd.DataFrame()
#for sheet_name in rawPT1XL.sheet_names:
#    #print sheet_name
#    sheet = rawPT1XL.parse(sheet_name,header=1,index_col=0,parse_cols='B,C',parse_dates=True)
#    sheet.columns=['Pressure']
#    rawPT1 = rawPT1.append(sheet)


PT1 = PT1.reindex(pd.date_range(start2012,stop2015,freq='15Min'))

def plot_uncorrected_stage_data(show=False):
    fig, (baro,pt1,t) = plt.subplots(3,sharex=True,sharey=False,figsize=(12,8))
    for ax in [baro,pt1]:
        ax.xaxis.set_visible(False)
    allbaro['Baropress'].plot(ax=baro,c='k',label='Barometric Pressure (kPa)')
    allbaro['Baropress'].plot(ax=t,c='k',label='Barometric Pressure (kPa)')
    baro.legend()
    ## PT1 at LBJ
    PT1list = [PT1aa,PT1ab,PT1ba,PT1bb,PT1bc,PT1ca,PT1cb,PT1cc]
    count = 0
    count_dict = {1:'aa',2:'ab',3:'ba',4:'bb',5:'bc',6:'ca',7:'cb',8:'cc'}
    for PT in PT1list:
        count+=1
        try:
            PT['Pressure'].plot(ax=pt1,c=np.random.rand(3,1),label='PT1'+count_dict[count])
            PT['Pressure'].plot(ax=t,c=np.random.rand(3,1),label='PT1'+count_dict[count])
        except KeyError:
            PT['LEVEL'].plot(ax=pt1,c=np.random.rand(3,1),label='PT1'+count_dict[count])
            PT['LEVEL'].plot(ax=t,c=np.random.rand(3,1),label='PT1'+count_dict[count])
    pt1.legend()
    
    t.legend(ncol=2)
    
    if show==True:
        plt.tight_layout(pad=0.1)
        plt.show()
    return
#plot_uncorrected_stage_data(show=True)
    
    
    
## BAROMETRIC PRESSURE DATA FROM DIFFERENT SOURCES
## WITH PRESSURE FROM PT (MAKE SURE THEY'RE IN SYNC)
## Not sure what the difference plot is for....
def plot_barometric_pressure():   
    fig, (baro, pt, diff) = plt.subplots(3,1,sharex=True)
    ## Barometric Data
    allbaro['Baropress'].plot(ax=baro,c='k', label='Barometric Pressure (kPa)')
    allbaro['NDBCbaro'].plot(ax=baro,c='r', label='NDBC NSTP6')
    allbaro['FPbaro'].plot(ax=baro,c='g', label='Weather Station')
    ## PT Data
    PT1['Pressure'].plot(ax=baro,c='b', label='LBJ PT Pressure')
    PT1['stage(cm)'].plot(ax=pt,c='b', label='LBJ PT Stage(cm)')
    ## Difference between PT pressure and Barometric pressure at low stages
    press_diff_baseflow = PT1['Pressure'][PT1['stage(cm)']<10]-PT1['barodata']
    m.rolling_mean(press_diff_baseflow,window=96).plot(ax=diff, label='Daily Mean difference kPa (PT-Baro)') ## 96 * 15min = 24 hours
    
    baro.legend(), pt.legend(), diff.legend()
    return
#plot_barometric_pressure()

    

def correct_Stage_data(Stage_Correction_XL,location,PTdata):
    print 'Correcting stage for '+location
    def my_parser(x,y):
        try:
            y = str(int(y))
            hour=y[:-2]
            minute=y[-2:]
            time=dt.time(int(hour),int(minute))
        except:
            time=dt.time(0,0)
        parsed=dt.datetime.combine(x,time)
        #print parsed
        return parsed
    Stage_Correction = Stage_Correction_XL.parse(location,parse_dates=False)
    Correction=pd.DataFrame()
    for correction in Stage_Correction.iterrows():
        t1_date = correction[1]['T1_date']
        t1_time = correction[1]['T1_time']
        t1 = my_parser(t1_date,t1_time)
        t2_date = correction[1]['T2_date']
        t2_time = correction[1]['T2_time']
        t2 = my_parser(t2_date,t2_time)
        z = correction[1]['z']    
        print t1,t2, z
        Correction = Correction.append(pd.DataFrame({'z':z},index=pd.date_range(t1,t2,freq='15Min')))
    Correction = Correction.reindex(pd.date_range(start2012,stop2014,freq='15Min'))
    PTdata['Manual_Correction'] = Correction['z']
    PTdata['stage_corrected_Manual'] = PTdata['Uncorrected_stage']+PTdata['Manual_Correction']
    PTdata['stage(cm)']=PTdata['stage_corrected_Manual'].where(PTdata['stage_corrected_Manual']>0,PTdata['stage(cm)'])#.round(0)
    return PTdata
Stage_Correction_XL = pd.ExcelFile(watershed_datadir+'Q/StageCorrection.xlsx')    
PT1 = correct_Stage_data(Stage_Correction_XL,'LBJ',PT1)


## STAGE DATA FOR PT's
#### FINAL STAGE DATA with CORRECTIONS
Fagaalu_stage_data = pd.DataFrame({'LBJ':PT1['stage(cm)']})
Fagaalu_stage_data = Fagaalu_stage_data.reindex(pd.date_range(start2012,stop2015,freq='15Min'))


#### STAGE TO DISCHARGE ####
#from stage2discharge_ratingcurve import AV_RatingCurve#, calcQ, Mannings_rect, Weir_rect, Weir_vnotch, Flume


### Calculate Q from a single AV measurement
#fileQ = calcQ(datadir+'Q/LBJ_4-18-13.txt','LBJ',Fagaalu_stage_data,slope=Slope,Mannings_n=n,trapezoid=True)
## and save to CSV
#pd.concat(fileQ).to_csv(datadir+'Q/LBJ_4-18-13.csv')

### Area Velocity and Mannings from in situ measurments
## Returns DataFrame of Stage (cm) and Discharge (L/sec) calc. from AV measurements with time index

def Stage_Q_AV_RatingCurve(path,location,stage_data,slope=.01,Mannings_n=.033,trapezoid=True,printResults=False):
    Filelist = os.listdir(path)
    ## iterate over files in directory to get Flow.txt file
    for f in Filelist:
        ## Select Flow.txt file
        if f.endswith('Flow.txt')==True and f.startswith(location)==True:
            print 'AV measurements file selected for analysis: '+f
            ## Open File, create blank parameters
            Flowfile = open(path+f)
            Qdf = pd.DataFrame() ## empty dataframe to append calculated Q
            for line in Flowfile:
                split = line.strip('\n').split('\t')
                #print split
                # Test if data is number
                try:
                    a= float(split[0]) ## dummy test
                    isfloat=True
                except ValueError:
                    isfloat=False            
                ## Determine DateTime of AV measurment
                if split[0]==location:
                    ## Create empty dataframe
                    df = pd.DataFrame(columns=['dist','depth','flow']) ## empty dataframe for Flowmeter data
                    date, time = split[1].split('/'),split[2]
                    if len(time)==3:
                        time = '0'+time
                    DateTime = dt.datetime(int(date[2]),int(date[0]),int(date[1]),int(time[0:2]),int(time[2:]))
                    DateTime = RoundTo15(DateTime)
                    #print DateTime
                ## Append data
                elif isfloat==True:
                    df=df.append(pd.DataFrame({'dist':split[0],'depth':split[1],'flow':split[2]},index=[DateTime]))
                elif split[0]=='Location' or split[0]=='Field Measurements' or split[0]=='Dist(S to N)(ft)' or split[0]=='Dist(ft)':
                    pass
                
                ## At the end of that AV measurment, calculate Q
                elif split[0]=='-':
                    #print 'calculating Q for '+str(DateTime)
                    df = df.astype('float')
                    if trapezoid==True:
                        ## Depth/flow measurements are made at the midpoint of the trapezoid, dimensions of the trapezoid have to be determined
                        df['right']= df['dist'].shift(-1).sub(df['dist'],fill_value=0) ##Distance next - Distance = the width to the right
                        df['left'] = df['dist'].sub(df['dist'].shift(1),fill_value=0) ## Distance previous - Distance = the width to the left
                        df['right'] = df['right'].where(df['right']>0,0)
                        df['width']=((df['right'] + df['left'])/2)*12*2.54 ## 2nd mark - first; then convert to cm
                        df['b1']=(df['depth'].add(df['depth'].shift(1),fill_value=0))/2 ## gives average of Depth Above and depth
                        df['b2']=(df['depth'].add(df['depth'].shift(-1),fill_value=0))/2 ## gives average of Depth Below and depth
                        df['trapezoidal-area']=.5*(df['b1']+df['b2'])*df['width'] ## Formula for area of a trapezoid = 1/2 * (B1+B2) * h; h is width of the interval and B1 and B2 are the depths at the midpoints between depth/flow measurements
                        df['trapezoidal-area']=df['trapezoidal-area']/10000 ##cm2 to m2
                        df['AV']=df['trapezoidal-area']*df['flow'] *1000 ## m2 x m/sec x 1000 = L/sec
                        AV_Q = df['AV'].sum()
                        Area = df['trapezoidal-area'].sum()
                        V = df['flow'].mean()
                        ## Wetted perimeter doesn't use midpoints between depth/flow measurments
                        df['WP']=  ((df['depth'].sub(df['depth'].shift(1),fill_value=0))**2 + (df['dist'].sub(df['dist'].shift(1),fill_value=0)*12*2.54)**2)**0.5 ## WP = SQRT((Dnext-D)^2 + Width^2)
                        df['WP']=(df['WP']*(df['b1']>0))/100 ## cm to m; and only take WP values where the depth to the left is not zero
                        
                        WP = df['WP'].sum()
                        R = (df['trapezoidal-area'].sum())/(df['WP'].sum()) ## m2/m = m
                        ## Mannings = (1R^2/3 * S^1/2)/n
                        S = slope
                        ## Jarrett (1990) equation for n
                        ## n = 0.32*(S**0.30)*(R**-0.16)
                        if Mannings_n == 'Jarrett':
                            n = 0.32*(S**0.30)*(R**-0.16)
                        else:
                            n = Mannings_n
                        ManningV = (1*(R**(2.0/3.0))*(S**0.5))/n
                        ManningQ = ManningV * df['trapezoidal-area'].sum() * 1000 ## L/Sec
                    elif trapezoid==False:
                        df = df.set_value(len(df),'dist',df['dist'][-1]) ## add a dummy distance value
                        valbelow = df['dist'].shift(-1).sub(df['dist'],fill_value=0) ## Width is value below - dist value
                        valabove = df['dist'].sub(df['dist'].shift(1),fill_value=0)
                        df['width']=(valbelow.add(valabove)/2)*12*2.54 ## 2nd mark - first
                        df['rectangular-area']=df['depth']*(df['width'])/10000 ##cm2 to m2
                        df['AV']=df['rectangular-area']*df['flow']
                        
                        AV_Q = df['AV'].sum().round(0)
                        Area = df['rectangular-area'].sum()
                        V = df['flow'].mean()
                        ManningV = np.nan
                    try:
                        stage = stage_data[location].ix[DateTime] ## Get Stage data
                        print location+' '+str(DateTime)+' '+'Stage= '+str(stage)+' Q= '+str(AV_Q)
                    except:
                        stage =np.nan
                        print location+' '+str(DateTime)+' '+'Stage= '+str(stage)+' Q= '+str(AV_Q)
                    Qdf = Qdf.append(pd.DataFrame({'stage(cm)':stage,'Q-AV(L/sec)':round(AV_Q,0),'Q-AManningV(L/sec)':round(ManningQ,0),
                    'Area(m2)':Area,'V(m/s)':V,'ManningV(m/s)':ManningV,'WP':WP,'R':R},index=[DateTime]))
                    
                    if printResults==True:                    
                        print str(DateTime)+': stage='+'%.2f'%stage+' Q= '+'%.0f'%AV_Q+' ManningQ= '+'%.2f'%ManningQ
                        print df              
    return Qdf  
#Stage_Q_AV_RatingCurve(path,location,stage_data,slope=.01,Mannings_n=.033,trapezoid=True,printResults=False)


### Discharge using Mannings and Surveyed Cros-section
#from ManningsRatingCurve import Mannings, Mannings_Series
def Mannings_Q_from_CrossSection(Cross_section_file,sheetname,Slope,Manning_n,k=1,stage_start=.01,stage_end=None,show=False,save=False,filename=''):    
    ## Open and parse file; drop NA  
    print Cross_section_file+' '+sheetname
    print 'Slope: '+str(Slope)+' Mannings n: '+str(Manning_n)
    XL = pd.ExcelFile(Cross_section_file) 
    df = XL.parse(sheetname,header=4,parse_cols='F:H')
    df = df.dropna()
    ## Mannings Parameters S:slope, n:Mannings n
    S = Slope # m/m
    n= Manning_n
    ## empty lists
    areas, wp, r, Man_n, v, q, = [],[],[],[],[],[]
    ## Stage data
    ## one stage measurement
    if stage_end == None:
        print 'Stage: '+str(stage_start)
        stages = np.array([stage_start])
    ## start and end stage
    elif stage_start != stage_end:
        print 'Stage_start: '+str(stage_start)+' Stage_end: '+str(stage_end)
        stages = np.arange(stage_start,stage_end,.1) #m
    ## stage Series         
    elif type(stage_start)==pd.Series:
        print 'Stage Series...'
        stages = stage_start.to_list()
        
    for stage in stages:
        print 'stage: '+str(stage)
        df['y1'] = df['depth']+df['Rod Reading'].max()
        df['y2'] = stage
        df['z'] = df['y2']-df['y1']
        df['z'] = df['z'][df['z']>=0]
        
        x = df['Dist'].values
        y1 = df['y1'].values
        y2 = df['y2'].values
        
        z = y2-y1
        z= np.where(z>=0,z,0)
        Area = np.trapz(z,x)
        
        ## Wetted Perimeter
        df['dx'] = df['Dist'].sub(df['Dist'].shift(1),fill_value=0)
        df['dy'] = df['z'].sub(df['z'].shift(1),fill_value=0)
        df['wp'] = (df['dx']**2 + df['dy']**2)**0.5
        print df        
        
        WP = df['wp'].sum()
        R = (Area/WP) ## m2/m = m
        ## Jarrett (1990) equation for n
        ## n = 0.32*(S**0.30)*(R**-0.16)
        if Manning_n == 'Jarrett':
            n = 0.32*(S**0.30)*(R**-0.16)
            n= n *k
        ## Mannings = (1R^2/3 * S^1/2)/n
        ManningV = (1*(R**(2.0/3.0))*(S**0.5))/n
        ManningQ = ManningV * Area ## M3/s
        
        plt.ioff()          
        fig, ax1 = plt.subplots(1)
        ax1.plot(df['Dist'],df['y1'],'-o',c='k')
        ax1.fill_between(df['Dist'], df['y1'], stage,where = df['y1']<=stage,alpha=.5, interpolate=True)
        
        ax1.annotate('stage: '+'%.2f'%stage+'m',xy=(0,1.5+.45))
        ax1.annotate('Mannings n: '+'%.3f'%n,xy=(0,1.5+.03))
        ax1.annotate('Area: '+'%.3f'%Area+'m2',xy=(0,1.5+.25))
        ax1.annotate('WP: '+'%.2f'%WP+'m',xy=(df['Dist'].mean(),1.5+.03))
        ax1.annotate('Manning V: '+'%.2f'%ManningV+'m/s ',xy=(df['Dist'].mean(),1.5+.25))
        ax1.annotate('Manning Q: '+'%.3f'%ManningQ+'m3/s',xy=(df['Dist'].mean(),1.5+.45))
        plt.axes().set_aspect('equal')
        plt.xlim(-1,df['Dist'].max()+1),plt.ylim(-1,2 + 1.)
    
        areas.append(Area)
        wp.append(WP)
        r.append(R)
        Man_n.append(n)
        v.append(ManningV)
        q.append(ManningQ)
        show_plot(show,fig)
        savefig(save,filename) 
        plt.close('all')
        plt.ion()
    
    DF = pd.DataFrame({'stage(m)':stages,'area(m2)':areas,'wp(m)':wp,'r':r,'Man_n':Man_n,'vel(m/s)':v,'Q(m3/s)':q}) 
    return DF,df
  
    
def Mannings_Q_from_stage_data(Cross_section_file,sheetname,stage_data,Slope,Manning_n,k=1):    
    ## Open and parse file; drop NA  
    print Cross_section_file+' '+sheetname
    print 'Slope: '+str(Slope)+' Mannings n: '+str(Manning_n)
    XL = pd.ExcelFile(Cross_section_file) 
    df = XL.parse(sheetname,header=4,parse_cols='F:H')
    df = df.dropna()
    ## Mannings Parameters S:slope, n:Mannings n
    S = Slope # m/m
    n= Manning_n
    ## empty lists
    areas, wp, r, Man_n, v, q, = [],[],[],[],[],[]
    ## Stage data
    stage_data = stage_data/100 ## cm to m
    for stage in stage_data.values:
        #print 'stage: '+str(stage)
        df['y1'] = df['depth']+df['Rod Reading'].max()
        df['y2'] = stage
        df['z'] = df['y2']-df['y1']
        df['z'] = df['z'][df['z']>=0]
        x = df['Dist'].values
        y1 = df['y1'].values
        y2 = df['y2'].values
        z = y2-y1
        z= np.where(z>=0,z,0)
        Area = np.trapz(z,x)
        ## Wetted Perimeter0.01
        df['dx'] =df['Dist'].sub(df['Dist'].shift(1),fill_value=0)
        df['dy'] = df['z'].sub(df['z'].shift(1),fill_value=0)
        df['wp'] = (df['dx']**2 + df['dy']**2)**0.5
        WP = df['wp'].sum()
        R = (Area/WP) ## m2/m = m
        ## Jarrett (1990) equation for n
        ## n = 0.32*(S**0.30)*(R**-0.16)
        if Manning_n == 'Jarrett':
            n = 0.32*(S**0.30)*(R**-0.16) 
            n = n * k
        ## Mannings = (1R^2/3 * S^1/2)/n
        ManningV = (1*(R**(2.0/3.0))*(S**0.5))/n
        ManningQ = ManningV * Area ## M3/s
        ManningQ= round(ManningQ,3)
        areas.append(Area)
        wp.append(WP)
        r.append(R)
        Man_n.append(n)
        v.append(ManningV)
        q.append(ManningQ)        
    DF = pd.DataFrame({'stage(m)':stage_data.values,'area(m2)':areas,'wp(m)':wp,'r':r,'Man_n':Man_n,'vel(m/s)':v,'Q(m3/s)':q},index=stage_data.index)
    return DF
    
## Read LBJ_Man Discharge from .csv, or calculate new if needed
if 'LBJ_Man' not in locals():
    try:
        print 'Loading Mannings Q for DAM from CSV'
        LBJ_Man_reduced = pd.DataFrame.from_csv(datadir+'Q/Manning_Q_files/LBJ_Q from Mannings_reduced.csv')
        LBJ_Man = pd.DataFrame.from_csv(datadir+'Q/Manning_Q_files/LBJ_Q from Mannings.csv')
    except:
        print 'Calculate Mannings Q for LBJ and saving to CSV'
        LBJ_S, LBJ_n, LBJ_k = 0.016, 'Jarrett', .06/.08
        LBJ_S, LBJ_n, LBJ_k = 0.016, .067, 1
        LBJ_stage_reduced = Fagaalu_stage_data['LBJ'].dropna().round(0).drop_duplicates().order()
        LBJ_Man_reduced = Mannings_Q_from_stage_data(watershed_datadir+'Q/Cross_Section_Surveys/LBJ_cross_section.xlsx','LBJ_m',Slope=LBJ_S,Manning_n=LBJ_n,k=LBJ_k,stage_data=LBJ_stage_reduced)
        LBJ_Man_reduced.to_csv(watershed_datadir+'Q/Manning_Q_files/LBJ_Q from Mannings_reduced.csv')
        LBJ_stage= Fagaalu_stage_data['LBJ']+5
        LBJ_Man= Mannings_Q_from_stage_data(watershed_datadir+'Q/Cross_Section_Surveys/LBJ_cross_section.xlsx','LBJ_m',Slope=LBJ_S,Manning_n=LBJ_n,k=LBJ_k,stage_data=LBJ_stage)
        LBJ_Man.to_csv(watershed_datadir+'Q/Manning_Q_files/LBJ_Q from Mannings.csv')
        pass
    

#### LBJ Stage-Discharge
# (3 rating curves: AV measurements, A measurement * Mannings V, Surveyed Cross-Section and Manning's equation)

## LBJ AV measurements
## Mannings parameters for A-ManningV
Slope = 0.0161 # m/m
LBJ_n=0.067 # Mountain stream rocky bed and rivers with variable sections and veg along banks (Dunne 1978)

#DataFrame with Q from AV measurements, Q from measured A with Manning-predicted V, stage, and Q from Manning's and assumed rectangular channel
LBJstageDischarge = Stage_Q_AV_RatingCurve(watershed_datadir+'Q/Flow_Files/','LBJ',Fagaalu_stage_data,slope=Slope,Mannings_n=LBJ_n,trapezoid=True).dropna() 
LBJstageDischarge = LBJstageDischarge.truncate(before=datetime.datetime(2012,3,20)) # throw out measurements when I didn't know how to use the flowmeter 
LBJstageDischargeLog = LBJstageDischarge.apply(np.log10) #log-transformed version

## LBJ: Discharge Ratings
## Linear
LBJ_AV= pd.ols(y=LBJstageDischarge['Q-AV(L/sec)'],x=LBJstageDischarge['stage(cm)'],intercept=True) 
## Power
LBJ_AVLog= pd.ols(y=LBJstageDischargeLog['Q-AV(L/sec)'],x=LBJstageDischargeLog['stage(cm)'],intercept=True) #linear fit to log-transformed stage and Q
## Linear with Mannings and measured Area
LBJ_AManningV = pd.ols(y=LBJstageDischarge['Q-AManningV(L/sec)'],x=LBJstageDischarge['stage(cm)'],intercept=True)
## Power with Mannings and measured Area
LBJ_AManningVLog = pd.ols(y=LBJstageDischargeLog['Q-AManningV(L/sec)'],x=LBJstageDischargeLog['stage(cm)'],intercept=True)


## This function calculates the coeff of determination (r2) for 
## a function (=Manning's rating curve) and some independent points (=AV Q measurements
def Manning_AV_r2(ManningsQ_Series,AV_Series):
    # LBJ Mannings = y predicted
    ManQ, Manstage = ManningsQ_Series['Q(m3/s)']*1000, ManningsQ_Series['stage(m)']*100
    y_predicted = pd.DataFrame({'Q_Man':ManQ.values},index=Manstage).sort()
    ## LBJ AV  = y
    AV_Q, AVstage = AV_Series['Q-AV(L/sec)'], AV_Series['stage(cm)'].apply(np.int)
    y_ = pd.DataFrame({'Q_AV':AV_Q.values},index=AVstage).sort()
    y_['Q_Man'] = y_predicted
    y_=  y_.dropna() # keep it clean
    
    y_bar = y_['Q_AV'].mean()
    y_var = (y_['Q_AV'] - y_bar)**2.
    ss_tot = y_var.sum()
    y_res = (y_['Q_AV']-y_['Q_Man'])**2.
    ss_res = y_res.sum()
    r2 = 1-(ss_res/ss_tot)
    return  r2
LBJ_Man_r2 = Manning_AV_r2(LBJ_Man_reduced,LBJstageDischarge)


def Manning_AV_rmse(Man_Series,AV_Series):
    # LBJ Mannings = y predicted
    ManQ, Manstage = Man_Series['Q(m3/s)']*1000, Man_Series['stage(m)']*100
    y_predicted = pd.DataFrame({'Q_Man':ManQ.values},index=Manstage).sort()
    ## LBJ AV  = y
    AV_Q, AVstage = AV_Series['Q-AV(L/sec)'], AV_Series['stage(cm)'].apply(np.int)
    y_ = pd.DataFrame({'Q_AV':AV_Q.values},index=AVstage).sort()
    y_['Q_Man'] = y_predicted
    y_=  y_.dropna() # keep it 
    y_['Q_diff'] = y_['Q_AV'] - y_['Q_Man']
    y_['Q_diff_squared'] = (y_['Q_diff'])**2.
    y_rmse = (y_['Q_diff_squared'].sum()/len(y_))**0.5
    
    mean_observed = AV_Q.mean()
    rmse_percent = y_rmse/mean_observed *100.
    return int(y_rmse),int(mean_observed),int(rmse_percent)
LBJ_Man_rmse = Manning_AV_rmse(LBJ_Man_reduced,LBJstageDischarge)[2]


### Compare Discharge Ratings from different methods
def plotQratingLBJ(ms=6,show=False,log=False,save=False,filename=figdir+''): ## Rating Curves
    mpl.rc('lines',markersize=ms)
    title="Water Discharge Ratings for FG3(LBJ)"
    fig, (site_lbj, site_lbj_zoom)= plt.subplots(1,2,figsize=(8,4))
    xy = np.linspace(0,8000,8000)
    site_lbj.text(0.1,0.95,'(a)',verticalalignment='top', horizontalalignment='right',transform=site_lbj.transAxes,color='k',fontsize=10,fontweight='bold')
    site_lbj_zoom.text(0.1,0.95,'(b)',verticalalignment='top', horizontalalignment='right',transform=site_lbj_zoom.transAxes,color='k',fontsize=10,fontweight='bold')
    #LBJ AV Measurements and Rating Curve
    site_lbj.plot(LBJstageDischarge['Q-AV(L/sec)'][start2012:stop2012],LBJstageDischarge['stage(cm)'][start2012:stop2012],'o',color='k',fillstyle='none',label='AV 2012') 
    site_lbj.plot(LBJstageDischarge['Q-AV(L/sec)'][start2013:stop2013],LBJstageDischarge['stage(cm)'][start2013:stop2013],'^',color='k',fillstyle='none',label='AV 2013') 
    site_lbj.plot(LBJstageDischarge['Q-AV(L/sec)'][start2014:stop2014],LBJstageDischarge['stage(cm)'][start2014:stop2014],'s',color='k',fillstyle='none',label='AV 2014') 
    site_lbj_zoom.plot(LBJstageDischarge['Q-AV(L/sec)'][start2012:stop2012],LBJstageDischarge['stage(cm)'][start2012:stop2012],'o',color='k',fillstyle='none',label='AV 2012') 
    site_lbj_zoom.plot(LBJstageDischarge['Q-AV(L/sec)'][start2013:stop2013],LBJstageDischarge['stage(cm)'][start2013:stop2013],'^',color='k',fillstyle='none',label='AV 2013') 
    site_lbj_zoom.plot(LBJstageDischarge['Q-AV(L/sec)'][start2014:stop2014],LBJstageDischarge['stage(cm)'][start2014:stop2014],'s',color='k',fillstyle='none',label='AV 2014') 

    ## LBJ MODELS
    ## Mannings for AV measurements
    #site_lbj.plot(LBJstageDischarge['Q-AManningV(L/sec)'],LBJstageDischarge['stage(cm)'],'.',ls='None',c='grey',label='A-ManningsV')
    #site_lbj_zoom.plot(LBJstageDischarge['Q-AManningV(L/sec)'],LBJstageDischarge['stage(cm)'],'.',ls='None',c='grey',label='A-ManningsV')
    ## LBJ Power
    LBJ_AVpower = powerfunction(LBJstageDischarge['Q-AV(L/sec)'],LBJstageDischarge['stage(cm)'])    
    PowerFit(LBJstageDischarge['Q-AV(L/sec)'],LBJstageDischarge['stage(cm)'],xy,site_lbj,c='grey',ls='-',label='AV power law '+r'$r^2$'+"%.2f"%LBJ_AVpower['r2'])    
    PowerFit(LBJstageDischarge['Q-AV(L/sec)'],LBJstageDischarge['stage(cm)'],xy,site_lbj_zoom,c='grey',ls='-',label='AV power law '+r'$r^2$'+"%.2f"%LBJ_AVpower['r2'])        
    ## LBJ Mannings from stream survey
    LBJ_ManQ, LBJ_Manstage = LBJ_Man_reduced['Q(m3/s)']*1000, LBJ_Man_reduced['stage(m)']*100
    site_lbj.plot(LBJ_ManQ,LBJ_Manstage,'-',markersize=2,c='k',label='Mannings: n='+str(LBJ_n)+r'$ r^2$'+"%.2f"%LBJ_Man_r2)
    site_lbj_zoom.plot(LBJ_ManQ,LBJ_Manstage,'-',markersize=2,c='k',label='Mannings')
    ## Label point -click
    labelindex_subplot(site_lbj, LBJstageDischarge.index,LBJstageDischarge['Q-AV(L/sec)'],LBJstageDischarge['stage(cm)'])
    labelindex_subplot(site_lbj_zoom, LBJstageDischarge.index,LBJstageDischarge['Q-AV(L/sec)'],LBJstageDischarge['stage(cm)'])
    ## Label subplots    
    site_lbj.set_ylabel('Stage(cm)'),site_lbj.set_xlabel('Q(L/sec)'),site_lbj_zoom.set_xlabel('Q(L/sec)')
    ## Format subplots
    site_lbj.set_ylim(0,PT1['stage(cm)'].max()+10)#,site_lbj.set_xlim(0,LBJ_AVnonLinear(PT1['stage'].max()+10))
    site_lbj_zoom.set_ylim(0,45), site_lbj_zoom.set_xlim(0,1600)
    ## Legends
    site_lbj.legend(loc='lower right',fancybox=True)  
    ## Figure title
    #plt.suptitle(title,fontsize=16)
    fig.canvas.manager.set_window_title('Figure : '+title) 
    logaxes(log,fig)
    for ax in fig.axes:
        ax.autoscale_view(True,True,True)
    plt.tight_layout(pad=0.1)
    show_plot(show,fig)
    savefig(save,filename)
    return
#plotQratingLBJ(ms=6,show=True,log=False,save=True,filename=figdir+'LBJ stage Q rating')
#plotQratingLBJ(ms=6,show=True,log=True,save=False,filename=figdir+'')


#### CALCULATE DISCHARGE
## Calculate Q for LBJ
## Stage
LBJ = DataFrame(PT1,columns=['stage(cm)']) ## Build DataFrame with all stage records for location (cm)
## Mannings
LBJ['Q-Mannings'] = LBJ_Man['Q(m3/s)']*1000
## Power Models
a,b = 10**LBJ_AVLog.beta[1], LBJ_AVLog.beta[0]# beta[1] is the intercept = log10(a), so a = 10**beta[1] # beta[0] is the slope = b
LBJ['Q-AVLog'] = a * (LBJ['stage(cm)']**b)
a,b = 10**LBJ_AManningVLog.beta[1], LBJ_AManningVLog.beta[0]
LBJ['Q-AManningVLog'] = a*(LBJ['stage(cm)']**b)


#### CHOOSE Q RATING CURVE
LBJ['Q']= LBJ['Q-Mannings']
LBJ['Q-RMSE'] = LBJ_Man_rmse
print 'LBJ Q from Mannings and Surveyed Cross Section'

## Convert to 15min interval LBJ
LBJq = (LBJ*900) ## Q above is in L/sec; L/sec * 900sec/15Min = L/15Min
LBJq['stage(cm)']=PT1['stage(cm)'] ## put unaltered stage back in


### Plot Q 
def plot_Q_by_year(log=False,show=False,save=False,filename=''):
    mpl.rc('lines',markersize=6)
    fig, (Q2012,Q2013,Q2014,Q2015)=plt.subplots(4)
    letter_subplots(fig,0.1,0.95,'top','right','k',font_size=10,font_weight='bold')
    
    for ax in fig.axes:
        ax.plot_date(LBJ['Q'].index,LBJ['Q'],ls='-',marker='None',c='k',label='Q FG3')
        #ax.plot(LBJstageDischarge.index,LBJstageDischarge['Q-AV(L/sec)'],ls='None',marker='o',color='k')
        ax.set_ylim(0,LBJ['Q'].max()+500)  
    
    Q2014.axvline(study_start), Q2015.axvline(study_end)  
    Q2012.set_xlim(start2012,stop2012),Q2013.set_xlim(start2013,stop2013)
    Q2014.set_xlim(start2014,stop2014),Q2015.set_xlim(start2015,stop2015)
    Q2012.legend(loc='best')
    Q2013.set_ylabel('Discharge (Q) L/sec')
    #Q2012.set_title("Discharge (Q) L/sec at the Upstream and Downstream Sites, Faga'alu")
    
    for ax in fig.axes:
        ax.locator_params(nbins=6,axis='y')
        ax.xaxis.set_major_locator(mpl.dates.MonthLocator(interval=2))
        ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%b %Y'))
        
    plt.tight_layout(pad=0.1)
    logaxes(log,fig)
    show_plot(show,fig)
    savefig(save,filename)
    return
plot_Q_by_year(log=False,show=True,save=False,filename='')


#### Separate Storm Hydrographs - Define storm start/end
#### Baseflow Separation


def Separate_Storms_by_Baseflow(Q_data):
    ## convert to R Data Frame
    hydrograph = com.convert_to_r_dataframe(pd.DataFrame({'Q':Q_data['Q'].values},index = Q_data['Q'].index))
    ## Send to R
    ro.globalenv['flowdata'] = hydrograph
    ## replace blanks with NA
    ro.r('flowdata[flowdata==""]<-NA')
    ## Drop NA rows from Data Frame
    ro.r('flow = flowdata[complete.cases(flowdata),]')
    ## run Baseflow Separation
    ro.r("library(EcoHydRology)")
    print 'running R baseflow separation....'
    ro.r("base = BaseflowSeparation(flow, filter_parameter = 0.95, passes=3)")
    print 'baseflow separated!'
    ## Convert back to Pandas
    flowdf = com.load_data("base")
    ## reindex with the original time index WITHOUT NA's (they're dropped in the R code)
    flow = pd.DataFrame({'Flow':Q_data['Q'].dropna().values,'bt':flowdf['bt'].values,'qft':flowdf['qft'].values},index=Q_data['Q'].dropna().index)
    
    ## optional threshold argument
    stormthresh = 0
    StormFlow = flow['qft'].where(flow['qft']>flow['bt']*0.10)
    ##returns list of data points that meet the condition, the rest are NaN (same shape as original array)
    ## or
    #PT1storm = PT1[PT1>stormthresh] ## NaN values are filtered out
    minimum_length = 4
    #### Get start and end times of events that meet >=stormthresh
    startstops=[]
    dprev = nan ## set first datapoint as NaN
    for d in StormFlow.iteritems():
        if isnan(d[1])==False and isnan(dprev)==True: ### Start of storm
            starttime = d[0]
            endtime = d[0]
            dprev = d[1]
        elif isnan(d[1])==False and isnan(dprev)==False:## Next value in storm
            endtime = d[0]
            dprev = d[1]
        elif isnan(d[1])==True and isnan(dprev)==False: ## Start of non-storm 
            startstops.append((starttime,endtime))
            dprev = d[1]
            pass
        elif isnan(d[1])==True and isnan(dprev)==True: ## Next value in non-storm
            dprev = d[1]
            pass
    #### Slice hydrograph by start:stop times and give count and summary
    eventlist = []
    for t in startstops:
        ## Adjust start of storm by X minutes to capture very start of hydrograph rise
        start = t[0]-dt.timedelta(minutes=15)
        end= t[1]
        event = flow.ix[start:end]
        eventduration = end-start
        seconds = eventduration.total_seconds()
        hours = seconds / 3600
        eventduration = round(hours,2)
        ## Filter out short storms and storms with low Qmax
        if event['qft'].count() >= minimum_length:
            if event['qft'].max()>=100:
                eventlist.append([start,end,eventduration])
        
    StormEvents=pd.DataFrame(eventlist,columns=['start','end','duration (hrs)'])
    #drop_rows = Events[Events['duration (min)'] <= timedelta(minutes=120)] ## Filters events that are too short
    #Events = Events.drop(drop_rows.index) ## Filtered DataFrame of storm start,stop,count,sum
    return StormEvents, flow
    
Storms_LBJ_PT, LBJ_flow_separated = Separate_Storms_by_Baseflow(LBJ)
Storms_LBJ_PT['sep from'] = 'LBJ PT'
LBJ['Q bf'] = LBJ_flow_separated['bt']

All_Storms = Storms_LBJ_PT     
All_Storms = All_Storms.sort('start').reset_index()  



    
def plot_Q_and_StormEvents(Storms_LBJ_PT, LBJ_flow_separated):
    fig, lbj = plt.subplots(1,1,figsize=(10,4))
    ax1 = lbj.twinx()
    ## Precip
    PrecipFilled['Precip'].plot(ax=lbj,color='b',alpha=0.5,ls='steps-pre',label='Timu1')
    lbj.set_ylim(0,25), lbj.set_ylabel('Precip mm')
    ## Q LBJ
    LBJ_flow_separated = LBJ_flow_separated.reindex(pd.date_range(start2012,stop2014,freq='15Min'))
    ax1.plot_date(LBJ_flow_separated.index,LBJ_flow_separated['Flow'],marker='None',ls='-',c='k', label='Q LBJ +15min start')
    ax1.plot_date(LBJ_flow_separated.index,LBJ_flow_separated['bt'],marker='None',ls='-',c='grey')
    ax1.set_ylim(0,LBJ_flow_separated['Flow'].max()+0.05*LBJ_flow_separated['Flow'].max())
    ax1.set_ylabel('Q L/s')
    ax1.legend()
    ## Shade over Storm Intervals
    for storm in Storms_LBJ_PT.iterrows(): ## shade over storm intervals
        ax1.axvspan(storm[1]['start'],storm[1]['end'],ymin=0,ymax=200,facecolor='grey', alpha=0.25)
        
    plt.tight_layout(pad=0.1)
    plt.show()
plot_Q_and_StormEvents(Storms_LBJ_PT, LBJ_flow_separated)

###

# At this point in the code there is data for Precip, Q, and the Storm Intervals are defined
print "Precip and Q are calculated, Storms are defined; moving on to SSC"
###
    
