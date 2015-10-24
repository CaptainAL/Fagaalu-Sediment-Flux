# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 12:52:41 2015

@author: Alex
"""

## Extra SSYEV Qmax plots


### Qmax vs S    
def plotQmaxS(show=True,log=True,save=False,norm=True): 
    fig, qs = plt.subplots(1)
    xy=np.linspace(.001,100)
    upperdotsize = 50#scaleSeries(SedFluxStorms_DAM['Qsum']/1000)
    lowerdotsize = 50#scaleSeries(SedFluxStorms_LBJ['Qsum']/1000)
    
    if norm==True:
        ALLStorms=NormalizeSSYbyCatchmentArea(compile_Storms_data())
        ylabel,xlabel= r'$SSY (Mg \ km^{-2})$',r'$Q_{max} (m^3 s^{-1} km^{-2})$'
    elif norm==False:
        ALLStorms=compile_Storms_data()
        ylabel,xlabel = 'SSY (Mg)',r'$Qmax (m^3 s^{-1})$'
   
    ## Lower is below in norm==False loop
    
    ## Upper Watershed (=DAM)
    ALLStorms_upper = ALLStorms[['Qmaxupper','Supper']].dropna()
    qs.scatter(ALLStorms_upper['Qmaxupper']/1000,ALLStorms_upper['Supper'],edgecolors='grey',color='g',s=upperdotsize,label='FOREST')
    QmaxS_upper_power = powerfunction(ALLStorms_upper['Qmaxupper']/1000,ALLStorms_upper['Supper'])
    PowerFit_CI(ALLStorms_upper['Qmaxupper']/1000,ALLStorms_upper['Supper'],xy,qs,linestyle='-',color='g',label='FOREST') 
    QmaxS_upper_linear = linearfunction(ALLStorms_upper['Qmaxupper']/1000,ALLStorms_upper['Supper'])
    #LinearFit(ALLStorms_upper['Qmaxupper']/1000,ALLStorms_upper['Supper'],xy,qs,linestyle='--',color='g',label='QmaxS_upper_linear') 
    labelindex(ALLStorms_upper.index,ALLStorms_upper['Qmaxupper']/1000,ALLStorms_upper['Supper'],qs)   
    
    ## Total Watershed (=LBJ)
    ALLStorms_total = ALLStorms[['Qmaxtotal','Stotal']].dropna()
    qs.scatter(ALLStorms_total['Qmaxtotal']/1000,ALLStorms_total['Stotal'],edgecolors='grey',color='r',s=lowerdotsize,label='VILLAGE')
    QmaxS_total_power = powerfunction(ALLStorms_total['Qmaxtotal']/1000,ALLStorms_total['Stotal'])
    PowerFit_CI(ALLStorms_total['Qmaxtotal']/1000,ALLStorms_total['Stotal'],xy,qs,linestyle='-',color='r',label='VILLAGE') 
    QmaxS_total_linear = linearfunction(ALLStorms_total['Qmaxtotal']/1000,ALLStorms_total['Stotal'])
    #LinearFit(ALLStorms_total['Qmaxtotal']/1000,ALLStorms_total['Stotal'],xy,qs,linestyle='--',color='r',label='QmaxS_total_linear') 
    labelindex(ALLStorms_total.index,ALLStorms_total['Qmaxtotal']/1000,ALLStorms_total['Stotal'],qs)   
    
    
    ## Lower Watershed (=LBJ-DAM)
    if norm==False:
        qs.scatter(ALLStorms['Qmaxlower']/1000,ALLStorms['Slower'],edgecolors='grey',color='y',s=lowerdotsize,label='Lower (VIL-FOR)')
        QmaxS_lower_power = powerfunction(ALLStorms['Qmaxlower']/1000,ALLStorms['Slower'])
        PowerFit(ALLStorms['Qmaxlower']/1000,ALLStorms['Slower'],xy,qs,linestyle='-',color='y',label='Qmax_LOWER') 
        QmaxS_lower_linear = linearfunction(ALLStorms['Qmaxlower']/1000,ALLStorms['Slower'])
        #LinearFit(ALLStorms['Qmaxlower']/1000,ALLStorms['Slower'],xy,qs,linestyle='--',color='y',label='QmaxS_lower_linear') 
        labelindex(ALLStorms.index,ALLStorms['Qmaxlower']/1000,ALLStorms['Slower'])
    
    if norm==True:
        #Duvert1 = 224.4*(xy**1.34)
        Duvert2 = 446.6*(xy**0.93)
        #DuvertLAFR = 408*(xy**0.95)
        #DuvertARES= 640*(xy**1.22)
        #DuvertCIES=5039*(xy**1.82)
        DuvertCOMX= 28*(xy**1.92)
        #PowerFit(xy,Duvert1,xy,qs,linestyle='-',color='grey',label='Duvert(2012)Linear')
        PowerFit(xy,Duvert2,xy,qs,linestyle='--',color='grey',label='Duvert(2012)Nonlinear')
        #PowerFit(xy,DuvertLAFR,xy,qs,linestyle='-',color='k',label=r'Duvert(2012)$LA_{FR}$')
        #PowerFit(xy,DuvertARES,xy,qs,linestyle='--',color='k',label=r'Duvert(2012)$AR_{ES}$')
        #PowerFit(xy,DuvertCIES,xy,qs,linestyle='-.',color='k',label=r'Duvert(2012)$CI_{ES}$')
        PowerFit(xy,DuvertCOMX,xy,qs,linestyle='-.',color='b',label=r'Duvert(2012)$Mexico$')        
        qs.legend(loc='best',ncol=3,fancybox=True)  
    qs.legend(loc='best',ncol=2,fancybox=True)  
    title="Maximum Event Discharge vs Event Sediment Yield from Fagaalu Stream"
    qs.set_title(title)
    qs.set_ylabel(ylabel)
    qs.set_xlabel(xlabel)#+r'$; DotSize= Qsum (m^3)$')
    logaxes(log,fig)
    qs.autoscale_view(True,True,True)
    
    fig.canvas.manager.set_window_title('Figure : '+'Qmax vs. S')
      
    show_plot(show,fig)
    savefig(save,title+'1.png')
    return
#plotQmaxS(show=True,log=True,save=False,norm=True)  
#plotQmaxS(show=True,log=True,save=True,norm=True)  
#plotQmaxS(show=True,log=False,save=True)
#plotQmaxS(show=True,log=True,save=True,norm=False)
#plotQmaxS(show=True,log=True,save=True,norm=True)

### Qmax vs S    
def plotQmaxStotal(subset='pre',ms=10,norm=False,log=False,show=False,save=False,filename=''): 
    mpl.rc('lines',markersize=ms)
    mpl.rc('grid',alpha=0)
    fig, qmaxs = plt.subplots(figsize=(5,4))
    ## Normalize by area
    if norm==True:
        ALLStorms=NormalizeSSYbyCatchmentArea(compile_Storms_data(subset))
        ylabel,xlabelP,xlabelEI,xlabelQsum,xlabelQmax = r'$SSY (Mg/km^2)$','Precip (mm)','Erosivity Index', r'$(m^3/km^2)$', r'$(m^3/sec/km^2)$'
    else:
        ALLStorms=compile_Storms_data(subset)
        ylabel,xlabelP,xlabelEI,xlabelQsum,xlabelQmax = 'SSY (Mg)','Precip (mm)','Erosivity Index',r'$(m^3)$',r'$(m^3/sec)$'
    xy=None ## let the Fit functions plot their own lines
    ## Qmax vs S at Upper, Total  
    ALLStorms_upper = ALLStorms[['Qmaxupper','Supper']].dropna()
    ALLStorms_total = ALLStorms[['Qmaxtotal','Stotal']].dropna() 
    qmaxs.plot(ALLStorms_upper['Qmaxupper'],ALLStorms_upper['Supper'],color='grey',linestyle='none',marker='s',fillstyle='none',label='F1 Upper watershed')
    qmaxs.plot(ALLStorms_total['Qmaxtotal'],ALLStorms_total['Stotal'],color='k',linestyle='none',marker='o',label='F3 Village')
    ## Upper Watershed (=DAM)       
    QmaxS_upper_power = powerfunction(ALLStorms_upper['Qmaxupper'],ALLStorms_upper['Supper'])
    PowerFit(ALLStorms_upper['Qmaxupper'],ALLStorms_upper['Supper'],xy,qmaxs,linestyle='-',color='grey',label='F1 Upper watershed '+r'$r^2$'+"%.2f"%QmaxS_upper_power.r2)
    ## Total Watershed (=LBJ)
    QmaxS_total_power = powerfunction(ALLStorms_total['Qmaxtotal'],ALLStorms_total['Stotal'])
    PowerFit(ALLStorms_total['Qmaxtotal'],ALLStorms_total['Stotal'],xy,qmaxs,linestyle='-',color='k',label='F3 Village '+r'$r^2$'+"%.2f"%QmaxS_total_power.r2)
    qmaxs.set_xlabel('Maximum Event Discharge '+xlabelQmax)
    qmaxs.set_ylabel(ylabel)
    #qmaxs.set_ylabel(ylabel)#qmaxs.set_xlabel(xlabelQmax)
    qmaxs.set_xlim(10**-1.2,10**1)#, qmaxs.set_ylim(10**-3,10**2.2)
    qmaxs.legend(loc='lower right',fancybox=True) 
    
    #letter_subplots(fig,x=0.1,y=0.95,vertical='top',horizontal='right',Color='k',font_size=10,font_weight='bold')
    for ax in fig.axes:
        ax.grid(False)          
        #ax.autoscale_view(True,True,True)
    logaxes(log,fig) 
    plt.grid(b=False,axis='both')
    
    plt.tight_layout(pad=0.1)
    show_plot(show,fig)
    savefig(save,filename)
    return
#plotQmaxStotal(subset='pre',ms=4,norm=True,log=True,show=True,save=False,filename='')  

### Qmax vs S    
def plotQmaxSseparate(show=True,log=True,save=False,norm=True): 
    fig, (qs_upper, qs_total) = plt.subplots(2,sharex=True,sharey=True)
    xy=np.linspace(.001,100)
    upperdotsize = 50#scaleSeries(SedFluxStorms_DAM['Qsum']/1000)
    lowerdotsize = 50#scaleSeries(SedFluxStorms_LBJ['Qsum']/1000)
    
    if norm==True:
        ALLStorms=NormalizeSSYbyCatchmentArea(compile_Storms_data())
        ylabel,xlabel= r'$SSY (Mg \ km^{-2})$',r'$Q_{max} (m^3 s^{-1} km^{-2})$'
    elif norm==False:
        ALLStorms=compile_Storms_data()
        ylabel,xlabel = 'SSY (Mg)',r'$Qmax (m^3 s^{-1})$'
   
    ## Lower is below in norm==False loop
    
    ## Upper Watershed (=DAM)
    QmaxS_upper = SedFluxStorms_DAM[['Qmax','Ssum']].dropna()
    qs_upper.scatter(QmaxS_upper['Qmax']/1000,QmaxS_upper['Ssum'],edgecolors='grey',color='g',s=upperdotsize,label='Upper(VILLAGE)')
    QmaxS_upper_power = powerfunction(QmaxS_upper['Qmax']/1000,QmaxS_upper['Ssum'])
    PowerFit_CI(QmaxS_upper['Qmax']/1000,QmaxS_upper['Ssum'],xy,qs_upper,linestyle='-',color='g',label='Qmax_TOTAL') 
    QmaxS_upper_linear = linearfunction(QmaxS_upper['Qmax']/1000,QmaxS_upper['Ssum'])
    #LinearFit(ALLStorms_upper['Qmaxupper']/1000,ALLStorms_upper['Supper'],xy,qs,linestyle='--',color='g',label='QmaxS_upper_linear') 
    labelindex(QmaxS_upper.index,QmaxS_upper['Qmax']/1000,QmaxS_upper['Ssum'],qs_upper)   
    
    ## Total Watershed (=LBJ)
    ALLStorms_total = ALLStorms[['Qmaxtotal','Stotal']].dropna()
    qs_total.scatter(ALLStorms_total['Qmaxtotal']/1000,ALLStorms_total['Stotal'],edgecolors='grey',color='r',s=lowerdotsize,label='Total(VILLAGE)')
    QmaxS_total_power = powerfunction(ALLStorms_total['Qmaxtotal']/1000,ALLStorms_total['Stotal'])
    PowerFit_CI(ALLStorms_total['Qmaxtotal']/1000,ALLStorms_total['Stotal'],xy,qs_total,linestyle='-',color='r',label='Qmax_TOTAL') 
    QmaxS_total_linear = linearfunction(ALLStorms_total['Qmaxtotal']/1000,ALLStorms_total['Stotal'])
    #LinearFit(ALLStorms_total['Qmaxtotal']/1000,ALLStorms_total['Stotal'],xy,qs,linestyle='--',color='r',label='QmaxS_total_linear') 
    labelindex(ALLStorms_total.index,ALLStorms_total['Qmaxtotal']/1000,ALLStorms_total['Stotal'],qs_total)   
    
    ## Lower Watershed (=LBJ-DAM)
    if norm==False:
        qs_total.scatter(ALLStorms['Qmaxlower']/1000,ALLStorms['Slower'],edgecolors='grey',color='y',s=lowerdotsize,label='Lower (VIL-FOR)')
        QmaxS_lower_power = powerfunction(ALLStorms['Qmaxlower']/1000,ALLStorms['Slower'])
        PowerFit(ALLStorms['Qmaxlower']/1000,ALLStorms['Slower'],xy,qs_total,linestyle='-',color='y',label='Qmax_LOWER') 
        QmaxS_lower_linear = linearfunction(ALLStorms['Qmaxlower']/1000,ALLStorms['Slower'])
        #LinearFit(ALLStorms['Qmaxlower']/1000,ALLStorms['Slower'],xy,qs_total,linestyle='--',color='y',label='QmaxS_lower_linear') 
        labelindex(ALLStorms.index,ALLStorms['Qmaxlower']/1000,ALLStorms['Slower'])
    
    if norm==True:
        Duvert1 = 224.4*(xy**1.34)
        Duvert2 = 446.6*(xy**0.93)
        DuvertLAFR = 408*(xy**0.95)
        DuvertARES= 640*(xy**1.22)
        DuvertCIES=5039*(xy**1.82)
        DuvertCOMX= 28*(xy**1.92)
        PowerFit(xy,Duvert1,xy,qs_total,linestyle='-',color='grey',label='Duvert(2012)Linear')
        PowerFit(xy,Duvert2,xy,qs_total,linestyle='--',color='grey',label='Duvert(2012)Nonlinear')
        PowerFit(xy,DuvertLAFR,xy,qs_total,linestyle='-',color='k',label=r'Duvert(2012)$LA_{FR}$')
        PowerFit(xy,DuvertARES,xy,qs_total,linestyle='--',color='k',label=r'Duvert(2012)$AR_{ES}$')
        PowerFit(xy,DuvertCIES,xy,qs_total,linestyle='-.',color='k',label=r'Duvert(2012)$CI_{ES}$')
        PowerFit(xy,DuvertCOMX,xy,qs_total,linestyle='-.',color='b',label=r'Duvert(2012)$CO_{MX}$')        
        qs_total.legend(loc='best',ncol=3,fancybox=True)  
    
    title="Maximum Event Discharge vs Event Sediment Yield from Fagaalu Stream"
    plt.suptitle(title)
    qs_upper.set_ylabel(ylabel)
    qs_upper.set_xlabel(xlabel)#+r'$; DotSize= Qsum (m^3)$')
    qs_total.set_xlabel(xlabel)#+r'$; DotSize= Qsum (m^3)$')

    fig.canvas.manager.set_window_title('Figure : '+'Qmax vs. S')
    
    logaxes(log,fig)
    #qs_upper.autoscale_view(True,True,True)
    #qs_total.autoscale_view(True,True,True)
    show_plot(show,fig)
    savefig(save,title)
    return
#plotQmaxSseparate(show=True,log=True,save=False,norm=True)  
