#### LOAD DATA FIRST
## OPEN AND RUN "StartHere-LoadDataForSession-Nuuuli.py"


# -*- coding: utf-8 -*-
"""
Created Aug 2014 (migrated to Github)

This code opens relevant precipitation, stream pressure transducer, stream flow measurement (A/V), turbidimeter, etc. data
to calculate the sediment loading at stream gauging locations in Nu'uuli watershed


@author: Alex Messina
"""
#### Import modules
import sys
if 'XL' not in locals(): ## XL is the Master_Data.xlsx file
    print"Please run Load_NUUULI_DATA."
    sys.exit()

##custom modules
from misc_time import * 
from misc_numpy import *
from misc_matplotlib import * 

## Statistical Analysis
import pandas.stats.moments as m
from scipy.stats import pearsonr as pearson_r
from scipy.stats import spearmanr as spearman_r

#timer
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
    figdir = datadir+'samoa/WATERSHED_ANALYSIS/GoodFigures/rawfigoutput/'
    return    
def pltsns(style='ticks',context='talk'):
    global figdir
    sns.set_style(style)
    sns.set_style({'legend.frameon':True})
    sns.set_context(context)
    figdir = datadir+'samoa/WATERSHED_ANALYSIS/GoodFigures/rawfigoutput/'
    return
def xkcd():
    global figdir
    plt.xkcd()
    figdir = datadir+'samoa/WATERSHED_ANALYSIS/GoodFigures/rawfigoutput/xkcd/'
    return

## Misc. plotting tools
def labelxy(i,x,y):
    annotes = pd.DataFrame([x,y]).apply(tuple,axis=0).values.tolist()
    annotestrings = ["%.1f"%an[0]+','+"%.1f"%an[1] for an in annotes]
    af = AnnoteFinder(x,y,annotestrings)
    pylab.connect('button_press_event', af)
    return

def labelindex(i,x,y): 
    indexstrings = [str(ind) for ind in i]
    af = AnnoteFinder(x,y,indexstrings)
    pylab.connect('button_press_event', af)
    return
    
def labelindex_subplot(ax,i,x,y): 
    indexstrings = [str(ind) for ind in i]
    af = AnnoteFinder(x,y,indexstrings)
    pylab.connect('button_press_event', af)
    return

def annotate_plot(frame,plot_col,label_col):
    frame = frame[frame[label_col].isnull()!=True]
    for label, x, y in zip(frame['fieldnotes'], frame.index, frame['TSS (mg/L)']):
            plt.annotate(label, xy=(x, y))
            
def scaleSeries(series,new_scale=[100,10]):
    new_scale = new_scale
    OldRange = (series.max() - series.min())  
    NewRange = (new_scale[0] - new_scale[1])  
    NewSeriesValues = (((series - series.min()) * NewRange) / OldRange) + new_scale[1]
    return NewSeriesValues            

def powerfunction(x,y,name='power rating'):
    datadf = pd.DataFrame.from_dict({'x':x,'y':y}).dropna().apply(np.log10) ## put x and y in a dataframe so you can drop ones that don't match up    
    datadf = datadf[datadf>=-10] ##verify data is valid (not inf)
    regression = pd.ols(y=datadf['y'],x=datadf['x'])
    pearson = pearson_r(datadf['x'],datadf['y'])[0]
    spearman = spearman_r(datadf['x'],datadf['y'])[0]
    coeffdf = pd.DataFrame({'a':[10**regression.beta[1]],'b':[regression.beta[0]],'r2':[regression.r2],'rmse':[regression.rmse],'pearson':[pearson],'spearman':[spearman]},index=[name])
    return coeffdf

def PowerFit(x,y,xspace=None,ax=plt,**kwargs):
    datadf = pd.DataFrame.from_dict({'x':x,'y':y}).dropna().apply(np.log10) ## put x and y in a dataframe so you can drop ones that don't match up    
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

def nonlinearfunction(x,y,order=2):
    datadf = pd.DataFrame.from_dict({'x':x,'y':y}).dropna() ## put x and y in a dataframe so you can drop ones that don't match up    
    datadf = datadf[datadf>=0].dropna() ##verify data is valid (not inf)
    PolyCoeffs = np.polyfit(datadf['x'], datadf['y'], order) ## calculates polynomial coeffs
    PolyEq = np.poly1d(PolyCoeffs) ## turns the coeffs into an equation
    return PolyEq

def NonlinearFit(x,y,order=2,subplotax=None):
    linfunc = nonlinearfunction(x,y,order)
    #print linfunc
    xvals = np.linspace(x.min(),x.max())
    ypred = linfunc(xvals)
    if subplotax == True:
        subplotax.plot(xvals,ypred)
    else:
        plt.plot(xvals,ypred)
    return linfunc
## test
#x= np.linspace(1.0,10.0,10)
#y = 10*x + 15
#name = 'x2' 
#plt.scatter(x,x2)
#xnonlinfun = nonlinearfunction(x,x2)
#xnonlinear = NonlinearFit(x,x2)
    
#### Define Storm Periods #####
## Define Storm Intervals
DefineStormIntervalsBy = {'User':'User','Separately':'BOTH','N1':'N1','N2':'N2'}
StormIntervalDef = DefineStormIntervalsBy['N2']
    
from HydrographTools import SeparateHydrograph, StormSums
## Define by Threshold = Mean Stage+ 1 Std Stage
N1_storm_threshold = PT1['stage'].describe()[1]+PT1['stage'].describe()[2] 
N2_storm_threshold = PT2['stage'].describe()[1]+PT2['stage'].describe()[2]


if StormIntervalDef=='N2' or StormIntervalDef=='Separately':
    ## Define Storm Intervals at N2
    N2_StormIntervals=DataFrame(SeparateHydrograph(hydrodata=PT2['stage']))
    ## Combine Storm Events where the storm end is the storm start for the next storm
    N2_StormIntervals['next storm start']=N2_StormIntervals['start'].shift(-1) ## add the next storm's start and end time to the storm in the row above (the previous storm)
    N2_StormIntervals['next storm end']=N2_StormIntervals['end'].shift(-1)
    need_to_combine =N2_StormIntervals[N2_StormIntervals['end']==N2_StormIntervals['next storm start']] #storms need to be combined if their end is the same time as the next storm's start
    need_to_combine['end']=need_to_combine['next storm end'] # change the end of the storm to the end of the next storm to combine them
    N2_StormIntervals=N2_StormIntervals.drop(need_to_combine.index) #drop the storms that need to be combined
    N2_StormIntervals=N2_StormIntervals.append(need_to_combine).sort(ascending=True) #append back in the combined storms
    N2_StormIntervals=N2_StormIntervals.drop_duplicates(cols=['end']) #drop the second storm that was combined
    StormIntervals = N2_StormIntervals    
    
## Use User-defined storm intervals
if StormIntervalDef=='User':
    stormintervalsXL = pd.ExcelFile(datadir+'StormIntervals.xlsx')
    StormIntervals = stormintervalsXL.parse('StormIntervals',header=0,parse_cols='A:C',index_col=0)
    N2_StormIntervals=StormIntervals
    N1_StormIntervals=StormIntervals

def showstormintervals(ax,storm_threshold=N2_storm_threshold,showStorms=StormIntervals,shade_color='grey',show=True):
    ## Storms
    if show==True:
        print 'Storm threshold stage= '+'%.1f'%storm_threshold+' cm'
        #ax.axhline(y=storm_threshold,ls='--',color=shade_color)    
        for storm in showStorms.iterrows(): ## shade over storm intervals
            ax.axvspan(storm[1]['start'],storm[1]['end'],ymin=0,ymax=200,facecolor=shade_color, alpha=0.25)
    return

from precip_data import raingauge, AddTimu1, AddTimu1Hourly, AddTimu1Daily, AddTimu1Monthly

def plotSTAGE(show=False):
    fig, stage = plt.subplots(1)
    title="Stage for PT's in Nu'uuli Stream"
    #### PT1 stage N1
    stage.plot_date(PT1['stage'].index,PT1['stage'],marker='None',ls='-',color='r',label='N1')
    print 'Lowest PT1 stage: '+'%.1f'%PT1['stage'].min()
    #### PT2 stage N2
    stage.plot_date(PT2['stage'].index,PT2['stage'],marker='None',ls='-',color='y',label='N2')

    ## show storm intervals?
    showstormintervals(stage,shade_color='g',show=True)
    
    #### Format X axis and Primary Y axis
    stage.set_title(title)
    stage.set_ylabel('Stage height in cm')
    stage.set_ylim(0,145)
    stage.legend(loc=2)
    #### Add Precip data from Timu1
    AddTimu1(fig,stage,Precip['Timu-Nuuuli1-15'])
    AddTimu1(fig,stage,Precip['Timu-Nuuuli2-15'],LineColor='g')
    
    plt.setp(stage.get_xticklabels(),rotation='vertical',fontsize=9)
    plt.subplots_adjust(left=0.1,right=0.83,top=0.93,bottom=0.15)
    #### Legend
    plt.legend(loc=1)
    fig.canvas.manager.set_window_title('Figure 1: '+title) 
    stage.grid(True)
    show_plot(show)
    return
plotSTAGE(True)

def plotPRECIP(show=False):
    fig = plt.figure(2)

    Precip['Timu-Nuuuli1-hourly'].dropna().plot(label='N1 Precip Hourly',color='g',linestyle='steps-mid',ls='--')
    Precip['Timu-Nuuuli1-daily'].dropna().plot(label='N1 Precip Daily',color='g',linestyle='steps-post')
    
    Precip['Timu-Nuuuli2-hourly'].dropna().plot(label='N2 Precip Hourly',color='r',linestyle='steps-mid',ls='--')
    Precip['Timu-Nuuuli2-daily'].dropna().plot(label='N2 Precip Daily',color='r',linestyle='steps-post')
    
    #PrecipMonthly = Timu1monthly.plot(label='Precip Monthly',color='k',linestyle='steps-post')    
    plt.axes().xaxis_date()
    plt.setp(plt.axes().get_xticklabels(), rotation=45, fontsize=9)
    plt.ylabel('Precipitation (mm)')
    fig.canvas.manager.set_window_title('Figure 2: Precipitation(mm)') 
    plt.legend(),plt.grid(True)
    if show==True:
        plt.show()
    return
plotPRECIP(True)


#### Analyze Storm Precip Characteristics: Intensity, Erosivity Index etc. ####
def StormPrecipAnalysis(StormIntervals):
    #### EROSIVITY INDEX for storms (ENGLISH UNITS)
    stormlist=[]
    for storm in StormIntervals.iterrows():
        index = storm[1]['start']
        start = storm[1]['start']-dt.timedelta(minutes=60) ## storm start is when PT exceeds threshold, retrieve Precip x min. prior to this.
        end =  storm[1]['end'] ## when to end the storm?? falling limb takes too long I think
        try:
            rain_data = pd.DataFrame.from_dict({'Timu':Precip['Timu-Nuuuli2'][start:end]})
            rain_data['AccumulativeDepth mm']=(rain_data['Timu']).cumsum() ## cumulative depth at 1 min. intervals
            rain_data['AccumulativeDepth in.']=(rain_data['Timu']/25.4).cumsum() ## cumulative depth at 1 min. intervals
            rain_data['Intensity (in./hr)']=rain_data['Timu']*60 ## intensity at each minute
            rain_data['30minMax (in./hr)']=m.rolling_sum(Precip['Timu-Nuuuli2'],window=30)/25.4
            I30 = rain_data['30minMax (in./hr)'].max()
            duration_hours = (end - start).days * 24 + (end - start).seconds//3600
            I = (rain_data['Timu'].sum())/25.4/duration_hours ## I = Storm Average Intensity
            E = 1099 * (1-(0.72*math.exp(-1.27*I))) ## E = Rain Kinetic Energy
            EI = E*I30
            stormlist.append((index,[rain_data['Timu'].sum()/25.4,duration_hours,I30,I,E,EI]))
        except:
            print "Can't analyze Storm Precip for storm:"+str(start)
            pass
    Stormdf = pd.DataFrame.from_items(stormlist,orient='index',columns=['Total(in)','Duration(hrs)','Max30minIntensity(in/hr)','AvgIntensity(in/hr)','E-RainKineticEnergy(ft-tons/acre/inch)','EI'])
    Stormdf = Stormdf[(Stormdf['Total(in)']>0.0)] ## filter out storms without good Timu1 data
    return Stormdf
    
N2_Stormdf = StormPrecipAnalysis(N2_StormIntervals)

## STAGE DATA FOR PT's
Nuuuli_stage_data = pd.DataFrame({'N1':PT1['stage'],'N2':PT2['stage']})

#### STAGE TO DISCHARGE ####
order=1
powerlaw = False
from AV_RatingCurve import AV_RatingCurve
## Q = a(stage)**b
def power(x,a,b):
    y = a*(x**b)
    return y

### Area Velocity and Mannings from in situ measurments
## stage2discharge_ratingcurve.AV_rating_curve(datadir,location,stage_data,trapezoid=False,Slope=0.01,Mannings_n=0.03,width=4.9276)
## Returns DataFrame of Stage (cm) and Discharge (L/sec) calc. from AV measurements with time index

#### N1 (rating curves:A measurment * Mannings V, Area of Rectangular section * Mannings V)
Slope = 0.013# m/m
Mannings_n=0.050 # Mountain stream rocky bed and rivers with variable sections and veg along banks (Dunne 1978)
#DataFrame with Q from AV measurements, Q from measured A with Manning-predicted V, stage, and Q from Manning's and assumed rectangular channel A
N1stageDischarge = AV_RatingCurve(datadir+'Q/','N1',Nuuuli_stage_data,slope=Slope,n=Mannings_n,trapezoid=True)

N1_AManningV = pd.ols(y=N1stageDischarge['Q-AManningV(L/sec)'],x=N1stageDischarge['stage(cm)'],intercept=True)
N1_AManningVLog = pd.ols(y=N1stageDischargeLog['Q-AManningV(L/sec)'],x=N1stageDischargeLog['stage(cm)'],intercept=True)
N1_Mannings = pd.ols(y=N1stageDischarge['Q-Mannings(L/sec)'],x=N1stageDischarge['stage(cm)'],intercept=True) ## Rectangular channel
N1_ManningsLog = pd.ols(y=N1stageDischargeLog['Q-Mannings(L/sec)'],x=N1stageDischargeLog['stage(cm)'],intercept=True) ## Rectangular channel

