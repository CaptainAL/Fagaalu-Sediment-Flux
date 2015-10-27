# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 05:52:52 2015

@author: Alex
"""

# for predicting SSY needed new storm intervals from DAM; not anymore, they're combined anyway

## Need to get storm intervals for DAM Q timeseries
## Define Storm Intervals at DAM
def DAM_Q_storm_with_new_DAMstormIntervals():
    All_Storms=SeparateHydrograph(hydrodata=PT3['stage'])
    ## Combine Storm Events where the storm end is the storm start for the next storm
    All_Storms['next storm start']=All_Storms['start'].shift(-1) ## add the next storm's start and end time to the storm in the row above (the previous storm)
    All_Storms['next storm end']=All_Storms['end'].shift(-1)
    need_to_combine =All_Storms[All_Storms['end']==All_Storms['next storm start']] #storms need to be combined if their end is the same time as the next storm's start
    need_to_combine['end']=need_to_combine['next storm end'] # change the end of the storm to the end of the next storm to combine them
    All_Storms=All_Storms.drop(need_to_combine.index) #drop the storms that need to be combined
    All_Storms=All_Storms.append(need_to_combine).sort(ascending=True) #append back in the combined storms
    All_Storms=All_Storms.drop_duplicates(cols=['end']) 
    
    Qstorms_DAM=Sum_Storms(All_Storms,DAMq['Q']) 
    Qstorms_DAM.columns=['Qstart','Qend','Qcount','Qsum','Qmax']
    Qstorms_DAM['Qmax']=Qstorms_DAM['Qmax']/900 ## Have to divide by 900 to get instantaneous 
    
    Pstorms_DAM = Sum_Storms(All_Storms,PrecipFilled['Precip'],60) ##30minute offset to get precip before stage started rising
    Pstorms_DAM.columns=['Pstart','Pend','Pcount','Psum','Pmax']
    Pstorms_DAM['EI'] = DAM_Stormdf['EI']
    Qstorms_DAM['Psum'] = Pstorms_DAM['Psum']
    return Qstorms_DAM
DAM_Qstorms_DAM_intervals = DAM_Q_storm_with_new_DAMstormIntervals()