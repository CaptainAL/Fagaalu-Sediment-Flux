# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 13:29:00 2015

@author: Alex
"""

## NOT SURE WHAT THIS WAS FOR

def SSCprobplots(subset='pre',withR2=False,show=False,save=False,filename=figdir+''):
   
    ## Subset SSC
    ## Pre-mitigation baseflow
    SSC = SSC_dict[subset[0]]
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
    
    ax1 = plt.subplot(231)
    stats.probplot(GrabSamples['DAM'].dropna(), plot=plt)
    
    ax2 = plt.subplot(232)
    stats.probplot(GrabSamples['QUARRY'].dropna(), plot=plt)
    ax3 = plt.subplot(233)
    stats.probplot(GrabSamples['LBJ'].dropna(), plot=plt)    
    
    ## Subset SSC
    ## Pre-mitigation stormflow
    SSC = SSC_dict[subset[1]]
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
    
    ax4 = plt.subplot(234)
    stats.probplot(GrabSamples['DAM'].dropna(), plot=plt)
    ax5 = plt.subplot(235)
    stats.probplot(GrabSamples['QUARRY'].dropna(), plot=plt)
    ax6 = plt.subplot(236)
    stats.probplot(GrabSamples['LBJ'].dropna(), plot=plt)
    
    ax1.set_ylabel('Baseflow'), ax4.set_ylabel('Stormflow')
    
    ax1.set_title('DAM'), ax2.set_title('QUARRY'), ax3.set_title('LBJ')
    ax4.set_title('DAM'), ax5.set_title('QUARRY'), ax6.set_title('LBJ')
    plt.tight_layout(pad=0.1)
    show_plot(show)
    savefig(save,filename)
    return
#SSCprobplots(subset=['Pre-baseflow','Pre-storm'],withR2=False,show=True,save=False,filename=figdir+'')