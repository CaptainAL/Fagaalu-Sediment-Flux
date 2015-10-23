# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 16:31:54 2015

@author: Alex
"""
## A bunch of Sediment or Discharge Budget tables in mpl; changed over to htmlTable in R

## Plot sediment budget table in matplotlib; changed to htmlTable in R


## Calculate the percent of total SSY with raw vales, BEFORE NORMALIZING by area!
def plotS_storm_table(show=False):
    diff = compile_Storms_data()
    diff = diff[diff['Stotal']>0]
    diff = diff[diff['Supper']>0]
    ## Calculate percent contributions from upper and lower watersheds
    diff['Supper']=diff['Supper'].round(3)
    diff['Slower']=diff['Slower'].round(3)
    diff['Stotal']=diff['Stotal'].round(3)
    diff['% Upper'] = diff['Supper']/diff['Stotal']*100
    diff['% Upper'] = diff['% Upper'].apply(np.int)
    diff['% Lower'] = diff['Slower']/diff['Stotal']*100
    diff['% Lower'] = diff['% Lower'].apply(np.int)
    diff['Psum'] = diff['Pstorms'].apply(int)
    diff['Storm#']=range(1,len(diff)+1) 
    ## Filter negative values for S at LBJ    
    diff = diff[diff['Slower']>0]
    ## add summary stats to bottom of table
    diff=diff.append(pd.DataFrame({'Storm#':'-','Psum':'-','Supper':'-','Slower':'-','Stotal':'Average:','% Upper':'%.1f'%diff['% Upper'].mean(),'% Lower':'%.1f'%diff['% Lower'].mean()},index=[pd.NaT]))
    diff.to_excel(datadir+'Storm S table.xlsx')
    ## BUild table
    nrows, ncols = len(diff),len(diff.columns)
    hcell, wcell=0.2,1
    hpad, wpad = .8,.5
    fig = plt.figure(figsize=(ncols*wcell+wpad,nrows*hcell+hpad)) 
    ax = fig.add_subplot(111)
    ax.patch.set_visible(False), ax.axis('off')
    ax.xaxis.set_visible(False), ax.yaxis.set_visible(False)
    plt.suptitle("Sediment Loading from subwatersheds in Faga'alu",fontsize=16)
 
    celldata = np.array(diff[['Storm#','Psum','Supper','Slower','Stotal','% Upper','% Lower']].values)
    rowlabels=[pd.to_datetime(t).strftime('%Y %b %d %H:%M') for t in diff.index[diff.index!=pd.NaT].values]
    rowlabels.extend([None])
    ax.table(cellText=celldata,rowLabels=rowlabels,colLabels=['Storm#','Precip(mm)','Upper (Mg)','Lower (Mg)','Total (Mg)','%Upper','%Lower'],loc='center',fontsize=16)
    
    plt.draw()
    if show==True:
        plt.show()
    return
#plotS_storm_table(show=True)
    


def Q_S_storm_diff_summary_table(subset='pre'):
    diff = compile_Storms_data(subset)
    ## Calculate percent contributions from upper and lower watersheds
    
    # Precip
    diff['Psum'] = diff['Pstorms'].dropna().apply(int)
    diff = diff[diff['Psum']>0]
    ## Q discharge
    diff['QupperMCM'] = diff['Qsumupper']/10.**6.
    diff['QtotalMCM'] = diff['Qsumtotal']/10.**6.    
     ## Q vol (m3) -> Q mm = Qvol(m3)/Watershed area(m2) * 1000mm/m
    diff['mmQupper']=diff['Qsumupper']/900000*1000
    diff['mmQtotal']=diff['Qsumtotal']/1780000*1000
    ## Sediment
    diff['Supper']=diff['Supper'].round(3)
    diff['Stotal']=diff['Stotal'].round(3)
    ## SSY Norm by Area
    diff['km2Supper'] = diff['Supper']/.9
    diff['km2Stotal'] = diff['Stotal']/1.78
    ## Filter negative values for S at LBJ (and getting rid of NaNs)    
    diff = diff[diff['Slower']>0]  
    ## Number Storms
    diff['Storm#']=range(1,len(diff)+1)  
    ## Disturbance Ratio
    SSYpre = 1.78 * diff['km2Supper'].sum()
    SSY = diff['Stotal'].sum()
    SSY_DR = SSY/SSYpre
    ## Q Disturbance Ratio
    Qpre = 1.78 * (diff['QupperMCM'].sum()/.9)
    Q = diff['QtotalMCM'].sum()
    Q_DR = Q/Qpre   

    ## Summarize
    table_data_dict = {
    'Storms':(len(diff),''),
    'Precipitation (mm)':('%.0f'%diff['Pstorms'].sum(),''),
    'subwatershed':('UPPER','LOWER'),
    'Q (MCM)':('%.2f'%diff['QupperMCM'].sum(),'%.2f'%diff['QtotalMCM'].sum()),
    'Q (mm)':('%.0f'%diff['mmQupper'].sum(),'%.0f'%diff['mmQtotal'].sum()),
    'Q Disturbance Ratio':('-','%.1f'%Q_DR),
    'SSY (Mg)':('%.1f'%diff['Supper'].sum(),'%.1f'%diff['Stotal'].sum()),
    'Spec SSY (Mg/km2)':('%.1f'%diff['km2Supper'].sum(),'%.1f'%diff['km2Stotal'].sum()),
    'SSY Disturbance Ratio':('-','%.1f'%SSY_DR)}
    
    summary =pd.DataFrame(table_data_dict,index=[str(n) for n in range(1,3)])[['Storms','Precipitation (mm)','subwatershed','Q (MCM)','Q (mm)','Q Disturbance Ratio','SSY (Mg)','Spec SSY (Mg/km2)','SSY Disturbance Ratio']].T
    summary['0'] = summary.index
    return summary[['0','1', '2']]
Q_S_storm_diff_summary_table()

def Spec_SSY_Quarry(subset='post'):
    diff = compile_Storms_data(subset)

    diff['QUARRY tons']=diff['Squarry'].round(3) - diff['Supper'].round(3)
    diff['km2SQUARRY'] = diff['QUARRY tons']/.27 #km2
    diff = diff[diff['QUARRY tons']>0]
    diff['km2SUPPER'] =  diff['Supper'].round(3)/.9 #km2
    percent_increase  = diff['km2SQUARRY'].sum()/diff['km2SUPPER'].sum() *100
    return '%.1f'%diff['km2SUPPER'].sum()+r'Mg/km^2', '%.1f'%diff['km2SQUARRY'].sum()+r'Mg/km2', "%.0f"%percent_increase
#Spec_SSY_Quarry()    

def plotS_storm_table_summary(fs=16,show=False):
    diff = compile_Storms_data().dropna()
    ## Calculate percent contributions from upper and lower watersheds
    ## Sediment
    diff['Supper']=diff['Supper'].round(3)
    diff['Slower']=diff['Slower'].round(3)
    diff['Stotal']=diff['Stotal'].round(3)
    diff['% Upper'] = diff['Supper']/diff['Stotal']*100
    diff['% Upper'] = diff['% Upper'].apply(np.int)
    diff['% Lower'] = diff['Slower']/diff['Stotal']*100
    diff['% Lower'] = diff['% Lower'].apply(np.int)
    ## Q discharge
    diff['Qupper']=diff['Qsumupper'].round(3)
    diff['Qlower']=diff['Qsumlower'].round(3)
    diff['Qtotal']=diff['Qsumtotal'].round(3)
    
    diff['Psum'] = diff['Pstorms'].apply(int)
    diff['Storm#']=range(1,len(diff)+1) 
    ## Filter negative values for S at LBJ    
    diff = diff[diff['Slower']>0]
    ## add summary stats to bottom of table
    diff=pd.DataFrame({'Storm#':len(diff),'Psum':diff['Pstorms'].sum(),
    'Qupper':diff['Qupper'].sum(),'Qlower':diff['Qlower'].sum(),'Qtotal':diff['Qtotal'].sum(),
    'Supper':diff['Supper'].sum(),'Slower':diff['Slower'].sum(),
    'Stotal':diff['Stotal'].sum(),'% Upper':'%.1f'%diff['% Upper'].mean(),
    '% Lower':'%.1f'%diff['% Lower'].mean()},index=[pd.NaT])
    ## Q vol (m3) -> Q mm = Qvol(m3)/Watershed area(m2) * 1000mm/m
    diff['mmQupper']=diff['Qupper']/900000*1000
    diff['mmQlower']=diff['Qlower']/880000*1000
    diff['mmQtotal']=diff['Qtotal']/1780000*1000
    diff.to_excel(datadir+'S storm table summary.xlsx')
    ## BUild table
    nrows, ncols = len(diff),len(diff.columns)
    hcell, wcell=0.3,1
    hpad, wpad = .5,.3
    fig = plt.figure(figsize=(ncols*wcell+wpad,nrows*hcell+hpad)) 
    ax = fig.add_subplot(111)
    ax.patch.set_visible(False), ax.axis('off')
    ax.xaxis.set_visible(False), ax.yaxis.set_visible(False)
    plt.suptitle("Sediment Loading from subwatersheds in Faga'alu",fontsize=16)
 
    celldata = np.array(diff[['Storm#','Psum','Qupper','Qlower','Qtotal',
    'mmQupper','mmQlower','mmQtotal',
    'Supper','Slower','Stotal','% Upper','% Lower']].values)
    rowlabels=[pd.to_datetime(t).strftime('%Y %b %d %H:%M') for t in diff.index[diff.index!=pd.NaT].values]
    rowlabels.extend([None])
    the_table=ax.table(cellText=celldata,rowLabels=rowlabels,colLabels=['Storms','Precip(mm)',
    'Q For(m3)','Q For-Vil (m3)','Q Vil(m3)','Q For(mm)','Q For-Vil (mm)','Q Vil(mm)','Upper (Mg)','Lower (Mg)','Total (Mg)','%Upper','%Lower'],loc='center')
    the_table.set_fontsize(fs)
    the_table.scale(1.5, 1.5)
    show_plot(show)
    return
#plotS_storm_table_summary(fs=22,show=True) 