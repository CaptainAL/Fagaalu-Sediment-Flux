# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 09:18:18 2015

@author: Alex
"""

## Q Storm diff table matplotlib
def Q_storm_diff_table():
    Q_Diff = pd.DataFrame({'UPPER m3':StormsDAM['Qsum']/1000,'TOTAL m3':StormsLBJ['Qsum']/1000,'Precip (mm)':StormsLBJ['Psum']}).dropna()
    ## Calculate Q from just Lower watershed
    Q_Diff['UPPER m3']=Q_Diff['UPPER m3'].apply(np.int) #m3
    Q_Diff['TOTAL m3']=Q_Diff['TOTAL m3'].apply(np.int) #m3
    Q_Diff['LOWER m3']=Q_Diff['TOTAL m3'] - Q_Diff['UPPER m3']
    Q_Diff = Q_Diff[Q_Diff['LOWER m3']>0]
    ## Calculate percentages
    Q_Diff['% Upper'] = Q_Diff['UPPER m3']/Q_Diff['TOTAL m3']*100
    Q_Diff['% Upper'] = Q_Diff['% Upper'].apply(np.int)
    Q_Diff['% Lower'] = Q_Diff['LOWER m3']/Q_Diff['TOTAL m3']*100
    Q_Diff['% Lower'] = Q_Diff['% Lower'].apply(np.int)
    Q_Diff['Precip (mm)'] = Q_Diff['Precip (mm)'].apply(np.int)
    Q_Diff['Storm#']=range(1,len(Q_Diff)+1)
    Q_Diff['Storm Start'] = Q_Diff.index
    Q_Diff['Storm Start'] = Q_Diff['Storm Start'].apply(lambda x: "{:%m/%d/%Y}".format(x))
    ## summary stats
    Percent_Upper = Q_Diff['UPPER m3'].sum()/Q_Diff['TOTAL m3'].sum()*100
    Percent_Lower =Q_Diff['LOWER m3'].sum()/Q_Diff['TOTAL m3'].sum()*100
    ## add summary stats to bottom of table
    Q_Diff=Q_Diff.append(pd.DataFrame({'Storm Start':'-','Storm#':'-','Precip (mm)':'-','UPPER m3':'-','LOWER m3':'-','TOTAL m3':'Average:','% Upper':"%.0f"%Percent_Upper,'% Lower':"%.0f"%Percent_Lower},index=['']))
    Q_Diff=Q_Diff[['Storm Start','Storm#','Precip (mm)','UPPER m3','LOWER m3','TOTAL m3','% Upper','% Lower']]
    return Q_Diff
Q_storm_diff_table()

## Calculate the percent of total Q with raw vales, BEFORE NORMALIZING by area!
def plotQ_storm_table(show=False):
    diff = pd.DataFrame({'Qupper':StormsDAM['Qsum']/1000,
    'Qtotal':StormsLBJ['Qsum']/1000,'Psum':StormsLBJ['Psum']}).dropna()
    ## Calculate Q from just Lower watershed
    diff['Qupper']=diff['Qupper'].apply(np.int) #m3
    diff['Qtotal']=diff['Qtotal'].apply(np.int) # m3
    diff['Qlower']=diff['Qtotal'] - diff['Qupper']
    ## Calculate percentages
    diff['% Upper'] = diff['Qupper']/diff['Qtotal']*100
    diff['% Upper'] = diff['% Upper'].round(0)
    diff['% Lower'] = diff['Qlower']/diff['Qtotal']*100
    diff['% Lower'] = diff['% Lower'].round(0)
    diff['Psum'] = diff['Psum'].apply(np.int)
    diff['Storm#']=range(1,len(diff)+1)
    ## add summary stats to bottom of table
    diff=diff.append(pd.DataFrame({'Storm#':'-','Psum':'-','Qupper':'-','Qlower':'-','Qtotal':'Average:','% Upper':'%.1f'%diff['% Upper'].mean(),'% Lower':'%.1f'%diff['% Lower'].mean()},index=['']))
    ## Build table
    nrows, ncols = len(diff),len(diff.columns)
    hcell, wcell=0.2,1
    hpad, wpad = .8,.5
    fig = plt.figure(figsize=(ncols*wcell+wpad,nrows*hcell+hpad)) 
    ax = fig.add_subplot(111)
    ax.patch.set_visible(False), ax.axis('off')
    ax.xaxis.set_visible(False), ax.yaxis.set_visible(False)
    celldata = np.array(diff[['Storm#','Psum','Qupper','Qlower','Qtotal','% Upper','% Lower']].values)
    ax.table(cellText=celldata,rowLabels=[pd.to_datetime(t) for t in diff.index.values],colLabels=['Storm#','Precip(mm)','Upper(m3)','Lower(m3)','Total(m3)','%Upper','%Lower'],loc='center')
    plt.suptitle("Discharge (Q) from Upstream (DAM) and Downstream (LBJ) watersheds in Faga'alu")
    plt.draw()
    if show==True:
        plt.show()
    return
#plotQ_storm_table(True)