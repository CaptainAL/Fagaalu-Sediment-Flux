# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 08:42:22 2015

@author: Alex
"""

#T SSC ratings parameter table


def linearfunction(x,y,name='linear rating'):
    datadf = pd.DataFrame.from_dict({'x':x,'y':y}).dropna() ## put x and y in a dataframe so you can drop ones that don't match up    
    datadf = datadf[datadf>=0].dropna() ##verify data is valid (not inf)
    regression = pd.ols(y=datadf['y'],x=datadf['x'],intercept=False)
    pearson = pearson_r(datadf['x'],datadf['y'])[0]
    spearman = spearman_r(datadf['x'],datadf['y'])[0]
    coeffdf = pd.DataFrame({'a':[regression.beta[1]],'b':[regression.beta[0]],'r2':[regression.r2],'rmse':[regression.rmse],'pearson':[pearson],'spearman':[spearman]},index=[name])
    return coeffdf
    
def plotNTUratingstable(show=False,save=False):
    ## NTU
    ## Lab
    LAB = linearfunction(SSC[SSC['Location']=='LBJ']['NTU'],SSC[SSC['Location']=='LBJ']['SSC (mg/L)'])
    lab = ['%.2f'%LAB['a'],'%.2f'%LAB['b'],'%.2f'%LAB['r2'],'%.2f'%LAB['pearson'],'%.2f'%LAB['spearman'],'%.2f'%LAB['rmse']]
    ## LBJ YSI
    LBJ_YSI = linearfunction(T_SSC_LBJ_YSI[1]['T-NTU'],T_SSC_LBJ_YSI[1]['SSC (mg/L)'])
    lbj_ysi = ['%.2f'%LBJ_YSI['a'],'%.2f'%LBJ_YSI['b'],'%.2f'%LBJ_YSI['r2'],'%.2f'%LBJ_YSI['pearson'],'%.2f'%LBJ_YSI['spearman'],'%.2f'%LBJ_YSI['rmse']]
    ## DAM TS3000
    DAM_TS3K = linearfunction(T_SSC_DAM_TS3K[1]['T-NTU'],T_SSC_DAM_TS3K[1]['SSC (mg/L)'])
    dam_ts3k = ['%.2f'%DAM_TS3K['a'],'%.2f'%DAM_TS3K['b'],'%.2f'%DAM_TS3K['r2'],'%.2f'%DAM_TS3K['pearson'],'%.2f'%DAM_TS3K['spearman'],'%.2f'%DAM_TS3K['rmse']]
    ## DAM YSI
    DAM_YSI = linearfunction(T_SSC_DAM_YSI[1]['T-NTU'],T_SSC_DAM_YSI[1]['SSC (mg/L)'])
    dam_ysi = ['%.2f'%DAM_YSI['a'],'%.2f'%DAM_YSI['b'],'%.2f'%DAM_YSI['r2'],'%.2f'%DAM_YSI['pearson'],'%.2f'%DAM_YSI['spearman'],'%.2f'%DAM_YSI['rmse']]    
    
    ## NTU
    ## LBJ OBS
    LBJ_OBS_2013 = linearfunction(T_SSC_LBJ_OBSa[1]['T-NTU'],T_SSC_LBJ_OBSa[1]['SSC (mg/L)'])
    lbj_obs_2013 = ['%.2f'%LBJ_OBS_2013['a'],'%.2f'%LBJ_OBS_2013['b'],'%.2f'%LBJ_OBS_2013['r2'],'%.2f'%LBJ_OBS_2013['pearson'],'%.2f'%LBJ_OBS_2013['spearman'],'%.2f'%LBJ_OBS_2013['rmse']]    

    LBJ_OBS_2014 = linearfunction(T_SSC_LBJ_OBSb[1]['T-NTU'],T_SSC_LBJ_OBSb[1]['SSC (mg/L)'])
    lbj_obs_2014 = ['%.2f'%LBJ_OBS_2014['a'],'%.2f'%LBJ_OBS_2014['b'],'%.2f'%LBJ_OBS_2014['r2'],'%.2f'%LBJ_OBS_2014['pearson'],'%.2f'%LBJ_OBS_2014['spearman'],'%.2f'%LBJ_OBS_2014['rmse']]    

    ## QUARRY OBS
    QUARRY_OBS = linearfunction(T_SSC_QUARRY_OBS[1]['T-NTU'],T_SSC_QUARRY_OBS[1]['SSC (mg/L)'])
    qua_obs = ['%.2f'%QUARRY_OBS['a'],'%.2f'%QUARRY_OBS['b'],'%.2f'%QUARRY_OBS['r2'],'%.2f'%QUARRY_OBS['pearson'],'%.2f'%QUARRY_OBS['spearman'],'%.2f'%QUARRY_OBS['rmse']]    

    nrows, ncols = 3,6
    hcell, wcell=0.3,1
    hpad, wpad = 1,1
    fig = plt.figure(figsize=(ncols*wcell+wpad,nrows*hcell+hpad)) 
    coeff = fig.add_subplot(111)
    coeff.patch.set_visible(False), coeff.axis('off')
    coeff.xaxis.set_visible(False), coeff.yaxis.set_visible(False) 
    coeff.table(cellText = [lab,lbj_ysi,lbj_obs_2013,lbj_obs_2014,qua_obs,dam_ts3k,dam_ysi],rowLabels=['Lab','VILL-YSI','VILL-OBS-2013','VILL-OBS-2014','QUA-OBS','FOR-TS3K','FOR-YSI'],colLabels=[r'$\alpha$',r'$\beta$',r'$r^2$',"Pearson's","Spearman's",'RMSE'],loc='center left')
    
    plt.suptitle('Paramters for Turbidity to Suspended Sediment Concetration Rating Curves',fontsize=12)    
    
    plt.tight_layout()
    plt.subplots_adjust(left=0.2)
    if show==True:
        plt.show()
    return
plotNTUratingstable(show=True,save=False)


def plotNTUratings(plot_param_table=True,show=False,log=False,save=False,lwidth=0.3,ms=10):
    #fig, (lab,ysi,obs) = plt.subplots(1,3,sharex=True,sharey=True,) 
    fig =plt.figure(figsize=(8,6))
    if plot_param_table==False:
        ysi = plt.subplot2grid((1,2),(0,0))
        obs = plt.subplot2grid((1,2),(0,1))
    if plot_param_table==True:
        ysi = plt.subplot2grid((2,2),(0,0))
        obs = plt.subplot2grid((2,2),(0,1))
        param_table = plt.subplot2grid((2,3),(1,0),colspan=2)
    xy = np.linspace(0,2000)
    mpl.rc('lines',markersize=ms,linewidth=lwidth)
    dotsize=50
    ## Grab Samples: LBJ-YSI, DAM-TS3k, DAM-YSI
    ysi.scatter(T_SSC_LBJ_YSI[1]['T-NTU'],T_SSC_LBJ_YSI[1]['SSC (mg/L)'],s=dotsize,color='r',marker='o',label='VILLAGE-YSI',edgecolors='grey')
    ysi.scatter(T_SSC_DAM_TS3K[1]['T-NTU'],T_SSC_DAM_TS3K[1]['SSC (mg/L)'],s=dotsize,color='g',marker='o',label='FOREST-TS3K',edgecolors='grey')
    ysi.scatter(T_SSC_DAM_YSI[1]['T-NTU'],T_SSC_DAM_YSI[1]['SSC (mg/L)'],s=dotsize,color='g',marker='v',label='FOREST-YSI',edgecolors='grey')
    ## NTU ratings LBJ-YSI, DAM-YSI, DAM-TS3K  
    ysi.plot(xy,xy*LBJ_YSI_rating.beta[0],ls='-',c='r',label='VILLAGE-YSI rating')
    #ysi.plot(xy,xy*DAM_TS3Krating.beta[0]+DAM_TS3Krating.beta[1],ls='-',c='g',label='FOREST-TS3K rating')
    ysi.plot(xy,xy*DAM_YSI_rating.beta[0],ls='--',c='g',label='FOREST-YSI rating')
    ## Format OBS
    ysi.grid(True), ysi.set_xlim(-5,4000), ysi.set_ylim(0,4000), ysi.set_ylabel('SSC (mg/L)'),ysi.set_xlabel('Turbidity (NTU)'),ysi.legend(fancybox=True,ncol=1,loc='best')
    ## NTU LBJ-OBS, QUARRY-OBS
    obs.scatter(T_SSC_LBJ_OBSa[1]['T-NTU'],T_SSC_LBJ_OBSa[1]['SSC (mg/L)'],s=dotsize,color='y',marker='.',label='VILLAGE-OBS-2013',edgecolors='grey')
    obs.plot(xy,xy*LBJ_OBSa_rating.beta[0],ls='-',c='y',label='VILLAGE-OBS-2013 rating')
    
    obs.scatter(T_SSC_LBJ_OBSb[1]['T-NTU'],T_SSC_LBJ_OBSb[1]['SSC (mg/L)'],s=dotsize,color='r',marker='.',label='VILLAGE-OBS-2014',edgecolors='grey')
    obs.plot(xy,xy*LBJ_OBSb_rating.beta[0],ls='-',c='r',label='VILLAGE-OBS-2014 rating')

    obs.scatter(T_SSC_QUARRY_OBS[1]['T-NTU'],T_SSC_QUARRY_OBS[1]['SSC (mg/L)'],s=dotsize,color='grey',marker='.',label='QUARRY-OBS',edgecolors='grey')
    obs.plot(xy,xy*QUARRY_OBS_rating.beta[0],ls='-',c='grey',label='QUARRY-OBS rating')

    ## Format NTU
    obs.grid(True), obs.set_xlabel('Turbidity (NTU)'), obs.legend(fancybox=True,ncol=2)
    obs.set_xlim(-5,4000), obs.set_ylim(0,4000),
    #labelindex_subplot(ts3k,T_SSC_LBJ_OBS[1].index,T_SSC_LBJ_OBS[1]['LBJ-OBS-NTU'],T_SSC_LBJ_OBS[1]['SSC (mg/L)'])    
    #labelindex_subplot(ts3k,T_SSC_LBJ_YSI[1].index,T_SSC_LBJ_YSI[1]['LBJ-YSI-NTU'],T_SSC_LBJ_OBS[1]['SSC (mg/L)'])
    title = 'Turbidity to Suspended Sediment Concetration Rating Curves'
    #plt.suptitle(title,fontsize=16) 
    ## TABLE
    if plot_param_table == True:
        ## NTU
        LAB = linearfunction(SSC[SSC['Location']=='LBJ']['NTU'],SSC[SSC['Location']=='LBJ']['SSC (mg/L)'])
        LBJ_YSI=linearfunction(T_SSC_LBJ_YSI[1]['T-NTU'],T_SSC_LBJ_YSI[1]['SSC (mg/L)'])
        DAM_TS3K = linearfunction(T_SSC_DAM_TS3K[1]['T-NTU'],T_SSC_DAM_TS3K[1]['SSC (mg/L)'])
        DAM_YSI = linearfunction(T_SSC_DAM_YSI[1]['T-NTU'],T_SSC_DAM_YSI[1]['SSC (mg/L)'])
        ## NTU
        LBJ_OBS_2013 = linearfunction(T_SSC_LBJ_OBSa[1]['T-NTU'],T_SSC_LBJ_OBSa[1]['SSC (mg/L)'])
        LBJ_OBS_2014 = linearfunction(T_SSC_LBJ_OBSb[1]['T-NTU'],T_SSC_LBJ_OBSb[1]['SSC (mg/L)'])
        QUA_OBS = linearfunction(T_SSC_QUARRY_OBS[1]['T-NTU'],T_SSC_QUARRY_OBS[1]['SSC (mg/L)'])        
        ## ROW/COLUMN Data
        lab = ['%.2f'%LAB['a'],'%.2f'%LAB['b'],'%.2f'%LAB['r2'],'%.2f'%LAB['pearson'],'%.2f'%LAB['spearman'],'%.2f'%LAB['rmse']]
        lbj_ysi = ['%.2f'%LBJ_YSI['a'],'%.2f'%LBJ_YSI['b'],'%.2f'%LBJ_YSI['r2'],'%.2f'%LBJ_YSI['pearson'],'%.2f'%LBJ_YSI['spearman'],'%.2f'%LBJ_YSI['rmse']]
        lbj_obs_2013 = ['%.2f'%LBJ_OBS_2013['a'],'%.2f'%LBJ_OBS_2013['b'],'%.2f'%LBJ_OBS_2013['r2'],'%.2f'%LBJ_OBS_2013['pearson'],'%.2f'%LBJ_OBS_2013['spearman'],'%.2f'%LBJ_OBS_2013['rmse']]    
        lbj_obs_2014 = ['%.2f'%LBJ_OBS_2014['a'],'%.2f'%LBJ_OBS_2014['b'],'%.2f'%LBJ_OBS_2014['r2'],'%.2f'%LBJ_OBS_2014['pearson'],'%.2f'%LBJ_OBS_2014['spearman'],'%.2f'%LBJ_OBS_2014['rmse']]    
        qua_obs = ['%.2f'%QUA_OBS['a'],'%.2f'%QUA_OBS['b'],'%.2f'%QUA_OBS['r2'],'%.2f'%QUA_OBS['pearson'],'%.2f'%QUA_OBS['spearman'],'%.2f'%QUA_OBS['rmse']]    
        dam_ts3k = ['%.2f'%DAM_TS3K['a'],'%.2f'%DAM_TS3K['b'],'%.2f'%DAM_TS3K['r2'],'%.2f'%DAM_TS3K['pearson'],'%.2f'%DAM_TS3K['spearman'],'%.2f'%DAM_TS3K['rmse']]
        dam_ysi = ['%.2f'%DAM_YSI['a'],'%.2f'%DAM_YSI['b'],'%.2f'%DAM_YSI['r2'],'%.2f'%DAM_YSI['pearson'],'%.2f'%DAM_YSI['spearman'],'%.2f'%DAM_YSI['rmse']]    
        ## Plot Table
        param_table.patch.set_visible(False), param_table.axis('off')
        param_table.xaxis.set_visible(False), param_table.yaxis.set_visible(False) 
        param_table.table(cellText = [lab,lbj_ysi,lbj_obs_2013,lbj_obs_2014,qua_obs,dam_ts3k,dam_ysi],rowLabels=['Lab','VILL-YSI','VILL-OBS-2013','VILL-OBS-2014','QUA-OBS','FOR-TS3K','FOR-YSI'],colLabels=[r'$\alpha$',r'$\beta$',r'$r^2$',"Pearson's","Spearman's",'RMSE'],loc='center left')
        ## Adjust subplots    
        #plt.subplots_adjust(left=0.08, bottom=0,hspace=0.01)
    else:
        plt.tight_layout(pad=0.1)
        pass
    show_plot(show)
    return
plotNTUratings(plot_param_table=True,show=True,log=False,save=False,lwidth=0.5,ms=20)


def plotNTUratings_no_int(plot_param_table=True,show=False,log=False,save=False,lwidth=0.3,ms=10):
    #fig, (lab,ysi,obs) = plt.subplots(1,3,sharex=True,sharey=True,) 
    fig =plt.figure(figsize=(14,6))
    lab = plt.subplot2grid((2,3),(0,0))
    ysi = plt.subplot2grid((2,3),(0,1))
    obs = plt.subplot2grid((2,3),(0,2))
    param_table = plt.subplot2grid((2,3),(1,0),colspan=3)
    
    xy = np.linspace(0,2000)
    mpl.rc('lines',markersize=ms,linewidth=lwidth)
    dotsize=50
    
    ## All Samples LAB
    lab.scatter(SSC['NTU'],SSC['SSC (mg/L)'],s=dotsize,color='b',marker='v',label='LAB',edgecolors='grey')
    lab.plot(xy,xy*T_SSC_Lab.beta[0],ls='-',c='b',label='LAB')
    lab.grid(True),lab.set_ylabel('SSC (mg/L)'),lab.set_xlabel('Turbidity (NTU)'),lab.legend(fancybox=True,ncol=2)
    lab.set_xlim(-5,4000), lab.set_ylim(0,4000)
    ## Grab Samples: LBJ-YSI, DAM-TS3k, DAM-YSI
    ysi.scatter(T_SSC_LBJ_YSI[1]['LBJ-YSI-NTU'],T_SSC_LBJ_YSI[1]['SSC (mg/L)'],s=dotsize,color='r',marker='o',label='VILLAGE-YSI',edgecolors='grey')
    ysi.scatter(T_SSC_DAM_TS3K[1]['DAM-TS3K-NTU'],T_SSC_DAM_TS3K[1]['SSC (mg/L)'],s=dotsize,color='g',marker='o',label='FOREST-TS3K',edgecolors='grey')
    ysi.scatter(T_SSC_DAM_YSI[1]['DAM-YSI-NTU'],T_SSC_DAM_YSI[1]['SSC (mg/L)'],s=dotsize,color='g',marker='v',label='FOREST-YSI',edgecolors='grey')
    ## NTU ratings LBJ-YSI, DAM-YSI, DAM-TS3K  
    ysi.plot(xy,xy*LBJ_YSI_rating.beta[0],ls='-',c='r',label='VILLAGE-YSI rating')
    #ysi.plot(xy,xy*DAM_TS3Krating.beta[0]+DAM_TS3Krating.beta[1],ls='-',c='g',label='FOREST-TS3K rating')
    ysi.plot(xy,xy*DAM_YSI_rating.beta[0],ls='--',c='g',label='FOREST-YSI rating')
    ## Format OBS
    ysi.grid(True), ysi.set_xlim(-5,4000), ysi.set_ylim(0,4000), ysi.set_ylabel('SSC (mg/L)'),ysi.set_xlabel('Turbidity (NTU)'),ysi.legend(fancybox=True,ncol=1,loc='best')
    ## NTU LBJ-OBS, QUARRY-OBS
    obs.scatter(T_SSC_LBJ_OBSa[1]['LBJ-OBS-NTU'],T_SSC_LBJ_OBSa[1]['SSC (mg/L)'],s=dotsize,color='y',marker='.',label='VILLAGE-OBS-2013',edgecolors='grey')
    obs.plot(xy,xy*LBJ_OBSa_rating.beta[0],ls='-',c='y',label='VILLAGE-OBS-2013 rating')
    
    obs.scatter(T_SSC_LBJ_OBSb[1]['LBJ-OBS-NTU'],T_SSC_LBJ_OBSb[1]['SSC (mg/L)'],s=dotsize,color='r',marker='.',label='VILLAGE-OBS-2014',edgecolors='grey')
    obs.plot(xy,xy*LBJ_OBSb_rating.beta[0],ls='-',c='r',label='VILLAGE-OBS-2014 rating')

    obs.scatter(T_SSC_QUARRY_OBS[1]['QUARRY-OBS-NTU'],T_SSC_QUARRY_OBS[1]['SSC (mg/L)'],s=dotsize,color='grey',marker='.',label='QUARRY-OBS',edgecolors='grey')
    obs.plot(xy,xy*QUARRY_OBS_rating.beta[0],ls='-',c='grey',label='QUARRY-OBS rating')

    ## Format NTU
    obs.grid(True), obs.set_xlabel('Turbidity (NTU)'), obs.legend(fancybox=True,ncol=2)
    obs.set_xlim(-5,4000), obs.set_ylim(0,4000),
    #labelindex_subplot(ts3k,T_SSC_LBJ_OBS[1].index,T_SSC_LBJ_OBS[1]['LBJ-OBS-NTU'],T_SSC_LBJ_OBS[1]['SSC (mg/L)'])    
    #labelindex_subplot(ts3k,T_SSC_LBJ_YSI[1].index,T_SSC_LBJ_YSI[1]['LBJ-YSI-NTU'],T_SSC_LBJ_OBS[1]['SSC (mg/L)'])
    title = 'Turbidity to Suspended Sediment Concetration Rating Curves'
    #plt.suptitle(title,fontsize=16) 
    ## TABLE
    if plot_param_table == True:
        ## NTU
        LAB = linearfunction(SSC[SSC['Location']=='LBJ']['NTU'],SSC[SSC['Location']=='LBJ']['SSC (mg/L)'])
        LBJ_YSI=linearfunction(T_SSC_LBJ_YSI[1]['LBJ-YSI-NTU'],T_SSC_LBJ_YSI[1]['SSC (mg/L)'])
        DAM_TS3K = linearfunction(T_SSC_DAM_TS3K[1]['DAM-TS3K-NTU'],T_SSC_DAM_TS3K[1]['SSC (mg/L)'])
        DAM_YSI = linearfunction(T_SSC_DAM_YSI[1]['DAM-YSI-NTU'],T_SSC_DAM_YSI[1]['SSC (mg/L)'])
        ## NTU
        LBJ_OBS_2013 = linearfunction(T_SSC_LBJ_OBSa[1]['LBJ-OBS-NTU'],T_SSC_LBJ_OBSa[1]['SSC (mg/L)'])
        LBJ_OBS_2014 = linearfunction(T_SSC_LBJ_OBSb[1]['LBJ-OBS-NTU'],T_SSC_LBJ_OBSb[1]['SSC (mg/L)'])
        QUA_OBS = linearfunction(T_SSC_QUARRY_OBS[1]['QUARRY-OBS-NTU'],T_SSC_QUARRY_OBS[1]['SSC (mg/L)'])        
        ## ROW/COLUMN Data
        lab = ['%.2f'%LAB['a'],'%.2f'%LAB['b'],'%.2f'%LAB['r2'],'%.2f'%LAB['pearson'],'%.2f'%LAB['spearman'],'%.2f'%LAB['rmse']]
        lbj_ysi = ['%.2f'%LBJ_YSI['a'],'%.2f'%LBJ_YSI['b'],'%.2f'%LBJ_YSI['r2'],'%.2f'%LBJ_YSI['pearson'],'%.2f'%LBJ_YSI['spearman'],'%.2f'%LBJ_YSI['rmse']]
        lbj_obs_2013 = ['%.2f'%LBJ_OBS_2013['a'],'%.2f'%LBJ_OBS_2013['b'],'%.2f'%LBJ_OBS_2013['r2'],'%.2f'%LBJ_OBS_2013['pearson'],'%.2f'%LBJ_OBS_2013['spearman'],'%.2f'%LBJ_OBS_2013['rmse']]    
        lbj_obs_2014 = ['%.2f'%LBJ_OBS_2014['a'],'%.2f'%LBJ_OBS_2014['b'],'%.2f'%LBJ_OBS_2014['r2'],'%.2f'%LBJ_OBS_2014['pearson'],'%.2f'%LBJ_OBS_2014['spearman'],'%.2f'%LBJ_OBS_2014['rmse']]    
        qua_obs = ['%.2f'%QUA_OBS['a'],'%.2f'%QUA_OBS['b'],'%.2f'%QUA_OBS['r2'],'%.2f'%QUA_OBS['pearson'],'%.2f'%QUA_OBS['spearman'],'%.2f'%QUA_OBS['rmse']]    
        dam_ts3k = ['%.2f'%DAM_TS3K['a'],'%.2f'%DAM_TS3K['b'],'%.2f'%DAM_TS3K['r2'],'%.2f'%DAM_TS3K['pearson'],'%.2f'%DAM_TS3K['spearman'],'%.2f'%DAM_TS3K['rmse']]
        dam_ysi = ['%.2f'%DAM_YSI['a'],'%.2f'%DAM_YSI['b'],'%.2f'%DAM_YSI['r2'],'%.2f'%DAM_YSI['pearson'],'%.2f'%DAM_YSI['spearman'],'%.2f'%DAM_YSI['rmse']]    
        ## Plot Table
        param_table.patch.set_visible(False), param_table.axis('off')
        param_table.xaxis.set_visible(False), param_table.yaxis.set_visible(False) 
        param_table.table(cellText = [lab,lbj_ysi,lbj_obs_2013,lbj_obs_2014,qua_obs,dam_ts3k,dam_ysi],rowLabels=['Lab','VILL-YSI','VILL-OBS-2013','VILL-OBS-2014','QUA-OBS','FOR-TS3K','FOR-YSI'],colLabels=[r'$\alpha$',r'$\beta$',r'$r^2$',"Pearson's","Spearman's",'RMSE'],loc='center left')
        ## Adjust subplots    
        plt.subplots_adjust(left=0.08, bottom=0,hspace=0.01)
    else:
        plt.tight_layout()
    
    plt.draw()
    if show==True:
        plt.show()
    return
#plotNTUratings_no_int(plot_param_table=True,show=True,log=False,save=True,lwidth=0.5,ms=20)    
