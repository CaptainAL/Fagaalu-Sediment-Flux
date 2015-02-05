# -*- coding: utf-8 -*-
"""
Created on Wed Dec 03 20:32:00 2014

@author: Alex
"""

## PT3 DAM
# tshift in 15Min(or whatever the timestep is), zshift in cm
PT3aa = PT_Hobo(allbaro,'PT3a Dam',XL,'PT-Fagaalu3aa',12,zshift=-3.75)
PT3ab = PT_Hobo(allbaro,'PT3a Dam',XL,'PT-Fagaalu3ab',12,zshift=-3.75)
PT3b = PT_Levelogger(allbaro,'PT3b Dam',XL,'PT-Fagaalu3b',0,zshift=-23)
PT3c = PT_Levelogger(allbaro,'PT3c Dam',XL,'PT-Fagaalu3c',0,zshift=-19.5)
PT3d = PT_Levelogger(allbaro,'PT3d Dam',XL,'PT-Fagaalu3d',0,zshift=-17.1)
PT3e = PT_Levelogger(allbaro,'PT3e Dam',XL,'PT-Fagaalu3e',0,zshift=-18.4)
PT3f = PT_Levelogger(allbaro,'PT3f Dam',XL,'PT-Fagaalu3f',0,zshift=-17)
PT3g = PT_Levelogger(allbaro-1.5,'PT3g Dam',XL,'PT-Fagaalu3g',0,zshift=-10.5)
PT3 = pd.concat([PT3a,PT3b,PT3c,PT3d,PT3e,PT3f,PT3g])
PT3 = PT3[PT3>0]

#storm_data=pd.DataFrame(columns=['DAM-Sed','DAM-Sed-cum','DAMgrab','DAMgrabSed','DAMgrabssc', 
    'DAMntu','DAMq','DAMssc','DAMtSed','DAMtssc','LBJ-Sed','LBJ-Sed-cum','LBJfnu','LBJgrab',
    'LBJgrabSed','LBJgrabssc','LBJntu','LBJq','LBJssc','LBJtSed','LBJtssc','Precip',
    'QUARRY-Sed','QUARRY-Sed-cum','QUARRYfnu','QUARRYgrab','QUARRYgrabSed','QUARRYgrabssc',
    'QUARRYq','QUARRYssc','QUARRYtSed','QUARRYtssc'],
    index=pd.date_range(start2012,stop2014,freq='15Min'))
    
data = pd.DataFrame({'Precip':Precip['Timu1-15'][start:end],
        'LBJq':LBJ['Q'][start:end],'QUARRYq':QUARRY['Q'][start:end],'DAMq':DAM['Q'][start:end],
        'LBJntu':LBJ['YSI-NTU'],'LBJfnu':LBJ['OBS-FNU'],'DAMntu':DAM['NTU'],
        'LBJssc':LBJ['SSC-mg/L'][start:end],'QUARRYssc':QUARRY['SSC-mg/L'][start:end],'DAMssc':DAM['SSC-mg/L'][start:end],
        'LBJgrabssc':LBJ['Grab-SSC-mg/L'][start:end],'QUARRYgrabssc':QUARRY['Grab-SSC-mg/L'][start:end],'DAMgrabssc':DAM['Grab-SSC-mg/L'][start:end],
        'LBJ-Sed':LBJ['SedFlux-tons/15min'][start:end],'QUARRY-Sed':QUARRY['SedFlux-tons/15min'][start:end],
        'DAM-Sed':DAM['SedFlux-tons/15min'][start:end],
        'LBJgrab':LBJgrab['SSC (mg/L)'][start:end],'QUARRYgrab':QUARRYgrab['SSC (mg/L)'][start:end],
        'DAMgrab':DAMgrab['SSC (mg/L)'][start:end]},index=pd.date_range(start,end,freq='15Min')) 
   
    
data = pd.DataFrame({'Precip':Precip['Timu1-15'][start:end].dropna(),
        'LBJq':LBJ['Q'][start:end],'QUARRYq':QUARRY['Q'][start:end],'DAMq':DAM['Q'][start:end],
        'LBJgrab':LBJgrab['SSC (mg/L)'][start:end],'QUARRYgrab':QUARRYgrab['SSC (mg/L)'][start:end],'DAMgrab':DAMgrab['SSC (mg/L)'][start:end],        
        'LBJntu':LBJ['YSI-NTU'][start:end],'LBJfnu':LBJ['OBS-FNU'][start:end],'QUARRYfnu':QUARRY['OBS-FNU'][start:end],'DAMntu':DAM['NTU'][start:end],
        'LBJtssc':LBJ['T-SSC-mg/L'][start:end],'QUARRYtssc':QUARRY['T-SSC-mg/L'][start:end],'DAMtssc':DAM['T-SSC-mg/L'][start:end],
        'LBJtSed':LBJ['T-SedFlux-tons/sec'][start:end],'QUARRYtSed':QUARRY['T-SedFlux-tons/sec'][start:end],'DAMtSed':DAM['T-SedFlux-tons/sec'][start:end],
        'LBJgrabssc':LBJ['Grab-SSC-mg/L'][start:end],'QUARRYgrabssc':QUARRY['Grab-SSC-mg/L'][start:end],'DAMgrabssc':DAM['Grab-SSC-mg/L'][start:end],        
        'LBJgrabSed':LBJ['Grab-SedFlux-tons/sec'][start:end],'QUARRYgrabSed':QUARRY['Grab-SedFlux-tons/sec'][start:end],'DAMgrabSed':DAM['Grab-SedFlux-tons/sec'][start:end],
        'LBJssc':LBJ['SSC-mg/L'][start:end],'QUARRYssc':QUARRY['SSC-mg/L'][start:end],'DAMssc':DAM['SSC-mg/L'][start:end],
        'LBJ-Sed':LBJ['SedFlux-tons/sec'][start:end],'QUARRY-Sed':QUARRY['SedFlux-tons/sec'][start:end],'DAM-Sed':DAM['SedFlux-tons/sec'][start:end],
        'LBJ-Sed-cum':LBJ['SedFlux-tons/15min'][start:end].cumsum(),'QUARRY-Sed-cum':QUARRY['SedFlux-tons/15min'][start:end].cumsum(),
        'DAM-Sed-cum':DAM['SedFlux-tons/15min'][start:end].cumsum()},index=pd.date_range(start,end,freq='15Min'))


        ## Summary stats
        total_storm = len(data[start:end])
        percent_P = len(data['Precip'].dropna())/total_storm *100.
        percent_Q_LBJ = len(data['LBJq'].dropna())/total_storm * 100.
        percent_Q_DAM = len(data['DAMq'].dropna())/total_storm * 100.
        count_LBJgrab = len(LBJgrab.dropna())
        count_QUARRYgrab = len(QUARRYgrab.dropna())
        count_DAMgrab = len(DAMgrab.dropna())
        percent_SSC_LBJ = len(data['LBJssc'].dropna())/total_storm * 100.
        percent_SSC_DAM = len(data['DAMssc'].dropna())/total_storm * 100.
        percent_SED_LBJ = len(data['LBJ-Sed'].dropna())/total_storm * 100.
        percent_SED_DAM = len(data['DAM-Sed'].dropna())/total_storm * 100.
        if print_stats==True:
            print str(start)+' '+str(end)+' Storm#:'+str(count)
            print '%P:'+str(percent_P)+' %Q_LBJ:'+str(percent_Q_LBJ)+' %Q_DAM:'+str(percent_Q_DAM)
            print '%SSC_LBJ:'+str(percent_SSC_LBJ)+' %SSC_DAM:'+str(percent_SSC_DAM)
            print '#LBJgrab:'+str(count_LBJgrab)+' #QUARRYgrab:'+str(count_QUARRYgrab)+' #DAMgrab:'+str(count_DAMgrab)        
        ## Calculate Event Mean Concentration
        if len(data['DAMgrab'])>=3:
            data['sEMC-DAM']=data['DAMgrab'].mean()
        if len(data['QUARRYgrab'])>=3:
            data['sEMC-QUARRY']=data['QUARRYgrab'].mean()
        if len(data['QUARRYgrab'])>=3:
            data['sEMC-LBJ']=data['LBJgrab'].mean()
        ## Make sure data is complete for storms
        if percent_Q_LBJ <= 95:
            data['LBJq'] = np.nan
        if percent_Q_DAM <= 95:
            data['DAMq'] = np.nan
        if percent_SSC_LBJ <= 95:
            data['LBJssc'] = np.nan
        if percent_SSC_LBJ <= 95:
            data['LBJssc'] = np.nan
        if percent_SSC_DAM <= 95:
            data['DAMssc'] = np.nan
        if percent_SED_LBJ <= 95:
            data['LBJ-Sed'] = np.nan
        if percent_SED_DAM <= 95:
            data['DAM-Sed'] = np.nan    
        if data['LBJ-Sed'].sum() < 0:
            data['LBJ-Sed'] = np.nan
        if data['LBJ-Sed'].sum() < 0:
            data['LBJ-Sed'] = np.nan