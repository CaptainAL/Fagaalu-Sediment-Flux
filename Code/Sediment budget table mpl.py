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
    
    
    
def SSY_dist_table_quarry(subset='pre',manual_edit=True):
    S_diff = compile_Storms_data(subset)
    ## Calculate percent contributions from upper and lower watersheds
    S_diff['TOTAL tons']=S_diff['Stotal'].round(2)
    S_diff['UPPER tons']=S_diff['Supper'].round(2)
    #S_diff['FOREST PE %'] = S_diff['Supper_PE'].apply(int)
    S_diff['LOWER_QUARRY tons']=S_diff['Squarry'].round(2) - S_diff['UPPER tons']
    S_diff['LOWER_VILLAGE tons']= S_diff['TOTAL tons'].round(2) - S_diff['UPPER tons'] - S_diff['LOWER_QUARRY tons'] 
    #S_diff['TOTAL PE %'] = S_diff['Stotal_PE'].apply(int)
    S_diff['% UPPER'] = S_diff['UPPER tons']/S_diff['TOTAL tons']*100
    S_diff['% UPPER'] = S_diff['% UPPER'].dropna().apply(int)
    S_diff['% LOWER_QUARRY'] = S_diff['LOWER_QUARRY tons']/S_diff['TOTAL tons']*100
    S_diff['% LOWER_QUARRY'] = S_diff['% LOWER_QUARRY'].dropna().apply(int)    
    S_diff['% LOWER_VILLAGE'] = S_diff['LOWER_VILLAGE tons']/S_diff['TOTAL tons']*100
    S_diff['% LOWER_VILLAGE'] = S_diff['% LOWER_VILLAGE'].dropna().apply(int)
    S_diff['Precip (mm)'] = S_diff['Pstorms'].dropna().apply(int)
    S_diff = S_diff[S_diff['Precip (mm)']>0]
    ## Filter negative values for S at LBJ    
    S_diff = S_diff[S_diff['LOWER_VILLAGE tons']>0]
    S_diff['Storm#']=range(1,len(S_diff)+1) 
    S_diff['Storm Start'] = S_diff.index
    S_diff['Storm Start'] =S_diff['Storm Start'].apply(lambda x: "{:%m/%d/%Y}".format(x))
    ## Select storms with valid data
    if manual_edit == True:
        S_diff = S_diff[S_diff['Storm Start'].isin(['03/06/2013','04/16/2013','04/23/2013','04/30/2013','06/05/2013','02/14/2014','02/20/2014','02/21/2014'])==True]
    ## Summary Stats    
    Percent_Forest = S_diff['UPPER tons'].sum()/S_diff['TOTAL tons'].sum()*100
    Percent_Quarry= S_diff['LOWER_QUARRY tons'].sum()/S_diff['TOTAL tons'].sum()*100
    Percent_Village = S_diff['LOWER_VILLAGE tons'].sum()/S_diff['TOTAL tons'].sum()*100

    ## add summary stats to bottom of table
    # Total/Avg
    SSY_UPPER, SSY_QUARRY, SSY_VILLAGE, SSY_TOTAL = S_diff['UPPER tons'].sum(), S_diff['LOWER_QUARRY tons'].sum(), S_diff['LOWER_VILLAGE tons'].sum(), S_diff['TOTAL tons'].sum()

    # sSSY
    sSSY_UPPER, sSSY_QUARRY, sSSY_VILLAGE, sSSY_TOTAL = SSY_UPPER/0.9, SSY_QUARRY/0.27, SSY_VILLAGE/0.61, SSY_TOTAL/1.78
    
    # sSSY:sSSY_UPPER
    DR_sSSY_UPPER, DR_sSSY_QUARRY, DR_sSSY_VILLAGE, DR_sSSY_TOTAL = sSSY_UPPER/sSSY_UPPER,sSSY_QUARRY/sSSY_UPPER,sSSY_VILLAGE/sSSY_UPPER,sSSY_TOTAL/sSSY_UPPER
    
    # fraction Disturbed = % disturbed from % Disturbed in Land cover table
    lc_table = LandCover_table()
    frac_disturbed_UPPER, frac_disturbed_LOWER_QUARRY, frac_disturbed_LOWER_VILLAGE, frac_disturbed_TOTAL= lc_table.ix[0]['% Disturbed'], lc_table.ix[1]['% Disturbed'], lc_table.ix[2]['% Disturbed'],lc_table.ix[4]['% Disturbed']
    
    SSY_dist = pd.DataFrame({' ':'fraction disturbed (%)','UPPER':"%.1f"%frac_disturbed_UPPER,'LOWER_QUARRY':"%.1f"%frac_disturbed_LOWER_QUARRY,'LOWER_VILLAGE':"%.1f"%frac_disturbed_LOWER_VILLAGE,'TOTAL':"%.1f"%frac_disturbed_TOTAL}, index=['fraction disturbed (%)'])
    
    # SSY from forested areas of subwatersheds = SSY forest (tons) =  sSSY_UPPER x (1-disturbed_fraction) x subwatershed area
    def SSY_from_forest(sSSY_UPPER,disturbed_fraction,subwatershed_area):
        disturbed_fraction= disturbed_fraction/100
        SSY_forest = sSSY_UPPER*(1-disturbed_fraction)*subwatershed_area
        return SSY_forest
    SSY_forest_UPPER,SSY_forest_QUARRY,SSY_forest_VILLAGE, SSY_forest_TOTAL = SSY_from_forest(sSSY_UPPER,frac_disturbed_UPPER,0.9), SSY_from_forest(sSSY_UPPER,frac_disturbed_LOWER_QUARRY,0.27), SSY_from_forest(sSSY_UPPER,frac_disturbed_LOWER_VILLAGE,0.61), SSY_from_forest(sSSY_UPPER,frac_disturbed_TOTAL,1.78)
    
    SSY_dist = SSY_dist.append(pd.DataFrame({' ':'SSY from forested areas (tons)','UPPER':"%.1f"%SSY_forest_UPPER,'LOWER_QUARRY':"%.1f"%SSY_forest_QUARRY,'LOWER_VILLAGE':"%.1f"%SSY_forest_VILLAGE,'TOTAL':"%.1f"%SSY_forest_TOTAL}, index=['SSY from forested areas (tons)']))
    
    # SSY from disturbed areas
    SSY_disturbed_UPPER, SSY_disturbed_QUARRY,SSY_disturbed_VILLAGE,SSY_disturbed_TOTAL = SSY_UPPER-SSY_forest_UPPER, SSY_QUARRY-SSY_forest_QUARRY,SSY_VILLAGE-SSY_forest_VILLAGE, SSY_TOTAL-SSY_forest_TOTAL
    
    SSY_dist = SSY_dist.append(pd.DataFrame({' ':'SSY from disturbed areas (tons)','UPPER':"%.1f"%SSY_disturbed_UPPER,'LOWER_QUARRY':"%.2f"%SSY_disturbed_QUARRY,'LOWER_VILLAGE':"%.1f"%SSY_disturbed_VILLAGE,'TOTAL':"%.1f"%SSY_disturbed_TOTAL}, index=['SSY from disturbed areas (tons)']))
      
    # % from disturbed parts of watershed
    SSY_percent_dist_UPPER, SSY_percent_dist_QUARRY, SSY_percent_dist_VILLAGE, SSY_percent_dist_TOTAL = SSY_disturbed_UPPER/SSY_UPPER*100, SSY_disturbed_QUARRY/SSY_QUARRY*100, SSY_disturbed_VILLAGE/SSY_VILLAGE*100, SSY_disturbed_TOTAL/SSY_TOTAL*100
    
    SSY_dist = SSY_dist.append(pd.DataFrame({' ':'% SSY from disturbed areas','UPPER':"%.1f"%SSY_percent_dist_UPPER,'LOWER_QUARRY':"%.0f"%SSY_percent_dist_QUARRY,'LOWER_VILLAGE':"%.0f"%SSY_percent_dist_VILLAGE,'TOTAL':"%.0f"%SSY_percent_dist_TOTAL}, index=['% SSY from disturbed areas']))  
    
    # sSSY from disturbed areas = SSY_disturbed/(fraction_disturbed x subwatershed area)
    sSSY_disturbed_UPPER, sSSY_disturbed_QUARRY, sSSY_disturbed_VILLAGE, sSSY_disturbed_TOTAL = SSY_disturbed_UPPER/(frac_disturbed_UPPER/100*0.9), SSY_disturbed_QUARRY/(frac_disturbed_LOWER_QUARRY/100*0.27), SSY_disturbed_VILLAGE/(frac_disturbed_LOWER_VILLAGE/100*0.61), SSY_disturbed_TOTAL/(frac_disturbed_TOTAL/100*1.78)
    
    SSY_dist = SSY_dist.append(pd.DataFrame({' ':'sSSY from disturbed areas (tons/km2)','UPPER':"%.1f"%sSSY_disturbed_UPPER,'LOWER_QUARRY':"%.1f"%sSSY_disturbed_QUARRY,'LOWER_VILLAGE':"%.1f"%sSSY_disturbed_VILLAGE,'TOTAL':"%.1f"%sSSY_disturbed_TOTAL}, index=['sSSY from disturbed areas (tons/km2)']))        
 
    # sSSY_DR
    sSSY_DR_QUARRY, sSSY_DR_VILLAGE, sSSY_DR_TOTAL= sSSY_disturbed_QUARRY/sSSY_UPPER, sSSY_disturbed_VILLAGE/sSSY_UPPER, sSSY_disturbed_TOTAL/sSSY_UPPER
    
    SSY_dist = SSY_dist.append(pd.DataFrame({' ':'DR for sSSY from disturbed areas','UPPER':'','LOWER_QUARRY':"%.1f"%sSSY_DR_QUARRY,'LOWER_VILLAGE':"%.1f"%sSSY_DR_VILLAGE,'TOTAL':"%.1f"%sSSY_DR_TOTAL}, index=['DR for sSSY from disturbed areas']))     
    
    QUARRY_percent_of_TOTAL_SSY = SSY_disturbed_QUARRY/SSY_TOTAL * 100
    VILLAGE_percent_of_TOTAL_SSY = SSY_disturbed_VILLAGE/SSY_TOTAL * 100
    QUA_VIL_percent_of_TOTAL_SSY = (SSY_disturbed_QUARRY+SSY_disturbed_VILLAGE)/SSY_TOTAL * 100
    
    # Order columns    
    SSY_dist = SSY_dist[[' ','UPPER','LOWER_QUARRY','LOWER_VILLAGE','TOTAL']]
    return SSY_dist, "%.0f"%QUARRY_percent_of_TOTAL_SSY, "%.0f"%VILLAGE_percent_of_TOTAL_SSY, "%.0f"%QUA_VIL_percent_of_TOTAL_SSY
#SSY_dist_table_quarry(manual_edit=False)
SSY_dist_table_quarry(manual_edit=True)