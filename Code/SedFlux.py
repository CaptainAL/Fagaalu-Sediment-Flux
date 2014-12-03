# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 07:40:01 2014

@author: Alex
"""

#### Import modules
## Data Processing
import os
import numpy as np
import pandas as pd
#import math
import datetime as dt
import matplotlib.pyplot as plt

##custom modules
from misc_time import * 
from misc_numpy import *
from misc_matplotlib import * 

## Statistical Analysis
import pandas.stats.moments as m
from scipy.stats import pearsonr as pearson_r
from scipy.stats import spearmanr as spearman_r

#timer
import datetime as dt
start_time = dt.datetime.now()
print 'Start time: '+start_time.strftime('%H:%M:%S')

#### Plotting Tools
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.gridspec as gridspec 
import pylab
from AnnoteFinder import AnnoteFinder
import seaborn as sns
plt.close('all')
plt.ion()


## Set Pandas display options
pd.set_option('display.large_repr', 'truncate')
pd.set_option('display.width', 180)
pd.set_option('display.max_rows', 25)
pd.set_option('display.max_columns', 10)

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
    
def show_plot(show=False,fig=figure):
    if show==True:
        plt.draw()
        plt.show()
def logaxes(log=False,fig=figure):
    if log==True:
        for sub in fig.axes:
            sub.set_yscale('log'),sub.set_xscale('log')
def savefig(save=False,title='fig'):
    if save==True:
        plt.savefig(figdir+title)
    return
def pltdefault():
    global figdir
    plt.rcdefaults()
    #figdir = datadir+'samoa/WATERSHED_ANALYSIS/GoodFigures/rawfigoutput/'
    return    
def pltsns(style='ticks',context='talk'):
    global figdir
    sns.set_style(style)
    sns.set_style({'legend.frameon':True})
    sns.set_context(context)
    #figdir = datadir+'samoa/WATERSHED_ANALYSIS/GoodFigures/rawfigoutput/'
    return
def xkcd():
    global figdir
    plt.xkcd()
    #figdir = datadir+'samoa/WATERSHED_ANALYSIS/GoodFigures/rawfigoutput/xkcd/'
    return

## Misc. plotting tools
def labelxy(i,x,y):
    annotes = pd.DataFrame([x,y]).apply(tuple,axis=0).values.tolist()
    annotestrings = ["%.1f"%an[0]+','+"%.1f"%an[1] for an in annotes]
    af = AnnoteFinder(x,y,annotestrings)
    pylab.connect('button_press_event', af)
    return

def labelindex(i,x,y,ax,display=False): 
    if ax==None:
        ax=plt.gca()
    indexstrings = [str(ind) for ind in i]
    if display ==True:
        for i in zip(indexstrings,x,y):
            print i
    af = AnnoteFinder(x,y,indexstrings,axis=ax)
    pylab.connect('button_press_event', af)
    return
    
def labelindex_subplot(ax,i,x,y): 
    indexstrings = [str(ind) for ind in i]
    af = AnnoteFinder(x,y,indexstrings,axis=ax)
    connect('button_press_event', af)
    return

def annotate_plot(frame,plot_col,label_col):
    frame = frame[frame[label_col].isnull()!=True]
    for label, x, y in zip(frame['fieldnotes'], frame.index, frame['SSC (mg/L)']):
            plt.annotate(label, xy=(x, y))
            
def scaleSeries(series,new_scale=[100,10]):
    new_scale = new_scale
    OldRange = (series.max() - series.min())  
    NewRange = (new_scale[0] - new_scale[1])  
    NewSeriesValues = (((series - series.min()) * NewRange) / OldRange) + new_scale[1]
    return NewSeriesValues          
    
def power(x,a,b):
    y = a*(x**b)
    return y
    
def powerfunction(x,y,name='power rating'):
    datadf = pd.DataFrame.from_dict({'x':x,'y':y}).dropna().apply(np.log10) ## put x and y in a dataframe so you can drop ones that don't match up    
    datadf = datadf[datadf>=-10] ##verify data is valid (not inf)
    regression = pd.ols(y=datadf['y'],x=datadf['x'])
    pearson = pearson_r(datadf['x'],datadf['y'])[0]
    spearman = spearman_r(datadf['x'],datadf['y'])[0]
    coeffdf = pd.DataFrame({'a':[10**regression.beta[1]],'b':[regression.beta[0]],'r2':[regression.r2],'rmse':[regression.rmse],'pearson':[pearson],'spearman':[spearman]},index=[name])
    return coeffdf

def PowerFit(x,y,xspace=None,ax=plt,**kwargs):
    ## Develop power function for x and y
    powfunc = powerfunction(x,y) ## x and y should be Series
    a, b = powfunc['a'].values, powfunc['b'].values
    #print a,b
    if xspace==None:
        xvals = np.linspace(0,x.max()*1.2)
        #print 'No xspace, calculating xvals: '+str(x.max())+'*1.5= '+str(x.max()*1.5)
    else:
        xvals=xspace
    ypred = a*(xvals**b)
    ax.plot(xvals,ypred,**kwargs)
    plt.draw()
    return powfunc

def PowerFit_CI(x,y,xspace=None,ax=plt,**kwargs):
    datadf = pd.DataFrame.from_dict({'x':x,'y':y}).dropna().apply(np.log10) ## put x and y in a dataframe so you can drop ones that don't match up    
    regression = pd.ols(y=datadf['y'],x=datadf['x'])    
    ## Develop power function for x and y
    powfunc = powerfunction(x,y) ## x and y should be Series
    a, b = powfunc['a'].values, powfunc['b'].values
    #print a,b
    if xspace==None:
        xvals = np.linspace(0,x.max()*1.2)
        #print 'No xspace, calculating xvals: '+str(x.max())+'*1.5= '+str(x.max()*1.5)
    else:
        xvals=xspace
    ypred = a*(xvals**b)
    ax.plot(xvals,ypred,**kwargs)
    ## Confidence interals
    ci=.5
    a_cilo,a_ciup = 10**regression.sm_ols.conf_int(alpha=ci)[1][0],10**regression.sm_ols.conf_int(alpha=ci)[1][1]
    b_cilo,b_ciup = regression.sm_ols.conf_int(alpha=ci)[0][0],regression.sm_ols.conf_int(alpha=ci)[0][1]
    ypred_cilo=a_cilo*(xvals**b_cilo)
    ypred_ciup=a_ciup*(xvals**b_ciup)
    ax.fill_between(xvals,ypred_cilo,ypred_ciup,alpha=0.5,**kwargs)
    plt.draw()
    return powfunc
## test 
#x= np.linspace(1.0,10.0,10)
#y = 10.0*(x**0.5)
#name = 'x2'
#plt.scatter(x,x2)
#xpowfun = powerfunction(x,x2,name)
#xpower = PowerFit(x,y)
    
def linearfunction(x,y,name='linear rating'):
    datadf = pd.DataFrame.from_dict({'x':x,'y':y}).dropna() ## put x and y in a dataframe so you can drop ones that don't match up    
    datadf = datadf[datadf>=0].dropna() ##verify data is valid (not inf)
    regression = pd.ols(y=datadf['y'],x=datadf['x'])
    pearson = pearson_r(datadf['x'],datadf['y'])[0]
    spearman = spearman_r(datadf['x'],datadf['y'])[0]
    coeffdf = pd.DataFrame({'a':[regression.beta[1]],'b':[regression.beta[0]],'r2':[regression.r2],'rmse':[regression.rmse],'pearson':[pearson],'spearman':[spearman]},index=[name])
    return coeffdf
    
def LinearFit(x,y,xspace=None,ax=plt,**kwargs):
    linfunc = linearfunction(x,y)
    a, b = linfunc['a'].values, linfunc['b'].values
    #print a,b
    if xspace==None:
        xvals = np.linspace(0,x.max()*1.2) ##list of dummy x's as predictors
    else:
        xvals=xspace
    ypred = b*xvals + a ## predicted y from dummy list of x's
    ax.plot(xvals,ypred,**kwargs)
    plt.draw()
    return linfunc
## test
#x= np.linspace(1.0,10.0,10)
#y = 10*x + 15
#name = 'x2'
#plt.scatter(x,y)
#xlinfun = linearfunction(x,y,name)
#xlinear = LinearFit(x,y)

def nonlinearfunction(x,y,order=2,interceptZero=False):
    datadf = pd.DataFrame.from_dict({'x':x,'y':y}).dropna() ## put x and y in a dataframe so you can drop ones that don't match up    
    datadf = datadf[datadf>=0].dropna() ##verify data is valid (not inf)
    if interceptZero!=True:
        PolyCoeffs = np.polyfit(datadf['x'].values, datadf['y'].values, order) ## calculates polynomial coeffs
        PolyEq = np.poly1d(PolyCoeffs) ## turns the coeffs into an equation
        
    ## Calculate polynomial with a y-intercept of zero    
    if interceptZero==True:
        coeff = np.transpose([datadf['x'].values*datadf['x'].values, datadf['x'].values])
        ((a, b), _, _, _) = np.linalg.lstsq(coeff, datadf['y'].values)
        PolyEq = np.poly1d([a, b, 0])
    return PolyEq

def NonlinearFit(x,y,order=2,interceptZero=False,xspace=None,Ax=plt,**kwargs):
    nonlinfunc = nonlinearfunction(x,y,order,interceptZero)
    #print linfunc
    if xspace==None:
        xvals = np.linspace(0,x.max()*1.2) ##list of dummy x's as predictors
    else:
        xvals=xspace
    ypred = nonlinfunc(xvals)
    Ax.plot(xvals,ypred,**kwargs)
    plt.draw()
    return nonlinfunc

## test
#x= np.linspace(1.0,10.0,10)
#y = 10*x + 15
#name = 'x2' 
#plt.scatter(x,x2)
#xnonlinfun = nonlinearfunction(x,x2)
#xnonlinear = NonlinearFit(x,x2)

def plotregressionline(data,ols_object,ax,color):
    slope,intercept = ols_object.beta
    x = np.array([min(data), max(data)])
    y = intercept + slope * x
    ax.plot(x, y,color)
    return
    
def showstormintervals(ax,storm_threshold,StormsList,shade_color='grey',show=True):
    ## Storms
    if show==True:
        if storm_threshold==True:
            print 'Storm threshold stage= '+ '%.'%storm_threshold   
            ax.axhline(y=storm_threshold,ls='--',color=shade_color)    
        for storm in StormsList.iterrows(): ## shade over storm intervals
            ax.axvspan(storm[1]['start'],storm[1]['end'],ymin=0,ymax=200,facecolor=shade_color, alpha=0.25)
    return


## Year Interval Times
start2012, stop2012 = dt.datetime(2012,1,7,0,0), dt.datetime(2012,12,31,11,59)    
start2013, stop2013 = dt.datetime(2013,1,1,0,0), dt.datetime(2013,12,31,11,59)
start2014, stop2014 = dt.datetime(2014,1,1,0,0), dt.datetime(2014,12,31,11,59)     

if 'XL' not in locals():
    print 'opening MASTER_DATA excel file...'+dt.datetime.now().strftime('%H:%M:%S')
    XL = pd.ExcelFile(datadir+'MASTER_DATA_FAGAALU.xlsx')
if 'XL' in locals():
    print 'MASTER_DATA opened: '+dt.datetime.now().strftime('%H:%M:%S')    
    
#### Import PRECIP Data
#from precip_data import raingauge#, AddTimu1, AddTimu1Hourly, AddTimu1Daily, AddTimu1Monthly
def raingauge(XL,sheet='',shift=0):
    print 'loading precip: '+sheet+'...'
    #my_parser= lambda x: dt.datetime.strptime(x,"%m/%d/%Y %H:%M")
    gauge = XL.parse(sheet,header=1,index_col=0,parse_cols='B,C',parse_dates=True)#,date_parser=my_parser)
    gauge= gauge.shift(shift)
    gauge = gauge*.254 ##hundredths to mm
    gauge.columns=['Events']
    return gauge    

## Timu-Fagaalu 1 (by the Quarry)
if 'Precip' not in locals():
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
Precip['FPrain-30']=Precip['FPrain'].resample('30Min',how=sum)
Precip['FPhourly'] = Precip['FPrain'].resample('H',how='sum') ## label=left?? 
Precip['FPdaily'] = Precip['FPrain'].resample('D',how='sum')
Precip['FPmonthly'] = Precip['FPrain'].resample('MS',how='sum')

Precip['FPhourly'].dropna().to_csv(datadir+'OUTPUT/FPhourly.csv',header=['FPhourly'])
Precip['FPdaily'].dropna().to_csv(datadir+'OUTPUT/FPdaily.csv',header=['FPdaily'])
Precip['FPmonthly'].dropna().to_csv(datadir+'OUTPUT/FPmonthly.csv',header=['FPmonthly'])

## Filled Precipitation record, priority = Timu1, fill with FPrain
PrecipFilled=pd.DataFrame(pd.concat([Precip['Timu1-15'][dt.datetime(2012,1,7):dt.datetime(2013,2,8)],Precip['FPrain'][dt.datetime(2013,2,8,0,15):dt.datetime(2013,3,12)],Precip['Timu1-15'][dt.datetime(2013,3,12,0,15):dt.datetime(2013,3,24)],Precip['FPrain'][dt.datetime(2013,3,24,0,15):dt.datetime(2013,5,1)],Precip['Timu1-15'][dt.datetime(2013,5,1,0,15):dt.datetime(2014,8,5)]]),columns=['Precip']).dropna()

#from HydrographTools import StormSums
#def StormSums(Stormslist,Data,offset=0):
#    Events = pd.DataFrame(columns=['start','end','count','sum','max'])
#    print 'Summing storms...'
#    for storm_index,storm in Stormslist.iterrows():
#        start = storm['start']-dt.timedelta(minutes=offset) ##if Storms are defined by stream response you have to grab the preceding precip data
#        end= storm['end']
#        data = True ## Innocent until proven guilty
#        try:
#            print 'start: '+str(start) +' end: '+str(end)
#            event = Data.ix[start:end] ### slice list of Data for event
#        except KeyError:
#            start = start+dt.timedelta(minutes=15) ## if the start time falls between 2 30minute periods
#            print 'change storm start to '+str(start)            
#            try:
#                event = Data.ix[start:end]
#            except KeyError:
#                end = end+dt.timedelta(minutes=15)
#                print 'change storm end to '+str(end) 
#                try:
#                    event = Data.ix[start:end]
#                except KeyError:
#                    print 'no storm data available for storm '+str(start)
#                    pass
#        Events = Events.append(pd.DataFrame(
#        {'start':start,'end':end,'count':event.count(),
#        'sum':event.sum(),'max':event.max()},index=[storm['start']]))
#        Events[['count','sum','max']]=Events[['count','sum','max']].astype(float)
#    return Events
def StormSums(Stormslist,Data,offset=0):
    eventlist = []
    print 'Summing storms...'
    for storm_index,storm in Stormslist.iterrows():
        start = storm['start']-dt.timedelta(minutes=offset) ##if Storms are defined by stream response you have to grab the preceding precip data
        end= storm['end']
        data = True ## Innocent until proven guilty
        try:
            #print str(start) +' '+str(end)
            event = Data.ix[start:end] ### slice list of Data for event
        except KeyError:
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
            eventcount = event.count()
            eventsum = event.sum()
            eventmax = event.max()
            eventlist.append((storm['start'],[storm['start'],storm['end'],eventcount,eventsum,eventmax])) 
        if data == False:
            eventcount,eventsum,eventmax=np.nan,np.nan,np.nan
            eventlist.append((storm['start'],[storm['start'],storm['end'],eventcount,eventsum,eventmax])) 
    Events=DataFrame.from_items(eventlist,orient='index',columns=['start','end','count','sum','max'])
    return Events

#### Import FIELD NOTEBOOK Data
#from notebook import FieldNotes
def FieldNotes(sheet,headerrow,Book):
    print 'Opening field notes...'
    def my_parser(x,y):
        y = str(int(y))
        hour=y[:-2]
        minute=y[-2:]
        time=dt.time(int(hour),int(minute))
        parsed=dt.datetime.combine(x,time)
        #print parsed
        return parsed
    notebook_file = pd.ExcelFile(Book)
    notebook = notebook_file.parse(sheet,header=headerrow,parse_dates=[['Date','Time']],date_parser=my_parser,index_col=['Date_Time'])
    return notebook


### Check tipping bucket at RG1 (Timu1) against non-recording (World's Best)
fieldbookdata = datadir+'FieldNotebook-dataonly.xlsx'
Timu1fieldnotes = FieldNotes('Timu-F1notes',3,fieldbookdata)

Timu1mmcheck = Timu1fieldnotes.ix[:,'mm':'to 0.1'] ##take the records from the manual gage and if it was emptied to zero
Timu1mmcheck['mm true'] = Timu1mmcheck['mm']-Timu1mmcheck['to 0.1'].shift(1)

Timu1mmcheck['end']=Timu1mmcheck.index## add a column for time
Timu1mmcheck['start']=Timu1mmcheck['end'].shift(1) ## take the time and shift it down so you have a start and stop time: When the gauge was emptied to zero, it was the start of the next interval
Timu1mmcheck=Timu1mmcheck.truncate(before = Timu1mmcheck.index[5])

Timu1mmcheck['Timu1 mm sum']=StormSums(Timu1mmcheck,Precip['Timu1'])['sum'] ## from 1/20/12 onward. Timu1 QC data begins 1/21/12
Timu1mmcheck['WorldsBest - Timu1'] = Timu1mmcheck['Timu1 mm sum']-Timu1mmcheck['mm']

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
                                Time = dt.datetime(int(year),int(month),int(day),int(hour),int(minute)) ## -10 so it lines up with other times
                                #print Time
                                timedelta =-dt.timedelta(hours=11)
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
##load data from NOAA Climate Observatory at Tula, East Tutuila
#TULAbaro= pd.DataFrame(Tula(datadir+'BARO/TulaStation/TulaMetData/'),columns=['TULAbaro']) ## add TULA barometer data

##load data from Tafuna Intl ## To get more data from the Airport run wundergrabber_NSTU.py in the 'Maindir+Data/NSTU/' folder
airport = pd.DataFrame.from_csv(datadir+'BARO/NSTU/NSTU-current.csv') ## download new data using wundergrabber
airport['Wind Speed m/s']=airport['Wind SpeedMPH'] * 0.44704
#TAFUNAbaro= pd.DataFrame({'TAFUNAbaro':airport['Sea LevTim Bodellel PressureIn'] * 3.3863881579}).resample('15Min',fill_method='ffill',limit=2)## inches to kPa

##load data from NDBC NSTP6 station at DMWR, Pago Harbor
## To get more NSTP6 data either go to their website and copy and paste the historical data
## or use wundergrabber_NSTP6-REALTIME.py and copy and paste frome the .csv
def ndbc(datafile = datadir+'BARO/NSTP6/NSTP6-2012-14.xlsx'):
    ndbcXL = pd.ExcelFile(datafile)
    ndbc_parse = lambda yr,mo,dy,hr,mn: dt.datetime(yr,mo,dy,hr,mn)
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
NDBCbaro = NDBCbaro-.022
 
## Build data frame of barometric data: Make column 'baropress' with best available data
allbaro = pd.DataFrame(NDBCbaro/10)
allbaro['FPbaro']=FP['Bar']/10
allbaro['NDBCbaro']=NDBCbaro/10
#allbaro['TULAbaro']=TULAbaro['TULAbaro']

## Fill priority = FP,NDBC,TAFUNA,TULA
allbaro['Baropress']=allbaro['FPbaro'].where(allbaro['FPbaro']>0,allbaro['NDBCbaro']) ## create a new column and fill with FP or NDBC
#allbaro['Baropress']=allbaro['Baropress'].where(allbaro['Baropress']>0,allbaro['TAFUNAbaro'])
#allbaro['Baropress']=allbaro['Baropress'].where(allbaro['Baropress']>0,allbaro['TULAbaro']) 

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
    PT['stage']=(PT['Pressure']-PT['barodata'])/9.81*100.0
    #PT['stage']=PT['stage'].where(PT['stage']>0,PT['barodata']) ## filter negative values
    PT['stage']=PT['stage'].round(1)  
    PT['stage']=PT['stage']+zshift
    return PT

def PT_Levelogger(allbaro,PTname,XL,sheet,tshift=0,zshift=0): # tshift in hours, zshift in cm
    print 'loading Levelogger PT: '+sheet+'...'
    PT = XL.parse(sheet,header=11,parse_cols='A,B,D',parse_dates=[['Date','Time']],index_col=['Date_Time'])
    PT.columns= ['LEVEL']
    PT=PT.resample('15Min',how='mean')
    PT['barodata']=allbaro['Baropress']
    PT=PT.shift(tshift) ## shift by 3 hours (12 x 15minutes)
    PT['stage']=(PT['LEVEL']-PT['barodata'])/9.81*100.0
    #PT['stage']=PT['stage'].where(PT['stage']>0,0) ## filter negative values
    PT['stage']=PT['stage'].round(1)  
    PT['stage']=PT['stage']+zshift
    return PT
## PT1 LBJ
# tshift in 15Min(or whatever the timestep is), zshift in cm
PT1a = PT_Hobo(allbaro,'PT1 LBJ bridge',XL,'PT-Fagaalu1a',12) #12 x 15min = 3hours
PT1ba = PT_Hobo(allbaro,'PT1 LBJ bridge',XL,'PT-Fagaalu1ba',3)
PT1bb = PT_Hobo(allbaro,'PT1 LBJ bridge',XL,'PT-Fagaalu1bb',3,zshift=-1.5)
PT1c = PT_Hobo(allbaro,'PT1 LBJ bridge',XL,'PT-Fagaalu1c',0)
PT1 = pd.concat([PT1a,PT1ba,PT1bb,PT1c])
## PT2 QUARRY
# tshift in 15Min(or whatever the timestep is), zshift in cm
PT2 = PT_Levelogger(allbaro,'PT2 Drive Thru',XL,'PT-Fagaalu2',0,-22)
## PT3 DAM
# tshift in 15Min(or whatever the timestep is), zshift in cm
PT3a = PT_Hobo(allbaro,'PT3a Dam',XL,'PT-Fagaalu3a',12,zshift=-3.75)
PT3b = PT_Levelogger(allbaro,'PT3b Dam',XL,'PT-Fagaalu3b',0,zshift=-23)
PT3c = PT_Levelogger(allbaro,'PT3c Dam',XL,'PT-Fagaalu3c',0,zshift=-19.5)
PT3d = PT_Levelogger(allbaro,'PT3d Dam',XL,'PT-Fagaalu3d',0,zshift=-17.1)
PT3e = PT_Levelogger(allbaro,'PT3e Dam',XL,'PT-Fagaalu3e',0,zshift=-18.4)
PT3f = PT_Levelogger(allbaro,'PT3f Dam',XL,'PT-Fagaalu3f',0,zshift=-17)
PT3g = PT_Levelogger(allbaro-1.5,'PT3g Dam',XL,'PT-Fagaalu3g',0,zshift=-10.5)
PT3 = pd.concat([PT3a,PT3b,PT3c,PT3d,PT3e,PT3f,PT3g])
PT3 = PT3[PT3>0]

PT1 = PT1.reindex(pd.date_range(start2012,stop2014,freq='15Min'))
PT2 = PT2.reindex(pd.date_range(start2012,stop2014,freq='15Min'))
PT3 = PT3.reindex(pd.date_range(start2012,stop2014,freq='15Min'))

def plot_stage_data(show=False):
    fig, (baro,pt1,pt3,t) = plt.subplots(4,sharex=True,sharey=False)
    allbaro['Baropress'].plot(ax=baro,c='k')
    allbaro['Baropress'].plot(ax=t,c='k')
    baro.legend()
    ## PT1 at LBJ
    PT1list = [PT1a,PT1ba,PT1bb,PT1c]
    count = 0
    count_dict = {1:'a',2:'bs',3:'bb',4:'c'}
    for PT in PT1list:
        count+=1
        try:
            PT['Pressure'].plot(ax=pt1,c=np.random.rand(3,1),label='PT1'+count_dict[count])
            PT['Pressure'].plot(ax=t,c=np.random.rand(3,1),label='PT1'+count_dict[count])
        except KeyError:
            PT['LEVEL'].plot(ax=pt1,c=np.random.rand(3,1),label='PT1'+count_dict[count])
            PT['LEVEL'].plot(ax=t,c=np.random.rand(3,1),label='PT1'+count_dict[count])
    pt1.legend()
    ## PT3 at DAM
    PT3list = [PT3a,PT3b,PT3c,PT3d,PT3e,PT3f,PT3g]
    count = 0
    count_dict = {1:'a',2:'b',3:'c',4:'d',5:'e',6:'f',7:'g',8:'h'}
    for PT in PT3list:
        count+=1
        try:
            PT['Pressure'].plot(ax=pt3,c=np.random.rand(3,1),label='PT3'+count_dict[count])
            PT['Pressure'].plot(ax=t,c=np.random.rand(3,1),label='PT3'+count_dict[count])
        except KeyError:
            PT['LEVEL'].plot(ax=pt3,c=np.random.rand(3,1),label='PT3'+count_dict[count])
            PT['LEVEL'].plot(ax=t,c=np.random.rand(3,1),label='PT3'+count_dict[count])
    pt3.legend()
    t.legend()
    
    if show==True:
        plt.draw()
        plt.show()
    return
#plot_stage_data(show=True)
    
  
### Check PT against reference staff gage at LBJ
LBJfieldnotes = FieldNotes('LBJstage',1,fieldbookdata)
LBJfieldnotesStage = pd.DataFrame(LBJfieldnotes['RefGageHeight(cm)'].resample('15Min',how='first').dropna(),columns=['RefGageHeight(cm)'])
LBJfieldnotesStage['PT1']=PT1['stage']
LBJfieldnotesStage['GH-PT']=LBJfieldnotesStage['RefGageHeight(cm)']-PT1['stage']

PT1['GH Correction']=LBJfieldnotesStage['GH-PT']
PT1['GH Correction Int']= PT1['GH Correction'].interpolate()
PT1['stage corrected'] = PT1['stage']+PT1['GH Correction Int']

## Plot Stage Correction
#PT1['stage'].plot=('y')
#LBJfieldnotesStage['RefGageHeight(cm)'].plot(ls='None',marker='o',markersize=6,c='g')
#PT1['stage corrected'].plot(color='k')

StageCorrXL = pd.ExcelFile(datadir+'Q/StageCorrection.xlsx')
def correct_Stage(StageCorrXL,location,PTdata):
    print 'Correcting stage for '+location
    StageCorr = StageCorrXL.parse(location)
    Correction=pd.DataFrame()
    for correction in StageCorr.iterrows():
        t1 = correction[1]['T1_date']
        t2 = correction[1]['T2_date']
        z = correction[1]['z']    
        print t1,t2, z
        Correction = Correction.append(pd.DataFrame({'z':z},index=pd.date_range(t1,t2,freq='15Min')))
    Correction = Correction.reindex(pd.date_range(start2012,stop2014,freq='15Min'))
    PTdata['stage_Correction'] = Correction['z']
    PTdata['stage_Corrected'] = PTdata['stage']+PTdata['stage_Correction']
    PTdata['stage']=PTdata['stage_Corrected'].where(PTdata['stage_Corrected']>0,PTdata['stage'])
    return PTdata
    
PT1 = correct_Stage(StageCorrXL,'LBJ',PT1)
PT3 = correct_Stage(StageCorrXL,'DAM',PT3)

## STAGE DATA FOR PT's
#### FINAL STAGE DATA with CORRECTIONS
Fagaalu_stage_data = pd.DataFrame({'LBJ':PT1['stage'],'DT':PT2['stage'],'Dam':PT3['stage']})
Fagaalu_stage_data = Fagaalu_stage_data.reindex(pd.date_range(start2012,stop2014,freq='15Min'))

#### ..
#### STAGE TO DISCHARGE ####
#from stage2discharge_ratingcurve import AV_RatingCurve#, calcQ, Mannings_rect, Weir_rect, Weir_vnotch, Flume
def AV_RatingCurve(path,location,stage_data,slope=.01,Mannings_n=.033,trapezoid=True,printResults=False):
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
                split = line.strip('\n')
                split = split.split('\t')
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
                        
                        AV_Q = df['AV'].sum()
                        Area = df['rectangular-area'].sum()
                        V = df['flow'].mean()
                        ManningV = np.nan
                    try:
                        stage = stage_data[location].ix[DateTime] ## Get Stage data
                    except:
                        stage =np.nan
                    Qdf = Qdf.append(pd.DataFrame({'stage(cm)':stage,'Q-AV(L/sec)':AV_Q,'Q-AManningV(L/sec)':ManningQ,'Area(m2)':Area,'V(m/s)':V,'ManningV(m/s)':ManningV,'WP':WP,'R':R},index=[DateTime]))
                    
                    if printResults==True:                    
                        print str(DateTime)+': stage='+'%.2f'%stage+' Q= '+'%.2f'%AV_Q+' ManningQ= '+'%.2f'%ManningQ
                        print df              
    return Qdf 
### Area Velocity and Mannings from in situ measurments
## stage2discharge_ratingcurve.AV_rating_curve(datadir,location,Fagaalu_stage_data,trapezoid=False,Slope=0.01,Mannings_n=0.03,width=4.9276)
## Returns DataFrame of Stage (cm) and Discharge (L/sec) calc. from AV measurements with time index

### Calculate Q from a single AV measurement
#fileQ = calcQ(datadir+'Q/LBJ_4-18-13.txt','LBJ',Fagaalu_stage_data,slope=Slope,Mannings_n=n,trapezoid=True)
## and save to CSV
#pd.concat(fileQ).to_csv(datadir+'Q/LBJ_4-18-13.csv')


### Discharge using Mannings and Surveyed Cros-section
#from ManningsRatingCurve import Mannings, Mannings_Series
def Mannings(XSfile,sheetname,Slope,Manning_n,stage_start,stage_end=None,display=True):    
    ## Open and parse file; drop NA  
    print XSfile+' '+sheetname
    print 'Slope: '+str(Slope)+' Mannings n: '+str(Manning_n)
    XL = pd.ExcelFile(XSfile) 
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
        ## Mannings = (1R^2/3 * S^1/2)/n
        ManningV = (1*(R**(2.0/3.0))*(S**0.5))/n
        ManningQ = ManningV * Area ## M3/s
        if display == True:
            fig, ax1 = plt.subplots(1)
            ax1.plot(df['Dist'],df['y1'],'-o',c='k')
            ax1.fill_between(df['Dist'], df['y1'], stage,where = df['y1']<=stage,alpha=.5, interpolate=True)
            ax1.annotate('stage: '+'%.2f'%stage+'m',xy=(2,stage+.45))
            ax1.annotate('Mannings n: '+'%.3f'%n,xy=(2,stage+.03))
            ax1.annotate('Area: '+'%.3f'%Area+'m2',xy=(2,stage+.25))
            ax1.annotate('WP: '+'%.2f'%WP+'m',xy=(df['Dist'].mean(),stage+.03))
            ax1.annotate('Manning V: '+'%.2f'%ManningV+'m/s ',xy=(df['Dist'].mean(),stage+.25))
            ax1.annotate('Manning Q: '+'%.3f'%ManningQ+'m3/s',xy=(df['Dist'].mean(),stage+.45))
            plt.axes().set_aspect('equal')
            plt.xlim(-1,df['Dist'].max()+1),plt.ylim(-1,stage + 1.)
        areas.append(Area)
        wp.append(WP)
        r.append(R)
        Man_n.append(n)
        v.append(ManningV)
        q.append(ManningQ)
    DF = pd.DataFrame({'stage':stages,'area':areas,'wp':wp,'r':r, 'Man_n':Man_n,'vel':v,'Q':q})
    return DF,df
    
def Mannings_Series(XSfile,sheetname,Slope,Manning_n,stage_series):    
    ## Open and parse file; drop NA  
    print XSfile+' '+sheetname
    print 'Slope: '+str(Slope)+' Mannings n: '+str(Manning_n)
    XL = pd.ExcelFile(XSfile) 
    df = XL.parse(sheetname,header=4,parse_cols='F:H')
    df = df.dropna()
    ## Mannings Parameters S:slope, n:Mannings n
    S = Slope # m/m
    n= Manning_n
    ## empty lists
    areas, wp, r, Man_n, v, q, = [],[],[],[],[],[]
    ## Stage data
    stage_series = stage_series/100 ## cm to m
    stages = stage_series.values
    for stage in stages:
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
        ## Mannings = (1R^2/3 * S^1/2)/n
        ManningV = (1*(R**(2.0/3.0))*(S**0.5))/n
        ManningQ = ManningV * Area ## M3/s
        areas.append(Area)
        wp.append(WP)
        r.append(R)
        Man_n.append(n)
        v.append(ManningV)
        q.append(ManningQ)        
    DF = pd.DataFrame({'stage':stages,'area':areas,'wp':wp,'r':r,'Man_n':Man_n,'vel':v,'Q':q},index=stage_series.index)
    return DF
    
## Read LBJ_Man Discharge from .csv, or calculate new if needed
if 'LBJ_Man' not in locals():
    try:
        print 'Calculate Mannings Q for LBJ'
        LBJ_Man = pd.DataFrame.from_csv(datadir+'Q/LBJ_Man.csv')
    except:
        LBJ_Man = Mannings_Series(datadir+'Q/LBJ_cross_section.xlsx','LBJ_m',Slope=0.016,Manning_n='Jarrett',stage_series=Fagaalu_stage_data['LBJ'])
        LBJ_Man.to_csv(datadir+'Q/LBJ_Man.csv')
        pass
## Read DAM_Man Discharge from .csv, or calculate new if needed
if 'DAM_Man' not in locals():
    try:
        print 'Calculate Mannings Q for DAM'
        DAM_Man = pd.DataFrame.from_csv(datadir+'Q/DAM_Man.csv')
    except:
        DAM_Man = Mannings_Series(datadir+'Q/LBJ_cross_section.xlsx','DAM_m',Slope=0.03,Manning_n='Jarrett',stage_series=Fagaalu_stage_data['Dam'])
        DAM_Man.to_csv(datadir+'Q/DAM_Man.csv')
        pass 

#### LBJ Stage-Discharge
# (3 rating curves: AV measurements, A measurment * Mannings V, Surveyed Cross-Section and Manning's equation)

## LBJ AV measurements
## Mannings parameters for A-ManningV
Slope = 0.0161 # m/m
LBJ_n=0.080 # Mountain stream rocky bed and rivers with variable sections and veg along banks (Dunne 1978)
LBJ_n='Jarrett'
LBJstageDischarge = AV_RatingCurve(datadir+'Q/','LBJ',Fagaalu_stage_data,slope=Slope,Mannings_n=LBJ_n,trapezoid=True).dropna() #DataFrame with Q from AV measurements, Q from measured A with Manning-predicted V, stage, and Q from Manning's and assumed rectangular channel A
LBJstageDischarge = LBJstageDischarge.truncate(before=datetime.datetime(2012,3,20)) # throw out measurements when I didn't know how to use the flow meter very well
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

### Fit nonlinear wiht intercept zero
#for _ in range(3):## add zero/zero intercept
#    LBJstageDischarge=LBJstageDischarge.append(pd.DataFrame({'stage(cm)':0,'Q-AV(L/sec)':0},index=[np.random.rand()])) 
#LBJ_AVnonLinear = nonlinearfunction(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AV(L/sec)'],order=3,interceptZero=False)  
#LBJstageDischarge=LBJstageDischarge.dropna() ## get rid of zero/zero interctp
#
#for _ in range(3):## add zero/zero intercept
#    LBJstageDischarge=LBJstageDischarge.append(pd.DataFrame({'stage(cm)':0,'Q-AManningV(L/sec)':0},index=[np.random.rand()])) 
#LBJ_AManningVnonLinear = nonlinearfunction(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AManningV(L/sec)'],order=3,interceptZero=False)
#LBJstageDischarge=LBJstageDischarge.dropna() ## get rid of zero/zero interctp

## LBJ: Q from OrangePeel method 
#from notebook import OrangePeel
def OrangePeel(sheet,headerrow,Book):
    def my_parser(x,y):
        y = str(int(y))
        hour=y[:-2]
        minute=y[-2:]
        time=dt.time(int(hour),int(minute))
        parsed=dt.datetime.combine(x,time)
        #print parsed
        return parsed
    opfile = pd.ExcelFile(Book)
    orangepeel = opfile.parse(sheet,header=headerrow,parse_dates=[['Date','Time']],date_parser=my_parser,index_col=['Date_Time'])
    orangepeel = orangepeel.drop(orangepeel.columns[16:],1)
    orangepeel = orangepeel[orangepeel['AVG L/sec']>=0]
    return orangepeel
orangepeel = OrangePeel('OrangePeel',1,datadir+'Q/Fagaalu-StageDischarge.xlsx')
orangepeel=orangepeel.append(pd.DataFrame({'stage cm':0,'L/sec':0},index=[pd.NaT]))


#### DAM Stage-Discharge
Slope= 0.3
DAM_n=.033
DAM_n = 'Jarrett'
## DAM AV Measurements
DAMstageDischarge = AV_RatingCurve(datadir+'Q/','Dam',Fagaalu_stage_data,slope=Slope,Mannings_n=DAM_n).dropna() ### Returns DataFrame of Stage and Discharge calc. from AV measurements with time index
DAMstageDischarge = DAMstageDischarge[10:]# throw out measurements when I didn't know how to use the flow meter very well
DAMstageDischargeLog=DAMstageDischarge.apply(np.log10) #log-transformed version

## DAM: Discharge Ratings
## Linear
DAM_AV = pd.ols(y=DAMstageDischarge['Q-AV(L/sec)'],x=DAMstageDischarge['stage(cm)'],intercept=True) 
## Power
DAM_AVLog = pd.ols(y=DAMstageDischargeLog['Q-AV(L/sec)'],x=DAMstageDischargeLog['stage(cm)'],intercept=True) 

### HEC-RAS Model of the DAM structure: Documents/HEC/FagaaluDam.prj
def HEC_piecewise(PTdata):
    if type(PTdata)!=pd.Series:
        PTdata = pd.Series(data=PTdata)
    HEC_a1, HEC_b1 = 9.9132, -5.7184## from excel DAM_HEC.xlsx
    HEC_a2, HEC_b2 = 25.823, -171.15 
    HEC_a3, HEC_b3 = 98.546, -3469.4
    
    Func1=PTdata[PTdata<=11]*HEC_a1 + HEC_b1
    Func2=PTdata[(PTdata>11)&(PTdata<=45)]*HEC_a2 + HEC_b2
    Func3=PTdata[PTdata>45]*HEC_a3 + HEC_b3
    AllValues = Func1.append([Func2,Func3])
    return AllValues
DAM_HECstageDischarge= pd.DataFrame(data=range(0,150),columns=['stage(cm)'])
DAM_HECstageDischarge['Q_HEC(L/sec)'] = HEC_piecewise(DAM_HECstageDischarge['stage(cm)'])

DAMstageDischarge['Q_HEC(L/sec)']= HEC_piecewise(DAMstageDischarge['stage(cm)']).values

DAM_HEC = pd.ols(y=DAMstageDischarge['Q_HEC(L/sec)'],x=DAMstageDischarge['stage(cm)'],intercept=True) 

### Compare Discharg Ratings
def plotStageDischargeRatings(show=False,log=False,save=False): ## Rating Curves
    fig =plt.figure(figsize=(12,8))
    ax = plt.subplot(2,2,1)
    site_lbj = plt.subplot2grid((2,2),(0,0))
    site_dam = plt.subplot2grid((2,2),(1,0))
    both = plt.subplot2grid((2,2),(0,1),rowspan=2)
    mpl.rc('lines',markersize=15)
    
    title="Discharge Ratings for LBJ and DAM"
    xy = np.linspace(0,8000,8000)
    
    #LBJ AV Measurements and Rating Curve
    site_lbj.plot(LBJstageDischarge['Q-AV(L/sec)'],LBJstageDischarge['stage(cm)'],'.',color='r',markeredgecolor='k',label='LBJ_AV')   
    #LBJ A*ManningV Measurements and Rating Curves
    #site_lbj.plot(LBJstageDischarge['Q-AManningV(L/sec)'],LBJstageDischarge['stage(cm)'],'.',color='grey',markeredgecolor='k',label='LBJ A*ManningsV')

    ## LBJ MODELS
    ## LBJ Linear    
    LBJ_AVlinear= linearfunction(LBJstageDischarge['Q-AV(L/sec)'],LBJstageDischarge['stage(cm)'])    
    LinearFit(LBJstageDischarge['Q-AV(L/sec)'],LBJstageDischarge['stage(cm)'],xy,site_lbj,c='grey',ls='--',label='LBJ_AVlinear '+r'$r^2$'+"%.2f"%LBJ_AVlinear['r2'])
    ## LBJ Power
    LBJ_AVpower = powerfunction(LBJstageDischarge['Q-AV(L/sec)'],LBJstageDischarge['stage(cm)'])    
    PowerFit(LBJstageDischarge['Q-AV(L/sec)'],LBJstageDischarge['stage(cm)'],xy,site_lbj,c='r',ls='-.',label='LBJ_AVpower '+r'$r^2$'+"%.2f"%LBJ_AVpower['r2'])    
    ## LBJ NonLinear
    #LBJ_AVnonLinear = nonlinearfunction(LBJstageDischarge['Q-AV(L/sec)'],LBJstageDischarge['stage(cm)'],order=2,interceptZero=False)  
    #site_lbj.plot(xy,LBJ_AVnonLinear(xy),color='r',ls='-',label='LBJ_AVnonLinear')    
    ## LBJ Mannings Linear    
    #LBJ_MANlinear=linearfunction(LBJstageDischarge['Q-AManningV(L/sec)'],LBJstageDischarge['stage(cm)'])
    #LinearFit(LBJstageDischarge['Q-AManningV(L/sec)'],LBJstageDischarge['stage(cm)'],xy,site_lbj,c='grey',ls='--',label='LBJ_MANlinear') ## rating from LBJ_AManningV
    ## LBJ Manning Power    
    #LBJ_MANpower =powerfunction(LBJstageDischarge['Q-AManningV(L/sec)'],LBJstageDischarge['stage(cm)'])    
    #PowerFit(LBJstageDischarge['Q-AManningV(L/sec)'],LBJstageDischarge['stage(cm)'],xy,site_lbj,c='grey',ls='-.',label='LBJ_MANpower') ## rating from LBJ_AManningVLog
    ## LBJ Manning NonLinear   
    #LBJ_AManningVnonLinear = nonlinearfunction(LBJstageDischarge['Q-AManningV(L/sec)'],LBJstageDischarge['stage(cm)'],order=2,interceptZero=False)
    #site_lbj.plot(xy,LBJ_AManningVnonLinear(xy),color='grey',ls='-',label='LBJ_AManningVnonLinear')
    ## LBJ Mannings from stream survey
    LBJ_ManQ, LBJ_Manstage = LBJ_Man['Q']*1000, LBJ_Man['stage']*100
    site_lbj.plot(LBJ_ManQ,LBJ_Manstage,'.',markersize=2,c='b',label='Mannings')
    labelindex_subplot(site_lbj, LBJstageDischarge.index,LBJstageDischarge['Q-AV(L/sec)'],LBJstageDischarge['stage(cm)'])
    
    #DAM AV Measurements and Rating Curve
    site_dam.plot(DAMstageDischarge['Q-AV(L/sec)'],DAMstageDischarge['stage(cm)'],'.',color='g',markeredgecolor='k',label='DAM_AV')
    ## DAM Linear
    DAM_AVlinear=linearfunction(DAMstageDischarge['Q-AV(L/sec)'],DAMstageDischarge['stage(cm)'])    
    LinearFit(DAMstageDischarge['Q-AV(L/sec)'],DAMstageDischarge['stage(cm)'],xy,site_dam,c='grey',ls='--',label='DAM_AVlinear '+r'$r^2$'+"%.2f"%DAM_AVlinear['r2']) ## rating from DAM_AVLog
    ## DAM Power    
    DAM_AVpower=powerfunction(DAMstageDischarge['Q-AV(L/sec)'],DAMstageDischarge['stage(cm)'])    
    PowerFit(DAMstageDischarge['Q-AV(L/sec)'],DAMstageDischarge['stage(cm)'],xy,site_dam,c='grey',ls='-.', label='DAM AVpower '+r'$r^2$'+"%.2f"%DAM_AVpower['r2']) ## rating from DAM_AV
    #DAM HEC-RAS Model and Rating Curve
    #LinearFit(DAM_HECstageDischarge['Q_HEC(L/sec)'],DAM_HECstageDischarge['stage(cm)'],xy,site_dam,c='b',ls='-',label='DAM_HEClinear') ## rating from DAM_HEC
    #PowerFit(DAM_HECstageDischarge['Q_HEC(L/sec)'],DAM_HECstageDischarge['stage(cm)'],xy,site_dam,c='b',ls='--',label='DAM_HECpower') ## rating from DAM_HEC
    #site_dam.plot(DAM_HECstageDischarge['Q_HEC(L/sec)'],DAM_HECstageDischarge['stage(cm)'],'-',color='b',label='DAM HEC-RAS Model')
    ## DAM Mannings from stream survey
    site_dam.plot(DAM_Man['Q']*1000,DAM_Man['stage']*100,'.',markersize=2,color='g',label='Mannings DAM')   
    
    labelindex_subplot(site_dam, DAMstageDischarge.index,DAMstageDischarge['Q-AV(L/sec)'],DAMstageDischarge['stage(cm)'])

    ## Plot selected rating curves for LBJ and DAM
    ## AV measurements
    both.plot(LBJstageDischarge['Q-AV(L/sec)'],LBJstageDischarge['stage(cm)'],'.',color='r',markeredgecolor='k',label='VILLAGE A-V')  
    both.plot(DAMstageDischarge['Q-AV(L/sec)'],DAMstageDischarge['stage(cm)'],'.',color='g',markeredgecolor='k',label='FOREST A-V')    
    
    ##LBJ Power
    PowerFit(LBJstageDischarge['Q-AV(L/sec)'],LBJstageDischarge['stage(cm)'],xy,both,c='r',ls='-.',label='LBJ_AVpower '+r'$r^2$'+"%.2f"%LBJ_AVpower['r2'])    
    ## LBJ Nonlinear Model
    #both.plot(xy,LBJ_AVnonLinear(xy),color='r',ls='--',label='LBJ_AVnonLinear')    
    #both.plot(xy,LBJ_AManningVnonLinear(xy),color='r',ls='-',label='LBJ_AManningVnonLinear')
    #both.plot(LBJ_Man['Q']*1000,LBJ_Man['stage']*100,'.',markersize=2,color='y',label='Mannings LBJ')
    #PowerFit(DAM_Man['Q']*1000,DAM_Man['stage']*100,xy,both,c='g',ls='-.',label='DAM_Mannings Power')    
    both.plot(DAM_Man['Q']*1000,DAM_Man['stage']*100,'.',markersize=2,color='g',label='Mannings DAM')   
    ## DAM Power    
    #PowerFit(DAMstageDischarge['Q-AV(L/sec)'],DAMstageDischarge['stage(cm)'],xy,both,c='g',ls='-.', label='DAM AVpower '+r'$r^2$'+"%.2f"%DAM_AVpower['r2']) ## rating from DAM_AV

    ## DAM HEC-RAS Model 
    #both.plot(xy, HEC_piecewise(xy),'-',color='g',label='DAM HEC-RAS piecewise')

    ## Label subplots    
    site_lbj.set_title('VILLLAGE'),site_lbj.set_ylabel('Stage(cm)'),site_lbj.set_xlabel('Q(L/sec)')
    site_dam.set_title('FOREST'),site_dam.set_ylabel('Stage(cm)'),site_dam.set_xlabel('Q(L/sec)')
    both.set_title('Selected Ratings'),both.set_ylabel('Stage(cm)'),both.set_xlabel('Q(L/sec)'),both.yaxis.tick_right(),both.yaxis.set_label_position('right')
    ## Format subplots
    site_lbj.set_ylim(0,PT1['stage'].max()+10)#,site_lbj.set_xlim(0,LBJ_AVnonLinear(PT1['stage'].max()+10))
    site_dam.set_ylim(0,PT3['stage'].max()+10)#,site_dam.set_xlim(0,HEC_piecewise(PT3['stage'].max()+10).values)
    both.set_ylim(0,PT1['stage'].max()+10)
    ## Legends
    site_lbj.legend(loc='lower right',fancybox=True),site_dam.legend(loc='lower right',fancybox=True),both.legend(loc='best',ncol=2,fancybox=True)
    plt.legend(loc='best')    
    ## Figure title
    #plt.suptitle(title,fontsize=16)
    fig.canvas.manager.set_window_title('Figure : '+title) 
    logaxes(log,fig)
    for ax in fig.axes:
        ax.autoscale_view(True,True,True)
    show_plot(show,fig)
    savefig(save,title)
    return
#plotStageDischargeRatings(show=True,log=False,save=False)
#plotStageDischargeRatings(show=True,log=False,save=True)
#plotStageDischargeRatings(show=True,log=True,save=True)
#plotStageDischargeRatings(show=True,log=True,save=False)

#### CALCULATE DISCHARGE
## Calculate Q for LBJ
## Stage
LBJ = DataFrame(PT1,columns=['stage']) ## Build DataFrame with all stage records for location (cm)
## Mannings
LBJ['Q-Mannings'] = LBJ_Man['Q']*1000
## Linear Models
LBJ['Q-AV']=(LBJ['stage']*LBJ_AV.beta[0]) + LBJ_AV.beta[1] ## Calculate Q from AV rating (L/sec)
LBJ['Q-AManningV']= (LBJ['stage']*LBJ_AManningV.beta[0]) + LBJ_AManningV.beta[1] ## Calculate Q from A-Mannings rating (L/sec)
## Power Models
a,b = 10**LBJ_AVLog.beta[1], LBJ_AVLog.beta[0]# beta[1] is the intercept = log10(a), so a = 10**beta[1] # beta[0] is the slope = b
LBJ['Q-AVLog'] = a * (LBJ['stage']**b)
a,b = 10**LBJ_AManningVLog.beta[1], LBJ_AManningVLog.beta[0]
LBJ['Q-AManningVLog'] = a*(LBJ['stage']**b)
## NonLinear Models
LBJ['Q-AVnonLinear'] = LBJ_AVnonLinear(LBJ['stage'])
LBJ['Q-AManningVnonLinear']= LBJ_AManningVnonLinear(LBJ['stage'])

## Calculate Q for DAM
## Stage
DAM = DataFrame(PT3,columns=['stage']) ## Build DataFrame with all stage records for location
## Mannings
DAM['Q-Mannings']=DAM_Man['Q']*1000 ## m3/s to L/sec
## Linear Model
DAM['Q-AV']=(DAM['stage']*DAM_AV.beta[0]) + DAM_AV.beta[1] ## Calculate Q from AV rating=
## Power Model
a,b = 10**DAM_AVLog.beta[1], DAM_AVLog.beta[0]
DAM['Q-AVLog']=(a)*(DAM['stage']**b) 
## HEC-RAS Model
DAM['Q-HEC']= HEC_piecewise(DAM['stage'])

#### CHOOSE Q RATING CURVE
LBJ['Q']= LBJ['Q-AVLog']
print 'LBJ Q from AV Power Law'
DAM['Q']= DAM['Q-Mannings']
print 'DAM Q from Mannings and Surveyed Cross Section'

#### Calculate Q for QUARRY TODO
QUARRY = pd.DataFrame((DAM['Q']/.9)*1.17) ## Q* from DAM x Area Quarry

## Convert to 15min interval LBJ
LBJq = (LBJ*900) ## Q above is in L/sec; L/sec * 900sec/15Min = L/15Min
LBJq['stage']=PT1['stage'] ## put unaltered stage back in

## Convert to 15min interval QUARRY
QUARRYq = (QUARRY*900) ## Q above is in L/sec; L/sec * 900sec/15Min = L/15Min
QUARRYq['stage']=PT3['stage'] ## put unaltered stage back in

## Convert to 15min interval DAM
DAMq= (DAM*900)## Q above is in L/sec; L/sec * 900sec/15Min = L/15Min
DAMq['stage']=PT3['stage'] ## put unaltered stage back in

def plotdischargeintervals(fig,ax,start,stop):
    LBJ['Q'][start:stop].dropna().plot(ax=ax,c='r',label='LBJ (Q-AV PowerLaw)')
    ax.plot(LBJstageDischarge.index,LBJstageDischarge['Q-AV(L/sec)'],ls='None',marker='o',color='r')
    DAM['Q'][start:stop].dropna().plot(ax=ax,c='g',ls='-',label='DAM (Q-Mannings)')
    ax.plot(DAMstageDischarge.index,DAMstageDischarge['Q-AV(L/sec)'],ls='None',marker='o',color='g')
    ax.set_ylim(0,2600)
    return
    
def QYears(show=False):
    mpl.rc('lines',markersize=8)
    fig, (Q2012,Q2013,Q2014)=plt.subplots(3)
    plotdischargeintervals(fig,Q2012,start2012,stop2012)
    plotdischargeintervals(fig,Q2013,start2013,stop2013)
    plotdischargeintervals(fig,Q2014,start2014,stop2014)
    
    Q2014.legend()
    Q2013.set_ylabel('Discharge (Q) L/sec')
    Q2012.set_title("Discharge (Q) L/sec at the Upstream and Downstream Sites, Faga'alu")
    plt.draw()
    if show==True:
        plt.show()
    return
#QYears(True)

#### Define Storm Periods #####
## Define Storm Intervals at LBJ
DefineStormIntervalsBy = {'User':'User','Separately':'BOTH','DAM':'DAM','LBJ':'LBJ'}
StormIntervalDef = DefineStormIntervalsBy['User']

#from HydrographTools import SeparateHydrograph
def SeparateHydrograph(hydrodata='stage',minimum_length=8):
    params = hydrodata.describe()
    mean = params[1]
    std = params[2]
    minimum = params[3]
    maximum = params[7]
    quartiles= params[4:8]
    stormthresh = mean+std
    print 'Storm threshold= '+'%.1f'%stormthresh
    StormFlow = hydrodata.where(hydrodata>stormthresh) 
    ##returns list of data points that meet the condition, the rest are NaN (same shape as original array)
    ## or
    #PT1storm = PT1[PT1>stormthresh] ## NaN values are filtered out

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
        start = t[0]-timedelta(minutes=30)
        end= t[1]
        event = hydrodata.ix[start:end]
        eventduration = end-start
        seconds = eventduration.total_seconds()
        hours = seconds / 3600
        eventduration = round(hours,2)
        if event.count() >= minimum_length:
            eventlist.append([start,end,eventduration])

    Events=pd.DataFrame(eventlist,columns=['start','end','duration (hrs)'])
    #drop_rows = Events[Events['duration (min)'] <= timedelta(minutes=120)] ## Filters events that are too short
    #Events = Events.drop(drop_rows.index) ## Filtered DataFrame of storm start,stop,count,sum
    return Events
## Define by Threshold = Mean Stage+ 1 Std Stage
LBJ_storm_threshold = PT1['stage'].describe()[1]+PT1['stage'].describe()[2] 
DAM_storm_threshold = PT3['stage'].describe()[1]+PT3['stage'].describe()[2]

## Take just one definition of Storm Intervals....
if StormIntervalDef=='LBJ':
    print 'Storm intervals defined at LBJ'
    ## Define Storm Intervals at LBJ
    LBJ_StormIntervals=SeparateHydrograph(hydrodata=PT1['stage'])
    ## Combine Storm Events where the storm end is the storm start for the next storm
    LBJ_StormIntervals['next storm start']=LBJ_StormIntervals['start'].shift(-1) ## add the next storm's start and end time to the storm in the row above (the previous storm)
    LBJ_StormIntervals['next storm end']=LBJ_StormIntervals['end'].shift(-1)
    need_to_combine =LBJ_StormIntervals[LBJ_StormIntervals['end']==LBJ_StormIntervals['next storm start']] #storms need to be combined if their end is the same time as the next storm's start
    need_to_combine['end']=need_to_combine['next storm end'] # change the end of the storm to the end of the next storm to combine them
    LBJ_StormIntervals=LBJ_StormIntervals.drop(need_to_combine.index) #drop the storms that need to be combined
    LBJ_StormIntervals=LBJ_StormIntervals.append(need_to_combine).sort(ascending=True) #append back in the combined storms
    LBJ_StormIntervals=LBJ_StormIntervals.drop_duplicates(cols=['end']) #drop the second storm that was combined
    ## Set Storm Intervals for DAM, same as LBJ   
    QUARRY_StormIntervals=LBJ_StormIntervals
    DAM_StormIntervals=LBJ_StormIntervals
    
if StormIntervalDef == 'DAM':
    print 'Storm intervals defined at DAM'
    ## Define Storm Intervals at DAM
    DAM_StormIntervals=SeparateHydrograph(hydrodata=PT3['stage'])
    ## Combine Storm Events where the storm end is the storm start for the next storm
    DAM_StormIntervals['next storm start']=DAM_StormIntervals['start'].shift(-1) ## add the next storm's start and end time to the storm in the row above (the previous storm)
    DAM_StormIntervals['next storm end']=DAM_StormIntervals['end'].shift(-1)
    need_to_combine =DAM_StormIntervals[DAM_StormIntervals['end']==DAM_StormIntervals['next storm start']] #storms need to be combined if their end is the same time as the next storm's start
    need_to_combine['end']=need_to_combine['next storm end'] # change the end of the storm to the end of the next storm to combine them
    DAM_StormIntervals=DAM_StormIntervals.drop(need_to_combine.index) #drop the storms that need to be combined
    DAM_StormIntervals=DAM_StormIntervals.append(need_to_combine).sort(ascending=True) #append back in the combined storms
    DAM_StormIntervals=DAM_StormIntervals.drop_duplicates(cols=['end']) 
    ## Set Storm Intervals for LBJ, same as DAM       
    LBJ_StormIntervals=DAM_StormIntervals
    QUARRY_StormIntervals=DAM_StormIntervals

if StormIntervalDef=='BOTH':
    print 'Storm intervals defined separately at LBJ and DAM'
    ## Define Storm Intervals at LBJ
    LBJ_StormIntervals=SeparateHydrograph(hydrodata=PT1['stage'])
    ## Combine Storm Events where the storm end is the storm start for the next storm
    LBJ_StormIntervals['next storm start']=LBJ_StormIntervals['start'].shift(-1) ## add the next storm's start and end time to the storm in the row above (the previous storm)
    LBJ_StormIntervals['next storm end']=LBJ_StormIntervals['end'].shift(-1)
    need_to_combine =LBJ_StormIntervals[LBJ_StormIntervals['end']==LBJ_StormIntervals['next storm start']] #storms need to be combined if their end is the same time as the next storm's start
    need_to_combine['end']=need_to_combine['next storm end'] # change the end of the storm to the end of the next storm to combine them
    LBJ_StormIntervals=LBJ_StormIntervals.drop(need_to_combine.index) #drop the storms that need to be combined
    LBJ_StormIntervals=LBJ_StormIntervals.append(need_to_combine).sort(ascending=True) #append back in the combined storms
    LBJ_StormIntervals=LBJ_StormIntervals.drop_duplicates(cols=['end']) #drop the second storm that was combined

    ## Define Storm Intervals at DAM
    DAM_StormIntervals=SeparateHydrograph(hydrodata=PT3['stage'])
    ## Combine Storm Events where the storm end is the storm start for the next storm
    DAM_StormIntervals['next storm start']=DAM_StormIntervals['start'].shift(-1) ## add the next storm's start and end time to the storm in the row above (the previous storm)
    DAM_StormIntervals['next storm end']=DAM_StormIntervals['end'].shift(-1)
    need_to_combine =DAM_StormIntervals[DAM_StormIntervals['end']==DAM_StormIntervals['next storm start']] #storms need to be combined if their end is the same time as the next storm's start
    need_to_combine['end']=need_to_combine['next storm end'] # change the end of the storm to the end of the next storm to combine them
    DAM_StormIntervals=DAM_StormIntervals.drop(need_to_combine.index) #drop the storms that need to be combined
    DAM_StormIntervals=DAM_StormIntervals.append(need_to_combine).sort(ascending=True) #append back in the combined storms
    DAM_StormIntervals=DAM_StormIntervals.drop_duplicates(cols=['end']) 
    ## QUARRY same as DAM
    QUARRY_StormIntervals=DAM_StormIntervals
    
## Use User-defined storm intervals
if StormIntervalDef=='User':
    print 'Storm intervals defined by user'
    LBJstormintervalsXL = pd.ExcelFile(datadir+'LBJ_StormIntervals_filtered.xlsx')
    LBJ_StormIntervals = LBJstormintervalsXL.parse('StormIntervals',header=0,parse_cols='A:C',index_col=0)
    ## 
    DAMstormintervalsXL = pd.ExcelFile(datadir+'DAM_StormIntervals_filtered.xlsx')
    DAM_StormIntervals = DAMstormintervalsXL.parse('StormIntervals',header=0,parse_cols='A:C',index_col=0)
    QUARRY_StormIntervals, DAM_StormIntervals = DAM_StormIntervals, DAM_StormIntervals


### SAVE Storm Intervals for LATER
LBJ_StormIntervals.to_excel(datadir+'Q/LBJ_StormIntervals.xlsx')
QUARRY_StormIntervals.to_excel(datadir+'Q/QUARRY_StormIntervals.xlsx')
DAM_StormIntervals.to_excel(datadir+'Q/DAM_StormIntervals.xlsx')
    

#### Analyze Storm Precip Characteristics: Intensity, Erosivity Index etc. ####
def StormPrecipAnalysis(storms=LBJ_StormIntervals):
    #### EROSIVITY INDEX for storms (ENGLISH UNITS)
    Stormdf = pd.DataFrame()
    for storm in storms.iterrows():
        StormIndex = storm[1]['start']
        start = storm[1]['start']-dt.timedelta(minutes=60) ## storm start is when PT exceeds threshold, retrieve Precip x min. prior to this.
        end =  storm[1]['end'] ## when to end the storm?? falling limb takes too long I think
        
        rain_data = pd.DataFrame.from_dict({'Timu1':PrecipFilled['Precip'][start:end]})
        if len(rain_data)>0:
            try:
                #print start,end
                rain_data['AccumulativeDepth mm']=(rain_data['Timu1']).cumsum() ## cumulative depth at 1 min. intervals
                rain_data['AccumulativeDepth in.']=rain_data['AccumulativeDepth mm']/25.4 ## cumulative depth at 1 min. intervals
                rain_data['Intensity (in./hr)']=rain_data['Timu1']*60 ## intensity at each minute
                rain_data['30minMax (in./hr)']=m.rolling_sum(Precip['Timu1'],window=30)/25.4
                
                Psum_in = rain_data['Timu1'].sum()/25.4
                duration_hours = (end - start).days * 24 + (end - start).seconds//3600
                I = Psum_in/duration_hours ## I = Storm Average Intensity
                E = 1099. * (1.-(0.72*math.exp(-1.27*I))) ## E = Rain Kinetic Energy
                I30 = rain_data['30minMax (in./hr)'].max()
                EI = E*I30
                EIm = EI*1.702
                Stormdf=Stormdf.append(pd.DataFrame({'Total(in)':Psum_in,'Duration(hrs)':duration_hours,
                'Max30minIntensity(in/hr)':I30,'AvgIntensity(in/hr)':I,'E-RainKineticEnergy(ft-tons/acre/inch)':E,'EI':EI,'EIm':EIm},index=[StormIndex]))
                Stormdf = Stormdf[(Stormdf['Total(in)']>0.0)] ## filter out storms without good Timu1 data
            except:
                raise
                print "Can't analyze Storm Precip for storm:"+str(start)
                pass
    return Stormdf
    
LBJ_Stormdf = StormPrecipAnalysis(storms=LBJ_StormIntervals)
QUARRY_Stormdf = StormPrecipAnalysis(storms=QUARRY_StormIntervals)
DAM_Stormdf = StormPrecipAnalysis(storms=DAM_StormIntervals)


### ..
#### SSC Grab sample ANALYSIS
SampleCounts = DataFrame(data=[str(val) for val in pd.unique(SSC['Location'])],columns=['Location'])
SampleCounts['#ofSSCsamples']=pd.Series([len(SSC[SSC['Location']==str(val)]) for val in pd.unique(SSC['Location'])]) ##add column of Locations

### SSC Sample Counts from Unique Sites
## from SampleCounts select rows where SampleCounts['Location'] starts with 'Quarry'; sum up the #ofSSCsamples column
AllQuarrySamples = pd.DataFrame(data=[[SampleCounts[SampleCounts['Location'].str.startswith('Quarry')]['#ofSSCsamples'].sum(),'AllQuarry']],columns=['#ofSSCsamples','Location']) ## make DataFrame of the sum of all records that Location starts wtih 'Quarry'
SampleCounts = SampleCounts.append(AllQuarrySamples)
## drop the columns that were counted above to get a DataFrame of unique sampling locations
SampleCounts= SampleCounts.drop(SampleCounts[SampleCounts['Location'].str.startswith(('N1','N2','Quarry'))].index)
SampleCounts.index=range(1,len(SampleCounts)+1)

## SSC Boxplots and Discharge Concentration
LBJgrab = SSC[SSC['Location'].isin(['LBJ'])].resample('15Min',fill_method='pad',limit=0)
QUARRYgrab =SSC[SSC['Location'].isin(['DT','R2'])].resample('15Min',fill_method='pad',limit=0)
R2grab =SSC[SSC['Location'].isin(['R2'])].resample('15Min',fill_method='pad',limit=0)
DAMgrab = SSC[SSC['Location'].isin(['DAM'])].resample('15Min',fill_method='pad',limit=0)
GrabSamples = pd.concat([DAMgrab['SSC (mg/L)'],QUARRYgrab['SSC (mg/L)'],LBJgrab['SSC (mg/L)']],axis=1)
GrabSamples.columns = ['DAM','QUARRY','LBJ']
GrabSampleMeans = [DAMgrab.mean(),QUARRYgrab.mean(),LBJgrab.mean()]
GrabSampleVals = np.concatenate([DAMgrab.values.tolist(),QUARRYgrab.values.tolist(),LBJgrab.values.tolist()])
GrabSampleCategories = np.concatenate([[1]*len(DAMgrab),[2]*len(QUARRYgrab),[3]*len(LBJgrab)])

def plotSSCboxplots(show=False):
    mpl.rc('lines',markersize=100)
    fig, (ax1,ax2)=plt.subplots(1,2)
    GrabSamples.columns = ['FOREST','QUARRY','VILLAGE']
    GrabSamples.boxplot(ax=ax1)
    GrabSamples.boxplot(ax=ax2)
    
    ax1.scatter(GrabSampleCategories,GrabSampleVals,s=40,marker='+',label='SSC (mg/L)')
    ax1.legend()
    ax2.scatter([1,2,3],GrabSampleMeans,s=40,color='k',label='Mean SSC (mg/L)')
    ax1.set_ylim(0,4000), ax2.set_ylim(0,300)    
    ax1.set_ylabel('SSC (mg/L)'),ax1.set_xlabel('Location'),ax2.set_xlabel('Location')
    plt.suptitle("Suspended Sediment Concentrations at sampling locations in Fag'alu",fontsize=16)
    plt.legend()
    plt.draw()
    if show==True:
        plt.show()
    return
#plotSSCboxplots(True)

### Build data for Sediment Rating Curve    
dam_ssc = pd.DataFrame(SSC[SSC['Location']=='DAM']['SSC (mg/L)']).resample('15Min')
dam_ssc['Q']=DAM['Q']
dam_ssc = dam_ssc.dropna()
dam_ssc2012,dam_ssc2013,dam_ssc2014 = dam_ssc[start2012:stop2012],dam_ssc[start2013:stop2013],dam_ssc[start2014:stop2014]

quarry_ssc = pd.DataFrame(SSC[SSC['Location'].isin(['DT','R2'])]['SSC (mg/L)']).resample('15Min')
quarry_ssc['Q']=QUARRY['Q']
quarry_ssc =quarry_ssc.dropna()
quarry2012,quarry2013,quarry2014 = quarry_ssc[start2012:stop2012],quarry_ssc[start2013:stop2013],quarry_ssc[start2014:stop2014]

lbj_ssc = pd.DataFrame(SSC[SSC['Location']=='LBJ']['SSC (mg/L)']).resample('15Min')
lbj_ssc['Q']=LBJ['Q']
lbj_ssc=lbj_ssc.dropna()
lbj_ssc2012,lbj_ssc2013,lbj_ssc2014 = lbj_ssc[start2012:stop2012],lbj_ssc[start2013:stop2013],lbj_ssc[start2014:stop2014]

damQC = pd.ols(y=dam_ssc['SSC (mg/L)'],x=dam_ssc['Q'])
lbjQC = pd.ols(y=lbj_ssc['SSC (mg/L)'],x=lbj_ssc['Q'])

def plotQvsC(ms=6,show=False,log=False,save=True):
    #fig, ((down_ex,up_ex),(down,up)) = plt.subplots(2,2,sharey='row',sharex='col') 
    fig=plt.figure()
    gs = gridspec.GridSpec(2,2,height_ratios=[1,3])
    up_ex,down_ex = plt.subplot(gs[0]),plt.subplot(gs[1])
    up,down = plt.subplot(gs[2],sharex=up_ex),plt.subplot(gs[3],sharex=down_ex)
    mpl.rc('lines',markersize=ms)
    ## plot LBJ samples
    down.plot(lbj_ssc2012['Q'],lbj_ssc2012['SSC (mg/L)'],'.',c='g',label='VILLAGE 2012')
    down.plot(lbj_ssc2013['Q'],lbj_ssc2013['SSC (mg/L)'],'.',c='y',label='VILLAGE 2013')
    down.plot(lbj_ssc2014['Q'],lbj_ssc2014['SSC (mg/L)'],'.',c='r',label='VILLAGE 2014')
    down_ex.plot(lbj_ssc2012['Q'],lbj_ssc2012['SSC (mg/L)'],'.',c='g',label='VILLAGE 2012')
    down_ex.plot(lbj_ssc2013['Q'],lbj_ssc2013['SSC (mg/L)'],'.',c='y',label='VILLAGE 2013')    
    down_ex.plot(lbj_ssc2014['Q'],lbj_ssc2014['SSC (mg/L)'],'.',c='r',label='VILLAGE 2014')
    ## plot quarry samples
    down.plot(quarry2012['Q'],quarry2012['SSC (mg/L)'],'^',markersize=ms/2,c='g',label='QUARRY 2012')
    down.plot(quarry2013['Q'],quarry2013['SSC (mg/L)'],'^',markersize=ms/2,c='y',label='QUARRY 2013')
    down.plot(quarry2014['Q'],quarry2014['SSC (mg/L)'],'^',markersize=ms/2,c='r',label='QUARRY 2014')
    down_ex.plot(quarry2012['Q'],quarry2012['SSC (mg/L)'],'^',markersize=ms/2,c='g',label='QUARRY 2012')
    down_ex.plot(quarry2013['Q'],quarry2013['SSC (mg/L)'],'^',markersize=ms/2,c='y',label='QUARRY 2013')    
    down_ex.plot(quarry2014['Q'],quarry2014['SSC (mg/L)'],'^',markersize=ms/2,c='r',label='QUARRY 2014')
    ## plot DAM samples
    up.plot(dam_ssc2012['Q'],dam_ssc2012['SSC (mg/L)'],'.',c='g',label='DAM 2012')
    up.plot(dam_ssc2013['Q'],dam_ssc2013['SSC (mg/L)'],'.',c='y',label='DAM 2013')
    up.plot(dam_ssc2014['Q'],dam_ssc2014['SSC (mg/L)'],'.',c='r',label='DAM 2014')
    up_ex.plot(dam_ssc2012['Q'],dam_ssc2012['SSC (mg/L)'],'.',c='g',label='DAM 2012')
    up_ex.plot(dam_ssc2013['Q'],dam_ssc2013['SSC (mg/L)'],'.',c='y',label='DAM 2013')
    up_ex.plot(dam_ssc2014['Q'],dam_ssc2014['SSC (mg/L)'],'.',c='r',label='DAM 2014')
    ## plot a line marking storm threshold and label it
    up.axvline(x=54,ls='--',color='k'),down.axvline(x=150,ls='--',color='k')  
    up_ex.axvline(x=54,ls='--',color='k'),down_ex.axvline(x=150,ls='--',color='k')  
    up.text(54,800,'storm threshold',rotation='vertical'), down.text(150,800,'storm threshold',rotation='vertical')      

    plotregressionline(lbj_ssc2013['Q'],lbjQC,down,'k--')
    plotregressionline(dam_ssc2013['Q'],damQC,up,'k--')
       
    down.set_ylim(0,1200),up.set_ylim(0,1200)
    down.set_xlim(0,lbj_ssc['Q'].max()+100),up.set_xlim(0,lbj_ssc['Q'].max()+100)
    down_ex.set_xlim(0,2000),up_ex.set_xlim(0,2000)
    down_ex.set_ylim(1500,13000),up_ex.set_ylim(1500,13000)
    
    down_ex.xaxis.set_visible(False),up_ex.xaxis.set_visible(False)
    up.set_ylabel('SSC (mg/L)'), up.set_xlabel('Q (L/sec)'), down.set_xlabel('Q (L/sec)')
    up.grid(True),up_ex.grid(True),up_ex.legend(),down.grid(True),down_ex.grid(True),down_ex.legend(ncol=2)

    up_ex.set_title('Upstream (FOREST)'), down_ex.set_title('Downstream (QUARRY,VILLAGE)')

    title='Instantaneous Q vs SSC in Fagaalu Upstream and Downstream'
    plt.suptitle(title,fontsize=16)
    logaxes(log,fig)
    show_plot(show,fig)
    savefig(save,title)
    return
#plotQvsC(ms=20,show=True,log=False,save=False)
#plotQvsC(ms=20,show=True,log=False,save=True)
 

#### ..
#### Import T and SSC Data
#from load_from_MASTER_XL import TS3000,YSI,OBS,loadSSC
def TS3000(XL,sheet='DAM-TS3K'):
    print 'loading : '+sheet+'...'
    TS3K = XL.parse(sheet,header=0,parse_cols='A,F',index_col=0,parse_dates=True)
    TS3K.columns=['NTU']
    return TS3K
def YSI(XL,sheet='LBJ-YSI'):
    print 'loading : '+sheet+'...'
    YSI = XL.parse(sheet,header=4,parse_cols='A:H',parse_dates=[['Date','Time']],index_col=['Date_Time'])
    YSI=YSI.resample('5Min')
    return YSI
def OBS(XL,sheet='LBJ-OBS'):
    print 'loading : '+sheet+'...'
    OBS=XL.parse(sheet,header=4,parse_cols='A:L',parse_dates=True,index_col=0)
    return OBS
    
## Turbidimeter Data DAM
DAM_TS3K = TS3000(XL,'DAM-TS3K')
DAM_TS3K = DAM_TS3K[DAM_TS3K>=0]
DAM_YSI = YSI(XL,'DAM-YSI')
## Correct negative NTU values
DAM_YSI['NTU'][dt.datetime(2013,6,1):dt.datetime(2013,12,31)]=DAM_YSI['NTU'][dt.datetime(2013,6,1):dt.datetime(2013,12,31)]+6

## Turbidimeter Data QUARRY
#QUARRYxl = pd.ExcelFile(datadir+'QUARRY-OBS.xlsx')
#QUARRY_OBS = QUARRYxl.parse('QUARRY-OBS',header=4,parse_cols='A:L',parse_dates=True,index_col=0)
QUARRY_OBS = OBS(XL,'QUARRY-OBS')
QUARRY_OBS=QUARRY_OBS.rename(columns={'Turb_SS_Mean':'FNU'})
QUARRY_OBS['FNU'] = QUARRY_OBS['FNU'][QUARRY_OBS['FNU']<=4000]

## Turbidimeter Data LBJ
LBJ_YSI = YSI(XL,'LBJ-YSI')
LBJ_OBSa = OBS(XL,'LBJ-OBSa').drop_duplicates()
LBJ_OBSa = pd.concat([LBJ_OBSa[:dt.datetime(2013,4,1)],LBJ_OBSa[dt.datetime(2013,5,5):]])
LBJ_OBSa=LBJ_OBSa.rename(columns={'Turb_SS_Avg':'FNU'})
LBJ_OBSb = OBS(XL,'LBJ-OBSb')

LBJ_OBSb=LBJ_OBSb.rename(columns={'Turb_SS_Mean':'FNU'})
LBJ_OBS=LBJ_OBSa.append(LBJ_OBSb)
LBJ_OBS['FNU'] = LBJ_OBS['FNU'][LBJ_OBS['FNU']<=4000]
LBJ_OBS['FNU'] = LBJ_OBS['FNU'].interpolate(limit=2)

## Despike turbidity data
## http://ocefpaf.github.io/python4oceanographers/blog/2013/05/20/spikes/

## SSC Data
def loadSSC(SSCXL,sheet='ALL_MASTER'):
    print 'loading SSC...'
    def my_parser(x,y):
        try:
            y = str(int(y))
            while len(y)!=4:
                y = '0'+y
            hour=y[:-2]
            minute=y[-2:]
            time=dt.time(int(hour),int(minute))
            parsed=dt.datetime.combine(x,time)
            #print parsed
        except:
            parsed = pd.to_datetime(np.nan)
        return parsed
            
    SSC= SSCXL.parse(sheet,header=0,parse_dates=[['Date','Time']],date_parser=my_parser,index_col=['Date_Time'])
    return SSC
SSCXL = pd.ExcelFile(datadir+'SSC/SSC_grab_samples.xlsx')
SSC = loadSSC(SSCXL,'ALL_MASTER')
SSC= SSC[SSC['SSC (mg/L)']>0]

#### TURBIDITY
#### T to SSC rating curve for FIELD INSTRUMENTS
def NTU_SSCrating(TurbidimeterData,SSCdata,TurbidimeterName,location='LBJ',log=False):
    T_name = TurbidimeterName+'-NTU'
    SSCsamples = SSCdata[SSCdata['Location'].isin([location])].resample('5Min',fill_method = 'pad',limit=0) ## pulls just the samples matching the location name and roll to 5Min.
    SSCsamples = SSCsamples[pd.notnull(SSCsamples['SSC (mg/L)'])] ## gets rid of ones that mg/L is null
    SSCsamples[T_name]=TurbidimeterData['NTU']## grabs turbidimeter NTU data 
    SSCsamples = SSCsamples[pd.notnull(SSCsamples[T_name])]
    T_SSCrating = pd.ols(y=SSCsamples['SSC (mg/L)'],x=SSCsamples[T_name],intercept=True)
    return T_SSCrating,SSCsamples## Rating, Turbidity and Grab Sample SSC data
    
def FNU_SSCrating(TurbidimeterData,SSCdata,TurbidimeterName,location='LBJ',sampleinterval='5Min',log=False):
    T_name = TurbidimeterName+'-FNU'
    SSCsamples = SSCdata[SSCdata['Location'].isin([location])].resample(sampleinterval,fill_method = 'pad',limit=0) ## pulls just the samples matching the location name and roll to 5Min.
    SSCsamples = SSCsamples[pd.notnull(SSCsamples['SSC (mg/L)'])] ## gets rid of ones that mg/L is null
    SSCsamples[T_name]=TurbidimeterData['FNU']## grabs turbidimeter NTU data 
    SSCsamples = SSCsamples[pd.notnull(SSCsamples[T_name])]
    T_SSCrating = pd.ols(y=SSCsamples['SSC (mg/L)'],x=SSCsamples[T_name],intercept=True)
    return T_SSCrating,SSCsamples## Rating, Turbidity and Grab Sample SSC data

#### NTU to SSC rating curve from LAB ANALYSIS
#T_SSC_Lab= pd.ols(y=SSC[SSC['Location']=='LBJ']['SSC (mg/L)'],x=SSC[SSC['Location']=='LBJ']['NTU'])
T_SSC_Lab= pd.ols(y=SSC['SSC (mg/L)'],x=SSC['NTU'])
### NTU ratings
## LBJ YSIQuarryGrabSampleSSC=InterpolateGrabSamples(LBJ_StormIntervals, QUARRYgrab,60)
T_SSC_LBJ_YSI=NTU_SSCrating(LBJ_YSI,SSC,'LBJ-YSI','LBJ',log=False)
LBJ_YSIrating = T_SSC_LBJ_YSI[0]
## DAM TS3K
T_SSC_DAM_TS3K=NTU_SSCrating(DAM_TS3K,SSC,'DAM-TS3K','DAM',log=False) ## Use 5minute data for NTU/SSC relationship
DAM_TS3Krating = T_SSC_DAM_TS3K[0]
## DAM YSI
T_SSC_DAM_YSI=NTU_SSCrating(DAM_YSI,SSC,'DAM-YSI','DAM',log=False) ## Won't work until there are some overlapping grab samples
DAM_YSIrating= T_SSC_DAM_YSI[0]
### FNU ratings
## LBJ
T_SSC_LBJ_OBS_2013=FNU_SSCrating(LBJ_OBSa,SSC,'LBJ-OBS','LBJ','5Min',log=False)
LBJ_OBS_2013rating = T_SSC_LBJ_OBS_2013[0]
T_SSC_LBJ_OBS_2014=FNU_SSCrating(LBJ_OBSb,SSC,'LBJ-OBS','LBJ','15Min',log=False)
LBJ_OBS_2014rating = T_SSC_LBJ_OBS_2014[0]
## QUARRY
T_SSC_QUARRY_OBS=FNU_SSCrating(QUARRY_OBS,SSC,'QUARRY-OBS','R2','15Min',log=False)
QUARRY_OBSrating = T_SSC_QUARRY_OBS[0]

## Plot ALL T-SSC
## LAB
def T_SSC_ALL(show=False):
    fig = plt.figure()
    plt.scatter(SSC['NTU'],SSC['SSC (mg/L)'],color='b',label='LAB')
    ## DAM
    ALL_T_DAM = pd.DataFrame(pd.concat([T_SSC_DAM_TS3K[1]['DAM-TS3K-NTU'],T_SSC_DAM_YSI[1]['DAM-YSI-NTU']]),columns=['NTU'])
    ALL_T_DAM = ALL_T_DAM.join(pd.concat([T_SSC_DAM_TS3K[1]['SSC (mg/L)'],T_SSC_DAM_YSI[1]['SSC (mg/L)']]))
    plt.scatter(ALL_T_DAM['NTU'],ALL_T_DAM['SSC (mg/L)'],c='g',label='DAM')
    ## LBJ
    ALL_T_LBJ = pd.DataFrame(pd.concat([T_SSC_LBJ_YSI[1]['LBJ-YSI-NTU'],T_SSC_LBJ_OBS_2013[1]['LBJ-OBS-FNU'],
                       T_SSC_LBJ_OBS_2014[1]['LBJ-OBS-FNU'],]),columns=['FNU'])     
    ALL_T_LBJ =ALL_T_LBJ.join(pd.concat([T_SSC_LBJ_YSI[1]['SSC (mg/L)'],T_SSC_LBJ_OBS_2013[1]['SSC (mg/L)'],
                             T_SSC_LBJ_OBS_2014[1]['SSC (mg/L)']]))                    
    plt.scatter(ALL_T_LBJ['FNU'],ALL_T_LBJ['SSC (mg/L)'],c='r',label='LBJ')
    ## QUARRY
    plt.scatter(T_SSC_QUARRY_OBS[1]['QUARRY-OBS-FNU'],T_SSC_QUARRY_OBS[1]['SSC (mg/L)'],c='y',label='QUARRY')
    
    plt.plot([0,3000],[0,3000],c='k')   
    plt.xlabel('Turbidity'), plt.ylabel('SSC mg/L')
    plt.xlim(-10,2000), plt.ylim(-10,2000)
    plt.legend(loc='best')
    if show == True:
        plt.draw()
        plt.show()
    return
#T_SSC_ALL(show=True)


       
## Overall RMSE for LBJ-YSI rating and all DAM and LBJ samples
## make DataFrame of all measured NTU and SSC at LBJ and DAM
#T_SSC_NTU = pd.concat([T_SSC_LBJ_YSI[1]['LBJ-YSI-NTU'],T_SSC_DAM_TS3K[1]['DAM-TS3K-NTU'],T_SSC_DAM_YSI[1]['DAM-YSI-NTU']])
#T_SSC_SSC= pd.concat([T_SSC_LBJ_YSI[1]['SSC (mg/L)'],T_SSC_DAM_TS3K[1]['SSC (mg/L)'],T_SSC_DAM_YSI[1]['SSC (mg/L)']])
#T_SSC_ALL_NTU_RMSE = pd.DataFrame({'NTUmeasured':T_SSC_NTU,'SSCmeasured':T_SSC_SSC})

## LBJ YSI
T_SSC_LBJ_YSI_RMSE = pd.DataFrame({'NTUmeasured':T_SSC_LBJ_YSI[1]['LBJ-YSI-NTU'],'SSCmeasured':T_SSC_LBJ_YSI[1]['SSC (mg/L)']})
T_SSC_LBJ_YSI_RMSE['SSC_LBJ_YSIpredicted']= T_SSC_LBJ_YSI_RMSE['NTUmeasured']*LBJ_YSIrating.beta[0]+LBJ_YSIrating.beta[1]
T_SSC_LBJ_YSI_RMSE['SSC_diff'] = T_SSC_LBJ_YSI_RMSE['SSCmeasured']-T_SSC_LBJ_YSI_RMSE['SSC_LBJ_YSIpredicted']
T_SSC_LBJ_YSI_RMSE['SSC_diffsquared'] = (T_SSC_LBJ_YSI_RMSE['SSC_diff'])**2
T_SSC_LBJ_YSI_RMSE['SSC_RMSE'] = T_SSC_LBJ_YSI_RMSE['SSC_diffsquared']**0.5
T_SSC_LBJ_YSI_RMSE_Value = (T_SSC_LBJ_YSI_RMSE['SSC_RMSE'].mean())

## DAM YSI
T_SSC_DAM_YSI_RMSE = pd.DataFrame({'NTUmeasured':T_SSC_DAM_YSI[1]['DAM-YSI-NTU'],'SSCmeasured':T_SSC_DAM_YSI[1]['SSC (mg/L)']})
T_SSC_DAM_YSI_RMSE['SSC_DAM_YSIpredicted']= T_SSC_DAM_YSI_RMSE['NTUmeasured']*LBJ_YSIrating.beta[0]+LBJ_YSIrating.beta[1]
T_SSC_DAM_YSI_RMSE['SSC_diff'] = T_SSC_DAM_YSI_RMSE['SSCmeasured']-T_SSC_DAM_YSI_RMSE['SSC_DAM_YSIpredicted']
T_SSC_DAM_YSI_RMSE['SSC_diffsquared'] = (T_SSC_DAM_YSI_RMSE['SSC_diff'])**2
T_SSC_DAM_YSI_RMSE['SSC_RMSE'] = T_SSC_DAM_YSI_RMSE['SSC_diffsquared']**0.5
T_SSC_DAM_YSI_RMSE_Value = (T_SSC_DAM_YSI_RMSE['SSC_RMSE'].mean())

## LBJ OBS
T_SSC_LBJ_OBS_2013_RMSE = pd.DataFrame({'NTUmeasured':T_SSC_LBJ_OBS_2013[1]['LBJ-OBS-FNU'],'SSCmeasured':T_SSC_LBJ_OBS_2013[1]['SSC (mg/L)']})
T_SSC_LBJ_OBS_2013_RMSE['SSC_LBJ_OBSpredicted']= T_SSC_LBJ_OBS_2013_RMSE['NTUmeasured']*LBJ_OBS_2013rating.beta[0]+LBJ_OBS_2013rating.beta[1]
T_SSC_LBJ_OBS_2013_RMSE['SSC_diff'] = T_SSC_LBJ_OBS_2013_RMSE['SSCmeasured']-T_SSC_LBJ_OBS_2013_RMSE['SSC_LBJ_OBSpredicted']
T_SSC_LBJ_OBS_2013_RMSE['SSC_diffsquared'] = (T_SSC_LBJ_OBS_2013_RMSE['SSC_diff'])**2
T_SSC_LBJ_OBS_2013_RMSE['SSC_RMSE'] = T_SSC_LBJ_OBS_2013_RMSE['SSC_diffsquared']**0.5
T_SSC_LBJ_OBS_2013_RMSE_Value = (T_SSC_LBJ_OBS_2013_RMSE['SSC_RMSE'].mean())

T_SSC_LBJ_OBS_2014_RMSE = pd.DataFrame({'NTUmeasured':T_SSC_LBJ_OBS_2014[1]['LBJ-OBS-FNU'],'SSCmeasured':T_SSC_LBJ_OBS_2014[1]['SSC (mg/L)']})
T_SSC_LBJ_OBS_2014_RMSE['SSC_LBJ_OBSpredicted']= T_SSC_LBJ_OBS_2014_RMSE['NTUmeasured']*LBJ_OBS_2014rating.beta[0]+LBJ_OBS_2014rating.beta[1]
T_SSC_LBJ_OBS_2014_RMSE['SSC_diff'] = T_SSC_LBJ_OBS_2014_RMSE['SSCmeasured']-T_SSC_LBJ_OBS_2014_RMSE['SSC_LBJ_OBSpredicted']
T_SSC_LBJ_OBS_2014_RMSE['SSC_diffsquared'] = (T_SSC_LBJ_OBS_2014_RMSE['SSC_diff'])**2
T_SSC_LBJ_OBS_2014_RMSE['SSC_RMSE'] = T_SSC_LBJ_OBS_2014_RMSE['SSC_diffsquared']**0.5
T_SSC_LBJ_OBS_2014_RMSE_Value = (T_SSC_LBJ_OBS_2014_RMSE['SSC_RMSE'].mean())

## LBJ OBS
T_SSC_QUARRY_OBS_RMSE = pd.DataFrame({'NTUmeasured':T_SSC_QUARRY_OBS[1]['QUARRY-OBS-FNU'],'SSCmeasured':T_SSC_QUARRY_OBS[1]['SSC (mg/L)']})
T_SSC_QUARRY_OBS_RMSE['SSC_QUARRY_OBSpredicted']= T_SSC_QUARRY_OBS_RMSE['NTUmeasured']*QUARRY_OBSrating.beta[0]+QUARRY_OBSrating.beta[1]
T_SSC_QUARRY_OBS_RMSE['SSC_diff'] = T_SSC_QUARRY_OBS_RMSE['SSCmeasured']-T_SSC_QUARRY_OBS_RMSE['SSC_QUARRY_OBSpredicted']
T_SSC_QUARRY_OBS_RMSE['SSC_diffsquared'] = (T_SSC_QUARRY_OBS_RMSE['SSC_diff'])**2
T_SSC_QUARRY_OBS_RMSE['SSC_RMSE'] = T_SSC_QUARRY_OBS_RMSE['SSC_diffsquared']**0.5
T_SSC_QUARRY_OBS_RMSE_Value = (T_SSC_QUARRY_OBS_RMSE['SSC_RMSE'].mean())
#### ..
#### TURBIDITY TO SSC to SEDFLUX
### LBJ Turbidity
## resample to 15min to match Q records
LBJ_YSI15minute = LBJ_YSI.resample('15Min',how='mean',label='right')
LBJ_OBS15minute = LBJ_OBS.resample('15Min',how='mean',label='right')
LBJntu15minute = pd.DataFrame({'NTU':LBJ_YSI15minute['NTU'],'FNU':LBJ_OBS15minute['FNU']},index=pd.date_range(start2012,stop2014,freq='15Min'))
#LBJntu = m.rolling_mean(LBJntu,window=3) ## Smooth out over 3 observations (45min) after already averaged to 5Min

## Both YSI and OBS data resampled to 15minutes and converted to SSC
LBJ['YSI-NTU']=LBJntu15minute['NTU']
LBJ['NTU-SSC']=LBJ_YSIrating.beta[0] * LBJntu15minute['NTU'] + LBJ_YSIrating.beta[1]
LBJ['OBS-FNU']=LBJntu15minute['FNU']
LBJ['OBS-FNU-2013']=LBJntu15minute['FNU'][start2013:stop2013]
LBJ['OBS-FNU-2014']=LBJntu15minute['FNU'][start2014:stop2014]
LBJ['FNU-SSC-2013']=LBJ_OBS_2013rating.beta[0] * LBJ['OBS-FNU-2013'] + LBJ_OBS_2013rating.beta[1]
LBJ['FNU-SSC-2014']=LBJ_OBS_2014rating.beta[0] * LBJ['OBS-FNU-2014'] + LBJ_OBS_2014rating.beta[1]

### LBJ SedFlux
LBJ['SSC-mg/L'] = pd.concat([LBJ['NTU-SSC'].dropna(),LBJ['FNU-SSC-2013'].dropna(),LBJ['FNU-SSC-2014'].dropna()])
LBJ['SedFlux-mg/sec']=LBJ['Q'] * LBJ['SSC-mg/L']# Q(L/sec) * C (mg/L) = mg/sec
LBJ['SedFlux-tons/sec']=LBJ['SedFlux-mg/sec']*(10**-9) ## mg x 10**-6 = tons
LBJ['SedFlux-tons/15min']=LBJ['SedFlux-tons/sec']*900. ## 15min x 60sec/min = 900sec -> tons/sec * 900sec/15min = tons/15min

### QUARRY Turbidity
QUARRY_OBS15minute = QUARRY_OBS.resample('15Min',how='mean',label='right')
QUARRY['OBS-FNU'] = QUARRY_OBS15minute['FNU']
### QUARRY SedFlux
QUARRY['SSC-mg/L'] = QUARRY_OBSrating.beta[0] * QUARRY['OBS-FNU'] + QUARRY_OBSrating.beta[1]
QUARRY['SedFlux-mg/sec']=QUARRY['Q'] * QUARRY['SSC-mg/L']# Q(L/sec) * C (mg/L) = mg/sec
QUARRY['SedFlux-tons/sec']=QUARRY['SedFlux-mg/sec']*(10**-9) ## mg x 10**-6 = tons
QUARRY['SedFlux-tons/15min']=QUARRY['SedFlux-tons/sec']*900. ## 15min x 60sec/min = 900sec -> tons/sec * 900sec/15min = tons/15min

### DAM Turbidity
## resample to 15min to match Q records
DAM_TS3K15minute = DAM_TS3K.resample('15Min',how='mean',label='right') ## Resample to 15 minutes for the SedFlux calc
DAM_YSI15minute = DAM_YSI.resample('15Min',how='mean',label='right')
DAMntu15minute =  pd.DataFrame(pd.concat([DAM_TS3K15minute['NTU'],DAM_YSI15minute['NTU']])).reindex(pd.date_range(start2012,stop2014,freq='15Min'))
### DAM SedFlux
DAM['TS3k-NTU']=DAM_TS3K15minute['NTU']
DAM['YSI-NTU']=DAM_YSI15minute['NTU']
## Both TS3K and YSI data resampled to 15minutes
DAM['NTU']=DAMntu15minute['NTU']

## DAM SedFlux
DAM['SSC-mg/L']=DAM_YSIrating.beta[0] * DAM['NTU']# + DAM_YSIrating.beta[1]
DAM['SedFlux-mg/sec']=DAM['Q'] * DAM['SSC-mg/L']# Q(L/sec) * C (mg/L)
DAM['SedFlux-tons/sec']=DAM['SedFlux-mg/sec']*(10**-9) ## mg x 10**-6 = tons
DAM['SedFlux-tons/15min']=DAM['SedFlux-tons/sec']*900. ## 15min x 60sec/min = 900sec -> tons/sec * 900sec/15min = tons/15min

### Grab samples to SSYev   
def InterpolateGrabSamples(Stormslist,Data,offset=0):
    Events=pd.DataFrame()
    for storm_index,storm in Stormslist.iterrows():
        #print storm
        start = storm['start']-dt.timedelta(minutes=offset) ##if Storms are defined by stream response you have to grab the preceding precip data
        end= storm['end']
        #print str(start)+' '+str(end)
        try:
            event = Data['SSC (mg/L)'].ix[start:end] ### slice list of Data for event
        except KeyError:
            #print 'Data Error'+str(start)
            pass
        ## Test for valid data
        if len(event.dropna())<3:
            #print 'Not enough data for storm '+str(start)
            pass
        elif len(event.dropna())>=3:
            #print 'Interpolating data for storm '+str(start)
            event.ix[start] = 0
            event.ix[end]=0
            Event=pd.DataFrame({'Grab':event})
            Event['GrabInterpolated']=Event['Grab'].interpolate('linear')
            Events = Events.append(Event)
        #Events = Events.drop_duplicates().reindex(pd.date_range(start2012,stop2014,freq='15Min'))
    return Events
    
## LBJ
LBJGrabSampleSSC=InterpolateGrabSamples(LBJ_StormIntervals, LBJgrab,60)      
LBJ['Grab-SSC-mg/L'] = LBJGrabSampleSSC['GrabInterpolated']
LBJ['Grab-SedFlux-mg/sec']=LBJ['Q'] * LBJ['Grab-SSC-mg/L']# Q(L/sec) * C (mg/L)
LBJ['Grab-SedFlux-tons/sec']=LBJ['Grab-SedFlux-mg/sec']*(10**-9) ## mg x 10**-6 = tons
LBJ['Grab-SedFlux-tons/15min']=LBJ['Grab-SedFlux-tons/sec']*900. ## 15min x 60sec/min = 900sec -> tons/sec * 900sec/15min = tons/15min
LBJ['SedFlux-tons/15min']=LBJ['SedFlux-tons/15min'].where(LBJ['SedFlux-tons/15min']>=0,LBJ['Grab-SedFlux-tons/15min'])
 
## QUARRY
QuarryGrabSampleSSC=InterpolateGrabSamples(QUARRY_StormIntervals, QUARRYgrab,60)   
R2GrabSampleSSC=InterpolateGrabSamples(QUARRY_StormIntervals, R2grab,60) 
QUARRY['Grab-SSC-mg/L'] = QuarryGrabSampleSSC['GrabInterpolated']
QUARRY['Grab-SedFlux-mg/sec']=QUARRY['Q'] * QUARRY['Grab-SSC-mg/L']# Q(L/sec) * C (mg/L)
QUARRY['Grab-SedFlux-tons/sec']=QUARRY['Grab-SedFlux-mg/sec']*(10**-9) ## mg x 10**-6 = tons
QUARRY['Grab-SedFlux-tons/15min']=QUARRY['Grab-SedFlux-tons/sec']*900. ## 15min x 60sec/min = 900sec -> tons/sec * 900sec/15min = tons/15min  
QUARRY['SedFlux-tons/15min']=QUARRY['SedFlux-tons/15min'].where(QUARRY['SedFlux-tons/15min']>=0,QUARRY['Grab-SedFlux-tons/15min'])

## DAM
DAMGrabSampleSSC=InterpolateGrabSamples(DAM_StormIntervals, DAMgrab,60) 
DAM['Grab-SSC-mg/L'] = DAMGrabSampleSSC['GrabInterpolated']
DAM['Grab-SedFlux-mg/sec']=DAM['Q'] * DAM['Grab-SSC-mg/L']# Q(L/sec) * C (mg/L)
DAM['Grab-SedFlux-tons/sec']=DAM['Grab-SedFlux-mg/sec']*(10**-9) ## mg x 10**-6 = tons
DAM['Grab-SedFlux-tons/15min']=DAM['Grab-SedFlux-tons/sec']*900. ## 15min x 60sec/min = 900sec -> tons/sec * 900sec/15min = tons/15min  
DAM['SedFlux-tons/15min']=DAM['SedFlux-tons/15min'].where(DAM['SedFlux-tons/15min']>=0,DAM['Grab-SedFlux-tons/15min'])

def plot_eventSSCinterpolated(GrabSamples,show=False):
    fig, ax = plt.subplots(1)

    ## Plot all grab samples
    ax.plot_date(QUARRYgrab.index,QUARRYgrab['SSC (mg/L)'],marker='o',ls='None',color='grey', label='All Grab Samples')
    ## Plot samples that are interpolated    
    ax.plot_date(QuarryGrabSampleSSC.index,QuarryGrabSampleSSC['Grab'],marker='o',ls='None',color='k',label='Interpolated Grab Samples')
    ## Plot continuous SSC    
    ax.plot_date(QuarryGrabSampleSSC.index,QuarryGrabSampleSSC['GrabInterpolated'],marker='None',ls='-',color='y',label='Interpolation')
    ## Shade Storms    
    showstormintervals(ax,LBJ_storm_threshold,LBJ_StormIntervals)
    
    if show==True:
        plt.show()
    return
#plot_eventSSCinterpolated(QuarryGrabSampleSSC,show=True)
#plot_eventSSCinterpolated(R2GrabSampleSSC,show=True)


def plot_T_BOTH(show=False,lwidth=0.5):
    fig, (precip, Q, ntu) = plt.subplots(3,1,sharex=True)
    mpl.rc('lines',markersize=10,linewidth=lwidth)
    ##Precip
    precip.plot_date(PrecipFilled.index,PrecipFilled['Precip'],ls='steps-post',marker='None',c='b',label='Precip-Filled')
    ##Discharge
    Q.plot_date(LBJ['Q'].index,LBJ['Q'],ls='-',marker='None',c='r',label='VILLAGE Q')
    Q.plot_date(DAM['Q'].index,DAM['Q'],ls='-',marker='None',c='g',label='FOREST Q')
    Q.axhline(y=66,ls='--',color='k')
    ## Total storm sediment flux (Mg)
    #sed = fig.add_axes(Q.get_position(), frameon=False, sharex=Q)
    
    #SedFluxStorms_diff = SedFluxStorms_LBJ['Ssum'] - SedFluxStorms_DAM['Ssum']
    #SedFluxStorms_diff = SedFluxStorms_diff.dropna()
    #sed.plot_date(SedFluxStorms_LBJ['Ssum'].index,SedFluxStorms_LBJ['Ssum'],ls='None',marker='o',color='r')
    #sed.plot_date(SedFluxStorms_DAM['Ssum'].index,SedFluxStorms_DAM['Ssum'],ls='None',marker='o',color='g')
    #sed.plot_date(SedFluxStorms_diff.index,SedFluxStorms_diff,ls='None',marker='o',color='y')
    
    #sed.yaxis.set_ticks_position('right')
    #sed.yaxis.set_label_position('right')
    #sed.set_ylabel('Total Storm SedFlux (Mg)')
    
    ##Turbidity
    ntu.plot_date(LBJntu15minute.index,LBJntu15minute,ls='-',marker='None',c='r',label='VILLAGE 15min NTU')
    ntu.plot_date(DAMntu15minute.index,DAMntu15minute,ls='-',marker='None',c='g',label='FOREST 15min NTU')
    ##plot all Grab samples at location 
    ssc = fig.add_axes(ntu.get_position(), frameon=False, sharex=ntu,sharey=ntu)
    ssc.plot_date(LBJgrab.index,LBJgrab['SSC (mg/L)'],'.',markeredgecolor='grey',color='r',label='VILLAGE SSC grab')
    ssc.plot_date(QUARRYgrab.index,QUARRYgrab['SSC (mg/L)'],'.',markeredgecolor='grey',color='y',label='QUARRY SSC grab')
    ssc.plot_date(DAMgrab.index,DAMgrab['SSC (mg/L)'],'.',markeredgecolor='grey',color='g',label='FOREST SSC grab')    
    ##plot Grab samples used for rating
    ssc.yaxis.set_ticks_position('right'),ssc.yaxis.set_label_position('right')
    ssc.set_ylabel('SSC (mg/L)'),ssc.legend(loc='upper right')
    ## Shade storm intervals
    showstormintervals(precip,LBJ_storm_threshold, LBJ_StormIntervals)
    showstormintervals(Q, LBJ_storm_threshold, LBJ_StormIntervals,shade_color='r')
    showstormintervals(ntu,DAM_storm_threshold, DAM_StormIntervals,shade_color='g')

    precip.set_ylabel('Precip (mm/15min)'),precip.legend()
    Q.set_ylabel('Discharge (L/sec)'),Q.set_ylim(0,LBJ['Q'].max()+100),Q.legend()
    ntu.set_ylabel('Turbidity (NTU)'),ntu.set_ylim(0,LBJntu15minute['NTU'].max()),ntu.legend(loc='upper left')
    plt.suptitle('Precipitation, Discharge, Turbidity and SSC at FOREST and VILLAGE',fontsize=14)
    plt.draw()
    if show==True:
        plt.show()
    return
#plot_T_BOTH(True,lwidth=0.5)

def plotNTUratingstable(show=False,save=False):
    ## NTU
    ## Lab
    LAB = linearfunction(SSC[SSC['Location']=='LBJ']['NTU'],SSC[SSC['Location']=='LBJ']['SSC (mg/L)'])
    lab = ['%.2f'%LAB['a'],'%.2f'%LAB['b'],'%.2f'%LAB['r2'],'%.2f'%LAB['pearson'],'%.2f'%LAB['spearman'],'%.2f'%LAB['rmse']]
    ## LBJ YSI
    LBJ_YSI=linearfunction(T_SSC_LBJ_YSI[1]['LBJ-YSI-NTU'],T_SSC_LBJ_YSI[1]['SSC (mg/L)'])
    lbj_ysi = ['%.2f'%LBJ_YSI['a'],'%.2f'%LBJ_YSI['b'],'%.2f'%LBJ_YSI['r2'],'%.2f'%LBJ_YSI['pearson'],'%.2f'%LBJ_YSI['spearman'],'%.2f'%LBJ_YSI['rmse']]
    ## DAM TS3000
    DAM_TS3K = linearfunction(T_SSC_DAM_TS3K[1]['DAM-TS3K-NTU'],T_SSC_DAM_TS3K[1]['SSC (mg/L)'])
    dam_ts3k = ['%.2f'%DAM_TS3K['a'],'%.2f'%DAM_TS3K['b'],'%.2f'%DAM_TS3K['r2'],'%.2f'%DAM_TS3K['pearson'],'%.2f'%DAM_TS3K['spearman'],'%.2f'%DAM_TS3K['rmse']]
    ## DAM YSI
    DAM_YSI = linearfunction(T_SSC_DAM_YSI[1]['DAM-YSI-NTU'],T_SSC_DAM_YSI[1]['SSC (mg/L)'])
    dam_ysi = ['%.2f'%DAM_YSI['a'],'%.2f'%DAM_YSI['b'],'%.2f'%DAM_YSI['r2'],'%.2f'%DAM_YSI['pearson'],'%.2f'%DAM_YSI['spearman'],'%.2f'%DAM_YSI['rmse']]    
    
    ## FNU
    ## LBJ OBS
    LBJ_OBS_2013 = linearfunction(T_SSC_LBJ_OBS_2013[1]['LBJ-OBS-FNU'],T_SSC_LBJ_OBS_2013[1]['SSC (mg/L)'])
    lbj_obs_2013 = ['%.2f'%LBJ_OBS_2013['a'],'%.2f'%LBJ_OBS_2013['b'],'%.2f'%LBJ_OBS_2013['r2'],'%.2f'%LBJ_OBS_2013['pearson'],'%.2f'%LBJ_OBS_2013['spearman'],'%.2f'%LBJ_OBS_2013['rmse']]    

    LBJ_OBS_2014 = linearfunction(T_SSC_LBJ_OBS_2014[1]['LBJ-OBS-FNU'],T_SSC_LBJ_OBS_2014[1]['SSC (mg/L)'])
    lbj_obs_2014 = ['%.2f'%LBJ_OBS_2014['a'],'%.2f'%LBJ_OBS_2014['b'],'%.2f'%LBJ_OBS_2014['r2'],'%.2f'%LBJ_OBS_2014['pearson'],'%.2f'%LBJ_OBS_2014['spearman'],'%.2f'%LBJ_OBS_2014['rmse']]    

    ## QUARRY OBS
    QUARRY_OBS = linearfunction(T_SSC_QUARRY_OBS[1]['QUARRY-OBS-FNU'],T_SSC_QUARRY_OBS[1]['SSC (mg/L)'])
    qua_obs = ['%.2f'%QUARRY_OBS['a'],'%.2f'%QUARRY_OBS['b'],'%.2f'%QUARRY_OBS['r2'],'%.2f'%QUARRY_OBS['pearson'],'%.2f'%QUARRY_OBS['spearman'],'%.2f'%QUARRY_OBS['rmse']]    
 
     
    nrows, ncols = 3,6
    hcell, wcell=0.3,1
    hpad, wpad = 1,1
    fig = plt.figure(figsize=(ncols*wcell+wpad,nrows*hcell+hpad)) 
    coeff = fig.add_subplot(111)
    coeff.patch.set_visible(False), coeff.axis('off')
    coeff.xaxis.set_visible(False), coeff.yaxis.set_visible(False) 
    coeff.table(cellText = [lab,lbj_ysi,lbj_obs_2013,lbj_obs_2014,qua_obs,dam_ts3k,dam_ysi],rowLabels=['Lab','VILL-YSI','VILL-OBS-2013','VILL-OBS-2014','QUA-OBS','FOR-TS3K','FOR-YSI'],colLabels=[r'$\alpha$',r'$\beta$',r'$r^2$',"Pearson's","Spearman's",'RMSE'],loc='center left')
    
    plt.suptitle('Paramters for Turbidity to Suspended Sediment Concetration Rating Curves',fontsize=16)    
    
    plt.draw()
    if show==True:
        plt.show()
    return
#plotNTUratingstable(show=True,save=False)


def plotNTUratings(plot_param_table=True,show=False,log=False,save=False,lwidth=0.3,ms=10):
    #fig, (lab,ntu,fnu) = plt.subplots(1,3,sharex=True,sharey=True,) 
    fig =plt.figure(figsize=(14,6))
    lab = plt.subplot2grid((2,3),(0,0))
    ntu = plt.subplot2grid((2,3),(0,1))
    fnu = plt.subplot2grid((2,3),(0,2))
    param_table = plt.subplot2grid((2,3),(1,0),colspan=3)
    
    xy = np.linspace(0,2000)
    mpl.rc('lines',markersize=ms,linewidth=lwidth)
    dotsize=50
    
    ## All Samples LAB
    lab.scatter(SSC['NTU'],SSC['SSC (mg/L)'],s=dotsize,color='b',marker='v',label='LAB',edgecolors='grey')
    lab.plot(xy,xy*T_SSC_Lab.beta[0]+T_SSC_Lab.beta[1],ls='-',c='b',label='LAB')
    lab.grid(True),lab.set_ylabel('SSC (mg/L)'),lab.set_xlabel('Turbidity (NTU)'),lab.legend(fancybox=True,ncol=2)
    lab.set_xlim(-5,2000), lab.set_ylim(0,2000)
    ## Grab Samples: LBJ-YSI, DAM-TS3k, DAM-YSI
    ntu.scatter(T_SSC_LBJ_YSI[1]['LBJ-YSI-NTU'],T_SSC_LBJ_YSI[1]['SSC (mg/L)'],s=dotsize,color='r',marker='o',label='VILLAGE-YSI',edgecolors='grey')
    ntu.scatter(T_SSC_DAM_TS3K[1]['DAM-TS3K-NTU'],T_SSC_DAM_TS3K[1]['SSC (mg/L)'],s=dotsize,color='g',marker='o',label='FOREST-TS3K',edgecolors='grey')
    ntu.scatter(T_SSC_DAM_YSI[1]['DAM-YSI-NTU'],T_SSC_DAM_YSI[1]['SSC (mg/L)'],s=dotsize,color='g',marker='v',label='FOREST-YSI',edgecolors='grey')
    ## NTU ratings LBJ-YSI, DAM-YSI, DAM-TS3K  
    ntu.plot(xy,xy*LBJ_YSIrating.beta[0]+LBJ_YSIrating.beta[1],ls='-',c='r',label='VILLAGE-YSI rating')
    #ntu.plot(xy,xy*DAM_TS3Krating.beta[0]+DAM_TS3Krating.beta[1],ls='-',c='g',label='FOREST-TS3K rating')
    ntu.plot(xy,xy*DAM_YSIrating.beta[0]+DAM_YSIrating.beta[1],ls='--',c='g',label='FOREST-YSI rating')
    ## Format NTU
    ntu.grid(True), ntu.set_xlim(-5,2000), ntu.set_ylim(0,2000), ntu.set_ylabel('SSC (mg/L)'),ntu.set_xlabel('Turbidity (NTU)'),ntu.legend(fancybox=True,ncol=2)
    ## FNU LBJ-OBS, QUARRY-OBS
    fnu.scatter(T_SSC_LBJ_OBS_2013[1]['LBJ-OBS-FNU'],T_SSC_LBJ_OBS_2013[1]['SSC (mg/L)'],s=dotsize,color='y',marker='.',label='VILLAGE-OBS-2013',edgecolors='grey')
    fnu.plot(xy,xy*LBJ_OBS_2013rating.beta[0]+LBJ_OBS_2013rating.beta[1],ls='-',c='y',label='VILLAGE-OBS-2013 rating')
    
    fnu.scatter(T_SSC_LBJ_OBS_2014[1]['LBJ-OBS-FNU'],T_SSC_LBJ_OBS_2014[1]['SSC (mg/L)'],s=dotsize,color='r',marker='.',label='VILLAGE-OBS-2014',edgecolors='grey')
    fnu.plot(xy,xy*LBJ_OBS_2014rating.beta[0]+LBJ_OBS_2014rating.beta[1],ls='-',c='r',label='VILLAGE-OBS-2014 rating')

    fnu.scatter(T_SSC_QUARRY_OBS[1]['QUARRY-OBS-FNU'],T_SSC_QUARRY_OBS[1]['SSC (mg/L)'],s=dotsize,color='grey',marker='.',label='VILLAGE-OBS',edgecolors='grey')
    fnu.plot(xy,xy*QUARRY_OBSrating.beta[0]+QUARRY_OBSrating.beta[1],ls='-',c='grey',label='QUARRY-OBS rating')

    ## Format FNU
    fnu.grid(True), fnu.set_xlabel('Turbidity (FNU)'), fnu.legend(fancybox=True,ncol=2)
    fnu.set_xlim(-5,2000), fnu.set_ylim(0,2000),
    #labelindex_subplot(ts3k,T_SSC_LBJ_OBS[1].index,T_SSC_LBJ_OBS[1]['LBJ-OBS-NTU'],T_SSC_LBJ_OBS[1]['SSC (mg/L)'])    
    #labelindex_subplot(ts3k,T_SSC_LBJ_YSI[1].index,T_SSC_LBJ_YSI[1]['LBJ-YSI-NTU'],T_SSC_LBJ_OBS[1]['SSC (mg/L)'])
    title = 'Turbidity to Suspended Sediment Concetration Rating Curves'
    #plt.suptitle(title,fontsize=16) 
    ## TABLE
    if plot_param_table == True:
        ## NTU
        LAB = linearfunction(SSC[SSC['Location']=='LBJ']['NTU'],SSC[SSC['Location']=='LBJ']['SSC (mg/L)'])
        LBJ_YSI=linearfunction(T_SSC_LBJ_YSI[1]['LBJ-YSI-NTU'],T_SSC_LBJ_YSI[1]['SSC (mg/L)'])
        DAM_TS3K = linearfunction(T_SSC_DAM_TS3K[1]['DAM-TS3K-NTU'],T_SSC_DAM_TS3K[1]['SSC (mg/L)'])
        DAM_YSI = linearfunction(T_SSC_DAM_YSI[1]['DAM-YSI-NTU'],T_SSC_DAM_YSI[1]['SSC (mg/L)'])
        ## FNU
        LBJ_OBS_2013 = linearfunction(T_SSC_LBJ_OBS_2013[1]['LBJ-OBS-FNU'],T_SSC_LBJ_OBS_2013[1]['SSC (mg/L)'])
        LBJ_OBS_2014 = linearfunction(T_SSC_LBJ_OBS_2014[1]['LBJ-OBS-FNU'],T_SSC_LBJ_OBS_2014[1]['SSC (mg/L)'])
        QUA_OBS = linearfunction(T_SSC_QUARRY_OBS[1]['QUARRY-OBS-FNU'],T_SSC_QUARRY_OBS[1]['SSC (mg/L)'])        
        ## ROW/COLUMN Data
        lab = ['%.2f'%LAB['a'],'%.2f'%LAB['b'],'%.2f'%LAB['r2'],'%.2f'%LAB['pearson'],'%.2f'%LAB['spearman'],'%.2f'%LAB['rmse']]
        lbj_ysi = ['%.2f'%LBJ_YSI['a'],'%.2f'%LBJ_YSI['b'],'%.2f'%LBJ_YSI['r2'],'%.2f'%LBJ_YSI['pearson'],'%.2f'%LBJ_YSI['spearman'],'%.2f'%LBJ_YSI['rmse']]
        lbj_obs_2013 = ['%.2f'%LBJ_OBS_2013['a'],'%.2f'%LBJ_OBS_2013['b'],'%.2f'%LBJ_OBS_2013['r2'],'%.2f'%LBJ_OBS_2013['pearson'],'%.2f'%LBJ_OBS_2013['spearman'],'%.2f'%LBJ_OBS_2013['rmse']]    
        lbj_obs_2014 = ['%.2f'%LBJ_OBS_2014['a'],'%.2f'%LBJ_OBS_2014['b'],'%.2f'%LBJ_OBS_2014['r2'],'%.2f'%LBJ_OBS_2014['pearson'],'%.2f'%LBJ_OBS_2014['spearman'],'%.2f'%LBJ_OBS_2014['rmse']]    
        qua_obs = ['%.2f'%QUA_OBS['a'],'%.2f'%QUA_OBS['b'],'%.2f'%QUA_OBS['r2'],'%.2f'%QUA_OBS['pearson'],'%.2f'%QUA_OBS['spearman'],'%.2f'%QUA_OBS['rmse']]    
        dam_ts3k = ['%.2f'%DAM_TS3K['a'],'%.2f'%DAM_TS3K['b'],'%.2f'%DAM_TS3K['r2'],'%.2f'%DAM_TS3K['pearson'],'%.2f'%DAM_TS3K['spearman'],'%.2f'%DAM_TS3K['rmse']]
        dam_ysi = ['%.2f'%DAM_YSI['a'],'%.2f'%DAM_YSI['b'],'%.2f'%DAM_YSI['r2'],'%.2f'%DAM_YSI['pearson'],'%.2f'%DAM_YSI['spearman'],'%.2f'%DAM_YSI['rmse']]    
        ## Plot Table
        param_table.patch.set_visible(False), param_table.axis('off')
        param_table.xaxis.set_visible(False), param_table.yaxis.set_visible(False) 
        param_table.table(cellText = [lab,lbj_ysi,lbj_obs_2013,lbj_obs_2014,qua_obs,dam_ts3k,dam_ysi],rowLabels=['Lab','VILL-YSI','VILL-OBS-2013','VILL-OBS-2014','QUA-OBS','FOR-TS3K','FOR-YSI'],colLabels=[r'$\alpha$',r'$\beta$',r'$r^2$',"Pearson's","Spearman's",'RMSE'],loc='center left')
        ## Adjust subplots    
        plt.subplots_adjust(left=0.08, bottom=0,hspace=0.01)
    else:
        plt.tight_layout()
    
    plt.draw()
    if show==True:
        plt.show()
    return
plotNTUratings(plot_param_table=True,show=True,log=False,save=True,lwidth=0.5,ms=20)
    

#### ..
#### EVENT-WISE ANALYSES

#### Integrate over P and Q over Storm Event
#from HydrographTools_revert import StormSums
## LBJ P and Q
Pstorms_LBJ = StormSums(LBJ_StormIntervals,PrecipFilled['Precip'],60) ##30minute offset to get precip before stage started rising
Pstorms_LBJ.columns=['Pstart','Pend','Pcount','Psum','Pmax']
Pstorms_LBJ['EI'] = LBJ_Stormdf['EI']
Qstorms_LBJ=StormSums(LBJ_StormIntervals,LBJq['Q']) 
Qstorms_LBJ.columns=['Qstart','Qend','Qcount','Qsum','Qmax']
Qstorms_LBJ['Qmax']=Qstorms_LBJ['Qmax']/900 ## Have to divide by 900 to get instantaneous 

## QUARRY P and Q
Pstorms_QUARRY = StormSums(QUARRY_StormIntervals,PrecipFilled['Precip'],60) ##30minute offset to get precip before stage started rising
Pstorms_QUARRY.columns=['Pstart','Pend','Pcount','Psum','Pmax']
Pstorms_QUARRY['EI'] = QUARRY_Stormdf['EI']
Qstorms_QUARRY= StormSums(QUARRY_StormIntervals,QUARRYq['Q']) 
Qstorms_QUARRY.columns=['Qstart','Qend','Qcount','Qsum','Qmax']
Qstorms_QUARRY['Qmax']=Qstorms_QUARRY['Qmax']/900 ## Have to divide by 900 to get instantaneous 

## DAM P and Q
Pstorms_DAM = StormSums(DAM_StormIntervals,PrecipFilled['Precip'],60) ##30minute offset to get precip before stage started rising
Pstorms_DAM.columns=['Pstart','Pend','Pcount','Psum','Pmax']
Pstorms_DAM['EI'] = DAM_Stormdf['EI']
Qstorms_DAM= StormSums(DAM_StormIntervals,DAMq['Q']) 
Qstorms_DAM.columns=['Qstart','Qend','Qcount','Qsum','Qmax']
Qstorms_DAM['Qmax']=Qstorms_DAM['Qmax']/900 ## Have to divide by 900 to get instantaneous 

#### Event Runoff Coefficient
### LBJ Runoff Coeff
StormsLBJ = Pstorms_LBJ[Pstorms_LBJ['Psum']>0].join(Qstorms_LBJ)
## Event precip x Area = Event Precip Volume: Psum/1000 (mm to m) * 1.78*1000000 (km2 to m2) *1000 (m3 to L)
StormsLBJ['PsumVol'] = (StormsLBJ['Psum']/1000)*(1.78*1000000)*1000  
StormsLBJ['RunoffCoeff']=StormsLBJ['Qsum']/StormsLBJ['PsumVol']
### DAM Runoff Coeff
StormsDAM=Pstorms_DAM[Pstorms_DAM['Psum']>0].join(Qstorms_DAM)
## Event precip x Area = Event Precip Volume: Psum/1000 (mm to m) * 1.78*1000000 (km2 to m2) *1000 (m3 to L)
StormsDAM['PsumVol'] = (StormsDAM['Psum']/1000)*(0.9*1000000)*1000  
StormsDAM['RunoffCoeff']=StormsDAM['Qsum']/StormsDAM['PsumVol']
 
## Calculate the percent of total Q with raw vales, BEFORE NORMALIZING by area!
def plotQ_storm_table(show=False):
    diff = ALLStorms.dropna()
    ## Calculate percent contributions from upper and lower watersheds
    diff['Qupper']=diff['Qsumupper'].apply(np.int)
    diff['Qlower']=diff['Qsumlower'].apply(np.int)
    diff['Qtotal']=diff['Qsumtotal'].apply(np.int)
    diff['% Upper'] = diff['Qupper']/diff['Qtotal']*100
    diff['% Upper'] = diff['% Upper'].round(0)
    diff['% Lower'] = diff['Qlower']/diff['Qtotal']*100
    diff['% Lower'] = diff['% Lower'].round(0)
    diff['Psum'] = diff['Pstorms'].apply(np.int)
    diff['Storm#']=range(1,len(diff)+1)
    ## add summary stats to bottom of table
    diff=diff.append(pd.DataFrame({'Storm#':'-','Psum':'-','Qupper':'-','Qlower':'-','Qtotal':'Average:','% Upper':'%.1f'%diff['% Upper'].mean(),'% Lower':'%.1f'%diff['% Lower'].mean()},index=['']))
   
    nrows, ncols = len(diff),len(diff.columns)
    hcell, wcell=0.2,1
    hpad, wpad = .8,.5
    fig = plt.figure(figsize=(ncols*wcell+wpad,nrows*hcell+hpad)) 
    ax = fig.add_subplot(111)
    ax.patch.set_visible(False), ax.axis('off')
    ax.xaxis.set_visible(False), ax.yaxis.set_visible(False)
    plt.suptitle("Discharge (Q) from Upstream (DAM) and Downstream (LBJ) watersheds in Faga'alu")
 
    celldata = np.array(diff[['Storm#','Psum','Qupper','Qlower','Qtotal','% Upper','% Lower']].values)
    
    ax.table(cellText=celldata,rowLabels=[pd.to_datetime(t) for t in diff.index.values],colLabels=['Storm#','Precip(mm)','Upper(m3)','Lower(m3)','Total(m3)','%Upper','%Lower'],loc='center')
    
    plt.draw()
    if show==True:
        plt.show()
    return
#plotQ_storm_table(True)

#### Event Sediment Flux Data
def stormdata(StormIntervals,print_stats=False):
    storm_data = pd.DataFrame(columns=['Precip','LBJq','DAMq','LBJssc','DAMssc','LBJ-Sed','DAM-Sed','LBJgrab','QUARRYgrab','DAMgrab'],dtype=np.float64,index=pd.date_range(PT1.index[0],PT1.index[-1],freq='15Min'))   
    storm_data=pd.DataFrame()
    count = 0
    for storm in StormIntervals.iterrows():
        count+=1
        start = storm[1]['start']-dt.timedelta(minutes=60)
        end =  storm[1]['end']
        #print start, end
        ## Slice data from storm start to start end
        data = pd.DataFrame({'Precip':Precip['Timu1-15'][start:end],
        'LBJq':LBJ['Q'][start:end],'QUARRYq':QUARRY['Q'][start:end],'DAMq':DAM['Q'][start:end],
        'LBJntu':LBJ['YSI-NTU'],'LBJfnu':LBJ['OBS-FNU'],'DAMntu':DAM['NTU'],        
        'LBJssc':LBJ['SSC-mg/L'][start:end],'QUARRYssc':QUARRY['SSC-mg/L'][start:end],'DAMssc':DAM['SSC-mg/L'][start:end],
        'LBJgrabssc':LBJ['Grab-SSC-mg/L'][start:end],'QUARRYgrabssc':QUARRY['Grab-SSC-mg/L'][start:end],'DAMgrabssc':DAM['Grab-SSC-mg/L'][start:end],        
        'LBJ-Sed':LBJ['SedFlux-tons/15min'][start:end],'QUARRY-Sed':QUARRY['SedFlux-tons/15min'][start:end],
        'DAM-Sed':DAM['SedFlux-tons/15min'][start:end],
        'LBJgrab':LBJgrab['SSC (mg/L)'][start:end],'QUARRYgrab':QUARRYgrab['SSC (mg/L)'][start:end],
        'DAMgrab':DAMgrab['SSC (mg/L)'][start:end]},index=pd.date_range(start,end,freq='15Min')) ## slice desired data by storm 
        ## Summary stats
        total_storm = len(data[start:end])
        percent_P = len(data['Precip'].dropna())/total_storm *100.
        percent_Q_LBJ = len(data['LBJq'].dropna())/total_storm * 100.
        percent_Q_DAM = len(data['DAMq'].dropna())/total_storm * 100.
        percent_SSC_LBJ = len(data['LBJssc'].dropna())/total_storm * 100.
        percent_SSC_DAM = len(data['DAMssc'].dropna())/total_storm * 100.
        count_LBJgrab = len(LBJgrab.dropna())
        count_QUARRYgrab = len(QUARRYgrab.dropna())
        count_DAMgrab = len(DAMgrab.dropna())
        if print_stats==True:
            print str(start)+' '+str(end)+' Storm#:'+str(count)
            print '%P:'+str(percent_P)+' %Q_LBJ:'+str(percent_Q_LBJ)+' %Q_DAM:'+str(percent_Q_DAM)
            print '%SSC_LBJ:'+str(percent_SSC_LBJ)+' %SSC_DAM:'+str(percent_SSC_DAM)
            print '#LBJgrab:'+str(count_LBJgrab)+' #QUARRYgrab:'+str(count_QUARRYgrab)+' #DAMgrab:'+str(count_DAMgrab)        
        ## Calculate Event Mean Concentration
        if len(data['DAMgrab'])>=3:
            data['sEMC-DAM']=data['DAMgrab'].mean()
        if len(data['QUARRYgrab'])>=3:
            data['sEMC-QUARRY']=data['QUARRYgrab'].mean()
        if len(data['QUARRYgrab'])>=3:
            data['sEMC-LBJ']=data['LBJgrab'].mean()
        ## Make sure data is complete for storms
        if percent_Q_LBJ <= 95:
            data['LBJq'] = np.nan
        if percent_Q_DAM <= 95:
            data['DAMq'] = np.nan
        if percent_SSC_LBJ <= 95:
            data['LBJssc'] = np.nan
        if percent_SSC_LBJ <= 95:
            data['LBJssc'] = np.nan
        if percent_SSC_DAM <= 95:
            data['DAMssc'] = np.nan
        if data['LBJ-Sed'].sum() < 0:
            data['LBJ-Sed'] = np.nan
        if data['LBJ-Sed'].sum() < 0:
            data['LBJ-Sed'] = np.nan
        storm_data = storm_data.append(data) ## add each storm to each other
    storm_data = storm_data.drop_duplicates().reindex(pd.date_range(start2012,stop2014,freq='15Min'))
    return storm_data
storm_data_LBJ = stormdata(LBJ_StormIntervals)
storm_data_QUARRY = stormdata(QUARRY_StormIntervals)
storm_data_DAM = stormdata(DAM_StormIntervals)


def Q_EMC(storm_data, show=False):
    fig, qemc = plt.subplots(1,1)
    #Plot event mean concentration
    storm_data['sEMC-LBJ'].dropna().plot(ax=qemc,c='r',marker='o',ls='None')
    storm_data['sEMC-QUARRY'].dropna().plot(ax=qemc,c='y',marker='o',ls='None')
    storm_data['sEMC-DAM'].dropna().plot(ax=qemc,c='g',marker='o',ls='None')
    #Plot grab samples
    storm_data['LBJgrab'].plot(ax=qemc,color='r',marker='o',ls='None',markersize=6,label='LBJ-grab')
    storm_data['QUARRYgrab'].plot(ax=qemc,color='y',marker='o',ls='None',markersize=6,label='QUARRY-grab')
    storm_data['DAMgrab'].plot(ax=qemc,color='g',marker='o',ls='None',markersize=6,label='DAM-grab')
    
    showstormintervals(qemc,LBJ_storm_threshold,LBJ_StormIntervals)
    plt.grid()
    
    plt.draw()
    if show==True:
        plt.show()
    return
#Q_EMC(storm_data_LBJ,True)

def Storm_SedFlux(storm_data,storm_threshold,storm_intervals,title,show=False):

    fig, (P,Q,T,SSC,SED) = plt.subplots(nrows=5,ncols=1,sharex=True)
    ## Precip
    storm_data['Precip'].plot(ax=P,color='b',ls='steps-pre',label='Timu1')
    P.set_ylabel('Precip mm/15min.')
    ## Discharge
    storm_data['LBJq'].plot(ax=Q,color='r',label='LBJ-Q')
    storm_data['QUARRYq'].plot(ax=Q,color='y',label='QUARRY-Q')
    storm_data['DAMq'].plot(ax=Q,color='g',label='DAM-Q')
    Q.set_ylabel('Q m^3/15min.')#, Q.set_yscale('log')
    ## Turbidity
    storm_data['LBJntu'].plot(ax=T,color='r',label='LBJ-NTU')
    storm_data['LBJfnu'].plot(ax=T,color='r',alpha=0.8,label='LBJ-FNU')
    storm_data['DAMntu'].plot(ax=T,color='g',label='DAM-NTU')
    T.set_ylabel('T (NTU,FNU)'),T.set_ylim(-1)
    ## SSC from turbidity
    storm_data['LBJssc'].plot(ax=SSC,color='r',label='LBJ-SSC')
    storm_data['QUARRYssc'].plot(ax=SSC,color='y',label='QUARRY-SSC')
    storm_data['DAMssc'].plot(ax=SSC,color='g',label='DAM-SSC')
    ### SSC interpolated from grab samples
    storm_data['LBJgrabssc'].plot(ax=SSC,ls='--',color='r',label='LBJ-SSC')
    storm_data['QUARRYgrabssc'].plot(ax=SSC,ls='--',color='y',label='QUARRY-SSC')
    storm_data['DAMgrabssc'].plot(ax=SSC,ls='--',color='g',label='DAM-SSC')
    ## SSC grab samples
    storm_data['LBJgrab'].plot(ax=SSC,color='r',marker='o',ls='None',markersize=6,label='LBJ-grab')
    storm_data['QUARRYgrab'].plot(ax=SSC,color='y',marker='o',ls='None',markersize=6,label='QUARRY-grab')
    storm_data['DAMgrab'].plot(ax=SSC,color='g',marker='o',ls='None',markersize=6,label='DAM-grab')
    SSC.set_ylabel('SSC mg/L')#, SSC.set_ylim(0,1400)
    
    
    ## Sediment discharge
    storm_data['LBJ-Sed'].plot(ax=SED,color='r',label='LBJ-SedFlux',ls='-')
    storm_data['QUARRY-Sed'].plot(ax=SED,color='y',label='QUARRY-SedFlux',ls='-')
    storm_data['DAM-Sed'].plot(ax=SED,color='g',label='DAM-SedFlux',ls='-')
    SED.set_ylabel('Sediment Flux (Mg/15minutes)')#, SED.set_yscale('log')#, SED.set_ylim(0,10)
    #QP.legend(loc=0), P.legend(loc=1)             
    #SSC.legend(loc=0),SED.legend(loc=1)
    #Shade Storms
    showstormintervals(P,storm_threshold,storm_intervals)
    showstormintervals(Q,storm_threshold,storm_intervals)
    showstormintervals(T,storm_threshold,storm_intervals)
    showstormintervals(SSC,storm_threshold,storm_intervals)
    showstormintervals(SED,storm_threshold,storm_intervals)
    
    plt.suptitle(title)
    if show==True:
        plt.show()
    return
Storm_SedFlux(storm_data_LBJ,LBJ_storm_threshold,LBJ_StormIntervals,'LBJ_StormIntervals',True)
Storm_SedFlux(storm_data_DAM,DAM_storm_threshold,DAM_StormIntervals,'DAM_StormIntervals',True)

def plot_storms_individually(storm_threshold,storm_intervals):
    count = 0
    for storm in storm_intervals.iterrows():
        count+=1
        start = storm[1]['start']-dt.timedelta(minutes=60)
        end =  storm[1]['end']+dt.timedelta(minutes=60)
        #print start, end
        ## Slice data from storm start to start end
        storm_data = pd.DataFrame({'Precip':Precip['Timu1-15'][start:end],
        'LBJq':LBJ['Q'][start:end],'QUARRYq':QUARRY['Q'][start:end],'DAMq':DAM['Q'][start:end],
        'LBJntu':LBJ['YSI-NTU'],'LBJfnu':LBJ['OBS-FNU'],'QUARRYfnu':QUARRY['OBS-FNU'],'DAMntu':DAM['NTU'],
        'LBJssc':LBJ['SSC-mg/L'][start:end],'QUARRYssc':QUARRY['SSC-mg/L'][start:end],'DAMssc':DAM['SSC-mg/L'][start:end],
        'LBJgrabssc':LBJ['Grab-SSC-mg/L'][start:end],'QUARRYgrabssc':QUARRY['Grab-SSC-mg/L'][start:end],'DAMgrabssc':DAM['Grab-SSC-mg/L'][start:end],        
        'LBJ-Sed':LBJ['SedFlux-tons/15min'][start:end],'QUARRY-Sed':QUARRY['SedFlux-tons/15min'][start:end],'DAM-Sed':DAM['SedFlux-tons/15min'][start:end],
        'LBJgrab':LBJgrab['SSC (mg/L)'][start:end],'QUARRYgrab':QUARRYgrab['SSC (mg/L)'][start:end],'DAMgrab':DAMgrab['SSC (mg/L)'][start:end]},
        index=pd.date_range(start,end,freq='15Min'))
        total_storm = len(storm_data[start:end])
        percent_P = len(storm_data['Precip'].dropna())/total_storm *100.
        percent_Q_LBJ = len(storm_data['LBJq'].dropna())/total_storm * 100.
        percent_Q_DAM = len(storm_data['DAMq'].dropna())/total_storm * 100.
        percent_SSC_LBJ = len(storm_data['LBJssc'].dropna())/total_storm * 100.
        percent_SSC_QUARRY = len(storm_data['QUARRYssc'].dropna())/total_storm * 100.
        percent_SSC_DAM = len(storm_data['DAMssc'].dropna())/total_storm * 100.
        count_LBJgrab = len(LBJgrab.dropna())
        count_QUARRYgrab = len(QUARRYgrab.dropna())
        count_DAMgrab = len(DAMgrab.dropna())
        print str(start)+' '+str(end)+' Storm#:'+str(count)
        #print '%P:'+str(percent_P)+' %Q_LBJ:'+str(percent_Q_LBJ)+' %Q_DAM:'+str(percent_Q_DAM)
        #print '%SSC_LBJ:'+str(percent_SSC_LBJ)+' %SSC_DAM:'+str(percent_SSC_DAM)
        #print '#LBJgrab:'+str(count_LBJgrab)+' #QUARRYgrab:'+str(count_QUARRYgrab)+' #DAMgrab:'+str(count_DAMgrab)        
        
        ##Plotting per storm
        plt.ioff()
        fig, (P,Q,T,SSC,SED) = plt.subplots(nrows=5,ncols=1,sharex=True,figsize=(15,15))
        
        plt.suptitle('Storm: '+str(count)+' start: '+str(start)+' end: '+str(end), fontsize=22)
        ## Precip
        storm_data['Precip'].plot(ax=P,color='b',ls='steps-pre',label='Timu1')
        P_max, P_sum = storm_data['Precip'].max(), storm_data['Precip'].sum()
        P.set_ylabel('Precip mm'),P.set_ylim(-1,Precip['Timu1-15'].max()+2)

        ## Discharge
        storm_data['LBJq'].plot(ax=Q,color='r',label='LBJ-Q')
        LBJ_Qmax, LBJ_Qmean, LBJ_Qsum = storm_data['LBJq'].max(), storm_data['LBJq'].mean(), storm_data['LBJq'].sum()
        storm_data['QUARRYq'].plot(ax=Q,color='y',label='QUARRY-Q')
        QUARRY_Qmax, QUARRY_Qmean, QUARRY_Qsum = storm_data['QUARRYq'].max(), storm_data['QUARRYq'].mean(),storm_data['QUARRYq'].sum()
        storm_data['DAMq'].plot(ax=Q,color='g',label='DAM-Q')
        DAM_Qmax, DAM_Qmean, DAM_Qsum = storm_data['DAMq'].max(), storm_data['DAMq'].mean(), storm_data['DAMq'].sum()
        Q.set_ylabel('Q L/sec'), Q.set_ylim(-1,6000)
        ## Turbidity
        storm_data['LBJntu'].plot(ax=T,color='r',label='LBJ-NTU')
        LBJ_NTUmax, LBJ_NTUmean = storm_data['LBJntu'].max(), storm_data['LBJntu'].mean()
        storm_data['LBJfnu'].plot(ax=T,color='y',label='LBJ-FNU')
        LBJ_FNUmax, LBJ_FNUmean = storm_data['LBJfnu'].max(), storm_data['LBJfnu'].mean()
        storm_data['QUARRYfnu'].plot(ax=T,color='y',label='QUARRY-FNU')
        QUARRY_FNUmax, QUARRY_FNUmean = storm_data['QUARRYfnu'].max(), storm_data['QUARRYfnu'].mean()
        storm_data['DAMntu'].plot(ax=T,color='g',label='DAM-NTU')
        DAM_NTUmax, DAM_NTUmean, DAM_NTUsum = storm_data['DAMntu'].max(), storm_data['DAMntu'].mean()
        T.set_ylabel('T (NTU,FNU)'),T.set_ylim(-1,2000)
        ## SSC and grab samples
        storm_data['LBJssc'].plot(ax=SSC,color='r',label='LBJ-SSC')
        LBJ_SSCmax, LBJ_SSCmean = storm_data['LBJssc'].max(), storm_data['LBJssc'].mean()
        storm_data['QUARRYssc'].plot(ax=SSC,color='y',label='QUARRY-SSC')
        QUARRY_SSCmax, QUARRY_SSCmean = storm_data['QUARRYssc'].max(), storm_data['QUARRYssc'].mean()
        storm_data['DAMssc'].plot(ax=SSC,color='g',label='DAM-SSC')
        DAM_SSCmax, DAM_SSCmean = storm_data['DAMssc'].max(), storm_data['DAMssc'].mean()
        ## Grabs
        storm_data['LBJgrab'].plot(ax=SSC,color='r',marker='o',ls='None',markersize=6,label='LBJ-grab')
        storm_data['QUARRYgrab'].plot(ax=SSC,color='y',marker='o',ls='None',markersize=6,label='QUARRY-grab')
        storm_data['DAMgrab'].plot(ax=SSC,color='g',marker='o',ls='None',markersize=6,label='DAM-grab')
        SSC.set_ylabel('SSC mg/L'), SSC.set_ylim(-1,1500)
        ### SSC interpolated from grab samples
        storm_data['LBJgrabssc'].plot(ax=SSC,ls='--',color='r',label='LBJ-SSC')
        LBJ_SSCgrabmax, LBJ_SSCgrabmean = storm_data['LBJgrabssc'].max(), storm_data['LBJgrabssc'].mean()
        storm_data['QUARRYgrabssc'].plot(ax=SSC,ls='--',color='y',label='QUARRY-SSC')
        QUARRY_SSCgrabmax, QUARRY_SSCgrabmean = storm_data['QUARRYgrabssc'].max(), storm_data['QUARRYgrabssc'].mean()
        storm_data['DAMgrabssc'].plot(ax=SSC,ls='--',color='g',label='DAM-SSC')
        DAM_SSCgrabmax, DAM_SSCgrabmean = storm_data['DAMgrabssc'].max(), storm_data['DAMgrabssc'].mean()
        ## Sediment discharge
        storm_data['LBJ-Sed'].plot(ax=SED,color='r',label='LBJ-SedFlux',ls='-')
        LBJ_Smax, LBJ_Smean, LBJ_Ssum = storm_data['LBJ-Sed'].max(), storm_data['LBJ-Sed'].mean(), storm_data['LBJSed'].sum()
        storm_data['QUARRY-Sed'].plot(ax=SED,color='y',label='QUARRY-SedFlux',ls='-')
        QUARRY_Smax, QUARRY_Smean, QUARRY_Ssum = storm_data['QUARRY-Sed'].max(), storm_data['QUARRY-Sed'].mean(), storm_data['QUARRYSed'].sum()
        storm_data['DAM-Sed'].plot(ax=SED,color='g',label='DAM-SedFlux',ls='-')
        DAM_Smax, DAM_Smean, DAM_Ssum = storm_data['DAM-Sed'].max(), storm_data['DAM-Sed'].mean(), storm_data['DAMSed'].sum()
        SED.set_ylabel('SSY tons'), SED.set_ylim(-.1,4000)
        
        #P.legend(loc='best'), 
        Q.legend(loc='best',ncol=2), T.legend(loc='best',ncol=3)          
        SSC.legend(loc='best',ncol=5),SED.legend(loc='best',ncol=2)
        
        #Shade Storms
        shade_color='grey'
        start, end = storm[1]['start'], storm[1]['end']
        P.axvspan(start,end,ymin=0,ymax=200,facecolor=shade_color, alpha=0.25), Q.axvspan(start,end,ymin=0,ymax=200,facecolor=shade_color, alpha=0.25)
        T.axvspan(start,end,ymin=0,ymax=200,facecolor=shade_color, alpha=0.25), SSC.axvspan(start,end,ymin=0,ymax=200,facecolor=shade_color, alpha=0.25)
        SED.axvspan(start,end,ymin=0,ymax=200,facecolor=shade_color, alpha=0.25)
        
        plt.tight_layout()        
    
        title='Storm_'+str(count)+' '+str(start.year)+'-'+str(start.month)+'-'+str(start.day)
        plt.savefig(figdir+'storm_figures/'+title)
        plt.close('all')
    plt.ion()
    return
plot_storms_individually(LBJ_storm_threshold,LBJ_StormIntervals)      

#### Event Sediment Flux
#### LBJ Event-wise Sediment Flux DataFrame
SedFluxStorms_LBJ = StormSums(LBJ_StormIntervals,LBJ['SedFlux-tons/15min'])
SedFluxStorms_LBJ.columns = ['Sstart','Send','Scount','Ssum','Smax']
SedFluxStorms_LBJ=Pstorms_LBJ.join(SedFluxStorms_LBJ) ## Add Event S (which will be fewer events than Event Precip)
SedFluxStorms_LBJ=SedFluxStorms_LBJ.join(Qstorms_LBJ) ## Add Event Discharge
#### QUARRY Event-wise Sediment Flux DataFrame
SedFluxStorms_QUARRY = StormSums(QUARRY_StormIntervals,QUARRY['SedFlux-tons/15min'])
SedFluxStorms_QUARRY.columns = ['Sstart','Send','Scount','Ssum','Smax']
SedFluxStorms_QUARRY=Pstorms_QUARRY.join(SedFluxStorms_QUARRY)#Add Event S (which will be fewer events than Event Precip)
SedFluxStorms_QUARRY=SedFluxStorms_QUARRY.join(Qstorms_QUARRY)
#### DAM Event-wise Sediment Flux DataFrame
SedFluxStorms_DAM = StormSums(DAM_StormIntervals,DAM['SedFlux-tons/15min'])
SedFluxStorms_DAM.columns = ['Sstart','Send','Scount','Ssum','Smax']
SedFluxStorms_DAM=Pstorms_DAM.join(SedFluxStorms_DAM)#Add Event S (which will be fewer events than Event Precip)
SedFluxStorms_DAM=SedFluxStorms_DAM.join(Qstorms_DAM)


#### EDITED STORMS LIST
#### LBJ Event-wise Sediment Flux DataFrame
SedFluxStorms_LBJ = StormSums(LBJ_StormIntervals,storm_data_LBJ['LBJ-Sed'])
SedFluxStorms_LBJ.columns = ['Sstart','Send','Scount','Ssum','Smax']
SedFluxStorms_LBJ=Pstorms_LBJ.join(SedFluxStorms_LBJ) ## Add Event S (which will be fewer events than Event Precip)
SedFluxStorms_LBJ=SedFluxStorms_LBJ.join(Qstorms_LBJ) ## Add Event Discharge
#### QUARRY Event-wise Sediment Flux DataFrame
SedFluxStorms_QUARRY = StormSums(DAM_StormIntervals,storm_data_QUARRY['QUARRY-Sed'])
SedFluxStorms_QUARRY.columns = ['Sstart','Send','Scount','Ssum','Smax']
SedFluxStorms_QUARRY=Pstorms_QUARRY.join(SedFluxStorms_QUARRY)#Add Event S (which will be fewer events than Event Precip)
SedFluxStorms_QUARRY=SedFluxStorms_QUARRY.join(Qstorms_QUARRY)
#### DAM Event-wise Sediment Flux DataFrame
SedFluxStorms_DAM = StormSums(DAM_StormIntervals,storm_data_DAM['DAM-Sed'])
SedFluxStorms_DAM.columns = ['Sstart','Send','Scount','Ssum','Smax']
SedFluxStorms_DAM=Pstorms_DAM.join(SedFluxStorms_DAM)#Add Event S (which will be fewer events than Event Precip)
SedFluxStorms_DAM=SedFluxStorms_DAM.join(Qstorms_DAM)
    
#### Calculate correlation coefficients and sediment rating curves    
def compileALLStorms():
    ALLStorms=pd.DataFrame({'Supper':SedFluxStorms_DAM['Ssum'],
    'Slower':SedFluxStorms_LBJ['Ssum']-SedFluxStorms_DAM['Ssum'],
    'Stotal':SedFluxStorms_LBJ['Ssum']})
    
    ## Qsum
    ALLStorms['Qsumtotal']=SedFluxStorms_LBJ['Qsum']
    ALLStorms['Qsumupper']=SedFluxStorms_DAM['Qsum']
    ALLStorms['Qsumlower']=SedFluxStorms_LBJ['Qsum']-SedFluxStorms_DAM['Qsum']
    
    ## Qmax
    ALLStorms['Qmaxupper']=SedFluxStorms_DAM['Qmax']
    ALLStorms['Qmaxlower']=SedFluxStorms_LBJ['Qmax']
    ALLStorms['Qmaxtotal']=SedFluxStorms_LBJ['Qmax']
    
    ## Add Event Precipitation and EI
    ALLStorms['Pstorms']=Pstorms_LBJ['Psum'] ## Add Event Precip
    #ALLStorms['EI'] = LBJ_Stormdf['EI'][LBJ_Stormdf['EI']>1] ## Add Event Erosion Index
    return ALLStorms
ALLStorms = compileALLStorms()

## Calculate the percent of total SSY with raw vales, BEFORE NORMALIZING by area!
def plotS_storm_table(show=False):
    diff = ALLStorms.dropna()
    ## Calculate percent contributions from upper and lower watersheds
    diff['Supper']=diff['Supper'].apply(np.int)
    diff['Slower']=diff['Slower'].apply(np.int)
    diff['Stotal']=diff['Stotal'].apply(np.int)
    diff['% Upper'] = diff['Supper']/diff['Stotal']*100
    diff['% Upper'] = diff['% Upper'].apply(np.int)
    diff['% Lower'] = diff['Slower']/diff['Stotal']*100
    diff['% Lower'] = diff['% Lower'].apply(np.int)
    diff['Psum'] = diff['Pstorms'].apply(int)
    diff['Storm#']=range(1,len(diff)+1) 
    ## Filter negative values for S at LBJ    
    diff = diff[diff['Slower']>0]
    ## add summary stats to bottom of table
    diff=diff.append(pd.DataFrame({'Storm#':'-','Psum':'-','Supper':'-','Slower':'-','Stotal':'Average:','% Upper':'%.1f'%diff['% Upper'].mean(),'% Lower':'%.1f'%diff['% Lower'].mean()},index=[pd.NaT]))

    ## BUild table
    nrows, ncols = len(diff),len(diff.columns)
    hcell, wcell=0.2,1
    hpad, wpad = .8,.5
    fig = plt.figure(figsize=(ncols*wcell+wpad,nrows*hcell+hpad)) 
    ax = fig.add_subplot(111)
    ax.patch.set_visible(False), ax.axis('off')
    ax.xaxis.set_visible(False), ax.yaxis.set_visible(False)
    plt.suptitle("Sediment Loading from subwatersheds in Faga'alu",fontsize=16)
 
    celldata = np.array(diff[['Storm#','Psum','Supper','Slower','Stotal','% Upper','% Lower']].values)
    rowlabels=[pd.to_datetime(t).strftime('%Y %b %d %H:%M') for t in diff.index[diff.index!=pd.NaT].values]
    rowlabels.extend([None])
    ax.table(cellText=celldata,rowLabels=rowlabels,colLabels=['Storm#','Precip(mm)','Upper (Mg)','Lower (Mg)','Total (Mg)','%Upper','%Lower'],loc='center',fontsize=16)
    
    plt.draw()
    if show==True:
        plt.show()
    return
#plotS_storm_table(show=True)

def NormalizeSSYbyCatchmentArea(ALLStorms):
    ## DAM = 0.9 km2
    ## QUARRY = 1.17 km2
    ## LBJ = 1.78 km2
    ## Normalize Sediment Load by catchment area (Duvert 2012)
    ALLStorms['Supper']=ALLStorms['Supper']/.9
    ALLStorms['Slower']=ALLStorms['Slower']/.88
    ALLStorms['Stotal']=ALLStorms['Stotal']/1.78
    ## Add Event Discharge ad Normalize by catchment area
    ALLStorms['Qsumlower']=SedFluxStorms_LBJ['Qsum']-SedFluxStorms_DAM['Qsum']
    ALLStorms['Qsumupper']=SedFluxStorms_DAM['Qsum']/.9 
    ALLStorms['Qsumlower']=ALLStorms['Qsumlower']/.88
    ALLStorms['Qsumtotal']=SedFluxStorms_LBJ['Qsum']/1.78
    ## Duvert (2012) Fig. 3 shows SSY (Qmax m3/s/km2 vs. Mg/km2); but shows correlation coefficients in Qmax m3/s vs SSY Mg (table )
    ALLStorms['Qmaxupper']=SedFluxStorms_DAM['Qmax']/.9
    ALLStorms['Qmaxlower']=SedFluxStorms_LBJ['Qmax']/.88
    ALLStorms['Qmaxtotal']=SedFluxStorms_LBJ['Qmax']/1.78
    ## Add Event Precipitation and EI
    ALLStorms['Pstorms']=Pstorms_LBJ['Psum'] ## Add Event Precip
    #ALLStorms['EI'] = LBJ_Stormdf['EI'][LBJ_Stormdf['EI']>1] ## Add Event Erosion Index
    return ALLStorms

def plotPearsonTable(SedFluxStorms_DAM=SedFluxStorms_DAM,SedFluxStorms_LBJ=SedFluxStorms_LBJ,ALLStorms=ALLStorms,pval=0.05,show=False):
    nrows, ncols = 3,4
    hcell, wcell=0.3,1
    hpad, wpad = 1,1
    fig = plt.figure(figsize=(ncols*wcell+wpad,nrows*hcell+hpad)) 
    pearson = fig.add_subplot(111)
    pearson.patch.set_visible(False), pearson.axis('off')
    pearson.xaxis.set_visible(False), pearson.yaxis.set_visible(False) 

        
    SedFluxStorms_DAM = SedFluxStorms_DAM.dropna()
    SedFluxStorms_LBJ= SedFluxStorms_LBJ.dropna()
    ALLStorms = ALLStorms[ALLStorms['Slower']>0].dropna()
    
    pvalue=pval
    ## Psum vs. Ssum
    
    if pearson_r(SedFluxStorms_DAM['Psum'],SedFluxStorms_DAM['Ssum'])[1] < pvalue:
        Upper_Psum_Ssum_Pearson_r = '%.2f'%pearson_r(SedFluxStorms_DAM['Psum'],SedFluxStorms_DAM['Ssum'])[0]
    if pearson_r(ALLStorms['Pstorms'],ALLStorms['Slower'])[1] < pvalue:
        Lower_Psum_Ssum_Pearson_r = '%.2f'%pearson_r(ALLStorms['Pstorms'],ALLStorms['Slower'])[0]
    if pearson_r(SedFluxStorms_LBJ['Psum'],SedFluxStorms_LBJ['Ssum'])[1] < pvalue:
        Total_Psum_Ssum_Pearson_r = '%.2f'%pearson_r(SedFluxStorms_LBJ['Psum'],SedFluxStorms_LBJ['Ssum'])[0]
    ## EI vs. Ssum
    if pearson_r(SedFluxStorms_DAM['EI'],SedFluxStorms_DAM['Ssum'])[1] < pvalue:
        Upper_EI_Ssum_Pearson_r = '%.2f'%pearson_r(SedFluxStorms_DAM['EI'],SedFluxStorms_DAM['Ssum'])[0]
    elif pearson_r(SedFluxStorms_DAM['EI'],SedFluxStorms_DAM['Ssum'])[1] >= pvalue:
        Upper_EI_Ssum_Pearson_r = ' ' 
    if pearson_r(ALLStorms['EI'],ALLStorms['Slower'])[1] < pvalue:
        Lower_EI_Ssum_Pearson_r = '%.2f'%pearson_r(ALLStorms['EI'],ALLStorms['Slower'])[0]
    elif pearson_r(ALLStorms['EI'],ALLStorms['Slower'])[1] >= pvalue:
        Lower_EI_Ssum_Pearson_r = ' ' 
    if pearson_r(SedFluxStorms_LBJ['EI'],SedFluxStorms_LBJ['Ssum'])[1] < pvalue:
        Total_EI_Ssum_Pearson_r = '%.2f'%pearson_r(SedFluxStorms_LBJ['EI'],SedFluxStorms_LBJ['Ssum'])[0]
    elif pearson_r(SedFluxStorms_LBJ['EI'],SedFluxStorms_LBJ['Ssum'])[1] >= pvalue:
        Total_EI_Ssum_Pearson_r = ' ' 
    ## Qsum vs. Ssum
    if pearson_r(SedFluxStorms_DAM['Qsum'],SedFluxStorms_DAM['Ssum'])[1] < pvalue:
        Upper_Qsum_Ssum_Pearson_r = '%.2f'%pearson_r(SedFluxStorms_DAM['Qsum'],SedFluxStorms_DAM['Ssum'])[0]
    if pearson_r(ALLStorms['Qsumlower'],ALLStorms['Slower'])[1] < pvalue:
        Lower_Qsum_Ssum_Pearson_r = '%.2f'%pearson_r(ALLStorms['Qsumlower'],ALLStorms['Slower'])[0]
    if pearson_r(SedFluxStorms_LBJ['Qsum'],SedFluxStorms_LBJ['Ssum'])[1] < pvalue:
        Total_Qsum_Ssum_Pearson_r = '%.2f'%pearson_r(SedFluxStorms_LBJ['Qsum'],SedFluxStorms_LBJ['Ssum'])[0]
    elif pearson_r(SedFluxStorms_LBJ['Qsum'],SedFluxStorms_LBJ['Ssum'])[1] >= pvalue:
        Total_Qsum_Ssum_Pearson_r =' '
    ## Qmaxvs. Ssum
    if pearson_r(SedFluxStorms_DAM['Qmax'],SedFluxStorms_DAM['Ssum'])[1] < pvalue:
        Upper_Qmax_Ssum_Pearson_r = '%.2f'%pearson_r(SedFluxStorms_DAM['Qmax'],SedFluxStorms_DAM['Ssum'])[0]
    if pearson_r(ALLStorms['Qmaxlower'],ALLStorms['Slower'])[1] < pvalue:
        Lower_Qmax_Ssum_Pearson_r = '%.2f'%pearson_r(ALLStorms['Qmaxlower'],ALLStorms['Slower'])[0]
    if pearson_r(SedFluxStorms_LBJ['Qmax'],SedFluxStorms_LBJ['Ssum'])[1] < pvalue:
        Total_Qmax_Ssum_Pearson_r = '%.2f'%pearson_r(SedFluxStorms_LBJ['Qmax'],SedFluxStorms_LBJ['Ssum'])[0]
    
    ## Put data together, and put in table
    PsumS = [Upper_Psum_Ssum_Pearson_r,Lower_Psum_Ssum_Pearson_r,Total_Psum_Ssum_Pearson_r]
    EIS = [Upper_EI_Ssum_Pearson_r,Lower_EI_Ssum_Pearson_r,Total_EI_Ssum_Pearson_r]
    QsumS = [Upper_Qsum_Ssum_Pearson_r,Lower_Qsum_Ssum_Pearson_r,Total_Qsum_Ssum_Pearson_r]
    QmaxS = [Upper_Qmax_Ssum_Pearson_r,Lower_Qmax_Ssum_Pearson_r,Total_Qmax_Ssum_Pearson_r]
    pearson.table(cellText = [PsumS,EIS,QsumS,QmaxS],rowLabels=['Psum','EI','Qsum','Qmax'],colLabels=['Upper','Lower','Total'],loc='center left')
    
    plt.suptitle("Pearson's coefficients for each variable\n as compared to SSY (Mg), p<"+str(pvalue),fontsize=12)  
    plt.draw()
    if show==True:
        plt.show()
    return
#plotPearsonTable(pval=0.05,show=True)

def plotSpearmanTable(SedFluxStorms_DAM=SedFluxStorms_DAM,SedFluxStorms_LBJ=SedFluxStorms_LBJ,ALLStorms=ALLStorms,pval=0.05,show=False):
    nrows, ncols = 3,4
    hcell, wcell=0.3,1
    hpad, wpad = 1,1
    fig = plt.figure(figsize=(ncols*wcell+wpad,nrows*hcell+hpad)) 
    spearman = fig.add_subplot(111)
    spearman.patch.set_visible(False), spearman.axis('off')
    spearman.xaxis.set_visible(False), spearman.yaxis.set_visible(False) 
    
        
    SedFluxStorms_DAM = SedFluxStorms_DAM.dropna()
    SedFluxStorms_LBJ= SedFluxStorms_LBJ.dropna()
    ALLStorms = ALLStorms[ALLStorms['Slower']>0].dropna()
    
    pvalue=pval
    ## Psum vs. Ssum
    if spearman_r(SedFluxStorms_DAM['Psum'],SedFluxStorms_DAM['Ssum'])[1] < pvalue:
        Upper_Psum_Ssum_Spearman_r = '%.2f'%spearman_r(SedFluxStorms_DAM['Psum'],SedFluxStorms_DAM['Ssum'])[0]
    if spearman_r(ALLStorms['Pstorms'],ALLStorms['Slower'])[1] < pvalue:
        Lower_Psum_Ssum_Spearman_r = '%.2f'%spearman_r(ALLStorms['Pstorms'],ALLStorms['Slower'])[0]
    if spearman_r(SedFluxStorms_LBJ['Psum'],SedFluxStorms_LBJ['Ssum'])[1] < pvalue:
        Total_Psum_Ssum_Spearman_r = '%.2f'%spearman_r(SedFluxStorms_LBJ['Psum'],SedFluxStorms_LBJ['Ssum'])[0]
    ## EI vs. Ssum
    if spearman_r(SedFluxStorms_DAM['EI'],SedFluxStorms_DAM['Ssum'])[1] < pvalue:
        Upper_EI_Ssum_Spearman_r = '%.2f'%spearman_r(SedFluxStorms_DAM['EI'],SedFluxStorms_DAM['Ssum'])[0]
    elif spearman_r(SedFluxStorms_DAM['EI'],SedFluxStorms_DAM['Ssum'])[1] >= pvalue:
        Upper_EI_Ssum_Spearman_r = ' ' 
    if spearman_r(ALLStorms['EI'],ALLStorms['Slower'])[1] < pvalue:
        Lower_EI_Ssum_Spearman_r = '%.2f'%spearman_r(ALLStorms['EI'],ALLStorms['Slower'])[0]
    elif spearman_r(ALLStorms['EI'],ALLStorms['Slower'])[1] >= pvalue:
        Lower_EI_Ssum_Spearman_r = ' ' 
    if spearman_r(SedFluxStorms_LBJ['EI'],SedFluxStorms_LBJ['Ssum'])[1] < pvalue:
        Total_EI_Ssum_Spearman_r = '%.2f'%spearman_r(SedFluxStorms_LBJ['EI'],SedFluxStorms_LBJ['Ssum'])[0]
    elif spearman_r(SedFluxStorms_LBJ['EI'],SedFluxStorms_LBJ['Ssum'])[1] >= pvalue:
        Total_EI_Ssum_Spearman_r = ' ' 
    ## Qsum vs. Ssum
    if spearman_r(SedFluxStorms_DAM['Qsum'],SedFluxStorms_DAM['Ssum'])[1] < pvalue:
        Upper_Qsum_Ssum_Spearman_r = '%.2f'%spearman_r(SedFluxStorms_DAM['Qsum'],SedFluxStorms_DAM['Ssum'])[0]
    if spearman_r(ALLStorms['Qsumlower'],ALLStorms['Slower'])[1] < pvalue:
        Lower_Qsum_Ssum_Spearman_r = '%.2f'%spearman_r(ALLStorms['Qsumlower'],ALLStorms['Slower'])[0]
    elif spearman_r(ALLStorms['Qsumlower'],ALLStorms['Slower'])[1] >= pvalue:
        Lower_Qsum_Ssum_Spearman_r = ' '
    if spearman_r(SedFluxStorms_LBJ['Qsum'],SedFluxStorms_LBJ['Ssum'])[1] < pvalue:
        Total_Qsum_Ssum_Spearman_r = '%.2f'%spearman_r(SedFluxStorms_LBJ['Qsum'],SedFluxStorms_LBJ['Ssum'])[0]
    elif spearman_r(SedFluxStorms_LBJ['Qsum'],SedFluxStorms_LBJ['Ssum'])[1] >= pvalue:
        Total_Qsum_Ssum_Spearman_r =' '
    ## Qmaxvs. Ssum
    if spearman_r(SedFluxStorms_DAM['Qmax'],SedFluxStorms_DAM['Ssum'])[1] < pvalue:
        Upper_Qmax_Ssum_Spearman_r = '%.2f'%spearman_r(SedFluxStorms_DAM['Qmax'],SedFluxStorms_DAM['Ssum'])[0]
    if spearman_r(ALLStorms['Qmaxlower'],ALLStorms['Slower'])[1] < pvalue:
        Lower_Qmax_Ssum_Spearman_r = '%.2f'%spearman_r(ALLStorms['Qmaxlower'],ALLStorms['Slower'])[0]
    if spearman_r(SedFluxStorms_LBJ['Qmax'],SedFluxStorms_LBJ['Ssum'])[1] < pvalue:
        Total_Qmax_Ssum_Spearman_r = '%.2f'%spearman_r(SedFluxStorms_LBJ['Qmax'],SedFluxStorms_LBJ['Ssum'])[0]
    
    ## Put data together, and put in table
    PsumS = [Upper_Psum_Ssum_Spearman_r,Lower_Psum_Ssum_Spearman_r,Total_Psum_Ssum_Spearman_r]
    EIS = [Upper_EI_Ssum_Spearman_r,Lower_EI_Ssum_Spearman_r,Total_EI_Ssum_Spearman_r]
    QsumS = [Upper_Qsum_Ssum_Spearman_r,Lower_Qsum_Ssum_Spearman_r,Total_Qsum_Ssum_Spearman_r]
    QmaxS = [Upper_Qmax_Ssum_Spearman_r,Lower_Qmax_Ssum_Spearman_r,Total_Qmax_Ssum_Spearman_r]
    spearman.table(cellText = [PsumS,EIS,QsumS,QmaxS],rowLabels=['Psum','EI','Qsum','Qmax'],colLabels=['Upper','Lower','Total'],loc='center left')
    
    plt.suptitle("Spearman's coefficients for each variable\n as compared to SSY (Mg), p<"+str(pvalue),fontsize=12)  
    plt.draw()
    if show==True:
        plt.show()
    return
#plotSpearmanTable(pval=0.001,show=True)
    
 
def plotCoeffTable(show=False,norm=False):
    if norm==True:
        ALLStorms=NormalizeSSYbyCatchmentArea(compileALLStorms())
        Upper = powerfunction(ALLStorms['Qmaxupper']/1000,ALLStorms['Supper'])
        Total = powerfunction(ALLStorms['Qmaxtotal']/1000,ALLStorms['Stotal'])    
        
        Up = ['%.2f'%Upper['a'],'%.2f'%Upper['b'],'%.2f'%Upper['r2'],'%.2f'%Upper['pearson'],'%.2f'%Upper['spearman'],'%.2f'%Upper['rmse']]
        Tot = ['%.2f'%Total['a'],'%.2f'%Total['b'],'%.2f'%Total['r2'],'%.2f'%Total['pearson'],'%.2f'%Total['spearman'],'%.2f'%Total['rmse']]
        
        nrows, ncols = 2,6
        hcell, wcell=0.3,1
        hpad, wpad = 1,1
        fig = plt.figure(figsize=(ncols*wcell+wpad,nrows*hcell+hpad)) 
        coeff = fig.add_subplot(111)
        coeff.patch.set_visible(False), coeff.axis('off')
        coeff.xaxis.set_visible(False), coeff.yaxis.set_visible(False) 
        coeff.table(cellText = [Up,Tot],rowLabels=['Upper','Total'],colLabels=[r'$\alpha$',r'$\beta$',r'$r^2$',"Pearson's","Spearman's",'RMSE'],loc='center left',fontsize=14)
   
    elif norm==False:
        ALLStorms = compileALLStorms()
        Upper = powerfunction(ALLStorms['Qmaxupper']/1000,ALLStorms['Supper'])
        Lower = powerfunction(ALLStorms['Qmaxlower']/1000,ALLStorms['Slower'])    
        Total = powerfunction(ALLStorms['Qmaxtotal']/1000,ALLStorms['Stotal'])
        
        Up = ['%.2f'%Upper['a'],'%.2f'%Upper['b'],'%.2f'%Upper['r2'],'%.2f'%Upper['pearson'],'%.2f'%Upper['spearman'],'%.2f'%Upper['rmse']]
        Low = ['%.2f'%Lower['a'],'%.2f'%Lower['b'],'%.2f'%Lower['r2'],'%.2f'%Lower['pearson'],'%.2f'%Lower['spearman'],'%.2f'%Lower['rmse']]
        Tot = ['%.2f'%Total['a'],'%.2f'%Total['b'],'%.2f'%Total['r2'],'%.2f'%Total['pearson'],'%.2f'%Total['spearman'],'%.2f'%Total['rmse']]    
    
        nrows, ncols = 3,6
        hcell, wcell=0.3,1
        hpad, wpad = 1,1
        fig = plt.figure(figsize=(ncols*wcell+wpad,nrows*hcell+hpad)) 
        coeff = fig.add_subplot(111)
        coeff.patch.set_visible(False), coeff.axis('off')
        coeff.xaxis.set_visible(False), coeff.yaxis.set_visible(False) 
        coeff.table(cellText = [Up,Low,Tot],rowLabels=['Upper','Lower','Total'],colLabels=[r'$\alpha$',r'$\beta$',r'$r^2$',"Pearson's","Spearman's",'RMSE'],loc='center left',fontsize=14)
    
    plt.suptitle("Model parameters for POWER law Qmax-SSYev model: "+r'$SSY_{ev} = \alpha Q^\beta$',fontsize=14)
    plt.draw()
    if show==True:
        plt.show()
    return
#plotCoeffTable(show=True,norm=False)


#### Sediment Rating Curves: on area-normalized SSY, Q and Qmax
def plotALLStorms_ALLRatings(ms=10,show=False,log=False,save=False,norm=False):    
    fig, ((ps,ei),(qsums,qmaxs)) = plt.subplots(2,2)
    title = 'All sediment rating curves for all predictors'
    if norm==True:
        ALLStorms=NormalizeSSYbyCatchmentArea(compileALLStorms())
        ylabel,xlabelP,xlabelEI,xlabelQsum,xlabelQmax = r'$SSY (Mg/km^2)$','Precip (mm)','Erosivity Index',r'$Qsum (L/km^2)$',r'$Qmax (L/sec/km^2)$'
    else:
        ALLStorms=compileALLStorms()
        ylabel,xlabelP,xlabelEI,xlabelQsum,xlabelQmax = 'SSY (Mg)','Precip (mm)','Erosivity Index','Qsum (L)','Qmax (L/sec)'
    xy=None ## let the Fit functions plot their own lines
    #mpl.rc('lines',markersize=ms)
    ## P vs S at Upper,Lower,Total (power)
    ps.plot(ALLStorms['Pstorms'],ALLStorms['Supper'],'.',color='g',label='Upper')
    ps.plot(ALLStorms['Pstorms'],ALLStorms['Slower'],'.',color='y',label='Lower')
    ps.plot(ALLStorms['Pstorms'],ALLStorms['Stotal'],'.',color='r',label='Total')
    ## Upper Watershed (=DAM)
    PS_upper_power = powerfunction(ALLStorms['Pstorms'],ALLStorms['Supper'])
    PowerFit(ALLStorms['Pstorms'],ALLStorms['Supper'],xy,ps,linestyle='-',color='g',label='PS_upper_power')
    PS_upper_linear = linearfunction(ALLStorms['Pstorms'],ALLStorms['Supper'])
    LinearFit(ALLStorms['Pstorms'],ALLStorms['Supper'],xy,ps,linestyle='--',color='g',label='PS_upper_linear')  
    ## Lower Watershed (=LBJ-DAM)
    PS_lower_power = powerfunction(ALLStorms['Pstorms'],ALLStorms['Slower'])
    PowerFit(ALLStorms['Pstorms'],ALLStorms['Slower'],xy,ps,linestyle='-',color='y',label='PS_lower_power') 
    PS_lower_linear = linearfunction(ALLStorms['Pstorms'],ALLStorms['Slower'])
    LinearFit(ALLStorms['Pstorms'],ALLStorms['Slower'],xy,ps,linestyle='--',color='y',label='PS_lower_linear') 
    ## Total Watershed (=LBJ)
    PS_total_power = powerfunction(ALLStorms['Pstorms'],ALLStorms['Stotal'])
    PowerFit(ALLStorms['Pstorms'],ALLStorms['Stotal'],xy,ps,linestyle='-',color='r',label='PS_total_power') 
    PS_total_linear = linearfunction(ALLStorms['Pstorms'],ALLStorms['Stotal'])
    LinearFit(ALLStorms['Pstorms'],ALLStorms['Stotal'],xy,ps,linestyle='--',color='r',label='PS_total_linear') 

    ps.set_title('Total Event Precip (mm)')
    ps.set_ylabel(ylabel)
    
    ## EI vs S at Upper,Lower,Total (power)
    ei.plot(ALLStorms['EI'],ALLStorms['Supper'],'.',color='g',label='Upper')
    ei.plot(ALLStorms['EI'],ALLStorms['Slower'],'.',color='y',label='Lower')
    ei.plot(ALLStorms['EI'],ALLStorms['Stotal'],'.',color='r',label='Total')
    
    EI_upper_power = powerfunction(ALLStorms['EI'],ALLStorms['Supper'])
    PowerFit(ALLStorms['EI'],ALLStorms['Supper'],xy,ei,linestyle='-',color='g',label='EI_upper_power')
    EI_upper_linear = linearfunction(ALLStorms['EI'],ALLStorms['Supper'])
    LinearFit(ALLStorms['EI'],ALLStorms['Supper'],xy,ei,linestyle='--',color='g',label='EI_upper_linear')  
    
    EI_lower_power = powerfunction(ALLStorms['EI'],ALLStorms['Slower'])
    PowerFit(ALLStorms['EI'],ALLStorms['Slower'],xy,ei,linestyle='-',color='y',label='EI_lower_power') 
    EI_lower_linear = linearfunction(ALLStorms['EI'],ALLStorms['Slower'])
    LinearFit(ALLStorms['EI'],ALLStorms['Slower'],xy,ei,linestyle='--',color='y',label='EI_lower_linear') 
    
    EI_total_power = powerfunction(ALLStorms['EI'],ALLStorms['Stotal'])
    PowerFit(ALLStorms['EI'],ALLStorms['Stotal'],xy,ei,linestyle='-',color='r',label='EI_total_power') 
    EI_total_linear = linearfunction(ALLStorms['EI'],ALLStorms['Stotal'])
    LinearFit(ALLStorms['EI'],ALLStorms['Stotal'],xy,ei,linestyle='--',color='r',label='EI_total_linear') 
    
    ei.set_title('Erosivity Index (MJmm ha-1 h-1)')
    ei.set_ylabel(ylabel)

    ## Qsum vs S at Upper,Lower,Total (power)
    qsums.plot(ALLStorms['Qsumupper'],ALLStorms['Supper'],'.',color='g',label='Upper')
    qsums.plot(ALLStorms['Qsumlower'],ALLStorms['Slower'],'.',color='y',label='Lower')
    qsums.plot(ALLStorms['Qsumtotal'],ALLStorms['Stotal'],'.',color='r',label='Total')
    
    QsumS_upper_power = powerfunction(ALLStorms['Qsumupper'],ALLStorms['Supper'])
    PowerFit(ALLStorms['Qsumupper'],ALLStorms['Supper'],xy,qsums,linestyle='-',color='g',label='QsumS_upper_power')
    QsumS_upper_linear = linearfunction(ALLStorms['Qsumupper'],ALLStorms['Supper'])
    LinearFit(ALLStorms['Qsumupper'],ALLStorms['Supper'],xy,qsums,linestyle='--',color='g',label='QsumS_upper_linear')  

    QsumS_lower_power = powerfunction(ALLStorms['Qsumlower'],ALLStorms['Slower'])
    PowerFit(ALLStorms['Qsumlower'],ALLStorms['Slower'],xy,qsums,linestyle='-',color='y',label='QsumS_lower_power') 
    QsumS_lower_linear = linearfunction(ALLStorms['Qsumlower'],ALLStorms['Slower'])
    LinearFit(ALLStorms['Qsumlower'],ALLStorms['Slower'],xy,qsums,linestyle='--',color='y',label='QsumS_lower_linear') 
    
    QsumS_total_power = powerfunction(ALLStorms['Qsumtotal'],ALLStorms['Stotal'])
    PowerFit(ALLStorms['Qsumtotal'],ALLStorms['Stotal'],xy,qsums,linestyle='-',color='r',label='QsumS_total_power') 
    QsumS_total_linear = linearfunction(ALLStorms['Qsumtotal'],ALLStorms['Stotal'])
    LinearFit(ALLStorms['Qsumtotal'],ALLStorms['Stotal'],xy,qsums,linestyle='--',color='r',label='QsumS_total_linear') 
    
    qsums.set_title('Event Q sum')
    qsums.set_ylabel(ylabel), qsums.set_xlabel(xlabelQsum)

    ## Qmax vs S at Upper,Lower,Total (power)
    qmaxs.plot(ALLStorms['Qmaxupper'],ALLStorms['Supper'],'.',color='g',label='Upper')
    qmaxs.plot(ALLStorms['Qmaxlower'],ALLStorms['Slower'],'.',color='y',label='Lower')
    qmaxs.plot(ALLStorms['Qmaxtotal'],ALLStorms['Stotal'],'.',color='r',label='Total')
    
    QmaxS_upper_power = powerfunction(ALLStorms['Qmaxupper'],ALLStorms['Supper'])
    PowerFit(ALLStorms['Qmaxupper'],ALLStorms['Supper'],xy,qmaxs,linestyle='-',color='g',label='QmaxS_upper_power')
    QmaxS_upper_linear = linearfunction(ALLStorms['Qmaxupper'],ALLStorms['Supper'])
    LinearFit(ALLStorms['Qmaxupper'],ALLStorms['Supper'],xy,qmaxs,linestyle='--',color='g',label='QmaxS_upper_linear')  
    
    QmaxS_lower_power = powerfunction(ALLStorms['Qmaxlower'],ALLStorms['Slower'])
    PowerFit(ALLStorms['Qmaxlower'],ALLStorms['Slower'],xy,qmaxs,linestyle='-',color='y',label='QmaxS_lower_power') 
    QmaxS_lower_linear = linearfunction(ALLStorms['Qmaxlower'],ALLStorms['Slower'])
    LinearFit(ALLStorms['Qmaxlower'],ALLStorms['Slower'],xy,qmaxs,linestyle='--',color='y',label='QmaxS_lower_linear') 
    
    QmaxS_total_power = powerfunction(ALLStorms['Qmaxtotal'],ALLStorms['Stotal'])
    PowerFit(ALLStorms['Qmaxtotal'],ALLStorms['Stotal'],xy,qmaxs,linestyle='-',color='r',label='QmaxS_total_power') 
    QmaxS_total_linear = linearfunction(ALLStorms['Qmaxtotal'],ALLStorms['Stotal'])
    LinearFit(ALLStorms['Qmaxtotal'],ALLStorms['Stotal'],xy,qmaxs,linestyle='--',color='r',label='QmaxS_total_linear') 
    
    qmaxs.set_title('Event Qmax')
    qmaxs.set_ylabel(ylabel),qmaxs.set_xlabel(xlabelQmax)
    
    
    l1,l2,l3 = plt.plot(None,None,'g-',None,None,'y-',None,None,'r-')
    fig.legend((l1,l2,l3),('UPPER','LOWER','TOTAL'), 'upper left',fancybox=True)

        #for ax in fig.axes:
        #ax.legend(loc='best',ncol=2,fancybox=True)           
            
    logaxes(log,fig)
    for ax in fig.axes:
        ax.autoscale_view(True,True,True)
    plt.tight_layout()
    show_plot(show,fig)
    savefig(save,title)
    return
#plotALLStorms_ALLRatings(show=True,log=True,save=False)
#plotALLStorms_ALLRatings(show=True,log=False,save=True)
#plotALLStorms_ALLRatings(ms=20,show=True,log=True,save=True,norm=False)

    
### Qmax vs S    
def plotQmaxS(show=True,log=True,save=False,norm=True): 
    fig, qs = plt.subplots(1)
    xy=np.linspace(.001,100)
    upperdotsize = 50#scaleSeries(SedFluxStorms_DAM['Qsum']/1000)
    lowerdotsize = 50#scaleSeries(SedFluxStorms_LBJ['Qsum']/1000)
    
    if norm==True:
        ALLStorms=NormalizeSSYbyCatchmentArea(compileALLStorms())
        ylabel,xlabel= r'$SSY (Mg \ km^{-2})$',r'$Q_{max} (m^3 s^{-1} km^{-2})$'
    elif norm==False:
        ALLStorms=compileALLStorms()
        ylabel,xlabel = 'SSY (Mg)',r'$Qmax (m^3 s^{-1})$'
   
    ## Lower is below in norm==False loop
    
    ## Upper Watershed (=DAM)
    ALLStorms_upper = ALLStorms[['Qmaxupper','Supper']].dropna()
    qs.scatter(ALLStorms_upper['Qmaxupper']/1000,ALLStorms_upper['Supper'],edgecolors='grey',color='g',s=upperdotsize,label='Upper(VILLAGE)')
    QmaxS_upper_power = powerfunction(ALLStorms_upper['Qmaxupper']/1000,ALLStorms_upper['Supper'])
    PowerFit_CI(ALLStorms_upper['Qmaxupper']/1000,ALLStorms_upper['Supper'],xy,qs,linestyle='-',color='g',label='Qmax_TOTAL') 
    QmaxS_upper_linear = linearfunction(ALLStorms_upper['Qmaxupper']/1000,ALLStorms_upper['Supper'])
    #LinearFit(ALLStorms_upper['Qmaxupper']/1000,ALLStorms_upper['Supper'],xy,qs,linestyle='--',color='g',label='QmaxS_upper_linear') 
    labelindex(ALLStorms_upper.index,ALLStorms_upper['Qmaxupper']/1000,ALLStorms_upper['Supper'],qs)   
    
    ## Total Watershed (=LBJ)
    ALLStorms_total = ALLStorms[['Qmaxtotal','Stotal']].dropna()
    qs.scatter(ALLStorms_total['Qmaxtotal']/1000,ALLStorms_total['Stotal'],edgecolors='grey',color='r',s=lowerdotsize,label='Total(VILLAGE)')
    QmaxS_total_power = powerfunction(ALLStorms_total['Qmaxtotal']/1000,ALLStorms_total['Stotal'])
    PowerFit_CI(ALLStorms_total['Qmaxtotal']/1000,ALLStorms_total['Stotal'],xy,qs,linestyle='-',color='r',label='Qmax_TOTAL') 
    QmaxS_total_linear = linearfunction(ALLStorms_total['Qmaxtotal']/1000,ALLStorms_total['Stotal'])
    #LinearFit(ALLStorms_total['Qmaxtotal']/1000,ALLStorms_total['Stotal'],xy,qs,linestyle='--',color='r',label='QmaxS_total_linear') 
    labelindex(ALLStorms_total.index,ALLStorms_total['Qmaxtotal']/1000,ALLStorms_total['Stotal'],qs)   
    
    
    ## Lower Watershed (=LBJ-DAM)
    if norm==False:
        qs.scatter(ALLStorms['Qmaxlower']/1000,ALLStorms['Slower'],edgecolors='grey',color='y',s=lowerdotsize,label='Lower (VIL-FOR)')
        QmaxS_lower_power = powerfunction(ALLStorms['Qmaxlower']/1000,ALLStorms['Slower'])
        PowerFit(ALLStorms['Qmaxlower']/1000,ALLStorms['Slower'],xy,qs,linestyle='-',color='y',label='Qmax_LOWER') 
        QmaxS_lower_linear = linearfunction(ALLStorms['Qmaxlower']/1000,ALLStorms['Slower'])
        #LinearFit(ALLStorms['Qmaxlower']/1000,ALLStorms['Slower'],xy,qs,linestyle='--',color='y',label='QmaxS_lower_linear') 
        labelindex(ALLStorms.index,ALLStorms['Qmaxlower']/1000,ALLStorms['Slower'])
    
    if norm==True:
        Duvert1 = 224.4*(xy**1.34)
        Duvert2 = 446.6*(xy**0.93)
        DuvertLAFR = 408*(xy**0.95)
        DuvertARES= 640*(xy**1.22)
        DuvertCIES=5039*(xy**1.82)
        DuvertCOMX= 28*(xy**1.92)
        PowerFit(xy,Duvert1,xy,qs,linestyle='-',color='grey',label='Duvert(2012)Linear')
        PowerFit(xy,Duvert2,xy,qs,linestyle='--',color='grey',label='Duvert(2012)Nonlinear')
        PowerFit(xy,DuvertLAFR,xy,qs,linestyle='-',color='k',label=r'Duvert(2012)$LA_{FR}$')
        PowerFit(xy,DuvertARES,xy,qs,linestyle='--',color='k',label=r'Duvert(2012)$AR_{ES}$')
        PowerFit(xy,DuvertCIES,xy,qs,linestyle='-.',color='k',label=r'Duvert(2012)$CI_{ES}$')
        PowerFit(xy,DuvertCOMX,xy,qs,linestyle='-.',color='b',label=r'Duvert(2012)$CO_{MX}$')        
        qs.legend(loc='best',ncol=3,fancybox=True)  
    qs.legend(loc='best',ncol=2,fancybox=True)  
    title="Event Peak Discharge vs Event Sediment Yield from Fagaalu Stream"
    qs.set_title(title)
    qs.set_ylabel(ylabel)
    qs.set_xlabel(xlabel)#+r'$; DotSize= Qsum (m^3)$')
    logaxes(log,fig)
    qs.autoscale_view(True,True,True)
    
    fig.canvas.manager.set_window_title('Figure : '+'Qmax vs. S')
      
    show_plot(show,fig)
    savefig(save,title+'.svg')
    return
plotQmaxS(show=True,log=True,save=False,norm=True)  
#plotQmaxS(show=True,log=False,save=True)
#plotQmaxS(show=True,log=True,save=True,norm=False)
#plotQmaxS(show=True,log=True,save=True,norm=True)

### Qmax vs S    
def plotQmaxStotal(show=True,log=True,save=False,norm=True): 
    fig, qs = plt.subplots(1)
    xy=np.linspace(.001,100)
    upperdotsize = 50#scaleSeries(SedFluxStorms_DAM['Qsum']/1000)
    lowerdotsize = 50#scaleSeries(SedFluxStorms_LBJ['Qsum']/1000)
    
    if norm==True:
        ALLStorms=NormalizeSSYbyCatchmentArea(compileALLStorms())
        ylabel,xlabel= r'$SSY (Mg \ km^{-2})$',r'$Q_{max} (m^3 s^{-1} km^{-2})$'
    elif norm==False:
        ALLStorms=compileALLStorms()
        ylabel,xlabel = 'SSY (Mg)',r'$Qmax (m^3 s^{-1})$'
   
    ## Lower is below in norm==False loop
    
    ## Total Watershed (=LBJ)
    ALLStorms_total = ALLStorms[['Qmaxtotal','Stotal']].dropna()
    qs.scatter(ALLStorms_total['Qmaxtotal']/1000,ALLStorms_total['Stotal'],edgecolors='grey',color='r',s=lowerdotsize,label='Total(VILLAGE)')
    QmaxS_total_power = powerfunction(ALLStorms_total['Qmaxtotal']/1000,ALLStorms_total['Stotal'])
    PowerFit_CI(ALLStorms_total['Qmaxtotal']/1000,ALLStorms_total['Stotal'],xy,qs,linestyle='-',color='r',label='Qmax_TOTAL') 
    QmaxS_total_linear = linearfunction(ALLStorms_total['Qmaxtotal']/1000,ALLStorms_total['Stotal'])
    #LinearFit(ALLStorms_total['Qmaxtotal']/1000,ALLStorms_total['Stotal'],xy,qs,linestyle='--',color='r',label='QmaxS_total_linear') 
    labelindex(ALLStorms_total.index,ALLStorms_total['Qmaxtotal']/1000,ALLStorms_total['Stotal'],qs)   
    
    if norm==True:
        Duvert1 = 224.4*(xy**1.34)
        Duvert2 = 446.6*(xy**0.93)
        DuvertLAFR = 408*(xy**0.95)
        DuvertARES= 640*(xy**1.22)
        DuvertCIES=5039*(xy**1.82)
        DuvertCOMX= 28*(xy**1.92)
        PowerFit(xy,Duvert1,xy,qs,linestyle='-',color='grey',label='Duvert(2012)Linear')
        PowerFit(xy,Duvert2,xy,qs,linestyle='--',color='grey',label='Duvert(2012)Nonlinear')
        PowerFit(xy,DuvertLAFR,xy,qs,linestyle='-',color='k',label=r'Duvert(2012)$LA_{FR}$')
        PowerFit(xy,DuvertARES,xy,qs,linestyle='--',color='k',label=r'Duvert(2012)$AR_{ES}$')
        PowerFit(xy,DuvertCIES,xy,qs,linestyle='-.',color='k',label=r'Duvert(2012)$CI_{ES}$')
        PowerFit(xy,DuvertCOMX,xy,qs_total,linestyle='-.',color='b',label=r'Duvert(2012)$CO_{MX}$')        
        qs.legend(loc='best',ncol=3,fancybox=True)  
    qs.legend(loc='best',ncol=2,fancybox=True)  
    title="Event Peak Discharge vs Event Sediment Yield from Fagaalu Stream"
    qs.set_title(title)
    qs.set_ylabel(ylabel)
    qs.set_xlabel(xlabel)#+r'$; DotSize= Qsum (m^3)$')
    logaxes(log,fig)
    qs.autoscale_view(True,True,True)
    
    fig.canvas.manager.set_window_title('Figure : '+'Qmax vs. S')

    show_plot(show,fig)
    savefig(save,title)
    return
plotQmaxStotal(show=True,log=True,save=False,norm=True)  

### Qmax vs S    
def plotQmaxSseparate(show=True,log=True,save=False,norm=True): 
    fig, (qs_upper, qs_total) = plt.subplots(2,sharex=True,sharey=True)
    xy=np.linspace(.001,100)
    upperdotsize = 50#scaleSeries(SedFluxStorms_DAM['Qsum']/1000)
    lowerdotsize = 50#scaleSeries(SedFluxStorms_LBJ['Qsum']/1000)
    
    if norm==True:
        ALLStorms=NormalizeSSYbyCatchmentArea(compileALLStorms())
        ylabel,xlabel= r'$SSY (Mg \ km^{-2})$',r'$Q_{max} (m^3 s^{-1} km^{-2})$'
    elif norm==False:
        ALLStorms=compileALLStorms()
        ylabel,xlabel = 'SSY (Mg)',r'$Qmax (m^3 s^{-1})$'
   
    ## Lower is below in norm==False loop
    
    ## Upper Watershed (=DAM)
    QmaxS_upper = SedFluxStorms_DAM[['Qmax','Ssum']].dropna()
    qs_upper.scatter(QmaxS_upper['Qmax']/1000,QmaxS_upper['Ssum'],edgecolors='grey',color='g',s=upperdotsize,label='Upper(VILLAGE)')
    QmaxS_upper_power = powerfunction(QmaxS_upper['Qmax']/1000,QmaxS_upper['Ssum'])
    PowerFit_CI(QmaxS_upper['Qmax']/1000,QmaxS_upper['Ssum'],xy,qs_upper,linestyle='-',color='g',label='Qmax_TOTAL') 
    QmaxS_upper_linear = linearfunction(QmaxS_upper['Qmax']/1000,QmaxS_upper['Ssum'])
    #LinearFit(ALLStorms_upper['Qmaxupper']/1000,ALLStorms_upper['Supper'],xy,qs,linestyle='--',color='g',label='QmaxS_upper_linear') 
    labelindex(QmaxS_upper.index,QmaxS_upper['Qmax']/1000,QmaxS_upper['Ssum'],qs_upper)   
    
    ## Total Watershed (=LBJ)
    ALLStorms_total = ALLStorms[['Qmaxtotal','Stotal']].dropna()
    qs_total.scatter(ALLStorms_total['Qmaxtotal']/1000,ALLStorms_total['Stotal'],edgecolors='grey',color='r',s=lowerdotsize,label='Total(VILLAGE)')
    QmaxS_total_power = powerfunction(ALLStorms_total['Qmaxtotal']/1000,ALLStorms_total['Stotal'])
    PowerFit_CI(ALLStorms_total['Qmaxtotal']/1000,ALLStorms_total['Stotal'],xy,qs_total,linestyle='-',color='r',label='Qmax_TOTAL') 
    QmaxS_total_linear = linearfunction(ALLStorms_total['Qmaxtotal']/1000,ALLStorms_total['Stotal'])
    #LinearFit(ALLStorms_total['Qmaxtotal']/1000,ALLStorms_total['Stotal'],xy,qs,linestyle='--',color='r',label='QmaxS_total_linear') 
    labelindex(ALLStorms_total.index,ALLStorms_total['Qmaxtotal']/1000,ALLStorms_total['Stotal'],qs_total)   
    
    ## Lower Watershed (=LBJ-DAM)
    if norm==False:
        qs_total.scatter(ALLStorms['Qmaxlower']/1000,ALLStorms['Slower'],edgecolors='grey',color='y',s=lowerdotsize,label='Lower (VIL-FOR)')
        QmaxS_lower_power = powerfunction(ALLStorms['Qmaxlower']/1000,ALLStorms['Slower'])
        PowerFit(ALLStorms['Qmaxlower']/1000,ALLStorms['Slower'],xy,qs_total,linestyle='-',color='y',label='Qmax_LOWER') 
        QmaxS_lower_linear = linearfunction(ALLStorms['Qmaxlower']/1000,ALLStorms['Slower'])
        #LinearFit(ALLStorms['Qmaxlower']/1000,ALLStorms['Slower'],xy,qs_total,linestyle='--',color='y',label='QmaxS_lower_linear') 
        labelindex(ALLStorms.index,ALLStorms['Qmaxlower']/1000,ALLStorms['Slower'])
    
    if norm==True:
        Duvert1 = 224.4*(xy**1.34)
        Duvert2 = 446.6*(xy**0.93)
        DuvertLAFR = 408*(xy**0.95)
        DuvertARES= 640*(xy**1.22)
        DuvertCIES=5039*(xy**1.82)
        DuvertCOMX= 28*(xy**1.92)
        PowerFit(xy,Duvert1,xy,qs_total,linestyle='-',color='grey',label='Duvert(2012)Linear')
        PowerFit(xy,Duvert2,xy,qs_total,linestyle='--',color='grey',label='Duvert(2012)Nonlinear')
        PowerFit(xy,DuvertLAFR,xy,qs_total,linestyle='-',color='k',label=r'Duvert(2012)$LA_{FR}$')
        PowerFit(xy,DuvertARES,xy,qs_total,linestyle='--',color='k',label=r'Duvert(2012)$AR_{ES}$')
        PowerFit(xy,DuvertCIES,xy,qs_total,linestyle='-.',color='k',label=r'Duvert(2012)$CI_{ES}$')
        PowerFit(xy,DuvertCOMX,xy,qs_total,linestyle='-.',color='b',label=r'Duvert(2012)$CO_{MX}$')        
        qs_total.legend(loc='best',ncol=3,fancybox=True)  
    
    title="Event Peak Discharge vs Event Sediment Yield from Fagaalu Stream"
    plt.suptitle(title)
    qs_upper.set_ylabel(ylabel)
    qs_upper.set_xlabel(xlabel)#+r'$; DotSize= Qsum (m^3)$')
    qs_total.set_xlabel(xlabel)#+r'$; DotSize= Qsum (m^3)$')

    fig.canvas.manager.set_window_title('Figure : '+'Qmax vs. S')
    
    logaxes(log,fig)
    #qs_upper.autoscale_view(True,True,True)
    #qs_total.autoscale_view(True,True,True)
    show_plot(show,fig)
    savefig(save,title)
    return
plotQmaxSseparate(show=True,log=True,save=False,norm=True)  

plt.show()
elapsed = dt.datetime.now() - start_time 
print 'run time: '+str(elapsed)


