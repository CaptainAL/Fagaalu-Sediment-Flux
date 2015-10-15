# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 14:32:12 2015

@author: Alex
"""

## Kind of a cool plot

def plotQvsC_with_timeseries(subset='pre',storm_samples_only=False,ms=6,show=False,log=False,save=False,filename=figdir+''):  
    ## Subset SSC
    if subset=='pre' and storm_samples_only==True:
        SSC = SSC_dict['Pre-storm']
    elif subset=='pre' and  storm_samples_only==False:
        SSC = SSC_dict['Pre-ALL']
    elif subset=='post' and storm_samples_only==True:
        SSC = SSC_dict['Post-storm']
    elif subset=='post' and  storm_samples_only==False:
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
    ## Regression
    damQC = pd.ols(y=dam_ssc['SSC (mg/L)'],x=dam_ssc['Q'])
    quarQC =  pd.ols(y=quarry_ssc['SSC (mg/L)'],x=quarry_ssc['Q'])
    lbjQC = pd.ols(y=lbj_ssc['SSC (mg/L)'],x=lbj_ssc['Q'])

    fig=plt.figure(figsize=(10,6))
    ts_log = plt.subplot2grid((3,3),(0,0),colspan=3)
    ts = plt.subplot2grid((3,3),(1,0),colspan=3)
    up = plt.subplot2grid((3,3),(2,0))
    quar = plt.subplot2grid((3,3),(2,1))
    down = plt.subplot2grid((3,3),(2,2))
    ts_log.text(0.05,0.95,'(a)',verticalalignment='top', horizontalalignment='right',transform=ts_log.transAxes,color='k',fontsize=10,fontweight='bold')
    ts.text(0.05,0.95,'(b)',verticalalignment='top', horizontalalignment='right',transform=ts.transAxes,color='k',fontsize=10,fontweight='bold')
    up.text(0.1,0.95,'(c)',verticalalignment='top', horizontalalignment='right',transform=up.transAxes,color='k',fontsize=10,fontweight='bold')
    quar.text(0.1,0.95,'(d)',verticalalignment='top', horizontalalignment='right',transform=quar.transAxes,color='k',fontsize=10,fontweight='bold')
    down.text(0.1,0.95,'(e)',verticalalignment='top', horizontalalignment='right',transform=down.transAxes,color='k',fontsize=10,fontweight='bold')
    #fig, (up,quar,down) = plt.subplots(1,3,figsize=(8,3))
    mpl.rc('lines',markersize=ms)
    mpl.rc('grid',alpha=0.0) 
    ## plot LBJ samples
    down.set_title('FG3',fontsize=10)
    down.loglog(lbj_ssc2012['Q'],lbj_ssc2012['SSC (mg/L)'],'o',fillstyle='none',c='k',label='2012')
    down.loglog(lbj_ssc2013['Q'],lbj_ssc2013['SSC (mg/L)'],'^',fillstyle='none',c='k',label='2013')
    down.loglog(lbj_ssc2014['Q'],lbj_ssc2014['SSC (mg/L)'],'s',fillstyle='none',c='k',label='2014')
    ## loglog quarry samples
    quar.set_title('FG2',fontsize=10)
    quar.loglog(quarry2012['Q'],quarry2012['SSC (mg/L)'],'o',fillstyle='none',c='k',label='2012')
    quar.loglog(quarry2013['Q'],quarry2013['SSC (mg/L)'],'^',fillstyle='none',c='k',label='2013')
    quar.loglog(quarry2014['Q'],quarry2014['SSC (mg/L)'],'s',fillstyle='none',c='k',label='2014')
    ## loglog DAM samples
    up.set_title('FG1',fontsize=10)
    up.loglog(dam_ssc2012['Q'],dam_ssc2012['SSC (mg/L)'],'o',fillstyle='none',c='k',label='2012')
    up.loglog(dam_ssc2013['Q'],dam_ssc2013['SSC (mg/L)'],'^',fillstyle='none',c='k',label='2013')
    up.loglog(dam_ssc2014['Q'],dam_ssc2014['SSC (mg/L)'],'s',fillstyle='none',c='k',label='2014')
    ## Limits
    down.set_ylim(10**0,10**5), quar.set_ylim(10**0,10**5), up.set_ylim(10**0,10**5)
    down.set_xlim(10**1,10**5),quar.set_xlim(10**1,10**5),up.set_xlim(10**1,10**5)
    up.set_ylabel('SSC (mg/L)'), up.set_xlabel('Q (L/sec)'), quar.set_xlabel('Q (L/sec)'), down.set_xlabel('Q (L/sec)')
    up.legend(loc='best'), quar.legend(loc='best'), down.legend(loc='best')

    #log
    dam_ssc['SSC (mg/L)'].plot(ax=ts_log,ls='None',marker='s',fillstyle='none',color='grey',label='FG1')
    quarry_ssc['SSC (mg/L)'].plot(ax=ts_log,ls='None',marker='o',fillstyle='none',color='k',label='FG2')
    ts_log.legend(),ts_log.set_ylabel('SSC mg/L'),ts_log.set_yscale('log')
    ts_log.axvline(dt.datetime(2012,8,1),0,13000,c='k',ls='--'),ts_log.text(dt.datetime(2012,8,1),5000,'Baseflow sediment mitigtaion at quarry')
    ts_log.tick_params(axis='x',which='both',bottom='off',top='off',labelbottom='off') # labels along the bottom edge are off
    ts_log.spines['bottom'].set_visible(False)
    #linear
    dam_ssc['SSC (mg/L)'].plot(ax=ts,ls='None',marker='s',fillstyle='none',color='grey',label='FG1')
    quarry_ssc['SSC (mg/L)'].plot(ax=ts,ls='None',marker='o',fillstyle='none',color='k',label='FG2')
    ts.legend(),ts.set_ylabel('SSC mg/L')#,ts.set_yscale('log')
    ts.axvline(dt.datetime(2012,8,1),0,13000,c='k',ls='--')
    ts.tick_params(axis='x',which='both',bottom='off',top='off',labelbottom='off') # labels along the bottom edge are off
    ts.spines['bottom'].set_visible(False)
    
    plt.tight_layout(pad=0.1)
    show_plot(show,fig)
    savefig(save,filename)
    return
plotQvsC_with_timeseries(subset='pre',storm_samples_only=False,ms=6,show=False,log=False,save=False,filename=figdir+'')



## THIS WAS WITH THE STAGE THRESHOLD METHOD AND SUBSET BY YEARS

def plotQvsC(subset='pre',storm_samples_only=False,ms=6,show=False,log=False,save=False,filename=figdir+''):  
    ## Subset SSC
    if subset=='pre' and storm_samples_only==True:
        SSC = SSC_dict['Pre-storm']
    elif subset=='pre' and  storm_samples_only==False:
        SSC = SSC_dict['Pre-ALL']
    elif subset=='post' and storm_samples_only==True:
        SSC = SSC_dict['Post-storm']
    elif subset=='post' and  storm_samples_only==False:
        SSC = SSC_dict['Post-ALL']    
    ## Append Discharge (Q) data
    dam_ssc = pd.DataFrame(SSC[SSC['Location']=='DAM'][['SSC (mg/L)','24hr_precip']])
    dam_ssc['Q']=DAM['Q']
    dam_ssc = dam_ssc.dropna()
    quarry_ssc = pd.DataFrame(SSC[SSC['Location'].isin(['DT','R2'])][['SSC (mg/L)','24hr_precip']])
    quarry_ssc['Q']=QUARRY['Q']
    quarry_ssc =quarry_ssc.dropna()
    quarry_ssc_noP = quarry_ssc[(quarry_ssc['24hr_precip']<=0) & (quarry_ssc['SSC (mg/L)']>=500)]
    lbj_ssc = pd.DataFrame(SSC[SSC['Location']=='LBJ'][['SSC (mg/L)','24hr_precip']])
    lbj_ssc['Q']=LBJ['Q']
    lbj_ssc=lbj_ssc.dropna()
    lbj_ssc_noP = lbj_ssc[lbj_ssc['24hr_precip']<=2]
    ## Subset by year
    dam_ssc2012,dam_ssc2013,dam_ssc2014 = dam_ssc[start2012:stop2012],dam_ssc[start2013:stop2013],dam_ssc[start2014:stop2014]
    quarry2012,quarry2013,quarry2014 = quarry_ssc[start2012:stop2012],quarry_ssc[start2013:stop2013],quarry_ssc[start2014:stop2014]
    lbj_ssc2012,lbj_ssc2013,lbj_ssc2014 = lbj_ssc[start2012:stop2012],lbj_ssc[start2013:stop2013],lbj_ssc[start2014:stop2014]
    
    Pquarry2012,Pquarry2013,Pquarry2014 = quarry_ssc_noP[start2012:stop2012],quarry_ssc_noP[start2013:stop2013],quarry_ssc_noP[start2014:stop2014]
    ## Regression
    damQC = pd.ols(y=dam_ssc['SSC (mg/L)'],x=dam_ssc['Q'])
    quarQC =  pd.ols(y=quarry_ssc['SSC (mg/L)'],x=quarry_ssc['Q'])
    lbjQC = pd.ols(y=lbj_ssc['SSC (mg/L)'],x=lbj_ssc['Q'])

    fig, (up,quar,down) = plt.subplots(1,3,figsize=(8,3))
    letter_subplots(fig,0.1,0.95,'top','right','k',font_size=10,font_weight='bold')
    #
    mpl.rc('lines',markersize=ms)
    mpl.rc('grid',alpha=0.0) 
    ## plot LBJ samples
    down.set_title('FG3',fontsize=10)
    down.loglog(lbj_ssc2012['Q'],lbj_ssc2012['SSC (mg/L)'],'o',fillstyle='none',c='k',label='2012')
    down.loglog(lbj_ssc2013['Q'],lbj_ssc2013['SSC (mg/L)'],'^',fillstyle='none',c='k',label='2013')
    down.loglog(lbj_ssc2014['Q'],lbj_ssc2014['SSC (mg/L)'],'s',fillstyle='none',c='k',label='2014')
    #down.loglog(lbj_ssc_noP['Q'],lbj_ssc_noP['SSC (mg/L)'],'s',fillstyle='none',c='r',label='<12mm P')
    ## loglog quarry samples
    quar.set_title('FG2',fontsize=10)
    quar.loglog(quarry2012['Q'],quarry2012['SSC (mg/L)'],'o',fillstyle='none',c='k',label='2012')
    quar.loglog(quarry2013['Q'],quarry2013['SSC (mg/L)'],'^',fillstyle='none',c='k',label='2013')
    quar.loglog(quarry2014['Q'],quarry2014['SSC (mg/L)'],'s',fillstyle='none',c='k',label='2014')
    ## with no P
    quar.loglog(Pquarry2012['Q'],Pquarry2012['SSC (mg/L)'],'o',c='k',label='2012-no P')
    quar.loglog(Pquarry2013['Q'],Pquarry2013['SSC (mg/L)'],'^',c='k',label='2013-no P')
    quar.loglog(Pquarry2014['Q'],Pquarry2014['SSC (mg/L)'],'s',c='k',label='2014-no P') 
    
    ## loglog DAM samples
    up.set_title('FG1',fontsize=10)
    up.loglog(dam_ssc2012['Q'],dam_ssc2012['SSC (mg/L)'],'o',fillstyle='none',c='k',label='2012')
    up.loglog(dam_ssc2013['Q'],dam_ssc2013['SSC (mg/L)'],'^',fillstyle='none',c='k',label='2013')
    up.loglog(dam_ssc2014['Q'],dam_ssc2014['SSC (mg/L)'],'s',fillstyle='none',c='k',label='2014')

    ## Limits
    down.set_ylim(10**0,10**5), quar.set_ylim(10**0,10**5), up.set_ylim(10**0,10**5)
    down.set_xlim(10**1,10**5),quar.set_xlim(10**1,10**5),up.set_xlim(10**1,10**5)
    up.set_ylabel('SSC (mg/L)'), up.set_xlabel('Q (L/sec)'), quar.set_xlabel('Q (L/sec)'), down.set_xlabel('Q (L/sec)')
    up.legend(loc='best')#, quar.legend(loc='best'), down.legend(loc='best')
    quar.loglog([10**2],[10**3.5],'s',markersize=60.,fillstyle='none',color='grey')
    
    plt.tight_layout(pad=0.1)
    show_plot(show,fig)
    savefig(save,filename)
    return
## Pre-mitigation
plotQvsC(subset='pre',storm_samples_only=False,ms=6,show=True,log=True,save=False,filename=figdir+'')
#plotQvsC(subset='pre',storm_samples_only=False,ms=5,show=True,log=False,save=False,filename=figdir+'')
## Post-mitgation
#plotQvsC(subset='post',storm_samples_only=False,ms=6,show=True,log=False,save=False,filename=figdir+'')
#plotQvsC(subset='post',storm_samples_only=True,ms=8,show=True,log=False,save=False,filename=figdir+'')