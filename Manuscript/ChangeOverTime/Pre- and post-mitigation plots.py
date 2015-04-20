# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 10:43:33 2015

@author: Alex
"""

def plotSSCboxplots_pre_and_post(withR2=False,log=False,show=False,save=False,filename=figdir+''):
    #mpl.rc('lines',markersize=300)
    fig, ((ax1,ax2),(ax3,ax4))=plt.subplots(2,2,figsize=(8,6),sharey=True)
    letter_subplots(fig,0.1,0.95,'top','right','k',font_size=10,font_weight='bold')
    
    ## Subset SSC
    ## Pre-mitigation baseflow
    SSC = SSC_dict['Pre-baseflow']
    LBJgrab = SSC[SSC['Location'].isin(['LBJ'])]
    QUARRYgrab =SSC[SSC['Location'].isin(['DT'])]
    DAMgrab = SSC[SSC['Location'].isin(['DAM'])]
    if withR2==True:
        ## Add samples from Autosampler at QUARRY
        print 'Adding R2 samples to QUARRY Grab (DT)'
        QUARRYgrab =SSC[SSC['Location'].isin(['DT','R2'])]
    elif withR2==False:
        QUARRYgrab =SSC[SSC['Location'].isin(['DT'])]  
    ## Compile
    GrabSamples = pd.concat([DAMgrab['SSC (mg/L)'].reset_index()['SSC (mg/L)'],QUARRYgrab['SSC (mg/L)'].reset_index()['SSC (mg/L)'],
                                 LBJgrab['SSC (mg/L)'].reset_index()['SSC (mg/L)']],ignore_index=True,axis=1)    
    GrabSamples.columns = ['DAM','QUARRY','LBJ']
    GrabSampleMeans = [DAMgrab['SSC (mg/L)'].mean(),QUARRYgrab['SSC (mg/L)'].mean(),LBJgrab['SSC (mg/L)'].mean()]
    GrabSampleVals = np.concatenate([DAMgrab['SSC (mg/L)'].values.tolist(),QUARRYgrab['SSC (mg/L)'].values.tolist(),LBJgrab['SSC (mg/L)'].values.tolist()])
    GrabSampleCategories = np.concatenate([[1]*len(DAMgrab['SSC (mg/L)']),[2]*len(QUARRYgrab['SSC (mg/L)']),[3]*len(LBJgrab['SSC (mg/L)'])])
    GrabSamples.columns = ['FG1','FG2','FG3']
    bp1 = GrabSamples.boxplot(ax=ax1)
    ax1.scatter(GrabSampleCategories,GrabSampleVals,s=40,marker='+',c='grey',label='SSC (mg/L)')    
    
    ## Subset SSC
    ## Pre-mitigation stormflow
    SSC = SSC_dict['Pre-storm']
    LBJgrab = SSC[SSC['Location'].isin(['LBJ'])]
    QUARRYgrab =SSC[SSC['Location'].isin(['DT'])]
    DAMgrab = SSC[SSC['Location'].isin(['DAM'])]
    if withR2==True:
        ## Add samples from Autosampler at QUARRY
        print 'Adding R2 samples to QUARRY Grab (DT)'
        QUARRYgrab =SSC[SSC['Location'].isin(['DT','R2'])]
    elif withR2==False:
        QUARRYgrab =SSC[SSC['Location'].isin(['DT'])]  
    ## Compile
    GrabSamples = pd.concat([DAMgrab['SSC (mg/L)'].reset_index()['SSC (mg/L)'],QUARRYgrab['SSC (mg/L)'].reset_index()['SSC (mg/L)'],
                                 LBJgrab['SSC (mg/L)'].reset_index()['SSC (mg/L)']],ignore_index=True,axis=1)    
    GrabSamples.columns = ['DAM','QUARRY','LBJ']
    GrabSampleMeans = [DAMgrab['SSC (mg/L)'].mean(),QUARRYgrab['SSC (mg/L)'].mean(),LBJgrab['SSC (mg/L)'].mean()]
    GrabSampleVals = np.concatenate([DAMgrab['SSC (mg/L)'].values.tolist(),QUARRYgrab['SSC (mg/L)'].values.tolist(),LBJgrab['SSC (mg/L)'].values.tolist()])
    GrabSampleCategories = np.concatenate([[1]*len(DAMgrab['SSC (mg/L)']),[2]*len(QUARRYgrab['SSC (mg/L)']),[3]*len(LBJgrab['SSC (mg/L)'])])
    GrabSamples.columns = ['FG1','FG2','FG3']    
    bp3 = GrabSamples.boxplot(ax=ax3)
    ax3.scatter(GrabSampleCategories,GrabSampleVals,s=40,marker='+',c='grey',label='SSC (mg/L)')    
    
    ## Format plots
    plt.setp(bp1['boxes'], color='black'), plt.setp(bp3['boxes'], color='black')
    plt.setp(bp1['whiskers'], color='black'), plt.setp(bp3['whiskers'], color='black')
    plt.setp(bp1['fliers'], color='grey', marker='+'), plt.setp(bp3['fliers'], color='grey', marker='+') 
    plt.setp(bp1['medians'], color='black', marker='+'), plt.setp(bp3['medians'], color='black', marker='+') 

    ## Add Mean values
    ax1.scatter([1,2,3],GrabSampleMeans,s=40,color='k',label='Mean SSC (mg/L)')
    ax3.scatter([1,2,3],GrabSampleMeans,s=40,color='k',label='Mean SSC (mg/L)')    
    
    ######################    
    ######################
    
    ## Subset SSC
    ## Post-mitigation baseflow
    SSC = SSC_dict['Post-baseflow']
    LBJgrab = SSC[SSC['Location'].isin(['LBJ'])]
    QUARRYgrab =SSC[SSC['Location'].isin(['DT'])]
    DAMgrab = SSC[SSC['Location'].isin(['DAM'])]
    if withR2==True:
        ## Add samples from Autosampler at QUARRY
        print 'Adding R2 samples to QUARRY Grab (DT)'
        QUARRYgrab =SSC[SSC['Location'].isin(['DT','R2'])]
    elif withR2==False:
        QUARRYgrab =SSC[SSC['Location'].isin(['DT'])]  
    ## Compile
    GrabSamples = pd.concat([DAMgrab['SSC (mg/L)'].reset_index()['SSC (mg/L)'],QUARRYgrab['SSC (mg/L)'].reset_index()['SSC (mg/L)'],
                                 LBJgrab['SSC (mg/L)'].reset_index()['SSC (mg/L)']],ignore_index=True,axis=1)    
    GrabSamples.columns = ['DAM','QUARRY','LBJ']
    GrabSampleMeans = [DAMgrab['SSC (mg/L)'].mean(),QUARRYgrab['SSC (mg/L)'].mean(),LBJgrab['SSC (mg/L)'].mean()]
    GrabSampleVals = np.concatenate([DAMgrab['SSC (mg/L)'].values.tolist(),QUARRYgrab['SSC (mg/L)'].values.tolist(),LBJgrab['SSC (mg/L)'].values.tolist()])
    GrabSampleCategories = np.concatenate([[1]*len(DAMgrab['SSC (mg/L)']),[2]*len(QUARRYgrab['SSC (mg/L)']),[3]*len(LBJgrab['SSC (mg/L)'])])
    GrabSamples.columns = ['FG1','FG2','FG3']
    bp2 = GrabSamples.boxplot(ax=ax2)
    ax2.scatter(GrabSampleCategories,GrabSampleVals,s=40,marker='+',c='grey',label='SSC (mg/L)')    
    
    ## Subset SSC
    ## Post-mitigation stormflow
    SSC = SSC_dict['Post-storm']
    LBJgrab = SSC[SSC['Location'].isin(['LBJ'])]
    QUARRYgrab =SSC[SSC['Location'].isin(['DT'])]
    DAMgrab = SSC[SSC['Location'].isin(['DAM'])]
    if withR2==True:
        ## Add samples from Autosampler at QUARRY
        print 'Adding R2 samples to QUARRY Grab (DT)'
        QUARRYgrab =SSC[SSC['Location'].isin(['DT','R2'])]
    elif withR2==False:
        QUARRYgrab =SSC[SSC['Location'].isin(['DT'])]  
    ## Compile
    GrabSamples = pd.concat([DAMgrab['SSC (mg/L)'].reset_index()['SSC (mg/L)'],QUARRYgrab['SSC (mg/L)'].reset_index()['SSC (mg/L)'],
                                 LBJgrab['SSC (mg/L)'].reset_index()['SSC (mg/L)']],ignore_index=True,axis=1)    
    GrabSamples.columns = ['DAM','QUARRY','LBJ']
    GrabSampleMeans = [DAMgrab['SSC (mg/L)'].mean(),QUARRYgrab['SSC (mg/L)'].mean(),LBJgrab['SSC (mg/L)'].mean()]
    GrabSampleVals = np.concatenate([DAMgrab['SSC (mg/L)'].values.tolist(),QUARRYgrab['SSC (mg/L)'].values.tolist(),LBJgrab['SSC (mg/L)'].values.tolist()])
    GrabSampleCategories = np.concatenate([[1]*len(DAMgrab['SSC (mg/L)']),[2]*len(QUARRYgrab['SSC (mg/L)']),[3]*len(LBJgrab['SSC (mg/L)'])])
    GrabSamples.columns = ['FG1','FG2','FG3']    
    bp4 = GrabSamples.boxplot(ax=ax4)
    ax4.scatter(GrabSampleCategories,GrabSampleVals,s=40,marker='+',c='grey',label='SSC (mg/L)')    
    
    ## Format plots
    plt.setp(bp2['boxes'], color='black'), plt.setp(bp4['boxes'], color='black')
    plt.setp(bp2['whiskers'], color='black'), plt.setp(bp4['whiskers'], color='black')
    plt.setp(bp2['fliers'], color='grey', marker='+'), plt.setp(bp4['fliers'], color='grey', marker='+') 
    plt.setp(bp2['medians'], color='black', marker='+'), plt.setp(bp4['medians'], color='black', marker='+') 

    ## Add Mean values
    ax2.scatter([1,2,3],GrabSampleMeans,s=40,color='k',label='Mean SSC (mg/L)')
    ax4.scatter([1,2,3],GrabSampleMeans,s=40,color='k',label='Mean SSC (mg/L)')      
    
    
    #ax2.legend()    
    if log==True:
        ax1.set_yscale('log'), ax2.set_yscale('log'), ax3.set_yscale('log'), ax4.set_yscale('log')     
    ax1.set_ylabel('SSC (mg/L)'),ax3.set_ylabel('SSC (mg/L)'),ax3.set_xlabel('Location'),ax4.set_xlabel('Location')
    
    ax1.text(.5,.9,'Pre-mitigation Baseflow',horizontalalignment='center',transform=ax1.transAxes)
    ax2.text(.5,.9,'Post-mitigation Baseflow',horizontalalignment='center',transform=ax2.transAxes)
    ax3.text(.5,.9,'Pre-mitigation Stormflow',horizontalalignment='center',transform=ax3.transAxes)
    ax4.text(.5,.9,'Post-mitigation Stormflow',horizontalalignment='center',transform=ax4.transAxes)

    plt.tight_layout(pad=0.1)
    show_plot(show)
    savefig(save,filename)
    return
## Premitigation
#plotSSCboxplots_pre_and_post(withR2=False,log=True,show=True,save=False,filename='')

def plotQvsC_pre_and_post(storm_samples_only=False,ms=6,show=False,log=False,save=False,filename=figdir+''):  
    fig, ((ax1,ax2,ax3),(ax4,ax5,ax6)) = plt.subplots(2,3,figsize=(8,6))
    letter_subplots(fig,0.1,0.95,'top','right','k',font_size=10,font_weight='bold')
    #
    mpl.rc('lines',markersize=ms)
    mpl.rc('grid',alpha=0.0)     
    
    ## Pre-mitigation
    SSC = SSC_dict['Pre-ALL']
    ## Append Discharge (Q) data
    dam_ssc = pd.DataFrame(SSC[SSC['Location']=='DAM']['SSC (mg/L)'])
    dam_ssc['Q']=DAM['Q']
    dam_ssc = dam_ssc.dropna()
    quarry_ssc = pd.DataFrame(SSC[SSC['Location'].isin(['DT','R2'])]['SSC (mg/L)'])
    quarry_ssc['Q']=QUARRY['Q']
    quarry_ssc =quarry_ssc.dropna()
    lbj_ssc = pd.DataFrame(SSC[SSC['Location']=='LBJ']['SSC (mg/L)'])
    lbj_ssc['Q']=LBJ['Q']
    lbj_ssc=lbj_ssc.dropna()
    ## Subset by year
    dam_ssc2012,dam_ssc2013,dam_ssc2014 = dam_ssc[start2012:stop2012],dam_ssc[start2013:stop2013],dam_ssc[start2014:stop2014]
    quarry2012,quarry2013,quarry2014 = quarry_ssc[start2012:stop2012],quarry_ssc[start2013:stop2013],quarry_ssc[start2014:stop2014]
    lbj_ssc2012,lbj_ssc2013,lbj_ssc2014 = lbj_ssc[start2012:stop2012],lbj_ssc[start2013:stop2013],lbj_ssc[start2014:stop2014]
    ## loglog DAM samples
    ax1.set_title('FG1',fontsize=10)
    ax1.loglog(dam_ssc2012['Q'],dam_ssc2012['SSC (mg/L)'],'o',fillstyle='none',c='k',label='2012')
    ax1.loglog(dam_ssc2013['Q'],dam_ssc2013['SSC (mg/L)'],'^',fillstyle='none',c='k',label='2013')
    ax1.loglog(dam_ssc2014['Q'],dam_ssc2014['SSC (mg/L)'],'s',fillstyle='none',c='k',label='2014')
    ## loglog quarry samples
    ax2.set_title('FG2',fontsize=10)
    ax2.loglog(quarry2012['Q'],quarry2012['SSC (mg/L)'],'o',fillstyle='none',c='k',label='2012')
    ax2.loglog(quarry2013['Q'],quarry2013['SSC (mg/L)'],'^',fillstyle='none',c='k',label='2013')
    ax2.loglog(quarry2014['Q'],quarry2014['SSC (mg/L)'],'s',fillstyle='none',c='k',label='2014')
    ## plot LBJ samples
    ax3.set_title('FG3',fontsize=10)
    ax3.loglog(lbj_ssc2012['Q'],lbj_ssc2012['SSC (mg/L)'],'o',fillstyle='none',c='k',label='2012')
    ax3.loglog(lbj_ssc2013['Q'],lbj_ssc2013['SSC (mg/L)'],'^',fillstyle='none',c='k',label='2013')
    ax3.loglog(lbj_ssc2014['Q'],lbj_ssc2014['SSC (mg/L)'],'s',fillstyle='none',c='k',label='2014')
    ## plot a line marking storm threshold and label it
    storm_Q_DAM = DAM[DAM['stage']==DAM_storm_threshold.round(0)]['Q'][0]
    storm_Q_LBJ = LBJ[LBJ['stage']==LBJ_storm_threshold.round(0)]['Q'][0]
    ax3.axvline(x=storm_Q_DAM,ls='--',color='k'),ax2.axvline(x=storm_Q_DAM,ls='--',color='k'),ax1.axvline(x=storm_Q_LBJ,ls='--',color='k')  
    ## Limits
    ax1.set_ylim(10**0,10**5), ax2.set_ylim(10**0,10**5), ax3.set_ylim(10**0,10**5)
    ax1.set_xlim(10**1,10**5), ax2.set_xlim(10**1,10**5), ax3.set_xlim(10**1,10**5)
    ax3.set_ylabel('SSC (mg/L)'), ax3.set_xlabel('Q (L/sec)'), ax2.set_xlabel('Q (L/sec)'), ax1.set_xlabel('Q (L/sec)')
    ax3.legend(loc='best')#, ax2.legend(loc='best'), ax1.legend(loc='best')
    ax2.loglog([10**2],[10**3.5],'s',markersize=60.,fillstyle='none',color='grey')
    
    ## Post-mitigation
    SSC = SSC_dict['Post-ALL']
    ## Append Discharge (Q) data
    dam_ssc = pd.DataFrame(SSC[SSC['Location']=='DAM']['SSC (mg/L)'])
    dam_ssc['Q']=DAM['Q']
    dam_ssc = dam_ssc.dropna()
    quarry_ssc = pd.DataFrame(SSC[SSC['Location'].isin(['DT','R2'])]['SSC (mg/L)'])
    quarry_ssc['Q']=QUARRY['Q']
    quarry_ssc =quarry_ssc.dropna()
    lbj_ssc = pd.DataFrame(SSC[SSC['Location']=='LBJ']['SSC (mg/L)'])
    lbj_ssc['Q']=LBJ['Q']
    lbj_ssc=lbj_ssc.dropna()
    ## Subset by year
    dam_ssc2012,dam_ssc2013,dam_ssc2014 = dam_ssc[start2012:stop2012],dam_ssc[start2013:stop2013],dam_ssc[start2014:stop2014]
    quarry2012,quarry2013,quarry2014 = quarry_ssc[start2012:stop2012],quarry_ssc[start2013:stop2013],quarry_ssc[start2014:stop2014]
    lbj_ssc2012,lbj_ssc2013,lbj_ssc2014 = lbj_ssc[start2012:stop2012],lbj_ssc[start2013:stop2013],lbj_ssc[start2014:stop2014]
    ## loglog DAM samples
    ax4.set_title('FG1',fontsize=10)
    ax4.loglog(dam_ssc2014['Q'],dam_ssc2014['SSC (mg/L)'],'s',fillstyle='none',c='k',label='2014-2015')
    ## loglog quarry samples
    ax5.set_title('FG2',fontsize=10)
    ax5.loglog(quarry2014['Q'],quarry2014['SSC (mg/L)'],'s',fillstyle='none',c='k',label='2014-2015')
    ## plot LBJ samples
    ax6.set_title('FG3',fontsize=10)
    ax6.loglog(lbj_ssc2014['Q'],lbj_ssc2014['SSC (mg/L)'],'s',fillstyle='none',c='k',label='2014-2015')
    ## plot a line marking storm threshold and label it
    storm_Q_DAM = DAM[DAM['stage']==DAM_storm_threshold.round(0)]['Q'][0]
    storm_Q_LBJ = LBJ[LBJ['stage']==LBJ_storm_threshold.round(0)]['Q'][0]
    ax6.axvline(x=storm_Q_DAM,ls='--',color='k'),ax5.axvline(x=storm_Q_DAM,ls='--',color='k'),ax4.axvline(x=storm_Q_LBJ,ls='--',color='k')  
    ## Limits
    ax4.set_ylim(10**0,10**5), ax5.set_ylim(10**0,10**5), ax6.set_ylim(10**0,10**5)
    ax4.set_xlim(10**1,10**5), ax5.set_xlim(10**1,10**5), ax6.set_xlim(10**1,10**5)
    ax6.set_ylabel('SSC (mg/L)'), ax6.set_xlabel('Q (L/sec)'), ax5.set_xlabel('Q (L/sec)'), ax4.set_xlabel('Q (L/sec)')
    ax6.legend(loc='best')#, ax5.legend(loc='best'), ax4.legend(loc='best')
    ax5.loglog([10**2],[10**3.5],'s',markersize=60.,fillstyle='none',color='grey')

    
    plt.tight_layout(pad=0.1)
    show_plot(show,fig)
    savefig(save,filename)
    return
## Pre-mitigation
plotQvsC_pre_and_post(storm_samples_only=False,ms=6,show=True,log=True,save=False,filename=figdir+'')