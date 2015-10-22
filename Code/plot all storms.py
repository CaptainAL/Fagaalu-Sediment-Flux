# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 13:44:07 2015

@author: Alex
"""

## Plot all storms individuall
## should just make a loop to plot all of them right?

def plot_storm_data_individually(storm_threshold,storm_intervals,show=False,save=True):
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
#plot_all_storms_individually(All_Storms,show=True,save=False) # for individual storm pd.DataFrame(Intervals.loc[index#]).T 
