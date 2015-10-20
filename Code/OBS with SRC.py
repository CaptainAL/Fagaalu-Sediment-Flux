# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 17:05:17 2015

@author: Alex
"""

#OBS with SRC


## PLOT T-SSC rating for OBSa (BS and SS Avg only)
def OBSa_compare_ratings(df,df_SRC,SSC_loc,plot_SRC=True,Use_All_SSC=False,storm_samples_only=False,show=True,save=False,filename='',sub_plot_count=0):
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
    ss_average=NTU_SSCrating(SSC,df['Turb_SS_Avg'],location=SSC_loc,T_interval='5Min',Intercept=False,log=False)
    ss_avg.scatter(ss_average[1]['T-NTU'],ss_average[1]['SSC (mg/L)'],c='k')
    ss_avg.plot(xy,xy*ss_average[0].beta[0],ls='-',c='k',label='SS_Avg '+r'$r^2$'+"%.2f"%ss_average[0].r2)   
    #ss_avg.set_title(SSC_loc+' SS_Avg '+r'$r^2=$'+"%.2f"%ss_average[0].r2) 
    ss_avg.set_xlabel('SS Avg')
    ## SS Mean SRC
    #ss_mean_SRC = pd.ols(y=df_SRC['SSC(mg/L)'],x=df_SRC['SS_Mean'],intercept=False)
    #ss_avg.scatter(df_SRC['SS_Mean'],df_SRC['SSC(mg/L)'],c='grey')
    #ss_avg.plot(xy,xy*ss_mean_SRC.beta[0],ls='--',c='grey',label='SS_Mean_SRC'+r'$r^2$'+"%.2f"%ss_mean_SRC.r2)
    ss_avg.legend()
    plt.tight_layout(pad=0.1)
    for ax in fig.axes:
        ax.locator_params(nbins=4)
        ax.set_xlim(0,max_x), ax.set_ylim(0,max_y)
        
    #letter_subplots(fig,x=0.1,y=0.95,vertical='top',horizontal='right',Color='k',font_size=10,font_weight='bold')
    show_plot(show)
    savefig(save,filename)
    return
OBSa_compare_ratings(df=LBJ_OBSa,df_SRC=LBJ_SRC,SSC_loc='LBJ',plot_SRC=True,Use_All_SSC=False,storm_samples_only=False,show=True,save=False,filename='')  
#OBSa_compare_ratings(df=LBJ_OBSa,df_SRC=LBJ_SRC,SSC_loc='LBJ',Use_All_SSC=False,storm_samples_only=True,show=True,save=False,filename='')  

## PLOT T-SSC ratings with all parameters (BS and SS Mean, Median, Min, Max)
def OBSb_compare_ratings(df,df_SRC,SSC_loc,plot_SRC=False,Use_All_SSC=False,storm_samples_only=True,show=True,save=False,filename='',sub_plot_count=0):
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
    bs_median=NTU_SSCrating(SSC,df['Turb_BS_Median'],location=SSC_loc,T_interval='15Min',Intercept=False,log=False)
    bs_med.scatter(bs_median[1]['T-NTU'],bs_median[1]['SSC (mg/L)'],c='k')
    bs_med.plot(xy,xy*bs_median[0].beta[0],ls='-',c='k',label='BS_Median'+r'$r^2$'+"%.2f"%bs_median[0].r2)
    #bs_med.set_title('BS_Median '+r'$r^2=$'+"%.2f"%bs_median[0].r2)
    bs_med.set_ylabel('SSC (mg/L)'),bs_med.set_xlabel('BS Median') 
    ## BS Mean
    bs_mean=NTU_SSCrating(SSC,df['Turb_BS_Mean'],location=SSC_loc,T_interval='15Min',Intercept=False,log=False)
    bs_mea.scatter(bs_mean[1]['T-NTU'],bs_mean[1]['SSC (mg/L)'],c='k')
    bs_mea.plot(xy,xy*bs_mean[0].beta[0],ls='-',c='k',label='BS_Mean'+r'$r^2$'+"%.2f"%bs_mean[0].r2)
    #bs_mea.set_title('BS_Mean '+r'$r^2=$'+"%.2f"%bs_mean[0].r2)  
    bs_mea.set_xlabel('BS Mean')
    ## BS Min
    bs_minimum=NTU_SSCrating(SSC,df['Turb_BS_Min'],location=SSC_loc,T_interval='15Min',Intercept=False,log=False)
    bs_min.scatter(bs_minimum[1]['T-NTU'],bs_minimum[1]['SSC (mg/L)'],c='k')
    bs_min.plot(xy,xy*bs_minimum[0].beta[0],ls='-',c='k',label='BS_Min'+r'$r^2$'+"%.2f"%bs_minimum[0].r2)
    #bs_min.set_title('BS_Min '+r'$r^2=$'+"%.2f"%bs_minimum[0].r2)
    bs_min.set_xlabel('BS Min')
    ## BS Max
    bs_maximum=NTU_SSCrating(SSC,df['Turb_BS_Max'],location=SSC_loc,T_interval='15Min',Intercept=False,log=False)
    bs_max.scatter(bs_maximum[1]['T-NTU'],bs_maximum[1]['SSC (mg/L)'],c='k')
    bs_max.plot(xy,xy*bs_maximum[0].beta[0],ls='-',c='k',label='BS_Max'+r'$r^2$'+"%.2f"%bs_maximum[0].r2)    
    #bs_max.set_title('BS_Max '+r'$r^2=$'+"%.2f"%bs_maximum[0].r2)    
    bs_max.set_xlabel('BS Max')
    ## SS Median
    ss_median=NTU_SSCrating(SSC,df['Turb_SS_Median'],location=SSC_loc,T_interval='15Min',Intercept=False,log=False)
    ss_med.scatter(ss_median[1]['T-NTU'],ss_median[1]['SSC (mg/L)'],c='k')
    ss_med.plot(xy,xy*ss_median[0].beta[0],ls='-',c='k',label='SS_Median'+r'$r^2$'+"%.2f"%ss_median[0].r2)
    #ss_med.set_title('SS_Median '+r'$r^2=$'+"%.2f"%ss_median[0].r2)
    ss_med.set_ylabel('SSC (mg/L)'),ss_med.set_xlabel('SS Median')
    ## SS Mean
    ss_mean=NTU_SSCrating(SSC,df['Turb_SS_Mean'],location=SSC_loc,T_interval='15Min',Intercept=False,log=False)
    ss_mea.scatter(ss_mean[1]['T-NTU'],ss_mean[1]['SSC (mg/L)'],c='k')
    ss_mea.plot(xy,xy*ss_mean[0].beta[0],ls='-',c='k',label='SS_Mean'+r'$r^2$'+"%.2f"%ss_mean[0].r2)
    #ss_mea.set_title('SS_Mean '+r'$r^2=$'+"%.2f"%ss_mean[0].r2)    
    ss_mea.set_xlabel('SS Mean')
    ## SS Min
    ss_minimum=NTU_SSCrating(SSC,df['Turb_SS_Min'],location=SSC_loc,T_interval='15Min',Intercept=False,log=False)
    ss_min.scatter(ss_minimum[1]['T-NTU'],ss_minimum[1]['SSC (mg/L)'],c='k')
    ss_min.plot(xy,xy*ss_minimum[0].beta[0],ls='-',c='k',label='SS_Min'+r'$r^2$'+"%.2f"%ss_minimum[0].r2)
    #ss_min.set_title('SS_Min '+r'$r^2=$'+"%.2f"%ss_minimum[0].r2)    
    ss_min.set_xlabel('SS Min')
    ## SS Max
    ss_maximum=NTU_SSCrating(SSC,df['Turb_SS_Max'],location=SSC_loc,T_interval='15Min',Intercept=False,log=False)
    ss_max.scatter(ss_maximum[1]['T-NTU'],ss_maximum[1]['SSC (mg/L)'],c='k')
    ss_max.plot(xy,xy*ss_maximum[0].beta[0],ls='-',c='k',label='SS_Max'+r'$r^2$'+"%.2f"%ss_maximum[0].r2)    
    #ss_max.set_title('SS_Max '+r'$r^2=$'+"%.2f"%ss_maximum[0].r2)
    ss_max.set_xlabel('SS Max')
    if plot_SRC==True:
        ## BS Median SRC
        bs_median_SRC = pd.ols(y=df_SRC['SSC(mg/L)'],x=df_SRC['BS_Median'],intercept=False)
        bs_med.scatter(df_SRC['BS_Median'],df_SRC['SSC(mg/L)'],c='grey')
        bs_med.plot(xy,xy*bs_median_SRC.beta[0],ls='--',c='grey',label='BS_Median_SRC'+r'$r^2$'+"%.2f"%bs_median_SRC.r2)
        ## BS Mean SRC
        bs_mean_SRC = pd.ols(y=df_SRC['SSC(mg/L)'],x=df_SRC['BS_Mean'],intercept=False)
        bs_mea.scatter(df_SRC['BS_Mean'],df_SRC['SSC(mg/L)'],c='grey')
        bs_mea.plot(xy,xy*bs_mean_SRC.beta[0],ls='--',c='grey',label='BS_Mean_SRC'+r'$r^2$'+"%.2f"%bs_mean_SRC.r2)
        ## BS Min SRC
        bs_min_SRC = pd.ols(y=df_SRC['SSC(mg/L)'],x=df_SRC['BS_Min'],intercept=False)
        bs_min.scatter(df_SRC['BS_Min'],df_SRC['SSC(mg/L)'],c='grey')
        bs_min.plot(xy,xy*bs_min_SRC.beta[0],ls='--',c='grey',label='BS_Min_SRC'+r'$r^2$'+"%.2f"%bs_min_SRC.r2)
        ## BS Max SRC
        bs_max_SRC = pd.ols(y=df_SRC['SSC(mg/L)'],x=df_SRC['BS_Max'],intercept=False)
        bs_max.scatter(df_SRC['BS_Max'],df_SRC['SSC(mg/L)'],c='grey')
        bs_max.plot(xy,xy*bs_max_SRC.beta[0],ls='--',c='grey',label='BS_Max_SRC'+r'$r^2$'+"%.2f"%bs_max_SRC.r2)
        ## SS Median SRC
        ss_median_SRC = pd.ols(y=df_SRC['SSC(mg/L)'],x=df_SRC['SS_Median'],intercept=False)
        ss_med.scatter(df_SRC['SS_Median'],df_SRC['SSC(mg/L)'],c='grey')
        ss_med.plot(xy,xy*ss_median_SRC.beta[0],ls='--',c='grey',label='SS_Median_SRC'+r'$r^2$'+"%.2f"%ss_median_SRC.r2)
        ## SS Mean SRC
        ss_mean_SRC = pd.ols(y=df_SRC['SSC(mg/L)'],x=df_SRC['SS_Mean'],intercept=False)
        ss_mea.scatter(df_SRC['SS_Mean'],df_SRC['SSC(mg/L)'],c='grey')
        ss_mea.plot(xy,xy*ss_mean_SRC.beta[0],ls='--',c='grey',label='SS_Mean_SRC'+r'$r^2$'+"%.2f"%ss_mean_SRC.r2)
        ## SS Min SRC
        ss_min_SRC = pd.ols(y=df_SRC['SSC(mg/L)'],x=df_SRC['SS_Min'],intercept=False)
        ss_min.scatter(df_SRC['SS_Min'],df_SRC['SSC(mg/L)'],c='grey')
        ss_min.plot(xy,xy*ss_min_SRC.beta[0],ls='--',c='grey',label='SS_Min_SRC'+r'$r^2$'+"%.2f"%ss_min_SRC.r2) 

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
#OBSb_compare_ratings(df=LBJ_OBSb,df_SRC=LBJ_SRC,SSC_loc='LBJ',plot_SRC=False,Use_All_SSC=True,storm_samples_only=False,show=True,save=False,filename='')  ## ALL SSC
#OBSb_compare_ratings(df=LBJ_OBSb,df_SRC=LBJ_SRC,SSC_loc='LBJ',Use_All_SSC=True,storm_samples_only=True,show=True,save=False,filename='')   ## ALL SSC, storm only
#OBSb_compare_ratings(df=LBJ_OBSb,df_SRC=LBJ_SRC,SSC_loc='LBJ',Use_All_SSC=False,storm_samples_only=False,show=True,save=False,filename='') ## Pre-mitigation
#OBSb_compare_ratings(df=LBJ_OBSb,df_SRC=LBJ_SRC,SSC_loc='LBJ',Use_All_SSC=False,storm_samples_only=True,show=True,save=False,filename='')## Pre-mitigation, storm only
## LBJ R2
#OBSb_compare_ratings(df=LBJ_OBSb,df_SRC=LBJ_SRC,SSC_loc='LBJ R2',Use_All_SSC=True,storm_samples_only=False)  
## QUARRY
#OBSb_compare_ratings(df=QUARRY_OBS,df_SRC=QUARRY_SRC,SSC_loc='R2',Use_All_SSC=True)   
