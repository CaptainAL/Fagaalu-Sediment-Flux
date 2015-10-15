# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 07:04:59 2015

@author: Alex
"""

### THIS CODE IS FOR THE DEPRECATED STAGE THRESHOLD METHOD OF STORM SEPARATION
### DEPRECATED OCTOBER 2015

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
    #LBJstormintervalsXL = pd.ExcelFile(datadir+'LBJ_StormIntervals_filtered.xlsx')
    #LBJ_StormIntervals = LBJstormintervalsXL.parse('StormIntervals',header=0,parse_cols='A:C',index_col=0)
    
    LBJstormintervalsXL = pd.ExcelFile(datadir+'StormIntervals_defined.xlsx')
    LBJ_StormIntervals = LBJstormintervalsXL.parse('StormIntervals',header=0,parse_cols='A:C',index_col=0)    
    
    ## 
    DAMstormintervalsXL = pd.ExcelFile(datadir+'DAM_StormIntervals_filtered.xlsx')
    DAM_StormIntervals = DAMstormintervalsXL.parse('StormIntervals',header=0,parse_cols='A:C',index_col=0)
    
    DAM_StormIntervals = LBJ_StormIntervals
    QUARRY_StormIntervals, DAM_StormIntervals = DAM_StormIntervals, DAM_StormIntervals

### SAVE Storm Intervals for LATER
LBJ_StormIntervals.to_excel(datadir+'Q/StormIntervals/LBJ_StormIntervals.xlsx')
QUARRY_StormIntervals.to_excel(datadir+'Q/StormIntervals/QUARRY_StormIntervals.xlsx')
DAM_StormIntervals.to_excel(datadir+'Q/StormIntervals/DAM_StormIntervals.xlsx')



