# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 12:41:15 2015

@author: Alex
"""

#plot Precip Q and Turbidity data

def plot_P_Q_T(lwidth=0.5, show=False):
    fig, (precip, Q, ntu) = plt.subplots(3,1,sharex=True,figsize=(6.5,6))
    mpl.rc('lines',markersize=10,linewidth=lwidth)
    ##Precip
    precip.plot_date(PrecipFilled.index,PrecipFilled['Precip'],ls='steps-post',marker='None',c='b',label='Precip-Filled')

    ##Discharge
    Q.plot_date(LBJ['Q'].index,LBJ['Q'],ls='-',marker='None',c='r',label='VILLAGE Q')
    Q.plot_date(DAM['Q'].index,DAM['Q'],ls='-',marker='None',c='g',label='FOREST Q')
    Q.axhline(y=66,ls='--',color='k')

    ## Total storm sediment flux (Mg)
    #sed = fig.add_axes(Q.get_position(), frameon=False, sharex=Q)
    
    #SedFluxStorms_diff = SedFluxStorms_LBJ['Ssum'] - SedFluxStorms_DAM['Ssum']
    #SedFluxStorms_diff = SedFluxStorms_diff.dropna()
    #sed.plot_date(SedFluxStorms_LBJ['Ssum'].index,SedFluxStorms_LBJ['Ssum'],ls='None',marker='o',color='r')
    #sed.plot_date(SedFluxStorms_DAM['Ssum'].index,SedFluxStorms_DAM['Ssum'],ls='None',marker='o',color='g')
    #sed.plot_date(SedFluxStorms_diff.index,SedFluxStorms_diff,ls='None',marker='o',color='y')
    
    #sed.yaxis.set_ticks_position('right')
    #sed.yaxis.set_label_position('right')
    #sed.set_ylabel('Total Storm SedFlux (Mg)')
    
    ##Turbidity
    ntu.plot_date(LBJ['NTU'].index,LBJ['NTU'],ls='-',marker='None',c='r',label='VILLAGE 15min NTU')
    ntu.plot_date(DAM['NTU'].index,DAM['NTU'],ls='-',marker='None',c='g',label='FOREST 15min NTU')
    ntu.yaxis.set_major_locator(my_locator)
    ##plot all Grab samples at location 
    ssc = fig.add_axes(ntu.get_position(), frameon=False, sharex=ntu)#,sharey=ntu)
    ssc.plot_date(LBJ['Grab-SSC-mg/L'].index,LBJ['Grab-SSC-mg/L'],'.',markeredgecolor='grey',color='r',label='VILLAGE SSC grab')
    ssc.plot_date(QUARRY['GrabDT-SSC-mg/L'].index,QUARRY['GrabDT-SSC-mg/L'],'.',markeredgecolor='grey',color='grey',label='QUARRY SSC grab (DT)')
    ssc.plot_date(QUARRY['GrabR2-SSC-mg/L'].index,QUARRY['GrabR2-SSC-mg/L'],'.',markeredgecolor='grey',color='y',label='QUARRY SSC (R2)')
    #ssc.plot_date(QUARRY['Grab-SSC-mg/L'].index,QUARRY['Grab-SSC-mg/L'],'.',markeredgecolor='grey',color='y',label='QUARRY SSC grab')
    ssc.plot_date(DAM['Grab-SSC-mg/L'].index,DAM['Grab-SSC-mg/L'],'.',markeredgecolor='grey',color='g',label='FOREST SSC grab')    
    ##
    ssc.yaxis.set_major_locator(my_locator)
    ssc.yaxis.set_ticks_position('right'),ssc.yaxis.set_label_position('right')
    ssc.set_ylabel('SSC (mg/L)'),ssc.legend(loc='upper right')
    ssc.set_ylim(0.15000)
    ## Shade storm intervals
    showstormintervals(precip,LBJ_storm_threshold, LBJ_StormIntervals)
    showstormintervals(Q, LBJ_storm_threshold, LBJ_StormIntervals,shade_color='r')
    showstormintervals(ntu,DAM_storm_threshold, DAM_StormIntervals,shade_color='g')

    precip.set_ylabel('Precip (mm/15min)'),precip.legend()
    Q.set_ylabel('Discharge (L/sec)'),Q.set_ylim(0,LBJ['Q'].max()+100),Q.legend()
    ntu.set_ylabel('Turbidity (NTU)'),ntu.set_ylim(0,LBJ['NTU'].max()),ntu.legend(loc='upper left')
    #ntu.xaxis.set_major_locator(matplotlib.dates.MonthLocator(range(1, 13), bymonthday=1, interval=6))
    #ntu.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%b '%y"))
    plt.tight_layout(pad=0.1)
    show_plot(show)
    return
#plot_P_Q_T(lwidth=0.5,show=True)