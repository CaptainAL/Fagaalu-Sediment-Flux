from pandas import DataFrame
from math import isnan
from numpy import nan
from datetime import timedelta

#### Hydrograph Separation #####
#### split into storms by defining stormthresh


def SeparateHydrograph(hydrodata='stage',minimum_length=8):
    params = hydrodata.describe()
    mean = params[1]
    std = params[2]
    minimum = params[3]
    maximum = params[7]
    quartiles= params[4:8]
    stormthresh = mean+std
    print 'Storm threshold= '+'%.1f'%stormthresh
    StormFlow = hydrodata.where(hydrodata>stormthresh) ##returns list of data points that meet the condition, the rest are NaN (same shape as original array)
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

    Events=DataFrame(eventlist,columns=['start','end','duration (hrs)'])
    #drop_rows = Events[Events['duration (min)'] <= timedelta(minutes=120)] ## Filters events that are too short
    #Events = Events.drop(drop_rows.index) ## Filtered DataFrame of storm start,stop,count,sum
    return Events

def StormSums(Stormslist,Data,offset=0):
    eventlist = []
    index =[]
    print 'Summing storms...'
    for storm_index,storm in Stormslist.iterrows():
        start = storm['start']-timedelta(minutes=offset) ##if Storms are defined by stream response you have to grab the preceding precip data
        end= storm['end']
        data = True ## Innocent until proven guilty
        try:
            print str(start) +' '+str(end)
            event = Data.ix[start:end] ### slice list of Data for event
        except KeyError:
            start = start+timedelta(minutes=15) ## if the start time falls between 2 30minute periods
            print 'change storm start to '+str(start)            
            try:
                event = Data.ix[start:end]
            except KeyError:
                end = end+timedelta(minutes=15)
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

