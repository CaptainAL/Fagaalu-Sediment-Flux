# -*- coding: utf-8 -*-
"""
Created on Fri Nov 06 08:39:58 2015

@author: Alex
"""

## TECHNICAL NOTE
## Stage-Discharge rating curve construction

## Based off Duvert 2010 and Duvert 2010 tech note

## Goal: document the development of T-SSC rating curves in Faga'alu (maybe another one for Nuuuli)


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
    SSC = SSC[['Location','Sample #','NTU','SSC (mg/L)']]
    return SSC

## ALL SSC samples
SSC= loadSSC(pd.ExcelFile(datadir+'SSC/SSC_grab_samples.xlsx'),'ALL_MASTER',round_to_15=False)
SSC['SSC (mg/L)'] = SSC['SSC (mg/L)'].where(SSC['SSC (mg/L)']>0, 0) ## Filter out any negative values

## ALL SSC stormflow samples
SSC_all_storm = pd.DataFrame()
for storm_index,storm in All_Storms.iterrows():
    #print storm[1]['start']
    start, end =storm['start'], storm['end']
    SSC_during_storm = SSC[(SSC.index > start) & (SSC.index < end)]
    SSC_all_storm = SSC_all_storm.append(SSC_during_storm)
    
## ALL SSC baseflow samples
SSC_all_baseflow = SSC.drop(SSC_all_storm.index) 

##ALL SSC samples pre-mitigation
SSC_pre_mitigation_all = SSC[SSC.index < Mitigation]
SSC_pre_mitigation_storm = SSC_all_storm[SSC_all_storm.index < Mitigation]
SSC_pre_mitigation_baseflow = SSC_all_baseflow[SSC_all_baseflow.index < Mitigation]

##ALL SSC samples post-mitigation
SSC_post_mitigation_all = SSC[SSC.index > Mitigation]
SSC_post_mitigation_storm = SSC_all_storm[SSC_all_storm.index > Mitigation]
SSC_post_mitigation_baseflow = SSC_all_baseflow[SSC_all_baseflow.index > Mitigation]

## Put SSC subsets in a dictionary
SSC_dict={'ALL':SSC, 
'ALL-storm':SSC_all_storm,
'ALL-baseflow':SSC_all_baseflow,
'Pre-ALL':SSC_pre_mitigation_all,
'Pre-storm':SSC_pre_mitigation_storm,
'Pre-baseflow':SSC_pre_mitigation_baseflow,
'Post-ALL':SSC_post_mitigation_all,
'Post-storm':SSC_post_mitigation_storm,
'Post-baseflow':SSC_post_mitigation_baseflow}

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
LBJ_grab_count = SampleCounts['#ofSSCsamples'][SampleCounts['Location']=='LBJ'].ix[1] ## the # in .ix[#] is the row number in SampleCounts above
#LBJ_R2 = SSC[SSC['Location'].isin(['LBJ R2'])].resample('5Min',fill_method='pad',limit=0)
#LBJ_R2_grab_count = SampleCounts['#ofSSCsamples'][SampleCounts['Location']=='LBJ R2'].ix[12] ## the # in .ix[#] is the row number in SampleCounts above

## QUARRY
# Just DT
QUARRYgrab =SSC[SSC['Location'].isin(['DT'])]#.resample('5Min',fill_method='pad',limit=0)
QUARRYgrab['index']= QUARRYgrab.index
QUARRY_grab_count =  SampleCounts['#ofSSCsamples'][SampleCounts['Location']=='DT'].ix[3] ## the # in .ix[#] is the row number in SampleCounts above
# Just R2
QUARRY_R2 = SSC[SSC['Location'].isin(['R2'])]#.resample('5Min',fill_method='pad',limit=0)
QUARRY_R2['index'] = QUARRY_R2.index
QUARRY_R2_grab_count =  SampleCounts[SampleCounts['Location']=='R2']['#ofSSCsamples']#.ix[5] ## the # in .ix[#] is the row number in SampleCounts above
# combined DT and R2
QUARRY_DT_and_R2 = SSC[SSC['Location'].isin(['DT','R2'])]
QUARRY_DT_and_R2['index'] = QUARRY_DT_and_R2.index

## DAM
DAMgrab = SSC[SSC['Location'].isin(['DAM'])]#.resample('5Min',fill_method='pad',limit=0)
DAMgrab['index'] = DAMgrab.index
DAM_grab_count =  SampleCounts['#ofSSCsamples'][SampleCounts['Location']=='DAM'].ix[2] ## the # in .ix[#] is the row number in SampleCounts above


## ADD Grab samples to Site DataFrames
LBJ['Grab-SSC-mg/L'] = LBJgrab.drop_duplicates(cols='index')['SSC (mg/L)'].resample('15Min',fill_method='pad',limit=0)
QUARRY['GrabDT-SSC-mg/L'] = QUARRYgrab.drop_duplicates(cols='index')['SSC (mg/L)'].resample('15Min',fill_method='pad',limit=0)
QUARRY['GrabR2-SSC-mg/L'] = QUARRY_R2.drop_duplicates(cols='index')['SSC (mg/L)'].resample('15Min',fill_method='pad',limit=0)
QUARRY['Grab-SSC-mg/L'] = QUARRY_DT_and_R2.drop_duplicates(cols='index')['SSC (mg/L)'].resample('15Min',fill_method='pad',limit=0)
DAM['Grab-SSC-mg/L'] = DAMgrab.drop_duplicates(cols='index')['SSC (mg/L)'].resample('15Min',fill_method='pad',limit=0)



#### IMPORT TURBIDITY DATA
#from load_from_MASTER_XL import TS3000,YSI,OBS,loadSSC
def TS3000(XL,sheet='DAM-TS3K'):
    print 'loading : '+sheet+'...'
    TS3K = XL.parse(sheet,header=0,parse_cols='A,F',index_col=0,parse_dates=True)
    TS3K.columns=['NTU']
    return TS3K
def YSI(XL,resample_interval,sheet='LBJ-YSI'):
    print 'loading : '+sheet+'...'
    YSI = XL.parse(sheet,header=4,parse_cols='A:H',parse_dates=[['Date','Time']],index_col=['Date_Time'])
    ## take off the 'seconds' so they're on 5Min interval
    YSI=YSI.resample(resample_interval,closed='right')
    YSI['NTU raw']=YSI['NTU']
    return YSI
def OBS(XL,sheet='LBJ-OBS'):
    print 'loading : '+sheet+'...'
    OBS=XL.parse(sheet,header=4,parse_cols='A:L',parse_dates=True,index_col=0,na_values='NAN')
    return OBS
    
def correct_Turbidity(Turbidity_Correction_XL,location,Tdata):
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
        
    Turbidity_Correction = Turbidity_Correction_XL.parse(location,parse_dates=False)
    Correction=pd.DataFrame()
    for correction in Turbidity_Correction.iterrows():
        t1_date = correction[1]['T1_date']
        t1_time = correction[1]['T1_time']
        t1 = my_parser(t1_date,t1_time)
        t2_date = correction[1]['T2_date']
        t2_time = correction[1]['T2_time']
        t2 = my_parser(t2_date,t2_time)
        ntu = correction[1]['NTU']    
        #print t1,t2, ntu
        Correction = Correction.append(pd.DataFrame({'NTU':ntu},index=pd.date_range(t1,t2,freq='5Min')))
    Correction = Correction.reindex(pd.date_range(start2012,stop2014,freq='5Min'))
    Tdata['Manual_Correction'] = Correction['NTU']
    Tdata['NTU_corrected_Manual'] = Tdata['NTU raw'] + Tdata['Manual_Correction']
    Tdata['NTU']=Tdata['NTU_corrected_Manual'].where(Tdata['NTU_corrected_Manual']>=0,Tdata['NTU raw'])#.round(0)
    return Tdata
    
Turbidity_Correction_XL = pd.ExcelFile(datadir+'T/TurbidityCorrection.xlsx')    
  
## Turbidimeter Data DAM
## TS3000
DAM_TS3K = TS3000(XL,'DAM-TS3K')
## filter negative values
DAM_TS3K = DAM_TS3K[DAM_TS3K>=0]

## YSI at DAM
DAM_YSI = YSI(XL,'5Min','DAM-YSI')
#DAM_YSI = DAM_YSI.resample('15Min',closed='right').shift(1)
## Just take readings at '15Min' intervals
DAM_YSI_15min = DAM_YSI[2:].asfreq('15Min')


## round data
for column in ['Temp','NTU raw','NTU']:
    DAM_YSI[column] = DAM_YSI[column].round(0)
for column in ['SpCond','Battery']:
    DAM_YSI[column] = DAM_YSI[column].round(1)
for column in ['TDS','Sal']:
    DAM_YSI[column] = DAM_YSI[column].round(3)
    
## Correct negative NTU values
DAM_YSI = correct_Turbidity(Turbidity_Correction_XL,'DAM-YSI',DAM_YSI)

def plot_YSI(df,SSC_at_location,end_time,show=True):
    fig, ntu = plt.subplots(1,1,figsize=(8,4),sharex=True,sharey=True)
    ## NTU
    ntu.plot_date(df['NTU'].index,df['NTU'],label='NTU',marker='None',ls='-',c='k')
    ntu.set_ylim(0,4000)
    ## legends
    for ax in fig.axes:
        print ax
        ax.legend()
        showstormintervals(ax,All_Storms)
        SSC_at_location['SSC (mg/L)'].plot(ax=ax,ls='none',marker='.',color='r')
        ax.set_xlim(df.index[0],end_time)
        
    ## Precip
    p = ntu.twinx()
    precip = PrecipFilled.reindex(pd.date_range(start2012,stop2014,freq='15Min'))
    p.plot_date(precip['Precip'].index,precip['Precip'],color='b',alpha=0.5,marker='None',ls='steps-pre',label='PrecipFilled')
    p.spines["right"].set_visible(True),p.set_ylabel('Precip mm'),p.set_ylim(0,25)
    
    plt.tight_layout(pad=0.1)
    if show== True:
        plt.show()
    return
#plot_YSI(DAM_YSI,SSC[SSC['Location']=='DAM'],end_time=stop2014,show=True)
#plot_YSI(DAM_YSI,SSC[SSC['Location']=='DAM'],dt.datetime(2015,1,10),show=True)

## Turbidimeter Data QUARRY
 
QUARRY_OBS = pd.ExcelFile(datadir+'T/QUARRY-OBS.xlsx').parse('QUARRY-OBS',header=4,parse_cols='A:L',parse_dates=True,index_col=0)
QUARRY_OBS = OBS(XL,'QUARRY-OBS')
QUARRY_OBS['NTU']=QUARRY_OBS['Turb_SS_Mean'].round(0)
## Filter out values that are over 4,000 (assumed to be errors)
QUARRY_OBS['NTU'] = QUARRY_OBS['NTU'][QUARRY_OBS['NTU']<=4000]

def plot_OBS_QUARRY(df,SSC_at_location,end_time,show=True):
    fig, ntu = plt.subplots(1,1,figsize=(8,4),sharex=True,sharey=True)
    ## NTU
    ntu.plot_date(df['NTU'].index,df['NTU'],label='QUARRY NTU',marker='None',ls='-',c='k')
    ntu.set_ylim(0,4000)
    ## legends
    for ax in fig.axes:
        print ax
        ax.legend()
        showstormintervals(ax,All_Storms)
        SSC_at_location['SSC (mg/L)'].plot(ax=ax,ls='none',marker='.',color='r')
        ax.set_xlim(df.index[0],end_time)
        
    ## Precip
    p = ntu.twinx()
    precip = PrecipFilled.reindex(pd.date_range(start2012,stop2014,freq='15Min'))
    p.plot_date(precip['Precip'].index,precip['Precip'],color='b',alpha=0.5,marker='None',ls='steps-pre',label='PrecipFilled')
    p.spines["right"].set_visible(True),p.set_ylabel('Precip mm'),p.set_ylim(0,25)
    
    plt.tight_layout(pad=0.1)
    if show== True:
        plt.show()
    return
#plot_OBS_QUARRY(QUARRY_OBS,SSC[SSC['Location'].isin(['DT','R2'])],end_time=stop2014,show=True)

## Turbidimeter Data LBJ
## LBJ YSI
LBJ_YSIa = YSI(XL,'5Min','LBJ-YSIa')
LBJ_YSIa_15Min = LBJ_YSIa.resample('15Min',closed='right').shift(1)
LBJ_YSIb = YSI(XL,'15Min','LBJ-YSIb')
LBJ_YSI = pd.concat([LBJ_YSIa_15Min,LBJ_YSIb])[:dt.datetime(2012,5,23,6,0)]
for column in LBJ_YSI.columns:
    #print column
    LBJ_YSI[column] = LBJ_YSI[column].round(0)
#plot_YSI(LBJ_YSIa,SSC[SSC['Location']=='LBJ'],end_time=stop2012,show=True)
## From this graph it looks like YSI data at LBJ from April 1,2012 - May 6 is messed up
LBJ_YSI.ix[dt.datetime(2012,4,1):dt.datetime(2012,5,7)] = np.nan ## clean data

## LBJ OBS
# OBS with only Avg BS and SS at 15Min 
LBJ_OBSa = OBS(XL,'LBJ-OBSa')
## remove junk data
LBJ_OBSa =pd.concat([LBJ_OBSa[dt.datetime(2013,3,11):dt.datetime(2013,4,1)],LBJ_OBSa[dt.datetime(2013,5,5):dt.datetime(2013,6,4)],LBJ_OBSa[dt.datetime(2013,6,7):]]) 
## round to zero
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
def plot_OBSa(df,SSCloc,show=True):
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
        showstormintervals(ax,All_Storms)
        SSCloc['SSC (mg/L)'].plot(ax=ax,ls='none',marker='.',color='r')
        ax.set_xlim(df.index[0],stop2013)
        
    ## Precip
    p = comb.twinx()
    precip = PrecipFilled.reindex(pd.date_range(start2012,stop2014,freq='15Min'))
    p.plot_date(precip['Precip'].index,precip['Precip'],color='b',alpha=0.5,marker='None',ls='steps-pre',label='PrecipFilled')
    p.spines["right"].set_visible(True),p.set_ylabel('Precip mm'),p.set_ylim(0,25)
    ## Turn off x axis in upper plots
    for ax in fig.axes[:-2]:
        ax.xaxis.set_visible(False)  
    plt.tight_layout(pad=0.1)
    if show== True:
        plt.show()
    return
#plot_OBSa(LBJ_OBSa,SSC[SSC['Location']=='LBJ'],show=True)
    
## PLOT OBSb BS Time Series with SSC grab samples
def plot_OBSb_BS(df,SSCloc,show=True):
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
        showstormintervals(ax,All_Storms)
        SSCloc['SSC (mg/L)'].plot(ax=ax,ls='none',marker='.',color='r')
        ax.set_xlim(df.index[0],Mitigation)
        ax.locator_params(nbins=4,axis='y') 
    ## Precip
    p = comb.twinx()
    precip = PrecipFilled.reindex(pd.date_range(start2012,stop2014,freq='15Min'))
    p.plot_date(precip['Precip'].index,precip['Precip'],color='b',alpha=0.5,marker='None',ls='steps-pre',label='PrecipFilled')
    p.spines["right"].set_visible(True),p.set_ylabel('Precip mm'),p.set_ylim(0,25)
        
    for ax in fig.axes[:-1]:
        ax.xaxis.set_visible(False)    
    plt.tight_layout(pad=0.1)
    if show== True:
        plt.show()
    return
#plot_OBSb_BS(LBJ_OBSb,SSC[SSC['Location']=='LBJ'],show=True)

## PLOT OBSb SS Time Series with SSC grab samples  
def plot_OBSb_SS(df,SSCloc,show=True):
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
        showstormintervals(ax,All_Storms)
        SSCloc['SSC (mg/L)'].plot(ax=ax,ls='none',marker='.',color='r')
        ax.set_xlim(df.index[0],Mitigation)
        ax.locator_params(nbins=4,axis='y')  
    ## Precip
    p = comb.twinx()
    precip = PrecipFilled.reindex(pd.date_range(start2012,stop2014,freq='15Min'))
    p.plot_date(precip['Precip'].index,precip['Precip'],color='b',alpha=0.5,marker='None',ls='steps-pre',label='PrecipFilled')
    p.spines["right"].set_visible(True),p.set_ylabel('Precip mm'),p.set_ylim(0,25)
    ## Turn off x axis in upper plots
    for ax in fig.axes[:-2]:
        ax.xaxis.set_visible(False) 
    plt.tight_layout(pad=0.1)
    if show== True:
        plt.show()
    return
#plot_OBSb_SS(LBJ_OBSb,SSC[SSC['Location']=='LBJ'],show=True)
#plot_OBSb_SS(QUARRY_OBS,SSC[SSC['Location'].isin(['DT','R2'])],show=True)


#### TURBIDITY TO SSC RATING CURVES
#### T to SSC rating curve for FIELD INSTRUMENTS
def T_SSC_rating(SSCdata,Turbidimeter_Data,TurbidimeterName='T',location='LBJ',T_interval='15Min',Intercept=False,log=False):
    T_name = TurbidimeterName+'-NTU'
    ## Get just the samples matching the location name and roll to 5Min.
    SSCsamples = SSCdata[SSCdata['Location'].isin([location])].resample(T_interval,fill_method = 'pad',limit=0) 
    ## Filter null values for mg/L
    SSCsamples = SSCsamples[pd.notnull(SSCsamples['SSC (mg/L)'])] 
    ## Get turbidimeter NTU data 
    SSCsamples[T_name]=Turbidimeter_Data
    ## Filter null values for NTU
    SSCsamples = SSCsamples[pd.notnull(SSCsamples[T_name])]
    ## Regression for rating curve equation
    T_SSC_rating = pd.ols(y=SSCsamples['SSC (mg/L)'],x=SSCsamples[T_name],intercept=Intercept)
    ## Calculate RMSE of rating curve
    mean_observed = SSCsamples['SSC (mg/L)'].mean()
    rmse_percent = T_SSC_rating.rmse/mean_observed * 100.
    ## Return the Rating, Turbidity and Grab Sample SSC data, and the RMSE
    return T_SSC_rating, SSCsamples[[T_name,'SSC (mg/L)']], int(rmse_percent)    
    
## Plot ALL T-SSC measured in LAB 
def T_SSC_ALL_LAB(show=False):
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
    plt.xlabel('Measured Turbidity (NTU)'), plt.ylabel('SSC mg/L')
    plt.xlim(-10,2000), plt.ylim(-10,2000)
    plt.legend(loc='best')
    show_plot(show,fig)
    return
#T_SSC_ALL(show=True)


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
    NTU=T_SSC_rating(SSC,df['NTU'],location=SSC_loc,T_interval='5Min',Intercept=False,log=False)
    ntu.scatter(NTU[1]['T-NTU'],NTU[1]['SSC (mg/L)'],c='k')
    ntu.plot(xy,xy*NTU[0].beta[0],ls='-',c='k',label='NTU '+r'$r^2$'+"%.2f"%NTU[0].r2)
    ntu.set_title(SSC_loc+' NTU '+r'$r^2=$'+"%.2f"%NTU[0].r2)
    ## Zoom in
    ntu_zoom.scatter(NTU[1]['T-NTU'],NTU[1]['SSC (mg/L)'],c='k')
    ntu_zoom.plot(xy,xy*NTU[0].beta[0],ls='-',c='k',label='NTU '+r'$r^2$'+"%.2f"%NTU[0].r2)
    ntu_zoom.set_title(SSC_loc+' NTU '+r'$r^2=$'+"%.2f"%NTU[0].r2)
    ntu_zoom.text(0.9,0.9,'Zoomed',verticalalignment='bottom', horizontalalignment='right',transform=ntu_zoom.transAxes)
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
#plotYSI_ratings(df=DAM_YSI,df_SRC=None,SSC_loc='DAM',Use_All_SSC=False,storm_samples_only=True) ## Pre-mitigation only, Storm only
## LBJ YSI rating
#plotYSI_ratings(LBJ_YSI,df_SRC=None,SSC_loc='LBJ',Use_All_SSC=False,storm_samples_only=False) ## Pre-mitigation only
#plotYSI_ratings(LBJ_YSI,df_SRC=None,SSC_loc='LBJ',Use_All_SSC=False,storm_samples_only=True) ## Pre-mitigation only, Storm only

## Plot T-SSC from YSI at DAM and LBJ to compare
def plotYSI_compare_ratings(DAM_YSI,LBJ_YSI,Use_All_SSC=False,storm_samples_only=True,show=True,save=False,filename=''):
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
    
    fig, ntu= plt.subplots(1,1,figsize=(5,4))
    max_y, max_x = LBJ_YSI['NTU'].max(),LBJ_YSI['NTU'].max()
    xy = np.linspace(0,max_y)  
    ## LBJ
    lbj=T_SSC_rating(SSC,LBJ_YSI['NTU'],location='LBJ',T_interval='15Min',Intercept=False,log=False)
    ntu.plot(lbj[1]['T-NTU'],lbj[1]['SSC (mg/L)'],ls='none',marker='o',fillstyle='none',c='grey',label='FG3')
    ntu.plot(xy,xy*lbj[0].beta[0],ls='-',c='grey',label='FG3 YSI '+r'$r^2$'+"%.2f"%lbj[0].r2)
    labelindex_subplot(ntu,lbj[1].index,lbj[1]['T-NTU'],lbj[1]['SSC (mg/L)'])  
    ## DAM
    dam=T_SSC_rating(SSC,DAM_YSI['NTU'],location='DAM',T_interval='15Min',Intercept=False,log=False)
    ntu.plot(dam[1]['T-NTU'],dam[1]['SSC (mg/L)'],ls='none',marker='s',c='k',label='FG1')
    ntu.plot(xy,xy*dam[0].beta[0],ls='-',c='k',label='FG1 YSI '+r'$r^2$'+"%.2f"%dam[0].r2)
    labelindex_subplot(ntu,dam[1].index,dam[1]['T-NTU'],dam[1]['SSC (mg/L)'])    
    ## Format subplots
    ntu.set_xlabel('NTU')
    ntu.set_xlim(0,3800)
    ntu.set_ylim(0,3800)
    ntu.plot([0,3800],[0,3800],ls='--',c='k',label='1:1')
    ntu.legend(loc='lower right')
    plt.tight_layout(pad=0.1)
    for ax in fig.axes:
        ax.locator_params(nbins=4)
    #letter_subplots(fig,x=0.1,y=0.95,vertical='top',horizontal='right',Color='k',font_size=10,font_weight='bold')
    show_plot(show)
    savefig(save,filename)
    return
#plotYSI_compare_ratings(DAM_YSI,LBJ_YSI,Use_All_SSC=False,storm_samples_only=False,show=True,save=False,filename='') ## Pre-mitigation
#plotYSI_compare_ratings(DAM_YSI,LBJ_YSI,Use_All_SSC=False,storm_samples_only=True,show=True,save=False,filename='') ## Pre-mitigation, storm only

## PLOT T-SSC rating for OBSa (BS and SS Avg only)
def OBSa_compare_ratings(df,SSC_loc,Use_All_SSC=False,storm_samples_only=False,show=True,save=False,filename='',sub_plot_count=0):
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
    ss_average=T_SSC_rating(SSC,df['Turb_SS_Avg'],location=SSC_loc,T_interval='5Min',Intercept=False,log=False)
    ss_avg.scatter(ss_average[1]['T-NTU'],ss_average[1]['SSC (mg/L)'],c='k')
    ss_avg.plot(xy,xy*ss_average[0].beta[0],ls='-',c='k',label='SS_Avg '+r'$r^2$'+"%.2f"%ss_average[0].r2)   
    ss_avg.set_title(SSC_loc+' SS_Avg '+r'$r^2=$'+"%.2f"%ss_average[0].r2) 
    ss_avg.set_xlabel('SS Avg')
    ss_avg.legend()
    plt.tight_layout(pad=0.1)
    
    for ax in fig.axes:
        ax.locator_params(nbins=4)
        ax.set_xlim(0,max_x), ax.set_ylim(0,max_y)
        
    #letter_subplots(fig,x=0.1,y=0.95,vertical='top',horizontal='right',Color='k',font_size=10,font_weight='bold')
    show_plot(show)
    savefig(save,filename)
    return
#OBSa_compare_ratings(df=LBJ_OBSa,SSC_loc='LBJ',Use_All_SSC=False,storm_samples_only=False,show=True,save=False,filename='')  
#OBSa_compare_ratings(df=LBJ_OBSa,SSC_loc='LBJ',Use_All_SSC=False,storm_samples_only=True,show=True,save=False,filename='')  
    
## PLOT T-SSC ratings with all parameters (BS and SS Mean, Median, Min, Max)
def OBSb_compare_ratings(df,SSC_loc,Use_All_SSC=False,storm_samples_only=True,show=True,save=False,filename='',sub_plot_count=0):
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
    bs_median=T_SSC_rating(SSC,df['Turb_BS_Median'],location=SSC_loc,T_interval='15Min',Intercept=False,log=False)
    bs_med.scatter(bs_median[1]['T-NTU'],bs_median[1]['SSC (mg/L)'],c='k')
    bs_med.plot(xy,xy*bs_median[0].beta[0],ls='-',c='k',label='BS_Median'+r'$r^2$'+"%.2f"%bs_median[0].r2)
    #bs_med.set_title('BS_Median '+r'$r^2=$'+"%.2f"%bs_median[0].r2)
    bs_med.set_ylabel('SSC (mg/L)'),bs_med.set_xlabel('BS Median') 
    ## BS Mean
    bs_mean=T_SSC_rating(SSC,df['Turb_BS_Mean'],location=SSC_loc,T_interval='15Min',Intercept=False,log=False)
    bs_mea.scatter(bs_mean[1]['T-NTU'],bs_mean[1]['SSC (mg/L)'],c='k')
    bs_mea.plot(xy,xy*bs_mean[0].beta[0],ls='-',c='k',label='BS_Mean'+r'$r^2$'+"%.2f"%bs_mean[0].r2)
    #bs_mea.set_title('BS_Mean '+r'$r^2=$'+"%.2f"%bs_mean[0].r2)  
    bs_mea.set_xlabel('BS Mean')
    ## BS Min
    bs_minimum=T_SSC_rating(SSC,df['Turb_BS_Min'],location=SSC_loc,T_interval='15Min',Intercept=False,log=False)
    bs_min.scatter(bs_minimum[1]['T-NTU'],bs_minimum[1]['SSC (mg/L)'],c='k')
    bs_min.plot(xy,xy*bs_minimum[0].beta[0],ls='-',c='k',label='BS_Min'+r'$r^2$'+"%.2f"%bs_minimum[0].r2)
    #bs_min.set_title('BS_Min '+r'$r^2=$'+"%.2f"%bs_minimum[0].r2)
    bs_min.set_xlabel('BS Min')
    ## BS Max
    bs_maximum=T_SSC_rating(SSC,df['Turb_BS_Max'],location=SSC_loc,T_interval='15Min',Intercept=False,log=False)
    bs_max.scatter(bs_maximum[1]['T-NTU'],bs_maximum[1]['SSC (mg/L)'],c='k')
    bs_max.plot(xy,xy*bs_maximum[0].beta[0],ls='-',c='k',label='BS_Max'+r'$r^2$'+"%.2f"%bs_maximum[0].r2)    
    #bs_max.set_title('BS_Max '+r'$r^2=$'+"%.2f"%bs_maximum[0].r2)    
    bs_max.set_xlabel('BS Max')
    ## SS Median
    ss_median=T_SSC_rating(SSC,df['Turb_SS_Median'],location=SSC_loc,T_interval='15Min',Intercept=False,log=False)
    ss_med.scatter(ss_median[1]['T-NTU'],ss_median[1]['SSC (mg/L)'],c='k')
    ss_med.plot(xy,xy*ss_median[0].beta[0],ls='-',c='k',label='SS_Median'+r'$r^2$'+"%.2f"%ss_median[0].r2)
    #ss_med.set_title('SS_Median '+r'$r^2=$'+"%.2f"%ss_median[0].r2)
    ss_med.set_ylabel('SSC (mg/L)'),ss_med.set_xlabel('SS Median')
    ## SS Mean
    ss_mean=T_SSC_rating(SSC,df['Turb_SS_Mean'],location=SSC_loc,T_interval='15Min',Intercept=False,log=False)
    ss_mea.scatter(ss_mean[1]['T-NTU'],ss_mean[1]['SSC (mg/L)'],c='k')
    ss_mea.plot(xy,xy*ss_mean[0].beta[0],ls='-',c='k',label='SS_Mean'+r'$r^2$'+"%.2f"%ss_mean[0].r2)
    #ss_mea.set_title('SS_Mean '+r'$r^2=$'+"%.2f"%ss_mean[0].r2)    
    ss_mea.set_xlabel('SS Mean')
    ## SS Min
    ss_minimum=T_SSC_rating(SSC,df['Turb_SS_Min'],location=SSC_loc,T_interval='15Min',Intercept=False,log=False)
    ss_min.scatter(ss_minimum[1]['T-NTU'],ss_minimum[1]['SSC (mg/L)'],c='k')
    ss_min.plot(xy,xy*ss_minimum[0].beta[0],ls='-',c='k',label='SS_Min'+r'$r^2$'+"%.2f"%ss_minimum[0].r2)
    #ss_min.set_title('SS_Min '+r'$r^2=$'+"%.2f"%ss_minimum[0].r2)    
    ss_min.set_xlabel('SS Min')
    ## SS Max
    ss_maximum=T_SSC_rating(SSC,df['Turb_SS_Max'],location=SSC_loc,T_interval='15Min',Intercept=False,log=False)
    ss_max.scatter(ss_maximum[1]['T-NTU'],ss_maximum[1]['SSC (mg/L)'],c='k')
    ss_max.plot(xy,xy*ss_maximum[0].beta[0],ls='-',c='k',label='SS_Max'+r'$r^2$'+"%.2f"%ss_maximum[0].r2)    
    #ss_max.set_title('SS_Max '+r'$r^2=$'+"%.2f"%ss_maximum[0].r2)
    ss_max.set_xlabel('SS Max')
    
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
## Turbidity-ALL SSC rating
#OBSb_compare_ratings(df=LBJ_OBSb,SSC_loc='LBJ',Use_All_SSC=True,storm_samples_only=False,show=True,save=False,filename='') 
## Turbidity-ALL storm SSC
#OBSb_compare_ratings(df=LBJ_OBSb,SSC_loc='LBJ',Use_All_SSC=True,storm_samples_only=True,show=True,save=False,filename='') 

## Turbidity-Pre-mitigation SSC rating
#OBSb_compare_ratings(df=LBJ_OBSb,SSC_loc='LBJ',Use_All_SSC=False,storm_samples_only=False,show=True,save=False,filename='') 
## Turbidity-Pre-mitigation storm SSC
#OBSb_compare_ratings(df=LBJ_OBSb,SSC_loc='LBJ',Use_All_SSC=False,storm_samples_only=True,show=True,save=False,filename='')

## LBJ R2 Turbidity-ALL SSC rating
#OBSb_compare_ratings(df=LBJ_OBSb,SSC_loc='LBJ R2',Use_All_SSC=True,storm_samples_only=False)  

## QUARRY Turbidity-ALL SSC rating
#OBSb_compare_ratings(df=QUARRY_OBS,SSC_loc='R2',Use_All_SSC=True)   

    

### Choose OBS parameters based on above relationships (which is the best one?)
LBJ_OBSa['NTU']=LBJ_OBSa['Turb_SS_Avg']
## choose which OBS parameter == NTU (SOME EVIDENCE MAYBE THE MEDIAN OR MIN IS BETTER)
LBJ_OBSb['NTU']=LBJ_OBSb['Turb_SS_Mean'] 

LBJ_OBS=LBJ_OBSa.append(LBJ_OBSb) ## append NTU's
LBJ_OBS['NTU'] = LBJ_OBS['NTU'].interpolate(limit=2)

##NTU to SSC rating curve from LAB ANALYSIS
#T_SSC_Lab= pd.ols(y=SSC[SSC['Location']=='LBJ']['SSC (mg/L)'],x=SSC[SSC['Location']=='LBJ']['NTU'])
T_SSC_Lab= pd.ols(y=SSC['SSC (mg/L)'],x=SSC['NTU'],intercept=False)

### RMSE for T-SSC ratings
def calc_RMSE(T_SSC): ## uses the T_SSC_rating object
    print 'Manually calculating RMSE'
    ## Make DataFrame of measured NTU and SSC
    T_SSC_RMSE = pd.DataFrame({'NTU_measured':T_SSC[1]['T-NTU'],'SSC_measured':T_SSC[1]['SSC (mg/L)']})
    ## USe the rating slope to calculate SSC from the NTU value
    rating_slope = T_SSC[0].beta[0]
    T_SSC_RMSE['SSC_predicted']= T_SSC_RMSE['NTU_measured'] * rating_slope # + T_SSC[0].beta[1] # no intercept, no beta[1]
    ## Subtract the predicted from the actual (residuals)
    T_SSC_RMSE['SSC_diff'] = T_SSC_RMSE['SSC_measured'] - T_SSC_RMSE['SSC_predicted'] 
    ## Square the difference (residuals)
    T_SSC_RMSE['SSC_diff_squared'] = (T_SSC_RMSE['SSC_diff'])**2.
    ## Take square root of average of residuals 
    T_SSC_RMSE_Value = (T_SSC_RMSE['SSC_diff_squared'].sum()/len(T_SSC_RMSE))**0.5 
    ## Calculate RMSE as a percent
    T_SSC_RMSE_Percent = (T_SSC_RMSE_Value / T_SSC_RMSE['SSC_measured'].mean())  *100.
    return "%.1f"%T_SSC_RMSE_Value, "%.1f"%T_SSC_RMSE_Percent

## DAM TS3K
T_SSC_DAM_TS3K=T_SSC_rating(SSC_dict['Pre-storm'],DAM_TS3K['NTU'],location='DAM',T_interval='15Min',log=False) ## Use 5minute data for NTU/SSC relationship
DAM_TS3K_rating = T_SSC_DAM_TS3K[0]
DAM_TS3K_rating_rmse = T_SSC_DAM_TS3K[2] ## This RMSE is the raw value, NOT percent
DAM_TS3K['T-SSC-RMSE'] = DAM_TS3K_rating_rmse 
print "%.1f"%DAM_TS3K_rating.rmse, "%.1f"%DAM_TS3K_rating_rmse 
print calc_RMSE(T_SSC_DAM_TS3K)

## DAM YSI
T_SSC_DAM_YSI = T_SSC_rating(SSC_dict['Pre-storm'],DAM_YSI['NTU'],location='DAM',T_interval='5Min',log=False) ## Won't work until there are some overlapping grab samples
#T_SSC_DAM_YSI = T_SSC_LBJ_YSI 
DAM_YSI_rating= T_SSC_DAM_YSI[0]
DAM_YSI_rating_rmse= T_SSC_DAM_YSI[2]
DAM_YSI['T-SSC-RMSE']= DAM_YSI_rating_rmse
print "%.1f"%DAM_YSI_rating.rmse, "%.1f"%DAM_YSI_rating_rmse
print calc_RMSE(T_SSC_DAM_YSI)

## QUARRY
T_SSC_QUARRY_OBS = T_SSC_rating(SSC_dict['ALL'],QUARRY_OBS['NTU'],location='R2',T_interval='15Min',log=False)
QUARRY_OBS_rating = T_SSC_QUARRY_OBS[0]
QUARRY_OBS_rating_rmse = T_SSC_QUARRY_OBS[2]
QUARRY_OBS['T-SSC-RMSE'] = QUARRY_OBS_rating_rmse
print "%.1f"%QUARRY_OBS_rating.rmse, "%.1f"%QUARRY_OBS_rating_rmse
print calc_RMSE(T_SSC_QUARRY_OBS)

## LBJ YSI
T_SSC_LBJ_YSI = T_SSC_rating(SSC_dict['Pre-storm'],LBJ_YSI['NTU'],location='LBJ',T_interval='15Min',log=False)
LBJ_YSI_rating = T_SSC_LBJ_YSI[0]
LBJ_YSI_rating_rmse = T_SSC_LBJ_YSI[2]
LBJ_YSI['T-SSC-RMSE'] = LBJ_YSI_rating_rmse 
print "%.1f"%LBJ_YSI_rating.rmse, "%.1f"%LBJ_YSI_rating_rmse
print calc_RMSE(T_SSC_LBJ_YSI)

## LBJ OBS 2013
T_SSC_LBJ_OBSa = T_SSC_rating(SSC_dict['Pre-storm'],LBJ_OBSa['NTU'],location='LBJ',T_interval='5Min',log=False)
LBJ_OBSa_rating = T_SSC_LBJ_OBSa[0]
LBJ_OBSa_rating_rmse = T_SSC_LBJ_OBSa[2]
LBJ_OBSa['T-SSC-RMSE'] = LBJ_OBSa_rating_rmse 
print "%.1f"%LBJ_OBSa_rating.rmse, "%.1f"%LBJ_OBSa_rating_rmse
print calc_RMSE(T_SSC_LBJ_OBSa)

## LBJ OBS 2014
T_SSC_LBJ_OBSb=T_SSC_rating(SSC_dict['Pre-storm'],LBJ_OBSb['NTU'],location='LBJ',T_interval='15Min',log=False)
LBJ_OBSb_rating = T_SSC_LBJ_OBSb[0]
LBJ_OBSb_rating_rmse = T_SSC_LBJ_OBSb[2]
LBJ_OBSb['T-SSC-RMSE']= LBJ_OBSb_rating_rmse 
print "%.1f"%LBJ_OBSb_rating.rmse, "%.1f"%LBJ_OBSb_rating_rmse 
print calc_RMSE(T_SSC_LBJ_OBSb)

## LBJ OBS ALL
T_SSC_LBJ_OBS=T_SSC_rating(SSC_dict['Pre-storm'],LBJ_OBS['NTU'],location='LBJ',T_interval='15Min',log=False)
LBJ_OBS_rating = T_SSC_LBJ_OBS[0]
LBJ_OBS_rating_rmse = T_SSC_LBJ_OBS[2]
LBJ_OBS['T-SSC-RMSE'] = LBJ_OBS_rating_rmse 
print "%.1f"%LBJ_OBS_rating.rmse, "%.1f"%LBJ_OBS_rating_rmse 
print calc_RMSE(T_SSC_LBJ_OBS)

## Overall RMSE for LBJ-YSI rating and all DAM and LBJ samples
## make DataFrame of all measured NTU and SSC at LBJ and DAM
#T_SSC_NTU = pd.concat([T_SSC_LBJ_YSI[1]['LBJ-YSI-NTU'],T_SSC_DAM_TS3K[1]['DAM-TS3K-NTU'],T_SSC_DAM_YSI[1]['DAM-YSI-NTU']])
#T_SSC_SSC= pd.concat([T_SSC_LBJ_YSI[1]['SSC (mg/L)'],T_SSC_DAM_TS3K[1]['SSC (mg/L)'],T_SSC_DAM_YSI[1]['SSC (mg/L)']])
#T_SSC_ALL_NTU_RMSE = pd.DataFrame({'NTUmeasured':T_SSC_NTU,'SSCmeasured':T_SSC_SSC})

def plot_all_T_SSC_ratings(Use_All_SSC=False,storm_samples_only=False,log=False,show=True,save=False,filename='',sub_plot_count=0):
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
    fig, (ysi,obs) = plt.subplots(1,2,sharex=True, sharey=True, figsize=(6.5,3.25))#,sharex=True,sharey=True)
            
    max_y, max_x = 3800, 3800
    xy = np.linspace(1,max_y)
    
    ## LBJ and DAM YSI
    ## LBJ
    lbj = T_SSC_LBJ_YSI
    ysi.plot(lbj[1]['T-NTU'],lbj[1]['SSC (mg/L)'],ls='none',marker='o',fillstyle='none',markersize=4,c='k',label='FG3')
    ysi.plot(xy,xy*lbj[0].beta[0],ls='-',c='k',label='YSI_FG3 '+r'$r^2$'+"%.2f"%lbj[0].r2)
    ## DAM
    dam = T_SSC_DAM_YSI
    ysi.plot(dam[1]['T-NTU'],dam[1]['SSC (mg/L)'],ls='none',marker='o',markersize=4,c='grey',label='FG1')
    ysi.plot(xy,xy*dam[0].beta[0],ls='--',c='grey',label='YSI_FG1 '+r'$r^2$'+"%.2f"%dam[0].r2)
    ysi.set_xlabel('Turb. (NTU)')
    ysi.set_ylabel('SSC (mg/L)')
    ysi.legend(ncol=1,fontsize=8,columnspacing=0.1,loc='lower right')
    ## LBJ OBSa
    ## SS Avg
    ss_average = T_SSC_LBJ_OBSa
    obs.plot(xy,xy*ss_average[0].beta[0],ls='-',c='k',label='OBSa '+r'$r^2$'+"%.2f"%ss_average[0].r2)  
    obs.plot(ss_average[1]['T-NTU'],ss_average[1]['SSC (mg/L)'],c='k',label='FG3 OBSa',ls='none',marker='o',markersize=4)
    
    ## LBJ OBSb
    ## SS Mean
    ss_mean=T_SSC_LBJ_OBSb
    obs.plot(xy,xy*ss_mean[0].beta[0],ls='-',c='grey',label='OBSb '+r'$r^2$'+"%.2f"%ss_mean[0].r2) 
    obs.plot(ss_mean[1]['T-NTU'],ss_mean[1]['SSC (mg/L)'],c='k',marker='o',ls='none',fillstyle='none',markersize=4,label='FG3 OBSb')
    
    
    obs.set_xlabel('Turb. (SS)')
    obs.yaxis.tick_right()
    obs.legend(ncol=1,fontsize=8,columnspacing=0.1,loc='lower right')
    
    for ax in fig.axes:
        if log==False:
            ax.locator_params(nbins=4,axis='y'), ax.locator_params(nbins=4,axis='x')
            ax.set_xlim(0,max_x), ax.set_ylim(0,max_y)
        if log==True:
            ax.set_xscale('log'), ax.set_yscale('log')
            ax.set_xlim(0,5000), ax.set_ylim(0,5000)
        
    letter_subplots(fig,x=0.1,y=0.95,vertical='top',horizontal='right',Color='k',font_size=10,font_weight='bold')
    plt.tight_layout(pad=0.1)
        
    show_plot(show)
    savefig(save,filename)
    return
#plot_all_T_SSC_ratings(Use_All_SSC=False,storm_samples_only=True,log=True,show=True,save=False,filename='',sub_plot_count=0)
plot_all_T_SSC_ratings(Use_All_SSC=True,storm_samples_only=False,log=False,show=True,save=False,filename='',sub_plot_count=0)




def NTUratingstable_html(caption,table_num,filename,save=False,show=False):
    
    df = pd.DataFrame(columns = ['b','r2','pearson','spearman','rmse'])

    ## Lab
    LAB = linearfunction(SSC[SSC['Location']=='LBJ']['NTU'],SSC[SSC['Location']=='LBJ']['SSC (mg/L)'])
    LAB_df = pd.DataFrame({'b':'%.2f'%LAB['b'],'r2':'%.2f'%LAB['r2'],'pearson':'%.2f'%LAB['pearson'],
                                 'spearman':'%.2f'%LAB['spearman'],'rmse':'%.2f'%LAB['rmse']},index=['Lab'])
    df = df.append(LAB_df)
    ## LBJ YSI
    LBJ_YSI = linearfunction(T_SSC_LBJ_YSI[1]['T-NTU'],T_SSC_LBJ_YSI[1]['SSC (mg/L)'])
    LBJ_YSI_df = pd.DataFrame({'b':'%.2f'%LBJ_YSI['b'],'r2':'%.2f'%LBJ_YSI['r2'],'pearson':'%.2f'%LBJ_YSI['pearson'],
                                 'spearman':'%.2f'%LBJ_YSI['spearman'],'rmse':'%.2f'%LBJ_YSI['rmse']},index=['LBJ_YSI'])
    df = df.append(LBJ_YSI_df)
    ## DAM TS3000
    DAM_TS3K = linearfunction(T_SSC_DAM_TS3K[1]['T-NTU'],T_SSC_DAM_TS3K[1]['SSC (mg/L)'])
    DAM_TS3K_df = pd.DataFrame({'b':'%.2f'%DAM_TS3K['b'],'r2':'%.2f'%DAM_TS3K['r2'],'pearson':'%.2f'%DAM_TS3K['pearson'],
                                 'spearman':'%.2f'%DAM_TS3K['spearman'],'rmse':'%.2f'%DAM_TS3K['rmse']},index=['DAM_TS3K'])
    df = df.append(DAM_TS3K_df)
    ## DAM YSI
    DAM_YSI = linearfunction(T_SSC_DAM_YSI[1]['T-NTU'],T_SSC_DAM_YSI[1]['SSC (mg/L)'])
    DAM_YSI_df = pd.DataFrame({'b':'%.2f'%DAM_YSI['b'],'r2':'%.2f'%DAM_YSI['r2'],'pearson':'%.2f'%DAM_YSI['pearson'],
                                 'spearman':'%.2f'%DAM_YSI['spearman'],'rmse':'%.2f'%DAM_YSI['rmse']},index=['DAM_YSI'])
    df = df.append(DAM_YSI_df)
    ## LBJ OBSa 2013
    LBJ_OBS_2013 = linearfunction(T_SSC_LBJ_OBSa[1]['T-NTU'],T_SSC_LBJ_OBSa[1]['SSC (mg/L)'])
    LBJ_OBS_2013_df = pd.DataFrame({'b':'%.2f'%LBJ_OBS_2013['b'],'r2':'%.2f'%LBJ_OBS_2013['r2'],'pearson':'%.2f'%LBJ_OBS_2013['pearson'],
                                 'spearman':'%.2f'%LBJ_OBS_2013['spearman'],'rmse':'%.2f'%LBJ_OBS_2013['rmse']},index=['LBJ_OBS_2013'])
    df = df.append(LBJ_OBS_2013_df)  
    ## LBJ OBSb 2014
    LBJ_OBS_2014 = linearfunction(T_SSC_LBJ_OBSb[1]['T-NTU'],T_SSC_LBJ_OBSb[1]['SSC (mg/L)'])
    LBJ_OBS_2014_df = pd.DataFrame({'b':'%.2f'%LBJ_OBS_2014['b'],'r2':'%.2f'%LBJ_OBS_2014['r2'],'pearson':'%.2f'%LBJ_OBS_2014['pearson'],
                                 'spearman':'%.2f'%LBJ_OBS_2014['spearman'],'rmse':'%.2f'%LBJ_OBS_2014['rmse']},index=['LBJ_OBS_2014'])
    df = df.append(LBJ_OBS_2014_df)   
    ## QUARRY OBS
    QUARRY_OBS = linearfunction(T_SSC_QUARRY_OBS[1]['T-NTU'],T_SSC_QUARRY_OBS[1]['SSC (mg/L)'])
    QUARRY_OBS_df = pd.DataFrame({'b':'%.2f'%QUARRY_OBS['b'],'r2':'%.2f'%QUARRY_OBS['r2'],'pearson':'%.2f'%QUARRY_OBS['pearson'],
                                 'spearman':'%.2f'%QUARRY_OBS['spearman'],'rmse':'%.2f'%QUARRY_OBS['rmse']},index=['QUARRY_OBS'])
    df = df.append(QUARRY_OBS_df)    
    
    ## Write table to html
    table_to_html_R(df, caption, table_num, filename, save=True, show=True)
    return
#NTUratingstable_html(caption='T-SSC relationship parameters', table_num='1', filename=datadir+'htmltabletest.html', show=True,save=False)
    
## Old test code:
#table_to_html_R(df, caption='Rating parameters', table_num='1', filename=datadir+'htmltabletest.html', save=True, show=True)
    




