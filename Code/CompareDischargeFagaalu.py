# -*- coding: utf-8 -*-
"""
Created on Tue Sep 02 16:07:43 2014

@author: Alex
"""

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
    
    
    

#### STAGE TO DISCHARGE ####

order=1
powerlaw = False
from stage2discharge_ratingcurve import AV_RatingCurve, calcQ, Mannings_rect, Weir_rect, Weir_vnotch, Flume
## Q = a(stage)**b
def power(x,a,b):
    y = a*(x**b)
    return y

### Area Velocity and Mannings from in situ measurments
## stage2discharge_ratingcurve.AV_rating_curve(datadir,location,Fagaalu_stage_data,trapezoid=False,Slope=0.01,Mannings_n=0.03,width=4.9276)
## Returns DataFrame of Stage (cm) and Discharge (L/sec) calc. from AV measurements with time index

#### LBJ (3 rating curves: AV measurements, A measurment * Mannings V, Area of Rectangular section * Mannings V)
Slope = 0.0161 # m/m
n=0.050 # Mountain stream rocky bed and rivers with variable sections and veg along banks (Dunne 1978)

LBJstageDischarge = AV_RatingCurve(datadir+'Q/','LBJ',Fagaalu_stage_data,slope=Slope,Mannings_n=n,trapezoid=True,printResults=False).dropna() #DataFrame with Q from AV measurements, Q from measured A with Manning-predicted V, stage, and Q from Manning's and assumed rectangular channel A
LBJstageDischarge = LBJstageDischarge.truncate(before=datetime.datetime(2012,3,20)) # throw out measurements when I didn't know how to use the flow meter very well
LBJstageDischargeLog = LBJstageDischarge.apply(np.log10) #log-transformed version

### Calculate Q from a single AV measurement
#fileQ = calcQ(datadir+'Q/LBJ_4-18-13.txt','LBJ',Fagaalu_stage_data,slope=Slope,Mannings_n=n,trapezoid=True)
### and save to CSV
#pd.concat(fileQ).to_csv(datadir+'Q/LBJ_4-18-13.csv')

## LBJ: Q Models 
LBJ_AV= pd.ols(y=LBJstageDischarge['Q-AV(L/sec)'],x=LBJstageDischarge['stage(cm)'],intercept=True) 
LBJ_AVLog= pd.ols(y=LBJstageDischargeLog['Q-AV(L/sec)'],x=LBJstageDischargeLog['stage(cm)'],intercept=True) #linear fit to log-transformed stage and Q
LBJ_AManningV = pd.ols(y=LBJstageDischarge['Q-AManningV(L/sec)'],x=LBJstageDischarge['stage(cm)'],intercept=True)
LBJ_AManningVLog = pd.ols(y=LBJstageDischargeLog['Q-AManningV(L/sec)'],x=LBJstageDischargeLog['stage(cm)'],intercept=True)
#LBJ_Mannings = pd.ols(y=LBJstageDischarge['Q-Mannings(L/sec)'],x=LBJstageDischarge['stage(cm)'],intercept=True) ## Rectangular channel
#LBJ_ManningsLog = pd.ols(y=LBJstageDischargeLog['Q-Mannings(L/sec)'],x=LBJstageDischargeLog['stage(cm)'],intercept=True) ## Rectangular channel

#### LBJ: Q from OrangePeel method 
from notebook import OrangePeel
orangepeel = OrangePeel('OrangePeel',1,datadir+'Q/Fagaalu-StageDischarge.xlsx')
orangepeel=orangepeel.append(pd.DataFrame({'stage cm':0,'L/sec':0},index=[pd.NaT]))

#### LBJ: Q directly from MANNING'S EQUATION:  Q = CrossSectionalArea * 1.0/n * R^(2/3) * S^(1/2)
#width = 4.9276 ## meters   
#LBJ['Q-ManningsRect']=(LBJ['stage']/100*width) * (((LBJ['stage']/100*width)/((2*LBJ['stage']/100)+width)**(2.0/3.0)) * (Slope**0.5))/Mannings_n
#LBJ['Q-ManningsRect']=LBJ['Q-ManningsRect']*1000 ##m3/s to L/s
###using rating curve from Mannings Rect
#LBJ['Q-ManningsRect']=LBJ_AVratingcurve_ManningsRect(LBJ['stage']) ## Calculate Q from A-Mannings rating
from ManningsRatingCurve import Mannings, Mannings_Series
LBJ_Man = Mannings_Series(datadir+'Q/LBJ_cross_section.xlsx','LBJ_m',Slope=0.016,Manning_n='Jarrett',stage_series=Fagaalu_stage_data['LBJ'])
Mannings_n_list = np.arange(.06,.24,.02)
Mannings_n_list = np.array(['Jarrett'])
slope_list = np.array([.016])
xy = np.arange(.01,1.5,.1)
#fig, ax = plt.subplots(1)
for s in slope_list:
    for n in Mannings_n_list:
        Mannings_calc = Mannings(datadir+'Q/LBJ_cross_section.xlsx','LBJ_m',Slope=s,Manning_n=n,stage_start=.1,stage_end=1.5,display=False)
        ax.plot(Mannings_calc['stage'],Mannings_calc['Q'],'-',color='r',label=str(n))
        #PowerFit(Mannings_calc['stage'],Mannings_calc['Q'],xy,ax,c='r',label='Mannings')
        #ax.plot(Mannings_calc['stage'],Mannings_calc['vel'],'-',color=np.random.rand(3,1),label=str(n))
ax.plot(LBJstageDischarge['stage(cm)']/100,LBJstageDischarge['Q-AV(L/sec)']/1000,'o',color='r',label='AV')        
        

#ax.plot(orangepeel['PT reading(cm)']/100,orangepeel['m/s'],'o',color='DarkOrange',label='Float')    
#ax.plot(LBJstageDischarge['stage(cm)']/100,LBJstageDischarge['V(m/s)'],'o',color='r',label='AV')
ax.plot(DAM_HECstageDischarge['stage(cm)']/100,DAM_HECstageDischarge['Q_HEC(L/sec)']/1000,'-',color='b',label='DAM HEC-RAS Model')

LBJ_AVnonLinear = nonlinearfunction(LBJstageDischarge['stage(cm)']/100,LBJstageDischarge['Q-AV(L/sec)']/1000,order=2,interceptZero=True)    
LBJ_AVpower = powerfunction(LBJstageDischarge['stage(cm)']/100,LBJstageDischarge['Q-AV(L/sec)']/1000)  

NonlinearFit(LBJstageDischarge['stage(cm)']/100,LBJstageDischarge['Q-AV(L/sec)']/1000,order=2,interceptZero=False,xspace=xy,Ax=ax,c='r',ls='-.',label='LBJ_AVnonLinear '+r'$r^2$')#+"%.2f"%LBJ_AVnonLinear['r2'])
PowerFit(LBJstageDischarge['stage(cm)']/100,LBJstageDischarge['Q-AV(L/sec)']/1000,xy,ax,c='y',ls='-.',label='LBJ_AVpower '+r'$r^2$'+"%.2f"%LBJ_AVpower['r2'])
plt.legend(loc='best')




plt.plot(LBJ_Man['stage'],LBJ_Man['Q'],'o',color='b')



def DAM_Mannings():

DAM_Man = Mannings_Series(datadir+'Q/LBJ_cross_section.xlsx','DAM_m',Slope=0.044,Manning_n=0.08,stage_series=Fagaalu_stage_data['Dam'])
Mannings_n_list = np.arange(.03,.09,.01)
slope_list = np.arange(.03,.044,.01)

Mannings_n_list = np.array([.08])
slope_list = np.array([.03])

xy = np.arange(.01,1.5,.1)
#fig, ax = plt.subplots(1)
for s in slope_list:
    for n in Mannings_n_list:
        Mannings_calc = Mannings(datadir+'Q/LBJ_cross_section.xlsx','DAM_m',Slope=s,Manning_n=n,stage_start=.0,stage_end=1.3,display=False)
        ax.plot(Mannings_calc['stage'],Mannings_calc['Q'],'-',color='g',label='Man_n'+str(n)+' S='+str(s))
        #PowerFit(Mannings_calc['stage'],Mannings_calc['Q'],xy,ax,c='g',label='Mannings')
        #ax.plot(Mannings_calc['stage'],Mannings_calc['vel'],'-',color=np.random.rand(3,1),label=str(n))
ax.plot(DAMstageDischarge['stage(cm)']/100,DAMstageDischarge['Q-AV(L/sec)']/1000,'o',color='g',label='AV')  
plt.legend(loc='best')      
        

#ax.plot(orangepeel['PT reading(cm)']/100,orangepeel['m/s'],'o',color='DarkOrange',label='Float')    
#ax.plot(LBJstageDischarge['stage(cm)']/100,LBJstageDischarge['V(m/s)'],'o',color='r',label='AV')
ax.plot(DAM_HECstageDischarge['stage(cm)']/100,DAM_HECstageDischarge['Q_HEC(L/sec)']/1000,'-',color='b',label='DAM HEC-RAS Model')

LBJ_AVnonLinear = nonlinearfunction(LBJstageDischarge['stage(cm)']/100,LBJstageDischarge['Q-AV(L/sec)']/1000,order=2,interceptZero=True)    
LBJ_AVpower = powerfunction(LBJstageDischarge['stage(cm)']/100,LBJstageDischarge['Q-AV(L/sec)']/1000)  

NonlinearFit(LBJstageDischarge['stage(cm)']/100,LBJstageDischarge['Q-AV(L/sec)']/1000,order=2,interceptZero=False,xspace=xy,Ax=ax,c='r',ls='-.',label='LBJ_AVnonLinear '+r'$r^2$')#+"%.2f"%LBJ_AVnonLinear['r2'])
PowerFit(LBJstageDischarge['stage(cm)']/100,LBJstageDischarge['Q-AV(L/sec)']/1000,xy,ax,c='y',ls='-.',label='LBJ_AVpower '+r'$r^2$'+"%.2f"%LBJ_AVpower['r2'])
plt.legend(loc='best')

#### DAM(3 rating curves: AV measurements, WinFlume, HEC-RAS
DAMstageDischarge = AV_RatingCurve(datadir+'Q/','Dam',Fagaalu_stage_data,printResults=False) ### Returns DataFrame of Stage and Discharge calc. from AV measurements with time index
#### DAM: Q from WinFlume equation
def D_Flume(stage):
    K1 = 252.5
    K2 = 0.02236
    u = 1.639
    Q = K1*(stage/25.4 + K2)**u ##ft to cm
    return Q
DAMstageDischarge['D_Flume(L/sec)'] = DAMstageDischarge['stage(cm)'].apply(lambda x: D_Flume(x)) ## runs the Flume equation on x (stage)
DAMstageDischargeLog=DAMstageDischarge.apply(np.log10) #log-transformed version

## HEC-RAS Model of the DAM structure: Documents/HEC/FagaaluDam.prj
DAM_HECstageDischarge = pd.DataFrame(np.array([[0,0],[19.0,15.0],[23.0,60],[31.0,203.0],[34.0,261],[61.0,10000.0],[99.0,3000.0]]),columns=['stage(cm)','Q(L/sec)']) ##rating curve from HEC-RAS FagaaluDAM.prj

## DAM: Q Models
DAM_AV = pd.ols(y=DAMstageDischarge['Q-AV(L/sec)'],x=DAMstageDischarge['stage(cm)'],intercept=True) 
DAM_AVLog = pd.ols(y=DAMstageDischargeLog['Q-AV(L/sec)'],x=DAMstageDischargeLog['stage(cm)'],intercept=True) 
DAM_D_Flume = pd.ols(y=DAMstageDischarge['D_Flume(L/sec)'],x=DAMstageDischarge['stage(cm)'],intercept=True) 
DAM_HEC = pd.ols(y=DAM_HECstageDischarge['Q(L/sec)'],x=DAM_HECstageDischarge['stage(cm)'],intercept=True) 

#h = float(stage)/30.48
#Qflume=479.5 * m.pow((h - 0.006),1.508)
#def D_Flume(stage,angle=150,notchHeight=47):
#    if float(stage)<=notchHeight:
#        Q = 479.5*((stage/30.48)-.006)**1.508 ### Flume equation up to flume height (=47cm)
#    elif float(stage)>notchHeight:
#        theta = angle
#        H = float(stage) - notchHeight #cm
#        H = H/30.48 #cm to feet
#        Cd = 0.6072-(0.000874*theta)+(0.0000061*(theta**2)) ## from LMNO engineering and Chin, 2006
#        k = 0.0144902648-(0.00033955535*theta)+(0.00000329819003*(theta**2))-(0.0000000106215442*(theta**3))
#        a = math.tan(math.radians(theta)/2.0)
#        b = (H + k)**2.5
#        VnotchQ = 4.28*Cd*a*b
#        VnotchQ = VnotchQ * 0.028316846593389  ## cfs to m^3/s from unitconverterpro.com
#        Q = VnotchQ * 1000 ##Q (L/sec)
#        Q = VnotchQ + 479.5*((notchHeight/30.48)-.006)**1.508 ## Accounts for the flume part
#    else:
#        pass
#    return Q

def V_vs_ManningV(show=False,log=False):
    fig, ((stage_Area, stage_WP), (V_Mv, Q_Mq)) = plt.subplots(2,2)
    plt.suptitle('LBJ-Hospital (VILLAGE)')
    stage_Area.scatter(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Area(m2)'])
    stage_Area.set_title('Stage vs. Cross sectional Area'), stage_Area.set_xlabel('stage cm'), stage_Area.set_ylabel('Area m2')
    
    stage_WP.scatter(LBJstageDischarge['stage(cm)'],LBJstageDischarge['WP'])
    stage_WP.set_title('Stage vs. Wetted Perimeter'), stage_WP.set_xlabel('stage cm'), stage_WP.set_ylabel('Wetted Perimeter m')
    
    V_Mv.scatter(LBJstageDischarge['V(m/s)'],LBJstageDischarge['ManningV(m/s)'])
    V_Mv.plot([0,1.5],[0,1.5])
    V_Mv.set_title('Measured Velocity m/s vs Mannings Velocity m/s'), V_Mv.set_xlabel('Measured Velocity m/s'), V_Mv.set_ylabel('Mannings Velocity m/s')
    
    Q_Mq.scatter(LBJstageDischarge['Q-AV(L/sec)'],LBJstageDischarge['Q-AManningV(L/sec)'])
    Q_Mq.plot([0,2000],[0,2000])
    Q_Mq.set_title('Q from AV measuremnt vs Q from measured A and Mannings V'), Q_Mq.set_xlabel('Q-AV L/sec'), Q_Mq.set_ylabel('Q-AManningV L/sec')
    return
#V_vs_ManningV(show=True,log=False)    

def A_vs_V(show=False,log=False):
    fig, ((stage_Area, stage_V), (A_V, V_Q)) = plt.subplots(2,2)
    plt.suptitle('LBJ-Hospital (VILLAGE)')
    
    stage_Area.scatter(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Area(m2)'])
    stage_Area.set_title('Stage vs. Cross sectional Area'), stage_Area.set_xlabel('stage cm'), stage_Area.set_ylabel('Area m2')
    
    stage_V.scatter(LBJstageDischarge['stage(cm)'],LBJstageDischarge['V(m/s)'])
    stage_V.set_title('Stage vs. Mean Velocity '), stage_V.set_xlabel('stage cm'), stage_V.set_ylabel('Velocity m/s')
    
    A_V.scatter(LBJstageDischarge['V(m/s)'],LBJstageDischarge['Area(m2)'])
    A_V.set_title('Measured Velocity m/s vs Crossectional Area'), A_V.set_xlabel('Mean Velocity m/s'), A_V.set_ylabel('Cross sectional Area')
    
    V_Q.scatter(LBJstageDischarge['V(m/s)'],LBJstageDischarge['Q-AV(L/sec)'])
    V_Q.set_title('V from AV measuremnt vs Q from measured AV'), V_Q.set_xlabel('V m/s'), V_Q.set_ylabel('Q-AV L/sec')
    return
#A_vs_V(show=True,log=False)    

def plotLBJstageDischargeRatings(show=False,log=False,save=False): ## Rating Curves
    fig, (ax, logax) = plt.subplots(1,2)
    xy = np.linspace(0,150,150)
    #### Linear
    #LBJ AV Measurements and Rating Curve
    LBJ_AVlinear= linearfunction(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AV(L/sec)'])
    LBJ_AVnonLinear = nonlinearfunction(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AV(L/sec)'],order=2,interceptZero=True)    
    LBJ_AVpower = powerfunction(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AV(L/sec)'])  
    
    LinearFit(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AV(L/sec)'],xy,ax,c='g',ls='-',label='LBJ_AVlinear '+r'$r^2$'+"%.2f"%LBJ_AVlinear['r2'])
    NonlinearFit(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AV(L/sec)'],order=3,interceptZero=False,xspace=xy,Ax=ax,c='r',ls='-',label='LBJ_AVnonLinear '+r'$r^2$')#+"%.2f"%LBJ_AVnonLinear['r2'])
    PowerFit(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AV(L/sec)'],xy,ax,c='y',ls='-',label='LBJ_AVpower '+r'$r^2$'+"%.2f"%LBJ_AVpower['r2'])    
    
    ax.plot(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AV(L/sec)'],'.',color='r',markeredgecolor='k',label='LBJ_AV')   
    
    #LBJ A*ManningV Measurements and Rating Curves
    LBJ_MANlinear=linearfunction(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AManningV(L/sec)'])
    LBJ_MANnonLinear = nonlinearfunction(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AManningV(L/sec)'])
    LBJ_MANpower =powerfunction(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AManningV(L/sec)'])
    
    LinearFit(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AManningV(L/sec)'],xy,ax,c='g',ls='--',label='LBJ_MANlinear') ## rating from LBJ_AManningV
    NonlinearFit(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AManningV(L/sec)'],order=3,interceptZero=False,xspace=xy,Ax=ax,c='r',ls='--',label='LBJ_MANnonLinear') ## rating from LBJ_AManningV
    PowerFit(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AManningV(L/sec)'],xy,ax,c='y',ls='-',label='LBJ_MANpower') ## rating from LBJ_AManningVLog
    ax.plot(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AManningV(L/sec)'],'.',color='grey',markeredgecolor='k',label='LBJ A*ManningsV')    
    
    ##LBJ Orange Peel Measurements and Rating Curve
    LinearFit(orangepeel['PT reading(cm)'],orangepeel['AVG L/sec'],xy,ax,c='DarkOrange',ls='--',label='LBJ_OPlinear') ## a b values from excel file  FagaaluStage-Discharge
    PowerFit(orangepeel['PT reading(cm)'],orangepeel['AVG L/sec'],xy,ax,c='DarkOrange',ls='-',label='LBJ_OPpower')    
    ax.plot(orangepeel['PT reading(cm)'],orangepeel['AVG L/sec'],'.',color='DarkOrange',label='LBJ_OP')  

    #### Logarithmic
    #LBJ AV Measurements and Rating Curve

    LinearFit(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AV(L/sec)'],xy,logax,c='g',ls='-',label='LBJ_AVlinear '+r'$r^2$'+"%.2f"%LBJ_AVlinear['r2'])
    NonlinearFit(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AV(L/sec)'],order=2,interceptZero=True,xspace=xy,Ax=logax,c='r',ls='-',label='LBJ_AVnonLinear '+r'$r^2$')
    PowerFit(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AV(L/sec)'],xy,logax,c='y',ls='-',label='LBJ_AVpower '+r'$r^2$'+"%.2f"%LBJ_AVpower['r2'])    
    logax.plot(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AV(L/sec)'],'.',color='r',markeredgecolor='k',label='LBJ_AV')   
    
    #LBJ A*ManningV Measurements and Rating Curves

    LinearFit(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AManningV(L/sec)'],xy,logax,c='g',ls='--',label='LBJ_MANlinear') ## rating from LBJ_AManningV
    NonlinearFit(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AManningV(L/sec)'],order=2,interceptZero=True,xspace=xy,Ax=logax,c='r',ls='--',label='LBJ_MANnonLinear')  ## rating from LBJ_AManningV
    PowerFit(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AManningV(L/sec)'],xy,logax,c='y',ls='--',label='LBJ_MANpower') ## rating from LBJ_AManningVLog
    logax.plot(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AManningV(L/sec)'],'.',color='grey',markeredgecolor='k',label='LBJ A*ManningsV')    
    
    ##LBJ Orange Peel Measurements and Rating Curve
    LinearFit(orangepeel['PT reading(cm)'],orangepeel['AVG L/sec'],xy,logax,c='DarkOrange',ls='--',label='LBJ_OPlinear') ## a b values from excel file  FagaaluStage-Discharge
    PowerFit(orangepeel['PT reading(cm)'],orangepeel['AVG L/sec'],xy,logax,c='DarkOrange',ls='-',label='LBJ_OPpower')    
    logax.plot(orangepeel['PT reading(cm)'],orangepeel['AVG L/sec'],'.',color='DarkOrange',label='LBJ_OP')  
    
    ## Label subplots    
    ax.set_title('VILLLAGE'),ax.set_xlabel('Stage(cm)'),ax.set_ylabel('Q(L/sec)')
    logax.set_title('VILLLAGE'),logax.set_xlabel('Stage(cm)'),logax.set_ylabel('Q(L/sec)')
    
    ## Format subplots
    ax.set_xlim(10,PT1['stage'].max()+10),ax.set_ylim(10,4000)
    logax.set_xlim(10,PT3['stage'].max()+10),logax.set_ylim(10,4000)
    ## Legends
    #site_lbj.legend(loc='best',ncol=2,fancybox=True),site_dam.legend(loc='best',ncol=2,fancybox=True),both.legend(loc='best',ncol=2,fancybox=True)
    plt.legend(loc='best')    
    ## Figure title
    #plt.suptitle(title,fontsize=16)

    logax.set_yscale('log'),logax.set_xscale('log')
    for ax in fig.axes:
        ax.autoscale_view(True,True,True)
    show_plot(show,fig)
    
    return
plotLBJstageDischargeRatings(show=True)

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
    LBJ_AVlinear= linearfunction(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AV(L/sec)'])    
    LBJ_AVpower = powerfunction(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AV(L/sec)'])    
    LinearFit(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AV(L/sec)'],xy,site_lbj,c='r',ls='--',label='LBJ_AVlinear '+r'$r^2$'+"%.2f"%LBJ_AVlinear['r2'])
    PowerFit(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AV(L/sec)'],xy,site_lbj,c='r',ls='-',label='LBJ_AVpower '+r'$r^2$'+"%.2f"%LBJ_AVpower['r2'])    
    site_lbj.plot(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AV(L/sec)'],'.',color='r',markeredgecolor='k',label='LBJ_AV')    
    #LBJ A*ManningV Measurements and Rating Curves
    LBJ_MANlinear=linearfunction(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AManningV(L/sec)'])
    LBJ_MANpower =powerfunction(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AManningV(L/sec)'])
    LinearFit(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AManningV(L/sec)'],xy,site_lbj,c='grey',ls='--',label='LBJ_MANlinear') ## rating from LBJ_AManningV
    PowerFit(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AManningV(L/sec)'],xy,site_lbj,c='grey',ls='-',label='LBJ_MANpower') ## rating from LBJ_AManningVLog
    site_lbj.plot(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AManningV(L/sec)'],'.',color='grey',markeredgecolor='k',label='LBJ A*ManningsV')    
    ##LBJ Orange Peel Measurements and Rating Curve
    #LinearFit(orangepeel['PT reading(cm)'],orangepeel['AVG L/sec'],xy,site_lbj,c='DarkOrange',ls='--',label='LBJ_OPlinear') ## a b values from excel file  FagaaluStage-Discharge
    #PowerFit(orangepeel['PT reading(cm)'],orangepeel['AVG L/sec'],xy,site_lbj,c='DarkOrange',ls='-',label='LBJ_OPpower')    
    #site_lbj.plot(orangepeel['PT reading(cm)'],orangepeel['AVG L/sec'],'.',color='DarkOrange',label='LBJ_OP')    
    #DAM AV Measurements and Rating Curve
    DAM_AVlinear=linearfunction(DAMstageDischarge['stage(cm)'],DAMstageDischarge['Q-AV(L/sec)'])    
    DAM_AVpower=powerfunction(DAMstageDischarge['stage(cm)'],DAMstageDischarge['Q-AV(L/sec)'])
    LinearFit(DAMstageDischarge['stage(cm)'],DAMstageDischarge['Q-AV(L/sec)'],xy,site_dam,c='g',ls='--',label='DAM_AVlinear '+r'$r^2$'+"%.2f"%DAM_AVlinear['r2']) ## rating from DAM_AVLog
    PowerFit(DAMstageDischarge['stage(cm)'],DAMstageDischarge['Q-AV(L/sec)'],xy,site_dam,c='g',ls='-', label='DAM AV '+r'$r^2$'+"%.2f"%DAM_AVpower['r2']) ## rating from DAM_AV
    site_dam.plot(DAMstageDischarge['stage(cm)'],DAMstageDischarge['Q-AV(L/sec)'],'.',color='g',markeredgecolor='k',label='DAM_AV')
    #DAM Flume Model and Rating Curve
    site_dam.plot(xy,[D_Flume(d) for d in xy],c='k',ls='-',label='DAM_Flume') ## rating from DAM_Flume
    site_dam.plot(DAMstageDischarge['stage(cm)'],DAMstageDischarge['D_Flume(L/sec)'],'.',color='grey',markeredgecolor='k',label='DAM Flume Model')
    #DAM HEC-RAS Model and Rating Curve
    PowerFit(DAM_HECstageDischarge['stage(cm)'],DAM_HECstageDischarge['Q(L/sec)'],xy,site_dam,c='b',ls='-',label='DAM_HECpower') ## rating from DAM_HEC
    site_dam.plot(DAM_HECstageDischarge['stage(cm)'],DAM_HECstageDischarge['Q(L/sec)'],'.',color='b',label='DAM HEC-RAS Model')
    
    ## Plot selected rating curves for LBJ and DAM
    xy = np.linspace(0,PT1['stage'].max())
    LBJ_AVpower=powerfunction(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AV(L/sec)'])
    PowerFit(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AV(L/sec)'],xy,both,c='r',ls='-',label='VILLAGE AV Power '+r'$r^2$'+"%.2f"%LBJ_AVpower['r2']) ## rating from LBJ_AVLog
    xy = np.linspace(0,PT3['stage'].max())  
    both.plot(xy,[D_Flume(d) for d in xy],c='grey',ls='-',label='FOREST WinFlume') ## rating from DAM_Flume
    both.plot(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AV(L/sec)'],'.',color='r',markeredgecolor='k',label='VILLAGE A-V')  
    both.plot(DAMstageDischarge['stage(cm)'],DAMstageDischarge['Q-AV(L/sec)'],'.',color='g',markeredgecolor='k',label='FOREST A-V')
    
    PowerFit(DAM_HECstageDischarge['stage(cm)'],DAM_HECstageDischarge['Q(L/sec)'],xy,both,c='b',ls='-',label='DAM_HECpower') ## rating from DAM_HEC
    both.plot(DAM_HECstageDischarge['stage(cm)'],DAM_HECstageDischarge['Q(L/sec)'],'.',color='b',label='DAM HEC-RAS Model')

    ## Label subplots    
    site_lbj.set_title('VILLLAGE'),site_lbj.set_xlabel('Stage(cm)'),site_lbj.set_ylabel('Q(L/sec)')
    site_dam.set_title('FOREST'),site_dam.set_xlabel('Stage(cm)'),site_dam.set_ylabel('Q(L/sec)')
    both.set_title('Selected Ratings'),both.set_xlabel('Stage(cm)'),both.set_ylabel('Q(L/sec)'),both.yaxis.tick_right(),both.yaxis.set_label_position('right')
    ## Format subplots
    site_lbj.set_xlim(10,PT1['stage'].max()+10),site_lbj.set_ylim(10,4000)
    site_dam.set_xlim(10,PT3['stage'].max()+10),site_dam.set_ylim(10,4000)
    ## Legends
    #site_lbj.legend(loc='best',ncol=2,fancybox=True),site_dam.legend(loc='best',ncol=2,fancybox=True),both.legend(loc='best',ncol=2,fancybox=True)
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

#### Calculate Discharge
## Calculate Q for LBJ: From AV rating, from A-Manning, from Manning-Rectangular Cross Section
LBJ = DataFrame(PT1,columns=['stage']) ## Build DataFrame with all stage records for location (cm)
LBJ['Q-AV']=(LBJ['stage']*LBJ_AV.beta[0]) + LBJ_AV.beta[1] ## Calculate Q from AV rating (L/sec)
LBJ['Q-AManningV']= (LBJ['stage']*LBJ_AManningV.beta[0]) + LBJ_AManningV.beta[1] ## Calculate Q from A-Mannings rating (L/sec)

a = 10**LBJ_AVLog.beta[1] # beta[1] is the intercept = log10(a), so a = 10**beta[1] 
b = LBJ_AVLog.beta[0] # beta[0] is the slope = b

LBJ['Q-AVLog'] = a * (LBJ['stage']**b)
LBJ['Q-AManningVLog'] = (10**LBJ_AManningVLog.beta[1])*(LBJ['stage']**LBJ_AManningVLog.beta[0])

## Build Dataframe of all discharge measurments
DAM = DataFrame(PT3,columns=['stage']) ## Build DataFrame with all stage records for location
DAM['Q-AV']=(DAM['stage']*DAM_AV.beta[0]) + DAM_AV.beta[1] ## Calculate Q from AV rating=
DAM['Q-AVLog']=(10**DAM_AVLog.beta[1])*(DAM['stage']**DAM_AVLog.beta[0]) 
DAM['Q-D_Flume']=DAM['stage'].dropna().apply(lambda x: D_Flume(x))
DAM['Q-HEC']=(10**DAM_HEC.beta[1])*(DAM['stage']**DAM_HEC.beta[0]) 

## Aggregate LBJ
LBJq = (LBJ*900) ## Q above is in L/sec; L/sec * 900sec/15Min = L/15Min
LBJq['stage']=PT1['stage'] ## put unaltered stage back in

LBJhourly = LBJq.resample('H',how='sum')
LBJdaily = DataFrame(LBJq.resample('D',how='sum'))

## Aggregate DAM
DAMq= (DAM*900)## Q above is in L/sec; L/sec * 900sec/15Min = L/15Min
DAMq['stage']=PT3['stage'] ## put unaltered stage back in

DAMhourly = DAMq.resample('H',how='sum')
DAMdaily = DAMq.resample('D',how='sum')