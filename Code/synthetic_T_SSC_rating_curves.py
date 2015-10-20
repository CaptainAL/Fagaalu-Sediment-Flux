# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 12:47:03 2015

@author: Alex
"""

#SYnthetic rating curve stuff

## Read Synthetic Rating Curves (SRC) from putting sediment in bucket and sampling
SRC_File = pd.ExcelFile(datadir+'T/SyntheticRatingCurve/SyntheticRatingCurve.xlsx')
LBJ_SRC = SRC_File.parse('LBJ')[0:5]
QUARRY_SRC = SRC_File.parse('QUARRY')
DAM_SRC = SRC_File.parse('DAM')
N1_SRC = SRC_File.parse('N1')
N2_SRC = SRC_File.parse('N2')[0:5]

## PLOT T-SSC for  Synthetic Rating Curves
def Synthetic_Rating_Curves(param,show=False,save=False,filename=figdir+''):
    fig, ((lbj,quarry,dam),(n1,n2,comb)) = plt.subplots(2,3,figsize=(8,4),sharex=True,sharey=True,)
    max_y,max_x = 8000, 8000
    xy = np.linspace(0,max_y)
    ## LBJ    
    lbj.scatter(LBJ_SRC[param],LBJ_SRC['SSC(mg/L)'],c='r')
    lbj_SRC = pd.ols(y=LBJ_SRC['SSC(mg/L)'],x=LBJ_SRC[param],intercept=False)
    lbj.plot(xy,xy*lbj_SRC.beta[0],ls='-',label='LBJ_SRC'+r'$r^2$'+"%.2f"%lbj_SRC.r2,c='r')
    comb.plot(xy,xy*lbj_SRC.beta[0],ls='-',label='LBJ_SRC'+r'$r^2$'+"%.2f"%lbj_SRC.r2,c='r')
    lbj.set_ylabel('SSC (mg/L)'), lbj.set_title('LBJ '+r'$r^2=$'+"%.2f"%lbj_SRC.r2)
    ## QUARRY
    quarry.scatter(QUARRY_SRC[param],QUARRY_SRC['SSC(mg/L)'],c='g')
    quarry_SRC = pd.ols(y=QUARRY_SRC['SSC(mg/L)'],x=QUARRY_SRC[param],intercept=False)
    quarry.plot(xy,xy*quarry_SRC.beta[0],ls='-',label='QUARRY_SRC'+r'$r^2$'+"%.2f"%quarry_SRC.r2,c='g')
    comb.plot(xy,xy*quarry_SRC.beta[0],ls='-',label='QUARRY_SRC'+r'$r^2$'+"%.2f"%quarry_SRC.r2,c='g')
    quarry.set_ylabel('SSC (mg/L)'), quarry.set_title('QUARRY '+r'$r^2=$'+"%.2f"%quarry_SRC.r2)
    ## DAM
    dam.scatter(DAM_SRC[param],DAM_SRC['SSC(mg/L)'],c='b')
    dam_SRC = pd.ols(y=DAM_SRC['SSC(mg/L)'],x=DAM_SRC[param],intercept=False)
    dam.plot(xy,xy*dam_SRC.beta[0],ls='-',label='DAM_SRC'+r'$r^2$'+"%.2f"%dam_SRC.r2,c='b')
    comb.plot(xy,xy*dam_SRC.beta[0],ls='-',label='DAM_SRC'+r'$r^2$'+"%.2f"%dam_SRC.r2,c='b')
    dam.set_ylabel('SSC (mg/L)'), dam.set_title('DAM '+r'$r^2=$'+"%.2f"%dam_SRC.r2)
    ## N1
    n1.scatter(N1_SRC[param],N1_SRC['SSC(mg/L)'],c='y')
    n1_SRC = pd.ols(y=N1_SRC['SSC(mg/L)'],x=N1_SRC[param],intercept=False)
    n1.plot(xy,xy*n1_SRC.beta[0],ls='-',label='N1_SRC'+r'$r^2$'+"%.2f"%n1_SRC.r2,c='y')
    comb.plot(xy,xy*n1_SRC.beta[0],ls='-',label='N1_SRC'+r'$r^2$'+"%.2f"%n1_SRC.r2,c='y')
    n1.set_ylabel('SSC (mg/L)'), n1.set_title('N1 '+r'$r^2=$'+"%.2f"%n1_SRC.r2)
    ## N2
    n2.scatter(N2_SRC[param],N2_SRC['SSC(mg/L)'],c='k')
    n2_SRC = pd.ols(y=N2_SRC['SSC(mg/L)'],x=N2_SRC[param],intercept=False)
    n2.plot(xy,xy*n1_SRC.beta[0],ls='-',label='N2_SRC'+r'$r^2$'+"%.2f"%n2_SRC.r2,c='k')
    comb.plot(xy,xy*n1_SRC.beta[0],ls='-',label='N2_SRC'+r'$r^2$'+"%.2f"%n2_SRC.r2,c='k')
    n2.set_ylabel('SSC (mg/L)'), n2.set_title('N2 '+r'$r^2=$'+"%.2f"%n2_SRC.r2)
    ## COMBINED
    comb.scatter(LBJ_SRC[param],LBJ_SRC['SSC(mg/L)'],c='r')
    comb.scatter(QUARRY_SRC[param],QUARRY_SRC['SSC(mg/L)'],c='g')
    comb.scatter(DAM_SRC[param],DAM_SRC['SSC(mg/L)'],c='b')
    comb.scatter(N1_SRC[param],N1_SRC['SSC(mg/L)'],c='y')
    comb.scatter(N2_SRC[param],N2_SRC['SSC(mg/L)'],c='k')
    comb.set_title('All')
    for ax in fig.axes:
        ax.set_xlabel(param)
        ax.set_ylim(0,max_y)
        ax.set_xlim(0,max_x)
        ax.locator_params(nbins=4)
    plt.tight_layout(pad=0.1)
    show_plot(show)
    savefig(save,filename)
    return
#Synthetic_Rating_Curves(param='SS_Mean',show=True,save=False)#,filename=figdir+'Synthetic Rating Curves.png')
    
## PLOT T-SSC for  Synthetic Rating Curves
def Synthetic_Rating_Curves_Fagaalu(param,show=False,save=False,filename=figdir+''):
    fig, (lbj,dam)= plt.subplots(1,2,figsize=(6,3),sharex=True,sharey=True,)
    lbj.text(0.1,0.95,'(a)',verticalalignment='top', horizontalalignment='right',transform=lbj.transAxes,color='k',fontsize=10,fontweight='bold')
    dam.text(0.1,0.95,'(b)',verticalalignment='top', horizontalalignment='right',transform=dam.transAxes,color='k',fontsize=10,fontweight='bold')
    max_y,max_x = 4000, 4000
    xy = np.linspace(0,max_y)
    ## LBJ    
    lbj.scatter(LBJ_SRC[param],LBJ_SRC['SSC(mg/L)'],c='k')
    lbj_SRC = pd.ols(y=LBJ_SRC['SSC(mg/L)'],x=LBJ_SRC[param],intercept=False)
    lbj.plot(xy,xy*lbj_SRC.beta[0],ls='-',label='FG3_OBS '+r'$r^2$'+"%.2f"%lbj_SRC.r2,c='k')
    lbj.set_xlabel('SS_Mean'), lbj.set_title('FG3_OBS '+r'$r^2=$'+"%.2f"%lbj_SRC.r2)
    ## DAM
    dam.scatter(DAM_SRC[param],DAM_SRC['SSC(mg/L)'],c='grey')
    dam_SRC = pd.ols(y=DAM_SRC['SSC(mg/L)'],x=DAM_SRC[param],intercept=False)
    dam.plot(xy,xy*dam_SRC.beta[0],ls='-',label='FG1_YSI'+r'$r^2$'+"%.2f"%dam_SRC.r2,c='grey')
    dam.set_xlabel('NTU'), dam.set_title('FG1_YSI '+r'$r^2=$'+"%.2f"%dam_SRC.r2)#, dam.set_ylabel('SSC (mg/L)'), 
    ## COMBINED
    for ax in fig.axes:
        ax.set_ylabel('SSC (mg/L)')
        ax.set_ylim(0,max_y)
        ax.set_xlim(0,max_x)
        ax.locator_params(nbins=4)
    plt.tight_layout(pad=0.1)
    show_plot(show)
    savefig(save,filename)
    return
#Synthetic_Rating_Curves_Fagaalu(param='SS_Mean',show=True,save=False,filename=figdir+'')