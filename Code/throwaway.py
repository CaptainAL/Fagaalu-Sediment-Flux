# -*- coding: utf-8 -*-
"""
Created on Wed Dec 03 20:32:00 2014

@author: Alex
"""

## PT3 DAM
# tshift in 15Min(or whatever the timestep is), zshift in cm
PT3aa = PT_Hobo(allbaro,'PT3a Dam',XL,'PT-Fagaalu3aa',12,zshift=-3.75)
PT3ab = PT_Hobo(allbaro,'PT3a Dam',XL,'PT-Fagaalu3ab',12,zshift=-3.75)
PT3b = PT_Levelogger(allbaro,'PT3b Dam',XL,'PT-Fagaalu3b',0,zshift=-23)
PT3c = PT_Levelogger(allbaro,'PT3c Dam',XL,'PT-Fagaalu3c',0,zshift=-19.5)
PT3d = PT_Levelogger(allbaro,'PT3d Dam',XL,'PT-Fagaalu3d',0,zshift=-17.1)
PT3e = PT_Levelogger(allbaro,'PT3e Dam',XL,'PT-Fagaalu3e',0,zshift=-18.4)
PT3f = PT_Levelogger(allbaro,'PT3f Dam',XL,'PT-Fagaalu3f',0,zshift=-17)
PT3g = PT_Levelogger(allbaro-1.5,'PT3g Dam',XL,'PT-Fagaalu3g',0,zshift=-10.5)
PT3 = pd.concat([PT3a,PT3b,PT3c,PT3d,PT3e,PT3f,PT3g])
PT3 = PT3[PT3>0]

#storm_data=pd.DataFrame(columns=['DAM-Sed','DAM-Sed-cum','DAMgrab','DAMgrabSed','DAMgrabssc', 
    'DAMntu','DAMq','DAMssc','DAMtSed','DAMtssc','LBJ-Sed','LBJ-Sed-cum','LBJfnu','LBJgrab',
    'LBJgrabSed','LBJgrabssc','LBJntu','LBJq','LBJssc','LBJtSed','LBJtssc','Precip',
    'QUARRY-Sed','QUARRY-Sed-cum','QUARRYfnu','QUARRYgrab','QUARRYgrabSed','QUARRYgrabssc',
    'QUARRYq','QUARRYssc','QUARRYtSed','QUARRYtssc'],
    index=pd.date_range(start2012,stop2014,freq='15Min'))
    
data = pd.DataFrame({'Precip':Precip['Timu1-15'][start:end],
        'LBJq':LBJ['Q'][start:end],'QUARRYq':QUARRY['Q'][start:end],'DAMq':DAM['Q'][start:end],
        'LBJntu':LBJ['YSI-NTU'],'LBJfnu':LBJ['OBS-FNU'],'DAMntu':DAM['NTU'],
        'LBJssc':LBJ['SSC-mg/L'][start:end],'QUARRYssc':QUARRY['SSC-mg/L'][start:end],'DAMssc':DAM['SSC-mg/L'][start:end],
        'LBJgrabssc':LBJ['Grab-SSC-mg/L'][start:end],'QUARRYgrabssc':QUARRY['Grab-SSC-mg/L'][start:end],'DAMgrabssc':DAM['Grab-SSC-mg/L'][start:end],
        'LBJ-Sed':LBJ['SedFlux-tons/15min'][start:end],'QUARRY-Sed':QUARRY['SedFlux-tons/15min'][start:end],
        'DAM-Sed':DAM['SedFlux-tons/15min'][start:end],
        'LBJgrab':LBJgrab['SSC (mg/L)'][start:end],'QUARRYgrab':QUARRYgrab['SSC (mg/L)'][start:end],
        'DAMgrab':DAMgrab['SSC (mg/L)'][start:end]},index=pd.date_range(start,end,freq='15Min')) 
   
    
data = pd.DataFrame({'Precip':Precip['Timu1-15'][start:end].dropna(),
        'LBJq':LBJ['Q'][start:end],'QUARRYq':QUARRY['Q'][start:end],'DAMq':DAM['Q'][start:end],
        'LBJgrab':LBJgrab['SSC (mg/L)'][start:end],'QUARRYgrab':QUARRYgrab['SSC (mg/L)'][start:end],'DAMgrab':DAMgrab['SSC (mg/L)'][start:end],        
        'LBJntu':LBJ['YSI-NTU'][start:end],'LBJfnu':LBJ['OBS-FNU'][start:end],'QUARRYfnu':QUARRY['OBS-FNU'][start:end],'DAMntu':DAM['NTU'][start:end],
        'LBJtssc':LBJ['T-SSC-mg/L'][start:end],'QUARRYtssc':QUARRY['T-SSC-mg/L'][start:end],'DAMtssc':DAM['T-SSC-mg/L'][start:end],
        'LBJtSed':LBJ['T-SedFlux-tons/sec'][start:end],'QUARRYtSed':QUARRY['T-SedFlux-tons/sec'][start:end],'DAMtSed':DAM['T-SedFlux-tons/sec'][start:end],
        'LBJgrabssc':LBJ['Grab-SSC-mg/L'][start:end],'QUARRYgrabssc':QUARRY['Grab-SSC-mg/L'][start:end],'DAMgrabssc':DAM['Grab-SSC-mg/L'][start:end],        
        'LBJgrabSed':LBJ['Grab-SedFlux-tons/sec'][start:end],'QUARRYgrabSed':QUARRY['Grab-SedFlux-tons/sec'][start:end],'DAMgrabSed':DAM['Grab-SedFlux-tons/sec'][start:end],
        'LBJssc':LBJ['SSC-mg/L'][start:end],'QUARRYssc':QUARRY['SSC-mg/L'][start:end],'DAMssc':DAM['SSC-mg/L'][start:end],
        'LBJ-Sed':LBJ['SedFlux-tons/sec'][start:end],'QUARRY-Sed':QUARRY['SedFlux-tons/sec'][start:end],'DAM-Sed':DAM['SedFlux-tons/sec'][start:end],
        'LBJ-Sed-cum':LBJ['SedFlux-tons/15min'][start:end].cumsum(),'QUARRY-Sed-cum':QUARRY['SedFlux-tons/15min'][start:end].cumsum(),
        'DAM-Sed-cum':DAM['SedFlux-tons/15min'][start:end].cumsum()},index=pd.date_range(start,end,freq='15Min'))


        ## Summary stats
        total_storm = len(data[start:end])
        percent_P = len(data['Precip'].dropna())/total_storm *100.
        percent_Q_LBJ = len(data['LBJq'].dropna())/total_storm * 100.
        percent_Q_DAM = len(data['DAMq'].dropna())/total_storm * 100.
        count_LBJgrab = len(LBJgrab.dropna())
        count_QUARRYgrab = len(QUARRYgrab.dropna())
        count_DAMgrab = len(DAMgrab.dropna())
        percent_SSC_LBJ = len(data['LBJssc'].dropna())/total_storm * 100.
        percent_SSC_DAM = len(data['DAMssc'].dropna())/total_storm * 100.
        percent_SED_LBJ = len(data['LBJ-Sed'].dropna())/total_storm * 100.
        percent_SED_DAM = len(data['DAM-Sed'].dropna())/total_storm * 100.
        if print_stats==True:
            print str(start)+' '+str(end)+' Storm#:'+str(count)
            print '%P:'+str(percent_P)+' %Q_LBJ:'+str(percent_Q_LBJ)+' %Q_DAM:'+str(percent_Q_DAM)
            print '%SSC_LBJ:'+str(percent_SSC_LBJ)+' %SSC_DAM:'+str(percent_SSC_DAM)
            print '#LBJgrab:'+str(count_LBJgrab)+' #QUARRYgrab:'+str(count_QUARRYgrab)+' #DAMgrab:'+str(count_DAMgrab)        
        ## Calculate Event Mean Concentration
        if len(data['DAMgrab'])>=3:
            data['sEMC-DAM']=data['DAMgrab'].mean()
        if len(data['QUARRYgrab'])>=3:
            data['sEMC-QUARRY']=data['QUARRYgrab'].mean()
        if len(data['QUARRYgrab'])>=3:
            data['sEMC-LBJ']=data['LBJgrab'].mean()
        ## Make sure data is complete for storms
        if percent_Q_LBJ <= 95:
            data['LBJq'] = np.nan
        if percent_Q_DAM <= 95:
            data['DAMq'] = np.nan
        if percent_SSC_LBJ <= 95:
            data['LBJssc'] = np.nan
        if percent_SSC_LBJ <= 95:
            data['LBJssc'] = np.nan
        if percent_SSC_DAM <= 95:
            data['DAMssc'] = np.nan
        if percent_SED_LBJ <= 95:
            data['LBJ-Sed'] = np.nan
        if percent_SED_DAM <= 95:
            data['DAM-Sed'] = np.nan    
        if data['LBJ-Sed'].sum() < 0:
            data['LBJ-Sed'] = np.nan
        if data['LBJ-Sed'].sum() < 0:
            data['LBJ-Sed'] = np.nan
            
            

### Fit nonlinear wiht intercept zero
#for _ in range(3):## add zero/zero intercept
#    LBJstageDischarge=LBJstageDischarge.append(pd.DataFrame({'stage(cm)':0,'Q-AV(L/sec)':0},index=[np.random.rand()])) 
#LBJ_AVnonLinear = nonlinearfunction(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AV(L/sec)'],order=3,interceptZero=False)  
#LBJstageDischarge=LBJstageDischarge.dropna() ## get rid of zero/zero interctp
#
#for _ in range(3):## add zero/zero intercept
#    LBJstageDischarge=LBJstageDischarge.append(pd.DataFrame({'stage(cm)':0,'Q-AManningV(L/sec)':0},index=[np.random.rand()])) 
#LBJ_AManningVnonLinear = nonlinearfunction(LBJstageDischarge['stage(cm)'],LBJstageDischarge['Q-AManningV(L/sec)'],order=3,interceptZero=False)
#LBJstageDischarge=LBJstageDischarge.dropna() ## get rid of zero/zero interctp



### Calibrate Mannings n factor at LBJ
def plotManningCalibrate_n(show=False,log=False,save=False): ## Rating Curves
    fig, (site_lbj, site_lbj_zoom)= plt.subplots(1,2,figsize=(8,4))
    xy = np.linspace(0,8000,8000)
    title="Discharge Ratings for VILLAGE (LBJ)"
    #LBJ AV Measurements and Rating Curve
    site_lbj.plot(LBJstageDischarge['Q-AV(L/sec)'][start2012:stop2012],LBJstageDischarge['stage(cm)'][start2012:stop2012],'.',color='g',markeredgecolor='k',label='LBJ_AV 12') 
    site_lbj.plot(LBJstageDischarge['Q-AV(L/sec)'][start2013:stop2013],LBJstageDischarge['stage(cm)'][start2013:stop2013],'.',color='y',markeredgecolor='k',label='LBJ_AV 13') 
    site_lbj.plot(LBJstageDischarge['Q-AV(L/sec)'][start2014:stop2014],LBJstageDischarge['stage(cm)'][start2014:stop2014],'.',color='r',markeredgecolor='k',label='LBJ_AV 14') 
    site_lbj_zoom.plot(LBJstageDischarge['Q-AV(L/sec)'][start2012:stop2012],LBJstageDischarge['stage(cm)'][start2012:stop2012],'.',color='g',markeredgecolor='k',label='LBJ_AV 12') 
    site_lbj_zoom.plot(LBJstageDischarge['Q-AV(L/sec)'][start2013:stop2013],LBJstageDischarge['stage(cm)'][start2013:stop2013],'.',color='y',markeredgecolor='k',label='LBJ_AV 13') 
    site_lbj_zoom.plot(LBJstageDischarge['Q-AV(L/sec)'][start2014:stop2014],LBJstageDischarge['stage(cm)'][start2014:stop2014],'.',color='r',markeredgecolor='k',label='LBJ_AV 14') 

    ## LBJ MODELS
    ## LBJ Power
    LBJ_AVpower = powerfunction(LBJstageDischarge['Q-AV(L/sec)'],LBJstageDischarge['stage(cm)'])    
    PowerFit(LBJstageDischarge['Q-AV(L/sec)'],LBJstageDischarge['stage(cm)'],xy,site_lbj,c='g',ls='--',label='LBJ_AVpower '+r'$r^2$'+"%.2f"%LBJ_AVpower['r2'])    
    PowerFit(LBJstageDischarge['Q-AV(L/sec)'],LBJstageDischarge['stage(cm)'],xy,site_lbj_zoom,c='g',ls='--',label='LBJ_AVpower '+r'$r^2$'+"%.2f"%LBJ_AVpower['r2'])        
    ## LBJ Mannings from stream survey
    LBJ_Manstage = LBJ_Man_reduced['stage']*100
    LBJ_S, LBJ_n, LBJ_k = 0.016, np.append(np.arange(0.035,.13,.02),np.array(.06)), 1
    for n in LBJ_n:
        print str(n)
        LBJ_Man = Mannings_Series(datadir+'Q/Cross_Section_Surveys/LBJ_cross_section.xlsx','LBJ_m',Slope=LBJ_S,Manning_n=n,k=LBJ_k,stage_series=LBJ_Manstage)
        LBJ_Man['Q'] = LBJ_Man['Q']*1000        
        site_lbj.plot(LBJ_Man['Q'],LBJ_Manstage,'-',markersize=2,label='n='+str(n))
        site_lbj_zoom.plot(LBJ_Man['Q'],LBJ_Manstage,'-',markersize=2,label='n='+str(n))
    ## 0 to 15
    LBJ_n, LBJ_k = .055, 1
    LBJ_0_15 = Mannings_Series(datadir+'Q/Cross_Section_Surveys/LBJ_cross_section.xlsx','LBJ_m',Slope=LBJ_S,Manning_n=LBJ_n,k=LBJ_k,stage_series=LBJ_Manstage[LBJ_Manstage<=15])
    LBJ_0_15['Q'] = LBJ_0_15['Q']*1000        
    site_lbj.plot(LBJ_0_15['Q'],LBJ_Manstage[LBJ_Manstage<=15],'-',markersize=2,label='n='+str(LBJ_n))
    site_lbj_zoom.plot(LBJ_0_15['Q'],LBJ_Manstage[LBJ_Manstage<=15],'-',c='k',markersize=4,label='n='+str(LBJ_n))
    ## 15 to 40
    LBJ_n, LBJ_k = .095, 1
    LBJ_15_40 = Mannings_Series(datadir+'Q/Cross_Section_Surveys/LBJ_cross_section.xlsx','LBJ_m',Slope=LBJ_S,Manning_n=LBJ_n,k=LBJ_k,stage_series=LBJ_Manstage[(LBJ_Manstage>15) & (LBJ_Manstage<=40)])
    LBJ_15_40['Q'] = LBJ_15_40['Q']*1000        
    site_lbj.plot(LBJ_15_40['Q'],LBJ_Manstage[(LBJ_Manstage>15) & (LBJ_Manstage<=40)],'-',markersize=2,label='n='+str(LBJ_n))
    site_lbj_zoom.plot(LBJ_15_40['Q'],LBJ_Manstage[(LBJ_Manstage>15) & (LBJ_Manstage<=40)],'-',c='k',markersize=4,label='n='+str(LBJ_n))    
    ## 40 and up    
    LBJ_n, LBJ_k = .07, 1
    LBJ_40 = Mannings_Series(datadir+'Q/Cross_Section_Surveys/LBJ_cross_section.xlsx','LBJ_m',Slope=LBJ_S,Manning_n=LBJ_n,k=LBJ_k,stage_series=LBJ_Manstage[LBJ_Manstage>40])
    LBJ_40['Q'] = LBJ_40['Q']*1000        
    site_lbj.plot(LBJ_40['Q'],LBJ_Manstage[LBJ_Manstage>40],'-',markersize=2,label='n='+str(LBJ_n))
    site_lbj_zoom.plot(LBJ_40['Q'],LBJ_Manstage[LBJ_Manstage>40],'-',c='k',markersize=4,label='n='+str(LBJ_n))   
    
    ## Storm Thresholds
    site_lbj.axhline(LBJ_storm_threshold,ls='--',linewidth=0.6,c='r',label='Storm threshold')
    site_lbj_zoom.axhline(LBJ_storm_threshold,ls='--',linewidth=0.6,c='r',label='Storm threshold')
    ## Label subplots    
    site_lbj.set_ylabel('Stage(cm)'),site_lbj.set_xlabel('Q(L/sec)'),site_lbj_zoom.set_xlabel('Q(L/sec)')
    ## Format subplots
    site_lbj.set_ylim(0,PT1['stage'].max()+10)#,site_lbj.set_xlim(0,LBJ_AVnonLinear(PT1['stage'].max()+10))
    site_lbj_zoom.set_ylim(0,45), site_lbj_zoom.set_xlim(0,1600)
    ## Legends
    site_lbj.legend(loc='lower right',fancybox=True)  
    ## Figure title
    #plt.suptitle(title,fontsize=16)
    fig.canvas.manager.set_window_title('Figure : '+title) 
    logaxes(log,fig)
    for ax in fig.axes:
        ax.autoscale_view(True,True,True)
    plt.tight_layout(pad=0.1)
    show_plot(show,fig)
    savefig(save,title)
    return
plotManningCalibrate_n(show=True,log=False,save=False)