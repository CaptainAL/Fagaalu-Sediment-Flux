# -*- coding: utf-8 -*-
"""
Created on Tue Oct 06 14:12:55 2015

@author: Alex
"""

flow = pd.DataFrame.from_csv("C:/Users/Alex/Documents/GitHub/Fagaalu-Sediment-Flux/Data/Q/flow.csv")


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

for storm in Events.iterrows(): ## shade over storm intervals
    ax.axvspan(storm[1]['start'],storm[1]['end'],ymin=0,ymax=200,facecolor=shade_color, alpha=0.25)


plt.show()