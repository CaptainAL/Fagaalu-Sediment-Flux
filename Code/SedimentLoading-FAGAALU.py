#### LOAD DATA FIRST
## OPEN AND RUN "StartHere-LoadDataForSession.py"


# -*- coding: utf-8 -*-
"""
Created Aug 2014 (migrated to Github)

This code opens relevant precipitation, stream pressure transducer, stream flow measurement (A/V), turbidimeter, etc. data
to calculate the sediment loading at stream gauging locations in Faga'alu watershed


@author: Alex Messina
"""
#### Import modules
import sys
if 'XL' not in locals(): ## XL is the Master_Data.xlsx file
    sys.exit("Need to load data first. Run 'StartHere-LoadData....'")
    

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

#### Define Storm Periods #####
## Define Storm Intervals at LBJ
DefineStormIntervalsBy = {'User':'User','Separately':'BOTH','DAM':'DAM','LBJ':'LBJ'}
StormIntervalDef = DefineStormIntervalsBy['LBJ']

from HydrographTools import SeparateHydrograph, StormSums
## Define by Threshold = Mean Stage+ 1 Std Stage
LBJ_storm_threshold = PT1['stage'].describe()[1]+PT1['stage'].describe()[2] 
DAM_storm_threshold = PT3['stage'].describe()[1]+PT3['stage'].describe()[2]

if StormIntervalDef=='LBJ' or StormIntervalDef=='BOTH':
    ## Define Storm Intervals at LBJ
    LBJ_StormIntervals=DataFrame(SeparateHydrograph(hydrodata=PT1['stage']))
    ## Combine Storm Events where the storm end is the storm start for the next storm
    LBJ_StormIntervals['next storm start']=LBJ_StormIntervals['start'].shift(-1) ## add the next storm's start and end time to the storm in the row above (the previous storm)
    LBJ_StormIntervals['next storm end']=LBJ_StormIntervals['end'].shift(-1)
    need_to_combine =LBJ_StormIntervals[LBJ_StormIntervals['end']==LBJ_StormIntervals['next storm start']] #storms need to be combined if their end is the same time as the next storm's start
    need_to_combine['end']=need_to_combine['next storm end'] # change the end of the storm to the end of the next storm to combine them
    LBJ_StormIntervals=LBJ_StormIntervals.drop(need_to_combine.index) #drop the storms that need to be combined
    LBJ_StormIntervals=LBJ_StormIntervals.append(need_to_combine).sort(ascending=True) #append back in the combined storms
    LBJ_StormIntervals=LBJ_StormIntervals.drop_duplicates(cols=['end']) #drop the second storm that was combined

if StormIntervalDef == 'DAM'or StormIntervalDef=='BOTH':  
    ## Define Storm Intervals at DAM
    DAM_StormIntervals=DataFrame(SeparateHydrograph(hydrodata=PT3['stage']))
    ## Combine Storm Events where the storm end is the storm start for the next storm
    DAM_StormIntervals['next storm start']=DAM_StormIntervals['start'].shift(-1) ## add the next storm's start and end time to the storm in the row above (the previous storm)
    DAM_StormIntervals['next storm end']=DAM_StormIntervals['end'].shift(-1)
    need_to_combine =DAM_StormIntervals[DAM_StormIntervals['end']==DAM_StormIntervals['next storm start']] #storms need to be combined if their end is the same time as the next storm's start
    need_to_combine['end']=need_to_combine['next storm end'] # change the end of the storm to the end of the next storm to combine them
    DAM_StormIntervals=DAM_StormIntervals.drop(need_to_combine.index) #drop the storms that need to be combined
    DAM_StormIntervals=DAM_StormIntervals.append(need_to_combine).sort(ascending=True) #append back in the combined storms
    DAM_StormIntervals=DAM_StormIntervals.drop_duplicates(cols=['end']) 

## Take just one definition of Storm Intervals....
if StormIntervalDef=='DAM':    
    LBJ_StormIntervals=DAM_StormIntervals 
    StormIntervals=LBJ_StormIntervals    
if StormIntervalDef=='LBJ':    
    DAM_StormIntervals=LBJ_StormIntervals     
    StormIntervals=LBJ_StormIntervals    
## Use User-defined storm intervals
if StormIntervalDef=='User':
    stormintervalsXL = pd.ExcelFile(datadir+'StormIntervals.xlsx')
    StormIntervals = stormintervalsXL.parse('StormIntervals',header=0,parse_cols='A:C',index_col=0)
    LBJ_StormIntervals, DAM_StormIntervals = StormIntervals, StormIntervals

    
def showstormintervals(ax,storm_threshold=LBJ_storm_threshold,showStorms=StormIntervals,shade_color='grey',show=True):
    ## Storms
    if show==True:
        if storm_threshold==True:
            print 'Storm threshold stage= '+ '%.'%storm_threshold   
            ax.axhline(y=storm_threshold,ls='--',color=shade_color)    
        for storm in showStorms.iterrows(): ## shade over storm intervals
            ax.axvspan(storm[1]['start'],storm[1]['end'],ymin=0,ymax=200,facecolor=shade_color, alpha=0.25)
    return


#### Analyze Storm Precip Characteristics: Intensity, Erosivity Index etc. ####
def StormPrecipAnalysis(storms=StormIntervals):
    storms=StormIntervals
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
DAM_Stormdf = StormPrecipAnalysis(storms=DAM_StormIntervals)

#### STAGE TO DISCHARGE ####
from stage2discharge_ratingcurve import AV_RatingCurve, calcQ, Mannings_rect, Weir_rect, Weir_vnotch, Flume
### Area Velocity and Mannings from in situ measurments
## stage2discharge_ratingcurve.AV_rating_curve(datadir,location,Fagaalu_stage_data,trapezoid=False,Slope=0.01,Mannings_n=0.03,width=4.9276)
## Returns DataFrame of Stage (cm) and Discharge (L/sec) calc. from AV measurements with time index

#### LBJ (3 rating curves: AV measurements, A measurment * Mannings V, Area of Rectangular section * Mannings V)
Slope = 0.0161 # m/m
n=0.050 # Mountain stream rocky bed and rivers with variable sections and veg along banks (Dunne 1978)
### Calculate Q from a single AV measurement
#fileQ = calcQ(datadir+'Q/LBJ_4-18-13.txt','LBJ',Fagaalu_stage_data,slope=Slope,Mannings_n=n,trapezoid=True)
### and save to CSV
#pd.concat(fileQ).to_csv(datadir+'Q/LBJ_4-18-13.csv')

## LBJ AV measurements
LBJstageDischarge = AV_RatingCurve(datadir+'Q/','LBJ',Fagaalu_stage_data,slope=Slope,Mannings_n=n,trapezoid=True).dropna() #DataFrame with Q from AV measurements, Q from measured A with Manning-predicted V, stage, and Q from Manning's and assumed rectangular channel A
LBJstageDischarge = LBJstageDischarge.truncate(before=datetime.datetime(2012,3,20)) # throw out measurements when I didn't know how to use the flow meter very well
LBJstageDischargeLog = LBJstageDischarge.apply(np.log10) #log-transformed version

## LBJ: Q Models 
## Linear
LBJ_AV= pd.ols(y=LBJstageDischarge['Q-AV(L/sec)'],x=LBJstageDischarge['stage(cm)'],intercept=True) 
## Power
LBJ_AVLog= pd.ols(y=LBJstageDischargeLog['Q-AV(L/sec)'],x=LBJstageDischargeLog['stage(cm)'],intercept=True) #linear fit to log-transformed stage and Q
## Linear with Mannings
LBJ_AManningV = pd.ols(y=LBJstageDischarge['Q-AManningV(L/sec)'],x=LBJstageDischarge['stage(cm)'],intercept=True)
## Power with Mannings
LBJ_AManningVLog = pd.ols(y=LBJstageDischargeLog['Q-AManningV(L/sec)'],x=LBJstageDischargeLog['stage(cm)'],intercept=True)

## Fit nonlinear wiht intercept zero
for _ in range(3):## add zero/zero intercept
    LBJstageDischarge=LBJstageDischarge.append(pd.DataFrame({'stage(cm)':0,'Q-AV(L/sec)':0},index=[np.random.rand()])) 
LBJ_AVnonLinear = nonlinearfunction(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AV(L/sec)'],order=3,interceptZero=False)  
LBJstageDischarge=LBJstageDischarge.dropna() ## get rid of zero/zero interctp

for _ in range(3):## add zero/zero intercept
    LBJstageDischarge=LBJstageDischarge.append(pd.DataFrame({'stage(cm)':0,'Q-AManningV(L/sec)':0},index=[np.random.rand()])) 
LBJ_AManningVnonLinear = nonlinearfunction(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AManningV(L/sec)'],order=3,interceptZero=False)
LBJstageDischarge=LBJstageDischarge.dropna() ## get rid of zero/zero interctp

## LBJ: Q from OrangePeel method 
from notebook import OrangePeel
orangepeel = OrangePeel('OrangePeel',1,datadir+'Q/Fagaalu-StageDischarge.xlsx')
orangepeel=orangepeel.append(pd.DataFrame({'stage cm':0,'L/sec':0},index=[pd.NaT]))


## LBJ: Mannings from Xsection
from ManningsRatingCurve import Mannings, Mannings_Series
LBJ_Man = Mannings_Series(datadir+'Q/LBJ_cross_section.xlsx','LBJ_m',Slope=0.016,Manning_n=0.08,stage_series=Fagaalu_stage_data['LBJ'])
DAM_Man = Mannings_Series(datadir+'Q/LBJ_cross_section.xlsx','DAM_m',Slope=0.03,Manning_n=0.08,stage_series=Fagaalu_stage_data['Dam'])


## DAM AV Measurements
DAMstageDischarge = AV_RatingCurve(datadir+'Q/','Dam',Fagaalu_stage_data) ### Returns DataFrame of Stage and Discharge calc. from AV measurements with time index
DAMstageDischargeLog=DAMstageDischarge.apply(np.log10) #log-transformed version

## DAM: Q Models
## Linear
DAM_AV = pd.ols(y=DAMstageDischarge['Q-AV(L/sec)'],x=DAMstageDischarge['stage(cm)'],intercept=True) 
## Power
DAM_AVLog = pd.ols(y=DAMstageDischargeLog['Q-AV(L/sec)'],x=DAMstageDischargeLog['stage(cm)'],intercept=True) 

## HEC-RAS Model of the DAM structure: Documents/HEC/FagaaluDam.prj
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

def plotStageDischargeRatings(show=False,log=False,save=False): ## Rating Curves
    fig =plt.figure()
    ax = plt.subplot(2,2,1)
    site_lbj = plt.subplot2grid((2,2),(0,0))
    site_dam = plt.subplot2grid((2,2),(1,0))
    both = plt.subplot2grid((2,2),(0,1),rowspan=2)
    mpl.rc('lines',markersize=15)
    
    title="Stage-Discharge Relationships for LBJ and DAM"
    xy = np.linspace(0,150,150)
    
    #LBJ AV Measurements and Rating Curve
    site_lbj.plot(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AV(L/sec)'],'.',color='r',markeredgecolor='k',label='LBJ_AV')   
    #LBJ A*ManningV Measurements and Rating Curves
    site_lbj.plot(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AManningV(L/sec)'],'.',color='grey',markeredgecolor='k',label='LBJ A*ManningsV')

    ## LBJ MODELS
    ## LBJ Linear    
    LBJ_AVlinear= linearfunction(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AV(L/sec)'])    
    LinearFit(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AV(L/sec)'],xy,site_lbj,c='r',ls='--',label='LBJ_AVlinear '+r'$r^2$'+"%.2f"%LBJ_AVlinear['r2'])
    ## LBJ Power
    LBJ_AVpower = powerfunction(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AV(L/sec)'])    
    PowerFit(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AV(L/sec)'],xy,site_lbj,c='r',ls='-.',label='LBJ_AVpower '+r'$r^2$'+"%.2f"%LBJ_AVpower['r2'])    
    ## LBJ NonLinear
    site_lbj.plot(xy,LBJ_AVnonLinear(xy),color='r',ls='-',label='LBJ_AVnonLinear')    
    ## LBJ Mannings Linear    
    LBJ_MANlinear=linearfunction(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AManningV(L/sec)'])
    LinearFit(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AManningV(L/sec)'],xy,site_lbj,c='grey',ls='--',label='LBJ_MANlinear') ## rating from LBJ_AManningV
    ## LBJ Manning Power    
    LBJ_MANpower =powerfunction(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AManningV(L/sec)'])    
    PowerFit(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AManningV(L/sec)'],xy,site_lbj,c='grey',ls='-.',label='LBJ_MANpower') ## rating from LBJ_AManningVLog
    ## LBJ Manning NonLinear    
    site_lbj.plot(xy,LBJ_AManningVnonLinear(xy),color='grey',ls='-',label='LBJ_AManningVnonLinear')
    
    #DAM AV Measurements and Rating Curve
    site_dam.plot(DAMstageDischarge['stage(cm)'],DAMstageDischarge['Q-AV(L/sec)'],'.',color='g',markeredgecolor='k',label='DAM_AV')
    ## DAM Linear
    DAM_AVlinear=linearfunction(DAMstageDischarge['stage(cm)'],DAMstageDischarge['Q-AV(L/sec)'])    
    LinearFit(DAMstageDischarge['stage(cm)'],DAMstageDischarge['Q-AV(L/sec)'],xy,site_dam,c='g',ls='--',label='DAM_AVlinear '+r'$r^2$'+"%.2f"%DAM_AVlinear['r2']) ## rating from DAM_AVLog
    ## DAM Power    
    DAM_AVpower=powerfunction(DAMstageDischarge['stage(cm)'],DAMstageDischarge['Q-AV(L/sec)'])    
    PowerFit(DAMstageDischarge['stage(cm)'],DAMstageDischarge['Q-AV(L/sec)'],xy,site_dam,c='g',ls='-.', label='DAM AV '+r'$r^2$'+"%.2f"%DAM_AVpower['r2']) ## rating from DAM_AV
    #DAM HEC-RAS Model and Rating Curve
    #LinearFit(DAM_HECstageDischarge['stage(cm)'],DAM_HECstageDischarge['Q_HEC(L/sec)'],xy,site_dam,c='b',ls='-',label='DAM_HEClinear') ## rating from DAM_HEC
    #PowerFit(DAM_HECstageDischarge['stage(cm)'],DAM_HECstageDischarge['Q_HEC(L/sec)'],xy,site_dam,c='b',ls='--',label='DAM_HECpower') ## rating from DAM_HEC
    site_dam.plot(DAM_HECstageDischarge['stage(cm)'],DAM_HECstageDischarge['Q_HEC(L/sec)'],'-',color='b',label='DAM HEC-RAS Model')
    
    ## Plot selected rating curves for LBJ and DAM
    ## AV measurements
    both.plot(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AV(L/sec)'],'.',color='r',markeredgecolor='k',label='VILLAGE A-V')  
    both.plot(DAMstageDischarge['stage(cm)'],DAMstageDischarge['Q-AV(L/sec)'],'.',color='g',markeredgecolor='k',label='FOREST A-V')    
    ## LBJ Nonlinear Model
    both.plot(xy,LBJ_AVnonLinear(xy),color='r',ls='--',label='LBJ_AVnonLinear')    
    both.plot(xy,LBJ_AManningVnonLinear(xy),color='r',ls='-',label='LBJ_AManningVnonLinear')
    both.plot(LBJ_Man['stage']*100,LBJ_Man['Q']*1000,ls='None',marker='o',markersize=4,color='b')
        
    ## DAM HEC-RAS Model 
    both.plot(xy, HEC_piecewise(xy),'-',color='g',label='DAM HEC-RAS piecewise')

    ## Label subplots    
    site_lbj.set_title('VILLLAGE'),site_lbj.set_xlabel('Stage(cm)'),site_lbj.set_ylabel('Q(L/sec)')
    site_dam.set_title('FOREST'),site_dam.set_xlabel('Stage(cm)'),site_dam.set_ylabel('Q(L/sec)')
    both.set_title('Selected Ratings'),both.set_xlabel('Stage(cm)'),both.set_ylabel('Q(L/sec)'),both.yaxis.tick_right(),both.yaxis.set_label_position('right')
    ## Format subplots
    site_lbj.set_xlim(0,PT1['stage'].max()+10),site_lbj.set_ylim(0,LBJ_AVnonLinear(PT1['stage'].max()+10))
    site_dam.set_xlim(0,PT3['stage'].max()+10),site_dam.set_ylim(0,HEC_piecewise(PT3['stage'].max()+10).values)
    ## Legends
    site_lbj.legend(loc='best',ncol=2,fancybox=True),site_dam.legend(loc='best',ncol=2,fancybox=True),both.legend(loc='best',ncol=2,fancybox=True)
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
plotStageDischargeRatings(show=True,log=False,save=False)
#plotStageDischargeRatings(show=True,log=False,save=True)
#plotStageDischargeRatings(show=True,log=True,save=True)

#### CALCULATE DISCHARGE
## Calculate Q for LBJ
## Stage
LBJ = DataFrame(PT1,columns=['stage']) ## Build DataFrame with all stage records for location (cm)
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
## Linear Model
DAM['Q-AV']=(DAM['stage']*DAM_AV.beta[0]) + DAM_AV.beta[1] ## Calculate Q from AV rating=
## Power Model
a,b = 10**DAM_AVLog.beta[1], DAM_AVLog.beta[0]
DAM['Q-AVLog']=(a)*(DAM['stage']**b) 
## HEC-RAS Model
DAM['Q-HEC']= HEC_piecewise(DAM['stage'])

#### CHOOSE Q RATING CURVE

LBJ['Q']=LBJ_AManningVnonLinear(LBJ['stage'])
print 'LBJ Q from Area * Manning V (NonLinear fit)'


DAM['Q']= HEC_piecewise(DAM['stage'])
print 'DAM Q from HEC-RAS piecewise'


LBJ['Q']= LBJ_Man['Q']*1000
DAM['Q']= LBJ_Man['Q']*1000


#### Calculate Q for QUARRY


## Convert to 15min interval LBJ
LBJq = (LBJ*900) ## Q above is in L/sec; L/sec * 900sec/15Min = L/15Min
LBJq['stage']=PT1['stage'] ## put unaltered stage back in

## Convert to 15min interval DAM
DAMq= (DAM*900)## Q above is in L/sec; L/sec * 900sec/15Min = L/15Min
DAMq['stage']=PT3['stage'] ## put unaltered stage back in


#### Integrate over P and Q over Storm Event
from HydrographTools import StormSums
## LBJ
Pstorms_LBJ = StormSums(LBJ_StormIntervals,PrecipFilled['Precip'],60) ##30minute offset to get precip before stage started rising
Pstorms_LBJ.columns=['Pstart','Pend','Pcount','Psum','Pmax']
Pstorms_LBJ['EI'] = LBJ_Stormdf['EI']
Qstorms_LBJ=StormSums(LBJ_StormIntervals,LBJq['Q']) 
Qstorms_LBJ.columns=['Qstart','Qend','Qcount','Qsum','Qmax']
Qstorms_LBJ['Qmax']=Qstorms_LBJ['Qmax']/900 ## Have to divide by 900 to get instantaneous 
## DAM
Pstorms_DAM = StormSums(DAM_StormIntervals,PrecipFilled['Precip'],60) ##30minute offset to get precip before stage started rising
Pstorms_DAM.columns=['Pstart','Pend','Pcount','Psum','Pmax']
Pstorms_DAM['EI'] = DAM_Stormdf['EI']
Qstorms_DAM= StormSums(DAM_StormIntervals,DAMq['Q']) 
Qstorms_DAM.columns=['Qstart','Qend','Qcount','Qsum','Qmax']
Qstorms_DAM['Qmax']=Qstorms_DAM['Qmax']/900 ## Have to divide by 900 to get instantaneous 

## Event Runoff Coefficient
StormsLBJ = Pstorms_LBJ[Pstorms_LBJ['Psum']>0].join(Qstorms_LBJ)
## Event precip x Area = Event Precip Volume: Psum/1000 (mm to m) * 1.78*1000000 (km2 to m2) *1000 (m3 to L)
StormsLBJ['PsumVol'] = (StormsLBJ['Psum']/1000)*(1.78*1000000)*1000  
StormsLBJ['RunoffCoeff']=StormsLBJ['Qsum']/StormsLBJ['PsumVol']

StormsDAM=Pstorms_DAM[Pstorms_DAM['Psum']>0].join(Qstorms_DAM)
StormsDAM['PsumVol'] = (StormsDAM['Psum']/1000)*(0.9*1000000)*1000  
StormsDAM['RunoffCoeff']=StormsDAM['Qsum']/StormsDAM['PsumVol']


#### SSC ANALYSIS
SampleCounts = DataFrame(data=[str(val) for val in pd.unique(TSS['Location'])],columns=['Location'])
SampleCounts['#ofTSSsamples']=pd.Series([len(TSS[TSS['Location']==str(val)]) for val in pd.unique(TSS['Location'])]) ##add column of Locations

### SSC Sample Counts from Unique Sites
## from SampleCounts select rows where SampleCounts['Location'] starts with 'Quarry'; sum up the #ofTSSsamples column
AllQuarrySamples = pd.DataFrame(data=[[SampleCounts[SampleCounts['Location'].str.startswith('Quarry')]['#ofTSSsamples'].sum(),'AllQuarry']],columns=['#ofTSSsamples','Location']) ## make DataFrame of the sum of all records that Location starts wtih 'Quarry'
SampleCounts = SampleCounts.append(AllQuarrySamples)
## drop the columns that were counted above to get a DataFrame of unique sampling locations
SampleCounts= SampleCounts.drop(SampleCounts[SampleCounts['Location'].str.startswith(('N1','N2','Quarry'))].index)
SampleCounts.index=range(1,len(SampleCounts)+1)

## SSC Boxplots and Discharge Concentration
LBJgrab = TSS['TSS (mg/L)'][TSS['Location'].isin(['LBJ'])].resample('15Min',fill_method='pad',limit=0)
DTgrab =TSS['TSS (mg/L)'][TSS['Location'].isin(['DT','R2'])].resample('15Min',fill_method='pad',limit=0)
DAMgrab = TSS['TSS (mg/L)'][TSS['Location'].isin(['DAM'])].resample('15Min',fill_method='pad',limit=0)
GrabSamples = pd.concat([DAMgrab,DTgrab,LBJgrab],axis=1)
GrabSamples.columns = ['DAM','DT','LBJ']
GrabSampleMeans = [DAMgrab.mean(),DTgrab.mean(),LBJgrab.mean()]
GrabSampleVals = np.concatenate([DAMgrab.values.tolist(),DTgrab.values.tolist(),LBJgrab.values.tolist()])
GrabSampleCategories = np.concatenate([[1]*len(DAMgrab),[2]*len(DTgrab),[3]*len(LBJgrab)])

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
    
dam_ssc = pd.DataFrame(TSS[TSS['Location']=='DAM']['TSS (mg/L)']).resample('15Min')
dam_ssc['Q']=DAM['Q']
dam_ssc = dam_ssc.dropna()
dam_ssc2012,dam_ssc2013,dam_ssc2014 = dam_ssc[start2012:stop2012],dam_ssc[start2013:stop2013],dam_ssc[start2014:stop2014]

dt_ssc = pd.DataFrame(TSS[TSS['Location'].isin(['DT','R2'])]['TSS (mg/L)']).resample('15Min')
dt_ssc['Q']=DAM['Q']
dt_ssc =dt_ssc.dropna()
dt2012,dt2013,dt2014 = dt_ssc[start2012:stop2012],dt_ssc[start2013:stop2013],dt_ssc[start2014:stop2014]

lbj_ssc = pd.DataFrame(TSS[TSS['Location']=='LBJ']['TSS (mg/L)']).resample('15Min')
lbj_ssc['Q']=LBJ['Q']
lbj_ssc=lbj_ssc.dropna()
lbj_ssc2012,lbj_ssc2013,lbj_ssc2014 = lbj_ssc[start2012:stop2012],lbj_ssc[start2013:stop2013],lbj_ssc[start2014:stop2014]

damQC = pd.ols(y=dam_ssc['TSS (mg/L)'],x=dam_ssc['Q'])
lbjQC = pd.ols(y=lbj_ssc['TSS (mg/L)'],x=lbj_ssc['Q'])

def plotQvsC(ms=6,show=False,log=False,save=True):
    #fig, ((down_ex,up_ex),(down,up)) = plt.subplots(2,2,sharey='row',sharex='col') 
    fig=plt.figure()
    gs = gridspec.GridSpec(2,2,height_ratios=[1,3])
    up_ex,down_ex = plt.subplot(gs[0]),plt.subplot(gs[1])
    up,down = plt.subplot(gs[2],sharex=up_ex),plt.subplot(gs[3],sharex=down_ex)
    mpl.rc('lines',markersize=ms)
    ## plot LBJ samples
    down.plot(lbj_ssc2012['Q'],lbj_ssc2012['TSS (mg/L)'],'.',c='g',label='VILLAGE 2012')
    down.plot(lbj_ssc2013['Q'],lbj_ssc2013['TSS (mg/L)'],'.',c='y',label='VILLAGE 2013')
    down.plot(lbj_ssc2014['Q'],lbj_ssc2014['TSS (mg/L)'],'.',c='r',label='VILLAGE 2014')
    down_ex.plot(lbj_ssc2012['Q'],lbj_ssc2012['TSS (mg/L)'],'.',c='g',label='VILLAGE 2012')
    down_ex.plot(lbj_ssc2013['Q'],lbj_ssc2013['TSS (mg/L)'],'.',c='y',label='VILLAGE 2013')    
    down_ex.plot(lbj_ssc2014['Q'],lbj_ssc2014['TSS (mg/L)'],'.',c='r',label='VILLAGE 2014')
    ## plot DT samples
    down.plot(dt2012['Q'],dt2012['TSS (mg/L)'],'^',markersize=ms/2,c='g',label='QUARRY 2012')
    down.plot(dt2013['Q'],dt2013['TSS (mg/L)'],'^',markersize=ms/2,c='y',label='QUARRY 2013')
    down.plot(dt2014['Q'],dt2014['TSS (mg/L)'],'^',markersize=ms/2,c='r',label='QUARRY 2014')
    down_ex.plot(dt2012['Q'],dt2012['TSS (mg/L)'],'^',markersize=ms/2,c='g',label='QUARRY 2012')
    down_ex.plot(dt2013['Q'],dt2013['TSS (mg/L)'],'^',markersize=ms/2,c='y',label='QUARRY 2013')    
    down_ex.plot(dt2014['Q'],dt2014['TSS (mg/L)'],'^',markersize=ms/2,c='r',label='QUARRY 2014')
    ## plot DAM samples
    up.plot(dam_ssc2012['Q'],dam_ssc2012['TSS (mg/L)'],'.',c='g',label='DAM 2012')
    up.plot(dam_ssc2013['Q'],dam_ssc2013['TSS (mg/L)'],'.',c='y',label='DAM 2013')
    up.plot(dam_ssc2014['Q'],dam_ssc2014['TSS (mg/L)'],'.',c='r',label='DAM 2014')
    up_ex.plot(dam_ssc2012['Q'],dam_ssc2012['TSS (mg/L)'],'.',c='g',label='DAM 2012')
    up_ex.plot(dam_ssc2013['Q'],dam_ssc2013['TSS (mg/L)'],'.',c='y',label='DAM 2013')
    up_ex.plot(dam_ssc2014['Q'],dam_ssc2014['TSS (mg/L)'],'.',c='r',label='DAM 2014')
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
 
## Grab samples to SSYev   
def InterpolateGrabSamples(Stormslist,Data,offset=0):
    Events=pd.DataFrame()
    data=True
    for storm_index,storm in Stormslist.iterrows():
        #print storm
        start = storm['start']-datetime.timedelta(minutes=offset) ##if Storms are defined by stream response you have to grab the preceding precip data
        end= storm['end']
        try:
            event = Data.ix[start:end] ### slice list of Data for event
        except KeyError:
            print 'no data available for storm'
            data = False
            pass
        if data != False:
            event=event.reindex(pd.date_range(start,end,freq='15Min'))
            event[start] = 0
            event[end]=0
            Event=pd.DataFrame(event,columns=['Grab'])
            Event['GrabInterpolated']=Event['Grab'].interpolate('linear')
        Events = Events.append(Event)
    return Events
QuarryGrabSampleSSC=InterpolateGrabSamples(LBJ_StormIntervals, DTgrab,0)
#plt.plot_date(QuarryGrabSampleSSC.index,QuarryGrabSampleSSC['Grab'],marker='o',ls='None',color='y')
#plt.plot_date(QuarryGrabSampleSSC.index,QuarryGrabSampleSSC['GrabInterpolated'],marker='None',ls='-',color='y')


#### T to SSC rating curve for FIELD INSTRUMENTS
def T_SSCrating(TurbidimeterData,TSSdata,TurbidimeterName,location='LBJ',log=False):
    T_name = TurbidimeterName+'-NTU'
    TSSsamples = TSSdata[TSSdata['Location'].isin([location])].resample('5Min',fill_method = 'pad',limit=0) ## pulls just the samples matching the location name and roll to 5Min.
    TSSsamples = TSSsamples[pd.notnull(TSSsamples['TSS (mg/L)'])] ## gets rid of ones that mg/L is null
    TSSsamples[T_name]=TurbidimeterData['NTU']## grabs turbidimeter NTU data 
    TSSsamples = TSSsamples[pd.notnull(TSSsamples[T_name])]
    T_SSCrating = pd.ols(y=TSSsamples['TSS (mg/L)'],x=TSSsamples[T_name],intercept=True)
    return T_SSCrating,TSSsamples## Rating, Turbidity and Grab Sample TSS data

#### NTU to SSC rating curve from LAB ANALYSIS
T_SSC_Lab= pd.ols(y=TSS[TSS['Location']=='LBJ']['TSS (mg/L)'],x=TSS[TSS['Location']=='LBJ']['NTU'])
T_SSC_Lab= pd.ols(y=TSS['TSS (mg/L)'],x=TSS['NTU'])

## LBJ YSI and OBS
T_SSC_LBJ_YSI=T_SSCrating(LBJ_YSI,TSS,'LBJ-YSI','LBJ',log=False)
LBJ_YSIrating = T_SSC_LBJ_YSI[0]
 ## label=right because you want to average the values ahead of the interval and record the data at that instant.
T_SSC_LBJ_OBS=T_SSCrating(LBJ_OBS,TSS,'LBJ-OBS','LBJ',log=False)
LBJ_OBSrating = T_SSC_LBJ_OBS[0]
## resample to 15min to match Q records
LBJ_YSI15minute = LBJ_YSI.resample('15Min',how='mean',label='right')
LBJ_OBS15minute = LBJ_OBS.resample('15Min',how='mean',label='right')
LBJntu15minute = pd.DataFrame(pd.concat([LBJ_YSI15minute['NTU'],LBJ_OBS15minute['NTU']])).reindex(pd.date_range(start2012,stop2014,freq='15Min'))
#LBJntu = m.rolling_mean(LBJntu,window=3) ## Smooth out over 3 observations (45min) after already averaged to 5Min

## Dam TS3000 and YSI
T_SSC_DAM_TS3K=T_SSCrating(DAM_TS3K,TSS,'DAM-TS3K','DAM',log=False) ## Use 5minute data for NTU/TSS relationship
DAM_TS3Krating = T_SSC_DAM_TS3K[0]
T_SSC_DAM_YSI=T_SSCrating(DAM_YSI,TSS,'DAM-YSI','DAM',log=False) ## Won't work until there are some overlapping grab samples
DAM_YSIrating= T_SSC_DAM_YSI[0]
## resample to 15min to match Q records
DAM_TS3K15minute = DAM_TS3K.resample('15Min',how='mean',label='right') ## Resample to 15 minutes for the SedFlux calc
DAM_YSI15minute = DAM_YSI.resample('15Min',how='mean',label='right')
DAMntu15minute =  pd.DataFrame(pd.concat([DAM_TS3K15minute['NTU'],DAM_YSI15minute['NTU']])).reindex(pd.date_range(start2012,stop2014,freq='15Min'))

def plotNTU_BOTH(show=False,lwidth=0.5):
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
    tss = fig.add_axes(ntu.get_position(), frameon=False, sharex=ntu,sharey=ntu)
    LBJtss = TSS[TSS['Location']=='LBJ']
    tss.plot_date(LBJtss.index,LBJtss['TSS (mg/L)'],'.',markeredgecolor='grey',color='r',label='VILLAGE SSC grab')   
    DAMtss = TSS[TSS['Location']=='DAM']
    tss.plot_date(DAMtss.index,DAMtss['TSS (mg/L)'],'.',markeredgecolor='grey',color='g',label='FOREST SSC grab')    
    ##plot Grab samples used for rating
    tss.yaxis.set_ticks_position('right'),tss.yaxis.set_label_position('right')
    tss.set_ylabel('SSC (mg/L)'),tss.legend(loc='upper right')
    ## Shade storm intervals
    showstormintervals(precip)
    showstormintervals(Q)
    showstormintervals(ntu)

    precip.set_ylabel('Precip (mm/15min)'),precip.legend()
    Q.set_ylabel('Discharge (L/sec)'),Q.set_ylim(0,LBJ['Q'].max()+100),Q.legend()
    ntu.set_ylabel('Turbidity (NTU)'),ntu.set_ylim(0,LBJntu15minute['NTU'].max()),ntu.legend(loc='upper left')
    plt.suptitle('Precipitation, Discharge, Turbidity and SSC at FOREST and VILLAGE',fontsize=14)
    plt.draw()
    if show==True:
        plt.show()
    return
plotNTU_BOTH(True,lwidth=0.5)

def plotNTUratingstable(show=False,save=False):
    
    LAB = linearfunction(TSS[TSS['Location']=='LBJ']['NTU'],TSS[TSS['Location']=='LBJ']['TSS (mg/L)'])
    LBJ_YSI=linearfunction(T_SSC_LBJ_YSI[1]['LBJ-YSI-NTU'],T_SSC_LBJ_YSI[1]['TSS (mg/L)'])
    LBJ_OBS = linearfunction(T_SSC_LBJ_OBS[1]['LBJ-OBS-NTU'],T_SSC_LBJ_OBS[1]['TSS (mg/L)'])
    DAM_TS3K = linearfunction(T_SSC_DAM_TS3K[1]['DAM-TS3K-NTU'],T_SSC_DAM_TS3K[1]['TSS (mg/L)'])
    DAM_YSI = linearfunction(T_SSC_DAM_YSI[1]['DAM-YSI-NTU'],T_SSC_DAM_YSI[1]['TSS (mg/L)'])

    lab = ['%.2f'%LAB['a'],'%.2f'%LAB['b'],'%.2f'%LAB['r2'],'%.2f'%LAB['pearson'],'%.2f'%LAB['spearman'],'%.2f'%LAB['rmse']]
    lbj_ysi = ['%.2f'%LBJ_YSI['a'],'%.2f'%LBJ_YSI['b'],'%.2f'%LBJ_YSI['r2'],'%.2f'%LBJ_YSI['pearson'],'%.2f'%LBJ_YSI['spearman'],'%.2f'%LBJ_YSI['rmse']]
    lbj_obs = ['%.2f'%LBJ_OBS['a'],'%.2f'%LBJ_OBS['b'],'%.2f'%LBJ_OBS['r2'],'%.2f'%LBJ_OBS['pearson'],'%.2f'%LBJ_OBS['spearman'],'%.2f'%LBJ_OBS['rmse']]    

    dam_ts3k = ['%.2f'%DAM_TS3K['a'],'%.2f'%DAM_TS3K['b'],'%.2f'%DAM_TS3K['r2'],'%.2f'%DAM_TS3K['pearson'],'%.2f'%DAM_TS3K['spearman'],'%.2f'%DAM_TS3K['rmse']]
    dam_ysi = ['%.2f'%DAM_YSI['a'],'%.2f'%DAM_YSI['b'],'%.2f'%DAM_YSI['r2'],'%.2f'%DAM_YSI['pearson'],'%.2f'%DAM_YSI['spearman'],'%.2f'%DAM_YSI['rmse']]    

    nrows, ncols = 3,6
    hcell, wcell=0.3,1
    hpad, wpad = 1,1
    fig = plt.figure(figsize=(ncols*wcell+wpad,nrows*hcell+hpad)) 
    coeff = fig.add_subplot(111)
    coeff.patch.set_visible(False), coeff.axis('off')
    coeff.xaxis.set_visible(False), coeff.yaxis.set_visible(False) 
    coeff.table(cellText = [lab,lbj_ysi,lbj_obs,dam_ts3k,dam_ysi],rowLabels=['Lab','VILL-YSI','VILL-OBS','FOR-TS3K','FOR-YSI'],colLabels=[r'$\alpha$',r'$\beta$',r'$r^2$',"Pearson's","Spearman's",'RMSE'],loc='center left')
    
    plt.suptitle('Paramters for Turbidity to Suspended Sediment Concetration Rating Curves',fontsize=16)    
    
    plt.draw()
    if show==True:
        plt.show()
    return
#plotNTUratingstable(show=True,save=False)

def plotNTUratings(ms=10,show=False,log=False,save=False,lwidth=0.3):
    fig, (ysi, obs, ts3k) = plt.subplots(1,3,sharex=True,sharey=True) 
    title = 'Rating curves: Turbidity (NTU) vs SSC (mg/L)'
    xy = np.linspace(0,1000)
    mpl.rc('lines',markersize=ms,linewidth=lwidth)
    dotsize=50
    
    ## All Samples LAB
    ysi.scatter(TSS['NTU'],TSS['TSS (mg/L)'],s=dotsize,color='b',marker='v',label='LAB',edgecolors='grey')
    ysi.plot(xy,xy*T_SSC_Lab.beta[0]+T_SSC_Lab.beta[1],ls='-',c='b',label='LAB')
    ## LBJ YSI samples
    ysi.scatter(T_SSC_LBJ_YSI[1]['LBJ-YSI-NTU'],T_SSC_LBJ_YSI[1]['TSS (mg/L)'],s=dotsize,color='r',marker='o',label='VILLAGE-YSI',edgecolors='grey')
    ysi.plot(xy,xy*LBJ_YSIrating.beta[0]+LBJ_YSIrating.beta[1],ls='-',c='r',label='VILLAGE-YSI rating')
    ## Format
    ysi.grid(), ysi.set_xlim(0,1000), ysi.set_ylim(0,1000),ysi.set_ylabel('SSC (mg/L)')

    ## LBJ OBS
    obs.scatter(T_SSC_LBJ_OBS[1]['LBJ-OBS-NTU'],T_SSC_LBJ_OBS[1]['TSS (mg/L)'],s=dotsize,color='y',marker='v',label='VILLAGE-OBS',edgecolors='grey')
    obs.plot(xy,xy*LBJ_OBSrating.beta[0]+LBJ_OBSrating.beta[1],ls='-',c='y',label='VILLAGE-OBS rating')
    ## LBJ YSI
    obs.plot(xy,xy*LBJ_YSIrating.beta[0]+LBJ_YSIrating.beta[1],ls='-',c='r',label='VILLAGE-YSI rating')
    ## Format
    obs.grid(), obs.set_xlim(0,2000),obs.set_xlabel('Turbidity (NTU)')

    ## Samples: LBJ-YSI,LBJ-OBS, DAM-TS3k, DAM-YSI
    ts3k.scatter(T_SSC_LBJ_YSI[1]['LBJ-YSI-NTU'],T_SSC_LBJ_YSI[1]['TSS (mg/L)'],s=dotsize,color='r',marker='o',label='VILLAGE-YSI',edgecolors='grey')
    ts3k.scatter(T_SSC_LBJ_OBS[1]['LBJ-OBS-NTU'],T_SSC_LBJ_OBS[1]['TSS (mg/L)'],s=dotsize,color='y',marker='v',label='VILLAGE-OBS',edgecolors='grey')
    ts3k.scatter(T_SSC_DAM_TS3K[1]['DAM-TS3K-NTU'],T_SSC_DAM_TS3K[1]['TSS (mg/L)'],s=dotsize,color='g',marker='o',label='FOREST-TS3K',edgecolors='grey')
    ts3k.scatter(T_SSC_DAM_YSI[1]['DAM-YSI-NTU'],T_SSC_DAM_YSI[1]['TSS (mg/L)'],s=dotsize,color='g',marker='v',label='FOREST-YSI',edgecolors='grey')
    ## LBJ YSI, OBS    
    ts3k.plot(xy,xy*LBJ_YSIrating.beta[0]+LBJ_YSIrating.beta[1],ls='-',c='r',label='VILLAGE-YSI rating')
    ts3k.plot(xy,xy*LBJ_OBSrating.beta[0]+LBJ_OBSrating.beta[1],ls='-',c='y',label='VILLAGE-OBS rating')
    ## DAM TS3k, YSI
    ts3k.plot(xy,xy*DAM_TS3Krating.beta[0]+DAM_TS3Krating.beta[1],ls='-',c='g',label='FOREST-TS3K rating')
    ts3k.plot(xy,xy*DAM_YSIrating.beta[0]+DAM_YSIrating.beta[1],ls='--',c='g',label='FOREST-YSI rating')
    ## Format
    ts3k.grid(),ts3k.legend(fancybox=True,ncol=2),ts3k.set_xlim(0,1100)

    #labelindex_subplot(ts3k,T_SSC_LBJ_OBS[1].index,T_SSC_LBJ_OBS[1]['LBJ-OBS-NTU'],T_SSC_LBJ_OBS[1]['TSS (mg/L)'])    
    #labelindex_subplot(ts3k,T_SSC_LBJ_YSI[1].index,T_SSC_LBJ_YSI[1]['LBJ-YSI-NTU'],T_SSC_LBJ_OBS[1]['TSS (mg/L)'])

    plt.suptitle('Turbidity to Suspended Sediment Concetration Rating Curves',fontsize=16)    
    
    plt.draw()
    if show==True:
        plt.show()
    return
#plotNTUratings(show=True,log=False,save=True,lwidth=0.5,ms=20)
    
## Overall RMSE for LBJ-YSI rating and all DAM and LBJ samples
## make DataFrame of all measured NTU and SSC at LBJ and DAM
T_SSC_NTU = pd.concat([T_SSC_LBJ_YSI[1]['LBJ-YSI-NTU'],T_SSC_LBJ_OBS[1]['LBJ-OBS-NTU'],T_SSC_DAM_TS3K[1]['DAM-TS3K-NTU'],T_SSC_DAM_YSI[1]['DAM-YSI-NTU']])
T_SSC_SSC= pd.concat([T_SSC_LBJ_YSI[1]['TSS (mg/L)'],T_SSC_LBJ_OBS[1]['TSS (mg/L)'],T_SSC_DAM_TS3K[1]['TSS (mg/L)'],T_SSC_DAM_YSI[1]['TSS (mg/L)']])
T_SSC_RMSE = pd.DataFrame({'NTUmeasured':T_SSC_NTU,'SSCmeasured':T_SSC_SSC})
## Calculate RMSE
T_SSC_RMSE['SSC_LBJ_YSIpredicted']= T_SSC_RMSE['NTUmeasured']*LBJ_YSIrating.beta[0]+LBJ_YSIrating.beta[1]
T_SSC_RMSE['SSC_diff'] = T_SSC_RMSE['SSCmeasured']-T_SSC_RMSE['SSC_LBJ_YSIpredicted']
T_SSC_RMSE['SSC_diffsquared'] = (T_SSC_RMSE['SSC_diff'])**2
T_SSC_RMSE['SSC_RMSE'] = T_SSC_RMSE['SSC_diffsquared']**0.5
T_SSC_RMSE_Value = (T_SSC_RMSE['SSC_RMSE'].mean())
 
#### DAM Event-wise Sediment Flux DataFrame
DAM['TS3k-NTU']=DAM_TS3K15minute['NTU']
DAM['YSI-NTU']=DAM_YSI15minute['NTU']
## Both TS3K and YSI data resampled to 15minutes
DAM['NTU']=DAMntu15minute['NTU']

DAM['TSS-mg/L']=T_SSC_LBJ_YSI[0].beta[0] * DAM['NTU'] + T_SSC_LBJ_YSI[0].beta[1]
DAM['SedFlux-mg/sec']=DAM['Q'] * DAM['TSS-mg/L']# Q(L/sec) * C (mg/L)
DAM['SedFlux-tons/sec']=DAM['SedFlux-mg/sec']*(10**-6) ## mg x 10**-6 = tons
DAM['SedFlux-tons/15min']=DAM['SedFlux-tons/sec']*900 ## 15min x 60sec/min = 900sec -> tons/sec * 900sec/15min = tons/15min
SedFluxStorms_DAM = StormSums(DAM_StormIntervals,DAM['SedFlux-tons/15min'])
SedFluxStorms_DAM.columns = ['Sstart','Send','Scount','Ssum','Smax']
SedFluxStorms_DAM=Pstorms_DAM.join(SedFluxStorms_DAM)#Add Event S (which will be fewer events than Event Precip)
SedFluxStorms_DAM=SedFluxStorms_DAM.join(Qstorms_DAM)

#### LBJ Event-wise Sediment Flux DataFrame
LBJ['YSI-NTU']=LBJ_YSI15minute['NTU']
LBJ['YSI-TSS']=T_SSC_LBJ_YSI[0].beta[0] * LBJ_YSI15minute['NTU'] + T_SSC_LBJ_YSI[0].beta[1]
LBJ['OBS-NTU']=LBJ_OBS15minute['NTU']
LBJ['OBS-TSS']=T_SSC_LBJ_YSI[0].beta[0] * LBJ_OBS15minute['NTU'] + T_SSC_LBJ_YSI[0].beta[1]
## Both YSI and OBS data resampled to 15minutes
LBJ['NTU'] = LBJntu15minute

LBJ['TSS-mg/L'] = T_SSC_LBJ_YSI[0].beta[0] * LBJ['NTU'] + T_SSC_LBJ_YSI[0].beta[1]
LBJ['SedFlux-mg/sec']=LBJ['Q'] * LBJ['TSS-mg/L']# Q(L/sec) * C (mg/L) = mg/sec
LBJ['SedFlux-tons/sec']=LBJ['SedFlux-mg/sec']*(10**-6) ## mg x 10**-6 = tons
LBJ['SedFlux-tons/15min']=LBJ['SedFlux-tons/sec']*900 ## 15min x 60sec/min = 900sec -> tons/sec * 900sec/15min = tons/15min
SedFluxStorms_LBJ = StormSums(LBJ_StormIntervals,LBJ['SedFlux-tons/15min'])
SedFluxStorms_LBJ.columns = ['Sstart','Send','Scount','Ssum','Smax']
SedFluxStorms_LBJ=Pstorms_LBJ.join(SedFluxStorms_LBJ) ## Add Event S (which will be fewer events than Event Precip)
SedFluxStorms_LBJ=SedFluxStorms_LBJ.join(Qstorms_LBJ) ## Add Event Discharge


#### Storm Data
def stormdata(StormIntervals):
    storm_data = pd.DataFrame(columns=['Precip','LBJq','DAMq','LBJtss','DAMtss','LBJ-Sed','DAM-Sed','LBJgrab','DTgrab','DAMgrab'],dtype=np.float64,index=pd.date_range(PT1.index[0],PT1.index[-1],freq='15Min'))
    for storm in StormIntervals.iterrows():
        start = storm[1]['start']-dt.timedelta(minutes=60)
        end =  storm[1]['end']
        data = pd.DataFrame.from_dict({'Precip':PrecipFilled['Precip'][start:end].dropna(),'LBJq':LBJ['Q'][start:end],'DAMq':DAM['Q'][start:end],'LBJtss':LBJ['TSS-mg/L'][start:end],'DAMtss':DAM['TSS-mg/L'][start:end],'LBJ-Sed':LBJ['SedFlux-tons/15min'][start:end],'DAM-Sed':DAM['SedFlux-tons/15min'][start:end],'LBJgrab':LBJgrab[start:end],'DTgrab':DTgrab[start:end],'DAMgrab':DAMgrab[start:end]},orient='columns') ## slice desired data by storm 
        data['sEMC-DAM']=data['DAMgrab'].mean()
        data['sEMC-LBJ']=data['LBJgrab'].mean()
        storm_data = storm_data.combine_first(data) ## add each storm to each other
        return storm_data
storm_data_LBJ = stormdata(LBJ_StormIntervals)
storm_data_DAM = stormdata(DAM_StormIntervals)

def SedFlux(show=False):
    title = 'Figure7:Storm Data'
    fig, (QP,TSS) = plt.subplots(nrows=2,ncols=1,sharex=True)
    
    storm_data_LBJ['LBJq'].plot(ax=QP,color='r',label='LBJ-Q')
    storm_data_DAM['DAMq'].plot(ax=QP,color='g',label='DAM-Q')
    P = QP.twinx()
    storm_data_LBJ['Precip'].plot(ax=P,color='b',ls='steps-pre',label='Timu1')
    QP.set_ylabel('Q m^3/15min.')
    P.set_ylabel('Precip mm/15min.')
    
    QP.legend(loc=0)
    P.legend(loc=1)
    
    storm_data_LBJ['LBJtss'].plot(ax=TSS,color='r',label='LBJ-TSS')
    storm_data_DAM['DAMtss'].plot(ax=TSS,color='g',label='DAM-TSS')
    
    storm_data_LBJ['LBJgrab'].plot(ax=TSS,color='r',marker='o',ls='None',label='LBJ-grab')
    storm_data_LBJ['DTgrab'].plot(ax=TSS,color='y',marker='o',ls='None',label='DT-grab')
    storm_data_DAM['DAMgrab'].plot(ax=TSS,color='g',marker='o',ls='None',label='DAM-grab')
    
    SED=TSS.twinx()
    storm_data_LBJ['LBJ-Sed'].plot(ax=SED,color='r',label='LBJ-SedFlux',ls='-.')
    storm_data_LBJ['DAM-Sed'].plot(ax=SED,color='g',label='DAM-SedFlux',ls='-.')
    
    TSS.set_ylabel('TSS mg/L')
    TSS.set_ylim(0,1400)
    SED.set_ylabel('Sediment Flux (Mg/15minutes)')
    SED.set_ylim(0,10)
                 
    TSS.legend(loc=0)
    SED.legend(loc=1)
    
    #Shade Storms
    showstormintervals(TSS)
    
    plt.draw()
    if show==True:
        plt.show()
    return
SedFlux(True)
    
def Q_EMC(show=False):
    fig, qemc = plt.subplots(1,1)
    
    qemc.plot(storm_data['sEMC-LBJ'].drop_duplicates(),c='r',marker='o',ls='None')
    qemc.plot(storm_data['sEMC-DAM'].drop_duplicates(),c='g',marker='o',ls='None')
    plt.grid()
    
    plt.draw()
    if show==True:
        plt.show()
    return
#Q_EMC(True)
    
    
#### Calculate correlation coefficients and sediment rating curves    
def compileALLStorms():
    ALLStorms=pd.DataFrame({'Supper':SedFluxStorms_DAM['Ssum'],'Slower':SedFluxStorms_LBJ['Ssum']-SedFluxStorms_DAM['Ssum'],'Stotal':SedFluxStorms_LBJ['Ssum']})
    
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
    ALLStorms['EI'] = LBJ_Stormdf['EI'][LBJ_Stormdf['EI']>1] ## Add Event Erosion Index
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
    ## add summary stats to bottom of table
    diff=diff.append(pd.DataFrame({'Storm#':'-','Psum':'-','Supper':'-','Slower':'-','Stotal':'Average:','% Upper':'%.1f'%diff['% Upper'].mean(),'% Lower':'%.1f'%diff['% Lower'].mean()},index=[pd.NaT]))
   
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
plotS_storm_table(show=True)

## Calculate the percent of total Q with raw vales, BEFORE NORMALIZING by area!
def plotQ_storm_table(show=False):
    diff = ALLStorms.dropna()
    ## Calculate percent contributions from upper and lower watersheds
    diff['Qupper']=diff['Qsumupper']
    diff['Qlower']=diff['Qsumlower']
    diff['Qtotal']=diff['Qsumtotal']
    diff['% Upper'] = diff['Qupper']/diff['Qtotal']*100
    diff['% Upper'] = diff['% Upper'].round(0)
    diff['% Lower'] = diff['Qlower']/diff['Qtotal']*100
    diff['% Lower'] = diff['% Lower'].round(0)
    diff['Psum'] = diff['Pstorms']
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
    
 
def NormalizeSSYbyCatchmentArea(ALLStorms):
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
    ALLStorms['EI'] = LBJ_Stormdf['EI'][LBJ_Stormdf['EI']>1] ## Add Event Erosion Index
    return ALLStorms


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
def plotQmaxS(show=False,log=False,save=True,norm=True): 
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
    qs.scatter(ALLStorms['Qmaxupper']/1000,ALLStorms['Supper'],edgecolors='grey',color='g',s=upperdotsize,label='Upper (FOREST)')
    QmaxS_upper_power = powerfunction(ALLStorms['Qmaxupper']/1000,ALLStorms['Supper'])
    PowerFit_CI(ALLStorms['Qmaxupper']/1000,ALLStorms['Supper'],xy,qs,linestyle='-',color='g',label='Qmax_UPPER')
    QmaxS_upper_linear = linearfunction(ALLStorms['Qmaxupper']/1000,ALLStorms['Supper'])
    #LinearFit(ALLStorms['Qmaxupper']/1000,ALLStorms['Supper'],xy,qs,linestyle='--',color='g',label='QmaxS_upper_linear')  
    labelindex(ALLStorms.index,ALLStorms['Qmaxupper']/1000,ALLStorms['Supper'])
    ## Total Watershed (=LBJ)
    qs.scatter(ALLStorms['Qmaxtotal']/1000,ALLStorms['Stotal'],edgecolors='grey',color='r',s=lowerdotsize,label='Total(VILLAGE)')
    QmaxS_total_power = powerfunction(ALLStorms['Qmaxtotal']/1000,ALLStorms['Stotal'])
    PowerFit_CI(ALLStorms['Qmaxtotal']/1000,ALLStorms['Stotal'],xy,qs,linestyle='-',color='r',label='Qmax_TOTAL') 
    QmaxS_total_linear = linearfunction(ALLStorms['Qmaxtotal']/1000,ALLStorms['Stotal'])
    #LinearFit(ALLStorms['Qmaxtotal']/1000,ALLStorms['Stotal'],xy,qs,linestyle='--',color='r',label='QmaxS_total_linear') 
    labelindex(ALLStorms.index,ALLStorms['Qmaxtotal']/1000,ALLStorms['Stotal'])    
    
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
        PowerFit(xy,Duvert1,xy,qs,linestyle='-',color='grey',label='Duvert(2012)Linear')
        PowerFit(xy,Duvert2,xy,qs,linestyle='--',color='grey',label='Duvert(2012)Nonlinear')
        PowerFit(xy,DuvertLAFR,xy,qs,linestyle='-',color='k',label=r'Duvert(2012)$LA_{FR}$')
        PowerFit(xy,DuvertARES,xy,qs,linestyle='--',color='k',label=r'Duvert(2012)$AR_{ES}$')
        PowerFit(xy,DuvertCIES,xy,qs,linestyle='-.',color='k',label=r'Duvert(2012)$CI_{ES}$')
        qs.legend(loc='best',ncol=3,fancybox=True)  
    qs.legend(loc='best',ncol=2,fancybox=True)  
    title="Event Peak Discharge vs Event Sediment Yield from Fagaalu Stream"
    qs.set_title(title)
    qs.set_ylabel(ylabel)
    qs.set_xlabel(xlabel)#+r'$; DotSize= Qsum (m^3)$')

    fig.canvas.manager.set_window_title('Figure : '+'Qmax vs. S')
    
    logaxes(log,fig)
    qs.autoscale_view(True,True,True)
    show_plot(show,fig)
    savefig(save,title)
    return
#plotQmaxS(show=True,log=True,save=False,norm=True)  
#plotQmaxS(show=True,log=False,save=True)
#plotQmaxS(show=True,log=True,save=True,norm=False)
#plotQmaxS(show=True,log=True,save=True,norm=True)


plt.show()
elapsed = dt.datetime.now() - start_time 
print 'run time: '+str(elapsed)
