# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 06:44:22 2015

@author: Alex
"""

### Long term rainfall records

TutPrecipXL =  pd.ExcelFile(datadir+'PRECIP/Tutuila-precipitation.xlsx')
def plot_prob_occurrence(sheet_name):
    P_Station= TutPrecipXL.parse(sheet_name,header=14,skiprows=[15],parse_cols='C:D',parse_dates=['datetime'],index_col=['datetime'])
    P_Station.columns=['PrecipDailyIn']
    P_Station['PrecipDailymm'] = P_Station['PrecipDailyIn']   *25.4
    
    P_Station = P_Station.dropna().sort(columns=['PrecipDailymm'],ascending=False)##ascending=False means highest values at top
    P_Station['rank'] = range(1,len(P_Station)+1)
    P_Station_n = len(P_Station)
    ## Calculate Prob of Occurrence and Return Interval(Tr)
    P_Station['ProbOcc']=P_Station['rank']/(P_Station_n + 1.)
    P_Station['Tr']=(P_Station_n +1.)/P_Station['rank']
    
    fig, ax=plt.subplots(1)
    plt.scatter(P_Station['PrecipDailymm'],P_Station['ProbOcc'])
    plt.ylabel('Prob. of Occurrence: % of time the precip value will be exceeded')
    plt.xlabel('Precipitation (mm)')
    ax.set_xlim(-5,500), ax.set_ylim(-.05,1.1)
    
    data_days= str(len(P_Station))
    data_years= str(len(P_Station)//365)
    plt.title(sheet_name+' '+data_days+' days of data('+data_years+' years)')
    fig.tight_layout()
    return P_Station
    
#VaipitoRes =plot_prob_occurrence('VaipitoRes')
#Afono= plot_prob_occurrence('Pioa-Afono')
#Aunuu = plot_prob_occurrence('Aunuu')
#Malaeimi = plot_prob_occurrence('Malaeimi-Mapusaga')

def prob_occurrence():
    P_Station= pd.DataFrame(Precip['Timu1daily'].dropna())
    P_Station.columns=['PrecipDailymm']
    
    P_Station = P_Station.dropna().sort(columns=['PrecipDailymm'],ascending=False)##ascending=False means highest values at top
    P_Station['rank'] = range(1,len(P_Station)+1)
    P_Station_n = len(P_Station)
    ## Calculate Prob of Occurrence and Return Interval(Tr)
    P_Station['ProbOcc']=P_Station['rank']/(P_Station_n + 1.)
    P_Station['Tr']=(P_Station_n +1.)/P_Station['rank']
    
    fig, ax=plt.subplots(1)
    plt.scatter(P_Station['PrecipDailymm'],P_Station['ProbOcc'])
    plt.ylabel('Prob. of Occurrence: % of time the precip value will be exceeded')
    plt.xlabel('Precipitation (mm)')
    ax.set_xlim(-5,500), ax.set_ylim(-.05,1.1)
    
    data_days= str(len(P_Station))
    data_years= str(len(P_Station)//365)
    plt.title(data_days+' days of data('+data_years+' years)')
    fig.tight_layout()
    return P_Station
#prob_occurrence()

