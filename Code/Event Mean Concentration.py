# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 10:49:58 2015

@author: Alex
"""

#   Event Mean Concentration


def Q_EMC(storm_data, show=False):
    fig, qemc = plt.subplots(1,1)
    #Plot event mean concentration
    storm_data['sEMC-LBJ'].dropna().plot(ax=qemc,c='r',marker='o',ls='None')
    storm_data['sEMC-QUARRY'].dropna().plot(ax=qemc,c='y',marker='o',ls='None')
    storm_data['sEMC-DAM'].dropna().plot(ax=qemc,c='g',marker='o',ls='None')
    #Plot grab samples
    storm_data['LBJgrab'].plot(ax=qemc,color='r',marker='o',ls='None',markersize=6,label='LBJ-grab')
    storm_data['QUARRYgrab'].plot(ax=qemc,color='y',marker='o',ls='None',markersize=6,label='QUARRY-grab')
    storm_data['DAMgrab'].plot(ax=qemc,color='g',marker='o',ls='None',markersize=6,label='DAM-grab')
    
    showstormintervals(qemc,All_Storms)
    plt.grid()
    
    plt.draw()
    if show==True:
        plt.show()
    return
#Q_EMC(storm_data_LBJ,True)