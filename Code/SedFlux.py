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
import misc_time
from misc_time import * 
from misc_numpy import *
from misc_matplotlib import * 

## Statistical Analysis
from scipy import stats
import pandas.stats.moments as m
from scipy.stats import pearsonr as pearson_r
from scipy.stats import spearmanr as spearman_r

import statsmodels.formula.api as smf
import statsmodels.stats.api

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
        print 'log axes'
        for ax in fig.axes:
            ax.set_yscale('log'), ax.set_xscale('log')
    return
def savefig(save=True,filename=''):
    if save==True:
        plt.savefig(filename+'.pdf') ## for publication
        plt.savefig(filename+'.png') ## for manuscript
    return
def pltdefault():
    global figdir
    plt.rcdefaults()
    #figdir = datadir+'samoa/WATERSHED_ANALYSIS/GoodFigures/rawfigoutput/'
    return  
    

def letter_subplots(fig,x=0.1,y=0.95,vertical='top',horizontal='right',Color='k',font_size=10,font_weight='bold'):
    sub_plot_count = 0
    sub_plot_letters = {0:'(a)',1:'(b)',2:'(c)',3:'(d)',4:'(e)',5:'(f)',6:'(g)',7:'(h)',8:'(i)'}
    for ax in fig.axes:
        ax.text(x,y,sub_plot_letters[sub_plot_count],verticalalignment=vertical, horizontalalignment=horizontal,transform=ax.transAxes,color=Color,fontsize=font_size,fontweight=font_weight)
        sub_plot_count+=1
    plt.draw()
    return 

    
## Figure formatting
#publishable =  plotsettings.Set('GlobEnvChange')    ## plotsettings.py
#publishable.set_figsize(n_columns = 2, n_rows = 2)
    
mpl.rc_file(maindir+'johrc.rc')
mpl.rcParams['savefig.directory']=maindir+'rawfig/'
mpl.rcParams
mpl.rc('legend',scatterpoints=1)  
## Ticks
my_locator = matplotlib.ticker.MaxNLocator(4)

    
def pltsns(style='white',context='paper'):
    global figdir
    sns.set_style(style)
    sns.set_style({'legend.frameon':True})
    sns.set_context(context)
    ## Some Formatting
    mpl.rcParams['savefig.directory']=maindir+'rawfig/'
    mpl.rcParams['savefig.format']= '.pdf'
    mpl.rcParams['figure.dpi']=100
    mpl.rcParams['savefig.dpi']= 300 # mpl.rcParams['figure.dpi']
    mpl.rcParams['axes.labelsize']= 11
    mpl.rcParams['xtick.labelsize']=11
    mpl.rcParams['ytick.labelsize']=11
    
    return
#pltsns()    

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
    return
    
def scaleSeries(series,new_scale=[100,10]):
    new_scale = new_scale
    OldRange = (series.max() - series.min())  
    NewRange = (new_scale[0] - new_scale[1])  
    NewSeriesValues = (((series - series.min()) * NewRange) / OldRange) + new_scale[1]
    return NewSeriesValues          
    
def power(x,a,b):
    y = a*(x**b)
    return y
    
def powerfunction(x,y,name='power rating',pvalue=0.01):
    datadf = pd.DataFrame.from_dict({'x':x,'y':y}).dropna().apply(np.log10) ## put x and y in a dataframe so you can drop ones that don't match up    
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
start2012, stop2012 = dt.datetime(2012,1,1,0,0), dt.datetime(2012,12,31,11,59)    
start2013, stop2013 = dt.datetime(2013,1,1,0,0), dt.datetime(2013,12,31,11,59)
start2014, stop2014 = dt.datetime(2014,1,1,0,0), dt.datetime(2015,1,9,11,59)   
## Field Seasons
fieldstart2012, fieldstop2012 =  dt.datetime(2012,1,5,0,0), dt.datetime(2012,3,29,11,59)    
fieldstart2013, fieldstop2013 =  dt.datetime(2013,2,4,0,0), dt.datetime(2013,7,17,11,59)    
fieldstart2014a, fieldstop2014a =  dt.datetime(2014,1,10,0,0), dt.datetime(2014,3,7,11,59)
fieldstart2014b, fieldstop2014b =  dt.datetime(2014,9,29,0,0), dt.datetime(2015,1,12,11,59)     
## Mitigation
Mitigation = dt.datetime(2014,10,1,0,0)

def LandCover_table():
    landcoverXL = pd.ExcelFile(datadir+'/LandCover/Watershed_Stats.xlsx')
    landcover_table = landcoverXL.parse('Fagaalu_Revised')
    landcover_table = landcover_table[['Subwatershed (pourpoint)','Cumulative Area km2','Cumulative %','Area km2','% of area','% Bare Land','% High Intensity Developed','% Developed Open Space','% Grassland (agriculture)','% Forest','% Scrub/ Shrub','% Disturbed','% Undisturbed']]
    # Format Table data                       
    for column in landcover_table.columns:
        try:
            if column.startswith('%')==True or column.startswith('Cumulative %')==True:
                landcover_table[column] = landcover_table[column]*100.
                landcover_table[column] = landcover_table[column].round(1)
            else:
                landcover_table[column] = landcover_table[column].round(2)
        except:
            pass
    landcover_table = landcover_table[landcover_table['Subwatershed (pourpoint)'].isin(['UPPER (FG1)','LOWER_QUARRY (FG2)','LOWER_VILLAGE (FG3)','LOWER (FG3)','TOTAL (FG3)','Fagaalu Stream'])==True].reset_index()
    landcover_table = landcover_table[['Subwatershed (pourpoint)','Cumulative Area km2','Cumulative %','Area km2','% of area','% Bare Land','% High Intensity Developed','% Developed Open Space','% Grassland (agriculture)','% Forest','% Scrub/ Shrub','% Disturbed','% Undisturbed']]
    return landcover_table
LandCover_table()

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
    gauge = gauge*0.254 ##hundredths to mm
    gauge.columns=['Events']
    return gauge    


if 'Precip' not in locals():
    ## Timu-Fagaalu 1 (by the Quarry)
    Precip = raingauge(XL,'Timu-Fagaalu1-2013',180) ## (path,sheet,shift) no header needed
    Precip = Precip.append(raingauge(XL,'Timu-Fagaalu1-2014',0)) ## (path,sheet,shift) no header needed
    #Precip = Precip.append(raingauge(XL,'Timu-Fagaalu1-2015',0)) ## (path,sheet,shift) no header needed
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
PrecipFilled=pd.DataFrame(pd.concat([Precip['Timu1-15'][dt.datetime(2012,1,7):dt.datetime(2013,2,8)],Precip['FPrain'][dt.datetime(2013,2,8,0,15):dt.datetime(2013,3,12)],Precip['Timu1-15'][dt.datetime(2013,3,12,0,15):dt.datetime(2013,3,24)],Precip['FPrain'][dt.datetime(2013,3,24,0,15):dt.datetime(2013,5,1)],Precip['Timu1-15'][dt.datetime(2013,5,1,0,15):dt.datetime(2014,12,31)]]),columns=['Precip']).dropna()

### Long term rainfall records

TutPrecipXL =  pd.ExcelFile(datadir+'PRECIP/Tutuila-precipitation.xlsx')
def plot_prob_occurrence(sheet_name):
    P_Station= TutPrecipXL.parse(sheet_name,header=14,skiprows=[15],parse_cols='C:D',parse_dates=['datetime'],index_col=['datetime'])
    P_Station.columns=['PrecipDailyIn']
    P_Station['PrecipDailymm'] = P_Station['PrecipDailyIn']   *25.4
    
    P_Station = P_Station.dropna().sort(columns=['PrecipDailymm'],ascending=False)##ascending=False means highest values at top
    P_Station['rank'] = range(1,len(P_Station)+1)
    P_Station_n = len(P_Station)
    ## Calculate Prob of Occurrence and Return Interval(Tr)
    P_Station['ProbOcc']=P_Station['rank']/(P_Station_n + 1.)
    P_Station['Tr']=(P_Station_n +1.)/P_Station['rank']
    
    fig, ax=plt.subplots(1)
    plt.scatter(P_Station['PrecipDailymm'],P_Station['ProbOcc'])
    plt.ylabel('Prob. of Occurrence: % of time the precip value will be exceeded')
    plt.xlabel('Precipitation (mm)')
    ax.set_xlim(-5,500), ax.set_ylim(-.05,1.1)
    
    data_days= str(len(P_Station))
    data_years= str(len(P_Station)//365)
    plt.title(sheet_name+' '+data_days+' days of data('+data_years+' years)')
    fig.tight_layout()
    return P_Station
    
#VaipitoRes =plot_prob_occurrence('VaipitoRes')
#Afono= plot_prob_occurrence('Pioa-Afono')
#Aunuu = plot_prob_occurrence('Aunuu')
#Malaeimi = plot_prob_occurrence('Malaeimi-Mapusaga')

def prob_occurrence():
    P_Station= pd.DataFrame(Precip['Timu1daily'].dropna())
    P_Station.columns=['PrecipDailymm']
    
    P_Station = P_Station.dropna().sort(columns=['PrecipDailymm'],ascending=False)##ascending=False means highest values at top
    P_Station['rank'] = range(1,len(P_Station)+1)
    P_Station_n = len(P_Station)
    ## Calculate Prob of Occurrence and Return Interval(Tr)
    P_Station['ProbOcc']=P_Station['rank']/(P_Station_n + 1.)
    P_Station['Tr']=(P_Station_n +1.)/P_Station['rank']
    
    fig, ax=plt.subplots(1)
    plt.scatter(P_Station['PrecipDailymm'],P_Station['ProbOcc'])
    plt.ylabel('Prob. of Occurrence: % of time the precip value will be exceeded')
    plt.xlabel('Precipitation (mm)')
    ax.set_xlim(-5,500), ax.set_ylim(-.05,1.1)
    
    data_days= str(len(P_Station))
    data_years= str(len(P_Station)//365)
    plt.title(data_days+' days of data('+data_years+' years)')
    fig.tight_layout()
    return P_Station
#prob_occurrence()

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
#TAFUNAbaro= pd.DataFrame({'TAFUNAbaro':airport['Sea Level PressureIn'] * 3.3863881579}).resample('15Min',fill_method='ffill',limit=2)## inches to kPa

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
allbaro = pd.DataFrame(NDBCbaro/10).reindex(pd.date_range(start2012,stop2014,freq='15Min'))
allbaro['FPbaro']=FP['Bar']/10
allbaro['NDBCbaro']=NDBCbaro/10
allbaro['BaroLogger']=BaroLogger
#allbaro['TULAbaro']=TULAbaro['TULAbaro']

## Fill priority = FP,NDBC,TAFUNA,TULA
allbaro['Baropress']=allbaro['FPbaro'].where(allbaro['FPbaro']>0,allbaro['BaroLogger']) ## create a new column and fill with FP or Barologger
allbaro['Baropress']=allbaro['Baropress'].where(allbaro['Baropress']>0,allbaro['NDBCbaro']) ## create a new column and fill with FP or NDBC
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
    PT['stage']=(PT['Pressure']-PT['barodata'])*.102*100.0 ## hPa  to cm
    #PT['stage']=PT['stage'].where(PT['stage']>0,PT['barodata']) ## filter negative values
    PT['stage']=PT['stage'].round(1)  
    PT['stage']=PT['stage']+zshift
    PT['Uncorrected_stage']=PT['stage'].round(0)
    return PT

def PT_Levelogger(allbaro,PTname,XL,sheet,tshift=0,zshift=0): # tshift in hours, zshift in cm
    print 'loading Levelogger PT: '+sheet+'...'
    PT = XL.parse(sheet,header=11,parse_cols='A,B,D',parse_dates=[['Date','Time']],index_col=['Date_Time'])
    PT.columns= ['LEVEL']
    PT=PT.resample('15Min',how='mean')
    PT['barodata']=allbaro['Baropress']
    PT=PT.shift(tshift) ## shift by 3 hours (12 x 15minutes)
    PT['stage']=(PT['LEVEL']-PT['barodata'])*.102*100.0
    #PT['stage']=PT['stage'].where(PT['stage']>0,0) ## filter negative values
    PT['stage']=PT['stage'].round(1)  
    PT['stage']=PT['stage']+zshift
    PT['Uncorrected_stage']=PT['stage'].round(0)
    return PT
## PT1 LBJ
# tshift in 15Min(or whatever the timestep is), zshift in cm
PT1aa = PT_Hobo(allbaro,'PT1 LBJ bridge',XL,'PT-Fagaalu1aa',tshift=12) #12 x 15min = 3hours (It says it was at GMT-8 instead of GMT-11 but the logger time was set to local anyway)
PT1ab = PT_Hobo(allbaro,'PT1 LBJ bridge',XL,'PT-Fagaalu1ab',tshift=12) #12 x 15min = 3hours (It says it was at GMT-8 instead of GMT-11 but the logger time was set to local anyway)
PT1ba = PT_Hobo(allbaro,'PT1 LBJ bridge',XL,'PT-Fagaalu1ba',tshift=4)
PT1bb = PT_Hobo(allbaro,'PT1 LBJ bridge',XL,'PT-Fagaalu1bb',tshift=4)
PT1bc = PT_Hobo(allbaro,'PT1 LBJ bridge',XL,'PT-Fagaalu1bc',tshift=4)
PT1c = PT_Hobo(allbaro,'PT1 LBJ bridge',XL,'PT-Fagaalu1c')
PT1 = pd.concat([PT1aa,PT1ab,PT1ba,PT1bb,PT1bc,PT1c])

#rawPT1XL = pd.ExcelFile(datadir+'PT-Fagaalu1-raw.xlsx') 
#rawPT1=pd.DataFrame()
#for sheet_name in rawPT1XL.sheet_names:
#    #print sheet_name
#    sheet = rawPT1XL.parse(sheet_name,header=1,index_col=0,parse_cols='B,C',parse_dates=True)
#    sheet.columns=['Pressure']
#    rawPT1 = rawPT1.append(sheet)

## PT2 QUARRY
# tshift in 15Min(or whatever the timestep is), zshift in cm
PT2 = PT_Levelogger(allbaro,'PT2 Drive Thru',XL,'PT-Fagaalu2',0,-22)

## PT3 DAM
# tshift in 15Min(or whatever the timestep is), zshift in cm
PT3aa = PT_Hobo(allbaro,'PT3a Dam',XL,'PT-Fagaalu3aa',12)
PT3ab = PT_Hobo(allbaro,'PT3a Dam',XL,'PT-Fagaalu3ab',12)
PT3b = PT_Levelogger(allbaro,'PT3b Dam',XL,'PT-Fagaalu3b',0)
PT3c = PT_Levelogger(allbaro,'PT3c Dam',XL,'PT-Fagaalu3c',0)
PT3d = PT_Levelogger(allbaro,'PT3d Dam',XL,'PT-Fagaalu3d',0)
PT3e = PT_Levelogger(allbaro,'PT3e Dam',XL,'PT-Fagaalu3e',0)
PT3f = PT_Levelogger(allbaro,'PT3f Dam',XL,'PT-Fagaalu3f',0)
PT3g = PT_Levelogger(allbaro-1.5,'PT3g Dam',XL,'PT-Fagaalu3g',0)
PT3 = pd.concat([PT3aa,PT3ab,PT3b,PT3c,PT3d,PT3e,PT3f,PT3g])
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
    
  
## Plot Stage Correction
#PT1['stage'].plot=('y')
#LBJfieldnotesStage['RefGageHeight(cm)'].plot(ls='None',marker='o',markersize=6,c='g')
#PT1['stage corrected'].plot(color='k')


def correct_Stage(StageCorrXL,location,PTdata):
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
    StageCorr = StageCorrXL.parse(location,parse_dates=False)
    Correction=pd.DataFrame()
    for correction in StageCorr.iterrows():
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
    PTdata['stage']=PTdata['stage_corrected_Manual'].where(PTdata['stage_corrected_Manual']>0,PTdata['stage'])#.round(0)
    return PTdata
StageCorrXL = pd.ExcelFile(datadir+'Q/StageCorrection.xlsx')    
PT1 = correct_Stage(StageCorrXL,'LBJ',PT1)
PT3 = correct_Stage(StageCorrXL,'DAM',PT3)


## STAGE DATA FOR PT's
#### FINAL STAGE DATA with CORRECTIONS
Fagaalu_stage_data = pd.DataFrame({'LBJ':PT1['stage'],'DT':PT2['stage'],'Dam':PT3['stage']})
Fagaalu_stage_data = Fagaalu_stage_data.reindex(pd.date_range(start2012,stop2014,freq='15Min'))

#### Define Storm Periods #####
## Define Storm Intervals at LBJ
DefineStormIntervalsBy = {'User':'User','Separately':'BOTH','DAM':'DAM','LBJ':'LBJ'}
StormIntervalDef = DefineStormIntervalsBy['LBJ']

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
        start = t[0]-dt.timedelta(minutes=30)
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

### Check PT against reference staff gage at LBJ
LBJfieldnotes = FieldNotes('LBJstage',1,fieldbookdata)
LBJfieldnotesStage = pd.DataFrame(LBJfieldnotes['RefGageHeight(cm)'].resample('5Min',how='first').dropna(),columns=['RefGageHeight(cm)'])
LBJfieldnotesStage =LBJfieldnotesStage.shift(0)
LBJfieldnotesStage['Uncorrected_stage']=PT1['Uncorrected_stage']
LBJfieldnotesStage['GH-Uncorrected_stage']=LBJfieldnotesStage['RefGageHeight(cm)']-LBJfieldnotesStage['Uncorrected_stage']
LBJfieldnotesStage['Corrected_stage']=PT1['stage']
LBJfieldnotesStage['GH-Corrected_stage']=LBJfieldnotesStage['RefGageHeight(cm)']-LBJfieldnotesStage['Corrected_stage']

PT1['GH Correction']=LBJfieldnotesStage['GH-Uncorrected_stage']
PT1['GH Correction Int']= PT1['GH Correction'].interpolate()
PT1['stage_corrected_RefGage'] = PT1['Uncorrected_stage']+PT1['GH Correction Int']

def compare_PT_Ref():
    fig, (uncorr, corr) = plt.subplots(2,1,sharex=True,sharey=True)
    LBJfieldnotesStage['GH-Uncorrected_stage'].plot(ax=uncorr,ls='None',marker='.',c='r',label='All Gage Height Readings (uncorrected)')
    LBJfieldnotesStage['GH-Uncorrected_stage'][LBJfieldnotesStage['Uncorrected_stage']<LBJ_storm_threshold].plot(ax=uncorr,ls='None',marker='.',c='b',label='Baseflow Gage Height Readings (uncorrected)')
    uncorr.legend(loc='best'), uncorr.set_title('Uncorrected PT stage')
    LBJfieldnotesStage['GH-Corrected_stage'].plot(ax=corr, ls='None',marker='.',c='r',label='All Gage Height Readings (corrected)')
    LBJfieldnotesStage['GH-Corrected_stage'][LBJfieldnotesStage['Corrected_stage']<LBJ_storm_threshold].plot(ax=corr,ls='None',marker='.',c='b',label='Baseflow Gage Height Readings (corrected)')
    corr.legend(loc='best'), corr.set_title('Corrected PT stage')
    return

def press_diff():   
    fig, (baro, pt, diff) = plt.subplots(3,1,sharex=True)
    allbaro['Baropress'].plot(ax=baro,c='k')
    allbaro['NDBCbaro'].plot(ax=baro,c='r')
    allbaro['FPbaro'].plot(ax=baro,c='g')
    
    PT1['Pressure'].plot(ax=baro,c='b')
    PT1['stage'].plot(ax=pt,c='b')
    press_diff_baseflow = PT1['Pressure'][PT1['stage']<10]-PT1['barodata']
    m.rolling_mean(press_diff_baseflow,window=96).plot(ax=diff)
    diff.axhline(0.63,ls='--',linewidth=1,c='b',label='Baseflow')
    plt.legend()
    return

## Take just one definition of Storm Intervals....
if StormIntervalDef=='LBJ':
    print 'Storm intervals defined at LBJ'
    ## Define Storm Intervals at LBJ
    LBJ_StormIntervals=SeparateHydrograph(hydrodata=PT1['stage'])
    ## Combine Storm Events where the storm end is the storm start for the next storm
    LBJ_StormIntervals['next storm start']=LBJ_StormIntervals['start'].shift(-1) ## add the next storm's start and end time to the storm in the row above (the previous storm)
    LBJ_StormIntervals['next storm end']=LBJ_StormIntervals['end'].shift(-1)  
    need_to_combine =LBJ_StormIntervals[LBJ_StormIntervals['end']==LBJ_StormIntervals['next storm start']] #storms need to be combined if their end is the same time as the next storm's start
    print need_to_combine
    need_to_combine['end']=need_to_combine['next storm end'] # change the end of the storm to the end of the next storm to combine them
    
    LBJ_StormIntervals=LBJ_StormIntervals.drop(need_to_combine.index) #drop the storms that need to be combined
    LBJ_StormIntervals=LBJ_StormIntervals.append(need_to_combine).sort(ascending=True) #append back in the combined storms
    LBJ_StormIntervals=LBJ_StormIntervals.drop_duplicates(cols=['end']) #drop the second storm that was combined
    
    ## Second pass
    LBJ_StormIntervals['next storm start']=LBJ_StormIntervals['next storm start'].shift(-1) ## add the next storm's start and end time to the storm in the row above (the previous storm)
    LBJ_StormIntervals['next storm end']=LBJ_StormIntervals['next storm end'].shift(-1)  
    need_to_combine =LBJ_StormIntervals[LBJ_StormIntervals['end']==LBJ_StormIntervals['next storm start']] #storms need to be combined if their end is the same time as the next storm's start
    print need_to_combine
    need_to_combine['end']=need_to_combine['next storm end'] # change the end of the storm to the end of the next storm to combine them
    LBJ_StormIntervals=LBJ_StormIntervals.drop(need_to_combine.index) #drop the storms that need to be combined
    LBJ_StormIntervals=LBJ_StormIntervals.append(need_to_combine).sort(ascending=True) #append back in the combined storms
    LBJ_StormIntervals=LBJ_StormIntervals.drop_duplicates(cols=['end']) 
    
    ## Third pass
    LBJ_StormIntervals['next storm start']=LBJ_StormIntervals['next storm start'].shift(-1) ## add the next storm's start and end time to the storm in the row above (the previous storm)
    LBJ_StormIntervals['next storm end']=LBJ_StormIntervals['next storm end'].shift(-1)  
    need_to_combine =LBJ_StormIntervals[LBJ_StormIntervals['end']==LBJ_StormIntervals['next storm start']] #storms need to be combined if their end is the same time as the next storm's start
    print need_to_combine
    need_to_combine['end']=need_to_combine['next storm end'] # change the end of the storm to the end of the next storm to combine them
    LBJ_StormIntervals=LBJ_StormIntervals.drop(need_to_combine.index) #drop the storms that need to be combined
    LBJ_StormIntervals=LBJ_StormIntervals.append(need_to_combine).sort(ascending=True) #append back in the combined storms
    LBJ_StormIntervals=LBJ_StormIntervals.drop_duplicates(cols=['end'])  
    ## Reset Duration
    LBJ_StormIntervals['duration'] = (LBJ_StormIntervals['end']- LBJ_StormIntervals['start'])
    LBJ_StormIntervals['duration (hrs)'] = LBJ_StormIntervals['duration'].apply(lambda x: x/np.timedelta64(1, 's')/3600)
    LBJ_StormIntervals = LBJ_StormIntervals[LBJ_StormIntervals['start']!=dt.datetime(2012,1,25,3,45)]
    
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
LBJ_StormIntervals.to_excel(datadir+'Q/StormIntervals/LBJ_StormIntervals.xlsx')
QUARRY_StormIntervals.to_excel(datadir+'Q/StormIntervals/QUARRY_StormIntervals.xlsx')
DAM_StormIntervals.to_excel(datadir+'Q/StormIntervals/DAM_StormIntervals.xlsx')

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
                        
                        AV_Q = df['AV'].sum()
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

### Area Velocity and Mannings from in situ measurments
## stage2discharge_ratingcurve.AV_rating_curve(datadir,location,Fagaalu_stage_data,trapezoid=False,Slope=0.01,Mannings_n=0.03,width=4.9276)
## Returns DataFrame of Stage (cm) and Discharge (L/sec) calc. from AV measurements with time index

### Calculate Q from a single AV measurement
#fileQ = calcQ(datadir+'Q/LBJ_4-18-13.txt','LBJ',Fagaalu_stage_data,slope=Slope,Mannings_n=n,trapezoid=True)
## and save to CSV
#pd.concat(fileQ).to_csv(datadir+'Q/LBJ_4-18-13.csv')

### Discharge using Mannings and Surveyed Cros-section
#from ManningsRatingCurve import Mannings, Mannings_Series
def Mannings(XSfile,sheetname,Slope,Manning_n,k=1,stage_start=.01,stage_end=None,show=False,save=False,filename=''):    
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
    
    DF = pd.DataFrame({'stage':stages,'area':areas,'wp':wp,'r':r, 'Man_n':Man_n,'vel':v,'Q':q})
       
    return DF,df

    
def Mannings_Series(XSfile,sheetname,stage_series,Slope,Manning_n,k=1):    
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
    DF = pd.DataFrame({'stage':stages,'area':areas,'wp':wp,'r':r,'Man_n':Man_n,'vel':v,'Q':q},index=stage_series.index)
    return DF
    
## Read LBJ_Man Discharge from .csv, or calculate new if needed
if 'LBJ_Man' not in locals():
    try:
        print 'Loading Mannings Q for DAM from CSV'
        LBJ_Man_reduced = pd.DataFrame.from_csv(datadir+'Q/Manning_Q_files/LBJ_Man_reduced.csv')
        LBJ_Man = pd.DataFrame.from_csv(datadir+'Q/Manning_Q_files/LBJ_Man.csv')
    except:
        print 'Calculate Mannings Q for LBJ and saving to CSV'
        LBJ_S, LBJ_n, LBJ_k = 0.016, 'Jarrett', .06/.08
        LBJ_S, LBJ_n, LBJ_k = 0.016, .067, 1
        LBJ_stage_reduced = Fagaalu_stage_data['LBJ'].dropna().round(0).drop_duplicates().order()
        LBJ_Man_reduced = Mannings_Series(datadir+'Q/Cross_Section_Surveys/LBJ_cross_section.xlsx','LBJ_m',Slope=LBJ_S,Manning_n=LBJ_n,k=LBJ_k,stage_series=LBJ_stage_reduced)
        LBJ_Man_reduced.to_csv(datadir+'Q/Manning_Q_files/LBJ_Man_reduced.csv')
        LBJ_stage= Fagaalu_stage_data['LBJ']+5
        LBJ_Man= Mannings_Series(datadir+'Q/Cross_Section_Surveys/LBJ_cross_section.xlsx','LBJ_m',Slope=LBJ_S,Manning_n=LBJ_n,k=LBJ_k,stage_series=LBJ_stage)
        LBJ_Man.to_csv(datadir+'Q/Manning_Q_files/LBJ_Man.csv')
        pass
## Read DAM_Man Discharge from .csv, or calculate new if needed
if 'DAM_Man' not in locals():
    try:
        print 'Loading Mannings Q for DAM from CSV'
        DAM_Man_reduced = pd.DataFrame.from_csv(datadir+'Q/Manning_Q_files/DAM_Man_reduced.csv')
        DAM_Man = pd.DataFrame.from_csv(datadir+'Q/Manning_Q_files/DAM_Man.csv')
    except:
        print 'Calculate Mannings Q for DAM and saving to CSV'
        DAM_S, DAM_n,  DAM_k = 0.03, 'Jarrett', .025/.06
        DAM_stage_reduced = Fagaalu_stage_data['Dam'].dropna().round(0).drop_duplicates().order()
        DAM_Man_reduced = Mannings_Series(datadir+'Q/Cross_Section_Surveys/DAM_cross_section.xlsx','DAM_m',Slope=DAM_S,Manning_n=DAM_n,k=DAM_k,stage_series=DAM_stage_reduced)
        DAM_Man_reduced.to_csv(datadir+'Q/Manning_Q_files/DAM_Man_reduced.csv')
        DAM_stage = Fagaalu_stage_data['Dam']
        DAM_Man= Mannings_Series(datadir+'Q/Cross_Section_Surveys/DAM_cross_section.xlsx','DAM_m',Slope=0.03,Manning_n='Jarrett',k=.025/.06,stage_series=DAM_stage)
        DAM_Man.to_csv(datadir+'Q/Manning_Q_files/DAM_Man.csv')
        pass 

#### LBJ Stage-Discharge
# (3 rating curves: AV measurements, A measurment * Mannings V, Surveyed Cross-Section and Manning's equation)

## LBJ AV measurements
## Mannings parameters for A-ManningV
Slope = 0.0161 # m/m
LBJ_n=0.067 # Mountain stream rocky bed and rivers with variable sections and veg along banks (Dunne 1978)
LBJstageDischarge = AV_RatingCurve(datadir+'Q/Flow_Files/','LBJ',Fagaalu_stage_data,slope=Slope,Mannings_n=LBJ_n,trapezoid=True).dropna() #DataFrame with Q from AV measurements, Q from measured A with Manning-predicted V, stage, and Q from Manning's and assumed rectangular channel A
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

#### DAM Stage-Discharge
Slope= 0.3
DAM_n = 'Jarrett'
DAM_k = 1
## DAM AV Measurements
DAMstageDischarge = AV_RatingCurve(datadir+'Q/Flow_Files/','Dam',Fagaalu_stage_data,slope=Slope,Mannings_n=DAM_n).dropna() ### Returns DataFrame of Stage and Discharge calc. from AV measurements with time index
#DAMstageDischarge = DAMstageDischarge[10:]# throw out measurements when I didn't know how to use the flow meter very well
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


## This function calculates the coeff of determination (r2) for 
## a function (=Manning's rating curve) and some independent points (=AV Q measurements
def Manning_AV_r2(Man_Series,AV_Series):
    # LBJ Mannings = y predicted
    ManQ, Manstage = Man_Series['Q']*1000, Man_Series['stage']*100
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
DAM_Man_r2 = Manning_AV_r2(DAM_Man_reduced,DAMstageDischarge)

def Manning_AV_rmse(Man_Series,AV_Series):
    # LBJ Mannings = y predicted
    ManQ, Manstage = Man_Series['Q']*1000, Man_Series['stage']*100
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
    
    
def HEC_AV_r2(HEC_Series,AV_Series):
    # LBJ Mannings = y predicted
    HEC_Q, HECstage = HEC_Series['Q_HEC(L/sec)'].round(0), HEC_Series['stage(cm)']
    y_predicted = pd.DataFrame({'Q_HEC':HEC_Q.values},index=HECstage).sort()
    ## LBJ AV  = y
    AV_Q, AVstage = AV_Series['Q-AV(L/sec)'], AV_Series['stage(cm)']
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
DAM_HEC_r2 = HEC_AV_r2(DAM_HECstageDischarge,DAMstageDischarge)

def HEC_AV_rmse(HEC_Series,AV_Series):
    # LBJ Mannings = y predicted
    HEC_Q, HECstage = HEC_Series['Q_HEC(L/sec)'].round(0), HEC_Series['stage(cm)']
    y_predicted = pd.DataFrame({'Q_HEC':HEC_Q.values},index=HECstage).sort()
    ## LBJ AV  = y
    AV_Q, AVstage = AV_Series['Q-AV(L/sec)'], AV_Series['stage(cm)']
    y_ = pd.DataFrame({'Q_AV':AV_Q.values},index=AVstage).sort()
    y_['Q_Man'] = y_predicted
    y_=  y_.dropna() # keep it clean
    y_['Q_diff'] = y_['Q_AV'] - y_['Q_Man']
    y_['Q_diff_squared'] = (y_['Q_diff'])**2.
    y_rmse = (y_['Q_diff_squared'].sum()/len(y_))**0.5
    
    mean_observed = AV_Q.mean()
    rmse_percent = y_rmse/mean_observed *100.
    return int(y_rmse),int(mean_observed),int(rmse_percent)
DAM_HEC_rmse = HEC_AV_rmse(DAM_HECstageDischarge,DAMstageDischarge)[2]   


### Compare Discharg Ratings
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
    LBJ_ManQ, LBJ_Manstage = LBJ_Man_reduced['Q']*1000, LBJ_Man_reduced['stage']*100
    site_lbj.plot(LBJ_ManQ,LBJ_Manstage,'-',markersize=2,c='k',label='Mannings: n='+str(LBJ_n)+r'$ r^2$'+"%.2f"%LBJ_Man_r2)
    site_lbj_zoom.plot(LBJ_ManQ,LBJ_Manstage,'-',markersize=2,c='k',label='Mannings')
    ## Storm Thresholds
    site_lbj.axhline(LBJ_storm_threshold,ls='--',linewidth=0.6,c='k',label='Storm threshold')
    site_lbj_zoom.axhline(LBJ_storm_threshold,ls='--',linewidth=0.6,c='k',label='Storm threshold')
    ## Label point -click
    labelindex_subplot(site_lbj, LBJstageDischarge.index,LBJstageDischarge['Q-AV(L/sec)'],LBJstageDischarge['stage(cm)'])
    labelindex_subplot(site_lbj_zoom, LBJstageDischarge.index,LBJstageDischarge['Q-AV(L/sec)'],LBJstageDischarge['stage(cm)'])
    ## Label subplots    
    site_lbj.set_ylabel('Stage(cm)'),site_lbj.set_xlabel('Q(L/sec)'),site_lbj_zoom.set_xlabel('Q(L/sec)')
    ## Format subplots
    site_lbj.set_ylim(0,PT1['stage'].max()+10)#,site_lbj.set_xlim(0,LBJ_AVnonLinear(PT1['stage'].max()+10))
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
#plotQratingLBJ(show=True,log=False,save=False,filename=figdir+'')
#plotQratingLBJ(show=True,log=False,save=True)
#plotQratingLBJ(show=True,log=True,save=True)
#plotQratingLBJ(show=True,log=True,save=False)

### Compare Discharg Ratings
def plotQratingDAM(ms=6,show=False,log=False,save=False,filename=figdir+''): ## Rating Curves
    mpl.rc('lines',markersize=ms)
    fig, (site_dam, site_dam_zoom) = plt.subplots(1,2,figsize=(8,4))
    site_dam.text(0.95,0.95,'(a)',verticalalignment='top', horizontalalignment='right',transform=site_dam.transAxes,color='k',fontsize=10,fontweight='bold')
    site_dam_zoom.text(0.95,0.95,'(b)',verticalalignment='top', horizontalalignment='right',transform=site_dam_zoom.transAxes,color='k',fontsize=10,fontweight='bold')
    title="Discharge Ratings for FG1 (DAM)"
    xy = np.linspace(0,8000,8000)
    #DAM AV Measurements and Rating Curve
    site_dam.plot(DAMstageDischarge['Q-AV(L/sec)'][start2012:stop2012],DAMstageDischarge['stage(cm)'][start2012:stop2012],'o',color='k',fillstyle='none',label='AV 2012')
    site_dam.plot(DAMstageDischarge['Q-AV(L/sec)'][start2013:stop2013],DAMstageDischarge['stage(cm)'][start2013:stop2013],'^',color='k',fillstyle='none',label='AV 2013')
    site_dam.plot(DAMstageDischarge['Q-AV(L/sec)'][start2014:stop2014],DAMstageDischarge['stage(cm)'][start2014:stop2014],'s',color='k',fillstyle='none',label='AV 2014')
    #DAM AV Measurements and Rating Curve
    site_dam_zoom.plot(DAMstageDischarge['Q-AV(L/sec)'][start2012:stop2012],DAMstageDischarge['stage(cm)'][start2012:stop2012],'o',color='k',fillstyle='none',label='AV 2012')
    site_dam_zoom.plot(DAMstageDischarge['Q-AV(L/sec)'][start2013:stop2013],DAMstageDischarge['stage(cm)'][start2013:stop2013],'^',color='k',fillstyle='none',label='AV 2013')
    site_dam_zoom.plot(DAMstageDischarge['Q-AV(L/sec)'][start2014:stop2014],DAMstageDischarge['stage(cm)'][start2014:stop2014],'s',color='k',fillstyle='none',label='AV 2014')
    
    ### DAM Linear
    ## DAM Power    
    DAM_AVpower=powerfunction(DAMstageDischarge['Q-AV(L/sec)'],DAMstageDischarge['stage(cm)'])    
    PowerFit(DAMstageDischarge['Q-AV(L/sec)'],DAMstageDischarge['stage(cm)'],xy,site_dam,c='grey',ls='-', label='AV power law '+r'$r^2$'+"%.2f"%DAM_AVpower['r2']) ## rating from DAM_AV
    PowerFit(DAMstageDischarge['Q-AV(L/sec)'],DAMstageDischarge['stage(cm)'],xy,site_dam_zoom,c='grey',ls='-', label='AV power law '+r'$r^2$'+"%.2f"%DAM_AVpower['r2']) ## rating from DAM_AV
    #DAM HEC-RAS Model and Rating Curve
    #PowerFit(DAM_HECstageDischarge['Q_HEC(L/sec)'],DAM_HECstageDischarge['stage(cm)'],xy,site_dam,c='b',ls='--',label='DAM_HECpower '+r'$r^2$'+"%.2f"%DAM_HEC_r2) ## rating from DAM_HEC
    site_dam.plot(DAM_HECstageDischarge['Q_HEC(L/sec)'],DAM_HECstageDischarge['stage(cm)'],'-',color='k',label='HEC-RAS model '+r'$r^2$'+"%.2f"%DAM_HEC.r2)
    #PowerFit(DAM_HECstageDischarge['Q_HEC(L/sec)'],DAM_HECstageDischarge['stage(cm)'],xy,site_dam_zoom,c='b',ls='--',label='DAM_HECpower '+r'$r^2$'+"%.2f"%DAM_HEC_r2) ## rating from DAM_HEC
    site_dam_zoom.plot(DAM_HECstageDischarge['Q_HEC(L/sec)'],DAM_HECstageDischarge['stage(cm)'],'-',color='k',label='HEC-RAS model '+r'$r^2$'+"%.2f"%DAM_HEC.r2)
    ## DAM  FLUME
    
    ## DAM Mannings from stream survey
    DAM_ManQ, DAM_Manstage = DAM_Man_reduced['Q']*1000,DAM_Man_reduced['stage']*100
    #site_dam.plot(DAM_ManQ, DAM_Manstage,'-',markersize=2,color='r',label='Mannings DAM '+r'$r^2$'+"%.2f"%DAM_Man_r2)   
    #site_dam_zoom.plot(DAM_ManQ, DAM_Manstage,'-',markersize=2,color='r',label='Mannings DAM')   
    ## Label point-click
    labelindex_subplot(site_dam, DAMstageDischarge.index,DAMstageDischarge['Q-AV(L/sec)'],DAMstageDischarge['stage(cm)'])
    labelindex_subplot(site_dam_zoom, DAMstageDischarge.index,DAMstageDischarge['Q-AV(L/sec)'],DAMstageDischarge['stage(cm)'])
    ## Storm Thresholds
    site_dam.axhline(46,ls='-.',linewidth=0.6,c='grey',label='Channel top')
    site_dam.axhline(DAM_storm_threshold,ls='--',linewidth=0.6,c='grey',label='Storm threshold')
    site_dam_zoom.axhline(DAM_storm_threshold,ls='--',linewidth=0.6,c='grey',label='Storm threshold')
    ## Label subplots    
    site_dam.set_ylabel('Stage(cm)'),site_dam.set_xlabel('Q(L/sec)'),site_dam_zoom.set_xlabel('Q(L/sec)')
    ## Format subplots
    site_dam.set_ylim(0,PT3['stage'].max()+10)#,site_dam.set_xlim(0,HEC_piecewise(PT3['stage'].max()+10).values)
    site_dam_zoom.set_ylim(0,20),site_dam_zoom.set_xlim(0,500)
    ## Legends
    site_dam.legend(loc='best',fancybox=True)    
    fig.canvas.manager.set_window_title('Figure : '+title) 
    logaxes(log,fig)
    for ax in fig.axes:
        ax.autoscale_view(True,True,True)
    plt.tight_layout(pad=0.1)
    show_plot(show,fig)
    savefig(save,filename)
    return
#plotQratingDAM(ms=6,show=True,log=False,save=False,filename=figdir+'')
#plotQratingDAM(show=True,log=False,save=True)
#plotQratingDAM(show=True,log=True,save=True)
#plotQratingDAM(show=True,log=True,save=False)

#### CALCULATE DISCHARGE
## Calculate Q for LBJ
## Stage
LBJ = DataFrame(PT1,columns=['stage']) ## Build DataFrame with all stage records for location (cm)
## Mannings
LBJ['Q-Mannings'] = LBJ_Man['Q']*1000
## Power Models
a,b = 10**LBJ_AVLog.beta[1], LBJ_AVLog.beta[0]# beta[1] is the intercept = log10(a), so a = 10**beta[1] # beta[0] is the slope = b
LBJ['Q-AVLog'] = a * (LBJ['stage']**b)
a,b = 10**LBJ_AManningVLog.beta[1], LBJ_AManningVLog.beta[0]
LBJ['Q-AManningVLog'] = a*(LBJ['stage']**b)

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
LBJ['Q']= LBJ['Q-Mannings']
LBJ['Q-RMSE'] = LBJ_Man_rmse
print 'LBJ Q from Mannings and Surveyed Cross Section'
DAM['Q']= DAM['Q-HEC'].round(0)
DAM['Q-RMSE'] = DAM_HEC_rmse
print 'DAM Q from HEC-RAS and Surveyed Cross Section'

#### Calculate Q for QUARRY TODO
QUARRY = pd.DataFrame((DAM['Q']/.9)*1.17) ## Q* from DAM x Area Quarry
QUARRY['Q-RMSE'] = DAM['Q-RMSE']
QUARRY['stage']=DAM['stage']
## Convert to 15min interval LBJ
LBJq = (LBJ*900) ## Q above is in L/sec; L/sec * 900sec/15Min = L/15Min
LBJq['stage']=PT1['stage'] ## put unaltered stage back in

## Convert to 15min interval QUARRY
QUARRYq = (QUARRY*900) ## Q above is in L/sec; L/sec * 900sec/15Min = L/15Min
QUARRYq['stage']=PT3['stage'] ## put unaltered stage back in

## Convert to 15min interval DAM
DAMq= (DAM*900)## Q above is in L/sec; L/sec * 900sec/15Min = L/15Min
DAMq['stage']=PT3['stage'] ## put unaltered stage back in


    
def QYears(log=False,show=False,save=False,filename=''):
    mpl.rc('lines',markersize=6)
    fig, (Q2012,Q2013,Q2014)=plt.subplots(3)
    letter_subplots(fig,0.1,0.95,'top','right','k',font_size=10,font_weight='bold')
    
    for ax in fig.axes:
        ax.plot_date(LBJ['Q'].index,LBJ['Q'],ls='-',marker='None',c='k',label='Q FG3')
        #ax.plot(LBJstageDischarge.index,LBJstageDischarge['Q-AV(L/sec)'],ls='None',marker='o',color='k')
        ax.plot_date(DAM['Q'].index,DAM['Q'],ls='-',marker='None',c='grey',label='Q FG1')
        #ax.plot(DAMstageDischarge.index,DAMstageDischarge['Q-AV(L/sec)'],ls='None',marker='o',color='grey')
        ax.set_ylim(0,LBJ['Q'].max()+500)    
    Q2012.set_xlim(start2012,stop2012),Q2013.set_xlim(start2013,stop2013),Q2014.set_xlim(start2014,stop2014)
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
QYears(log=False,show=True,save=False,filename='')
    
### ..
## Import SSC Data
def loadSSC(SSCXL,sheet='ALL_MASTER',round_to_5=False,round_to_15=False):
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
            if parsed > fieldstart2014b:
                parsed = parsed + dt.timedelta(minutes=15)
            if round_to_5==True:
                parsed = misc_time.RoundTo5(parsed)
            if round_to_15==True:
                parsed = misc_time.RoundTo15(parsed)
            else:
                pass
        except:
            raise
            parsed = pd.to_datetime(pd.NaT)
        #print parsed
        return parsed
            
    SSC= SSCXL.parse(sheet,header=0,parse_dates=[['Date','Time']],date_parser=my_parser,index_col=['Date_Time'])
    SSC['NTU'], SSC['SSC (mg/L)'] = SSC['NTU'].round(0), SSC['SSC (mg/L)'].round(0)
    return SSC
SSCXL = pd.ExcelFile(datadir+'SSC/SSC_grab_samples.xlsx')
## ALL SSC samples
SSC= loadSSC(SSCXL,'ALL_MASTER',round_to_15=True)
SSC = SSC[SSC['SSC (mg/L)']>0]

## ALL SSC stormflow samples
SSC_all_storm_samples = pd.DataFrame()
for storm_index,storm in LBJ_StormIntervals.iterrows():
    #print storm[1]['start']
    start, end =storm['start']-dt.timedelta(minutes=60), storm['end']
    SSC_storm = SSC[start:end]
    SSC_all_storm_samples = SSC_all_storm_samples.append(SSC_storm)
## ALL SSC baseflow samples
SSC_all_baseflow_samples = SSC.drop(SSC_all_storm_samples.index) 

##ALL SSC samples pre-mitigation
SSC_pre_mitigation = SSC[SSC.index<Mitigation]
SSC_pre_mitigation_storm_samples = SSC_all_storm_samples[SSC_all_storm_samples.index<Mitigation]
SSC_pre_mitigation_baseflow_samples = SSC_all_baseflow_samples[SSC_all_baseflow_samples.index<Mitigation]
##ALL SSC samples post-mitigation
SSC_post_mitigation = SSC[SSC.index>Mitigation]
SSC_post_mitigation_storm_samples = SSC_all_storm_samples[SSC_all_storm_samples.index>Mitigation]
SSC_post_mitigation_baseflow_samples = SSC_all_baseflow_samples[SSC_all_baseflow_samples.index>Mitigation]

## Put SSC subsets in a dictionary
SSC_dict={'ALL':SSC,'ALL-storm':SSC_all_storm_samples,'Pre-ALL':SSC_pre_mitigation,'Pre-storm':SSC_pre_mitigation_storm_samples,'Pre-baseflow':SSC_pre_mitigation_baseflow_samples,'Post-ALL':SSC_post_mitigation,'Post-storm':SSC_post_mitigation_storm_samples,'Post-baseflow':SSC_post_mitigation_baseflow_samples }
#SSC_raw_time = loadSSC(SSCXL,'ALL_MASTER')
#SSC_raw_time[SSC_raw_time['Location'].isin(['LBJ'])]['SSC (mg/L)'].plot(ls='None',marker='.',c='g')

#### SSC Grab sample ANALYSIS
def sample_counts(SSCdata):
    SampleCounts = DataFrame(data=[str(val) for val in pd.unique(SSCdata['Location'])],columns=['Location'])
    SampleCounts['#ofSSCsamples']=pd.Series([len(SSCdata[SSCdata['Location']==str(val)]) for val in pd.unique(SSCdata['Location'])]) ##add column of Locations
    return SampleCounts
SampleCounts = sample_counts(SSC_dict['Pre-ALL'])

### SSC Sample Counts from Unique Sites
## from SampleCounts select rows where SampleCounts['Location'] starts with 'Quarry'; sum up the #ofSSCsamples column
AllQuarrySamples = pd.DataFrame(data=[[SampleCounts[SampleCounts['Location'].str.startswith('Quarry')]['#ofSSCsamples'].sum(),'AllQuarry']],columns=['#ofSSCsamples','Location']) ## make DataFrame of the sum of all records that Location starts wtih 'Quarry'
SampleCounts = SampleCounts.append(AllQuarrySamples)
## drop the columns that were counted above to get a DataFrame of unique sampling locations
SampleCounts= SampleCounts.drop(SampleCounts[SampleCounts['Location'].str.startswith(('N1','N2','Quarry'))].index)
SampleCounts.index=range(1,len(SampleCounts)+1)

## SSC Boxplots and Discharge Concentration
## LBJ
LBJgrab = SSC[SSC['Location'].isin(['LBJ'])]#.resample('5Min',fill_method='pad',limit=0)
LBJgrab['index']=LBJgrab.index
LBJ_grab_count = SampleCounts['#ofSSCsamples'][SampleCounts['Location']=='LBJ'].ix[2] ## the # in .ix[#] is the row number in SampleCounts above
#LBJ_R2 = SSC[SSC['Location'].isin(['LBJ R2'])].resample('5Min',fill_method='pad',limit=0)
#LBJ_R2_grab_count = SampleCounts['#ofSSCsamples'][SampleCounts['Location']=='LBJ R2'].ix[12] ## the # in .ix[#] is the row number in SampleCounts above

## QUARRY
# Just DT
QUARRYgrab =SSC[SSC['Location'].isin(['DT'])]#.resample('5Min',fill_method='pad',limit=0)
QUARRYgrab['index']= QUARRYgrab.index
QUARRY_grab_count =  SampleCounts['#ofSSCsamples'][SampleCounts['Location']=='DT'].ix[3] ## the # in .ix[#] is the row number in SampleCounts above
# Just R2
QUARRY_R2 =SSC[SSC['Location'].isin(['R2'])]#.resample('5Min',fill_method='pad',limit=0)
QUARRY_R2['index'] = QUARRY_R2.index
QUARRY_R2_grab_count =  SampleCounts['#ofSSCsamples'][SampleCounts['Location']=='R2'].ix[5] ## the # in .ix[#] is the row number in SampleCounts above
# combined DT and R2
QUARRY_DT_and_R2 = SSC[SSC['Location'].isin(['DT','R2'])]
QUARRY_DT_and_R2['index'] = QUARRY_DT_and_R2.index

## DAM
DAMgrab = SSC[SSC['Location'].isin(['DAM'])]#.resample('5Min',fill_method='pad',limit=0)
DAMgrab['index'] = DAMgrab.index
DAM_grab_count =  SampleCounts['#ofSSCsamples'][SampleCounts['Location']=='DAM'].ix[1] ## the # in .ix[#] is the row number in SampleCounts above


## ADD Grab samples to Site DataFrames
LBJ['Grab-SSC-mg/L'] = LBJgrab.drop_duplicates(cols='index')['SSC (mg/L)']
QUARRY['GrabDT-SSC-mg/L'] = QUARRYgrab.drop_duplicates(cols='index')['SSC (mg/L)']
QUARRY['GrabR2-SSC-mg/L'] = QUARRY_R2.drop_duplicates(cols='index')['SSC (mg/L)']
QUARRY['Grab-SSC-mg/L'] = QUARRY_DT_and_R2.drop_duplicates(cols='index')['SSC (mg/L)']
DAM['Grab-SSC-mg/L'] = DAMgrab.drop_duplicates(cols='index')['SSC (mg/L)']





def SSCprobplots(subset='pre',withR2=False,show=False,save=False,filename=figdir+''):
   
    ## Subset SSC
    ## Pre-mitigation baseflow
    SSC = SSC_dict[subset[0]]
    LBJgrab = SSC[SSC['Location'].isin(['LBJ'])]
    QUARRYgrab =SSC[SSC['Location'].isin(['DT'])]
    DAMgrab = SSC[SSC['Location'].isin(['DAM'])]
    if withR2==True:
        ## Add samples from Autosampler at QUARRY
        print 'Adding R2 samples to QUARRY Grab (DT)'
        QUARRYgrab =SSC[SSC['Location'].isin(['DT','R2'])]
    elif withR2==False:
        QUARRYgrab =SSC[SSC['Location'].isin(['DT'])]  
    ## Compile
    GrabSamples = pd.concat([DAMgrab['SSC (mg/L)'].reset_index()['SSC (mg/L)'],QUARRYgrab['SSC (mg/L)'].reset_index()['SSC (mg/L)'],
                                 LBJgrab['SSC (mg/L)'].reset_index()['SSC (mg/L)']],ignore_index=True,axis=1)    
    GrabSamples.columns = ['DAM','QUARRY','LBJ']
    
    ax1 = plt.subplot(231)
    stats.probplot(GrabSamples['DAM'].dropna(), plot=plt)
    
    ax2 = plt.subplot(232)
    stats.probplot(GrabSamples['QUARRY'].dropna(), plot=plt)
    ax3 = plt.subplot(233)
    stats.probplot(GrabSamples['LBJ'].dropna(), plot=plt)    
    
    ## Subset SSC
    ## Pre-mitigation stormflow
    SSC = SSC_dict[subset[1]]
    LBJgrab = SSC[SSC['Location'].isin(['LBJ'])]
    QUARRYgrab =SSC[SSC['Location'].isin(['DT'])]
    DAMgrab = SSC[SSC['Location'].isin(['DAM'])]
    if withR2==True:
        ## Add samples from Autosampler at QUARRY
        print 'Adding R2 samples to QUARRY Grab (DT)'
        QUARRYgrab =SSC[SSC['Location'].isin(['DT','R2'])]
    elif withR2==False:
        QUARRYgrab =SSC[SSC['Location'].isin(['DT'])]  
    ## Compile
    GrabSamples = pd.concat([DAMgrab['SSC (mg/L)'].reset_index()['SSC (mg/L)'],QUARRYgrab['SSC (mg/L)'].reset_index()['SSC (mg/L)'],
                                 LBJgrab['SSC (mg/L)'].reset_index()['SSC (mg/L)']],ignore_index=True,axis=1)    
    GrabSamples.columns = ['DAM','QUARRY','LBJ']
    
    ax4 = plt.subplot(234)
    stats.probplot(GrabSamples['DAM'].dropna(), plot=plt)
    ax5 = plt.subplot(235)
    stats.probplot(GrabSamples['QUARRY'].dropna(), plot=plt)
    ax6 = plt.subplot(236)
    stats.probplot(GrabSamples['LBJ'].dropna(), plot=plt)
    
    ax1.set_ylabel('Baseflow'), ax4.set_ylabel('Stormflow')
    
    ax1.set_title('DAM'), ax2.set_title('QUARRY'), ax3.set_title('LBJ')
    ax4.set_title('DAM'), ax5.set_title('QUARRY'), ax6.set_title('LBJ')
    plt.tight_layout(pad=0.1)
    show_plot(show)
    savefig(save,filename)
    return
#SSCprobplots(subset=['Pre-baseflow','Pre-storm'],withR2=False,show=True,save=False,filename=figdir+'')

def plotSSCboxplots(subset='pre',withR2=False,log=False,show=False,save=False,filename=figdir+''):
    #mpl.rc('lines',markersize=300)
    mpl.rc('legend',scatterpoints=1)  
    fig, (ax1,ax2)=plt.subplots(1,2,figsize=(6,3),sharey=True)
    ax1.text(0.01,0.95,'(a) Baseflow',verticalalignment='top', horizontalalignment='left',transform=ax1.transAxes,color='k',fontsize=10,fontweight='bold')
    ax2.text(0.01,0.95,'(b) Stormflow',verticalalignment='top', horizontalalignment='left',transform=ax2.transAxes,color='k',fontsize=10,fontweight='bold')        
    
    ## Subset SSC
    ## Pre-mitigation baseflow
    SSC = SSC_dict[subset[0]]
    LBJgrab = SSC[SSC['Location'].isin(['LBJ'])]
    QUARRYgrab =SSC[SSC['Location'].isin(['DT'])]
    DAMgrab = SSC[SSC['Location'].isin(['DAM'])]
    if withR2==True:
        ## Add samples from Autosampler at QUARRY
        print 'Adding R2 samples to QUARRY Grab (DT)'
        QUARRYgrab =SSC[SSC['Location'].isin(['DT','R2'])]
    elif withR2==False:
        QUARRYgrab =SSC[SSC['Location'].isin(['DT'])]  
    ## Compile
    GrabSamples = pd.concat([DAMgrab['SSC (mg/L)'].reset_index()['SSC (mg/L)'],QUARRYgrab['SSC (mg/L)'].reset_index()['SSC (mg/L)'],
                                 LBJgrab['SSC (mg/L)'].reset_index()['SSC (mg/L)']],ignore_index=True,axis=1)    
    GrabSamples.columns = ['DAM','QUARRY','LBJ']
    
    ## Parametric
    f1,p1 =  stats.f_oneway(GrabSamples['DAM'].dropna(),GrabSamples['QUARRY'].dropna(),GrabSamples['LBJ'].dropna())   
    print "ANOVA: f = %g  p = %g" % (f1,p1)
    QUARRY_DAM_ttest1 = stats.ttest_ind(GrabSamples['QUARRY'].dropna(), GrabSamples['DAM'].dropna(), axis=0, equal_var=True)   
    print "QUARRY v DAM ttest_ind: t = %g  p = %g" % QUARRY_DAM_ttest1
    QUARRY_LBJ_ttest1 = stats.ttest_ind(GrabSamples['QUARRY'].dropna(), GrabSamples['LBJ'].dropna(), axis=0, equal_var=True)   
    print "QUARRY v LBJ ttest_ind: t = %g  p = %g" % QUARRY_LBJ_ttest1 
    ## Non-Parametric
    H1, KWp1 = stats.mstats.kruskalwallis(GrabSamples['DAM'].dropna(),GrabSamples['QUARRY'].dropna(),GrabSamples['LBJ'].dropna())
    print "Kruskall-Wallis: H = %g  p = %g" % (H1, KWp1) 
    QUARRY_DAM_mannwhit1 = stats.mannwhitneyu(GrabSamples['QUARRY'].dropna(), GrabSamples['DAM'].dropna())   
    print "QUARRY v DAM mannwhit: u = %g  p/2 = %g" % QUARRY_DAM_mannwhit1
    QUARRY_LBJ_mannwhit1 = stats.mannwhitneyu(GrabSamples['QUARRY'].dropna(), GrabSamples['LBJ'].dropna())   
    print "QUARRY v LBJ mannwhit: u = %g  p/2 = %g" % QUARRY_LBJ_mannwhit1 
    

    GrabSampleMeans = [DAMgrab['SSC (mg/L)'].mean(),QUARRYgrab['SSC (mg/L)'].mean(),LBJgrab['SSC (mg/L)'].mean()]
    GrabSampleVals = np.concatenate([DAMgrab['SSC (mg/L)'].values.tolist(),QUARRYgrab['SSC (mg/L)'].values.tolist(),LBJgrab['SSC (mg/L)'].values.tolist()])
    GrabSampleCategories = np.concatenate([[1]*len(DAMgrab['SSC (mg/L)']),[2]*len(QUARRYgrab['SSC (mg/L)']),[3]*len(LBJgrab['SSC (mg/L)'])])
    GrabSamples.columns = ['FG1','FG2','FG3']
    bp1 = GrabSamples.boxplot(ax=ax1)
    ax1.scatter(GrabSampleCategories,GrabSampleVals,s=40,marker='+',c='grey',label='SSC (mg/L)')    
    
    ## Subset SSC
    ## Pre-mitigation stormflow
    SSC = SSC_dict[subset[1]]
    LBJgrab = SSC[SSC['Location'].isin(['LBJ'])]
    QUARRYgrab =SSC[SSC['Location'].isin(['DT'])]
    DAMgrab = SSC[SSC['Location'].isin(['DAM'])]
    if withR2==True:
        ## Add samples from Autosampler at QUARRY
        print 'Adding R2 samples to QUARRY Grab (DT)'
        QUARRYgrab =SSC[SSC['Location'].isin(['DT','R2'])]
    elif withR2==False:
        QUARRYgrab =SSC[SSC['Location'].isin(['DT'])]  
    ## Compile
    GrabSamples = pd.concat([DAMgrab['SSC (mg/L)'].reset_index()['SSC (mg/L)'],QUARRYgrab['SSC (mg/L)'].reset_index()['SSC (mg/L)'],
                                 LBJgrab['SSC (mg/L)'].reset_index()['SSC (mg/L)']],ignore_index=True,axis=1)    
    GrabSamples.columns = ['DAM','QUARRY','LBJ']
    ## Parametric
    f2,p2 =  stats.f_oneway(GrabSamples['DAM'].dropna(),GrabSamples['QUARRY'].dropna(),GrabSamples['LBJ'].dropna())   
    print "ANOVA: f = %g  p = %g" % (f2,p2)
    QUARRY_DAM_ttest2 = stats.ttest_ind(GrabSamples['QUARRY'].dropna(), GrabSamples['DAM'].dropna(), axis=0, equal_var=True)   
    print "QUARRY v DAM ttest_ind: t = %g  p = %g" % QUARRY_DAM_ttest2 
    QUARRY_LBJ_ttest2 = stats.ttest_ind(GrabSamples['QUARRY'].dropna(), GrabSamples['LBJ'].dropna(), axis=0, equal_var=True)   
    print "QUARRY v LBJ ttest_ind: t = %g  p = %g" % QUARRY_LBJ_ttest2     
    ## Non-Parametric
    H2, KWp2 = stats.mstats.kruskalwallis(GrabSamples['DAM'].dropna(),GrabSamples['QUARRY'].dropna(),GrabSamples['LBJ'].dropna())
    print "Kruskall-Wallis: H = %g  p = %g" % (H2, KWp2) 
    QUARRY_DAM_mannwhit2 = stats.mannwhitneyu(GrabSamples['QUARRY'].dropna(), GrabSamples['DAM'].dropna())   
    print "QUARRY v DAM mannwhit: u = %g  p/2 = %g" % QUARRY_DAM_mannwhit2
    QUARRY_LBJ_mannwhit2 = stats.mannwhitneyu(GrabSamples['QUARRY'].dropna(), GrabSamples['LBJ'].dropna())   
    print "QUARRY v LBJ mannwhit: u = %g  p/2 = %g" % QUARRY_LBJ_mannwhit2  
    
    GrabSampleMeans = [DAMgrab['SSC (mg/L)'].mean(),QUARRYgrab['SSC (mg/L)'].mean(),LBJgrab['SSC (mg/L)'].mean()]
    GrabSampleVals = np.concatenate([DAMgrab['SSC (mg/L)'].values.tolist(),QUARRYgrab['SSC (mg/L)'].values.tolist(),LBJgrab['SSC (mg/L)'].values.tolist()])
    GrabSampleCategories = np.concatenate([[1]*len(DAMgrab['SSC (mg/L)']),[2]*len(QUARRYgrab['SSC (mg/L)']),[3]*len(LBJgrab['SSC (mg/L)'])])
    GrabSamples.columns = ['FG1','FG2','FG3']    
    bp2 = GrabSamples.boxplot(ax=ax2)
    ax2.scatter(GrabSampleCategories,GrabSampleVals,s=40,marker='+',c='grey',label='SSC (mg/L)')    
    
    ## Format plots
    plt.setp(bp1['boxes'], color='black'), plt.setp(bp2['boxes'], color='black')
    plt.setp(bp1['whiskers'], color='black'), plt.setp(bp2['whiskers'], color='black')
    plt.setp(bp1['fliers'], color='grey', marker='+'), plt.setp(bp2['fliers'], color='grey', marker='+') 
    plt.setp(bp1['medians'], color='black', marker='+'), plt.setp(bp2['medians'], color='black', marker='+') 

    ## Add Mean values
    ax1.scatter([1,2,3],GrabSampleMeans,s=40,color='k',label='Mean SSC (mg/L)')
    ax2.scatter([1,2,3],GrabSampleMeans,s=40,color='k',label='Mean SSC (mg/L)')    
    
    #ax1.legend(), ax2.legend()    
    if log==True:
        ax1.set_yscale('log'), ax2.set_yscale('log')   
    ax1.set_ylabel('SSC (mg/L)'),ax1.set_xlabel('Location'),ax2.set_xlabel('Location')
    #plt.suptitle("Suspended Sediment Concentrations at sampling locations in Fag'alu",fontsize=16)
    plt.legend()
    plt.tight_layout(pad=0.1)
    show_plot(show)
    savefig(save,filename)
    return f1,p1,QUARRY_DAM_ttest1,QUARRY_LBJ_ttest1,H1,KWp1,QUARRY_DAM_mannwhit1,QUARRY_LBJ_mannwhit1, f2,p2,QUARRY_DAM_ttest2,QUARRY_LBJ_ttest2,H2, KWp2,QUARRY_DAM_mannwhit2,QUARRY_LBJ_mannwhit2
## Premitigation
plotSSCboxplots(subset=['Pre-baseflow','Pre-storm'],withR2=False,log=True,show=True,save=False,filename='')
#plotSSCboxplots(subset='Pre-storm',withR2=False,show=True,save=False,filename='')
#plotSSCboxplots(subset='pre',withR2=True,show=True) # R2 samples not comparable with others

## Postmitigation
#plotSSCboxplots(subset='post',storm_samples_only=False,withR2=False,show=True,save=False,filename='')

### Build data for Discharge/Concentration Rating Curve   
   
def plotQvsC_with_timeseries(subset='pre',storm_samples_only=False,ms=6,show=False,log=False,save=False,filename=figdir+''):  
    ## Subset SSC
    if subset=='pre' and storm_samples_only==True:
        SSC = SSC_dict['Pre-storm']
    elif subset=='pre' and  storm_samples_only==False:
        SSC = SSC_dict['Pre-ALL']
    elif subset=='post' and storm_samples_only==True:
        SSC = SSC_dict['Post-storm']
    elif subset=='post' and  storm_samples_only==False:
        SSC = SSC_dict['Post-ALL']    
    ## Append Discharge (Q) data
    dam_ssc = pd.DataFrame(SSC[SSC['Location']=='DAM']['SSC (mg/L)'])
    dam_ssc['Q']=DAM['Q']
    dam_ssc = dam_ssc.dropna()
    quarry_ssc = pd.DataFrame(SSC[SSC['Location'].isin(['DT','R2'])]['SSC (mg/L)'])
    quarry_ssc['Q']=QUARRY['Q']
    quarry_ssc =quarry_ssc.dropna()
    lbj_ssc = pd.DataFrame(SSC[SSC['Location']=='LBJ']['SSC (mg/L)'])
    lbj_ssc['Q']=LBJ['Q']
    lbj_ssc=lbj_ssc.dropna()
    ## Subset by year
    dam_ssc2012,dam_ssc2013,dam_ssc2014 = dam_ssc[start2012:stop2012],dam_ssc[start2013:stop2013],dam_ssc[start2014:stop2014]
    quarry2012,quarry2013,quarry2014 = quarry_ssc[start2012:stop2012],quarry_ssc[start2013:stop2013],quarry_ssc[start2014:stop2014]
    lbj_ssc2012,lbj_ssc2013,lbj_ssc2014 = lbj_ssc[start2012:stop2012],lbj_ssc[start2013:stop2013],lbj_ssc[start2014:stop2014]
    ## Regression
    damQC = pd.ols(y=dam_ssc['SSC (mg/L)'],x=dam_ssc['Q'])
    quarQC =  pd.ols(y=quarry_ssc['SSC (mg/L)'],x=quarry_ssc['Q'])
    lbjQC = pd.ols(y=lbj_ssc['SSC (mg/L)'],x=lbj_ssc['Q'])

    fig=plt.figure(figsize=(10,6))
    ts_log = plt.subplot2grid((3,3),(0,0),colspan=3)
    ts = plt.subplot2grid((3,3),(1,0),colspan=3)
    up = plt.subplot2grid((3,3),(2,0))
    quar = plt.subplot2grid((3,3),(2,1))
    down = plt.subplot2grid((3,3),(2,2))
    ts_log.text(0.05,0.95,'(a)',verticalalignment='top', horizontalalignment='right',transform=ts_log.transAxes,color='k',fontsize=10,fontweight='bold')
    ts.text(0.05,0.95,'(b)',verticalalignment='top', horizontalalignment='right',transform=ts.transAxes,color='k',fontsize=10,fontweight='bold')
    up.text(0.1,0.95,'(c)',verticalalignment='top', horizontalalignment='right',transform=up.transAxes,color='k',fontsize=10,fontweight='bold')
    quar.text(0.1,0.95,'(d)',verticalalignment='top', horizontalalignment='right',transform=quar.transAxes,color='k',fontsize=10,fontweight='bold')
    down.text(0.1,0.95,'(e)',verticalalignment='top', horizontalalignment='right',transform=down.transAxes,color='k',fontsize=10,fontweight='bold')
    #fig, (up,quar,down) = plt.subplots(1,3,figsize=(8,3))
    mpl.rc('lines',markersize=ms)
    mpl.rc('grid',alpha=0.0) 
    ## plot LBJ samples
    down.set_title('FG3',fontsize=10)
    down.loglog(lbj_ssc2012['Q'],lbj_ssc2012['SSC (mg/L)'],'o',fillstyle='none',c='k',label='2012')
    down.loglog(lbj_ssc2013['Q'],lbj_ssc2013['SSC (mg/L)'],'^',fillstyle='none',c='k',label='2013')
    down.loglog(lbj_ssc2014['Q'],lbj_ssc2014['SSC (mg/L)'],'s',fillstyle='none',c='k',label='2014')
    ## loglog quarry samples
    quar.set_title('FG2',fontsize=10)
    quar.loglog(quarry2012['Q'],quarry2012['SSC (mg/L)'],'o',fillstyle='none',c='k',label='2012')
    quar.loglog(quarry2013['Q'],quarry2013['SSC (mg/L)'],'^',fillstyle='none',c='k',label='2013')
    quar.loglog(quarry2014['Q'],quarry2014['SSC (mg/L)'],'s',fillstyle='none',c='k',label='2014')
    ## loglog DAM samples
    up.set_title('FG1',fontsize=10)
    up.loglog(dam_ssc2012['Q'],dam_ssc2012['SSC (mg/L)'],'o',fillstyle='none',c='k',label='2012')
    up.loglog(dam_ssc2013['Q'],dam_ssc2013['SSC (mg/L)'],'^',fillstyle='none',c='k',label='2013')
    up.loglog(dam_ssc2014['Q'],dam_ssc2014['SSC (mg/L)'],'s',fillstyle='none',c='k',label='2014')
    ## plot a line marking storm threshold and label it
    storm_Q_DAM = DAM[DAM['stage']==DAM_storm_threshold.round(0)]['Q'][0]
    storm_Q_LBJ = LBJ[LBJ['stage']==LBJ_storm_threshold.round(0)]['Q'][0]
    up.axvline(x=storm_Q_DAM,ls='--',color='k'),quar.axvline(x=storm_Q_DAM,ls='--',color='k'),down.axvline(x=storm_Q_LBJ,ls='--',color='k')  
    ## Limits
    down.set_ylim(10**0,10**5), quar.set_ylim(10**0,10**5), up.set_ylim(10**0,10**5)
    down.set_xlim(10**1,10**5),quar.set_xlim(10**1,10**5),up.set_xlim(10**1,10**5)
    up.set_ylabel('SSC (mg/L)'), up.set_xlabel('Q (L/sec)'), quar.set_xlabel('Q (L/sec)'), down.set_xlabel('Q (L/sec)')
    up.legend(loc='best'), quar.legend(loc='best'), down.legend(loc='best')
    ## Time series plot
    DAM_Stormflow_conditions = DAM[DAM['stage']==DAM_storm_threshold.round(0)]['Q'][0]
    QUARRY_Stormflow_conditions = (DAM_Stormflow_conditions/.9)*1.17 
    SSC = SSC_dict['Pre-ALL']
    dam_ssc = dam_ssc[dam_ssc['Q'] <  DAM_Stormflow_conditions]
    quarry_ssc = quarry_ssc[quarry_ssc['Q'] < QUARRY_Stormflow_conditions]
    #log
    dam_ssc['SSC (mg/L)'].plot(ax=ts_log,ls='None',marker='s',fillstyle='none',color='grey',label='FG1')
    quarry_ssc['SSC (mg/L)'].plot(ax=ts_log,ls='None',marker='o',fillstyle='none',color='k',label='FG2')
    ts_log.legend(),ts_log.set_ylabel('SSC mg/L'),ts_log.set_yscale('log')
    ts_log.axvline(dt.datetime(2012,8,1),0,13000,c='k',ls='--'),ts_log.text(dt.datetime(2012,8,1),5000,'Baseflow sediment mitigtaion at quarry')
    ts_log.tick_params(axis='x',which='both',bottom='off',top='off',labelbottom='off') # labels along the bottom edge are off
    ts_log.spines['bottom'].set_visible(False)
    #linear
    dam_ssc['SSC (mg/L)'].plot(ax=ts,ls='None',marker='s',fillstyle='none',color='grey',label='FG1')
    quarry_ssc['SSC (mg/L)'].plot(ax=ts,ls='None',marker='o',fillstyle='none',color='k',label='FG2')
    ts.legend(),ts.set_ylabel('SSC mg/L')#,ts.set_yscale('log')
    ts.axvline(dt.datetime(2012,8,1),0,13000,c='k',ls='--')
    ts.tick_params(axis='x',which='both',bottom='off',top='off',labelbottom='off') # labels along the bottom edge are off
    ts.spines['bottom'].set_visible(False)
    
    plt.tight_layout(pad=0.1)
    show_plot(show,fig)
    savefig(save,filename)
    return
    
def plotQvsC(subset='pre',storm_samples_only=False,ms=6,show=False,log=False,save=False,filename=figdir+''):  
    ## Subset SSC
    if subset=='pre' and storm_samples_only==True:
        SSC = SSC_dict['Pre-storm']
    elif subset=='pre' and  storm_samples_only==False:
        SSC = SSC_dict['Pre-ALL']
    elif subset=='post' and storm_samples_only==True:
        SSC = SSC_dict['Post-storm']
    elif subset=='post' and  storm_samples_only==False:
        SSC = SSC_dict['Post-ALL']    
    ## Append Discharge (Q) data
    dam_ssc = pd.DataFrame(SSC[SSC['Location']=='DAM']['SSC (mg/L)'])
    dam_ssc['Q']=DAM['Q']
    dam_ssc = dam_ssc.dropna()
    quarry_ssc = pd.DataFrame(SSC[SSC['Location'].isin(['DT','R2'])]['SSC (mg/L)'])
    quarry_ssc['Q']=QUARRY['Q']
    quarry_ssc =quarry_ssc.dropna()
    lbj_ssc = pd.DataFrame(SSC[SSC['Location']=='LBJ']['SSC (mg/L)'])
    lbj_ssc['Q']=LBJ['Q']
    lbj_ssc=lbj_ssc.dropna()
    ## Subset by year
    dam_ssc2012,dam_ssc2013,dam_ssc2014 = dam_ssc[start2012:stop2012],dam_ssc[start2013:stop2013],dam_ssc[start2014:stop2014]
    quarry2012,quarry2013,quarry2014 = quarry_ssc[start2012:stop2012],quarry_ssc[start2013:stop2013],quarry_ssc[start2014:stop2014]
    lbj_ssc2012,lbj_ssc2013,lbj_ssc2014 = lbj_ssc[start2012:stop2012],lbj_ssc[start2013:stop2013],lbj_ssc[start2014:stop2014]
    ## Regression
    damQC = pd.ols(y=dam_ssc['SSC (mg/L)'],x=dam_ssc['Q'])
    quarQC =  pd.ols(y=quarry_ssc['SSC (mg/L)'],x=quarry_ssc['Q'])
    lbjQC = pd.ols(y=lbj_ssc['SSC (mg/L)'],x=lbj_ssc['Q'])

    fig, (up,quar,down) = plt.subplots(1,3,figsize=(8,3))
    letter_subplots(fig,0.1,0.95,'top','right','k',font_size=10,font_weight='bold')
    #
    mpl.rc('lines',markersize=ms)
    mpl.rc('grid',alpha=0.0) 
    ## plot LBJ samples
    down.set_title('FG3',fontsize=10)
    down.loglog(lbj_ssc2012['Q'],lbj_ssc2012['SSC (mg/L)'],'o',fillstyle='none',c='k',label='2012')
    down.loglog(lbj_ssc2013['Q'],lbj_ssc2013['SSC (mg/L)'],'^',fillstyle='none',c='k',label='2013')
    down.loglog(lbj_ssc2014['Q'],lbj_ssc2014['SSC (mg/L)'],'s',fillstyle='none',c='k',label='2014')
    ## loglog quarry samples
    quar.set_title('FG2',fontsize=10)
    quar.loglog(quarry2012['Q'],quarry2012['SSC (mg/L)'],'o',fillstyle='none',c='k',label='2012')
    quar.loglog(quarry2013['Q'],quarry2013['SSC (mg/L)'],'^',fillstyle='none',c='k',label='2013')
    quar.loglog(quarry2014['Q'],quarry2014['SSC (mg/L)'],'s',fillstyle='none',c='k',label='2014')
    ## loglog DAM samples
    up.set_title('FG1',fontsize=10)
    up.loglog(dam_ssc2012['Q'],dam_ssc2012['SSC (mg/L)'],'o',fillstyle='none',c='k',label='2012')
    up.loglog(dam_ssc2013['Q'],dam_ssc2013['SSC (mg/L)'],'^',fillstyle='none',c='k',label='2013')
    up.loglog(dam_ssc2014['Q'],dam_ssc2014['SSC (mg/L)'],'s',fillstyle='none',c='k',label='2014')
    ## plot a line marking storm threshold and label it
    storm_Q_DAM = DAM[DAM['stage']==DAM_storm_threshold.round(0)]['Q'][0]
    storm_Q_LBJ = LBJ[LBJ['stage']==LBJ_storm_threshold.round(0)]['Q'][0]
    up.axvline(x=storm_Q_DAM,ls='--',color='k'),quar.axvline(x=storm_Q_DAM,ls='--',color='k'),down.axvline(x=storm_Q_LBJ,ls='--',color='k')  
    ## Limits
    down.set_ylim(10**0,10**5), quar.set_ylim(10**0,10**5), up.set_ylim(10**0,10**5)
    down.set_xlim(10**1,10**5),quar.set_xlim(10**1,10**5),up.set_xlim(10**1,10**5)
    up.set_ylabel('SSC (mg/L)'), up.set_xlabel('Q (L/sec)'), quar.set_xlabel('Q (L/sec)'), down.set_xlabel('Q (L/sec)')
    up.legend(loc='best')#, quar.legend(loc='best'), down.legend(loc='best')
    quar.loglog([10**2],[10**3.5],'s',markersize=60.,fillstyle='none',color='grey')
    
    plt.tight_layout(pad=0.1)
    show_plot(show,fig)
    savefig(save,filename)
    return
## Pre-mitigation
#plotQvsC(subset='pre',storm_samples_only=False,ms=6,show=True,log=True,save=False,filename=figdir+'')
#plotQvsC(subset='pre',storm_samples_only=True,ms=8,show=True,log=False,save=False,filename=figdir+'')
## Post-mitgation
#plotQvsC(subset='post',storm_samples_only=False,ms=6,show=True,log=False,save=False,filename=figdir+'')
#plotQvsC(subset='post',storm_samples_only=True,ms=8,show=True,log=False,save=False,filename=figdir+'')
#    
### Grab samples to SSYev   
def InterpolateGrabSamples(Stormslist,Data,storm_offset=0):
    Events=pd.DataFrame()
    for storm_index,storm in Stormslist.iterrows():
        print storm
        start = storm['start']-dt.timedelta(minutes=storm_offset) ##if Storms are defined by stream response you have to grab the preceding precip data
        end= storm['end']
        print str(start)+' '+str(end)
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
            print 'Interpolating data for storm '+str(start)
            event.ix[start] = 1
            event.ix[end]= 1
            Event=pd.DataFrame({'Grab':event}).resample('15Min')
            ## interpolation methods: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.interpolate.html
            Event['GrabInterpolated']=Event['Grab'].interpolate('time')
            Events = Events.append(Event)
        #Events = Events.drop_duplicates().reindex(pd.date_range(start2012,stop2014,freq='15Min'))
    return Events
    
## LBJ
LBJGrabSampleSSC=InterpolateGrabSamples(LBJ_StormIntervals, LBJgrab,60)      
LBJ['GrabInt-SSC-mg/L'] = LBJGrabSampleSSC['GrabInterpolated']
LBJ['GrabInt-SSC-mg/L-RMSE'] = 0
LBJ['GrabInt-SedFlux-mg/sec']=LBJ['Q'] * LBJ['GrabInt-SSC-mg/L']# Q(L/sec) * C (mg/L)
LBJ['GrabInt-SedFlux-tons/sec']=LBJ['GrabInt-SedFlux-mg/sec']*(10**-9) ## mg x 10**-6 = tons
LBJ['GrabInt-SedFlux-tons/15min']=LBJ['GrabInt-SedFlux-tons/sec']*900. ## 15min x 60sec/min = 900sec -> tons/sec * 900sec/15min = tons/15min
 
## QUARRY
# Grab only
QuarryGrabSampleSSC=InterpolateGrabSamples(QUARRY_StormIntervals, QUARRYgrab,60)   
# R2 only
R2GrabSampleSSC=InterpolateGrabSamples(QUARRY_StormIntervals, QUARRY_R2,60) 
# Combined Grab and R2
QUARRY_grab_and_R2 = SSC[SSC['Location'].isin(['DT','R2'])].resample('5Min',fill_method='pad',limit=0)
QUARRY_grab_and_R2_SSC = InterpolateGrabSamples(QUARRY_StormIntervals, QUARRY_grab_and_R2,60)   
QUARRY['GrabInt-SSC-mg/L'] = QUARRY_grab_and_R2_SSC['GrabInterpolated']
QUARRY['GrabInt-SSC-mg/L-RMSE'] = 0
QUARRY['GrabInt-SedFlux-mg/sec']=QUARRY['Q'] * QUARRY['GrabInt-SSC-mg/L']# Q(L/sec) * C (mg/L)
QUARRY['GrabInt-SedFlux-tons/sec']=QUARRY['GrabInt-SedFlux-mg/sec']*(10**-9) ## mg x 10**-6 = tons
QUARRY['GrabInt-SedFlux-tons/15min']=QUARRY['GrabInt-SedFlux-tons/sec']*900. ## 15min x 60sec/min = 900sec -> tons/sec * 900sec/15min = tons/15min  

## DAM
DAMGrabSampleSSC=InterpolateGrabSamples(DAM_StormIntervals, DAMgrab,60) 
DAM['GrabInt-SSC-mg/L'] = DAMGrabSampleSSC['GrabInterpolated']
DAM['GrabInt-SSC-mg/L-RMSE'] = 0
DAM['GrabInt-SedFlux-mg/sec']=DAM['Q'] * DAM['GrabInt-SSC-mg/L']# Q(L/sec) * C (mg/L)
DAM['GrabInt-SedFlux-tons/sec']=DAM['GrabInt-SedFlux-mg/sec']*(10**-9) ## mg x 10**-6 = tons
DAM['GrabInt-SedFlux-tons/15min']=DAM['GrabInt-SedFlux-tons/sec']*900. ## 15min x 60sec/min = 900sec -> tons/sec * 900sec/15min = tons/15min  

def plot_eventSSCinterpolated(GrabSamples,show=False):
    mpl.rc('lines',markersize=6,linewidth=2)
    fig, ax = plt.subplots(1,figsize=(8,6))
    ## PLOT THE INTERPOLATION (cont. SSC)    
    ## Plot continuous SSC    
    ax.plot_date(QUARRY_grab_and_R2_SSC.index,QUARRY_grab_and_R2_SSC['GrabInterpolated'],marker='.',ls='-',color='y',label='Interpolated SSC')
    ## PLOT GRAB SAMPLES
    ## Plot all grab samples from DT
    ax.plot_date(QUARRYgrab.index,QUARRYgrab['SSC (mg/L)'],marker='o',ls='None',color='k', label='QUARRY Grab Samples')
    ## Plot samples from Autosampler R2
    ax.plot_date(QUARRY_R2.index,QUARRY_R2['SSC (mg/L)'],marker='o',ls='None',color='grey', label='QUARRY AutoSampler')
    ## PLOT  ONES USED FOR INTERPOLATION
    ## Plot samples that are interpolated    
    ax.plot_date(QUARRY_grab_and_R2_SSC.index,QUARRY_grab_and_R2_SSC['Grab'],marker='.',ls='None',color='r',label='Samples for Interpolation')
    ax.legend(loc='best'), ax.set_ylabel('SSC (mg/L)')    
    ## Shade Storms    
    showstormintervals(ax,LBJ_storm_threshold,LBJ_StormIntervals)
    if show==True:
        plt.show()
    return
#plot_eventSSCinterpolated(QuarryGrabSampleSSC,show=True)
#plot_eventSSCinterpolated(R2GrabSampleSSC,show=True)

#### ..
#### Import Turbidity Data
#from load_from_MASTER_XL import TS3000,YSI,OBS,loadSSC
def TS3000(XL,sheet='DAM-TS3K'):
    print 'loading : '+sheet+'...'
    TS3K = XL.parse(sheet,header=0,parse_cols='A,F',index_col=0,parse_dates=True)
    TS3K.columns=['NTU']
    return TS3K
def YSI(XL,resample_interval,sheet='LBJ-YSI'):
    print 'loading : '+sheet+'...'
    YSI = XL.parse(sheet,header=4,parse_cols='A:H',parse_dates=[['Date','Time']],index_col=['Date_Time'])
    YSI=YSI.resample(resample_interval,closed='right')
    YSI['NTU raw']=YSI['NTU']
    return YSI
def OBS(XL,sheet='LBJ-OBS'):
    print 'loading : '+sheet+'...'
    OBS=XL.parse(sheet,header=4,parse_cols='A:L',parse_dates=True,index_col=0,na_values='NAN')
    return OBS
    
def correct_Turbidity(TurbidityCorrXL,location,Tdata):
    print 'Correcting turbidity for '+location
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
    TurbidityCorr = TurbidityCorrXL.parse(location,parse_dates=False)
    Correction=pd.DataFrame()
    for correction in TurbidityCorr.iterrows():
        t1_date = correction[1]['T1_date']
        t1_time = correction[1]['T1_time']
        t1 = my_parser(t1_date,t1_time)
        t2_date = correction[1]['T2_date']
        t2_time = correction[1]['T2_time']
        t2 = my_parser(t2_date,t2_time)
        ntu = correction[1]['NTU']    
        print t1,t2, ntu
        Correction = Correction.append(pd.DataFrame({'NTU':ntu},index=pd.date_range(t1,t2,freq='5Min')))
    Correction = Correction.reindex(pd.date_range(start2012,stop2014,freq='5Min'))
    Tdata['Manual_Correction'] = Correction['NTU']
    Tdata['NTU_corrected_Manual'] = Tdata['NTU raw']+Tdata['Manual_Correction']
    Tdata['NTU']=Tdata['NTU_corrected_Manual'].where(Tdata['NTU_corrected_Manual']>=0,Tdata['NTU raw'])#.round(0)
    return Tdata
TurbidityCorrXL = pd.ExcelFile(datadir+'T/TurbidityCorrection.xlsx')    
  
## Turbidimeter Data DAM
DAM_TS3K = TS3000(XL,'DAM-TS3K')
DAM_TS3K = DAM_TS3K[DAM_TS3K>=0]
DAM_YSI = YSI(XL,'5Min','DAM-YSI')
DAM_YSI = DAM_YSI.resample('15Min',closed='right').shift(1)
for column in ['Temp','NTU raw','NTU']:
    DAM_YSI[column] = DAM_YSI[column].round(0)
for column in ['SpCond','Battery']:
    DAM_YSI[column] = DAM_YSI[column].round(1)
for column in ['TDS','Sal']:
    DAM_YSI[column] = DAM_YSI[column].round(3)
## Correct negative NTU values
DAM_YSI = correct_Turbidity(TurbidityCorrXL,'DAM-YSI',DAM_YSI)

def plotYSI(df,SSCloc,end_time,show=True):
    fig, ntu = plt.subplots(1,1,figsize=(8,4),sharex=True,sharey=True)
    ## NTU
    df['NTU'].plot(ax=ntu,label='NTU',c='b')
    ntu.set_ylim(0,4000)
    ## legends
    for ax in fig.axes:
        ax.legend()
        showstormintervals(ax,LBJ_storm_threshold,LBJ_StormIntervals)
        SSCloc['SSC (mg/L)'].plot(ax=ax,ls='none',marker='.',color='r')
        ax.set_xlim(df.index[0],end_time)
    plt.tight_layout(pad=0.1)
    if show== True:
        plt.show()
    return
#plotYSI(DAM_YSI,SSC[SSC['Location']=='DAM'],end_time=stop2014,show=True)
#plotYSI(DAM_YSI,SSC[SSC['Location']=='DAM'],dt.datetime(2015,1,10),show=True)

## Turbidimeter Data QUARRY
QUARRYxl = pd.ExcelFile(datadir+'T/QUARRY-OBS.xlsx')
QUARRY_OBS = QUARRYxl.parse('QUARRY-OBS',header=4,parse_cols='A:L',parse_dates=True,index_col=0)
QUARRY_OBS = OBS(XL,'QUARRY-OBS')
QUARRY_OBS['NTU']=QUARRY_OBS['Turb_SS_Mean'].round(0)
QUARRY_OBS['NTU'] = QUARRY_OBS['NTU'][QUARRY_OBS['NTU']<=4000]

## Turbidimeter Data LBJ
## LBJ YSI
LBJ_YSIa = YSI(XL,'5Min','LBJ-YSIa')
LBJ_YSIa_15Min = LBJ_YSIa.resample('15Min',closed='right').shift(1)
LBJ_YSIb = YSI(XL,'15Min','LBJ-YSIb')
LBJ_YSI = pd.concat([LBJ_YSIa_15Min,LBJ_YSIb])[:dt.datetime(2012,5,23,6,0)]
for column in LBJ_YSI.columns:
    #print column
    LBJ_YSI[column] = LBJ_YSI[column].round(0)
#plotYSI(LBJ_YSI,SSC[SSC['Location']=='LBJ'],end_time=stop2012,show=True)

## LBJ OBS
# OBS with only Avg BS and SS at 15Min 
LBJ_OBSa = OBS(XL,'LBJ-OBSa')
LBJ_OBSa =pd.concat([LBJ_OBSa[dt.datetime(2013,3,11):dt.datetime(2013,4,1)],LBJ_OBSa[dt.datetime(2013,5,5):dt.datetime(2013,6,4)],LBJ_OBSa[dt.datetime(2013,6,7):]]) ## remove junk data
for column in LBJ_OBSa.columns:
    LBJ_OBSa[column] = LBJ_OBSa[column].round(0)
# OBS with BS and SS 100 times at 15Min
LBJ_OBSb = OBS(XL,'LBJ-OBSb')
LBJ_OBSb = pd.concat([LBJ_OBSb[:dt.datetime(2014,11,3,0)],LBJ_OBSb[dt.datetime(2014,11,5):]])
for column in LBJ_OBSb.columns: ##remove junk data
    #print column
    LBJ_OBSb[column] = LBJ_OBSb[column][LBJ_OBSb[column]<=4000]  
    LBJ_OBSb[column] = LBJ_OBSb[column].round(0)
    
## PLOT OBSa Time Series with SSC grab samples
def plotOBSa(df,SSCloc,show=True):
    fig, (bsavg,ssavg,comb) = plt.subplots(3,1,figsize=(8,4),sharex=True,sharey=True)
    ## BS
    df['Turb_BS_Avg'].plot(ax=bsavg,label='BS Avg',c='b')
    df['Turb_BS_Avg'].plot(ax=comb,label='BS Avg',c='b')
    ## SS
    df['Turb_SS_Avg'].plot(ax=ssavg,label='SS Avg',c='g')
    df['Turb_SS_Avg'].plot(ax=comb,label='SS Avg',c='g')
    ssavg.set_ylim(0,2000)
    ## legends
    for ax in fig.axes:
        ax.legend()
        showstormintervals(ax,LBJ_storm_threshold,LBJ_StormIntervals)
        SSCloc['SSC (mg/L)'].plot(ax=ax,ls='none',marker='.',color='r')
        ax.set_xlim(df.index[0],stop2013)
    plt.tight_layout(pad=0.1)
    if show== True:
        plt.show()
    return
#plotOBSa(LBJ_OBSa,SSC[SSC['Location']=='LBJ'],show=True)
    
## PLOT OBSb BS Time Series with SSC grab samples
def plotOBSb_BS(df,SSCloc,show=True):
    fig, (bsmedian,bsmean,bsstd,bsmax,bsmin,comb) = plt.subplots(6,1,sharex=True,sharey=True)
    bsmedian.set_ylim(0,4000)
    df['Turb_BS_Median'].plot(ax=bsmedian,label='BS Median')
    bsmedian.legend()
    df['Turb_BS_Mean'].plot(ax=bsmean,label='BS Mean')
    bsmean.legend()
    df['Turb_BS_STD'].plot(ax=bsstd,label='BS STD')
    bsstd.legend()
    df['Turb_BS_Max'].plot(ax=bsmax,label='BS Max')
    bsmax.legend()
    df['Turb_BS_Min'].plot(ax=bsmin,label='BS Min')
    bsmin.legend()
    ##combined plot
    df['Turb_BS_Median'].plot(ax=comb,label='BS Median',color='b')
    df['Turb_BS_Mean'].plot(ax=comb,label='BS Mean (NTU)',color='k')
    df['Turb_BS_Max'].plot(ax=comb,label='BS Max',color='grey')
    df['Turb_BS_Min'].plot(ax=comb,label='BS Min',color='g')
    ## legends
    for ax in fig.axes:
        showstormintervals(ax,LBJ_storm_threshold,LBJ_StormIntervals)
        SSCloc['SSC (mg/L)'].plot(ax=ax,ls='none',marker='.',color='r')
        ax.set_xlim(df.index[0],Mitigation)
        ax.locator_params(nbins=4,axis='y')
    plt.tight_layout(pad=0.1)
    if show== True:
        plt.show()
    return
#plotOBSb_BS(LBJ_OBSb,SSC[SSC['Location']=='LBJ'],show=True)

## PLOT OBSb SS Time Series with SSC grab samples  
def plotOBSb_SS(df,SSCloc,show=True):
    fig, (ssmedian,ssmean,ssstd,ssmax,ssmin,comb) = plt.subplots(6,1,sharex=True,sharey=True)
    
    ssmedian.set_ylim(0,4000)
    df['Turb_SS_Median'].plot(ax=ssmedian,label='SS Median')
    ssmedian.legend()
    df['Turb_SS_Mean'].plot(ax=ssmean,label='SS Mean')
    ssmean.legend()
    df['Turb_SS_STD'].plot(ax=ssstd,label='SS STD')
    ssstd.legend()
    df['Turb_SS_Max'].plot(ax=ssmax,label='SS Max')
    ssmax.legend()
    df['Turb_SS_Min'].plot(ax=ssmin,label='SS Min')
    ssmin.legend()
    ##combined plot
    df['Turb_SS_Median'].plot(ax=comb,label='SS Median',color='b')
    df['Turb_SS_Mean'].plot(ax=comb,label='SS Mean (NTU)',color='k')
    df['Turb_SS_Max'].plot(ax=comb,label='SS Max',color='grey')
    df['Turb_SS_Min'].plot(ax=comb,label='SS Min',color='g')
    ## legends
    for ax in fig.axes:
        showstormintervals(ax,LBJ_storm_threshold,LBJ_StormIntervals)
        SSCloc['SSC (mg/L)'].plot(ax=ax,ls='none',marker='.',color='r')
        ax.set_xlim(df.index[0],Mitigation)
        ax.locator_params(nbins=4,axis='y')
    plt.tight_layout(pad=0.1)
    if show== True:
        plt.show()
    return
#plotOBSb_SS(LBJ_OBSb,SSC[SSC['Location']=='LBJ'],show=True)
#plotOBSb_SS(QUARRY_OBS,SSC[SSC['Location']=='R2'],show=True)

## Despike turbidity data
## http://ocefpaf.github.io/python4oceanographers/blog/2013/05/20/spikes/

def plot_P_Q_T(lwidth=0.5, show=False):
    fig, (precip, Q, ntu) = plt.subplots(3,1,sharex=True,figsize=(6.5,6))
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
    ntu.plot_date(LBJ['NTU'].index,LBJ['NTU'],ls='-',marker='None',c='r',label='VILLAGE 15min NTU')
    ntu.plot_date(DAM['NTU'].index,DAM['NTU'],ls='-',marker='None',c='g',label='FOREST 15min NTU')
    ntu.yaxis.set_major_locator(my_locator)
    ##plot all Grab samples at location 
    ssc = fig.add_axes(ntu.get_position(), frameon=False, sharex=ntu)#,sharey=ntu)
    ssc.plot_date(LBJ['Grab-SSC-mg/L'].index,LBJ['Grab-SSC-mg/L'],'.',markeredgecolor='grey',color='r',label='VILLAGE SSC grab')
    ssc.plot_date(QUARRY['GrabDT-SSC-mg/L'].index,QUARRY['GrabDT-SSC-mg/L'],'.',markeredgecolor='grey',color='grey',label='QUARRY SSC grab (DT)')
    ssc.plot_date(QUARRY['GrabR2-SSC-mg/L'].index,QUARRY['GrabR2-SSC-mg/L'],'.',markeredgecolor='grey',color='y',label='QUARRY SSC (R2)')
    #ssc.plot_date(QUARRY['Grab-SSC-mg/L'].index,QUARRY['Grab-SSC-mg/L'],'.',markeredgecolor='grey',color='y',label='QUARRY SSC grab')
    ssc.plot_date(DAM['Grab-SSC-mg/L'].index,DAM['Grab-SSC-mg/L'],'.',markeredgecolor='grey',color='g',label='FOREST SSC grab')    
    ##
    ssc.yaxis.set_major_locator(my_locator)
    ssc.yaxis.set_ticks_position('right'),ssc.yaxis.set_label_position('right')
    ssc.set_ylabel('SSC (mg/L)'),ssc.legend(loc='upper right')
    ssc.set_ylim(0.15000)
    ## Shade storm intervals
    showstormintervals(precip,LBJ_storm_threshold, LBJ_StormIntervals)
    showstormintervals(Q, LBJ_storm_threshold, LBJ_StormIntervals,shade_color='r')
    showstormintervals(ntu,DAM_storm_threshold, DAM_StormIntervals,shade_color='g')

    precip.set_ylabel('Precip (mm/15min)'),precip.legend()
    Q.set_ylabel('Discharge (L/sec)'),Q.set_ylim(0,LBJ['Q'].max()+100),Q.legend()
    ntu.set_ylabel('Turbidity (NTU)'),ntu.set_ylim(0,LBJ['NTU'].max()),ntu.legend(loc='upper left')
    #ntu.xaxis.set_major_locator(matplotlib.dates.MonthLocator(range(1, 13), bymonthday=1, interval=6))
    #ntu.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%b '%y"))
    plt.tight_layout(pad=0.1)
    show_plot(show)
    return
#plot_P_Q_T(lwidth=0.5,show=True)

#### TURBIDITY
#### T to SSC rating curve for FIELD INSTRUMENTS
def NTU_SSCrating(SSCdata,TurbidimeterData,TurbidimeterName='T',location='LBJ',T_interval='15Min',Intercept=False,log=False):
    T_name = TurbidimeterName+'-NTU'
    SSCsamples = SSCdata[SSCdata['Location'].isin([location])].resample(T_interval,fill_method = 'pad',limit=0) ## pulls just the samples matching the location name and roll to 5Min.
    SSCsamples = SSCsamples[pd.notnull(SSCsamples['SSC (mg/L)'])] ## gets rid of ones that mg/L is null
    #print SSCsamples[40:]    
    SSCsamples[T_name]=TurbidimeterData## grabs turbidimeter NTU data 
    SSCsamples = SSCsamples[pd.notnull(SSCsamples[T_name])]
    #print SSCsamples[20:]
    T_SSCrating = pd.ols(y=SSCsamples['SSC (mg/L)'],x=SSCsamples[T_name],intercept=Intercept)
    
    mean_observed = SSCsamples['SSC (mg/L)'].mean()
    rmse_percent = T_SSCrating.rmse/mean_observed *100.
    return T_SSCrating,SSCsamples[[T_name,'SSC (mg/L)']],int(rmse_percent)    ## Rating, Turbidity and Grab Sample SSC data

## Read Synthetic Rating Curves (SRC) from putting sediment in bucket and sampling
SRC_File = pd.ExcelFile(datadir+'T/SyntheticRatingCurve/SyntheticRatingCurve.xlsx')
LBJ_SRC = SRC_File.parse('LBJ')[0:5]
QUARRY_SRC = SRC_File.parse('QUARRY')
DAM_SRC = SRC_File.parse('DAM')
N1_SRC = SRC_File.parse('N1')
N2_SRC = SRC_File.parse('N2')[0:5]

## PLOT T-SSC for  Synthetic Rating Curves
def Synthetic_Rating_Curves(param,show=False,save=False,filename=figdir+''):
    fig, ((lbj,quarry,dam),(n1,n2,comb)) = plt.subplots(2,3,figsize=(8,4),sharex=True,sharey=True,)
    max_y,max_x = 8000, 8000
    xy = np.linspace(0,max_y)
    ## LBJ    
    lbj.scatter(LBJ_SRC[param],LBJ_SRC['SSC(mg/L)'],c='r')
    lbj_SRC = pd.ols(y=LBJ_SRC['SSC(mg/L)'],x=LBJ_SRC[param],intercept=False)
    lbj.plot(xy,xy*lbj_SRC.beta[0],ls='-',label='LBJ_SRC'+r'$r^2$'+"%.2f"%lbj_SRC.r2,c='r')
    comb.plot(xy,xy*lbj_SRC.beta[0],ls='-',label='LBJ_SRC'+r'$r^2$'+"%.2f"%lbj_SRC.r2,c='r')
    lbj.set_ylabel('SSC (mg/L)'), lbj.set_title('LBJ '+r'$r^2=$'+"%.2f"%lbj_SRC.r2)
    ## QUARRY
    quarry.scatter(QUARRY_SRC[param],QUARRY_SRC['SSC(mg/L)'],c='g')
    quarry_SRC = pd.ols(y=QUARRY_SRC['SSC(mg/L)'],x=QUARRY_SRC[param],intercept=False)
    quarry.plot(xy,xy*quarry_SRC.beta[0],ls='-',label='QUARRY_SRC'+r'$r^2$'+"%.2f"%quarry_SRC.r2,c='g')
    comb.plot(xy,xy*quarry_SRC.beta[0],ls='-',label='QUARRY_SRC'+r'$r^2$'+"%.2f"%quarry_SRC.r2,c='g')
    quarry.set_ylabel('SSC (mg/L)'), quarry.set_title('QUARRY '+r'$r^2=$'+"%.2f"%quarry_SRC.r2)
    ## DAM
    dam.scatter(DAM_SRC[param],DAM_SRC['SSC(mg/L)'],c='b')
    dam_SRC = pd.ols(y=DAM_SRC['SSC(mg/L)'],x=DAM_SRC[param],intercept=False)
    dam.plot(xy,xy*dam_SRC.beta[0],ls='-',label='DAM_SRC'+r'$r^2$'+"%.2f"%dam_SRC.r2,c='b')
    comb.plot(xy,xy*dam_SRC.beta[0],ls='-',label='DAM_SRC'+r'$r^2$'+"%.2f"%dam_SRC.r2,c='b')
    dam.set_ylabel('SSC (mg/L)'), dam.set_title('DAM '+r'$r^2=$'+"%.2f"%dam_SRC.r2)
    ## N1
    n1.scatter(N1_SRC[param],N1_SRC['SSC(mg/L)'],c='y')
    n1_SRC = pd.ols(y=N1_SRC['SSC(mg/L)'],x=N1_SRC[param],intercept=False)
    n1.plot(xy,xy*n1_SRC.beta[0],ls='-',label='N1_SRC'+r'$r^2$'+"%.2f"%n1_SRC.r2,c='y')
    comb.plot(xy,xy*n1_SRC.beta[0],ls='-',label='N1_SRC'+r'$r^2$'+"%.2f"%n1_SRC.r2,c='y')
    n1.set_ylabel('SSC (mg/L)'), n1.set_title('N1 '+r'$r^2=$'+"%.2f"%n1_SRC.r2)
    ## N2
    n2.scatter(N2_SRC[param],N2_SRC['SSC(mg/L)'],c='k')
    n2_SRC = pd.ols(y=N2_SRC['SSC(mg/L)'],x=N2_SRC[param],intercept=False)
    n2.plot(xy,xy*n1_SRC.beta[0],ls='-',label='N2_SRC'+r'$r^2$'+"%.2f"%n2_SRC.r2,c='k')
    comb.plot(xy,xy*n1_SRC.beta[0],ls='-',label='N2_SRC'+r'$r^2$'+"%.2f"%n2_SRC.r2,c='k')
    n2.set_ylabel('SSC (mg/L)'), n2.set_title('N2 '+r'$r^2=$'+"%.2f"%n2_SRC.r2)
    ## COMBINED
    comb.scatter(LBJ_SRC[param],LBJ_SRC['SSC(mg/L)'],c='r')
    comb.scatter(QUARRY_SRC[param],QUARRY_SRC['SSC(mg/L)'],c='g')
    comb.scatter(DAM_SRC[param],DAM_SRC['SSC(mg/L)'],c='b')
    comb.scatter(N1_SRC[param],N1_SRC['SSC(mg/L)'],c='y')
    comb.scatter(N2_SRC[param],N2_SRC['SSC(mg/L)'],c='k')
    comb.set_title('All')
    for ax in fig.axes:
        ax.set_xlabel(param)
        ax.set_ylim(0,max_y)
        ax.set_xlim(0,max_x)
        ax.locator_params(nbins=4)
    plt.tight_layout(pad=0.1)
    show_plot(show)
    savefig(save,filename)
    return
#Synthetic_Rating_Curves(param='SS_Mean',show=True,save=False)#,filename=figdir+'Synthetic Rating Curves.png')
    
## PLOT T-SSC for  Synthetic Rating Curves
def Synthetic_Rating_Curves_Fagaalu(param,show=False,save=False,filename=figdir+''):
    fig, (lbj,dam)= plt.subplots(1,2,figsize=(6,3),sharex=True,sharey=True,)
    lbj.text(0.1,0.95,'(a)',verticalalignment='top', horizontalalignment='right',transform=lbj.transAxes,color='k',fontsize=10,fontweight='bold')
    dam.text(0.1,0.95,'(b)',verticalalignment='top', horizontalalignment='right',transform=dam.transAxes,color='k',fontsize=10,fontweight='bold')
    max_y,max_x = 4000, 4000
    xy = np.linspace(0,max_y)
    ## LBJ    
    lbj.scatter(LBJ_SRC[param],LBJ_SRC['SSC(mg/L)'],c='k')
    lbj_SRC = pd.ols(y=LBJ_SRC['SSC(mg/L)'],x=LBJ_SRC[param],intercept=False)
    lbj.plot(xy,xy*lbj_SRC.beta[0],ls='-',label='FG3_OBS '+r'$r^2$'+"%.2f"%lbj_SRC.r2,c='k')
    lbj.set_xlabel('SS_Mean'), lbj.set_title('FG3_OBS '+r'$r^2=$'+"%.2f"%lbj_SRC.r2)
    ## DAM
    dam.scatter(DAM_SRC[param],DAM_SRC['SSC(mg/L)'],c='grey')
    dam_SRC = pd.ols(y=DAM_SRC['SSC(mg/L)'],x=DAM_SRC[param],intercept=False)
    dam.plot(xy,xy*dam_SRC.beta[0],ls='-',label='FG1_YSI'+r'$r^2$'+"%.2f"%dam_SRC.r2,c='grey')
    dam.set_xlabel('NTU'), dam.set_title('FG1_YSI '+r'$r^2=$'+"%.2f"%dam_SRC.r2)#, dam.set_ylabel('SSC (mg/L)'), 
    ## COMBINED
    for ax in fig.axes:
        ax.set_ylabel('SSC (mg/L)')
        ax.set_ylim(0,max_y)
        ax.set_xlim(0,max_x)
        ax.locator_params(nbins=4)
    plt.tight_layout(pad=0.1)
    show_plot(show)
    savefig(save,filename)
    return
#Synthetic_Rating_Curves_Fagaalu(param='SS_Mean',show=True,save=False,filename=figdir+'')

## PLOT T-SSC rating curves for the YSI turbidimeter
def plotYSI_ratings(df,df_SRC,SSC_loc,Use_All_SSC=False,storm_samples_only=False):
    ## Subset SSC
    if Use_All_SSC==True:
        if storm_samples_only==True:
            SSC = SSC_dict['ALL-storm']
        elif storm_samples_only==False:
            SSC = SSC_dict['ALL']
    elif Use_All_SSC==False:
        if storm_samples_only==True:
            SSC = SSC_dict['Pre-storm']
        elif storm_samples_only==False:
            SSC = SSC_dict['Pre-ALL']        
    ### Plot
    fig, (ntu,ntu_zoom) = plt.subplots(1,2,figsize=(8,4))
    max_y, max_x = df['NTU'].max(),df['NTU'].max()
    xy = np.linspace(0,max_y)  
    ## NTU
    NTU=NTU_SSCrating(SSC,df['NTU'],location=SSC_loc,T_interval='5Min',Intercept=False,log=False)
    ntu.scatter(NTU[1]['T-NTU'],NTU[1]['SSC (mg/L)'])
    ntu.plot(xy,xy*NTU[0].beta[0],ls='-',label='NTU '+r'$r^2$'+"%.2f"%NTU[0].r2)
    ntu.set_title(SSC_loc+' NTU '+r'$r^2=$'+"%.2f"%NTU[0].r2)
    ## Zoom in
    ntu_zoom.scatter(NTU[1]['T-NTU'],NTU[1]['SSC (mg/L)'])
    ntu_zoom.plot(xy,xy*NTU[0].beta[0],ls='-',label='NTU '+r'$r^2$'+"%.2f"%NTU[0].r2)
    ntu_zoom.set_title(SSC_loc+' NTU '+r'$r^2=$'+"%.2f"%NTU[0].r2)
    try:
        df_SRC==None
    except:
        NTU_SRC = pd.ols(y=df_SRC['SSC(mg/L)'],x=df_SRC['SS_Mean'],intercept=False)
        ntu.scatter(df_SRC['SS_Mean'],df_SRC['SSC(mg/L)'],c='r')
        ntu.plot(xy,xy*NTU_SRC.beta[0],ls='-',label='NTU_SRC '+r'$r^2$'+"%.2f"%NTU_SRC.r2,c='r')  
        ntu_zoom.scatter(df_SRC['SS_Mean'],df_SRC['SSC(mg/L)'],c='r')
        ntu_zoom.plot(xy,xy*NTU_SRC.beta[0],ls='-',label='NTU_SRC '+r'$r^2$'+"%.2f"%NTU_SRC.r2,c='r')  
        
    ntu.set_xlabel('NTU')
    ntu.set_xlim(0,max_x), ntu.set_ylim(0,max_y)
    ntu_zoom.set_xlim(0,NTU[1]['T-NTU'].max()+50), ntu_zoom.set_ylim(0,NTU[1]['SSC (mg/L)'].max()+50)    
    ntu.legend()
    plt.tight_layout(pad=0.1)
    for ax in fig.axes:
        ax.locator_params(nbins=4)
    plt.show()
    return
## DAM YSI rating
#plotYSI_ratings(df=DAM_YSI,df_SRC=DAM_SRC,SSC_loc='DAM',Use_All_SSC=True,storm_samples_only=False) ## ALL SSC 
#plotYSI_ratings(df=DAM_YSI,df_SRC=DAM_SRC,SSC_loc='DAM',Use_All_SSC=True,storm_samples_only=True) ## ALL SSC, Storm Only
#plotYSI_ratings(df=DAM_YSI,df_SRC=DAM_SRC,SSC_loc='DAM',Use_All_SSC=False,storm_samples_only=False) ## Pre-mitigation only
#plotYSI_ratings(df=DAM_YSI,df_SRC=DAM_SRC,SSC_loc='DAM',Use_All_SSC=False,storm_samples_only=True) ## Pre-mitigation only, Storm only
## LBJ YSI rating
#plotYSI_ratings(LBJ_YSI,df_SRC=None,SSC_loc='LBJ',Use_All_SSC=False,storm_samples_only=False) ## Pre-mitigation only
#plotYSI_ratings(LBJ_YSI,df_SRC=None,SSC_loc='LBJ',Use_All_SSC=False,storm_samples_only=True) ## Pre-mitigation only, Storm only

## Plot T-SSC from YSI at DAM and LBJ to compare
def plotYSI_compare_ratings(DAM_YSI,DAM_SRC,LBJ_YSI,show_DAM_SRC=True,Use_All_SSC=False,storm_samples_only=True,show=True,save=False,filename=''):
    ## Subset SSC
    if Use_All_SSC==True:
        if storm_samples_only==True:
            SSC = SSC_dict['ALL-storm']
        elif storm_samples_only==False:
            SSC = SSC_dict['ALL']
    elif Use_All_SSC==False:
        if storm_samples_only==True:
            SSC = SSC_dict['Pre-storm']
        elif storm_samples_only==False:
            SSC = SSC_dict['Pre-ALL']   
    
    fig, ntu= plt.subplots(1,1,figsize=(4,4))
    max_y, max_x = LBJ_YSI['NTU'].max(),LBJ_YSI['NTU'].max()
    xy = np.linspace(0,max_y)  
    ## LBJ
    lbj=NTU_SSCrating(SSC,LBJ_YSI['NTU'],location='LBJ',T_interval='15Min',Intercept=False,log=False)
    ntu.plot(lbj[1]['T-NTU'],lbj[1]['SSC (mg/L)'],ls='none',marker='o',fillstyle='none',c='grey',label='FG3')
    ntu.plot(xy,xy*lbj[0].beta[0],ls='-',c='grey',label='FG3 YSI '+r'$r^2$'+"%.2f"%lbj[0].r2)
    labelindex_subplot(ntu,lbj[1].index,lbj[1]['T-NTU'],lbj[1]['SSC (mg/L)'])  
    ## DAM
    dam=NTU_SSCrating(SSC,DAM_YSI['NTU'],location='DAM',T_interval='15Min',Intercept=False,log=False)
    ntu.plot(dam[1]['T-NTU'],dam[1]['SSC (mg/L)'],ls='none',marker='s',c='k',label='FG1')
    ntu.plot(xy,xy*dam[0].beta[0],ls='-',c='k',label='FG1 YSI '+r'$r^2$'+"%.2f"%dam[0].r2)
    labelindex_subplot(ntu,dam[1].index,dam[1]['T-NTU'],dam[1]['SSC (mg/L)'])    
    ## DAM SRC
    if show_DAM_SRC==True:
        try:
            DAM_SRC==None
        except:
            dam_SRC = pd.ols(y=DAM_SRC['SSC(mg/L)'],x=DAM_SRC['SS_Mean'],intercept=False)
            ntu_fg1.plot(DAM_SRC['SS_Mean'],DAM_SRC['SSC(mg/L)'],ls='none',marker='^',fillstyle='none',c='grey',label='DAM_SRC')
            ntu_fg1.plot(xy,xy*dam_SRC.beta[0],ls='-',label='DAM_SRC '+r'$r^2$'+"%.2f"%dam_SRC.r2,c='grey')  
    ## Format subplots
    ntu.set_xlabel('NTU')
    ntu.set_xlim(0,1000)
    ntu.set_ylim(0,1000)
    ntu.legend()
    plt.tight_layout(pad=0.1)
    for ax in fig.axes:
        ax.locator_params(nbins=4)
    #letter_subplots(fig,x=0.1,y=0.95,vertical='top',horizontal='right',Color='k',font_size=10,font_weight='bold')
    show_plot(show)
    savefig(save,filename)
    return
#plotYSI_compare_ratings(DAM_YSI,DAM_SRC,LBJ_YSI,show_DAM_SRC=False,Use_All_SSC=False,storm_samples_only=False,show=True,save=False,filename='') ## Pre-mitigation
#plotYSI_compare_ratings(DAM_YSI,DAM_SRC,LBJ_YSI,show_DAM_SRC=True,Use_All_SSC=False,storm_samples_only=True,show=True,save=False,filename='') ## Pre-mitigation, storm only

## PLOT T-SSC rating for OBSa (BS and SS Avg only)
def OBSa_compare_ratings(df,df_SRC,SSC_loc,plot_SRC=True,Use_All_SSC=False,storm_samples_only=False,show=True,save=False,filename='',sub_plot_count=0):
    ## Subset SSC
    if Use_All_SSC==True:
        if storm_samples_only==True:
            SSC = SSC_dict['ALL-storm']
        elif storm_samples_only==False:
            SSC = SSC_dict['ALL']
    elif Use_All_SSC==False:
        if storm_samples_only==True:
            SSC = SSC_dict['Pre-storm']
        elif storm_samples_only==False:
            SSC = SSC_dict['Pre-ALL']   
        
    fig, (ss_avg) = plt.subplots(1,1,figsize=(4,4))#,sharex=True,sharey=True)
    max_y, max_x = 1000, 1000
    xy = np.linspace(0,max_y)

    ## SS Avg
    ss_average=NTU_SSCrating(SSC,df['Turb_SS_Avg'],location=SSC_loc,T_interval='5Min',Intercept=False,log=False)
    ss_avg.scatter(ss_average[1]['T-NTU'],ss_average[1]['SSC (mg/L)'],c='k')
    ss_avg.plot(xy,xy*ss_average[0].beta[0],ls='-',c='k',label='SS_Avg '+r'$r^2$'+"%.2f"%ss_average[0].r2)   
    #ss_avg.set_title(SSC_loc+' SS_Avg '+r'$r^2=$'+"%.2f"%ss_average[0].r2) 
    ss_avg.set_xlabel('SS Avg')
    ## SS Mean SRC
    #ss_mean_SRC = pd.ols(y=df_SRC['SSC(mg/L)'],x=df_SRC['SS_Mean'],intercept=False)
    #ss_avg.scatter(df_SRC['SS_Mean'],df_SRC['SSC(mg/L)'],c='grey')
    #ss_avg.plot(xy,xy*ss_mean_SRC.beta[0],ls='--',c='grey',label='SS_Mean_SRC'+r'$r^2$'+"%.2f"%ss_mean_SRC.r2)
    ss_avg.legend()
    plt.tight_layout(pad=0.1)
    for ax in fig.axes:
        ax.locator_params(nbins=4)
        ax.set_xlim(0,max_x), ax.set_ylim(0,max_y)
        
    #letter_subplots(fig,x=0.1,y=0.95,vertical='top',horizontal='right',Color='k',font_size=10,font_weight='bold')
    show_plot(show)
    savefig(save,filename)
    return
#OBSa_compare_ratings(df=LBJ_OBSa,df_SRC=LBJ_SRC,SSC_loc='LBJ',plot_SRC=True,Use_All_SSC=False,storm_samples_only=False,show=True,save=False,filename='')  
#OBSa_compare_ratings(df=LBJ_OBSa,df_SRC=LBJ_SRC,SSC_loc='LBJ',Use_All_SSC=False,storm_samples_only=True,show=True,save=False,filename='')  
    
## PLOT T-SSC ratings with all parameters (BS and SS Mean, Median, Min, Max)
def OBSb_compare_ratings(df,df_SRC,SSC_loc,plot_SRC=False,Use_All_SSC=False,storm_samples_only=True,show=True,save=False,filename='',sub_plot_count=0):
    ## Subset SSC
    if Use_All_SSC==True:
        if storm_samples_only==True:
            SSC = SSC_dict['ALL-storm']
        elif storm_samples_only==False:
            SSC = SSC_dict['ALL']
    elif Use_All_SSC==False:
        if storm_samples_only==True:
            SSC = SSC_dict['Pre-storm']
        elif storm_samples_only==False:
            SSC = SSC_dict['Pre-ALL']  
    fig, ((bs_med,bs_mea,bs_min,bs_max),(ss_med,ss_mea,ss_min,ss_max)) = plt.subplots(2,4,figsize=(12,6))#,sharex=True,sharey=True)
            
    max_y, max_x = 1000, 1000
    xy = np.linspace(0,max_y)
    ## BS Median
    bs_median=NTU_SSCrating(SSC,df['Turb_BS_Median'],location=SSC_loc,T_interval='15Min',Intercept=False,log=False)
    bs_med.scatter(bs_median[1]['T-NTU'],bs_median[1]['SSC (mg/L)'],c='k')
    bs_med.plot(xy,xy*bs_median[0].beta[0],ls='-',c='k',label='BS_Median'+r'$r^2$'+"%.2f"%bs_median[0].r2)
    #bs_med.set_title('BS_Median '+r'$r^2=$'+"%.2f"%bs_median[0].r2)
    bs_med.set_ylabel('SSC (mg/L)'),bs_med.set_xlabel('BS Median') 
    ## BS Mean
    bs_mean=NTU_SSCrating(SSC,df['Turb_BS_Mean'],location=SSC_loc,T_interval='15Min',Intercept=False,log=False)
    bs_mea.scatter(bs_mean[1]['T-NTU'],bs_mean[1]['SSC (mg/L)'],c='k')
    bs_mea.plot(xy,xy*bs_mean[0].beta[0],ls='-',c='k',label='BS_Mean'+r'$r^2$'+"%.2f"%bs_mean[0].r2)
    #bs_mea.set_title('BS_Mean '+r'$r^2=$'+"%.2f"%bs_mean[0].r2)  
    bs_mea.set_xlabel('BS Mean')
    ## BS Min
    bs_minimum=NTU_SSCrating(SSC,df['Turb_BS_Min'],location=SSC_loc,T_interval='15Min',Intercept=False,log=False)
    bs_min.scatter(bs_minimum[1]['T-NTU'],bs_minimum[1]['SSC (mg/L)'],c='k')
    bs_min.plot(xy,xy*bs_minimum[0].beta[0],ls='-',c='k',label='BS_Min'+r'$r^2$'+"%.2f"%bs_minimum[0].r2)
    #bs_min.set_title('BS_Min '+r'$r^2=$'+"%.2f"%bs_minimum[0].r2)
    bs_min.set_xlabel('BS Min')
    ## BS Max
    bs_maximum=NTU_SSCrating(SSC,df['Turb_BS_Max'],location=SSC_loc,T_interval='15Min',Intercept=False,log=False)
    bs_max.scatter(bs_maximum[1]['T-NTU'],bs_maximum[1]['SSC (mg/L)'],c='k')
    bs_max.plot(xy,xy*bs_maximum[0].beta[0],ls='-',c='k',label='BS_Max'+r'$r^2$'+"%.2f"%bs_maximum[0].r2)    
    #bs_max.set_title('BS_Max '+r'$r^2=$'+"%.2f"%bs_maximum[0].r2)    
    bs_max.set_xlabel('BS Max')
    ## SS Median
    ss_median=NTU_SSCrating(SSC,df['Turb_SS_Median'],location=SSC_loc,T_interval='15Min',Intercept=False,log=False)
    ss_med.scatter(ss_median[1]['T-NTU'],ss_median[1]['SSC (mg/L)'],c='k')
    ss_med.plot(xy,xy*ss_median[0].beta[0],ls='-',c='k',label='SS_Median'+r'$r^2$'+"%.2f"%ss_median[0].r2)
    #ss_med.set_title('SS_Median '+r'$r^2=$'+"%.2f"%ss_median[0].r2)
    ss_med.set_ylabel('SSC (mg/L)'),ss_med.set_xlabel('SS Median')
    ## SS Mean
    ss_mean=NTU_SSCrating(SSC,df['Turb_SS_Mean'],location=SSC_loc,T_interval='15Min',Intercept=False,log=False)
    ss_mea.scatter(ss_mean[1]['T-NTU'],ss_mean[1]['SSC (mg/L)'],c='k')
    ss_mea.plot(xy,xy*ss_mean[0].beta[0],ls='-',c='k',label='SS_Mean'+r'$r^2$'+"%.2f"%ss_mean[0].r2)
    #ss_mea.set_title('SS_Mean '+r'$r^2=$'+"%.2f"%ss_mean[0].r2)    
    ss_mea.set_xlabel('SS Mean')
    ## SS Min
    ss_minimum=NTU_SSCrating(SSC,df['Turb_SS_Min'],location=SSC_loc,T_interval='15Min',Intercept=False,log=False)
    ss_min.scatter(ss_minimum[1]['T-NTU'],ss_minimum[1]['SSC (mg/L)'],c='k')
    ss_min.plot(xy,xy*ss_minimum[0].beta[0],ls='-',c='k',label='SS_Min'+r'$r^2$'+"%.2f"%ss_minimum[0].r2)
    #ss_min.set_title('SS_Min '+r'$r^2=$'+"%.2f"%ss_minimum[0].r2)    
    ss_min.set_xlabel('SS Min')
    ## SS Max
    ss_maximum=NTU_SSCrating(SSC,df['Turb_SS_Max'],location=SSC_loc,T_interval='15Min',Intercept=False,log=False)
    ss_max.scatter(ss_maximum[1]['T-NTU'],ss_maximum[1]['SSC (mg/L)'],c='k')
    ss_max.plot(xy,xy*ss_maximum[0].beta[0],ls='-',c='k',label='SS_Max'+r'$r^2$'+"%.2f"%ss_maximum[0].r2)    
    #ss_max.set_title('SS_Max '+r'$r^2=$'+"%.2f"%ss_maximum[0].r2)
    ss_max.set_xlabel('SS Max')
    if plot_SRC==True:
        ## BS Median SRC
        bs_median_SRC = pd.ols(y=df_SRC['SSC(mg/L)'],x=df_SRC['BS_Median'],intercept=False)
        bs_med.scatter(df_SRC['BS_Median'],df_SRC['SSC(mg/L)'],c='grey')
        bs_med.plot(xy,xy*bs_median_SRC.beta[0],ls='--',c='grey',label='BS_Median_SRC'+r'$r^2$'+"%.2f"%bs_median_SRC.r2)
        ## BS Mean SRC
        bs_mean_SRC = pd.ols(y=df_SRC['SSC(mg/L)'],x=df_SRC['BS_Mean'],intercept=False)
        bs_mea.scatter(df_SRC['BS_Mean'],df_SRC['SSC(mg/L)'],c='grey')
        bs_mea.plot(xy,xy*bs_mean_SRC.beta[0],ls='--',c='grey',label='BS_Mean_SRC'+r'$r^2$'+"%.2f"%bs_mean_SRC.r2)
        ## BS Min SRC
        bs_min_SRC = pd.ols(y=df_SRC['SSC(mg/L)'],x=df_SRC['BS_Min'],intercept=False)
        bs_min.scatter(df_SRC['BS_Min'],df_SRC['SSC(mg/L)'],c='grey')
        bs_min.plot(xy,xy*bs_min_SRC.beta[0],ls='--',c='grey',label='BS_Min_SRC'+r'$r^2$'+"%.2f"%bs_min_SRC.r2)
        ## BS Max SRC
        bs_max_SRC = pd.ols(y=df_SRC['SSC(mg/L)'],x=df_SRC['BS_Max'],intercept=False)
        bs_max.scatter(df_SRC['BS_Max'],df_SRC['SSC(mg/L)'],c='grey')
        bs_max.plot(xy,xy*bs_max_SRC.beta[0],ls='--',c='grey',label='BS_Max_SRC'+r'$r^2$'+"%.2f"%bs_max_SRC.r2)
        ## SS Median SRC
        ss_median_SRC = pd.ols(y=df_SRC['SSC(mg/L)'],x=df_SRC['SS_Median'],intercept=False)
        ss_med.scatter(df_SRC['SS_Median'],df_SRC['SSC(mg/L)'],c='grey')
        ss_med.plot(xy,xy*ss_median_SRC.beta[0],ls='--',c='grey',label='SS_Median_SRC'+r'$r^2$'+"%.2f"%ss_median_SRC.r2)
        ## SS Mean SRC
        ss_mean_SRC = pd.ols(y=df_SRC['SSC(mg/L)'],x=df_SRC['SS_Mean'],intercept=False)
        ss_mea.scatter(df_SRC['SS_Mean'],df_SRC['SSC(mg/L)'],c='grey')
        ss_mea.plot(xy,xy*ss_mean_SRC.beta[0],ls='--',c='grey',label='SS_Mean_SRC'+r'$r^2$'+"%.2f"%ss_mean_SRC.r2)
        ## SS Min SRC
        ss_min_SRC = pd.ols(y=df_SRC['SSC(mg/L)'],x=df_SRC['SS_Min'],intercept=False)
        ss_min.scatter(df_SRC['SS_Min'],df_SRC['SSC(mg/L)'],c='grey')
        ss_min.plot(xy,xy*ss_min_SRC.beta[0],ls='--',c='grey',label='SS_Min_SRC'+r'$r^2$'+"%.2f"%ss_min_SRC.r2) 

    #fig.canvas.manager.set_window_title(SSC_loc)
    for ax in fig.axes:
        ax.locator_params(nbins=4,axis='y'), ax.locator_params(nbins=3,axis='x')
        ax.set_xlim(0,max_x), ax.set_ylim(0,max_y)
        ax.legend()
    letter_subplots(fig,x=0.1,y=0.95,vertical='top',horizontal='right',Color='k',font_size=10,font_weight='bold')
    plt.tight_layout(pad=0.1)
    show_plot(show)
    savefig(save,filename)
    return
## LBJ
#OBSb_compare_ratings(df=LBJ_OBSb,df_SRC=LBJ_SRC,SSC_loc='LBJ',plot_SRC=False,Use_All_SSC=True,storm_samples_only=False,show=True,save=False,filename='')  ## ALL SSC
#OBSb_compare_ratings(df=LBJ_OBSb,df_SRC=LBJ_SRC,SSC_loc='LBJ',Use_All_SSC=True,storm_samples_only=True,show=True,save=False,filename='')   ## ALL SSC, storm only
#OBSb_compare_ratings(df=LBJ_OBSb,df_SRC=LBJ_SRC,SSC_loc='LBJ',Use_All_SSC=False,storm_samples_only=False,show=True,save=False,filename='') ## Pre-mitigation
#OBSb_compare_ratings(df=LBJ_OBSb,df_SRC=LBJ_SRC,SSC_loc='LBJ',Use_All_SSC=False,storm_samples_only=True,show=True,save=False,filename='')## Pre-mitigation, storm only
## LBJ R2
#OBSb_compare_ratings(df=LBJ_OBSb,df_SRC=LBJ_SRC,SSC_loc='LBJ R2',Use_All_SSC=True,storm_samples_only=False)  
## QUARRY
#OBSb_compare_ratings(df=QUARRY_OBS,df_SRC=QUARRY_SRC,SSC_loc='R2',Use_All_SSC=True)   
    
def plot_all_T_SSC(Use_All_SSC=False,storm_samples_only=False,show=True,save=False,filename='',sub_plot_count=0):
    ## Subset SSC
    if Use_All_SSC==True:
        if storm_samples_only==True:
            SSC = SSC_dict['ALL-storm']
        elif storm_samples_only==False:
            SSC = SSC_dict['ALL']
    elif Use_All_SSC==False:
        if storm_samples_only==True:
            SSC = SSC_dict['Pre-storm']
        elif storm_samples_only==False:
            SSC = SSC_dict['Pre-ALL']  
    fig, (ysi,obsa,obsb) = plt.subplots(1,3,figsize=(8,3))#,sharex=True,sharey=True)
            
    max_y, max_x = 1100, 1100
    xy = np.linspace(0,max_y)
    
    ## LBJ and DAM YSI
    ## LBJ
    lbj=NTU_SSCrating(SSC,LBJ_YSI['NTU'],location='LBJ',T_interval='15Min',Intercept=False,log=False)
    ysi.plot(lbj[1]['T-NTU'],lbj[1]['SSC (mg/L)'],ls='none',marker='o',fillstyle='none',markersize=4,c='grey',label='FG3')
    ysi.plot(xy,xy*lbj[0].beta[0],ls='-',c='grey',label='FG3 '+r'$r^2$'+"%.2f"%lbj[0].r2)
    ## DAM
    dam=NTU_SSCrating(SSC,DAM_YSI['NTU'],location='DAM',T_interval='15Min',Intercept=False,log=False)
    ysi.plot(dam[1]['T-NTU'],dam[1]['SSC (mg/L)'],ls='none',marker='s',markersize=4,c='k',label='FG1')
    ysi.plot(xy,xy*dam[0].beta[0],ls='-',c='k',label='FG1 '+r'$r^2$'+"%.2f"%dam[0].r2)
    ysi.set_xlabel('NTU')
    ysi.set_ylabel('SSC (mg/L)')
    ysi.legend(ncol=2,fontsize=8,columnspacing=0.1)
    ## LBJ OBSa
    ## SS Avg
    ss_average=NTU_SSCrating(SSC,LBJ_OBSa['Turb_SS_Avg'],location='LBJ',T_interval='5Min',Intercept=False,log=False)
    obsa.scatter(ss_average[1]['T-NTU'],ss_average[1]['SSC (mg/L)'],c='k')
    obsa.plot(xy,xy*ss_average[0].beta[0],ls='-',c='k',label='SS_Avg '+r'$r^2$'+"%.2f"%ss_average[0].r2)   
    obsa.set_xlabel('SS Avg')
    obsa.yaxis.set_visible(False)
    obsa.legend(fontsize=8)
    ## LBJ OBSb
    ## SS Mean
    ss_mean=NTU_SSCrating(SSC,LBJ_OBSb['Turb_SS_Mean'],location='LBJ',T_interval='15Min',Intercept=False,log=False)
    obsb.scatter(ss_mean[1]['T-NTU'],ss_mean[1]['SSC (mg/L)'],c='k')
    obsb.plot(xy,xy*ss_mean[0].beta[0],ls='-',c='k',label='SS_Mean '+r'$r^2$'+"%.2f"%ss_mean[0].r2) 
    obsb.set_xlabel('SS Mean')
    obsb.yaxis.set_visible(False)
    obsb.legend(fontsize=8)
    for ax in fig.axes:
        ax.locator_params(nbins=4,axis='y'), ax.locator_params(nbins=3,axis='x')
        ax.set_xlim(0,max_x), ax.set_ylim(0,max_y)
        
    letter_subplots(fig,x=0.1,y=0.95,vertical='top',horizontal='right',Color='k',font_size=10,font_weight='bold')
    plt.tight_layout(pad=0.1)
    show_plot(show)
    savefig(save,filename)
    return
#plot_all_T_SSC(Use_All_SSC=False,storm_samples_only=True,show=True,save=False,filename='',sub_plot_count=0)

### Choose OBS parameters
LBJ_OBSa['NTU']=LBJ_OBSa['Turb_SS_Avg']
LBJ_OBSb['NTU']=LBJ_OBSb['Turb_SS_Mean'] ## choose which OBS parameter == NTU

LBJ_OBS=LBJ_OBSa.append(LBJ_OBSb) ## append NTU's
LBJ_OBS['NTU'] = LBJ_OBS['NTU'].interpolate(limit=2)

#### NTU to SSC rating curve from LAB ANALYSIS
#T_SSC_Lab= pd.ols(y=SSC[SSC['Location']=='LBJ']['SSC (mg/L)'],x=SSC[SSC['Location']=='LBJ']['NTU'])
T_SSC_Lab= pd.ols(y=SSC['SSC (mg/L)'],x=SSC['NTU'],intercept=False)

### NTU ratings
def calc_RMSE(T_SSC): ## uses the NTU_SSCrating object
    print 'Manually calculating RMSE'
    T_SSC_RMSE = pd.DataFrame({'NTUmeasured':T_SSC[1]['T-NTU'],'SSCmeasured':T_SSC[1]['SSC (mg/L)']})
    T_SSC_RMSE['SSC_predicted']= T_SSC_RMSE['NTUmeasured']*T_SSC[0].beta[0] ## USe the rating slope to calculate SSC from the NTU value
    T_SSC_RMSE['SSC_diff'] = T_SSC_RMSE['SSCmeasured']-T_SSC_RMSE['SSC_predicted'] ## Subtract the predicted from the actual (residuals)
    T_SSC_RMSE['SSC_diffsquared'] = (T_SSC_RMSE['SSC_diff'])**2. ## Square the difference (residuals)
    T_SSC_RMSE_Value = (T_SSC_RMSE['SSC_diffsquared'].sum()/len(T_SSC_RMSE))**0.5 ## Take square root of average of residuals 
    return T_SSC_RMSE_Value.round(0)

## DAM TS3K
T_SSC_DAM_TS3K=NTU_SSCrating(SSC_dict['Pre-storm'],DAM_TS3K['NTU'],location='DAM',T_interval='15Min',log=False) ## Use 5minute data for NTU/SSC relationship
DAM_TS3K_rating = T_SSC_DAM_TS3K[0]
DAM_TS3K_rating_rmse = T_SSC_DAM_TS3K[2]
DAM_TS3K['T-SSC-RMSE'] = DAM_TS3K_rating_rmse 
#print DAM_TS3K_rating.rmse
#print calc_RMSE(T_SSC_DAM_TS3K)

## DAM YSI
T_SSC_DAM_YSI=NTU_SSCrating(SSC_dict['Pre-storm'],DAM_YSI['NTU'],location='DAM',T_interval='15Min',log=False) ## Won't work until there are some overlapping grab samples
DAM_YSI_rating= T_SSC_DAM_YSI[0]
DAM_YSI_rating_rmse= T_SSC_DAM_YSI[2]
DAM_YSI['T-SSC-RMSE']= DAM_YSI_rating_rmse
#print DAM_YSI_rating.rmse
#print calc_RMSE(T_SSC_DAM_YSI)

## QUARRY
T_SSC_QUARRY_OBS=NTU_SSCrating(SSC_dict['ALL'],QUARRY_OBS['NTU'],location='R2',T_interval='15Min',log=False)
QUARRY_OBS_rating = T_SSC_QUARRY_OBS[0]
QUARRY_OBS_rating_rmse = T_SSC_QUARRY_OBS[2]
QUARRY_OBS['T-SSC-RMSE'] = QUARRY_OBS_rating_rmse
#print QUARRY_OBS_rating.rmse
#print calc_RMSE(T_SSC_QUARRY_OBS)

## LBJ YSI
T_SSC_LBJ_YSI=NTU_SSCrating(SSC_dict['Pre-storm'],LBJ_YSI['NTU'],location='LBJ',T_interval='15Min',log=False)
LBJ_YSI_rating = T_SSC_LBJ_YSI[0]
LBJ_YSI_rating_rmse = T_SSC_LBJ_YSI[2]
LBJ_YSI['T-SSC-RMSE'] = LBJ_YSI_rating_rmse 
#print LBJ_YSI_rating.rmse
#print calc_RMSE(T_SSC_LBJ_YSI)

## LBJ OBS 2013
T_SSC_LBJ_OBSa =NTU_SSCrating(SSC_dict['Pre-storm'][start2013:dt.datetime(2013,4,1)],LBJ_OBSa['NTU'],location='LBJ',T_interval='5Min',log=False)
LBJ_OBSa_rating = T_SSC_LBJ_OBSa[0]
LBJ_OBSa_rating_rmse = T_SSC_LBJ_OBSa[2]
LBJ_OBSa['T-SSC-RMSE'] = LBJ_OBSa_rating_rmse 
#print LBJ_OBSa_rating.rmse
#print calc_RMSE(T_SSC_LBJ_OBSa)

## LBJ OBS 2014
T_SSC_LBJ_OBSb=NTU_SSCrating(SSC_dict['Pre-storm'],LBJ_OBSb['NTU'],location='LBJ',T_interval='15Min',log=False)
LBJ_OBSb_rating = T_SSC_LBJ_OBSb[0]
LBJ_OBSb_rating_rmse = T_SSC_LBJ_OBSb[2]
LBJ_OBSb['T-SSC-RMSE']= LBJ_OBSb_rating_rmse 
#print LBJ_OBSb_rating.rmse
#print calc_RMSE(T_SSC_LBJ_OBSb)

## LBJ OBS ALL
T_SSC_LBJ_OBS=NTU_SSCrating(SSC_dict['Pre-storm'],LBJ_OBS['NTU'],location='LBJ',T_interval='15Min',log=False)
LBJ_OBS_rating = T_SSC_LBJ_OBS[0]
LBJ_OBS_rating_rmse = T_SSC_LBJ_OBS[2]
LBJ_OBS['T-SSC-RMSE'] = LBJ_OBS_rating_rmse 
#print LBJ_OBS_rating.rmse
#print calc_RMSE(T_SSC_LBJ_OBS)


## Plot ALL T-SSC
## LAB
def T_SSC_ALL(show=False):
    ## Plot Grab Samples, NTU measured in LAB
    fig = plt.figure()
    plt.scatter(SSC[SSC['Location'].isin(['LBJ','DT','R2','DAM'])==True]['NTU'],
                    SSC[SSC['Location'].isin(['LBJ','DT','R2','DAM'])==True]['SSC (mg/L)'],color='b',label='Measured in LAB')
    ## LBJ, NTU measured by YSI and OBSa, OBSb
    ALL_T_LBJ = pd.DataFrame(pd.concat([T_SSC_LBJ_YSI[1]['T-NTU'],T_SSC_LBJ_OBSa[1]['T-NTU'],
                       T_SSC_LBJ_OBSb[1]['T-NTU'],]),columns=['T-NTU'])     
    ALL_T_LBJ =ALL_T_LBJ.join(pd.concat([T_SSC_LBJ_YSI[1]['SSC (mg/L)'],T_SSC_LBJ_OBSa[1]['SSC (mg/L)'],
                             T_SSC_LBJ_OBSb[1]['SSC (mg/L)']]))                    
    plt.scatter(ALL_T_LBJ['T-NTU'],ALL_T_LBJ['SSC (mg/L)'],c='r',label='LBJ')
    ## QUARRY, NTU measured by OBSb
    plt.scatter(T_SSC_QUARRY_OBS[1]['T-NTU'],T_SSC_QUARRY_OBS[1]['SSC (mg/L)'],c='y',label='QUARRY')
    ## DAM, NTU measured by TS3K and YSI
    ALL_T_DAM = pd.DataFrame(pd.concat([T_SSC_DAM_TS3K[1]['T-NTU'],T_SSC_DAM_YSI[1]['T-NTU']]),columns=['T-NTU'])
    ALL_T_DAM = ALL_T_DAM.join(pd.concat([T_SSC_DAM_TS3K[1]['SSC (mg/L)'],T_SSC_DAM_YSI[1]['SSC (mg/L)']]))
    plt.scatter(ALL_T_DAM['T-NTU'],ALL_T_DAM['SSC (mg/L)'],c='g',label='DAM')
    ## Format plot
    plt.plot([0,3000],[0,3000],c='k')   
    plt.xlabel('Lab Measured Turbidity (NTU)'), plt.ylabel('SSC mg/L')
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
    
    ## NTU
    ## LBJ OBS
    LBJ_OBS_2013 = linearfunction(T_SSC_LBJ_OBSa[1]['LBJ-OBS-NTU'],T_SSC_LBJ_OBSa[1]['SSC (mg/L)'])
    lbj_obs_2013 = ['%.2f'%LBJ_OBS_2013['a'],'%.2f'%LBJ_OBS_2013['b'],'%.2f'%LBJ_OBS_2013['r2'],'%.2f'%LBJ_OBS_2013['pearson'],'%.2f'%LBJ_OBS_2013['spearman'],'%.2f'%LBJ_OBS_2013['rmse']]    

    LBJ_OBS_2014 = linearfunction(T_SSC_LBJ_OBSb[1]['LBJ-OBS-NTU'],T_SSC_LBJ_OBSb[1]['SSC (mg/L)'])
    lbj_obs_2014 = ['%.2f'%LBJ_OBS_2014['a'],'%.2f'%LBJ_OBS_2014['b'],'%.2f'%LBJ_OBS_2014['r2'],'%.2f'%LBJ_OBS_2014['pearson'],'%.2f'%LBJ_OBS_2014['spearman'],'%.2f'%LBJ_OBS_2014['rmse']]    

    ## QUARRY OBS
    QUARRY_OBS = linearfunction(T_SSC_QUARRY_OBS[1]['QUARRY-OBS-NTU'],T_SSC_QUARRY_OBS[1]['SSC (mg/L)'])
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
    #fig, (lab,ysi,obs) = plt.subplots(1,3,sharex=True,sharey=True,) 
    fig =plt.figure(figsize=(8,6))
    if plot_param_table==False:
        ysi = plt.subplot2grid((1,2),(0,0))
        obs = plt.subplot2grid((1,2),(0,1))
    if plot_param_table==True:
        ysi = plt.subplot2grid((2,2),(0,0))
        obs = plt.subplot2grid((2,2),(0,1))
        param_table = plt.subplot2grid((2,3),(1,0),colspan=2)
    xy = np.linspace(0,2000)
    mpl.rc('lines',markersize=ms,linewidth=lwidth)
    dotsize=50
    ## Grab Samples: LBJ-YSI, DAM-TS3k, DAM-YSI
    ysi.scatter(T_SSC_LBJ_YSI[1]['T-NTU'],T_SSC_LBJ_YSI[1]['SSC (mg/L)'],s=dotsize,color='r',marker='o',label='VILLAGE-YSI',edgecolors='grey')
    ysi.scatter(T_SSC_DAM_TS3K[1]['T-NTU'],T_SSC_DAM_TS3K[1]['SSC (mg/L)'],s=dotsize,color='g',marker='o',label='FOREST-TS3K',edgecolors='grey')
    ysi.scatter(T_SSC_DAM_YSI[1]['T-NTU'],T_SSC_DAM_YSI[1]['SSC (mg/L)'],s=dotsize,color='g',marker='v',label='FOREST-YSI',edgecolors='grey')
    ## NTU ratings LBJ-YSI, DAM-YSI, DAM-TS3K  
    ysi.plot(xy,xy*LBJ_YSI_rating.beta[0],ls='-',c='r',label='VILLAGE-YSI rating')
    #ysi.plot(xy,xy*DAM_TS3Krating.beta[0]+DAM_TS3Krating.beta[1],ls='-',c='g',label='FOREST-TS3K rating')
    ysi.plot(xy,xy*DAM_YSI_rating.beta[0],ls='--',c='g',label='FOREST-YSI rating')
    ## Format OBS
    ysi.grid(True), ysi.set_xlim(-5,4000), ysi.set_ylim(0,4000), ysi.set_ylabel('SSC (mg/L)'),ysi.set_xlabel('Turbidity (NTU)'),ysi.legend(fancybox=True,ncol=1,loc='best')
    ## NTU LBJ-OBS, QUARRY-OBS
    obs.scatter(T_SSC_LBJ_OBSa[1]['T-NTU'],T_SSC_LBJ_OBSa[1]['SSC (mg/L)'],s=dotsize,color='y',marker='.',label='VILLAGE-OBS-2013',edgecolors='grey')
    obs.plot(xy,xy*LBJ_OBSa_rating.beta[0],ls='-',c='y',label='VILLAGE-OBS-2013 rating')
    
    obs.scatter(T_SSC_LBJ_OBSb[1]['T-NTU'],T_SSC_LBJ_OBSb[1]['SSC (mg/L)'],s=dotsize,color='r',marker='.',label='VILLAGE-OBS-2014',edgecolors='grey')
    obs.plot(xy,xy*LBJ_OBSb_rating.beta[0],ls='-',c='r',label='VILLAGE-OBS-2014 rating')

    obs.scatter(T_SSC_QUARRY_OBS[1]['T-NTU'],T_SSC_QUARRY_OBS[1]['SSC (mg/L)'],s=dotsize,color='grey',marker='.',label='QUARRY-OBS',edgecolors='grey')
    obs.plot(xy,xy*QUARRY_OBS_rating.beta[0],ls='-',c='grey',label='QUARRY-OBS rating')

    ## Format NTU
    obs.grid(True), obs.set_xlabel('Turbidity (NTU)'), obs.legend(fancybox=True,ncol=2)
    obs.set_xlim(-5,4000), obs.set_ylim(0,4000),
    #labelindex_subplot(ts3k,T_SSC_LBJ_OBS[1].index,T_SSC_LBJ_OBS[1]['LBJ-OBS-NTU'],T_SSC_LBJ_OBS[1]['SSC (mg/L)'])    
    #labelindex_subplot(ts3k,T_SSC_LBJ_YSI[1].index,T_SSC_LBJ_YSI[1]['LBJ-YSI-NTU'],T_SSC_LBJ_OBS[1]['SSC (mg/L)'])
    title = 'Turbidity to Suspended Sediment Concetration Rating Curves'
    #plt.suptitle(title,fontsize=16) 
    ## TABLE
    if plot_param_table == True:
        ## NTU
        LAB = linearfunction(SSC[SSC['Location']=='LBJ']['NTU'],SSC[SSC['Location']=='LBJ']['SSC (mg/L)'])
        LBJ_YSI=linearfunction(T_SSC_LBJ_YSI[1]['T-NTU'],T_SSC_LBJ_YSI[1]['SSC (mg/L)'])
        DAM_TS3K = linearfunction(T_SSC_DAM_TS3K[1]['T-NTU'],T_SSC_DAM_TS3K[1]['SSC (mg/L)'])
        DAM_YSI = linearfunction(T_SSC_DAM_YSI[1]['T-NTU'],T_SSC_DAM_YSI[1]['SSC (mg/L)'])
        ## NTU
        LBJ_OBS_2013 = linearfunction(T_SSC_LBJ_OBSa[1]['T-NTU'],T_SSC_LBJ_OBSa[1]['SSC (mg/L)'])
        LBJ_OBS_2014 = linearfunction(T_SSC_LBJ_OBSb[1]['T-NTU'],T_SSC_LBJ_OBSb[1]['SSC (mg/L)'])
        QUA_OBS = linearfunction(T_SSC_QUARRY_OBS[1]['T-NTU'],T_SSC_QUARRY_OBS[1]['SSC (mg/L)'])        
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
        #plt.subplots_adjust(left=0.08, bottom=0,hspace=0.01)
    else:
        plt.tight_layout(pad=0.1)
        pass
    show_plot(show)
    return
#plotNTUratings(plot_param_table=True,show=True,log=False,save=False,lwidth=0.5,ms=20)

def plotNTUratings_no_int(plot_param_table=True,show=False,log=False,save=False,lwidth=0.3,ms=10):
    #fig, (lab,ysi,obs) = plt.subplots(1,3,sharex=True,sharey=True,) 
    fig =plt.figure(figsize=(14,6))
    lab = plt.subplot2grid((2,3),(0,0))
    ysi = plt.subplot2grid((2,3),(0,1))
    obs = plt.subplot2grid((2,3),(0,2))
    param_table = plt.subplot2grid((2,3),(1,0),colspan=3)
    
    xy = np.linspace(0,2000)
    mpl.rc('lines',markersize=ms,linewidth=lwidth)
    dotsize=50
    
    ## All Samples LAB
    lab.scatter(SSC['NTU'],SSC['SSC (mg/L)'],s=dotsize,color='b',marker='v',label='LAB',edgecolors='grey')
    lab.plot(xy,xy*T_SSC_Lab.beta[0],ls='-',c='b',label='LAB')
    lab.grid(True),lab.set_ylabel('SSC (mg/L)'),lab.set_xlabel('Turbidity (NTU)'),lab.legend(fancybox=True,ncol=2)
    lab.set_xlim(-5,4000), lab.set_ylim(0,4000)
    ## Grab Samples: LBJ-YSI, DAM-TS3k, DAM-YSI
    ysi.scatter(T_SSC_LBJ_YSI[1]['LBJ-YSI-NTU'],T_SSC_LBJ_YSI[1]['SSC (mg/L)'],s=dotsize,color='r',marker='o',label='VILLAGE-YSI',edgecolors='grey')
    ysi.scatter(T_SSC_DAM_TS3K[1]['DAM-TS3K-NTU'],T_SSC_DAM_TS3K[1]['SSC (mg/L)'],s=dotsize,color='g',marker='o',label='FOREST-TS3K',edgecolors='grey')
    ysi.scatter(T_SSC_DAM_YSI[1]['DAM-YSI-NTU'],T_SSC_DAM_YSI[1]['SSC (mg/L)'],s=dotsize,color='g',marker='v',label='FOREST-YSI',edgecolors='grey')
    ## NTU ratings LBJ-YSI, DAM-YSI, DAM-TS3K  
    ysi.plot(xy,xy*LBJ_YSI_rating.beta[0],ls='-',c='r',label='VILLAGE-YSI rating')
    #ysi.plot(xy,xy*DAM_TS3Krating.beta[0]+DAM_TS3Krating.beta[1],ls='-',c='g',label='FOREST-TS3K rating')
    ysi.plot(xy,xy*DAM_YSI_rating.beta[0],ls='--',c='g',label='FOREST-YSI rating')
    ## Format OBS
    ysi.grid(True), ysi.set_xlim(-5,4000), ysi.set_ylim(0,4000), ysi.set_ylabel('SSC (mg/L)'),ysi.set_xlabel('Turbidity (NTU)'),ysi.legend(fancybox=True,ncol=1,loc='best')
    ## NTU LBJ-OBS, QUARRY-OBS
    obs.scatter(T_SSC_LBJ_OBSa[1]['LBJ-OBS-NTU'],T_SSC_LBJ_OBSa[1]['SSC (mg/L)'],s=dotsize,color='y',marker='.',label='VILLAGE-OBS-2013',edgecolors='grey')
    obs.plot(xy,xy*LBJ_OBSa_rating.beta[0],ls='-',c='y',label='VILLAGE-OBS-2013 rating')
    
    obs.scatter(T_SSC_LBJ_OBSb[1]['LBJ-OBS-NTU'],T_SSC_LBJ_OBSb[1]['SSC (mg/L)'],s=dotsize,color='r',marker='.',label='VILLAGE-OBS-2014',edgecolors='grey')
    obs.plot(xy,xy*LBJ_OBSb_rating.beta[0],ls='-',c='r',label='VILLAGE-OBS-2014 rating')

    obs.scatter(T_SSC_QUARRY_OBS[1]['QUARRY-OBS-NTU'],T_SSC_QUARRY_OBS[1]['SSC (mg/L)'],s=dotsize,color='grey',marker='.',label='QUARRY-OBS',edgecolors='grey')
    obs.plot(xy,xy*QUARRY_OBS_rating.beta[0],ls='-',c='grey',label='QUARRY-OBS rating')

    ## Format NTU
    obs.grid(True), obs.set_xlabel('Turbidity (NTU)'), obs.legend(fancybox=True,ncol=2)
    obs.set_xlim(-5,4000), obs.set_ylim(0,4000),
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
        ## NTU
        LBJ_OBS_2013 = linearfunction(T_SSC_LBJ_OBSa[1]['LBJ-OBS-NTU'],T_SSC_LBJ_OBSa[1]['SSC (mg/L)'])
        LBJ_OBS_2014 = linearfunction(T_SSC_LBJ_OBSb[1]['LBJ-OBS-NTU'],T_SSC_LBJ_OBSb[1]['SSC (mg/L)'])
        QUA_OBS = linearfunction(T_SSC_QUARRY_OBS[1]['QUARRY-OBS-NTU'],T_SSC_QUARRY_OBS[1]['SSC (mg/L)'])        
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
#plotNTUratings_no_int(plot_param_table=True,show=True,log=False,save=True,lwidth=0.5,ms=20)    

#### ..
#### TURBIDITY TO SSC to SEDFLUX
### LBJ Turbidity

#LBJ_OBS_15Min = pd.concat([LBJ_OBSa_15Min['NTU'],LBJ_OBSb['NTU']])
#LBJntu15minute = pd.concat([LBJ_YSI['NTU'],LBJ_OBSa_15Min['NTU'],LBJ_OBSb['NTU']])

# YSI
LBJ['YSI-NTU']=LBJ_YSI['NTU']
LBJ['YSI-SSC']=LBJ_YSI_rating.beta[0] * LBJ['YSI-NTU']
LBJ['YSI-SSC-RMSE'] = LBJ_YSI['T-SSC-RMSE']
# OBSa
## resample to 15min to match Q records
LBJ_OBSa_15Min = LBJ_OBSa.resample('15Min',closed='right').shift(1)
LBJ['OBSa-NTU']=LBJ_OBSa_15Min['NTU']
LBJ['OBSa-SSC']=LBJ_OBSa_rating.beta[0] * LBJ['OBSa-NTU']
LBJ['OBSa-SSC-RMSE'] = LBJ_OBSa_15Min['T-SSC-RMSE']
# OBSb
LBJ['OBSb-NTU']=LBJ_OBSb['NTU']
LBJ['OBSb-SSC']=LBJ_OBSb_rating.beta[0] * LBJ['OBSb-NTU']
LBJ['OBSb-SSC-RMSE'] = LBJ_OBSb['T-SSC-RMSE']
# OBS combined
LBJ['OBS-NTU'] = pd.concat([LBJ_OBSa_15Min['NTU'],LBJ_OBSb['NTU']])
LBJ['OBS-SSC'] = pd.concat([LBJ['OBSa-SSC'].dropna(),LBJ['OBSb-SSC'].dropna()])## has dups since both are on a 2012-2015 index
LBJ['OBS-SSC-RMSE']=pd.concat([LBJ['OBSa-SSC-RMSE'].dropna(),LBJ['OBSb-SSC-RMSE'].dropna()])
# All NTU combined
LBJ['NTU'] = pd.concat([LBJ['YSI-NTU'].dropna(),LBJ['OBS-NTU'].dropna()])
LBJ['NTU-SSC'] = pd.concat([LBJ['YSI-SSC'].dropna(),LBJ['OBS-SSC'].dropna()])
LBJ['NTU-SSC-RMSE'] = pd.concat([LBJ['YSI-SSC-RMSE'].dropna(),LBJ['OBS-SSC-RMSE'].dropna()])
### LBJ SedFlux
LBJ['T-SSC-mg/L'] = LBJ['NTU-SSC']
LBJ['T-SSC-mg/L-RMSE'] = LBJ['NTU-SSC-RMSE']
LBJ['T-SedFlux-mg/sec']=LBJ['Q'] * LBJ['T-SSC-mg/L']# Q(L/sec) * C (mg/L) = mg/sec
LBJ['T-SedFlux-tons/sec']=LBJ['T-SedFlux-mg/sec']*(10**-9) ## mg x 10**-9 = tons
LBJ['T-SedFlux-tons/15min']=LBJ['T-SedFlux-tons/sec']*900. ## 15min x 60sec/min = 900sec -> tons/sec * 900sec/15min = tons/15min
## Combine with Interpolated SSC from Grab samples
LBJ['SSC-mg/L'] = LBJ['T-SSC-mg/L'].where(LBJ['T-SSC-mg/L']>=0,LBJ['GrabInt-SSC-mg/L'])
LBJ['SSC-mg/L-RMSE'] = LBJ['T-SSC-mg/L-RMSE'].where(LBJ['T-SSC-mg/L-RMSE']>=0,LBJ['GrabInt-SSC-mg/L-RMSE'])
LBJ['SedFlux-tons/sec']=LBJ['T-SedFlux-tons/sec'].where(LBJ['T-SedFlux-tons/sec']>=0,LBJ['GrabInt-SedFlux-tons/sec'])
LBJ['SedFlux-kg/sec']=LBJ['SedFlux-tons/sec']*10**3 ## tons x 10**3 = kg
LBJ['SedFlux-tons/15min']=LBJ['T-SedFlux-tons/15min'].where(LBJ['T-SedFlux-tons/15min']>=0,LBJ['GrabInt-SedFlux-tons/15min'])


### QUARRY Turbidity
QUARRY['NTU'] = QUARRY_OBS['NTU']
QUARRY['NTU-SSC'] = QUARRY_OBS_rating.beta[0] * QUARRY['NTU']
QUARRY['NTU-SSC-RMSE'] = QUARRY_OBS['T-SSC-RMSE']
### QUARRY SedFlux
QUARRY['T-SSC-mg/L'] = QUARRY['NTU-SSC']
QUARRY['T-SSC-mg/L-RMSE'] = QUARRY['NTU-SSC-RMSE']
QUARRY['T-SedFlux-mg/sec']=QUARRY['Q'] * QUARRY['T-SSC-mg/L']# Q(L/sec) * C (mg/L) = mg/sec
QUARRY['T-SedFlux-tons/sec']=QUARRY['T-SedFlux-mg/sec']*(10**-9) ## mg x 10**-9 = tons
QUARRY['T-SedFlux-tons/15min']=QUARRY['T-SedFlux-tons/sec']*900. ## 15min x 60sec/min = 900sec -> tons/sec * 900sec/15min = tons/15min
## Combine with Interpolated SSC from Grab samples
QUARRY['SSC-mg/L'] = QUARRY['T-SSC-mg/L'].where(QUARRY['T-SSC-mg/L']>=0,QUARRY['GrabInt-SSC-mg/L'])
QUARRY['SSC-mg/L-RMSE'] = QUARRY['T-SSC-mg/L-RMSE'].where(QUARRY['T-SSC-mg/L-RMSE']>=0,QUARRY['GrabInt-SSC-mg/L-RMSE'])
QUARRY['SedFlux-tons/sec']=QUARRY['T-SedFlux-tons/sec'].where(QUARRY['T-SedFlux-tons/sec']>=0,QUARRY['GrabInt-SedFlux-tons/sec'])
QUARRY['SedFlux-kg/sec']=QUARRY['SedFlux-tons/sec']*10**3 ## tons x 10**3 = kg
QUARRY['SedFlux-tons/15min']=QUARRY['T-SedFlux-tons/15min'].where(QUARRY['T-SedFlux-tons/15min']>=0,QUARRY['GrabInt-SedFlux-tons/15min'])

### DAM Turbidity

#DAMntu15minute =  pd.DataFrame(pd.concat([DAM_TS3K_15Min['NTU'],DAM_YSI['NTU']])).reindex(pd.date_range(start2012,stop2014,freq='15Min'))

#TS3000
## resample to 15min to match Q records
DAM_TS3K_15Min = DAM_TS3K.resample('15Min',closed='right').shift(1) ## Resample to 15 minutes for the SedFlux calc
DAM['TS3K-NTU']=DAM_TS3K_15Min['NTU']
DAM['TS3K-SSC']=DAM_YSI_rating.beta[0] * DAM['TS3K-NTU'] ## USES YSI rating for TS3000
DAM['TS3K-SSC-RMSE']=DAM_TS3K['T-SSC-RMSE']/2
#YSI
DAM['YSI-NTU']=DAM_YSI['NTU']
DAM['YSI-SSC']=DAM_YSI_rating.beta[0] * DAM['YSI-NTU']
DAM['YSI-SSC-RMSE']= DAM_YSI['T-SSC-RMSE']
## Both TS3K and YSI data resampled to 15minutes
DAM['NTU']=pd.concat([DAM['TS3K-NTU'].dropna(),DAM['YSI-NTU'].dropna()])
DAM['NTU-SSC'] = pd.concat([DAM['TS3K-SSC'].dropna(),DAM['YSI-SSC'].dropna()])
DAM['NTU-SSC-RMSE'] = pd.concat([DAM['TS3K-SSC-RMSE'].dropna(),DAM['YSI-SSC-RMSE'].dropna()])
## DAM SedFlux
DAM['T-SSC-mg/L']=DAM['NTU-SSC']
DAM['T-SSC-mg/L-RMSE'] = DAM['NTU-SSC-RMSE']
DAM['T-SedFlux-mg/sec']=DAM['Q'] * DAM['T-SSC-mg/L']# Q(L/sec) * C (mg/L)
DAM['T-SedFlux-tons/sec']=DAM['T-SedFlux-mg/sec']*(10**-9) ## mg x 10**-9 = tons
DAM['T-SedFlux-tons/15min']=DAM['T-SedFlux-tons/sec']*900. ## 15min x 60sec/min = 900sec -> tons/sec * 900sec/15min = tons/15min
## Combine with Interpolated SSC from Grab samples
DAM['SSC-mg/L'] = DAM['T-SSC-mg/L'].where(DAM['T-SSC-mg/L']>=0,DAM['GrabInt-SSC-mg/L'])
DAM['SSC-mg/L-RMSE'] = DAM['T-SSC-mg/L-RMSE'].where(DAM['T-SSC-mg/L-RMSE']>=0,DAM['GrabInt-SSC-mg/L-RMSE'])
DAM['SedFlux-tons/sec']=DAM['T-SedFlux-tons/sec'].where(DAM['T-SedFlux-tons/sec']>=0,DAM['GrabInt-SedFlux-tons/sec'])
DAM['SedFlux-kg/sec']=DAM['SedFlux-tons/sec']*10**3 ## tons x 10**3 = kg
DAM['SedFlux-tons/15min']=DAM['T-SedFlux-tons/15min'].where(DAM['T-SedFlux-tons/15min']>=0,DAM['GrabInt-SedFlux-tons/15min'])


#### ..
#### EVENT-WISE ANALYSES

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

def PQvol_years_BOTH(StormsLBJ,StormsDAM,show=False):
    fig, (site_lbj,site_dam)=plt.subplots(1,2,sharey=True,sharex=True)
    dotsize=20
    RCmax, RCmean, RCmin = StormsLBJ['RunoffCoeff'].describe()[[7,1,3]]
    site_lbj.annotate('Runoff Coeff-Max:'+'%.2f'%RCmax+' Mean:'+'%.2f'%RCmean+' Min:'+'%.2f'%RCmin, xy=(0.05, 0.95), xycoords='axes fraction')
    stormsLBJ=StormsLBJ[['PsumVol','Qsum']]/1000
    stormsLBJ['Pmax']=StormsLBJ[['Pmax']]
    site_lbj.scatter(stormsLBJ['PsumVol'][start2012:stop2012],stormsLBJ['Qsum'][start2012:stop2012],color='g',marker='o',s=scaleSeries(stormsLBJ['Pmax'][start2012:stop2012].dropna().values),label='2012')
    site_lbj.scatter(stormsLBJ['PsumVol'][start2013:stop2013],stormsLBJ['Qsum'][start2013:stop2013],color='y',marker='o',s=scaleSeries(stormsLBJ['Pmax'][start2013:stop2013].dropna().values),label='2013')
    site_lbj.scatter(stormsLBJ['PsumVol'][start2014:stop2014],stormsLBJ['Qsum'][start2014:stop2014],color='r',marker='o',s=scaleSeries(stormsLBJ['Pmax'][start2014:stop2014].dropna().values),label='2014')

    site_lbj.set_title('LBJ')
    site_lbj.set_ylabel('Event Discharge (m3)'),site_lbj.set_xlabel('Precipitation (m3) - DotSize=15minMaxPrecip(mm)')
    #site_lbj.set_ylim(0,stormsLBJ['Qsum'].max()+50000000), site_lbj.set_xlim(0,250)
    site_lbj.legend(loc=4)
    site_lbj.grid(True)

    RCmax, RCmean, RCmin = StormsDAM['RunoffCoeff'].describe()[[7,1,3]]
    site_dam.annotate('Runoff Coeff-Max:'+'%.2f'%RCmax+' Mean:'+'%.2f'%RCmean+' Min:'+'%.2f'%RCmin, xy=(0.05, 0.95), xycoords='axes fraction')

    stormsDAM=StormsDAM[['PsumVol','Qsum']]/1000
    stormsDAM['Pmax']=StormsDAM[['Pmax']]
    site_dam.scatter(stormsDAM['PsumVol'][start2012:stop2012],stormsDAM['Qsum'][start2012:stop2012],color='g',marker='o',s=scaleSeries(stormsDAM['Pmax'].dropna()[start2012:stop2012].values),label='2012')
    site_dam.scatter(stormsDAM['PsumVol'][start2013:stop2013],stormsDAM['Qsum'][start2013:stop2013],color='y',marker='o',s=scaleSeries(stormsDAM['Pmax'].dropna()[start2013:stop2013].values),label='2013')
    site_dam.scatter(stormsDAM['PsumVol'][start2014:stop2014],stormsDAM['Qsum'][start2014:stop2014],color='r',marker='o',s=scaleSeries(stormsDAM['Pmax'].dropna()[start2014:stop2014].values),label='2014')
    
    site_dam.set_title('DAM')
    site_dam.set_ylabel('Event Discharge (m3)'),site_dam.set_xlabel('Precipitation (m3) - DotSize=15minMaxPrecip(mm)')
    #site_dam.set_ylim(0,stormsLBJ['Qsum'].max()+50000000), site_dam.set_xlim(0,250)
    site_dam.legend(loc=4)
    site_dam.grid(True)
    
    ### Label on click
    labelindex_subplot(site_lbj,stormsLBJ.index,stormsLBJ['PsumVol'],stormsLBJ['Qsum'])
    labelindex_subplot(site_dam,stormsDAM.index,stormsDAM['PsumVol'],stormsDAM['Qsum'])
    
    title="Event Rainfall vs. Event Discharge Fagaalu Stream"
    fig.suptitle(title,fontsize=16)
    fig.canvas.manager.set_window_title('Figure: '+title)

    log=False
    if log==True:
        site_lbj.set_yscale('log'), site_lbj.set_xscale('log')
        site_dam.set_yscale('log'), site_dam.set_xscale('log')
    plt.draw()
    if show==True:
        plt.show()
    return
#PQvol_years_BOTH(StormsLBJ,StormsDAM,True)

def Q_storm_diff_table():
    Q_Diff = pd.DataFrame({'UPPER m3':StormsDAM['Qsum']/1000,'TOTAL m3':StormsLBJ['Qsum']/1000,'Precip (mm)':StormsLBJ['Psum']}).dropna()
    ## Calculate Q from just Lower watershed
    Q_Diff['UPPER m3']=Q_Diff['UPPER m3'].apply(np.int) #m3
    Q_Diff['TOTAL m3']=Q_Diff['TOTAL m3'].apply(np.int) #m3
    Q_Diff['LOWER m3']=Q_Diff['TOTAL m3'] - Q_Diff['UPPER m3']
    ## Calculate percentages
    Q_Diff['% Upper'] = Q_Diff['UPPER m3']/Q_Diff['TOTAL m3']*100
    Q_Diff['% Upper'] = Q_Diff['% Upper'].apply(np.int)
    Q_Diff['% Lower'] = Q_Diff['LOWER m3']/Q_Diff['TOTAL m3']*100
    Q_Diff['% Lower'] = Q_Diff['% Lower'].apply(np.int)
    Q_Diff['Precip (mm)'] = Q_Diff['Precip (mm)'].apply(np.int)
    Q_Diff['Storm#']=range(1,len(Q_Diff)+1)
    Q_Diff['Storm Start'] = Q_Diff.index
    Q_Diff['Storm Start'] = Q_Diff['Storm Start'].apply(lambda x: "{:%m/%d/%Y}".format(x))
    ## summary stats
    Percent_Upper = Q_Diff['UPPER m3'].sum()/Q_Diff['TOTAL m3'].sum()*100
    Percent_Lower =Q_Diff['LOWER m3'].sum()/Q_Diff['TOTAL m3'].sum()*100
    ## add summary stats to bottom of table
    Q_Diff=Q_Diff.append(pd.DataFrame({'Storm Start':'-','Storm#':'-','Precip (mm)':'-','UPPER m3':'-','LOWER m3':'-','TOTAL m3':'Average:','% Upper':"%.0f"%Percent_Upper,'% Lower':"%.0f"%Percent_Lower},index=['']))
    Q_Diff=Q_Diff[['Storm Start','Storm#','Precip (mm)','UPPER m3','LOWER m3','TOTAL m3','% Upper','% Lower']]
    return Q_Diff
Q_storm_diff_table()

## Calculate the percent of total Q with raw vales, BEFORE NORMALIZING by area!
def plotQ_storm_table(show=False):
    diff = pd.DataFrame({'Qupper':StormsDAM['Qsum']/1000,
    'Qtotal':StormsLBJ['Qsum']/1000,'Psum':StormsLBJ['Psum']}).dropna()
    ## Calculate Q from just Lower watershed
    diff['Qupper']=diff['Qupper'].apply(np.int) #m3
    diff['Qtotal']=diff['Qtotal'].apply(np.int) # m3
    diff['Qlower']=diff['Qtotal'] - diff['Qupper']
    ## Calculate percentages
    diff['% Upper'] = diff['Qupper']/diff['Qtotal']*100
    diff['% Upper'] = diff['% Upper'].round(0)
    diff['% Lower'] = diff['Qlower']/diff['Qtotal']*100
    diff['% Lower'] = diff['% Lower'].round(0)
    diff['Psum'] = diff['Psum'].apply(np.int)
    diff['Storm#']=range(1,len(diff)+1)
    ## add summary stats to bottom of table
    diff=diff.append(pd.DataFrame({'Storm#':'-','Psum':'-','Qupper':'-','Qlower':'-','Qtotal':'Average:','% Upper':'%.1f'%diff['% Upper'].mean(),'% Lower':'%.1f'%diff['% Lower'].mean()},index=['']))
    ## Build table
    nrows, ncols = len(diff),len(diff.columns)
    hcell, wcell=0.2,1
    hpad, wpad = .8,.5
    fig = plt.figure(figsize=(ncols*wcell+wpad,nrows*hcell+hpad)) 
    ax = fig.add_subplot(111)
    ax.patch.set_visible(False), ax.axis('off')
    ax.xaxis.set_visible(False), ax.yaxis.set_visible(False)
    celldata = np.array(diff[['Storm#','Psum','Qupper','Qlower','Qtotal','% Upper','% Lower']].values)
    ax.table(cellText=celldata,rowLabels=[pd.to_datetime(t) for t in diff.index.values],colLabels=['Storm#','Precip(mm)','Upper(m3)','Lower(m3)','Total(m3)','%Upper','%Lower'],loc='center')
    plt.suptitle("Discharge (Q) from Upstream (DAM) and Downstream (LBJ) watersheds in Faga'alu")
    plt.draw()
    if show==True:
        plt.show()
    return
#plotQ_storm_table(True)

### ALL SSY Data
def SSY_Data(storm_threshold,storm_intervals,title,show=False):
    #storm_data = storm_data[dt.datetime(2014,2,14,14,30):dt.datetime(2014,2,14,19,30)]
    fig, (P,Q,T,SSC,SED) = plt.subplots(nrows=5,ncols=1,sharex=True) 
    P.tick_params(\
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off') # labels along the bottom edge are off
    ## Precip
    PrecipFilled['Precip'].plot(ax=P,color='b',ls='steps-pre',label='RG1')
    max_yticks =4
    yloc = MaxNLocator(max_yticks)
    P.yaxis.set_major_locator(yloc) 
    P.set_ylabel('P\nmm/15min'), P.grid(False)
    P.set_ylim(0,28)
    ## Discharge
    LBJ['Q'].plot(ax=Q,color='r',label='VILLAGE')
    #storm_data['QUARRY-Q''].plot(ax=Q,color='y',label='QUARRY-Q')
    DAM['Q'].plot(ax=Q,color='g',label='FOREST')
    Q.legend()
    Q.set_ylabel('Q\nL/s'),#, Q.set_yscale('log')
    Q.spines['bottom'].set_visible(False),Q.grid(False)
    Q.tick_params(axis='x',which='both',bottom='off',top='off',labelbottom='off') # labels along the bottom edge are off
    max_yticks = 4
    yloc = plt.MaxNLocator(max_yticks)    
    Q.yaxis.set_major_locator(yloc)    
    ## SSC grab samples
    LBJ['Grab-SSC-mg/L'].plot(ax=SSC,color='r',marker='o',ls='None',markersize=6,label='VILLAGE')
    QUARRY['Grab-SSC-mg/L'].plot(ax=SSC,color='y',marker='o',ls='None',markersize=6,label='QUARRY')
    DAM['Grab-SSC-mg/L'].plot(ax=SSC,color='g',marker='o',ls='None',markersize=6,label='FOREST')
    ## Turbidity
    LBJ['NTU'].plot(ax=T,color='r',label='VILLAGE')
    QUARRY['NTU'].plot(ax=T,color='r',alpha=0.8,label='QUARRY')
    DAM['NTU'].plot(ax=T,color='g',label='FOREST')
    T.set_ylabel('T NTU'),T.set_ylim(-1)
    max_yticks = 4
    yloc = plt.MaxNLocator(max_yticks)
    T.yaxis.set_major_locator(yloc) 
    T.grid(False), T.spines['bottom'].set_visible(False)
    T.tick_params(axis='x',which='both',bottom='off',top='off',labelbottom='off') # labels along the bottom edge are off
    ## SSC from turbidity
    LBJ['T-SSC-mg/L'].plot(ax=SSC,color='r',label='VILLAGE')
    QUARRY['T-SSC-mg/L'].plot(ax=SSC,ls='--',color='y',label='QUARRY')
    DAM['T-SSC-mg/L'].plot(ax=SSC,color='g')
    ### SSC interpolated from grab samples
    LBJ['GrabInt-SSC-mg/L'].plot(ax=SSC,ls='--',color='r',label='VILLAGE')
    QUARRY['GrabInt-SSC-mg/L'].plot(ax=SSC,ls='--',color='y',label='QUARRY-SSC-grab')
    DAM['GrabInt-SSC-mg/L'].plot(ax=SSC,ls='--',color='g',label='FOREST')
    SSC.set_ylabel('SSC\nmg/L')#, SSC.set_ylim(0,1400)
    max_yticks = 4
    yloc = plt.MaxNLocator(max_yticks)
    SSC.yaxis.set_major_locator(yloc) 
    SSC.grid(False),SSC.spines['bottom'].set_visible(False)
    SSC.tick_params(axis='x',which='both',bottom='off',top='off',labelbottom='off') # labels along the bottom edge are off
    ## Sediment Yield from Interpolated grab samples
    LBJ['GrabInt-SedFlux-tons/sec'].plot(ax=SED,color='r',label='VILLAGE',ls='--')
    QUARRY['GrabInt-SedFlux-tons/sec'].plot(ax=SED,color='y',label='QUARRY-SedFlux-grab',ls='--')
    DAM['GrabInt-SedFlux-tons/sec'].plot(ax=SED,color='g',label='FOREST',ls='--')
    ## Sediment discharge from Turbidity Measurements
    LBJ['T-SedFlux-kg/sec']=LBJ['T-SedFlux-tons/sec']/1000
    LBJ['T-SedFlux-kg/sec'].plot(ax=SED,color='r',label='VILLAGE',ls='-')
    QUARRY['T-SedFlux-kg/sec']=QUARRY['T-SedFlux-tons/sec']/1000    
    QUARRY['T-SedFlux-kg/sec'].plot(ax=SED,color='y',label='QUARRY',ls='-')
    DAM['T-SedFlux-kg/sec']=DAM['T-SedFlux-tons/sec']/1000
    DAM['T-SedFlux-kg/sec'].plot(ax=SED,color='g',label='FOREST',ls='-')
    SED.set_ylabel('SSY\nkg/s')#, SED.set_yscale('log')#, SED.set_ylim(0,10)
    max_yticks = 3
    yloc = plt.MaxNLocator(max_yticks)
    SED.yaxis.set_major_locator(yloc) 
    SED.grid(False), SED.spines['bottom'].set_visible(False)

    #QP.legend(loc=0), P.legend(loc=1)             
    #SSC.legend(loc=0),SED.legend(loc=1)
    #Shade Storms
    showstormintervals(P,storm_threshold,storm_intervals)
    showstormintervals(Q,storm_threshold,storm_intervals)
    showstormintervals(T,storm_threshold,storm_intervals)
    showstormintervals(SSC,storm_threshold,storm_intervals)
    showstormintervals(SED,storm_threshold,storm_intervals)
    #plt.suptitle(title)
    plt.tight_layout(pad=0.1)
    show_plot(show)
    return
#SSY_Data(LBJ_storm_threshold,LBJ_StormIntervals,'LBJ_StormIntervals',show=True)


#### Event Sediment Flux Data
def stormdata(StormIntervals,print_stats=False):
    #storm_data = pd.DataFrame(columns=['Precip','LBJq','DAMq','LBJssc','DAMssc','LBJ-Sed','DAM-Sed','LBJgrab','QUARRYgrab','DAMgrab'],dtype=np.float64,index=pd.date_range(PT1.index[0],PT1.index[-1],freq='15Min'))   
    storm_data = pd.DataFrame()
    count = 0
    for storm in LBJ_StormIntervals.iterrows():
        count+=1
        start = storm[1]['start']
        end =  storm[1]['end']
        print start, end
        ## Slice data from storm start to start end
        ## LBJ
        LBJ_storm = LBJ[start:end]
        LBJ_storm['Sed-cumsum'] = LBJ_storm['SedFlux-tons/15min'].cumsum()
        LBJ_new_columns = []
        for column in LBJ_storm.columns:
            #print column
            LBJ_new_columns.append('LBJ-'+column)
        LBJ_storm.columns = LBJ_new_columns 
        ## QUARRY
        QUARRY_storm = QUARRY[start:end]
        QUARRY['Sed-cumsum'] = QUARRY_storm['SedFlux-tons/15min'].cumsum()
        QUARRY_new_columns=[]
        for column in QUARRY_storm.columns:
            QUARRY_new_columns.append('QUARRY-'+column)
        QUARRY_storm.columns = QUARRY_new_columns
        ## DAM
        DAM_storm = DAM[start:end]
        DAM_storm['Sed-cumsum'] = DAM_storm['SedFlux-tons/15min'].cumsum()
        DAM_new_columns = []
        for column in DAM_storm.columns:
            DAM_new_columns.append('DAM-'+column)
        DAM_storm.columns = DAM_new_columns
        
        P_storm = PrecipFilled['Precip'][start:end]
        #print data.index[0], data.index[-1]     
        ## add each storm to each other
        storm_data = storm_data.append(LBJ_storm.join(DAM_storm).join(QUARRY_storm).join(P_storm)) ## add each storm to each other
    storm_data = storm_data.reindex(pd.date_range(start2012,stop2014,freq='15Min'))
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
    #storm_data = storm_data[dt.datetime(2014,2,14,14,30):dt.datetime(2014,2,14,19,30)]
    fig, (P,Q,T,SSC,SED,SEDcum) = plt.subplots(nrows=6,ncols=1,sharex=True) 
    P.tick_params(\
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off') # labels along the bottom edge are off
    ## Precip
    storm_data['Precip'].plot(ax=P,color='b',ls='steps-pre',label='RG1')
    max_yticks =4
    yloc = MaxNLocator(max_yticks)
    P.yaxis.set_major_locator(yloc) 
    P.set_ylabel('P\nmm/15min'), P.grid(False)
    P.set_ylim(0,28)
    ## Discharge
    storm_data['LBJ-Q'].plot(ax=Q,color='r',label='VILLAGE')
    #storm_data['QUARRY-Q''].plot(ax=Q,color='y',label='QUARRY-Q')
    storm_data['DAM-Q'].plot(ax=Q,color='g',label='FOREST')
    Q.legend()
    Q.set_ylabel('Q\nL/s'),#, Q.set_yscale('log')
    Q.spines['bottom'].set_visible(False),Q.grid(False)
    Q.tick_params(axis='x',which='both',bottom='off',top='off',labelbottom='off') # labels along the bottom edge are off
    max_yticks = 4
    yloc = plt.MaxNLocator(max_yticks)    
    Q.yaxis.set_major_locator(yloc)    
    ## SSC grab samples
    storm_data['LBJ-Grab-SSC-mg/L'].plot(ax=SSC,color='r',marker='o',ls='None',markersize=6,label='VILLAGE')
    storm_data['QUARRY-Grab-SSC-mg/L'].plot(ax=SSC,color='y',marker='o',ls='None',markersize=6,label='QUARRY')
    storm_data['DAM-Grab-SSC-mg/L'].plot(ax=SSC,color='g',marker='o',ls='None',markersize=6,label='FOREST')
    ## Turbidity
    storm_data['LBJ-NTU'].plot(ax=T,color='r',label='VILLAGE')
    storm_data['QUARRY-NTU'].plot(ax=T,color='r',alpha=0.8,label='QUARRY')
    storm_data['DAM-NTU'].plot(ax=T,color='g',label='FOREST')
    T.set_ylabel('T NTU'),T.set_ylim(-1)
    max_yticks = 4
    yloc = plt.MaxNLocator(max_yticks)
    T.yaxis.set_major_locator(yloc) 
    T.grid(False), T.spines['bottom'].set_visible(False)
    T.tick_params(axis='x',which='both',bottom='off',top='off',labelbottom='off') # labels along the bottom edge are off
    ## SSC from turbidity
    storm_data['LBJ-T-SSC-mg/L'].plot(ax=SSC,color='r',label='VILLAGE')
    storm_data['QUARRY-T-SSC-mg/L'].plot(ax=SSC,ls='--',color='y',label='QUARRY')
    storm_data['DAM-T-SSC-mg/L'].plot(ax=SSC,color='g')
    ### SSC interpolated from grab samples
    storm_data['LBJ-GrabInt-SSC-mg/L'].plot(ax=SSC,ls='--',color='r',label='VILLAGE')
    storm_data['QUARRY-GrabInt-SSC-mg/L'].plot(ax=SSC,ls='--',color='y',label='QUARRY-SSC-grab')
    storm_data['DAM-GrabInt-SSC-mg/L'].plot(ax=SSC,ls='--',color='g',label='FOREST')
    SSC.set_ylabel('SSC\nmg/L')#, SSC.set_ylim(0,1400)
    max_yticks = 4
    yloc = plt.MaxNLocator(max_yticks)
    SSC.yaxis.set_major_locator(yloc) 
    SSC.grid(False),SSC.spines['bottom'].set_visible(False)
    SSC.tick_params(axis='x',which='both',bottom='off',top='off',labelbottom='off') # labels along the bottom edge are off
    ## Sediment Yield from Interpolated grab samples
    storm_data['LBJ-GrabInt-SedFlux-tons/sec'].plot(ax=SED,color='r',label='VILLAGE',ls='--')
    storm_data['QUARRY-GrabInt-SedFlux-tons/sec'].plot(ax=SED,color='y',label='QUARRY-SedFlux-grab',ls='--')
    storm_data['DAM-GrabInt-SedFlux-tons/sec'].plot(ax=SED,color='g',label='FOREST',ls='--')
    ## Sediment discharge from Turbidity Measurements
    storm_data['LBJ-T-SedFlux-kg/sec']=storm_data['LBJ-T-SedFlux-tons/sec']/1000
    storm_data['LBJ-T-SedFlux-kg/sec'].plot(ax=SED,color='r',label='VILLAGE',ls='-')
    storm_data['QUARRY-T-SedFlux-kg/sec']=storm_data['QUARRY-T-SedFlux-tons/sec']/1000    
    storm_data['QUARRY-T-SedFlux-kg/sec'].plot(ax=SED,color='y',label='QUARRY',ls='-')
    storm_data['DAM-T-SedFlux-kg/sec']=storm_data['DAM-T-SedFlux-tons/sec']/1000
    storm_data['DAM-T-SedFlux-kg/sec'].plot(ax=SED,color='g',label='FOREST',ls='-')
    SED.set_ylabel('SSY\nkg/s')#, SED.set_yscale('log')#, SED.set_ylim(0,10)
    max_yticks = 3
    yloc = plt.MaxNLocator(max_yticks)
    SED.yaxis.set_major_locator(yloc) 
    SED.grid(False), SED.spines['bottom'].set_visible(False)
    SED.tick_params(axis='x',which='both',bottom='off',top='off',labelbottom='off') # labels along the bottom edge are off
    ## Cumulative Sediment Load
    storm_data['LBJ-Sed-cumsum'].plot(ax=SEDcum,color='r',ls='-',label='VILLAGE')
    storm_data['QUARRY-Sed-cumsum'].plot(ax=SEDcum,color='y',ls='-',label='QUARRY-Cumulative Sed')    
    storm_data['DAM-Sed-cumsum'].plot(ax=SEDcum,color='g',ls='-',label='FOREST') 
    SEDcum.set_ylabel('Cum. SSY\ntons')
    max_yticks = 4
    yloc = plt.MaxNLocator(max_yticks)
    SEDcum.yaxis.set_major_locator(yloc) 
    SEDcum.yaxis.set_ticks_position('right')
    SEDcum.grid(False)
    #QP.legend(loc=0), P.legend(loc=1)             
    #SSC.legend(loc=0),SED.legend(loc=1)
    #Shade Storms
    showstormintervals(P,storm_threshold,storm_intervals)
    showstormintervals(Q,storm_threshold,storm_intervals)
    showstormintervals(T,storm_threshold,storm_intervals)
    showstormintervals(SSC,storm_threshold,storm_intervals)
    showstormintervals(SED,storm_threshold,storm_intervals)
    showstormintervals(SEDcum,storm_threshold,storm_intervals)
    #plt.suptitle(title)
    show_plot(show)
    return
#Storm_SedFlux(storm_data_LBJ,LBJ_storm_threshold,LBJ_StormIntervals,'LBJ_StormIntervals',show=True)
#Storm_SedFlux(storm_data_DAM,DAM_storm_threshold,DAM_StormIntervals,'DAM_StormIntervals',show=True)

def plot_all_storms_individually(storm_threshold,storm_intervals,show=False,save=True):
    count = 0
    for storm in storm_intervals.iterrows():
        count+=1
        start = storm[1]['start']-dt.timedelta(minutes=60)
        end =  storm[1]['end']+dt.timedelta(minutes=60)
        #print start, end
        ## Slice data from storm start to start end
        ## LBJ
        LBJ_storm = LBJ[start:end]
        LBJ_storm['Sed-cumsum'] = LBJ_storm['SedFlux-tons/15min'].cumsum()
        LBJ_new_columns = []
        for column in LBJ_storm.columns:
            #print column
            LBJ_new_columns.append('LBJ-'+column)
        LBJ_storm.columns = LBJ_new_columns 
        ## QUARRY
        QUARRY_storm = QUARRY[start:end]
        QUARRY['Sed-cumsum'] = QUARRY_storm['SedFlux-tons/15min'].cumsum()
        QUARRY_new_columns=[]
        for column in QUARRY_storm.columns:
            QUARRY_new_columns.append('QUARRY-'+column)
        QUARRY_storm.columns = QUARRY_new_columns
        ## DAM
        DAM_storm = DAM[start:end]
        DAM_storm['Sed-cumsum'] = DAM_storm['SedFlux-tons/15min'].cumsum()
        DAM_new_columns = []
        for column in DAM_storm.columns:
            DAM_new_columns.append('DAM-'+column)
        DAM_storm.columns = DAM_new_columns
        
        P_storm = PrecipFilled['Precip'][start:end]

        storm_data = LBJ_storm.join(DAM_storm).join(QUARRY_storm).join(P_storm)
        ## Summary stats
        total_storm = len(storm_data[start:end])
        percent_P = len(storm_data['Precip'].dropna())/total_storm *100.
        percent_Q_LBJ = len(storm_data['LBJ-Q'].dropna())/total_storm * 100.
        percent_Q_DAM = len(storm_data['DAM-Q'].dropna())/total_storm * 100.
        percent_SSC_LBJ = len(storm_data['LBJ-SSC-mg/L'].dropna())/total_storm * 100.
        percent_SSC_QUARRY = len(storm_data['QUARRY-SSC-mg/L'].dropna())/total_storm * 100.
        percent_SSC_DAM = len(storm_data['DAM-SSC-mg/L'].dropna())/total_storm * 100.
        count_LBJgrab = len(LBJ['Grab-SSC-mg/L'].dropna())
        count_QUARRYgrab = len(QUARRY['Grab-SSC-mg/L'].dropna())
        count_DAMgrab = len(DAM['Grab-SSC-mg/L'].dropna())
        #print str(start)+' '+str(end)+' Storm#:'+str(count)
        #print '%P:'+str(percent_P)+' %Q_LBJ:'+str(percent_Q_LBJ)+' %Q_DAM:'+str(percent_Q_DAM)
        #print '%SSC_LBJ:'+str(percent_SSC_LBJ)+' %SSC_DAM:'+str(percent_SSC_DAM)
        #print '#LBJgrab:'+str(count_LBJgrab)+' #QUARRYgrab:'+str(count_QUARRYgrab)+' #DAMgrab:'+str(count_DAMgrab)        
        ##Plotting per storm
        plt.ioff()
        fig, (P,Q,T,SSC,SED,SEDcum) = plt.subplots(nrows=6,ncols=1,sharex=True) 
        P.tick_params(\
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelbottom='off') # labels along the bottom edge are off
        plt.suptitle('Storm: '+str(count)+' start: '+str(start)+' end: '+str(end), fontsize=22)
        ## Precip
        storm_data['Precip'].plot(ax=P,color='b',ls='steps-pre',label='Timu1')
        P_max, P_sum = storm_data['Precip'].max(), storm_data['Precip'].sum()
        P.set_ylabel('Precip mm'),P.set_ylim(-1,Precip['Timu1-15'].max()+2)
        ## Discharge
        storm_data['LBJ-Q'].plot(ax=Q,color='r',label='LBJ-Q')
        LBJ_Qmax, LBJ_Qmean, LBJ_Qsum = storm_data['LBJ-Q'].max(), storm_data['LBJ-Q'].mean(), storm_data['LBJ-Q'].sum()
        storm_data['QUARRY-Q'].plot(ax=Q,color='y',label='QUARRY-Q')
        QUARRY_Qmax, QUARRY_Qmean, QUARRY_Qsum = storm_data['QUARRY-Q'].max(),storm_data['QUARRY-Q'].mean(),storm_data['QUARRY-Q'].sum()
        storm_data['DAM-Q'].plot(ax=Q,color='g',label='DAM-Q')
        DAM_Qmax, DAM_Qmean, DAM_Qsum = storm_data['DAM-Q'].max(), storm_data['DAM-Q'].mean(), storm_data['DAM-Q'].sum()
        Q.set_ylabel('Q L/sec'), Q.set_ylim(-1,6000)
        ## Turbidity
        storm_data['LBJ-NTU'].plot(ax=T,color='r',label='LBJ-NTU')
        LBJ_NTUmax, LBJ_NTUmean = storm_data['LBJ-NTU'].max(), storm_data['LBJ-NTU'].mean()
        storm_data['QUARRY-NTU'].plot(ax=T,color='y',label='QUARRY-NTU')
        QUARRY_NTUmax, QUARRY_NTUmean = storm_data['QUARRY-NTU'].max(), storm_data['QUARRY-NTU'].mean()
        storm_data['DAM-NTU'].plot(ax=T,color='g',label='DAM-NTU')
        DAM_NTUmax, DAM_NTUmean = storm_data['DAM-NTU'].max(), storm_data['DAM-NTU'].mean()
        T.set_ylabel('T (NTU)'),T.set_ylim(-1,2000)
        ## SSC from Turbidity
        storm_data['LBJ-T-SSC-mg/L'].plot(ax=SSC,color='r',label='LBJ-SSC')
        LBJ_SSCmax, LBJ_SSCmean = storm_data['LBJ-T-SSC-mg/L'].max(), storm_data['LBJ-T-SSC-mg/L'].mean()
        storm_data['QUARRY-T-SSC-mg/L'].plot(ax=SSC,color='y',label='QUARRY-SSC')
        QUARRY_SSCmax, QUARRY_SSCmean = storm_data['QUARRY-T-SSC-mg/L'].max(), storm_data['QUARRY-T-SSC-mg/L'].mean()
        storm_data['DAM-T-SSC-mg/L'].plot(ax=SSC,color='g',label='DAM-SSC')
        DAM_SSCmax, DAM_SSCmean = storm_data['DAM-T-SSC-mg/L'].max(), storm_data['DAM-T-SSC-mg/L'].mean()
        ## Grabs
        storm_data['LBJ-Grab-SSC-mg/L'].plot(ax=SSC,color='r',marker='o',ls='None',markersize=6,label='LBJ-grab')
        storm_data['QUARRY-Grab-SSC-mg/L'].plot(ax=SSC,color='y',marker='o',ls='None',markersize=6,label='QUARRY-grab')
        storm_data['DAM-Grab-SSC-mg/L'].plot(ax=SSC,color='g',marker='o',ls='None',markersize=6,label='DAM-grab')
        SSC.set_ylabel('SSC mg/L'), SSC.set_ylim(-1,1500)
        ### SSC interpolated from grab samples
        storm_data['LBJ-GrabInt-SSC-mg/L'].plot(ax=SSC,ls='--',color='r',label='LBJ-SSC')
        LBJ_SSCgrabmax, LBJ_SSCgrabmean = storm_data['LBJ-GrabInt-SSC-mg/L'].max(), storm_data['LBJ-GrabInt-SSC-mg/L'].mean()
        storm_data['QUARRY-GrabInt-SSC-mg/L'].plot(ax=SSC,ls='--',color='y',label='QUARRY-SSC')
        QUARRY_SSCgrabmax, QUARRY_SSCgrabmean = storm_data['QUARRY-GrabInt-SSC-mg/L'].max(), storm_data['QUARRY-GrabInt-SSC-mg/L'].mean()
        storm_data['DAM-GrabInt-SSC-mg/L'].plot(ax=SSC,ls='--',color='g',label='DAM-SSC')
        DAM_SSCgrabmax, DAM_SSCgrabmean = storm_data['DAM-GrabInt-SSC-mg/L'].max(), storm_data['DAM-GrabInt-SSC-mg/L'].mean()
        ## Sediment discharge
        storm_data['LBJ-SedFlux-tons/sec'].plot(ax=SED,color='r',label='LBJ-SedFlux',ls='-')
        LBJ_Smax, LBJ_Smean, LBJ_Ssum = storm_data['LBJ-SedFlux-tons/sec'].max(), storm_data['LBJ-SedFlux-tons/sec'].mean(), storm_data['LBJ-SedFlux-tons/sec'].sum()
        storm_data['QUARRY-SedFlux-tons/sec'].plot(ax=SED,color='y',label='QUARRY-SedFlux',ls='-')
        QUARRY_Smax, QUARRY_Smean, QUARRY_Ssum = storm_data['QUARRY-SedFlux-tons/sec'].max(), storm_data['QUARRY-SedFlux-tons/sec'].mean(), storm_data['QUARRY-SedFlux-tons/sec'].sum()
        storm_data['DAM-SedFlux-tons/sec'].plot(ax=SED,color='g',label='DAM-SedFlux',ls='-')
        DAM_Smax, DAM_Smean, DAM_Ssum = storm_data['DAM-SedFlux-tons/sec'].max(), storm_data['DAM-SedFlux-tons/sec'].mean(), storm_data['DAM-SedFlux-tons/sec'].sum()
        SED.set_ylabel('SSY tons/sec')#, SED.set_ylim(-.1,4000)
        #P.legend(loc='best'), 
        Q.legend(loc='best',ncol=2), T.legend(loc='best',ncol=3)          
        SSC.legend(loc='best',ncol=5),SED.legend(loc='best',ncol=2)
        ## Cumulative Sediment Load
        storm_data['LBJ-Sed-cumsum'].plot(ax=SEDcum,color='r',ls='--',label='VILLAGE')
        storm_data['QUARRY-Sed-cumsum'].plot(ax=SEDcum,color='y',ls='--',label='QUARRY-Cumulative Sed')    
        storm_data['DAM-Sed-cumsum'].plot(ax=SEDcum,color='g',ls='--',label='FOREST') 
        SEDcum.set_ylabel('Cum. SSY\ntons')
        max_yticks = 4
        yloc = plt.MaxNLocator(max_yticks)
        SEDcum.yaxis.set_major_locator(yloc) 
        SEDcum.yaxis.set_ticks_position('right')
        SEDcum.grid(False)
        #Shade Storms
        shade_color='grey'
        start, end = storm[1]['start'], storm[1]['end']
        P.axvspan(start,end,ymin=0,ymax=200,facecolor=shade_color, alpha=0.25), Q.axvspan(start,end,ymin=0,ymax=200,facecolor=shade_color, alpha=0.25)
        T.axvspan(start,end,ymin=0,ymax=200,facecolor=shade_color, alpha=0.25), SSC.axvspan(start,end,ymin=0,ymax=200,facecolor=shade_color, alpha=0.25)
        SED.axvspan(start,end,ymin=0,ymax=200,facecolor=shade_color, alpha=0.25)
        SEDcum.axvspan(start,end,ymin=0,ymax=200,facecolor=shade_color, alpha=0.25)
        plt.tight_layout()        
    
        title='Storm_'+str(count)+' '+str(start.year)+'-'+str(start.month)+'-'+str(start.day)
        if save ==True:
            plt.savefig(figdir+'storm_figures/'+title+'.png')
        if show==True:
            plt.show()
        elif show==False:
            plt.close('all')
    plt.ion()
    return
#plot_all_storms_individually(LBJ_storm_threshold,LBJ_StormIntervals,show=True,save=False) # for individual storm pd.DataFrame(Intervals.loc[index#]).T 

def plot_storm_individually(storm_threshold,storm,show=False,save=True,filename=''):
    ## Storm Intervals -60 minutes to show whole storm
    start = storm['start']-dt.timedelta(minutes=60)
    end =  storm['end']+dt.timedelta(minutes=60)
    #print start, end
    ## Slice data from storm start to start end
    ## LBJ
    LBJ_storm = LBJ[start:end]
    LBJ_storm['Sed-cumsum'] = LBJ_storm['SedFlux-tons/15min'].cumsum()
    LBJ_new_columns = []
    for column in LBJ_storm.columns:
        #print column
        LBJ_new_columns.append('LBJ-'+column)
    LBJ_storm.columns = LBJ_new_columns 
    ## QUARRY
    QUARRY_storm = QUARRY[start:end]
    QUARRY['Sed-cumsum'] = QUARRY_storm['SedFlux-tons/15min'].cumsum()
    QUARRY_new_columns=[]
    for column in QUARRY_storm.columns:
        QUARRY_new_columns.append('QUARRY-'+column)
    QUARRY_storm.columns = QUARRY_new_columns
    ## DAM
    DAM_storm = DAM[start:end]
    DAM_storm['Sed-cumsum'] = DAM_storm['SedFlux-tons/15min'].cumsum()
    DAM_new_columns = []
    for column in DAM_storm.columns:
        DAM_new_columns.append('DAM-'+column)
    DAM_storm.columns = DAM_new_columns
    ## Precip
    P_storm = PrecipFilled['Precip'][start:end]
    ## Compile Storm Data
    storm_data = LBJ_storm.join(DAM_storm).join(QUARRY_storm).join(P_storm)
    ## Summary stats
    total_storm = len(storm_data[start:end])
    percent_P = len(storm_data['Precip'].dropna())/total_storm *100.
    percent_Q_LBJ = len(storm_data['LBJ-Q'].dropna())/total_storm * 100.
    percent_Q_DAM = len(storm_data['DAM-Q'].dropna())/total_storm * 100.
    percent_SSC_LBJ = len(storm_data['LBJ-SSC-mg/L'].dropna())/total_storm * 100.
    percent_SSC_QUARRY = len(storm_data['QUARRY-SSC-mg/L'].dropna())/total_storm * 100.
    percent_SSC_DAM = len(storm_data['DAM-SSC-mg/L'].dropna())/total_storm * 100.
    count_LBJgrab = len(LBJ['Grab-SSC-mg/L'].dropna())
    count_QUARRYgrab = len(QUARRY['Grab-SSC-mg/L'].dropna())
    count_DAMgrab = len(DAM['Grab-SSC-mg/L'].dropna())
    #print str(start)+' '+str(end)
    #print '%P:'+str(percent_P)+' %Q_LBJ:'+str(percent_Q_LBJ)+' %Q_DAM:'+str(percent_Q_DAM)
    #print '%SSC_LBJ:'+str(percent_SSC_LBJ)+' %SSC_DAM:'+str(percent_SSC_DAM)
    #print '#LBJgrab:'+str(count_LBJgrab)+' #QUARRYgrab:'+str(count_QUARRYgrab)+' #DAMgrab:'+str(count_DAMgrab)        
    ##Plotting per storm
    fig, (P,Q,T,SSC,SED,SEDcum) = plt.subplots(nrows=6,ncols=1,sharex=True,figsize=(8,8)) 
    P.tick_params(\
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off') # labels along the bottom edge are off
    #plt.suptitle(' start: '+str(start)+' end: '+str(end), fontsize=22)
    ## Precip
    storm_data['Precip'].plot(ax=P,color='k',ls='steps-pre',label='Timu1')
    P_max, P_sum = storm_data['Precip'].max(), storm_data['Precip'].sum()
    P.set_ylabel('Precip mm'),P.set_ylim(-1,Precip['Timu1-15'].max()+2)
    ## Discharge Q
    storm_data['LBJ-Q'].plot(ax=Q,color='k',label='FG3')
    LBJ_Qmax, LBJ_Qmean, LBJ_Qsum = storm_data['LBJ-Q'].max(), storm_data['LBJ-Q'].mean(), storm_data['LBJ-Q'].sum()
    storm_data['QUARRY-Q'].plot(ax=Q,color='grey',ls='-.',label='FG2')
    QUARRY_Qmax, QUARRY_Qmean, QUARRY_Qsum = storm_data['QUARRY-Q'].max(),storm_data['QUARRY-Q'].mean(),storm_data['QUARRY-Q'].sum()
    storm_data['DAM-Q'].plot(ax=Q,color='grey',label='FG1')
    DAM_Qmax, DAM_Qmean, DAM_Qsum = storm_data['DAM-Q'].max(), storm_data['DAM-Q'].mean(), storm_data['DAM-Q'].sum()
    Q.set_ylabel('Q L/sec')#, Q.set_ylim(-1,6000)
    ## Turbidity T
    storm_data['LBJ-NTU'].plot(ax=T,color='k',label='LBJ-NTU')
    LBJ_NTUmax, LBJ_NTUmean = storm_data['LBJ-NTU'].max(), storm_data['LBJ-NTU'].mean()
    #storm_data['QUARRY-NTU'].plot(ax=T,color='y',label='QUARRY-NTU')
    #QUARRY_NTUmax, QUARRY_NTUmean = storm_data['QUARRY-NTU'].max(), storm_data['QUARRY-NTU'].mean()
    storm_data['DAM-NTU'].plot(ax=T,color='grey',label='DAM-NTU')
    DAM_NTUmax, DAM_NTUmean = storm_data['DAM-NTU'].max(), storm_data['DAM-NTU'].mean()
    T.set_ylabel('T (NTU)')#,T.set_ylim(-1,2000)
    ## SSC from Turbidity T-SSC
    storm_data['LBJ-T-SSC-mg/L'].plot(ax=SSC,ls='-',color='k',label='VILLAGE')
    LBJ_SSCmax, LBJ_SSCmean = storm_data['LBJ-T-SSC-mg/L'].max(), storm_data['LBJ-T-SSC-mg/L'].mean()
    storm_data['QUARRY-T-SSC-mg/L'].plot(ax=SSC,ls='-.',color='grey',label='QUARRY')
    QUARRY_SSCmax, QUARRY_SSCmean = storm_data['QUARRY-T-SSC-mg/L'].max(), storm_data['QUARRY-T-SSC-mg/L'].mean()
    storm_data['DAM-T-SSC-mg/L'].plot(ax=SSC,ls='-',color='grey',label='FOREST')
    DAM_SSCmax, DAM_SSCmean = storm_data['DAM-T-SSC-mg/L'].max(), storm_data['DAM-T-SSC-mg/L'].mean()
    #SSC.legend(loc='best',ncol=1)
    ## Grabs Grab-SSC
    storm_data['LBJ-Grab-SSC-mg/L'].plot(ax=SSC,color='k',marker='o',ls='None',markersize=4,label=None)
    storm_data['QUARRY-Grab-SSC-mg/L'].plot(ax=SSC,color='grey',marker='s',ls='None',markersize=4,label=None)
    storm_data['DAM-Grab-SSC-mg/L'].plot(ax=SSC,color='grey',marker='^',ls='None',markersize=4,label=None)
    SSC.set_ylabel('SSC mg/L')#, SSC.set_ylim(-1,1500)
    ### SSC interpolated from grab samples GrabInt-SSC
    storm_data['LBJ-GrabInt-SSC-mg/L'].plot(ax=SSC,ls='--',color='k')#,label='VIL-int')
    LBJ_SSCgrabmax, LBJ_SSCgrabmean = storm_data['LBJ-GrabInt-SSC-mg/L'].max(), storm_data['LBJ-GrabInt-SSC-mg/L'].mean()
    storm_data['QUARRY-GrabInt-SSC-mg/L'].plot(ax=SSC,ls='-.',color='grey')#,label='QUA-int')
    QUARRY_SSCgrabmax, QUARRY_SSCgrabmean = storm_data['QUARRY-GrabInt-SSC-mg/L'].max(), storm_data['QUARRY-GrabInt-SSC-mg/L'].mean()
    storm_data['DAM-GrabInt-SSC-mg/L'].plot(ax=SSC,ls='--',color='grey')#,label='FOR-int')
    DAM_SSCgrabmax, DAM_SSCgrabmean = storm_data['DAM-GrabInt-SSC-mg/L'].max(), storm_data['DAM-GrabInt-SSC-mg/L'].mean()
    ## Sediment Yield SedFlux
    storm_data['LBJ-SedFlux-kg/sec'].plot(ax=SED,ls='-',color='k',label='FG3')
    LBJ_Smax, LBJ_Smean, LBJ_Ssum = storm_data['LBJ-SedFlux-tons/sec'].max(), storm_data['LBJ-SedFlux-tons/sec'].mean(), storm_data['LBJ-SedFlux-tons/sec'].sum()
    storm_data['QUARRY-SedFlux-kg/sec'].plot(ax=SED,ls='-.',color='grey',label='FG2')
    QUARRY_Smax, QUARRY_Smean, QUARRY_Ssum = storm_data['QUARRY-SedFlux-tons/sec'].max(), storm_data['QUARRY-SedFlux-tons/sec'].mean(), storm_data['QUARRY-SedFlux-tons/sec'].sum()
    storm_data['DAM-SedFlux-kg/sec'].plot(ax=SED,ls='-',color='grey',label='FG1')
    DAM_Smax, DAM_Smean, DAM_Ssum = storm_data['DAM-SedFlux-tons/sec'].max(), storm_data['DAM-SedFlux-tons/sec'].mean(), storm_data['DAM-SedFlux-tons/sec'].sum()
    SED.set_ylabel('SSY kg/sec')#, SED.set_ylim(-.1,4000)
    ## Cumulative Sediment Load
    storm_data['LBJ-Sed-cumsum'].plot(ax=SEDcum,color='k',ls='-',label='FG3')
    storm_data['QUARRY-Sed-cumsum'].plot(ax=SEDcum,color='grey',ls='-.',label='FG2')    
    storm_data['DAM-Sed-cumsum'].plot(ax=SEDcum,color='grey',ls='-',label='FG1') 
    SEDcum.set_ylabel('Cumulative SSY\ntons'),SEDcum.yaxis.set_ticks_position('right')
    for axis in fig.axes:
        max_yticks = 4
        yloc = plt.MaxNLocator(max_yticks)
        axis.yaxis.set_major_locator(yloc) 
        axis.grid(False)
    ## Legends
    #P.legend(loc='best'), 
    Q.legend(loc='best',ncol=2)#, T.legend(loc='best',ncol=3)          
    #SED.legend(loc='best',ncol=3)#,SSC.legend(loc='best',ncol=5)
    #Shade Storms
    shade_storms=False
    if shade_storms==True:
        shade_color='grey'
        start, end = storm[1]['start'], storm[1]['end']
        P.axvspan(start,end,ymin=0,ymax=200,facecolor=shade_color, alpha=0.25), Q.axvspan(start,end,ymin=0,ymax=200,facecolor=shade_color, alpha=0.25)
        T.axvspan(start,end,ymin=0,ymax=200,facecolor=shade_color, alpha=0.25), SSC.axvspan(start,end,ymin=0,ymax=200,facecolor=shade_color, alpha=0.25)
        SED.axvspan(start,end,ymin=0,ymax=200,facecolor=shade_color, alpha=0.25)
        SEDcum.axvspan(start,end,ymin=0,ymax=200,facecolor=shade_color, alpha=0.25)
    letter_subplots(fig,x=0.10,y=0.95,vertical='top',horizontal='right',Color='k',font_size=10,font_weight='bold')
    plt.tight_layout(pad=0.1)        
    #title=str(start.year)+'-'+str(start.month)+'-'+str(start.day)
    show_plot(show)
    savefig(save,filename)
    return
#plot_storm_individually(LBJ_storm_threshold,LBJ_StormIntervals.loc[63],show=True,save=False,filename='') # for individual storm pd.DataFrame(Intervals.loc[index#]).T 

#### Event Sediment Flux
AV_Q_measurement_RMSE = 8.5 # these come from Harmel 2009 lookup table in DUET-HWQ
SSC_measurement_RMSE = 12.4 + 3.9 # includes collection and lab analysis; these come from Harmel 2009 lookup table in DUET-HWQ
#### LBJ Event-wise Sediment Flux DataFrame
SedFluxStorms_LBJ = StormSums(LBJ_StormIntervals,LBJ['SedFlux-tons/15min'])
SedFluxStorms_LBJ.columns = ['Sstart','Send','Scount','Ssum','Smax']
SedFluxStorms_LBJ=SedFluxStorms_LBJ.join(Qstorms_LBJ) ## Add Event Discharge
SedFluxStorms_LBJ = SedFluxStorms_LBJ.join(Pstorms_LBJ)
## SSY RMSE
SedFluxStorms_LBJ['Stage-Q-model-RMSE'] = StormSums(LBJ_StormIntervals,LBJ['Q-RMSE'])['max'] ## Add Stage-Q model RMSE
SedFluxStorms_LBJ['T-SSC-model-RMSE'] = StormSums(LBJ_StormIntervals,LBJ['SSC-mg/L-RMSE'])['max'] ##  Add T-SSC model RMSE
SedFluxStorms_LBJ['PE'] = ((AV_Q_measurement_RMSE**2. + SSC_measurement_RMSE**2.)+(SedFluxStorms_LBJ['Stage-Q-model-RMSE']**2. + SedFluxStorms_LBJ['T-SSC-model-RMSE']**2.))**0.5 ## Calculate Cumulative Probable Error Harmel  2009

#### QUARRY Event-wise Sediment Flux DataFrame
SedFluxStorms_QUARRY = StormSums(QUARRY_StormIntervals,QUARRY['SedFlux-tons/15min'])
SedFluxStorms_QUARRY.columns = ['Sstart','Send','Scount','Ssum','Smax']
SedFluxStorms_QUARRY=SedFluxStorms_QUARRY.join(Qstorms_QUARRY)
SedFluxStorms_QUARRY=SedFluxStorms_QUARRY.join(Pstorms_QUARRY)
## SSY RMSE
SedFluxStorms_QUARRY['Stage-Q-model-RMSE'] = StormSums(QUARRY_StormIntervals,QUARRY['Q-RMSE'])['max'] ## Add Stage-Q model RMSE
SedFluxStorms_QUARRY['T-SSC-model-RMSE'] = StormSums(QUARRY_StormIntervals,QUARRY['SSC-mg/L-RMSE'])['max'] ##  Add T-SSC model RMSE
SedFluxStorms_QUARRY['PE'] = ((AV_Q_measurement_RMSE**2. + SSC_measurement_RMSE**2.)+(SedFluxStorms_QUARRY['Stage-Q-model-RMSE']**2. + SedFluxStorms_QUARRY['T-SSC-model-RMSE']**2.))**0.5 ## Calculate Cumulative Probable Error Harmel  2009

#### DAM Event-wise Sediment Flux DataFrame
SedFluxStorms_DAM = StormSums(DAM_StormIntervals,DAM['SedFlux-tons/15min'])
SedFluxStorms_DAM.columns = ['Sstart','Send','Scount','Ssum','Smax']
SedFluxStorms_DAM=SedFluxStorms_DAM.join(Qstorms_DAM)
SedFluxStorms_DAM=SedFluxStorms_DAM.join(Pstorms_DAM)
## SSY RMSE
SedFluxStorms_DAM['Stage-Q-model-RMSE'] = StormSums(DAM_StormIntervals,DAM['Q-RMSE'])['max'] ## Add Stage-Q model RMSE
SedFluxStorms_DAM['T-SSC-model-RMSE'] = StormSums(DAM_StormIntervals,DAM['SSC-mg/L-RMSE'])['max'] ##  Add T-SSC model RMSE
SedFluxStorms_DAM['PE'] = ((AV_Q_measurement_RMSE**2. + SSC_measurement_RMSE**2.)+(SedFluxStorms_DAM['Stage-Q-model-RMSE']**2. + SedFluxStorms_DAM['T-SSC-model-RMSE']**2.))**0.5 ## Calculate Cumulative Probable Error Harmel  2009


### Grab vs T for SSY
## LBJ
LBJ_GrabInt_storms = StormSums(LBJ_StormIntervals,LBJ['GrabInt-SedFlux-tons/15min']).dropna()
LBJ_GrabInt_storms['datasource'] = 'int. grab'
LBJ_T_SSC_storms = StormSums(LBJ_StormIntervals,LBJ['T-SedFlux-tons/15min']).dropna()
LBJ_T_SSC_storms['datasource'] = 'T-YSI'
LBJ_T_SSC_storms['datasource'].ix[dt.datetime(2013,1,1):] = 'T-OBS'
SedFluxStorms_LBJ['datasource']= LBJ_T_SSC_storms['datasource']
SedFluxStorms_LBJ['datasource']=SedFluxStorms_LBJ['datasource'].fillna(LBJ_GrabInt_storms['datasource'])
## DAM
DAM_GrabInt_storms = StormSums(LBJ_StormIntervals,DAM['GrabInt-SedFlux-tons/15min']).dropna()
DAM_GrabInt_storms['datasource'] = 'int. grab'
DAM_T_SSC_storms = StormSums(LBJ_StormIntervals,DAM['T-SedFlux-tons/15min']).dropna()
DAM_T_SSC_storms['datasource'] = 'T-TS'
DAM_T_SSC_storms['datasource'].ix[dt.datetime(2013,1,1):] = 'T-YSI'
SedFluxStorms_DAM['datasource']= DAM_T_SSC_storms['datasource']
SedFluxStorms_DAM['datasource']=SedFluxStorms_DAM['datasource'].fillna(DAM_GrabInt_storms['datasource'])

#### Calculate correlation coefficients and sediment rating curves    
def compileALLStorms(subset = 'pre'):
    ## Sediment Yield
    ALLStorms=pd.DataFrame({'Supper':SedFluxStorms_DAM['Ssum'],'Supper_PE':SedFluxStorms_DAM['PE'],
    'Slower':SedFluxStorms_LBJ['Ssum']-SedFluxStorms_DAM['Ssum'],
    'Stotal':SedFluxStorms_LBJ['Ssum'],'Stotal_PE':SedFluxStorms_LBJ['PE'],
    'Squarry':SedFluxStorms_QUARRY['Ssum'],'Squarry_PE':SedFluxStorms_QUARRY['PE']})
    ## Sediment Yield datasource
    ALLStorms['SSY_data_source_total'] = SedFluxStorms_LBJ['datasource']
    ALLStorms['SSY_data_source_upper'] = SedFluxStorms_DAM['datasource']
    
    ## Qsum
    ALLStorms['Qsumtotal']=SedFluxStorms_LBJ['Qsum']/1000 # L to m3
    ALLStorms['Qsumupper']=SedFluxStorms_DAM['Qsum']/1000 # L to m3
    ALLStorms['Qsumlower']=SedFluxStorms_LBJ['Qsum']-SedFluxStorms_DAM['Qsum']
    ALLStorms['Qsumquarry'] =SedFluxStorms_QUARRY['Qsum']/1000 #L to m3
    ## Qmax
    ALLStorms['Qmaxupper']=SedFluxStorms_DAM['Qmax']/1000 # L to m3
    ALLStorms['Qmaxlower']=SedFluxStorms_LBJ['Qmax']/1000 # L to m3
    ALLStorms['Qmaxtotal']=SedFluxStorms_LBJ['Qmax']/1000 # L to m3
    ## Add Event Precipitation and EI
    ALLStorms['Pstorms']=Pstorms_LBJ['Psum'] ## Add Event Precip
    ALLStorms['EI'] = LBJ_Stormdf['EI'][LBJ_Stormdf['EI']>1] ## Add Event Erosion Index
    if subset == 'pre':
        ALLStorms = ALLStorms[ALLStorms.index<Mitigation]
    elif subset == 'post':
        ALLStorms = ALLStorms[ALLStorms.index>Mitigation]
    return ALLStorms
ALLStorms = compileALLStorms()

def S_storm_diff_table(subset='pre'):
    S_diff = compileALLStorms(subset)
    ## Calculate percent contributions from upper and lower watersheds
    S_diff['UPPER tons']=S_diff['Supper'].round(2)
    #S_diff['UPPER SSY data source'] = S_diff['SSY_data_source_upper']
    S_diff['UPPER PE %'] = S_diff['Supper_PE'].apply(int)
    S_diff['LOWER tons']=S_diff['Slower'].round(2)
    S_diff['TOTAL tons']=S_diff['Stotal'].round(2)
    #S_diff['TOTAL SSY data source'] = S_diff['SSY_data_source_total']
    S_diff['SSY data source'] = S_diff['SSY_data_source_total']
    S_diff['TOTAL PE %'] = S_diff['Stotal_PE'].apply(int)
    S_diff['% UPPER'] = S_diff['Supper']/S_diff['Stotal']*100
    S_diff['% UPPER'] = S_diff['% UPPER'].dropna().apply(int)
    S_diff['% LOWER'] = S_diff['Slower']/S_diff['Stotal']*100
    S_diff['% LOWER'] = S_diff['% LOWER'].dropna().apply(int)
    S_diff['Precip (mm)'] = S_diff['Pstorms'].apply(int)
    S_diff = S_diff[S_diff['Precip (mm)']>0]
    ## Filter negative values for S at LBJ    
    S_diff = S_diff[S_diff['Slower']>0]
    ## Storm Indices
    S_diff['Storm#']=range(1,len(S_diff)+1) 
    S_diff['Storm Start'] = S_diff.index
    S_diff['Storm Start'] =S_diff['Storm Start'].apply(lambda x: "{:%m/%d/%Y}".format(x))
    ## summary stats
    Percent_Upper = S_diff['Supper'].sum()/S_diff['Stotal'].sum()*100
    Percent_Lower = S_diff['Slower'].sum()/S_diff['Stotal'].sum()*100    
    ## add summary stats to bottom of table
    # Total/Avg
    SSY_UPPER, SSY_LOWER, SSY_TOTAL = S_diff['UPPER tons'].sum(), S_diff['LOWER tons'].sum(), S_diff['TOTAL tons'].sum()
    S_diff=S_diff.append(pd.DataFrame({'Storm Start':'Total/Avg:','Storm#':"%.0f"%len(S_diff),'Precip (mm)':"%.0f"%S_diff['Precip (mm)'].sum(),'UPPER tons':"%.1f"%SSY_UPPER,'UPPER PE %':"%.0f"%S_diff['UPPER PE %'].mean(),'LOWER tons':"%.1f"%SSY_LOWER,'TOTAL tons':"%.1f"%SSY_TOTAL,'SSY data source':' ','TOTAL PE %':"%.0f"%S_diff['TOTAL PE %'].mean(),'% UPPER':"%.0f"%Percent_Upper,'% LOWER':"%.0f"%Percent_Lower},index=['Total/Avg:']))
    
    # sSSY
    sSSY_UPPER, sSSY_LOWER, sSSY_TOTAL = SSY_UPPER/0.9, SSY_LOWER/0.88, SSY_TOTAL/1.78
    S_diff=S_diff.append(pd.DataFrame({'Storm Start':'Tons/km2','Storm#':'','Precip (mm)':'','UPPER tons':"%.1f"%sSSY_UPPER,'UPPER PE %':'','LOWER tons':"%.1f"%sSSY_LOWER,'TOTAL tons':"%.1f"%sSSY_TOTAL,'SSY data source':' ','TOTAL PE %':'','% UPPER':'-','% LOWER':'-'}, index=['Tons/km2']))
    
    # sSSY:sSSY_UPPER
    DR_sSSY_UPPER, DR_sSSY_LOWER, DR_sSSY_TOTAL = sSSY_UPPER/sSSY_UPPER,sSSY_LOWER/sSSY_UPPER,sSSY_TOTAL/sSSY_UPPER
    S_diff=S_diff.append(pd.DataFrame({'Storm Start':'DR','Storm#':'','Precip (mm)':'','UPPER tons':"%.0f"%DR_sSSY_UPPER,'UPPER PE %':'','LOWER tons':"%.1f"%DR_sSSY_LOWER,'TOTAL tons':"%.1f"%DR_sSSY_TOTAL,'SSY data source':' ','TOTAL PE %':'','% UPPER':'-','% LOWER':'-'}, index=['DR']))
 
    ## Order columns
    S_diff=S_diff[['Storm Start','Storm#','Precip (mm)','UPPER tons','UPPER PE %','LOWER tons','TOTAL tons','SSY data source','TOTAL PE %','% UPPER','% LOWER']]

    return S_diff
S_storm_diff_table()

def SSY_dist_table(subset='pre'):
    S_diff = compileALLStorms(subset)
    ## Calculate percent contributions from upper and lower watersheds
    S_diff['UPPER tons']=S_diff['Supper'].round(2)
    #S_diff['UPPER SSY data source'] = S_diff['SSY_data_source_upper']
    S_diff['UPPER PE %'] = S_diff['Supper_PE'].apply(int)
    S_diff['LOWER tons']=S_diff['Slower'].round(2)
    S_diff['TOTAL tons']=S_diff['Stotal'].round(2)
    #S_diff['TOTAL SSY data source'] = S_diff['SSY_data_source_total']
    S_diff['SSY data source'] = S_diff['SSY_data_source_total']
    S_diff['TOTAL PE %'] = S_diff['Stotal_PE'].apply(int)
    S_diff['% UPPER'] = S_diff['Supper']/S_diff['Stotal']*100
    S_diff['% UPPER'] = S_diff['% UPPER'].dropna().apply(int)
    S_diff['% LOWER'] = S_diff['Slower']/S_diff['Stotal']*100
    S_diff['% LOWER'] = S_diff['% LOWER'].dropna().apply(int)
    S_diff['Precip (mm)'] = S_diff['Pstorms'].apply(int)
    S_diff = S_diff[S_diff['Precip (mm)']>0]
    ## Filter negative values for S at LBJ    
    S_diff = S_diff[S_diff['Slower']>0]
    ## Storm Indices
    S_diff['Storm#']=range(1,len(S_diff)+1) 
    S_diff['Storm Start'] = S_diff.index
    S_diff['Storm Start'] =S_diff['Storm Start'].apply(lambda x: "{:%m/%d/%Y}".format(x))
    ## summary stats
    Percent_Upper = S_diff['Supper'].sum()/S_diff['Stotal'].sum()*100
    Percent_Lower = S_diff['Slower'].sum()/S_diff['Stotal'].sum()*100    
    ## add summary stats to bottom of table
    # Total/Avg
    SSY_UPPER, SSY_LOWER, SSY_TOTAL = S_diff['UPPER tons'].sum(), S_diff['LOWER tons'].sum(), S_diff['TOTAL tons'].sum()
    # sSSY
    sSSY_UPPER, sSSY_LOWER, sSSY_TOTAL = SSY_UPPER/0.9, SSY_LOWER/0.88, SSY_TOTAL/1.78
    
    
    # fraction Disturbed = % disturbed from % Disturbed in Land cover table
    lc_table = LandCover_table()
    frac_disturbed_UPPER, frac_disturbed_LOWER, frac_disturbed_TOTAL= lc_table.ix[0]['% Disturbed'], lc_table.ix[3]['% Disturbed'],lc_table.ix[4]['% Disturbed']
    
    SSY_dist = pd.DataFrame({' ':'fraction disturbed (%)', 'UPPER':"%.1f"%frac_disturbed_UPPER, 'LOWER':"%.1f"%frac_disturbed_LOWER,'TOTAL':"%.1f"%frac_disturbed_TOTAL},index=['fraction disturbed (%)']) 
    
    # SSY from forested areas of subwatersheds = SSY forest (tons) =  sSSY_UPPER x (1-disturbed_fraction) x subwatershed area
    def SSY_from_forest(sSSY_UPPER,disturbed_fraction,subwatershed_area):
        disturbed_fraction= disturbed_fraction/100
        SSY_forest = sSSY_UPPER*(1-disturbed_fraction)*subwatershed_area
        return SSY_forest
    SSY_forest_UPPER,SSY_forest_LOWER,SSY_forest_TOTAL = SSY_from_forest(sSSY_UPPER,frac_disturbed_UPPER,0.9),SSY_from_forest(sSSY_UPPER,frac_disturbed_LOWER,0.88),          SSY_from_forest(sSSY_UPPER,frac_disturbed_TOTAL,1.78)
    
    SSY_dist = SSY_dist.append(pd.DataFrame({' ':'SSY from forested areas (tons)', 'UPPER':"%.1f"%SSY_forest_UPPER,'LOWER':"%.1f"%SSY_forest_LOWER,'TOTAL':"%.1f"%SSY_forest_TOTAL}, index=['SSY from forested areas (tons)']))
    
    # SSY from disturbed areas
    SSY_disturbed_UPPER, SSY_disturbed_LOWER,SSY_disturbed_TOTAL = SSY_UPPER-SSY_forest_UPPER, SSY_LOWER-SSY_forest_LOWER, SSY_TOTAL-SSY_forest_TOTAL
    
    SSY_dist = SSY_dist.append(pd.DataFrame({' ':'SSY from disturbed areas (tons)','UPPER':"%.1f"%SSY_disturbed_UPPER,'LOWER':"%.1f"%SSY_disturbed_LOWER,'TOTAL':"%.1f"%SSY_disturbed_TOTAL}, index=['SSY from disturbed areas (tons)']))
    
    # % from disturbed parts of waterhshed
    SSY_percent_dist_UPPER, SSY_percent_dist_LOWER, SSY_percent_dist_TOTAL = SSY_disturbed_UPPER/SSY_UPPER*100, SSY_disturbed_LOWER/SSY_LOWER*100, SSY_disturbed_TOTAL/SSY_TOTAL*100
    
    SSY_dist = SSY_dist.append(pd.DataFrame({' ':'% SSY from disturbed areas','UPPER':"%0.1f"%SSY_percent_dist_UPPER,'LOWER':"%.0f"%SSY_percent_dist_LOWER,'TOTAL':"%.0f"%SSY_percent_dist_TOTAL}, index=['% SSY from disturbed areas']))  
    
    # sSSY from disturbed areas = SSY_disturbed/(fraction_disturbed x subwatershed area)
    sSSY_disturbed_UPPER, sSSY_disturbed_LOWER, sSSY_disturbed_TOTAL = SSY_disturbed_UPPER/(frac_disturbed_UPPER/100*0.9), SSY_disturbed_LOWER/(frac_disturbed_LOWER/100*0.88), SSY_disturbed_TOTAL/(frac_disturbed_TOTAL/100*1.78)
    
    SSY_dist = SSY_dist.append(pd.DataFrame({' ':'sSSY from disturbed areas (tons/km2)','UPPER':"%.1f"%sSSY_disturbed_UPPER,'LOWER':"%.1f"%sSSY_disturbed_LOWER,'TOTAL':"%.1f"%sSSY_disturbed_TOTAL}, index=['sSSY from disturbed areas (tons/km2)']))      
    
    # sSSY_DR
    sSSY_DR_LOWER, sSSY_DR_TOTAL= sSSY_disturbed_LOWER/sSSY_UPPER, sSSY_disturbed_TOTAL/sSSY_UPPER
    
    SSY_dist = SSY_dist.append(pd.DataFrame({' ':'DR for sSSY from disturbed areas','UPPER':'-','LOWER':"%.0f"%sSSY_DR_LOWER,'TOTAL':"%.0f"%sSSY_DR_TOTAL}, index=['DR for sSSY from disturbed areas']))     
    
    LOWER_percent_of_TOTAL_SSY = SSY_disturbed_LOWER/SSY_TOTAL * 100
    TOTAL_percent_of_TOTAL_SSY = (SSY_disturbed_TOTAL)/SSY_TOTAL * 100
      
    ## Order columns
    SSY_dist = SSY_dist[[' ','UPPER','LOWER','TOTAL']]
    return SSY_dist, "%.0f"%LOWER_percent_of_TOTAL_SSY, "%.0f"%TOTAL_percent_of_TOTAL_SSY
SSY_dist_table()



def S_storm_diff_table_quarry(subset='pre',manual_edit=True):
    S_diff = compileALLStorms(subset)
    ## Calculate percent contributions from upper and lower watersheds
    S_diff['TOTAL tons']=S_diff['Stotal'].round(2)
    S_diff['UPPER tons']=S_diff['Supper'].round(2)
    #S_diff['FOREST PE %'] = S_diff['Supper_PE'].apply(int)
    S_diff['LOWER_QUARRY tons']=S_diff['Squarry'].round(2) - S_diff['UPPER tons']
    S_diff['LOWER_VILLAGE tons']= S_diff['TOTAL tons'].round(2) - S_diff['UPPER tons'] - S_diff['LOWER_QUARRY tons'] 
    #S_diff['TOTAL PE %'] = S_diff['Stotal_PE'].apply(int)
    S_diff['% UPPER'] = S_diff['UPPER tons']/S_diff['TOTAL tons']*100
    S_diff['% UPPER'] = S_diff['% UPPER'].dropna().apply(int)
    S_diff['% LOWER_QUARRY'] = S_diff['LOWER_QUARRY tons']/S_diff['TOTAL tons']*100
    S_diff['% LOWER_QUARRY'] = S_diff['% LOWER_QUARRY'].dropna().apply(int)    
    S_diff['% LOWER_VILLAGE'] = S_diff['LOWER_VILLAGE tons']/S_diff['TOTAL tons']*100
    S_diff['% LOWER_VILLAGE'] = S_diff['% LOWER_VILLAGE'].dropna().apply(int)
    S_diff['Precip (mm)'] = S_diff['Pstorms'].apply(int)
    S_diff = S_diff[S_diff['Precip (mm)']>0]
    ## Filter negative values for S at LBJ    
    S_diff = S_diff[S_diff['LOWER_VILLAGE tons']>0]
    S_diff['Storm#']=range(1,len(S_diff)+1) 
    S_diff['Storm Start'] = S_diff.index
    S_diff['Storm Start'] =S_diff['Storm Start'].apply(lambda x: "{:%m/%d/%Y}".format(x))
    ## Select storms with valid data
    if manual_edit == True:
        S_diff = S_diff[S_diff['Storm Start'].isin(['03/06/2013','04/16/2013','04/23/2013','04/30/2013','06/05/2013','02/14/2014','02/20/2014','02/21/2014'])==True]
    ## Summary Stats    
    Percent_Forest = S_diff['UPPER tons'].sum()/S_diff['TOTAL tons'].sum()*100
    Percent_Quarry= S_diff['LOWER_QUARRY tons'].sum()/S_diff['TOTAL tons'].sum()*100
    Percent_Village = S_diff['LOWER_VILLAGE tons'].sum()/S_diff['TOTAL tons'].sum()*100

    ## add summary stats to bottom of table
    # Total/Avg
    SSY_UPPER, SSY_QUARRY, SSY_VILLAGE, SSY_TOTAL = S_diff['UPPER tons'].sum(), S_diff['LOWER_QUARRY tons'].sum(), S_diff['LOWER_VILLAGE tons'].sum(), S_diff['TOTAL tons'].sum()
    S_diff=S_diff.append(pd.DataFrame({'Storm Start':'Total/Avg:','Storm#':"%.0f"%len(S_diff),'Precip (mm)':"%.0f"%S_diff['Precip (mm)'].sum(),'UPPER tons':"%.0f"%SSY_UPPER,'LOWER_QUARRY tons':"%.0f"%SSY_QUARRY,'LOWER_VILLAGE tons':"%.0f"%SSY_VILLAGE,'TOTAL tons':"%.0f"%SSY_TOTAL,'% UPPER':"%.0f"%Percent_Forest,'% LOWER_QUARRY':"%.0f"%Percent_Quarry,'% LOWER_VILLAGE':"%.0f"%Percent_Village},index=['Total/Avg:']))
    
    # sSSY
    sSSY_UPPER, sSSY_QUARRY, sSSY_VILLAGE, sSSY_TOTAL = SSY_UPPER/0.9, SSY_QUARRY/0.27, SSY_VILLAGE/0.61, SSY_TOTAL/1.78
    S_diff=S_diff.append(pd.DataFrame({'Storm Start':'Tons/km2','Storm#':'','Precip (mm)':'','UPPER tons':"%.0f"%sSSY_UPPER,'LOWER_QUARRY tons':"%.0f"%sSSY_QUARRY,'LOWER_VILLAGE tons':"%.0f"%sSSY_VILLAGE,'TOTAL tons':"%.0f"%sSSY_TOTAL,'% UPPER':'-','% LOWER_QUARRY':'-','% LOWER_VILLAGE':'-'}, index=['Tons/km2']))
    
    # sSSY:sSSY_UPPER
    DR_sSSY_UPPER, DR_sSSY_QUARRY, DR_sSSY_VILLAGE, DR_sSSY_TOTAL = sSSY_UPPER/sSSY_UPPER,sSSY_QUARRY/sSSY_UPPER,sSSY_VILLAGE/sSSY_UPPER,sSSY_TOTAL/sSSY_UPPER
    S_diff=S_diff.append(pd.DataFrame({'Storm Start':'DR','Storm#':'','Precip (mm)':'','UPPER tons':"%.1f"%DR_sSSY_UPPER,'LOWER_QUARRY tons':"%.2f"%DR_sSSY_QUARRY,'LOWER_VILLAGE tons':"%.1f"%DR_sSSY_VILLAGE,'TOTAL tons':"%.1f"%DR_sSSY_TOTAL,'% UPPER':'-','% LOWER_QUARRY':'-','% LOWER_VILLAGE':'-'}, index=['DR']))
    
    # Order columns    
    S_diff=S_diff[['Storm Start','Storm#','Precip (mm)','UPPER tons','LOWER_QUARRY tons','LOWER_VILLAGE tons','TOTAL tons','% UPPER','% LOWER_QUARRY','% LOWER_VILLAGE']]
    return S_diff #, "%.0f"%QUARRY_percent_of_TOTAL_SSY, "%.0f"%VILLAGE_percent_of_TOTAL_SSY, "%.0f"%QUA_VIL_percent_of_TOTAL_SSY
    
#S_storm_diff_table_quarry(manual_edit=False)
#S_storm_diff_table_quarry(manual_edit=True)
    
def SSY_dist_table_quarry(subset='pre',manual_edit=True):
    S_diff = compileALLStorms(subset)
    ## Calculate percent contributions from upper and lower watersheds
    S_diff['TOTAL tons']=S_diff['Stotal'].round(2)
    S_diff['UPPER tons']=S_diff['Supper'].round(2)
    #S_diff['FOREST PE %'] = S_diff['Supper_PE'].apply(int)
    S_diff['LOWER_QUARRY tons']=S_diff['Squarry'].round(2) - S_diff['UPPER tons']
    S_diff['LOWER_VILLAGE tons']= S_diff['TOTAL tons'].round(2) - S_diff['UPPER tons'] - S_diff['LOWER_QUARRY tons'] 
    #S_diff['TOTAL PE %'] = S_diff['Stotal_PE'].apply(int)
    S_diff['% UPPER'] = S_diff['UPPER tons']/S_diff['TOTAL tons']*100
    S_diff['% UPPER'] = S_diff['% UPPER'].dropna().apply(int)
    S_diff['% LOWER_QUARRY'] = S_diff['LOWER_QUARRY tons']/S_diff['TOTAL tons']*100
    S_diff['% LOWER_QUARRY'] = S_diff['% LOWER_QUARRY'].dropna().apply(int)    
    S_diff['% LOWER_VILLAGE'] = S_diff['LOWER_VILLAGE tons']/S_diff['TOTAL tons']*100
    S_diff['% LOWER_VILLAGE'] = S_diff['% LOWER_VILLAGE'].dropna().apply(int)
    S_diff['Precip (mm)'] = S_diff['Pstorms'].apply(int)
    S_diff = S_diff[S_diff['Precip (mm)']>0]
    ## Filter negative values for S at LBJ    
    S_diff = S_diff[S_diff['LOWER_VILLAGE tons']>0]
    S_diff['Storm#']=range(1,len(S_diff)+1) 
    S_diff['Storm Start'] = S_diff.index
    S_diff['Storm Start'] =S_diff['Storm Start'].apply(lambda x: "{:%m/%d/%Y}".format(x))
    ## Select storms with valid data
    if manual_edit == True:
        S_diff = S_diff[S_diff['Storm Start'].isin(['03/06/2013','04/16/2013','04/23/2013','04/30/2013','06/05/2013','02/14/2014','02/20/2014','02/21/2014'])==True]
    ## Summary Stats    
    Percent_Forest = S_diff['UPPER tons'].sum()/S_diff['TOTAL tons'].sum()*100
    Percent_Quarry= S_diff['LOWER_QUARRY tons'].sum()/S_diff['TOTAL tons'].sum()*100
    Percent_Village = S_diff['LOWER_VILLAGE tons'].sum()/S_diff['TOTAL tons'].sum()*100

    ## add summary stats to bottom of table
    # Total/Avg
    SSY_UPPER, SSY_QUARRY, SSY_VILLAGE, SSY_TOTAL = S_diff['UPPER tons'].sum(), S_diff['LOWER_QUARRY tons'].sum(), S_diff['LOWER_VILLAGE tons'].sum(), S_diff['TOTAL tons'].sum()

    # sSSY
    sSSY_UPPER, sSSY_QUARRY, sSSY_VILLAGE, sSSY_TOTAL = SSY_UPPER/0.9, SSY_QUARRY/0.27, SSY_VILLAGE/0.61, SSY_TOTAL/1.78
    
    # sSSY:sSSY_UPPER
    DR_sSSY_UPPER, DR_sSSY_QUARRY, DR_sSSY_VILLAGE, DR_sSSY_TOTAL = sSSY_UPPER/sSSY_UPPER,sSSY_QUARRY/sSSY_UPPER,sSSY_VILLAGE/sSSY_UPPER,sSSY_TOTAL/sSSY_UPPER
    
    # fraction Disturbed = % disturbed from % Disturbed in Land cover table
    lc_table = LandCover_table()
    frac_disturbed_UPPER, frac_disturbed_LOWER_QUARRY, frac_disturbed_LOWER_VILLAGE, frac_disturbed_TOTAL= lc_table.ix[0]['% Disturbed'], lc_table.ix[1]['% Disturbed'], lc_table.ix[2]['% Disturbed'],lc_table.ix[4]['% Disturbed']
    
    SSY_dist = pd.DataFrame({' ':'fraction disturbed (%)','UPPER':"%.1f"%frac_disturbed_UPPER,'LOWER_QUARRY':"%.1f"%frac_disturbed_LOWER_QUARRY,'LOWER_VILLAGE':"%.1f"%frac_disturbed_LOWER_VILLAGE,'TOTAL':"%.1f"%frac_disturbed_TOTAL}, index=['fraction disturbed (%)'])
    
    # SSY from forested areas of subwatersheds = SSY forest (tons) =  sSSY_UPPER x (1-disturbed_fraction) x subwatershed area
    def SSY_from_forest(sSSY_UPPER,disturbed_fraction,subwatershed_area):
        disturbed_fraction= disturbed_fraction/100
        SSY_forest = sSSY_UPPER*(1-disturbed_fraction)*subwatershed_area
        return SSY_forest
    SSY_forest_UPPER,SSY_forest_QUARRY,SSY_forest_VILLAGE, SSY_forest_TOTAL = SSY_from_forest(sSSY_UPPER,frac_disturbed_UPPER,0.9), SSY_from_forest(sSSY_UPPER,frac_disturbed_LOWER_QUARRY,0.27), SSY_from_forest(sSSY_UPPER,frac_disturbed_LOWER_VILLAGE,0.61), SSY_from_forest(sSSY_UPPER,frac_disturbed_TOTAL,1.78)
    
    SSY_dist = SSY_dist.append(pd.DataFrame({' ':'SSY from forested areas (tons)','UPPER':"%.1f"%SSY_forest_UPPER,'LOWER_QUARRY':"%.1f"%SSY_forest_QUARRY,'LOWER_VILLAGE':"%.1f"%SSY_forest_VILLAGE,'TOTAL':"%.1f"%SSY_forest_TOTAL}, index=['SSY from forested areas (tons)']))
    
    # SSY from disturbed areas
    SSY_disturbed_UPPER, SSY_disturbed_QUARRY,SSY_disturbed_VILLAGE,SSY_disturbed_TOTAL = SSY_UPPER-SSY_forest_UPPER, SSY_QUARRY-SSY_forest_QUARRY,SSY_VILLAGE-SSY_forest_VILLAGE, SSY_TOTAL-SSY_forest_TOTAL
    
    SSY_dist = SSY_dist.append(pd.DataFrame({' ':'SSY from disturbed areas (tons)','UPPER':"%.1f"%SSY_disturbed_UPPER,'LOWER_QUARRY':"%.2f"%SSY_disturbed_QUARRY,'LOWER_VILLAGE':"%.1f"%SSY_disturbed_VILLAGE,'TOTAL':"%.1f"%SSY_disturbed_TOTAL}, index=['SSY from disturbed areas (tons)']))
      
    # % from disturbed parts of watershed
    SSY_percent_dist_UPPER, SSY_percent_dist_QUARRY, SSY_percent_dist_VILLAGE, SSY_percent_dist_TOTAL = SSY_disturbed_UPPER/SSY_UPPER*100, SSY_disturbed_QUARRY/SSY_QUARRY*100, SSY_disturbed_VILLAGE/SSY_VILLAGE*100, SSY_disturbed_TOTAL/SSY_TOTAL*100
    
    SSY_dist = SSY_dist.append(pd.DataFrame({' ':'% SSY from disturbed areas','UPPER':"%.1f"%SSY_percent_dist_UPPER,'LOWER_QUARRY':"%.0f"%SSY_percent_dist_QUARRY,'LOWER_VILLAGE':"%.0f"%SSY_percent_dist_VILLAGE,'TOTAL':"%.0f"%SSY_percent_dist_TOTAL}, index=['% SSY from disturbed areas']))  
    
    # sSSY from disturbed areas = SSY_disturbed/(fraction_disturbed x subwatershed area)
    sSSY_disturbed_UPPER, sSSY_disturbed_QUARRY, sSSY_disturbed_VILLAGE, sSSY_disturbed_TOTAL = SSY_disturbed_UPPER/(frac_disturbed_UPPER/100*0.9), SSY_disturbed_QUARRY/(frac_disturbed_LOWER_QUARRY/100*0.27), SSY_disturbed_VILLAGE/(frac_disturbed_LOWER_VILLAGE/100*0.61), SSY_disturbed_TOTAL/(frac_disturbed_TOTAL/100*1.78)
    
    SSY_dist = SSY_dist.append(pd.DataFrame({' ':'sSSY from disturbed areas (tons/km2)','UPPER':"%.1f"%sSSY_disturbed_UPPER,'LOWER_QUARRY':"%.1f"%sSSY_disturbed_QUARRY,'LOWER_VILLAGE':"%.1f"%sSSY_disturbed_VILLAGE,'TOTAL':"%.1f"%sSSY_disturbed_TOTAL}, index=['sSSY from disturbed areas (tons/km2)']))        
 
    # sSSY_DR
    sSSY_DR_QUARRY, sSSY_DR_VILLAGE, sSSY_DR_TOTAL= sSSY_disturbed_QUARRY/sSSY_UPPER, sSSY_disturbed_VILLAGE/sSSY_UPPER, sSSY_disturbed_TOTAL/sSSY_UPPER
    
    SSY_dist = SSY_dist.append(pd.DataFrame({' ':'DR for sSSY from disturbed areas','UPPER':'','LOWER_QUARRY':"%.1f"%sSSY_DR_QUARRY,'LOWER_VILLAGE':"%.1f"%sSSY_DR_VILLAGE,'TOTAL':"%.1f"%sSSY_DR_TOTAL}, index=['DR for sSSY from disturbed areas']))     
    
    QUARRY_percent_of_TOTAL_SSY = SSY_disturbed_QUARRY/SSY_TOTAL * 100
    VILLAGE_percent_of_TOTAL_SSY = SSY_disturbed_VILLAGE/SSY_TOTAL * 100
    QUA_VIL_percent_of_TOTAL_SSY = (SSY_disturbed_QUARRY+SSY_disturbed_VILLAGE)/SSY_TOTAL * 100
    
    # Order columns    
    SSY_dist = SSY_dist[[' ','UPPER','LOWER_QUARRY','LOWER_VILLAGE','TOTAL']]
    return SSY_dist, "%.0f"%QUARRY_percent_of_TOTAL_SSY, "%.0f"%VILLAGE_percent_of_TOTAL_SSY, "%.0f"%QUA_VIL_percent_of_TOTAL_SSY
#SSY_dist_table_quarry(manual_edit=False)
SSY_dist_table_quarry(manual_edit=True)

## Calculate the percent of total SSY with raw vales, BEFORE NORMALIZING by area!
def plotS_storm_table(show=False):
    diff = compileALLStorms()
    diff = diff[diff['Stotal']>0]
    diff = diff[diff['Supper']>0]
    ## Calculate percent contributions from upper and lower watersheds
    diff['Supper']=diff['Supper'].round(3)
    diff['Slower']=diff['Slower'].round(3)
    diff['Stotal']=diff['Stotal'].round(3)
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
    diff.to_excel(datadir+'Storm S table.xlsx')
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
    
def Q_S_storm_diff_summary_table(subset='pre'):
    diff = compileALLStorms(subset)
    ## Calculate percent contributions from upper and lower watersheds
    
    # Precip
    diff['Psum'] = diff['Pstorms'].apply(int)
    diff = diff[diff['Psum']>0]
    ## Q discharge
    diff['QupperMCM'] = diff['Qsumupper']/10.**6.
    diff['QtotalMCM'] = diff['Qsumtotal']/10.**6.    
     ## Q vol (m3) -> Q mm = Qvol(m3)/Watershed area(m2) * 1000mm/m
    diff['mmQupper']=diff['Qsumupper']/900000*1000
    diff['mmQtotal']=diff['Qsumtotal']/1780000*1000
    ## Sediment
    diff['Supper']=diff['Supper'].round(3)
    diff['Stotal']=diff['Stotal'].round(3)
    ## SSY Norm by Area
    diff['km2Supper'] = diff['Supper']/.9
    diff['km2Stotal'] = diff['Stotal']/1.78
    ## Filter negative values for S at LBJ (and getting rid of NaNs)    
    diff = diff[diff['Slower']>0]  
    ## Number Storms
    diff['Storm#']=range(1,len(diff)+1)  
    ## Disturbance Ratio
    SSYpre = 1.78 * diff['km2Supper'].sum()
    SSY = diff['Stotal'].sum()
    SSY_DR = SSY/SSYpre
    ## Q Disturbance Ratio
    Qpre = 1.78 * (diff['QupperMCM'].sum()/.9)
    Q = diff['QtotalMCM'].sum()
    Q_DR = Q/Qpre   

    ## Summarize
    table_data_dict = {
    'Storms':(len(diff),''),
    'Precipitation (mm)':('%.0f'%diff['Pstorms'].sum(),''),
    'subwatershed':('UPPER','LOWER'),
    'Q (MCM)':('%.2f'%diff['QupperMCM'].sum(),'%.2f'%diff['QtotalMCM'].sum()),
    'Q (mm)':('%.0f'%diff['mmQupper'].sum(),'%.0f'%diff['mmQtotal'].sum()),
    'Q Disturbance Ratio':('-','%.1f'%Q_DR),
    'SSY (Mg)':('%.1f'%diff['Supper'].sum(),'%.1f'%diff['Stotal'].sum()),
    'Spec SSY (Mg/km2)':('%.1f'%diff['km2Supper'].sum(),'%.1f'%diff['km2Stotal'].sum()),
    'SSY Disturbance Ratio':('-','%.1f'%SSY_DR)}
    
    summary =pd.DataFrame(table_data_dict,index=[str(n) for n in range(1,3)])[['Storms','Precipitation (mm)','subwatershed','Q (MCM)','Q (mm)','Q Disturbance Ratio','SSY (Mg)','Spec SSY (Mg/km2)','SSY Disturbance Ratio']].T
    summary['0'] = summary.index
    return summary[['0','1', '2']]
Q_S_storm_diff_summary_table()

def Spec_SSY_Quarry(subset='post'):
    diff = compileALLStorms(subset)

    diff['QUARRY tons']=diff['Squarry'].round(3) - diff['Supper'].round(3)
    diff['km2SQUARRY'] = diff['QUARRY tons']/.27 #km2
    diff = diff[diff['QUARRY tons']>0]
    diff['km2SUPPER'] =  diff['Supper'].round(3)/.9 #km2
    percent_increase  = diff['km2SQUARRY'].sum()/diff['km2SUPPER'].sum() *100
    return '%.1f'%diff['km2SUPPER'].sum()+r'Mg/km^2', '%.1f'%diff['km2SQUARRY'].sum()+r'Mg/km2', "%.0f"%percent_increase
#Spec_SSY_Quarry()    

def plotS_storm_table_summary(fs=16,show=False):
    diff = compileALLStorms().dropna()
    ## Calculate percent contributions from upper and lower watersheds
    ## Sediment
    diff['Supper']=diff['Supper'].round(3)
    diff['Slower']=diff['Slower'].round(3)
    diff['Stotal']=diff['Stotal'].round(3)
    diff['% Upper'] = diff['Supper']/diff['Stotal']*100
    diff['% Upper'] = diff['% Upper'].apply(np.int)
    diff['% Lower'] = diff['Slower']/diff['Stotal']*100
    diff['% Lower'] = diff['% Lower'].apply(np.int)
    ## Q discharge
    diff['Qupper']=diff['Qsumupper'].round(3)
    diff['Qlower']=diff['Qsumlower'].round(3)
    diff['Qtotal']=diff['Qsumtotal'].round(3)
    
    diff['Psum'] = diff['Pstorms'].apply(int)
    diff['Storm#']=range(1,len(diff)+1) 
    ## Filter negative values for S at LBJ    
    diff = diff[diff['Slower']>0]
    ## add summary stats to bottom of table
    diff=pd.DataFrame({'Storm#':len(diff),'Psum':diff['Pstorms'].sum(),
    'Qupper':diff['Qupper'].sum(),'Qlower':diff['Qlower'].sum(),'Qtotal':diff['Qtotal'].sum(),
    'Supper':diff['Supper'].sum(),'Slower':diff['Slower'].sum(),
    'Stotal':diff['Stotal'].sum(),'% Upper':'%.1f'%diff['% Upper'].mean(),
    '% Lower':'%.1f'%diff['% Lower'].mean()},index=[pd.NaT])
    ## Q vol (m3) -> Q mm = Qvol(m3)/Watershed area(m2) * 1000mm/m
    diff['mmQupper']=diff['Qupper']/900000*1000
    diff['mmQlower']=diff['Qlower']/880000*1000
    diff['mmQtotal']=diff['Qtotal']/1780000*1000
    diff.to_excel(datadir+'S storm table summary.xlsx')
    ## BUild table
    nrows, ncols = len(diff),len(diff.columns)
    hcell, wcell=0.3,1
    hpad, wpad = .5,.3
    fig = plt.figure(figsize=(ncols*wcell+wpad,nrows*hcell+hpad)) 
    ax = fig.add_subplot(111)
    ax.patch.set_visible(False), ax.axis('off')
    ax.xaxis.set_visible(False), ax.yaxis.set_visible(False)
    plt.suptitle("Sediment Loading from subwatersheds in Faga'alu",fontsize=16)
 
    celldata = np.array(diff[['Storm#','Psum','Qupper','Qlower','Qtotal',
    'mmQupper','mmQlower','mmQtotal',
    'Supper','Slower','Stotal','% Upper','% Lower']].values)
    rowlabels=[pd.to_datetime(t).strftime('%Y %b %d %H:%M') for t in diff.index[diff.index!=pd.NaT].values]
    rowlabels.extend([None])
    the_table=ax.table(cellText=celldata,rowLabels=rowlabels,colLabels=['Storms','Precip(mm)',
    'Q For(m3)','Q For-Vil (m3)','Q Vil(m3)','Q For(mm)','Q For-Vil (mm)','Q Vil(mm)','Upper (Mg)','Lower (Mg)','Total (Mg)','%Upper','%Lower'],loc='center')
    the_table.set_fontsize(fs)
    the_table.scale(1.5, 1.5)
    show_plot(show)
    return
#plotS_storm_table_summary(fs=22,show=True)

def NormalizeSSYbyCatchmentArea(ALLStorms):
    ## DAM = 0.9 km2
    ## QUARRY = 1.17 km2
    ## LBJ = 1.78 km2
    ## Normalize Sediment Load by catchment area (Duvert 2012)
    ALLStorms['Supper']=ALLStorms['Supper']/.9
    ALLStorms['Slower']=ALLStorms['Slower']/.88
    ALLStorms['Stotal']=ALLStorms['Stotal']/1.78
    ## Add Event Discharge ad Normalize by catchment area
    ALLStorms['Qsumlower']=ALLStorms['Qsumtotal']-ALLStorms['Qsumupper']
    ALLStorms['Qsumlower']=ALLStorms['Qsumlower']/.88
    ALLStorms['Qsumupper']=ALLStorms['Qsumupper']/.9 
    ALLStorms['Qsumtotal']=ALLStorms['Qsumtotal']/1.78
    ## Duvert (2012) Fig. 3 shows SSY (Qmax m3/s/km2 vs. Mg/km2); but shows correlation coefficients in Qmax m3/s vs SSY Mg (table )
    ALLStorms['Qmaxupper']=ALLStorms['Qmaxupper']/.9
    ALLStorms['Qmaxlower']=ALLStorms['Qmaxtotal']/.88
    ALLStorms['Qmaxtotal']=ALLStorms['Qmaxtotal']/1.78
    ## Add Event Precipitation and EI
    ALLStorms['Pstorms']=Pstorms_LBJ['Psum'] ## Add Event Precip
    ALLStorms['EI'] = LBJ_Stormdf['EI'][LBJ_Stormdf['EI']>1] ## Add Event Erosion Index
    return ALLStorms
    
def Pearson_r_Table(pvalue=0.05):
    ALLStorms = compileALLStorms()
    Upper = ALLStorms[['Pstorms','EI','Qsumupper','Qmaxupper','Supper','Supper_PE']].dropna()
    Lower = ALLStorms[['Pstorms','EI','Qsumlower','Qmaxlower','Slower']].dropna()
    Total = ALLStorms[['Pstorms','EI','Qsumtotal','Qmaxtotal','Stotal','Stotal_PE']].dropna()
    ## Psum vs. Ssum
    if pearson_r(Upper['Pstorms'],Upper['Supper'])[1] < pvalue:
        Upper_Psum_Ssum_Pearson_r = '%.2f'%pearson_r(Upper['Pstorms'],Upper['Supper'])[0]
    if pearson_r(Lower['Pstorms'],Lower['Slower'])[1] < pvalue:
        Lower_Psum_Ssum_Pearson_r = '%.2f'%pearson_r(Lower['Pstorms'],Lower['Slower'])[0]
    if pearson_r(Total['Pstorms'],Total['Stotal'])[1] < pvalue:
        Total_Psum_Ssum_Pearson_r = '%.2f'%pearson_r(Total['Pstorms'],Total['Stotal'])[0]      
    ## EI vs. Ssum
    if pearson_r(Upper['EI'],Upper['Supper'])[1] < pvalue:
        Upper_EI_Ssum_Pearson_r = '%.2f'%pearson_r(Upper['EI'],Upper['Supper'])[0]
    elif pearson_r(Upper['EI'],Upper['Supper'])[1] >= pvalue:
        Upper_EI_Ssum_Pearson_r = ' ' 
    if pearson_r(Lower['EI'],Lower['Slower'])[1] < pvalue:
        Lower_EI_Ssum_Pearson_r = '%.2f'%pearson_r(Lower['EI'],Lower['Slower'])[0]
    elif pearson_r(Lower['EI'],Lower['Slower'])[1] >= pvalue:
        Lower_EI_Ssum_Pearson_r = ' ' 
    if pearson_r(Total['EI'],Total['Stotal'])[1] < pvalue:
        Total_EI_Ssum_Pearson_r = '%.2f'%pearson_r(Total['EI'],Total['Stotal'])[0]
    elif pearson_r(Total['EI'],Total['Stotal'])[1] >= pvalue:
        Total_EI_Ssum_Pearson_r = ' ' 
    ## Qsum vs. Ssum
    if pearson_r(Upper['Qsumupper'],Upper['Supper'])[1] < pvalue:
        Upper_Qsum_Ssum_Pearson_r = '%.2f'%pearson_r(Upper['Qsumupper'],Upper['Supper'])[0]
    if pearson_r(Lower['Qsumlower'],Lower['Slower'])[1] < pvalue:
        Lower_Qsum_Ssum_Pearson_r = '%.2f'%pearson_r(Lower['Qsumlower'],Lower['Slower'])[0]
    elif pearson_r(Lower['Qsumlower'],Lower['Slower'])[1]>=pvalue:
        Lower_Qsum_Ssum_Pearson_r = ' '
    if pearson_r(Total['Qsumtotal'],Total['Stotal'])[1] < pvalue:
        Total_Qsum_Ssum_Pearson_r = '%.2f'%pearson_r(Total['Qsumtotal'],Total['Stotal'])[0]
    elif pearson_r(Total['Qsumtotal'],Total['Stotal'])[1] >= pvalue:
        Total_Qsum_Ssum_Pearson_r =' '
    ## Qmaxvs. Ssum
    if pearson_r(Upper['Qmaxupper'],Upper['Supper'])[1] < pvalue:
        Upper_Qmax_Ssum_Pearson_r = '%.2f'%pearson_r(Upper['Qmaxupper'],Upper['Supper'])[0]
    if pearson_r(Lower['Qmaxlower'],Lower['Slower'])[1] < pvalue:
        Lower_Qmax_Ssum_Pearson_r = '%.2f'%pearson_r(Lower['Qmaxlower'],Lower['Slower'])[0]
    if pearson_r(Total['Qmaxtotal'],Total['Stotal'])[1] < pvalue:
        Total_Qmax_Ssum_Pearson_r = '%.2f'%pearson_r(Total['Qmaxtotal'],Total['Stotal'])[0]
    ## Put data together, and put in table
    table_data_dict = {'FOREST':[Upper_Psum_Ssum_Pearson_r,Upper_EI_Ssum_Pearson_r,Upper_Qsum_Ssum_Pearson_r,Upper_Qmax_Ssum_Pearson_r],
    'VILLAGE-FOREST':[Lower_Psum_Ssum_Pearson_r,Lower_EI_Ssum_Pearson_r,Lower_Qsum_Ssum_Pearson_r,Lower_Qmax_Ssum_Pearson_r],
    'VILLAGE':[Total_Psum_Ssum_Pearson_r,Total_EI_Ssum_Pearson_r,Total_Qsum_Ssum_Pearson_r,Total_Qmax_Ssum_Pearson_r]} ## Put data in a dictionary to convert to DataFrame
    summary =pd.DataFrame(table_data_dict,index=['Precip','EI','Qsum','Qmax'])[['FOREST','VILLAGE-FOREST','VILLAGE']]
    summary['']= summary.index
    summary = summary[['','FOREST','VILLAGE-FOREST','VILLAGE']]
    return summary
#Pearson_r_Table(pvalue=0.05)

def plotPearsonTable(pvalue=0.05,show=False):
    nrows, ncols = 3,4
    hcell, wcell=0.3,1
    hpad, wpad = 1,1
    fig = plt.figure(figsize=(ncols*wcell+wpad,nrows*hcell+hpad)) 
    pearson = fig.add_subplot(111)
    pearson.patch.set_visible(False), pearson.axis('off')
    pearson.xaxis.set_visible(False), pearson.yaxis.set_visible(False) 
  
    ALLStorms = compileALLStorms()
    Upper = ALLStorms[['Pstorms','EI','Qsumupper','Qmaxupper','Supper','Supper_PE']].dropna()
    Lower = ALLStorms[['Pstorms','EI','Qsumlower','Qmaxlower','Slower']].dropna()
    Total = ALLStorms[['Pstorms','EI','Qsumtotal','Qmaxtotal','Stotal','Stotal_PE']].dropna()
    
    ## Psum vs. Ssum
    if pearson_r(Upper['Pstorms'],Upper['Supper'])[1] < pvalue:
        Upper_Psum_Ssum_Pearson_r = '%.2f'%pearson_r(Upper['Pstorms'],Upper['Supper'])[0]
        
    if pearson_r(Lower['Pstorms'],Lower['Slower'])[1] < pvalue:
        Lower_Psum_Ssum_Pearson_r = '%.2f'%pearson_r(Lower['Pstorms'],Lower['Slower'])[0]
        
    if pearson_r(Total['Pstorms'],Total['Stotal'])[1] < pvalue:
        Total_Psum_Ssum_Pearson_r = '%.2f'%pearson_r(Total['Pstorms'],Total['Stotal'])[0]
        
    ## EI vs. Ssum
    if pearson_r(Upper['EI'],Upper['Supper'])[1] < pvalue:
        Upper_EI_Ssum_Pearson_r = '%.2f'%pearson_r(Upper['EI'],Upper['Supper'])[0]
    elif pearson_r(Upper['EI'],Upper['Supper'])[1] >= pvalue:
        Upper_EI_Ssum_Pearson_r = ' ' 
        
    if pearson_r(Lower['EI'],Lower['Slower'])[1] < pvalue:
        Lower_EI_Ssum_Pearson_r = '%.2f'%pearson_r(Lower['EI'],Lower['Slower'])[0]
    elif pearson_r(Lower['EI'],Lower['Slower'])[1] >= pvalue:
        Lower_EI_Ssum_Pearson_r = ' ' 
        
    if pearson_r(Total['EI'],Total['Stotal'])[1] < pvalue:
        Total_EI_Ssum_Pearson_r = '%.2f'%pearson_r(Total['EI'],Total['Stotal'])[0]
    elif pearson_r(Total['EI'],Total['Stotal'])[1] >= pvalue:
        Total_EI_Ssum_Pearson_r = ' ' 
        
    ## Qsum vs. Ssum
    if pearson_r(Upper['Qsumupper'],Upper['Supper'])[1] < pvalue:
        Upper_Qsum_Ssum_Pearson_r = '%.2f'%pearson_r(Upper['Qsumupper'],Upper['Supper'])[0]
        
    if pearson_r(Lower['Qsumlower'],Lower['Slower'])[1] < pvalue:
        Lower_Qsum_Ssum_Pearson_r = '%.2f'%pearson_r(Lower['Qsumlower'],Lower['Slower'])[0]
    elif pearson_r(Lower['Qsumlower'],Lower['Slower'])[1]>=pvalue:
        Lower_Qsum_Ssum_Pearson_r = ' '
        
    if pearson_r(Total['Qsumtotal'],Total['Stotal'])[1] < pvalue:
        Total_Qsum_Ssum_Pearson_r = '%.2f'%pearson_r(Total['Qsumtotal'],Total['Stotal'])[0]
    elif pearson_r(Total['Qsumtotal'],Total['Stotal'])[1] >= pvalue:
        Total_Qsum_Ssum_Pearson_r =' '
        
    ## Qmaxvs. Ssum
    if pearson_r(Upper['Qmaxupper'],Upper['Supper'])[1] < pvalue:
        Upper_Qmax_Ssum_Pearson_r = '%.2f'%pearson_r(Upper['Qmaxupper'],Upper['Supper'])[0]
        
    if pearson_r(Lower['Qmaxlower'],Lower['Slower'])[1] < pvalue:
        Lower_Qmax_Ssum_Pearson_r = '%.2f'%pearson_r(Lower['Qmaxlower'],Lower['Slower'])[0]
        
    if pearson_r(Total['Qmaxtotal'],Total['Stotal'])[1] < pvalue:
        Total_Qmax_Ssum_Pearson_r = '%.2f'%pearson_r(Total['Qmaxtotal'],Total['Stotal'])[0]
        
    ## Put data together, and put in table
    PsumS = [Upper_Psum_Ssum_Pearson_r,Lower_Psum_Ssum_Pearson_r,Total_Psum_Ssum_Pearson_r]
    EIS = [Upper_EI_Ssum_Pearson_r,Lower_EI_Ssum_Pearson_r,Total_EI_Ssum_Pearson_r]
    QsumS = [Upper_Qsum_Ssum_Pearson_r,Lower_Qsum_Ssum_Pearson_r,Total_Qsum_Ssum_Pearson_r]
    QmaxS = [Upper_Qmax_Ssum_Pearson_r,Lower_Qmax_Ssum_Pearson_r,Total_Qmax_Ssum_Pearson_r]
    pearson.table(cellText = [PsumS,EIS,QsumS,QmaxS],rowLabels=['Psum','EI','Qsum','Qmax'],colLabels=['FOREST','FOR-VIL','VILLAGE'],loc='center left')
    plt.suptitle("Pearson's coefficients for each variable\n as compared to SSY (Mg), p<"+str(pvalue),fontsize=12)  
    show_plot(show)
    return
#plotPearsonTable(pvalue=0.05,show=True)

def Spearman_r_Table(pvalue=0.05):
    ALLStorms = compileALLStorms()
    Upper = ALLStorms[['Pstorms','EI','Qsumupper','Qmaxupper','Supper','Supper_PE']].dropna()
    Lower = ALLStorms[['Pstorms','EI','Qsumlower','Qmaxlower','Slower']].dropna()
    Total = ALLStorms[['Pstorms','EI','Qsumtotal','Qmaxtotal','Stotal','Stotal_PE']].dropna()
    ## Psum vs. Ssum
    if spearman_r(Upper['Pstorms'],Upper['Supper'])[1] < pvalue:
        Upper_Psum_Ssum_Spearman_r = '%.2f'%spearman_r(Upper['Pstorms'],Upper['Supper'])[0]
    if spearman_r(Lower['Pstorms'],Lower['Slower'])[1] < pvalue:
        Lower_Psum_Ssum_Spearman_r = '%.2f'%spearman_r(Lower['Pstorms'],Lower['Slower'])[0]
    if spearman_r(Total['Pstorms'],Total['Stotal'])[1] < pvalue:
        Total_Psum_Ssum_Spearman_r = '%.2f'%spearman_r(Total['Pstorms'],Total['Stotal'])[0]      
    ## EI vs. Ssum
    if spearman_r(Upper['EI'],Upper['Supper'])[1] < pvalue:
        Upper_EI_Ssum_Spearman_r = '%.2f'%spearman_r(Upper['EI'],Upper['Supper'])[0]
    elif spearman_r(Upper['EI'],Upper['Supper'])[1] >= pvalue:
        Upper_EI_Ssum_Spearman_r = ' ' 
    if spearman_r(Lower['EI'],Lower['Slower'])[1] < pvalue:
        Lower_EI_Ssum_Spearman_r = '%.2f'%spearman_r(Lower['EI'],Lower['Slower'])[0]
    elif spearman_r(Lower['EI'],Lower['Slower'])[1] >= pvalue:
        Lower_EI_Ssum_Spearman_r = ' ' 
    if spearman_r(Total['EI'],Total['Stotal'])[1] < pvalue:
        Total_EI_Ssum_Spearman_r = '%.2f'%spearman_r(Total['EI'],Total['Stotal'])[0]
    elif spearman_r(Total['EI'],Total['Stotal'])[1] >= pvalue:
        Total_EI_Ssum_Spearman_r = ' ' 
    ## Qsum vs. Ssum
    if spearman_r(Upper['Qsumupper'],Upper['Supper'])[1] < pvalue:
        Upper_Qsum_Ssum_Spearman_r = '%.2f'%spearman_r(Upper['Qsumupper'],Upper['Supper'])[0]
    if spearman_r(Lower['Qsumlower'],Lower['Slower'])[1] < pvalue:
        Lower_Qsum_Ssum_Spearman_r = '%.2f'%spearman_r(Lower['Qsumlower'],Lower['Slower'])[0]
    elif spearman_r(Lower['Qsumlower'],Lower['Slower'])[1]>=pvalue:
        Lower_Qsum_Ssum_Spearman_r = ' '
    if spearman_r(Total['Qsumtotal'],Total['Stotal'])[1] < pvalue:
        Total_Qsum_Ssum_Spearman_r = '%.2f'%spearman_r(Total['Qsumtotal'],Total['Stotal'])[0]
    elif spearman_r(Total['Qsumtotal'],Total['Stotal'])[1] >= pvalue:
        Total_Qsum_Ssum_Spearman_r =' '
    ## Qmaxvs. Ssum
    if spearman_r(Upper['Qmaxupper'],Upper['Supper'])[1] < pvalue:
        Upper_Qmax_Ssum_Spearman_r = '%.2f'%spearman_r(Upper['Qmaxupper'],Upper['Supper'])[0]
    if spearman_r(Lower['Qmaxlower'],Lower['Slower'])[1] < pvalue:
        Lower_Qmax_Ssum_Spearman_r = '%.2f'%spearman_r(Lower['Qmaxlower'],Lower['Slower'])[0]
    if spearman_r(Total['Qmaxtotal'],Total['Stotal'])[1] < pvalue:
        Total_Qmax_Ssum_Spearman_r = '%.2f'%spearman_r(Total['Qmaxtotal'],Total['Stotal'])[0]
    ## Put data together, and put in table
    table_data_dict = {'FOREST':[Upper_Psum_Ssum_Spearman_r,Upper_EI_Ssum_Spearman_r,Upper_Qsum_Ssum_Spearman_r,Upper_Qmax_Ssum_Spearman_r],
    'VILLAGE-FOREST':[Lower_Psum_Ssum_Spearman_r,Lower_EI_Ssum_Spearman_r,Lower_Qsum_Ssum_Spearman_r,Lower_Qmax_Ssum_Spearman_r],
    'VILLAGE':[Total_Psum_Ssum_Spearman_r,Total_EI_Ssum_Spearman_r,Total_Qsum_Ssum_Spearman_r,Total_Qmax_Ssum_Spearman_r]} ## Put data in a dictionary to convert to DataFrame
    summary =pd.DataFrame(table_data_dict,index=['Precip','EI','Qsum','Qmax'])[['FOREST','VILLAGE-FOREST','VILLAGE']]
    summary['']= summary.index
    summary = summary[['','FOREST','VILLAGE-FOREST','VILLAGE']]
    return summary
#Spearman_r_Table(pvalue=0.05)

def plotSpearmanTable(pvalue=0.05,show=False):
    nrows, ncols = 3,4
    hcell, wcell=0.3,1
    hpad, wpad = 1,1
    fig = plt.figure(figsize=(ncols*wcell+wpad,nrows*hcell+hpad)) 
    spearman = fig.add_subplot(111)
    spearman.patch.set_visible(False), spearman.axis('off')
    spearman.xaxis.set_visible(False), spearman.yaxis.set_visible(False) 
    
    ALLStorms = compileALLStorms()
    Upper = ALLStorms[['Supper','Supper_PE','Qsumupper','Qmaxupper','Pstorms','EI']].dropna()
    Lower = ALLStorms[['Slower','Qsumlower','Qmaxlower','Pstorms','EI']].dropna()
    Total = ALLStorms[['Stotal','Stotal_PE','Qsumtotal','Qmaxtotal','Pstorms','EI']].dropna()

    ## Psum vs. Ssum
    if spearman_r(Upper['Pstorms'],Upper['Supper'])[1] < pvalue:
        Upper_Psum_Ssum_Spearman_r = '%.2f'%spearman_r(Upper['Pstorms'],Upper['Supper'])[0]
        
    if spearman_r(Lower['Pstorms'],Lower['Slower'])[1] < pvalue:
        Lower_Psum_Ssum_Spearman_r = '%.2f'%spearman_r(Lower['Pstorms'],Lower['Slower'])[0]
    elif spearman_r(Lower['Pstorms'],Lower['Slower'])[1] >= pvalue:
        Lower_Psum_Ssum_Spearman_r = ' '
        
    if spearman_r(Total['Pstorms'],Total['Stotal'])[1] < pvalue:
        Total_Psum_Ssum_Spearman_r = '%.2f'%spearman_r(Total['Pstorms'],Total['Stotal'])[0]
        
    ## EI vs. Ssum
    if spearman_r(Upper['EI'],Upper['Supper'])[1] < pvalue:
        Upper_EI_Ssum_Spearman_r = '%.2f'%spearman_r(Upper['EI'],Upper['Supper'])[0]
    elif spearman_r(Upper['EI'],Upper['Supper'])[1] >= pvalue:
        Upper_EI_Ssum_Spearman_r = ' ' 
        
    if spearman_r(Lower['EI'],Lower['Slower'])[1] < pvalue:
        Lower_EI_Ssum_Spearman_r = '%.2f'%spearman_r(Lower['EI'],Lower['Slower'])[0]
    elif spearman_r(Lower['EI'],Lower['Slower'])[1] >= pvalue:
        Lower_EI_Ssum_Spearman_r = ' ' 
        
    if spearman_r(Total['EI'],Total['Stotal'])[1] < pvalue:
        Total_EI_Ssum_Spearman_r = '%.2f'%spearman_r(Total['EI'],Total['Stotal'])[0]
    elif spearman_r(Total['EI'],Total['Stotal'])[1] >= pvalue:
        Total_EI_Ssum_Spearman_r = ' ' 
        
    ## Qsum vs. Ssum
    if spearman_r(Upper['Qsumupper'],Upper['Supper'])[1] < pvalue:
        Upper_Qsum_Ssum_Spearman_r = '%.2f'%spearman_r(Upper['Qsumupper'],Upper['Supper'])[0]
        
    if spearman_r(Lower['Qsumlower'],Lower['Slower'])[1] < pvalue:
        Lower_Qsum_Ssum_Spearman_r = '%.2f'%spearman_r(Lower['Qsumlower'],Lower['Slower'])[0]
    elif spearman_r(Lower['Qsumlower'],Lower['Slower'])[1]>=pvalue:
        Lower_Qsum_Ssum_Spearman_r = ' '
        
    if spearman_r(Total['Qsumtotal'],Total['Stotal'])[1] < pvalue:
        Total_Qsum_Ssum_Spearman_r = '%.2f'%spearman_r(Total['Qsumtotal'],Total['Stotal'])[0]
    elif spearman_r(Total['Qsumtotal'],Total['Stotal'])[1] >= pvalue:
        Total_Qsum_Ssum_Spearman_r =' '
        
    ## Qmaxvs. Ssum
    if spearman_r(Upper['Qmaxupper'],Upper['Supper'])[1] < pvalue:
        Upper_Qmax_Ssum_Spearman_r = '%.2f'%spearman_r(Upper['Qmaxupper'],Upper['Supper'])[0]
        
    if spearman_r(Lower['Qmaxlower'],Lower['Slower'])[1] < pvalue:
        Lower_Qmax_Ssum_Spearman_r = '%.2f'%spearman_r(Lower['Qmaxlower'],Lower['Slower'])[0]
        
    if spearman_r(Total['Qmaxtotal'],Total['Stotal'])[1] < pvalue:
        Total_Qmax_Ssum_Spearman_r = '%.2f'%spearman_r(Total['Qmaxtotal'],Total['Stotal'])[0]
        
        
    ## Put data together, and put in table
    PsumS = [Upper_Psum_Ssum_Spearman_r,Lower_Psum_Ssum_Spearman_r,Total_Psum_Ssum_Spearman_r]
    EIS = [Upper_EI_Ssum_Spearman_r,Lower_EI_Ssum_Spearman_r,Total_EI_Ssum_Spearman_r]
    QsumS = [Upper_Qsum_Ssum_Spearman_r,Lower_Qsum_Ssum_Spearman_r,Total_Qsum_Ssum_Spearman_r]
    QmaxS = [Upper_Qmax_Ssum_Spearman_r,Lower_Qmax_Ssum_Spearman_r,Total_Qmax_Ssum_Spearman_r]
    spearman.table(cellText = [PsumS,EIS,QsumS,QmaxS],rowLabels=['Psum','EI','Qsum','Qmax'],colLabels=['FOREST','FOR-VIL','VILLAGE'],loc='center left')
    plt.suptitle("Spearman's coefficients for each variable\n as compared to SSY (Mg), p<"+str(pvalue),fontsize=12)  
    plt.draw()
    if show==True:
        plt.show()
    return
#plotSpearmanTable(pvalue=0.05,show=True)
    
def plotCoeffTable(show=False,norm=False):
    if norm==True:
        ALLStorms=NormalizeSSYbyCatchmentArea(compileALLStorms())
        Upper = powerfunction(ALLStorms['Qmaxupper'],ALLStorms['Supper'])
        Total = powerfunction(ALLStorms['Qmaxtotal'],ALLStorms['Stotal'])    
        
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
        Upper = powerfunction(ALLStorms['Qmaxupper'],ALLStorms['Supper'])
        Lower = powerfunction(ALLStorms['Qmaxlower'],ALLStorms['Slower'])    
        Total = powerfunction(ALLStorms['Qmaxtotal'],ALLStorms['Stotal'])
        
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
    


### ANCOVA

### duplicate TOTAL but name it upper: TEST for SAME data, should be pvalue=1
#ALLStorms_upper = ALLStorms[ALLStorms['Pstorms']>1][['Pstorms','EI','Qsumtotal','Qmaxtotal','Stotal']].dropna().apply(np.log10) 
#ALLStorms_upper['subwatershed'] = 'upper'
#ALLStorms_upper = ALLStorms_upper.rename(columns = {'Qsumtotal':'Qsum','Qmaxtotal':'Qmax','Stotal':'S'})

#R1= [[0,1,0,0],[0,0,1,0]]
#m1 = model_lm1.f_test(R1)
#print m1
#R2 = [[1,0,0],[0,1,0]]
#m2 = model_lm2.f_test(R2)

def ANCOVA(ALLStorms, ind_var, pvalue=0.05):
    ## Upper subwatershed
    ALLStorms_upper = ALLStorms[ALLStorms['Pstorms']>1][['Pstorms','EI','Qsumupper','Qmaxupper','Supper']].dropna().apply(np.log10) 
    ALLStorms_upper['subwatershed'] = 'upper'
    ALLStorms_upper = ALLStorms_upper.rename(columns = {'Pstorms':'Psum','Qsumupper':'Qsum','Qmaxupper':'Qmax','Supper':'SSY'})
    ## Total watershed
    ALLStorms_total = ALLStorms[ALLStorms['Pstorms']>1][['Pstorms','EI','Qsumtotal','Qmaxtotal','Stotal']].dropna().apply(np.log10) 
    ALLStorms_total['subwatershed'] = 'total'
    ALLStorms_total = ALLStorms_total.rename(columns = {'Pstorms':'Psum','Qsumtotal':'Qsum','Qmaxtotal':'Qmax','Stotal':'SSY'})
    
    s_data = pd.concat([ALLStorms_upper,ALLStorms_total])
        
    s_data = s_data[['subwatershed','SSY',ind_var]]
    formula1 = 'SSY ~ '+ind_var+' * subwatershed'
    #print formula1
    model_lm1 = smf.ols(formula1,data=s_data).fit()  
    model_table1 = statsmodels.stats.api.anova_lm(model_lm1) 
    #print model_table1
    
    m1_pvalue = model_table1.ix[ind_var+':subwatershed']['PR(>F)']
    if m1_pvalue <= pvalue:
        #print 'For independent variable: '+ind_var+', slopes significantly different at pvalue='+str(pvalue)+' pval='+str(m1_pvalue)
        slopes_significant = '*'
        slopes_sig = ''
    elif m1_pvalue > pvalue:
        #print 'For independent variable: '+ind_var+', slopes NOT significantly different at pvalue='+str(pvalue)+' pval='+str(m1_pvalue)
        slopes_significant = ''
        slopes_sig = ' NOT'
    formula2 = 'SSY ~ '+ind_var+' + subwatershed'
    #print formula2  
    model_lm2 = smf.ols(formula2,data=s_data).fit() 
    model_table2 = statsmodels.stats.api.anova_lm(model_lm2)
    #print model_table2        
    m2_pvalue = model_table1.ix['subwatershed']['PR(>F)']
    if m2_pvalue <= pvalue:
        #print 'For independent variable: '+ind_var+', intercepts significantly different at pvalue='+str(pvalue)+' pval='+str(m2_pvalue)
        intercepts_significant = '*'
        intercepts_sig = ''
    if m2_pvalue > pvalue:
        #print 'For independent variable: '+ind_var+', intercepts NOT significantly different at pvalue='+str(pvalue)+' pval='+str(m2_pvalue)
        intercepts_significant = ''
        intercepts_sig = ' NOT'
    m = statsmodels.stats.api.anova_lm(model_lm2,model_lm1)    
    #print m
    #print 'ANOVA of models, p-value = '+str(m.ix[1]['Pr(>F)'])
    print 'Predictor: '+ind_var+', slopes were'+slopes_sig+' significant (p='+"%.3f"%m1_pvalue+'), intercepts were'+intercepts_sig+' significant (p='+"%.3f"%m2_pvalue+').'
    return slopes_significant+intercepts_significant



#### Sediment Rating Curves: on area-normalized SSY, Q and Qmax
def plotALLStorms_ALLRatings(subset='pre',ms=10,norm=False,log=False,show=False,save=False,filename=''):  
    mpl.rc('lines',markersize=ms)
    mpl.rc('grid',alpha=0)
    fig, ((ps,ei),(qsums,qmaxs)) = plt.subplots(2,2,figsize=(8,6),sharex=False,sharey=True)
    title = 'All sediment rating curves for all predictors'
    ## Normalize by area
    if norm==True:
        ALLStorms=NormalizeSSYbyCatchmentArea(compileALLStorms(subset))
        ylabel,xlabelP,xlabelEI,xlabelQsum,xlabelQmax = r'$SSY (Mg/km^2)$','Precip (mm)','Erosivity Index', r'$(m^3/km^2)$', r'$(m^3/sec/km^2)$'
    else:
        ALLStorms=compileALLStorms(subset)
        ylabel,xlabelP,xlabelEI,xlabelQsum,xlabelQmax = 'SSY (Mg)','Precip (mm)','Erosivity Index',r'$(m^3)$',r'$(m^3/sec)$'
    xy=None ## let the Fit functions plot their own lines
    
    ## ANCOVA's
    PS_ANCOVA = ANCOVA(ALLStorms,'Psum')
    EI_ANCOVA = ANCOVA(ALLStorms,'EI')
    QsumS_ANCOVA  = ANCOVA(ALLStorms,'Qsum')  
    QmaxS_ANCOVA = ANCOVA(ALLStorms,'Qmax')     
    
    ## P vs S at Upper, Total
    ALLStorms_upper = ALLStorms[ALLStorms['Pstorms']>1][['Pstorms','Supper']].dropna()
    ALLStorms_total = ALLStorms[ALLStorms['Pstorms']>1][['Pstorms','Stotal']].dropna() 
    ps.plot(ALLStorms_upper['Pstorms'],ALLStorms_upper['Supper'],color='grey',linestyle='none',marker='s',fillstyle='none',label='Upper')
    ps.plot(ALLStorms_total['Pstorms'],ALLStorms_total['Stotal'],color='k',linestyle='none',marker='o',label='Total')
    ## Upper Watershed (=DAM)
    PS_upper_power = powerfunction(ALLStorms_upper['Pstorms'],ALLStorms_upper['Supper'])
    PowerFit(ALLStorms_upper['Pstorms'],ALLStorms_upper['Supper'],xy,ps,linestyle='-',color='grey', label='Upper ' +r'$r^2$'+"%.2f"%PS_upper_power.r2)
    ## Total Watershed (=LBJ)
    PS_total_power = powerfunction(ALLStorms_total['Pstorms'],ALLStorms_total['Stotal'])
    PowerFit(ALLStorms_total['Pstorms'],ALLStorms_total['Stotal'],xy,ps,linestyle='-',color='k',label='Total '+r'$r^2$'+"%.2f"%PS_total_power.r2+' '+PS_ANCOVA) 
    
    ps.set_xlabel('Total Event Precip (mm)'),ps.set_ylabel(ylabel)
    ps.set_xlim(10**0,10**3),ps.set_ylim(10**-3.1,10**2.2)
    ps.legend(loc='lower right',fancybox=True) 
    ## EI vs S at Upper, Total  
    ALLStorms_upper = ALLStorms[['EI','Supper']].dropna()
    ALLStorms_total = ALLStorms[['EI','Stotal']].dropna() 
    ei.plot(ALLStorms_upper['EI'],ALLStorms_upper['Supper'],color='grey',linestyle='none',marker='s',fillstyle='none')#,label='Upper')
    ei.plot(ALLStorms_total['EI'],ALLStorms_total['Stotal'],color='k',linestyle='none',marker='o')#,label='Total')
    ## Upper Watershed (=DAM)
    EI_upper_power = powerfunction(ALLStorms_upper['EI'],ALLStorms_upper['Supper'])
    PowerFit(ALLStorms_upper['EI'],ALLStorms_upper['Supper'],xy,ei,linestyle='-',color='grey',label='Upper '+r'$r^2$'+"%.2f"%EI_upper_power.r2) 
    ## Total Watershed (=LBJ)       
    EI_total_power = powerfunction(ALLStorms_total['EI'],ALLStorms_total['Stotal'])
    PowerFit(ALLStorms_total['EI'],ALLStorms_total['Stotal'],xy,ei,linestyle='-',color='k',label='Total '+r'$r^2$'+"%.2f"%EI_total_power.r2+' '+EI_ANCOVA) 
    ei.set_xlabel('Event Erosivity Index (MJmm ha-1 h-1)')#ei.set_ylabel(ylabel)
    ei.set_xlim(10**1,10**3)#,ps.set_ylim(10**-3,10**2.2)
    ei.legend(loc='lower left',fancybox=True) 
    ## Qsum vs S at Upper, Total 
    ALLStorms_upper = ALLStorms[['Qsumupper','Supper']].dropna()
    ALLStorms_total = ALLStorms[['Qsumtotal','Stotal']].dropna() 
    qsums.plot(ALLStorms_upper['Qsumupper'],ALLStorms_upper['Supper'],color='grey',linestyle='none',marker='s',fillstyle='none')#,label='Upper')
    qsums.plot(ALLStorms_total['Qsumtotal'],ALLStorms_total['Stotal'],color='k',linestyle='none',marker='o')#,label='Total')
    ## Upper Watershed (=DAM)    
    QsumS_upper_power = powerfunction(ALLStorms_upper['Qsumupper'],ALLStorms_upper['Supper'])
    PowerFit(ALLStorms_upper['Qsumupper'],ALLStorms_upper['Supper'],xy,qsums,linestyle='-',color='grey',label='Upper '+r'$r^2$'+"%.2f"%QsumS_upper_power.r2)
    ## Total Watershed (=LBJ)
    QsumS_total_power = powerfunction(ALLStorms_total['Qsumtotal'],ALLStorms_total['Stotal'])
    PowerFit(ALLStorms_total['Qsumtotal'],ALLStorms_total['Stotal'],xy,qsums,linestyle='-',color='k',label='Total '+r'$r^2$'+"%.2f"%QsumS_total_power.r2+' '+QsumS_ANCOVA) 
    qsums.set_xlabel('Total Event Discharge '+xlabelQsum)
    qsums.set_ylabel(ylabel)#qsums.set_xlabel(xlabelQsum)
    qsums.set_xlim(10**2.5,10**6)#, qsums.set_ylim(10**-3.1,10**2.2)
    qsums.legend(loc='lower right',fancybox=True) 
    ## Qmax vs S at Upper, Total  
    ALLStorms_upper = ALLStorms[['Qmaxupper','Supper']].dropna()
    ALLStorms_total = ALLStorms[['Qmaxtotal','Stotal']].dropna() 
    qmaxs.plot(ALLStorms_upper['Qmaxupper'],ALLStorms_upper['Supper'],color='grey',linestyle='none',marker='s',fillstyle='none')#,label='Upper')
    qmaxs.plot(ALLStorms_total['Qmaxtotal'],ALLStorms_total['Stotal'],color='k',linestyle='none',marker='o')#,label='Total')
    ## Upper Watershed (=DAM)       
    QmaxS_upper_power = powerfunction(ALLStorms_upper['Qmaxupper'],ALLStorms_upper['Supper'])
    PowerFit(ALLStorms_upper['Qmaxupper'],ALLStorms_upper['Supper'],xy,qmaxs,linestyle='-',color='grey',label='Upper '+r'$r^2$'+"%.2f"%QmaxS_upper_power.r2)
    ## Total Watershed (=LBJ)
    QmaxS_total_power = powerfunction(ALLStorms_total['Qmaxtotal'],ALLStorms_total['Stotal'])
    PowerFit(ALLStorms_total['Qmaxtotal'],ALLStorms_total['Stotal'],xy,qmaxs,linestyle='-',color='k',label='Total '+r'$r^2$'+"%.2f"%QmaxS_total_power.r2+' '+QmaxS_ANCOVA)
    qmaxs.set_xlabel('Event Peak Discharge '+xlabelQmax)
    #qmaxs.set_ylabel(ylabel)#qmaxs.set_xlabel(xlabelQmax)
    qmaxs.set_xlim(10**-1.2,10**1)#, qmaxs.set_ylim(10**-3,10**2.2)
    qmaxs.legend(loc='lower right',fancybox=True) 
    
    letter_subplots(fig,x=0.1,y=0.95,vertical='top',horizontal='right',Color='k',font_size=10,font_weight='bold')
    for ax in fig.axes:
        ax.grid(False)          
        #ax.autoscale_view(True,True,True)
    logaxes(log,fig) 
    plt.grid(b=False,axis='both')
    
    plt.tight_layout(pad=0.1)
    show_plot(show,fig)
    savefig(save,filename)
       
    
    return (PS_upper_power,PS_total_power,EI_upper_power,EI_total_power,QsumS_upper_power, QsumS_total_power,QmaxS_upper_power, QmaxS_total_power), (PS_ANCOVA, EI_ANCOVA, QsumS_ANCOVA, QmaxS_ANCOVA)
    
#plotALLStorms_ALLRatings(subset='pre',ms=4,norm=True,log=True,show=True,save=False,filename='')
#plotALLStorms_ALLRatings(subset='pre',ms=4,norm=True,log=False,show=True,save=False,filename='')
#plotALLStorms_ALLRatings(show=True,log=False,save=True)
#plotALLStorms_ALLRatings(ms=20,show=True,log=True,save=True,norm=False)
    
#plotALLStorms_ALLRatings(subset='post',ms=4,norm=True,log=True,show=True,save=False,filename='')

def ALLRatings_table(subset='pre'):
    models = plotALLStorms_ALLRatings(subset,show=False)
    ALLStorms_ALLRatings = models[0]
    ANCOVAs = models[1]
    
    pearsons = ["%.2f"%rating.pearson[0] for rating in ALLStorms_ALLRatings]
    spearmans = ["%.2f"%rating.spearman[0] for rating in ALLStorms_ALLRatings]
    r2s = ["%.2f"%rating.r2[0] for rating in ALLStorms_ALLRatings]
    rmses = ["%.2f"%10**rating.rmse[0] for rating in ALLStorms_ALLRatings]
    alphas= ["%.3f"%rating.a[0] for rating in ALLStorms_ALLRatings]
    betas  = ["%.2f"%rating.b[0] for rating in ALLStorms_ALLRatings]
    
    ALLRatings_stats = pd.DataFrame({'Pearson':pearsons,'Spearman':spearmans,'r2':r2s,'RMSE(tons)':rmses,'alpha':alphas,'Beta':betas},index =['Psum_upper','Psum_total','EI_upper','EI_total',
    'Qsum_upper','Qsum_total','Qmax_upper','Qmax_total'])
    ALLRatings_stats['Model'] = ALLRatings_stats.index
    ALLRatings_stats = ALLRatings_stats[['Model','Pearson','Spearman','r2','RMSE(tons)','alpha','Beta']]
    ALLRatings_stats = ALLRatings_stats.replace('nan','-')
    return ALLRatings_stats
#ALLRatings_table(subset='post')
    
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
    qs.scatter(ALLStorms_upper['Qmaxupper']/1000,ALLStorms_upper['Supper'],edgecolors='grey',color='g',s=upperdotsize,label='FOREST')
    QmaxS_upper_power = powerfunction(ALLStorms_upper['Qmaxupper']/1000,ALLStorms_upper['Supper'])
    PowerFit_CI(ALLStorms_upper['Qmaxupper']/1000,ALLStorms_upper['Supper'],xy,qs,linestyle='-',color='g',label='FOREST') 
    QmaxS_upper_linear = linearfunction(ALLStorms_upper['Qmaxupper']/1000,ALLStorms_upper['Supper'])
    #LinearFit(ALLStorms_upper['Qmaxupper']/1000,ALLStorms_upper['Supper'],xy,qs,linestyle='--',color='g',label='QmaxS_upper_linear') 
    labelindex(ALLStorms_upper.index,ALLStorms_upper['Qmaxupper']/1000,ALLStorms_upper['Supper'],qs)   
    
    ## Total Watershed (=LBJ)
    ALLStorms_total = ALLStorms[['Qmaxtotal','Stotal']].dropna()
    qs.scatter(ALLStorms_total['Qmaxtotal']/1000,ALLStorms_total['Stotal'],edgecolors='grey',color='r',s=lowerdotsize,label='VILLAGE')
    QmaxS_total_power = powerfunction(ALLStorms_total['Qmaxtotal']/1000,ALLStorms_total['Stotal'])
    PowerFit_CI(ALLStorms_total['Qmaxtotal']/1000,ALLStorms_total['Stotal'],xy,qs,linestyle='-',color='r',label='VILLAGE') 
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
        #Duvert1 = 224.4*(xy**1.34)
        Duvert2 = 446.6*(xy**0.93)
        #DuvertLAFR = 408*(xy**0.95)
        #DuvertARES= 640*(xy**1.22)
        #DuvertCIES=5039*(xy**1.82)
        DuvertCOMX= 28*(xy**1.92)
        #PowerFit(xy,Duvert1,xy,qs,linestyle='-',color='grey',label='Duvert(2012)Linear')
        PowerFit(xy,Duvert2,xy,qs,linestyle='--',color='grey',label='Duvert(2012)Nonlinear')
        #PowerFit(xy,DuvertLAFR,xy,qs,linestyle='-',color='k',label=r'Duvert(2012)$LA_{FR}$')
        #PowerFit(xy,DuvertARES,xy,qs,linestyle='--',color='k',label=r'Duvert(2012)$AR_{ES}$')
        #PowerFit(xy,DuvertCIES,xy,qs,linestyle='-.',color='k',label=r'Duvert(2012)$CI_{ES}$')
        PowerFit(xy,DuvertCOMX,xy,qs,linestyle='-.',color='b',label=r'Duvert(2012)$Mexico$')        
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
    savefig(save,title+'1.png')
    return
#plotQmaxS(show=True,log=True,save=False,norm=True)  
#plotQmaxS(show=True,log=True,save=True,norm=True)  
#plotQmaxS(show=True,log=False,save=True)
#plotQmaxS(show=True,log=True,save=True,norm=False)
#plotQmaxS(show=True,log=True,save=True,norm=True)

### Qmax vs S    
def plotQmaxStotal(subset='pre',ms=10,norm=False,log=False,show=False,save=False,filename=''): 
    mpl.rc('lines',markersize=ms)
    mpl.rc('grid',alpha=0)
    fig, qmaxs = plt.subplots(figsize=(5,4))
    ## Normalize by area
    if norm==True:
        ALLStorms=NormalizeSSYbyCatchmentArea(compileALLStorms(subset))
        ylabel,xlabelP,xlabelEI,xlabelQsum,xlabelQmax = r'$SSY (Mg/km^2)$','Precip (mm)','Erosivity Index', r'$(m^3/km^2)$', r'$(m^3/sec/km^2)$'
    else:
        ALLStorms=compileALLStorms(subset)
        ylabel,xlabelP,xlabelEI,xlabelQsum,xlabelQmax = 'SSY (Mg)','Precip (mm)','Erosivity Index',r'$(m^3)$',r'$(m^3/sec)$'
    xy=None ## let the Fit functions plot their own lines
    ## Qmax vs S at Upper, Total  
    ALLStorms_upper = ALLStorms[['Qmaxupper','Supper']].dropna()
    ALLStorms_total = ALLStorms[['Qmaxtotal','Stotal']].dropna() 
    qmaxs.plot(ALLStorms_upper['Qmaxupper'],ALLStorms_upper['Supper'],color='grey',linestyle='none',marker='s',fillstyle='none',label='F1 Upper watershed')
    qmaxs.plot(ALLStorms_total['Qmaxtotal'],ALLStorms_total['Stotal'],color='k',linestyle='none',marker='o',label='F3 Village')
    ## Upper Watershed (=DAM)       
    QmaxS_upper_power = powerfunction(ALLStorms_upper['Qmaxupper'],ALLStorms_upper['Supper'])
    PowerFit(ALLStorms_upper['Qmaxupper'],ALLStorms_upper['Supper'],xy,qmaxs,linestyle='-',color='grey',label='F1 Upper watershed '+r'$r^2$'+"%.2f"%QmaxS_upper_power.r2)
    ## Total Watershed (=LBJ)
    QmaxS_total_power = powerfunction(ALLStorms_total['Qmaxtotal'],ALLStorms_total['Stotal'])
    PowerFit(ALLStorms_total['Qmaxtotal'],ALLStorms_total['Stotal'],xy,qmaxs,linestyle='-',color='k',label='F3 Village '+r'$r^2$'+"%.2f"%QmaxS_total_power.r2)
    qmaxs.set_xlabel('Event Peak Discharge '+xlabelQmax)
    qmaxs.set_ylabel(ylabel)
    #qmaxs.set_ylabel(ylabel)#qmaxs.set_xlabel(xlabelQmax)
    qmaxs.set_xlim(10**-1.2,10**1)#, qmaxs.set_ylim(10**-3,10**2.2)
    qmaxs.legend(loc='lower right',fancybox=True) 
    
    #letter_subplots(fig,x=0.1,y=0.95,vertical='top',horizontal='right',Color='k',font_size=10,font_weight='bold')
    for ax in fig.axes:
        ax.grid(False)          
        #ax.autoscale_view(True,True,True)
    logaxes(log,fig) 
    plt.grid(b=False,axis='both')
    
    plt.tight_layout(pad=0.1)
    show_plot(show,fig)
    savefig(save,filename)
    return
#plotQmaxStotal(subset='pre',ms=4,norm=True,log=True,show=True,save=False,filename='')  

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
#plotQmaxSseparate(show=True,log=True,save=False,norm=True)  



#### Predict Annual SSY
## Models
PS_upper_power,PS_total_power,EI_upper_power,EI_total_power,QsumS_upper_power, QsumS_total_power,QmaxS_upper_power, QmaxS_total_power = plotALLStorms_ALLRatings(subset='pre',show=False)[0]

def predict_SSY(model,data,start,stop,watershed_area):
    a,b = model.iloc[0][['a','b']]
    SSY_predicted = a * ((data[start:stop]) **b)
    SSY = SSY_predicted.sum()
    spec_SSY  = SSY/watershed_area
    return "%.0f"%SSY, "%.0f"%spec_SSY
    
## Total
SSY_Total_2012, sSSY_Total_2012 = predict_SSY(QmaxS_total_power,SedFluxStorms_LBJ['Qmax']/1000,start2012,stop2012,1.78)
SSY_Total_2014, sSSY_Total_2014 = predict_SSY(QmaxS_total_power,SedFluxStorms_LBJ['Qmax']/1000,start2014,dt.datetime(2014,12,31),1.78)

## Upper
SSY_Upper_2012, sSSY_Upper_2012 = predict_SSY(QmaxS_upper_power,SedFluxStorms_DAM['Qmax']/1000,start2012,stop2012,0.9)
SSY_Upper_2014, sSSY_Upper_2014 = predict_SSY(QmaxS_upper_power,SedFluxStorms_DAM['Qmax']/1000,start2014,dt.datetime(2014,12,31),0.9)

## Use LBJ_Qmax to DAM_Qmax relationship to fill gaps in LBJ Q
Storms_Qmax = pd.DataFrame({'LBJ_Qmax':SedFluxStorms_LBJ['Qmax'],'DAM_Qmax':SedFluxStorms_DAM['Qmax']})
#plt.plot(Storms_Qmax['DAM_Qmax'],Storms_Qmax['LBJ_Qmax'],ls='none',marker='.')
Qmax_fill = pd.ols(x=Storms_Qmax['DAM_Qmax'],y=Storms_Qmax['LBJ_Qmax'])
## Need to get storm intervals for DAM Q timeseries
## Define Storm Intervals at DAM
def DAM_Q_storm_with_new_DAMstormIntervals():
    DAM_StormIntervals=SeparateHydrograph(hydrodata=PT3['stage'])
    ## Combine Storm Events where the storm end is the storm start for the next storm
    DAM_StormIntervals['next storm start']=DAM_StormIntervals['start'].shift(-1) ## add the next storm's start and end time to the storm in the row above (the previous storm)
    DAM_StormIntervals['next storm end']=DAM_StormIntervals['end'].shift(-1)
    need_to_combine =DAM_StormIntervals[DAM_StormIntervals['end']==DAM_StormIntervals['next storm start']] #storms need to be combined if their end is the same time as the next storm's start
    need_to_combine['end']=need_to_combine['next storm end'] # change the end of the storm to the end of the next storm to combine them
    DAM_StormIntervals=DAM_StormIntervals.drop(need_to_combine.index) #drop the storms that need to be combined
    DAM_StormIntervals=DAM_StormIntervals.append(need_to_combine).sort(ascending=True) #append back in the combined storms
    DAM_StormIntervals=DAM_StormIntervals.drop_duplicates(cols=['end']) 
    
    Qstorms_DAM=StormSums(DAM_StormIntervals,DAMq['Q']) 
    Qstorms_DAM.columns=['Qstart','Qend','Qcount','Qsum','Qmax']
    Qstorms_DAM['Qmax']=Qstorms_DAM['Qmax']/900 ## Have to divide by 900 to get instantaneous 
    
    Pstorms_DAM = StormSums(DAM_StormIntervals,PrecipFilled['Precip'],60) ##30minute offset to get precip before stage started rising
    Pstorms_DAM.columns=['Pstart','Pend','Pcount','Psum','Pmax']
    Pstorms_DAM['EI'] = DAM_Stormdf['EI']
    Qstorms_DAM['Psum'] = Pstorms_DAM['Psum']
    return Qstorms_DAM
DAM_Qstorms_DAM_intervals = DAM_Q_storm_with_new_DAMstormIntervals()

## Predict LBJ Qmax with new DAM storms
P_2014_storm = "%.0f"%DAM_Qstorms_DAM_intervals[start2014:dt.datetime(2014,12,31)]['Psum'].sum()
P_2014_perc_ann = "%.0f"%(DAM_Qstorms_DAM_intervals[start2014:dt.datetime(2014,12,31)]['Psum'].sum()/4000*100)
LBJ_Qmax_fill = DAM_Qstorms_DAM_intervals['Qmax'] * Qmax_fill.beta[0] + Qmax_fill.beta[1]

SedFluxStorms_LBJ_filled = pd.DataFrame({'LBJ_Q':SedFluxStorms_LBJ['Qmax'],'LBJ_Q_filled':LBJ_Qmax_fill},index = LBJ_Qmax_fill.index)

SedFluxStorms_LBJ_filled['LBJ_Q_combined'] =  SedFluxStorms_LBJ_filled['LBJ_Q'].where(SedFluxStorms_LBJ_filled['LBJ_Q']>0,SedFluxStorms_LBJ_filled['LBJ_Q_filled'])

SSY_Total_filled_2014, sSSY_Total_filled_2014 =predict_SSY(QmaxS_total_power,SedFluxStorms_LBJ_filled['LBJ_Q_combined']/1000,start2014,dt.datetime(2014,12,31),1.78)



def Annual_SSY_tables():
    Annual_SSY_table = pd.DataFrame({
    'SSY Table 2':[P_measured_2+' ('+"%.0f"%P_measured_2_perc_storm+'%)', annual_SSY_UPPER_2, annual_SSY_LOWER_2, '-', '-', annual_SSY_TOTAL_2],
    'SSY Table 3':[P_measured_3+' ('+"%.0f"%P_measured_3_perc_storm+'%)', annual_SSY_UPPER_3, annual_SSY_LOWER_3, annual_SSY_LOWER_QUARRY_3, annual_SSY_LOWER_VILLAGE_3, annual_SSY_TOTAL_3],
    'SSY ALL':["%.0f"%P_FG1_all_storms+' ('+"%.0f"%P_FG1_percent_storm+'%)', "%.0f"%annual_SSY_UPPER_ALL,'-','-','-',"%.0f"%annual_SSY_TOTAL_ALL],
    'SSY Qmax (2014)':[P_2014_storm,SSY_Upper_2014,'-','-','-',SSY_Total_filled_2014]}, index=['Precip(mm)','UPPER','LOWER','LOWER_QUARRY','LOWER_VILLAGE','TOTAL'])
    Annual_SSY_table[''] = Annual_SSY_table.index
    Annual_SSY_table = Annual_SSY_table[['','SSY Qmax (2014)','SSY Table 2','SSY Table 3','SSY ALL']]
    
    
    Annual_sSSY_table = pd.DataFrame({
    'sSSY Table 2':[P_measured_2+' ('+"%.0f"%P_measured_2_perc_storm+'%)', annual_sSSY_UPPER_2, annual_sSSY_LOWER_2, '-', '-', annual_sSSY_TOTAL_2],
    'sSSY Table 3':[P_measured_3+' ('+"%.0f"%P_measured_3_perc_storm+'%)', annual_sSSY_UPPER_3, annual_sSSY_LOWER_3, annual_sSSY_LOWER_QUARRY_3, annual_sSSY_LOWER_VILLAGE_3, annual_sSSY_TOTAL_3],
    'sSSY ALL':["%.0f"%P_FG1_all_storms+' ('+"%.0f"%P_FG1_percent_storm+'%)', "%.0f"%annual_sSSY_UPPER_ALL,'-','-','-',"%.0f"%annual_sSSY_TOTAL_ALL],
    'sSSY Qmax (2014)':[P_2014_storm, sSSY_Upper_2014,'-','-','-',sSSY_Total_filled_2014]}, index=['Precip(mm)','UPPER','LOWER','LOWER_QUARRY','LOWER_VILLAGE','TOTAL'])
    Annual_sSSY_table[''] = Annual_sSSY_table.index
    Annual_sSSY_table = Annual_sSSY_table[['','sSSY Qmax (2014)','sSSY Table 2','sSSY Table 3','sSSY ALL']]
    
    return Annual_SSY_table, Annual_sSSY_table
#Annual_SSY_tables()


plt.show()
elapsed = dt.datetime.now() - start_time 
print 'run time: '+str(elapsed)


