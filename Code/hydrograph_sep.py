# -*- coding: utf-8 -*-
"""
Created on Tue Oct 06 14:12:55 2015

@author: Alex
"""

#### LBJ Baseflow Separation
from numpy import *
import scipy as sp
from pandas import *
from rpy2.robjects.packages import importr
import rpy2.robjects as ro
import pandas.rpy.common as com

#
## Make sure R is communicating
ro.r('x=c()')
ro.r('x[1]=22')
ro.r('x[2]=44')
print(ro.r('x'))

LBJ_Q = pd.DataFrame({'Q':LBJ['Q'].values},index = LBJ['Q'].index)

## convert to R Data Frame
hydrograph = com.convert_to_r_dataframe(LBJ_Q)
## Send to R
ro.globalenv['flowdata'] = hydrograph
## replace blanks with NA
ro.r('flowdata[flowdata==""]<-NA')
## Drop NA rows from Data Frame
ro.r('flow = flowdata[complete.cases(flowdata),]')
## run Baseflow Separation
ro.r("library(EcoHydRology)")
print 'running R baseflow separation....'
ro.r("base = BaseflowSeparation(flow)")
print 'baseflow separated!'
## Convert back to Pandas
flowdf = com.load_data("base")
## reindex with the original time index WITHOUT NA's (they're dropped in the R code)
flow = pd.DataFrame({'Flow':LBJ_Q['Q'].dropna().values,'bt':flowdf['bt'].values,'qft':flowdf['qft'].values},index=LBJ_Q.dropna().index)



stormthresh = 0

StormFlow = flow['qft'].where(flow['qft']>stormthresh) 
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
    start = t[0]-dt.timedelta(minutes=30)
    end= t[1]
    event = flow.ix[start:end]
    eventduration = end-start
    seconds = eventduration.total_seconds()
    hours = seconds / 3600
    eventduration = round(hours,2)
    if event['qft'].count() >= minimum_length and event['qft'].max()>=100:
        eventlist.append([start,end,eventduration])
    

Events=pd.DataFrame(eventlist,columns=['start','end','duration (hrs)'])
#drop_rows = Events[Events['duration (min)'] <= timedelta(minutes=120)] ## Filters events that are too short
#Events = Events.drop(drop_rows.index) ## Filtered DataFrame of storm start,stop,count,sum


plt.close('all')

fig, ax = plt.subplots(1,1)
plt.plot_date(flow.index,flow['Flow'],marker='None',ls='-',c='k')
plt.plot_date(flow.index,flow['bt'],marker='None',ls='-',c='grey')

ax2 = ax.twinx()
PrecipFilled['Precip'].plot(ax=ax2,color='b',ls='steps-pre',label='Timu1')

for storm in Events.iterrows(): ## shade over storm intervals
    ax.axvspan(storm[1]['start'],storm[1]['end'],ymin=0,ymax=200,facecolor='grey', alpha=0.25)


plt.show()