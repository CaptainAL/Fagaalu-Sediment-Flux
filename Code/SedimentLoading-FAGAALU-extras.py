# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 11:09:32 2014

@author: Alex
"""

def plot_AirportWind(show=False):
    fig, (speed,direction) = plt.subplots(2,1,sharex=True)
    
    airport['Wind Speed m/s'].dropna().plot(ax=speed)
    airport['WindDirDegrees'].dropna().plot(ax=direction)
    
    speed.set_ylim(0,25)
    plt.suptitle('Wind speed and direction at TAFUNA INTL Airport')
    plt.draw()
    if show==True:
        plt.show()
    return
#plot_AirportWind(True)  ## No Data for Drifter Week  

def plotSTAGE(show=False):
    fig, stage = plt.subplots(1)
    title="Stage for PT's in Fagaalu Stream"
    #### PT1 stage LBJ
    stage.plot_date(PT1['stage'].index,PT1['stage'],marker='None',ls='-',color='r',label='LBJ')
    print 'Lowest PT1 stage: '+str(PT1['stage'].min())
    #### PT2 stage DT
    stage.plot_date(PT2['stage'].index,PT2['stage'],marker='None',ls='-',color='y',label='DT')
    #### PT3 stage Dam
    stage.plot_date(PT3['stage'].index,PT3['stage'],marker='None',ls='-',color='g',label='DAM')
    LBJfieldnotesStage['Stage (cm)'].plot(ax=stage,marker='o',ls='None',color='r',label='LBJ Field Notes')
    ## show storm intervals?
    showstormintervals(stage,shade_color='g',show=True)
    
    #### Format X axis and Primary Y axis
    stage.set_title(title)
    stage.set_ylabel('Gage height (cm)')
    stage.set_ylim(0,145)
    stage.legend(loc=2)
    #### Add Precip data from Timu1
    AddTimu1(fig,stage,Precip['Timu1-15'])
    
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
    Precip['FPhourly'].dropna().plot(label='Precip Hourly (Wx Station)',color='b',linestyle='steps-mid')
    Precip['FPdaily'].dropna().plot(label='Precip Daily (Wx Station)',color='c',linestyle='steps-post')
    Precip['Timu1hourly'].dropna().plot(label='Precip Hourly',color='y',linestyle='steps-mid')
    Precip['Timu1daily'].dropna().plot(label='Precip Daily',color='g',linestyle='steps-post')
    #PrecipMonthly = Timu1monthly.plot(label='Precip Monthly',color='k',linestyle='steps-post')    
    plt.axes().xaxis_date()
    plt.setp(plt.axes().get_xticklabels(), rotation=45, fontsize=9)
    plt.ylabel('Precipitation (mm)')
    fig.canvas.manager.set_window_title('Figure 2: Precipitation(mm)') 
    plt.legend(),plt.grid(True)
    if show==True:
        plt.show()
    return
#plotPRECIP(True)
    
def plotPrecipIntervals(fig,ax,start,stop):
    Precip['FPhourly'][start:stop].dropna().plot(ax=ax,label='Precip Hourly (Wx Station)',color='b',linestyle='steps-mid')
    Precip['Timu1hourly'][start:stop].dropna().plot(ax=ax,label='Precip Hourly',color='y',linestyle='steps-mid')
    showstormintervals(ax,show=True)
    ax.set_ylim(0,60)
    return

def plotPrecipYears(show=False):
    fig, (precip2012,precip2013,precip2014) = plt.subplots(3)
    title="Precipitation in Faga'alu"
    plotPrecipIntervals(fig,precip2012,start2012,stop2012)
    plotPrecipIntervals(fig,precip2013,start2013,stop2013)    
    plotPrecipIntervals(fig,precip2014,start2014,stop2014)    
    
    precip2012.set_title(title)
    precip2014.legend()
    plt.tight_layout()
    if show==True:
        plt.show()
    return
#plotPrecipYears(True)
    
def ALL_Q(show=False): ## Discharge
    plt.ion()
    fig, (site_lbj,site_dam) = plt.subplots(2,sharex=True)
    title = 'Discharge L/Sec from Rating Curves'
    
    LBJ['Q-AV'].plot(ax=site_lbj,c='r',marker='None',ls='-',label='LBJ-AV')

    LBJ['Q-AVLog'].plot(ax=site_lbj,c='r',ls='--',label='LBJ-AVLog')
    LBJ['Q-AManningV'].plot(ax=site_lbj,c='g',ls='-',label='LBJ-AManningV')
    LBJ['Q-AManningVLog'].plot(ax=site_lbj,c='g',ls='--',label='LBJ-AManningVLog')
    
    DAM['Q-AV'].plot(ax=site_dam,c='r',ls='-',label='DAM-AV')
    DAM['Q-AVLog'].plot(ax=site_dam,c='r',ls='--',label='DAM-AVLog')
    DAM['Q-HEC'].plot(ax=site_dam,c='g',ls='-',label='DAM-HEC')
    DAM['Q-D_Flume'].plot(ax=site_dam,c='g',ls='--',label='DAM-WinFlume')
    
    site_lbj.grid(True),site_dam.grid(True)
    site_lbj.legend(),site_dam.legend()
    plt.suptitle(title)
    plt.draw()
    if show==True:
        plt.show()
    return
#ALL_Q(True)
    
def Q_Analysis(show=False, log=False,):
    fig, (Q,stage) = plt.subplots(2,sharex=True)
    title = 'Discharge L/Sec from Rating Curves'
    
    ## Plot Q from the rating curve selected above
    LBJ['Q'].plot(ax=Q,c='r',label='LBJ Q (L/sec)')
    DAM['Q'].plot(ax=Q,c='g',ls='-',label='DAM Q (L/sec)')
    ## Plot Stage    
    LBJ['stage'].plot(ax=stage,c='r',ls='-',label='LBJ Stage(cm)')
    DAM['stage'].plot(ax=stage,c='g',ls='-',label='DAM Stage(cm)')
    
    showstormintervals(Q,storm_threshold=LBJ_storm_threshold,showStorms=LBJ_StormIntervals,shade_color='g',show=True)
    showstormintervals(stage,storm_threshold=LBJ_storm_threshold,showStorms=LBJ_StormIntervals,shade_color='g',show=True)
    
    Q.grid(True),stage.grid(True)
    Q.legend(),stage.legend()
    stage.set_ylim(0,100)
    plt.suptitle(title)
    
    logaxes(log,fig)
    for ax in fig.axes:
        ax.autoscale_view(True,True,True)    
    
    plt.draw()
    if show==True:
        plt.show()
    return
#Q_Analysis(show=True,log=False)

#    LBJfieldnotesStage['Stage (cm)']=LBJfieldnotesStage['Stage (cm)']-LBJfieldnotesStage['SG-PT'].mean() ## correct for staff gage offset   
def plotStageIntervals(fig,ax,start,stop):
    ## This is for the StageYears plot below
    #### PT1 stage LBJ
    ax.plot_date(PT1['stage'][start:stop].index,PT1['stage'][start:stop],marker='None',ls='-',color='r',label='LBJ')
    print 'Lowest PT1 stage: '+str(PT1['stage'].min())
    #### PT2 stage DT
    ax.plot_date(PT2['stage'][start:stop].index,PT2['stage'][start:stop],marker='None',ls='-',color='y',label='DT')
    #### PT3 stage Dam
    ax.plot_date(PT3['stage'][start:stop].index,PT3['stage'][start:stop],marker='None',ls='-',color='g',label='Dam')
    #### LBJ field notes for verification
    #ax.plot_date(LBJfieldnotesStage['Stage (cm)'][start:stop].index,LBJfieldnotesStage['Stage (cm)'][start:stop],marker='o',ls='None',color='r',label='LBJ Field Notes')
    ## show storm intervals?

    #showstormintervals(ax,storm_threshold=DAM_storm_threshold,showStorms=DAM_StormIntervals,shade_color='g',show=True)
    #showstormintervals(ax,storm_threshold=LBJ_storm_threshold,showStorms=LBJ_StormIntervals,shade_color='grey',show=True)
    
    #AddTimu1(fig,ax,Precip['Timu1-15'])
    #AddTimu1(fig,ax,Precip['FPrain'])
    
    ax.set_ylim(0,110)
    ax.set_xlim(start,stop)
    ax.set_ylabel('Stage (cm)')
    return
    
def plotStageYears(show=False):
    fig, (stage2012, stage2013, stage2014) = plt.subplots(3)
    title="Stage for PT's in Fagaalu Stream"
    #### PT1 stage LBJ
    plotStageIntervals(fig,stage2012,start2012,stop2012)
    stage2012.plot(DAMstageDischarge['stage(cm)'],'.')
    #### PT2 stage DT
    plotStageIntervals(fig,stage2013,start2013,stop2013)    
    #### PT3 stage Dam    
    plotStageIntervals(fig,stage2014,start2014,stop2014)    

    plt.subplots_adjust(left=0.1,right=0.83,top=0.93,bottom=0.15)
    #### Legend
    #LegendWithPrecip(stage2012)
    fig.canvas.manager.set_window_title('Figure 1: '+title) 
    stage2012.set_title(title)
    stage2014.legend()
    plt.tight_layout()
    plt.draw()
    if show==True:
        plt.show()
    return
plotStageYears(True)

def plotdischargeintervals(fig,ax,start,stop):
    LBJ['Q'][start:stop].dropna().plot(ax=ax,c='r',label='LBJ (Q-AV PowerLaw)')
    ax.plot(LBJstageDischarge.index,LBJstageDischarge['Q-AV(L/sec)'],ls='None',marker='o',color='r')
    DAM['Q'][start:stop].dropna().plot(ax=ax,c='g',ls='-',label='DAM (Q-Mannings)')
    ax.plot(DAMstageDischarge.index,DAMstageDischarge['Q-AV(L/sec)'],ls='None',marker='o',color='g')
    
    #AddTimu1(fig,ax,Precip['Timu1-15'][start:stop]) 
    showstormintervals(ax,storm_threshold=LBJ_storm_threshold,StormsList=LBJ_StormIntervals,show=True)
    ax.set_ylim(0,2600)
    return
    
def QYears(show=False):
    mpl.rc('lines',markersize=8)
    fig, (Q2012,Q2013,Q2014)=plt.subplots(3)
    plotdischargeintervals(fig,Q2012,start2012,stop2012)
    plotdischargeintervals(fig,Q2013,start2013,stop2013)
    plotdischargeintervals(fig,Q2014,start2014,stop2014)
    
    Q2014.legend()
    Q2013.set_ylabel('Discharge (Q) L/sec')
    Q2012.set_title("Discharge (Q) L/sec at the Upstream and Downstream Sites, Faga'alu")
    plt.draw()
    if show==True:
        plt.show()
    return
QYears(True)

#P_Q.scatter(PQdaily['Timu1daily'],PQdaily['Qdaily'],marker='o',s=dotsize,color='r')
def PQ(show=False): ## "Event Rainfall(mm) vs. Event Discharge (L) Fagaalu Stream"
    fig,P_Q = plt.subplots(1)    
    dotsize=20
    ### LBJ
    P_Q.scatter(StormsLBJ['Psum'],StormsLBJ['Qsum'],color='r',marker='o',s=scaleSeries(StormsLBJ['Pmax'].dropna().values),edgecolors='grey')
    Polyfit(StormsLBJ['Psum'],StormsLBJ['Qsum'],1,'r','Rainfall-Runoff-LBJ',100,P_Q)
    ### DAM
    P_Q.scatter(StormsDAM['Psum'],StormsDAM['Qsum'],color='g',marker='o',s=scaleSeries(StormsDAM['Pmax'].dropna().values),edgecolors='grey')
    Polyfit(StormsDAM['Psum'],StormsDAM['Qsum'],1,'g','Rainfall-Runoff-DAM',100,P_Q) ### Won't work if na values in np.array->polyfit
    ### Label on click
    labelindex(StormsLBJ.index,StormsLBJ['Psum'],StormsLBJ['Qsum'])
    labelindex(StormsDAM.index,StormsDAM['Psum'],StormsDAM['Qsum'])
    
    title="Event Rainfall(mm) vs. Event Discharge (L) Fagaalu Stream"
    P_Q.set_title(title)
    P_Q.set_ylabel('Event Discharge (L)'),P_Q.set_xlabel('Event Precipitation (mm)-DotSize = Max 15min. Precip')
    P_Q.set_ylim(0,StormsLBJ['Qsum'].max()+50000000), P_Q.set_xlim(0,250)
    fig.canvas.manager.set_window_title('Figure: '+title)
    P_Q.grid(True), P_Q.legend(loc=4)
    
    log=False
    if log==True:
        P_Q.set_yscale('log'), P_Q.set_xscale('log')

    plt.draw()
    if show==True:
        plt.show()
    return
#PQ(True)

def PQyears_LBJ(show=False):
    fig, site_lbj=plt.subplots(1)
    
    site_lbj.scatter(StormsLBJ['Psum'][start2012:stop2012],StormsLBJ['Qsum'][start2012:stop2012],color='g',marker='o',s=scaleSeries(StormsLBJ['Pmax'][start2012:stop2012].dropna().values),label='2012')
    site_lbj.scatter(StormsLBJ['Psum'][start2013:stop2013],StormsLBJ['Qsum'][start2013:stop2013],color='y',marker='o',s=scaleSeries(StormsLBJ['Pmax'][start2013:stop2013].dropna().values),label='2013')
    site_lbj.scatter(StormsLBJ['Psum'][start2014:stop2014],StormsLBJ['Qsum'][start2014:stop2014],color='r',marker='o',s=scaleSeries(StormsLBJ['Pmax'][start2014:stop2014].dropna().values),label='2014')

    ### Label on click
    labelindex(StormsLBJ.index,StormsLBJ['Psum'],StormsLBJ['Qsum'])
        
    title="Event Rainfall(mm) vs. Event Discharge (L) Fagaalu Stream"
    fig.suptitle(title)
    site_lbj.set_title('LBJ')
    site_lbj.set_ylabel('Discharge (L)'),site_lbj.set_xlabel('Precipitation (mm) - DotSize=15minMaxPrecip(mm)')
    site_lbj.set_ylim(0,StormsLBJ['Qsum'].max()+50000000), site_lbj.set_xlim(0,250)
    fig.canvas.manager.set_window_title('Figure: '+title)
    site_lbj.legend()
    site_lbj.grid(True)
    plt.draw()
    if show==True:
        plt.show()
    return
#PQyears_LBJ(True)

def PQyears_DAM(show=False):
    fig, site_dam=plt.subplots(1)
    dotsize=20
    site_dam.scatter(StormsDAM['Psum'][start2012:stop2012],StormsDAM['Qsum'][start2012:stop2012],color='g',marker='o',s=scaleSeries(StormsDAM['Pmax'].dropna()[start2012:stop2012].values),label='2012')
    site_dam.scatter(StormsDAM['Psum'][start2013:stop2013],StormsDAM['Qsum'][start2013:stop2013],color='y',marker='o',s=scaleSeries(StormsDAM['Pmax'].dropna()[start2013:stop2013].values),label='2013')
    site_dam.scatter(StormsDAM['Psum'][start2014:stop2014],StormsDAM['Qsum'][start2014:stop2014],color='r',marker='o',s=scaleSeries(StormsDAM['Pmax'].dropna()[start2014:stop2014].values),label='2014')

    ### Label on click
    labelindex(StormsDAM.index,StormsDAM['Psum'],StormsDAM['Qsum'])
    
    title="Event Rainfall(mm) vs. Event Discharge (L) Fagaalu Stream"
    fig.suptitle(title)
    site_dam.set_title('DAM')
    site_dam.set_ylabel('Discharge (L)'),site_dam.set_xlabel('Precipitation (mm) - DotSize=15minMaxPrecip(mm)')
    site_dam.set_ylim(0,StormsLBJ['Qsum'].max()+50000000), site_dam.set_xlim(0,250)
    fig.canvas.manager.set_window_title('Figure: '+title)
    site_dam.legend()
    site_dam.grid(True)
    plt.draw()
    if show==True:
        plt.show()
    return
#PQyears_DAM(True)

def PQyears_BOTH(show=False):
    fig, (site_dam,site_lbj)=plt.subplots(1,2,sharey=True,sharex=True)
    dotsize=30
    site_lbj.scatter(StormsLBJ['Psum'][start2012:stop2012],StormsLBJ['Qsum'][start2012:stop2012]*.001,color='g',marker='o',s=scaleSeries(StormsLBJ['Pmax'][start2012:stop2012].dropna().values),label='2012')
    site_lbj.scatter(StormsLBJ['Psum'][start2013:stop2013],StormsLBJ['Qsum'][start2013:stop2013]*.001,color='y',marker='o',s=scaleSeries(StormsLBJ['Pmax'][start2013:stop2013].dropna().values),label='2013')
    site_lbj.scatter(StormsLBJ['Psum'][start2014:stop2014],StormsLBJ['Qsum'][start2014:stop2014]*.001,color='r',marker='o',s=scaleSeries(StormsLBJ['Pmax'][start2014:stop2014].dropna().values),label='2014')

    site_lbj.set_title('VILLAGE',fontsize=16)
    site_lbj.set_ylabel(r'$Event Discharge (m^3)$'),site_lbj.set_xlabel('Precipitation (mm) - DotSize=Intensity(mm/15min)')
    #site_lbj.set_ylim(0,StormsLBJ['Qsum'].max()+50000000), site_lbj.set_xlim(0,250)
    site_lbj.legend(loc=4)
    site_lbj.grid(True)

    site_dam.scatter(StormsDAM['Psum'][start2012:stop2012],StormsDAM['Qsum'][start2012:stop2012]*.001,color='g',marker='o',s=scaleSeries(StormsDAM['Pmax'].dropna()[start2012:stop2012].values),label='2012')
    site_dam.scatter(StormsDAM['Psum'][start2013:stop2013],StormsDAM['Qsum'][start2013:stop2013]*.001,color='y',marker='o',s=scaleSeries(StormsDAM['Pmax'].dropna()[start2013:stop2013].values),label='2013')
    site_dam.scatter(StormsDAM['Psum'][start2014:stop2014],StormsDAM['Qsum'][start2014:stop2014]*.001,color='r',marker='o',s=scaleSeries(StormsDAM['Pmax'].dropna()[start2014:stop2014].values),label='2014')
    
    site_dam.set_title('FOREST',fontsize=16)
    site_dam.set_ylabel(r'$Event Discharge (m^3)$'),site_dam.set_xlabel('Precipitation (mm) - DotSize=Intensity(mm/15min)')
    #site_dam.set_ylim(0,StormsLBJ['Qsum'].max()+50000000), site_dam.set_xlim(0,250)
    site_dam.legend(loc=4)
    site_dam.grid(True)
    
    ### Label on click
    labelindex(StormsLBJ.index,StormsLBJ['Psum'],StormsLBJ['Qsum'])
    labelindex(StormsDAM.index,StormsDAM['Psum'],StormsDAM['Qsum'])
    
    title="Event Rainfall vs. Event Discharge Fagaalu Stream"
    fig.suptitle(title,fontsize=16)
    fig.canvas.manager.set_window_title('Figure: '+title)
    
    
    log=False
    if log==True:
        site_lbj.set_yscale('log'), site_lbj.set_xscale('log')
        site_dam.set_yscale('log'), site_dam.set_xscale('log')
    plt.draw()
    if show==True:
        plt.show()
    return
#PQyears_BOTH(True)

def PQvol_years_BOTH(StormsLBJ,StormsDAM,show=False):
    fig, (site_lbj,site_dam)=plt.subplots(1,2,sharey=True,sharex=True)
    dotsize=20
    stormsLBJ=StormsLBJ[['PsumVol','Qsum']]/1000
    stormsLBJ['Pmax']=StormsLBJ[['Pmax']]
    site_lbj.scatter(stormsLBJ['PsumVol'][start2012:stop2012],stormsLBJ['Qsum'][start2012:stop2012],color='g',marker='o',s=scaleSeries(stormsLBJ['Pmax'][start2012:stop2012].dropna().values),label='2012')
    site_lbj.scatter(stormsLBJ['PsumVol'][start2013:stop2013],stormsLBJ['Qsum'][start2013:stop2013],color='y',marker='o',s=scaleSeries(stormsLBJ['Pmax'][start2013:stop2013].dropna().values),label='2013')
    site_lbj.scatter(stormsLBJ['PsumVol'][start2014:stop2014],stormsLBJ['Qsum'][start2014:stop2014],color='r',marker='o',s=scaleSeries(stormsLBJ['Pmax'][start2014:stop2014].dropna().values),label='2014')

    site_lbj.set_title('LBJ')
    site_lbj.set_ylabel('Event Discharge (m3)'),site_lbj.set_xlabel('Precipitation (m3) - DotSize=15minMaxPrecip(mm)')
    #site_lbj.set_ylim(0,stormsLBJ['Qsum'].max()+50000000), site_lbj.set_xlim(0,250)
    site_lbj.legend(loc=4)
    site_lbj.grid(True)

    stormsDAM=StormsDAM[['PsumVol','Qsum']]/1000
    stormsDAM['Pmax']=StormsDAM[['Pmax']]
    site_dam.scatter(stormsDAM['PsumVol'][start2012:stop2012],stormsDAM['Qsum'][start2012:stop2012],color='g',marker='o',s=scaleSeries(stormsDAM['Pmax'].dropna()[start2012:stop2012].values),label='2012')
    site_dam.scatter(stormsDAM['PsumVol'][start2013:stop2013],stormsDAM['Qsum'][start2013:stop2013],color='y',marker='o',s=scaleSeries(stormsDAM['Pmax'].dropna()[start2013:stop2013].values),label='2013')
    site_dam.scatter(stormsDAM['PsumVol'][start2014:stop2014],stormsDAM['Qsum'][start2014:stop2014],color='r',marker='o',s=scaleSeries(stormsDAM['Pmax'].dropna()[start2014:stop2014].values),label='2014')
    
    site_dam.set_title('DAM')
    site_dam.set_ylabel('Event Discharge (m3)'),site_dam.set_xlabel('Precipitation (m3) - DotSize=15minMaxPrecip(mm)')
    #site_dam.set_ylim(0,stormsLBJ['Qsum'].max()+50000000), site_dam.set_xlim(0,250)
    site_dam.legend(loc=4)
    site_dam.grid(True)
    
    ### Label on click
    labelindex_subplot(site_lbj,stormsLBJ.index,stormsLBJ['PsumVol'],stormsLBJ['Qsum'])
    labelindex_subplot(site_dam,stormsDAM.index,stormsDAM['PsumVol'],stormsDAM['Qsum'])
    
    title="Event Rainfall vs. Event Discharge Fagaalu Stream"
    fig.suptitle(title,fontsize=16)
    fig.canvas.manager.set_window_title('Figure: '+title)
    
    
    log=False
    if log==True:
        site_lbj.set_yscale('log'), site_lbj.set_xscale('log')
        site_dam.set_yscale('log'), site_dam.set_xscale('log')
    plt.draw()
    if show==True:
        plt.show()
    return
PQvol_years_BOTH(StormsLBJ,StormsDAM,True)
    
def plotNTU_LBJ(show=False,lwidth=0.5):
    fig, (precip, lbjQ, ntu) = plt.subplots(3,1,sharex=True)
    mpl.rc('lines',markersize=10,linewidth=lwidth)
    ##Precip
    precip.plot_date(PrecipFilled.index,PrecipFilled['Precip'],ls='steps-post',marker='None',c='b',label='Precip-Filled')
    ##LBJ Discharge
    lbjQ.plot_date(LBJ['Q'].index,LBJ['Q'],ls='-',marker='None',c='k',label='LBJ Q-AVLog')
    ##LBJ Turbidity
    ntu.plot_date(LBJntu15minute.index,LBJntu15minute,ls='-',marker='None',c='r',label='LBJ 15min NTU')
    ntu.plot_date(LBJ_OBS.index,LBJ_OBS['NTU'],marker='None',ls='-',c='y',label='LBJ OBS 5min NTU')
    ntu.plot_date(LBJ_YSI.index,LBJ_YSI['NTU'],marker='None',ls='-',c='g',label='LBJ YSI 5min NTU')
    ##plot all Grab samples at location    
    tss = fig.add_axes(ntu.get_position(), frameon=False, sharex=ntu,sharey=ntu)
    LBJtss = TSS[TSS['Location']=='LBJ']
    tss.plot_date(LBJtss.index,LBJtss['TSS (mg/L)'],'.',markeredgecolor='grey',c='y')    
    ##plot Grab samples used for rating
    tss.plot_date(NTU_TSSrating_LBJ_OBS[1].index,NTU_TSSrating_LBJ_OBS[1]['TSS (mg/L)'],'.',markeredgecolor='grey',c='r',label='LBJ TSS samples')
    tss.yaxis.set_ticks_position('right'), tss.yaxis.set_label_position('right')
    tss.set_ylabel('SSC (mg/L)')
    ## label with field notes
    NTU_TSSrating_LBJ_OBS[1]['fieldnotes'] = LBJfieldnotes['Condition']
    #annotate_plot(NTU_TSSrating_LBJ_OBS[1],'TSS (mg/L)','fieldnotes')
    ## Shade storm intervals
    showstormintervals(precip)
    showstormintervals(lbjQ)
    showstormintervals(ntu)

    precip.set_ylabel('Precip (mm/15min)')
    lbjQ.set_ylabel('Discharge (L/sec)')
    ntu.set_ylabel('Turbidity (NTU)'),
    ntu.set_ylim(0,LBJntu15minute['NTU'].max())
    ntu.legend()
    plt.suptitle('Precipitation, Discharge, Turbidity and SSC grab samples at LBJ')
    plt.draw()
    if show==True:
        plt.show()
    return
#plotNTU_LBJ(True)

def plotNTU_DAM(show=False,lwidth=0.5):
    fig, (precip, damQ, ntu) = plt.subplots(3,1,sharex=True)
    mpl.rc('lines',markersize=10,linewidth=lwidth)
    ##Precip
    precip.plot_date(PrecipFilled.index,PrecipFilled['Precip'],ls='steps-post',marker='None',c='b',label='Precip-Filled')
    ##DAM Discharge
    damQ.plot_date(DAM['Q'].index,DAM['Q'],ls='-',marker='None',c='k',label='DAM D_Flume')
    ##DAM Turbidity
    ntu.plot_date(DAMntu15minute.index,DAMntu15minute,ls='-',marker='None',c='r',label='DAM 15min NTU')
    ntu.plot_date(DAM_YSI.index,DAM_YSI['NTU'],ls='-',marker='None',c='y',label='DAM YSI 5min NTU')
    ntu.plot_date(DAM_TS3K.index,DAM_TS3K['NTU'],ls='-',marker='None',c='g',label='DAM TS3K 5min NTU')
    ##plot all Grab samples at location 
    tss = fig.add_axes(ntu.get_position(), frameon=False, sharex=ntu,sharey=ntu)
    DAMtss = TSS[TSS['Location']=='DAM']
    tss.plot_date(DAMtss.index,DAMtss['TSS (mg/L)'],'.',markeredgecolor='grey',c='y')    
    ##plot Grab samples used for rating
    tss.plot_date(NTU_TSSrating_DAM_TS3K[1].index,NTU_TSSrating_DAM_TS3K[1]['TSS (mg/L)'],'.',markeredgecolor='grey',c='r',label='DAM TSS samples')
    tss.yaxis.set_ticks_position('right')
    tss.yaxis.set_label_position('right')
    tss.set_ylabel('SSC (mg/L)')
    ## Shade storm intervals
    showstormintervals(precip)
    showstormintervals(damQ)
    showstormintervals(ntu)

    precip.set_ylabel('Precip (mm/15min)')
    damQ.set_ylabel('Discharge (L/sec)')
    ntu.set_ylabel('Turbidity (NTU)'),ntu.set_ylim(0,DAMntu15minute['NTU'].max())
    plt.suptitle('Precipitation, Discharge, Turbidity and SSC grab samples at DAM')
    ntu.legend()
    plt.draw()
    if show==True:
        plt.show()
    return
#plotNTU_DAM(True)       
    
def plotNTU_TSS_lab(show=True):
    title='NTU-SSC relationship from Lab Analysis with LaMotte 2020'
    fig, ALL = plt.subplots(1)
    xy = np.linspace(0,1500,1500)
    
    ALL.scatter(TSS[TSS['Location']=='DT']['NTU'],TSS[TSS['Location']=='DT']['TSS (mg/L)'],c='y',label='DT',s=50)
    ALL.scatter(TSS[TSS['Location']=='DAM']['NTU'],TSS[TSS['Location']=='DAM']['TSS (mg/L)'],c='g',label='DAM',s=50)
    ALL.scatter(TSS[TSS['Location']=='LBJ']['NTU'],TSS[TSS['Location']=='LBJ']['TSS (mg/L)'],c='r',label='LBJ',s=50)
    nturating = pd.ols(y=TSS[TSS['Location']=='LBJ']['TSS (mg/L)'],x=TSS[TSS['Location']=='LBJ']['NTU'])
    ALL.plot(xy,np.poly1d(NTU_TSSrating_Lab.beta)(xy),c='r')

    DTlabels = TSS[TSS['Location']=='DT'][['NTU','TSS (mg/L)']].dropna()
    labelindex(DTlabels.index,DTlabels['NTU'],DTlabels['TSS (mg/L)'])
    LBJlabels = TSS[TSS['Location']=='LBJ'][['NTU','TSS (mg/L)']].dropna()
    labelindex(LBJlabels.index,LBJlabels['NTU'],LBJlabels['TSS (mg/L)'])

    ALL.grid(True),ALL.legend()
    ALL.set_xlabel('NTU lab')
    ALL.set_ylabel('SSC mg/L')
    plt.title(title)
    plt.draw()
    if show==True:
        plt.show()
    return
#plotNTU_TSS_lab(True)    

def plotLBJ_NTUratings(show=False):
    fig, (ax) = plt.subplots(1)
    xy = np.linspace(0,1000)
    dotsize = 20
    ax.scatter(NTU_TSSrating_LBJ_YSI[1]['LBJ-YSI-NTU'],NTU_TSSrating_LBJ_YSI[1]['TSS (mg/L)'],s=dotsize,color='g',marker='o',label='LBJ-YSI')
    ax.scatter(NTU_TSSrating_LBJ_OBS[1]['LBJ-OBS-NTU'],NTU_TSSrating_LBJ_OBS[1]['TSS (mg/L)'],s=dotsize,color='r',marker='o',label='LBJ-OBS')
    ax.plot(xy,xy*LBJ_OBSrating.beta[0]+LBJ_OBSrating.beta[1],ls='-',c='r',label='LBJ-OBS rating')
    ax.plot(xy,xy*LBJ_YSIrating.beta[0]+LBJ_YSIrating.beta[1],ls='-',c='g',label='LBJ-YSI rating')
    ax.set_ylim(0,1000),ax.set_xlim(0,1700)

    labelindex(NTU_TSSrating_LBJ_OBS[1].index,NTU_TSSrating_LBJ_OBS[1]['LBJ-OBS-NTU'],NTU_TSSrating_LBJ_OBS[1]['TSS (mg/L)'])
    labelindex(NTU_TSSrating_LBJ_YSI[1].index,NTU_TSSrating_LBJ_YSI[1]['LBJ-YSI-NTU'],NTU_TSSrating_LBJ_YSI[1]['TSS (mg/L)'])
    
    ax.set_xlabel('Turbidity (NTU)'),ax.set_ylabel('Suspended Sediment Concentration (mg/L)')
    ax.grid(True), ax.legend()
    plt.suptitle('Turbidity to Suspended Sediment Concentration Rating Curves at LBJ')
    plt.draw()
    if show==True:
        plt.show()
    return
#plotLBJ_NTUratings(True)
    
    
    
def plotLinCoeffTable(show=False,norm=False):
    if norm==True:
        ALLStorms=NormalizeSSYbyCatchmentArea(compileALLStorms())
        Upper = linearfunction(ALLStorms['Qmaxupper']/1000,ALLStorms['Supper'])
        Total = linearfunction(ALLStorms['Qmaxtotal']/1000,ALLStorms['Stotal'])    
        
        Up = ['%.2f'%Upper['a'],'%.2f'%Upper['b'],'%.2f'%Upper['r2'],'%.2f'%Upper['pearson'],'%.2f'%Upper['spearman'],'%.2f'%Upper['rmse']]
        Tot = ['%.2f'%Total['a'],'%.2f'%Total['b'],'%.2f'%Total['r2'],'%.2f'%Total['pearson'],'%.2f'%Total['spearman'],'%.2f'%Total['rmse']]
        
        nrows, ncols = 2,6
        hcell, wcell=0.3,1
        hpad, wpad = 1,1
        fig = plt.figure(figsize=(ncols*wcell+wpad,nrows*hcell+hpad)) 
        coeff = fig.add_subplot(111)
        coeff.patch.set_visible(False), coeff.axis('off')
        coeff.xaxis.set_visible(False), coeff.yaxis.set_visible(False) 
        coeff.table(cellText = [Up,Tot],rowLabels=['Upper','Total'],colLabels=[r'$\alpha$',r'$\beta$',r'$r^2$',"Pearson's","Spearman's",'RMSE'],loc='center left')
   
    elif norm==False:
        ALLStorms = compileALLStorms()
        Upper = linearfunction(ALLStorms['Qmaxupper']/1000,ALLStorms['Supper'])
        Lower = linearfunction(ALLStorms['Qmaxlower']/1000,ALLStorms['Slower'])    
        Total = linearfunction(ALLStorms['Qmaxtotal']/1000,ALLStorms['Stotal'])
        
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
        coeff.table(cellText = [Up,Low,Tot],rowLabels=['Upper','Lower','Total'],colLabels=[r'$\alpha$',r'$\beta$',r'$r^2$',"Pearson's","Spearman's",'RMSE'],loc='center left')
    
    plt.suptitle("Model parameters for LINEAR Qmax-SSYev model: "+r'$SSY_{ev} = \beta*Q_{max}+\alpha$',fontsize=14)
    plt.draw()
    if show==True:
        plt.show()
    return
#plotLinCoeffTable(show=True,norm=False)


def plotPS(show=False): ### P vs. S and Q vs. S,
    fig, ps = plt.subplots(1)
    xy=None
    upperdotsize = scaleSeries(SedFluxStorms_DAM['Pmax'])
    lowerdotsize = scaleSeries(SedFluxStorms_LBJ['Pmax'])
    
    ps.scatter(SedFluxStorms_DAM['Psum'],SedFluxStorms_DAM['Ssum'],color='g',s=upperdotsize.values,label='Upper (DAM)')
    ps.scatter(ALLStorms['Pstorms'],ALLStorms['Slower'],color='y',s=lowerdotsize.values,label='Lower (LBJ-DAM)')
    ps.scatter(SedFluxStorms_LBJ['Psum'],SedFluxStorms_LBJ['Ssum'],color='r',s=lowerdotsize.values,label='Total(LBJ)')
    ## Upper Watershed (=DAM)
    PS_upper_power = powerfunction(ALLStorms['Pstorms'],ALLStorms['Supper'])
    PowerFit(ALLStorms['Pstorms'],ALLStorms['Supper'],xy,ps,linestyle='-',color='g',label='PS_upper_power '+r'$r^2$'+'%.2f'%PS_upper_power['r2'].values)
    PS_upper_linear = linearfunction(ALLStorms['Pstorms'],ALLStorms['Supper'])
    LinearFit(ALLStorms['Pstorms'],ALLStorms['Supper'],xy,ps,linestyle='--',color='g',label='PS_upper_linear '+r'$r^2$'+'%.2f'%PS_upper_linear['r2'].values)  
    ## Lower Watershed (=LBJ-DAM)
    PS_lower_power = powerfunction(ALLStorms['Pstorms'],ALLStorms['Slower'])
    PowerFit(ALLStorms['Pstorms'],ALLStorms['Slower'],ps,linestyle='-',color='y',label='PS_lower_power '+r'$r^2$'+'%.2f'%PS_lower_power['r2'].values) 
    PS_lower_linear = linearfunction(ALLStorms['Pstorms'],ALLStorms['Slower'])
    LinearFit(ALLStorms['Pstorms'],ALLStorms['Slower'],ps,linestyle='--',color='y',label='PS_lower_linear '+r'$r^2$'+'%.2f'%PS_lower_linear['r2'].values) 
    ## Total Watershed (=LBJ)
    PS_total_power = powerfunction(ALLStorms['Pstorms'],ALLStorms['Stotal'])
    PowerFit(ALLStorms['Pstorms'],ALLStorms['Stotal'],ps,linestyle='-',color='r',label='PS_total_power '+r'$r^2$'+'%.2f'%PS_total_power['r2'].values) 
    PS_total_linear = linearfunction(ALLStorms['Pstorms'],ALLStorms['Stotal'])
    LinearFit(ALLStorms['Pstorms'],ALLStorms['Stotal'],ps,linestyle='--',color='r',label='PS_total_linear '+r'$r^2$'+'%.2f'%PS_total_linear['r2'].values) 
    
    labelindex(SedFluxStorms_LBJ.index,SedFluxStorms_LBJ['Psum'],SedFluxStorms_LBJ['Ssum'])
    labelindex(SedFluxStorms_DAM.index,SedFluxStorms_DAM['Psum'],SedFluxStorms_DAM['Ssum'])
    
    ps.set_title("Event Rainfall(mm) vs. Event Sediment Flux from Fagaalu Stream")
    ps.set_ylabel('Sediment Flux (Mg)')
    ps.set_xlabel('Precipitation (mm); Dot Size = MaxP (mm/15min.)')
    ps.grid(True)
    
    plt.legend(loc='upper right',fontsize=8)              
    fig.canvas.manager.set_window_title('Figure : '+'P vs. S')

    plt.draw()
    if show==True:
        plt.show()
    return
#plotPS(True)
    
def plotPsumS(show=False,log=False,save=True,norm=True): 
    fig, ps = plt.subplots(1)
    xy=np.linspace(10,200)
    upperdotsize = 50#scaleSeries(SedFluxStorms_DAM['Qsum']/1000)
    lowerdotsize = 50#scaleSeries(SedFluxStorms_LBJ['Qsum']/1000)
    
    if norm==True:
        ALLStorms=NormalizeSSYbyCatchmentArea(compileALLStorms())
        ylabel,xlabel= r'$SSY (Mg \ km^{-2})$','Precip (mm)'
    elif norm==False:
        ALLStorms=compileALLStorms()
        ylabel,xlabel = 'SSY (Mg)','Precip (mm)'
   
    ## Lower is below in norm==False loop
    
    ## Upper Watershed (=DAM)
    ps.scatter(ALLStorms['Pstorms'],ALLStorms['Supper'],edgecolors='grey',color='g',s=upperdotsize,label='Upper (FOREST)')
    PsumS_upper_power = powerfunction(ALLStorms['Qmaxupper']/1000,ALLStorms['Supper'])
    PowerFit(ALLStorms['Pstorms'],ALLStorms['Supper'],xy,ps,linestyle='-',color='g',label='Psum_UPPER')
    PsumS_upper_linear = linearfunction(ALLStorms['Pstorms'],ALLStorms['Supper'])
    #LinearFit(ALLStorms['Pstorms'],ALLStorms['Supper'],xy,ps,linestyle='--',color='g',label='PsumS_upper_linear')  
    labelindex(ALLStorms.index,ALLStorms['Pstorms'],ALLStorms['Supper'])
    ## Total Watershed (=LBJ)
    ps.scatter(ALLStorms['Pstorms'],ALLStorms['Stotal'],edgecolors='grey',color='r',s=lowerdotsize,label='Total(VILLAGE)')
    PsumS_total_power = powerfunction(ALLStorms['Pstorms'],ALLStorms['Stotal'])
    PowerFit(ALLStorms['Pstorms'],ALLStorms['Stotal'],xy,ps,linestyle='-',color='r',label='Psum_TOTAL') 
    PsumS_total_linear = linearfunction(ALLStorms['Pstorms'],ALLStorms['Stotal'])
    #LinearFit(ALLStorms['Pstorms'],ALLStorms['Stotal'],xy,ps,linestyle='--',color='r',label='PsumS_total_linear') 
    labelindex(ALLStorms.index,ALLStorms['Pstorms'],ALLStorms['Stotal'])    
    
    ## Lower Watershed (=LBJ-DAM)
    ps.scatter(ALLStorms['Pstorms'],ALLStorms['Slower'],edgecolors='grey',color='y',s=lowerdotsize,label='Lower (VIL-FOR)')
    PsumS_lower_power = powerfunction(ALLStorms['Pstorms'],ALLStorms['Slower'])
    PowerFit(ALLStorms['Pstorms'],ALLStorms['Slower'],xy,ps,linestyle='-',color='y',label='Psum_LOWER') 
    PsumS_lower_linear = linearfunction(ALLStorms['Pstorms'],ALLStorms['Slower'])
    #LinearFit(ALLStorms['Pstorms'],ALLStorms['Slower'],xy,ps,linestyle='--',color='y',label='PsumS_lower_linear') 
    labelindex(ALLStorms.index,ALLStorms['Pstorms'],ALLStorms['Slower'])

    ps.legend(loc='best',ncol=2,fancybox=True)  
    title="Event Precipitation vs Event Sediment Yield from Fagaalu Stream"
    ps.set_title(title)
    ps.set_ylabel(ylabel)
    ps.set_xlabel(xlabel)

    fig.canvas.manager.set_window_title('Figure : '+'Psum vs. S')
    
    logaxes(log,fig)
    ps.autoscale_view(True,True,True)
    show_plot(show,fig)
    savefig(save,title)
    return
#plotPsumS(show=True,log=False,save=True)
#plotPsumS(show=True,log=True,save=True,norm=False)
#plotPsumS(show=True,log=True,save=True,norm=True)


def plotQS(SedFluxStorms_DAM=SedFluxStorms_DAM,SedFluxStorms_LBJ=SedFluxStorms_LBJ,ALLStorms=ALLStorms,show=False,log=False): ### P vs. S and Q vs. S
    fig, qs = plt.subplots(1)
    xy=None
    upperdotsize = scaleSeries(SedFluxStorms_DAM['Qmax'])
    lowerdotsize = scaleSeries(SedFluxStorms_LBJ['Qmax'])
   
    qs.scatter(SedFluxStorms_DAM['Qsum'],SedFluxStorms_DAM['Ssum'],color='g',s=upperdotsize.values,label='Upper (DAM)')
    qs.scatter(ALLStorms['Qsumlower'],ALLStorms['Slower'],color='y',s=lowerdotsize.values,label='Lower (LBJ-DAM)')
    qs.scatter(SedFluxStorms_LBJ['Qsum'],SedFluxStorms_LBJ['Ssum'],color='r',s=lowerdotsize.values,label='Total(LBJ)')
    ## Upper Watershed (=DAM)
    QS_upper_power = powerfunction(ALLStorms['Qsumupper'],ALLStorms['Supper'])
    PowerFit(ALLStorms['Qsumupper'],ALLStorms['Supper'],xy,qs,linestyle='-',color='g',label='QS_upper_power '+r'$r^2$'+'%.2f'%QS_upper_power['r2'].values)
    QS_upper_linear = linearfunction(ALLStorms['Qsumupper'],ALLStorms['Supper'])
    LinearFit(ALLStorms['Qsumupper'],ALLStorms['Supper'],xy,qs,linestyle='--',color='g',label='QS_upper_linear '+r'$r^2$'+'%.2f'%QS_upper_linear['r2'].values)  
    ## Lower Watershed (=LBJ-DAM)
    QS_lower_power = powerfunction(ALLStorms['Qsumlower'],ALLStorms['Slower'])
    PowerFit(ALLStorms['Qsumlower'],ALLStorms['Slower'],xy,qs,linestyle='-',color='y',label='QS_lower_power '+r'$r^2$'+'%.2f'%QS_lower_power['r2'].values) 
    QS_lower_linear = linearfunction(ALLStorms['Qsumlower'],ALLStorms['Slower'])
    LinearFit(ALLStorms['Qsumlower'],ALLStorms['Slower'],xy,qs,linestyle='--',color='y',label='QS_lower_linear '+r'$r^2$'+'%.2f'%QS_lower_linear['r2'].values) 
    ## Total Watershed (=LBJ)
    QS_total_power = powerfunction(ALLStorms['Qsumtotal'],ALLStorms['Stotal'])
    PowerFit(ALLStorms['Qsumtotal'],ALLStorms['Stotal'],xy,qs,linestyle='-',color='r',label='QS_total_power '+r'$r^2$'+'%.2f'%QS_total_power['r2'].values) 
    QS_total_linear = linearfunction(ALLStorms['Qsumtotal'],ALLStorms['Stotal'])
    LinearFit(ALLStorms['Qsumtotal'],ALLStorms['Stotal'],xy,qs,linestyle='--',color='r',label='QS_total_linear '+r'$r^2$'+'%.2f'%QS_total_linear['r2'].values) 
    
    labelindex(SedFluxStorms_LBJ.index,SedFluxStorms_LBJ['Qsum'],SedFluxStorms_LBJ['Ssum'])
    labelindex(SedFluxStorms_DAM.index,SedFluxStorms_DAM['Qsum'],SedFluxStorms_DAM['Ssum'])
    
    qs.set_title("Event Discharge vs. Event Sediment Yield from Fagaalu Stream")
    qs.set_ylabel('Sediment Yield (Mg)')
    qs.set_xlabel('Discharge (L); DotSize= Qmax (L/sec)')
    qs.grid(True)
    
    plt.legend(loc=4,fontsize=8)              
    fig.canvas.manager.set_window_title('Figure : '+'Q vs. S')
    if log==True:
        qs.set_xscale('log'),qs.set_yscale('log')
    plt.draw()
    if show==True:
        plt.show()
    return
#plotQS(show=True)
#plotQS(show=True,log=True)
    
def plotPsumSyears(show=False): ### P vs. S and Q vs. S
    fig, (psLBJ,psDAM) = plt.subplots(1,2,sharex=True,sharey=True)
    
    lbjdotsize = scaleSeries(SedFluxStorms_LBJ['Pmax'])
    damdotsize = scaleSeries(SedFluxStorms_DAM['Pmax'])

    ## Psum vs. Ssum 
    LBJ_Psum_Ssum = pd.ols(y=SedFluxStorms_LBJ['Ssum'],x=SedFluxStorms_LBJ['Psum'])
    DAM_Psum_Ssum = pd.ols(y=SedFluxStorms_DAM['Ssum'],x=SedFluxStorms_DAM['Psum'])    
    
    psLBJ.scatter(SedFluxStorms_LBJ['Psum'][start2012:stop2012],SedFluxStorms_LBJ['Ssum'][start2012:stop2012],c='g',marker='o',s=lbjdotsize[start2012:stop2012].values,label='LBJ 2012')
    psLBJ.scatter(SedFluxStorms_LBJ['Psum'][start2013:stop2013],SedFluxStorms_LBJ['Ssum'][start2013:stop2013],c='y',marker='o',s=lbjdotsize[start2013:stop2013].values,label='LBJ 2013')
    psLBJ.scatter(SedFluxStorms_LBJ['Psum'][start2014:stop2014],SedFluxStorms_LBJ['Ssum'][start2014:stop2014],c='r',marker='o',s=lbjdotsize[start2014:stop2014].values,label='LBJ 2014')

    psDAM.scatter(SedFluxStorms_DAM['Psum'][start2012:stop2012],SedFluxStorms_DAM['Ssum'][start2012:stop2012],c='g',marker='o',s=damdotsize[start2012:stop2012].values,label='DAM 2012')
    psDAM.scatter(SedFluxStorms_DAM['Psum'][start2013:stop2013],SedFluxStorms_DAM['Ssum'][start2013:stop2013],c='y',marker='o',s=damdotsize[start2013:stop2013].values,label='DAM 2013')
    #psDAM.scatter(SedFluxStorms_DAM['Psum'][start2014:stop2014],SedFluxStorms_DAM['Ssum'][start2014:stop2014],c='r',marker='o',s=damdotsize[start2014:stop2014].values,label='DAM 2014')
  

    Polyfit(SedFluxStorms_LBJ['Psum'][start2012:stop2012],SedFluxStorms_LBJ['Ssum'][start2012:stop2012],1,'g','LBJ 2012',100,psLBJ)
    Polyfit(SedFluxStorms_LBJ['Psum'][start2013:stop2013],SedFluxStorms_LBJ['Ssum'][start2013:stop2013],1,'y','LBJ 2013',100,psLBJ)
    Polyfit(SedFluxStorms_LBJ['Psum'][start2014:stop2014],SedFluxStorms_LBJ['Ssum'][start2014:stop2014],1,'r','LBJ 2014',100,psLBJ)
    Polyfit(SedFluxStorms_LBJ['Psum'],SedFluxStorms_LBJ['Ssum'],1,'k','AllYears: '+r'$r^2$'+'%.2f'%LBJ_Psum_Ssum.r2,100,psLBJ)
    
    Polyfit(SedFluxStorms_DAM['Psum'][start2012:stop2012],SedFluxStorms_DAM['Ssum'][start2012:stop2012],1,'g','DAM 2012',100,psDAM) ### Won't work if na values in np.array->polyfit
    Polyfit(SedFluxStorms_DAM['Psum'][start2013:stop2013],SedFluxStorms_DAM['Ssum'][start2013:stop2013],1,'y','DAM 2013',100,psDAM) 
    Polyfit(SedFluxStorms_DAM['Psum'],SedFluxStorms_DAM['Ssum'],1,'k','AllYears: '+r'$r^2$'+'%.2f'%DAM_Psum_Ssum.r2,100,psDAM) 
    
    labelindex(SedFluxStorms_LBJ.index,SedFluxStorms_LBJ['Psum'],SedFluxStorms_LBJ['Ssum'])
    labelindex(SedFluxStorms_DAM.index,SedFluxStorms_DAM['Psum'],SedFluxStorms_DAM['Ssum'])
    
    plt.suptitle("Event Precipitation vs. Event Sediment Flux from Fagaalu Stream",fontsize=14)
    psLBJ.set_ylabel('Sediment Flux (Mg)')
    psLBJ.set_xlabel('Precipitation (mm)')
    psDAM.set_xlabel('Precipitation (mm)')
    psLBJ.set_title('LBJ'),psDAM.set_title('DAM')
    psLBJ.grid(True), psDAM.grid(True)
    
    psLBJ.legend(loc=4), psDAM.legend(loc=4)           
    fig.canvas.manager.set_window_title('Figure : '+'P vs. S')

    plt.draw()
    if show==True:
        plt.show()
    return
#plotPsumSyears(True)
    
def QsumSyears(show=False): ### P vs. S and Q vs. S
    fig, (lbj,dam) = plt.subplots(1,2,sharex=True,sharey=True)

    lbjdotsize = scaleSeries(SedFluxStorms_LBJ['Qmax'])
    damdotsize = scaleSeries(SedFluxStorms_DAM['Qmax'])
    
    
    ## Qsum vs. Ssum 
    LBJ_Qsum_Ssum = pd.ols(y=SedFluxStorms_LBJ['Ssum'],x=SedFluxStorms_LBJ['Qsum'])
    DAM_Qsum_Ssum = pd.ols(y=SedFluxStorms_DAM['Ssum'],x=SedFluxStorms_DAM['Qsum'])   
    
    lbj.scatter(SedFluxStorms_LBJ['Qsum'][start2012:stop2012],SedFluxStorms_LBJ['Ssum'][start2012:stop2012],c='g',marker='o',s=lbjdotsize[start2012:stop2012].values,label='LBJ-2012')
    lbj.scatter(SedFluxStorms_LBJ['Qsum'][start2013:stop2013],SedFluxStorms_LBJ['Ssum'][start2013:stop2013],c='y',marker='o',s=lbjdotsize[start2013:stop2013].values,label='LBJ-2013')
    lbj.scatter(SedFluxStorms_LBJ['Qsum'][start2014:stop2014],SedFluxStorms_LBJ['Ssum'][start2014:stop2014],c='r',marker='o',s=lbjdotsize[start2014:stop2014].values,label='LBJ-2014')
    
    dam.scatter(SedFluxStorms_DAM['Qsum'][start2012:stop2012],SedFluxStorms_DAM['Ssum'][start2012:stop2012],c='g',marker='o',s=damdotsize[start2012:stop2012].values,label='DAM-2012')
    dam.scatter(SedFluxStorms_DAM['Qsum'][start2013:stop2013],SedFluxStorms_DAM['Ssum'][start2013:stop2013],c='y',marker='o',s=damdotsize[start2013:stop2013].values,label='DAM-2013')
    #dam.scatter(SedFluxStorms_DAM['Qsum'][start2014:stop2014],SedFluxStorms_DAM['Ssum'][start2014:stop2014],c='r',marker='o',s=damdotsize[start2014:stop2014].values,label='DAM-2014')

    Polyfit(SedFluxStorms_LBJ['Qsum'][start2012:stop2012],SedFluxStorms_LBJ['Ssum'][start2012:stop2012],1,'g','LBJ 2012',100,lbj)
    Polyfit(SedFluxStorms_LBJ['Qsum'][start2013:stop2013],SedFluxStorms_LBJ['Ssum'][start2013:stop2013],1,'y','LBJ 2013',100,lbj)
    Polyfit(SedFluxStorms_LBJ['Qsum'][start2014:stop2014],SedFluxStorms_LBJ['Ssum'][start2014:stop2014],1,'r','LBJ 2014',100,lbj)
    Polyfit(SedFluxStorms_LBJ['Qsum'],SedFluxStorms_LBJ['Ssum'],1,'k','AllYears: '+r'$r^2$'+'%.2f'%LBJ_Qsum_Ssum.r2,100,lbj)
    
    Polyfit(SedFluxStorms_DAM['Qsum'][start2012:stop2012],SedFluxStorms_DAM['Ssum'][start2012:stop2012],1,'g','DAM 2012',100,dam) ### Won't work if na values in np.array->polyfit
    Polyfit(SedFluxStorms_DAM['Qsum'][start2013:stop2013],SedFluxStorms_DAM['Ssum'][start2013:stop2013],1,'y','DAM 2013',100,dam)
    Polyfit(SedFluxStorms_DAM['Qsum'],SedFluxStorms_DAM['Ssum'],1,'k','AllYears: '+r'$r^2$'+'%.2f'%DAM_Qsum_Ssum.r2,100,dam)
    
    labelindex(SedFluxStorms_LBJ.index,SedFluxStorms_LBJ['Qsum'],SedFluxStorms_LBJ['Ssum'])
    labelindex(SedFluxStorms_DAM.index,SedFluxStorms_DAM['Qsum'],SedFluxStorms_DAM['Ssum'])
    
    plt.suptitle("Event Discharge vs. Event Sediment Flux from Fagaalu Stream (dotsize=Qmax)",fontsize=16)
    lbj.set_ylabel('Sediment Flux (Mg)'),dam.set_ylabel('Sediment Flux (Mg)')
    lbj.set_xlabel('Discharge (L)'),dam.set_xlabel('Discharge (L)')
    lbj.set_title('LBJ'), dam.set_title('DAM')
    lbj.grid(True),dam.grid(True)
    
    lbj.legend(loc=4),dam.legend(loc=4)              
    fig.canvas.manager.set_window_title('Figure : '+'Q vs. S')

    plt.draw()
    if show==True:
        plt.show()
    return
#plotQsumSyears(True)

def QmaxSyears(show=False): ### P vs. S and Q vs. S
    fig, (lbj,dam) = plt.subplots(1,2,sharex=True,sharey=True)

    lbjdotsize = scaleSeries(SedFluxStorms_LBJ['Qmax']).values
    damdotsize = scaleSeries(SedFluxStorms_DAM['Qmax']).values
    
    ## Qmax vs. Ssum 
    LBJ_Qmax_Ssum = pd.ols(y=SedFluxStorms_LBJ['Ssum'],x=SedFluxStorms_LBJ['Qmax'])
    DAM_Qmax_Ssum = pd.ols(y=SedFluxStorms_DAM['Ssum'],x=SedFluxStorms_DAM['Qmax'])   
    
    lbj.scatter(SedFluxStorms_LBJ['Qmax'][start2012:stop2012],SedFluxStorms_LBJ['Ssum'][start2012:stop2012],c='g',marker='o',s=lbjdotsize,label='LBJ-2012')
    lbj.scatter(SedFluxStorms_LBJ['Qmax'][start2013:stop2013],SedFluxStorms_LBJ['Ssum'][start2013:stop2013],c='y',marker='o',s=lbjdotsize,label='LBJ-2013')
    lbj.scatter(SedFluxStorms_LBJ['Qmax'][start2014:stop2014],SedFluxStorms_LBJ['Ssum'][start2014:stop2014],c='r',marker='o',s=lbjdotsize,label='LBJ-2014')

    
    dam.scatter(SedFluxStorms_DAM['Qmax'][start2012:stop2012],SedFluxStorms_DAM['Ssum'][start2012:stop2012],c='g',marker='o',s=damdotsize,label='DAM-2012')
    dam.scatter(SedFluxStorms_DAM['Qmax'][start2013:stop2013],SedFluxStorms_DAM['Ssum'][start2013:stop2013],c='y',marker='o',s=damdotsize,label='DAM-2013')
    dam.scatter(SedFluxStorms_DAM['Qmax'][start2014:stop2014],SedFluxStorms_DAM['Ssum'][start2014:stop2014],c='r',marker='o',s=damdotsize,label='DAM-2014')
    
    Polyfit(SedFluxStorms_LBJ['Qmax'][start2012:stop2012],SedFluxStorms_LBJ['Ssum'][start2012:stop2012],1,'g','LBJ 2012',100,lbj)
    Polyfit(SedFluxStorms_LBJ['Qmax'][start2013:stop2013],SedFluxStorms_LBJ['Ssum'][start2013:stop2013],1,'y','LBJ 2013',100,lbj)
    Polyfit(SedFluxStorms_LBJ['Qmax'][start2014:stop2014],SedFluxStorms_LBJ['Ssum'][start2014:stop2014],1,'r','LBJ 2014',100,lbj)
    Polyfit(SedFluxStorms_LBJ['Qmax'],SedFluxStorms_LBJ['Ssum'],1,'k','AllYears: '+r'$r^2$'+'%.2f'%LBJ_Qmax_Ssum.r2,100,lbj)
    
    Polyfit(SedFluxStorms_DAM['Qmax'][start2012:stop2012],SedFluxStorms_DAM['Ssum'][start2012:stop2012],1,'g','DAM 2012',100,dam) ### Won't work if na values in np.array->polyfit
    Polyfit(SedFluxStorms_DAM['Qmax'][start2013:stop2013],SedFluxStorms_DAM['Ssum'][start2013:stop2013],1,'y','DAM 2013',100,dam)
    Polyfit(SedFluxStorms_DAM['Qmax'],SedFluxStorms_DAM['Ssum'],1,'k','AllYears: '+r'$r^2$'+'%.2f'%DAM_Qmax_Ssum.r2,100,dam)
   
    labelindex(SedFluxStorms_LBJ.index,SedFluxStorms_LBJ['Qmax'],SedFluxStorms_LBJ['Ssum'])
    labelindex(SedFluxStorms_DAM.index,SedFluxStorms_DAM['Qmax'],SedFluxStorms_DAM['Ssum'])
    
    plt.suptitle("Max Event Discharge vs. Total Event Sediment Flux from Fagaalu Stream  (dotsize=Pmax)",fontsize=14)
    lbj.set_ylabel('Sediment Flux (Mg)'),dam.set_ylabel('Sediment Flux (Mg)')
    lbj.set_xlabel('Max Event Discharge (L/sec)'),dam.set_xlabel('Max Event Discharge (L/sec)')
    lbj.set_title('LBJ'), dam.set_title('DAM')
    lbj.grid(True),dam.grid(True)
    
    log=False
    if log==True:
        lbj.set_yscale('log'),lbj.set_xscale('log')
        dam.set_yscale('log'),dam.set_xscale('log')
    
    lbj.legend(loc=4),dam.legend(loc=4)              
    fig.canvas.manager.set_window_title('Figure : '+'Qmax vs. S')

    plt.draw()
    if show==True:
        plt.show()
    return
#plotQmaxSyears(True)
