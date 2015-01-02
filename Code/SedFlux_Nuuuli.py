# -*- coding: utf-8 -*-
"""
Created on Fri Jan 02 05:05:03 2015

@author: Alex
"""

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
    datadir=maindir+'Data_Nuuuli/'
    dataoutputdir = datadir+'Output/'
    GISdir = maindir+'Data_Nuuuli/GIS/'
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
        print 'log axes'
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
        xvals = np.linspace(x.min()-10,x.max()*1.2)
        print 'No xspace, calculating xvals: '+'%.0f'%x.min()+'-'+'%.0f'%x.max()+'*1.5= '+'%.0f'%(x.max()*1.5)
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
    print 'opening MASTER_DATA_NUUULI excel file...'+dt.datetime.now().strftime('%H:%M:%S')
    XL = pd.ExcelFile(datadir+'MASTER_DATA_NUUULI.xlsx')
if 'XL' in locals():
    print 'MASTER_DATA_NUUULI opened: '+dt.datetime.now().strftime('%H:%M:%S')    
    
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

if 'Precip' not in locals():
    ## Timu-Nuuuli 1 (by the Pala Lagoon)
    Precip = raingauge(XL,'Timu-Nuuuli1',0) ## (path,sheet,shift) no header needed
    Precip.columns=['Timu1']
    Precip['Timu1-15']=Precip['Timu1'].resample('15Min',how='sum')
    Precip['Timu1-30']=Precip['Timu1'].resample('30Min',how='sum')
    
    Precip['Timu1hourly']= Precip['Timu1'].resample('H',how='sum')
    Precip['Timu1hourly'].dropna().to_csv(datadir+'OUTPUT/Timu1hourly.csv',header=['Timu1hourly'])
    
    Precip['Timu1daily'] = Precip['Timu1'].resample('D',how='sum')
    Precip['Timu1daily'].dropna().to_csv(datadir+'OUTPUT/Timu1daily.csv',header=['Timu1daily'])
    
    Precip['Timu1monthly'] = Precip['Timu1'].resample('MS',how='sum') ## Monthly Precip
    Precip['Timu1monthly'].dropna().to_csv(datadir+'OUTPUT/Timu1monthly.csv',header=['Timu1monthly'])
    
    ## Timu-Nuuuli2 (upstream by Loma's house)
    Precip['Timu2-30']=raingauge(XL,'Timu-Nuuuli2',0).resample('30Min',how='sum')
    
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
#PrecipFilled=pd.DataFrame(pd.concat([Precip['Timu1-15'][dt.datetime(2012,1,7):dt.datetime(2013,2,8)],Precip['FPrain'][dt.datetime(2013,2,8,0,15):dt.datetime(2013,3,12)],Precip['Timu1-15'][dt.datetime(2013,3,12,0,15):dt.datetime(2013,3,24)],Precip['FPrain'][dt.datetime(2013,3,24,0,15):dt.datetime(2013,5,1)],Precip['Timu1-15'][dt.datetime(2013,5,1,0,15):dt.datetime(2014,12,31)]]),columns=['Precip']).dropna()

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
## Timu-Nuuuli1
Timu1fieldnotes = FieldNotes('Timu-N1notes',3,fieldbookdata)
Timu1mmcheck = Timu1fieldnotes.ix[:,'mm':'to 0.1'] ##take the records from the manual gage and if it was emptied to zero
Timu1mmcheck['mm true'] = Timu1mmcheck['mm']-Timu1mmcheck['to 0.1'].shift(1)
Timu1mmcheck['end']=Timu1mmcheck.index## add a column for time
Timu1mmcheck['start']=Timu1mmcheck['end'].shift(1) ## take the time and shift it down so you have a start and stop time: When the gauge was emptied to zero, it was the start of the next interval
Timu1mmcheck=Timu1mmcheck.truncate(before = Timu1mmcheck.index[5])
Timu1mmcheck['Timu1 mm sum']=StormSums(Timu1mmcheck,Precip['Timu1'])['sum'] ## from 1/20/12 onward. Timu1 QC data begins 1/21/12
Timu1mmcheck['WorldsBest - Timu1'] = Timu1mmcheck['Timu1 mm sum']-Timu1mmcheck['mm']
## Timu-Nuuuli2
Timu2fieldnotes = FieldNotes('Timu-N2notes',3,fieldbookdata)
Timu2mmcheck = Timu2fieldnotes.ix[:,'mm':'to 0.1'] ##take the records from the manual gage and if it was emptied to zero
Timu2mmcheck['mm true'] = Timu2mmcheck['mm']-Timu2mmcheck['to 0.1'].shift(1)
Timu2mmcheck['end']=Timu2mmcheck.index## add a column for time
Timu2mmcheck['start']=Timu2mmcheck['end'].shift(1) ## take the time and shift it down so you have a start and stop time: When the gauge was emptied to zero, it was the start of the next interval
Timu2mmcheck=Timu2mmcheck.truncate(before = Timu2mmcheck.index[5])
Timu2mmcheck['Timu2 mm sum']=StormSums(Timu2mmcheck,Precip['Timu2'])['sum'] ## from 1/20/12 onward. Timu2 QC data begins 1/21/12
Timu2mmcheck['WorldsBest - Timu2'] = Timu2mmcheck['Timu2 mm sum']-Timu2mmcheck['mm']

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
    print 'Loading NDBC NSTP6 barometric data...'
    try:
        ndbc_data = pd.DataFrame.from_csv(datadir+'BARO/NSTP6/NDBC_Baro.csv')
    except:
        ndbcXL = pd.ExcelFile(datafile)
        ndbc_parse = lambda yr,mo,dy,hr,mn: dt.datetime(yr,mo,dy,hr,mn)
        ndbc_data = ndbcXL.parse('NSTP6-2012-14',header=0,skiprows=1,parse_dates=[['#yr','mo','dy','hr','mn']],index_col=0,date_parser=ndbc_parse,
                             na_values=['9999','999','99','99.0'])
        ndbc_data.to_csv(datadir+'BARO/NSTP6/NDBC_Baro.csv')
    #local = pytz.timezone('US/Samoa')
    #ndbc_data.index = ndbc_data.index.tz_localize(pytz.utc).tz_convert(local)
    print 'NDBC loaded'
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
PT1a = PT_Levelogger(allbaro,'PT1 Downstream bridge',XL,'PT-Nuuuli1') #12 x 15min = 3hours
## PT2 QUARRY
# tshift in 15Min(or whatever the timestep is), zshift in cm
PT2 = PT_Levelogger(allbaro,'PT2 Upstream bridge',XL,'PT-Nuuuli2')




















