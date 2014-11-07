import pandas as pd
from pandas import DataFrame
import numpy as np
import dateutil
import datetime as dt

def WeatherStation(XL,sheet=''):
    print 'loading Wx: '+sheet+'...'
    ## Fagaalu Weather Station
    my_parser= lambda x,y: dt.datetime.strptime(x+y,"%m/%d/%Y%I:%M %p")
    Wx= XL.parse(sheet,skiprows=1,header=0,parse_cols='A:AD',parse_dates=[['Date','Time']],index_col=['Date_Time'],na_values=['---'])
    Wx.columns=['TempOut', 'HiTemp', 'LowTemp', 'OutHum', 'DewPt', 'WindSpeed', 'WindDir', 'WindRun', 'HiSpeed', 'HiDir', 'WindChill', 'HeatIndex', 'THWIndex', 'Bar', 'Rain', 'RainRate', 'HeatD-D', 'CoolD-D', 'InTemp', 'InHum', 'InDew', 'InHeat', 'InEMC', 'InAirDensity', 'WindSamp', 'WindTx', 'ISSRecept', 'Arc.Int.']
    return Wx

def PT_Hobo(allbaro,PTname,XL,sheet='',tshift=0,zshift=0): # tshift in 15Min(or whatever the timestep is), zshift in cm
    print 'loading HOBO PT: '+sheet+'...'
    PT = XL.parse(sheet,header=1,index_col=0,parse_cols='B,C',parse_dates=True)
    PT.columns=['Pressure']
    PT=PT.resample('15Min',how='mean')
    PT=PT.shift(tshift) ## shift by 3 hours (12 x 15minutes)
    PT['barodata']=allbaro['Baropress']
    PT['stage']=(PT['Pressure']-PT['barodata'])/9.81*100.0
    #PT['stage']=PT['stage'].where(PT['stage']>0,PT['barodata']) ## filter negative values
    PT['stage']=PT['stage'].round(1)  
    PT['stage']=PT['stage']+zshift
    
    return PT

def PT_Levelogger(allbaro,PTname,XL,sheet,tshift=0,zshift=0): # tshift in hours, zshift in cm
    print 'loading Levelogger PT: '+sheet+'...'
    PT = XL.parse(sheet,header=11,parse_cols='A,B,D',parse_dates=[['Date','Time']],index_col=['Date_Time'])
    PT.columns= ['LEVEL']
    PT=PT.resample('15Min',how='mean')
    PT['barodata']=allbaro['Baropress']
    PT=PT.shift(tshift) ## shift by 3 hours (12 x 15minutes)
    PT['stage']=(PT['LEVEL']-PT['barodata'])/9.81*100.0
    #PT['stage']=PT['stage'].where(PT['stage']>0,0) ## filter negative values
    PT['stage']=PT['stage'].round(1)  
    PT['stage']=PT['stage']+zshift
    return PT

#FP = WeatherStation()
#allbaro= DataFrame(FP['Bar']/10)
#allbaro = allbaro.asfreq('15Min')
#allbaro = allbaro.fillna(method='pad',limit=2)
#allbaro['ndbc'] = ndbc() ## ndbc() returns a Series; add NDBC data 
#allbaro['TULAbaro']=Tula() ## add TULA barometer data
#allbaro.reindex(pd.date_range(min(allbaro.index),max(allbaro.index)))
#allbaro['Baropress']=allbaro['Bar'].where(allbaro['Bar']>0,allbaro['ndbc']) ## create a new column and fill with FP or NDBC
#allbaro['Baropress']=allbaro['Baropress'].where(allbaro['Baropress']>0,allbaro['TULAbaro']) ## add TULA data to the new column
#
#PTlevel= PT_Levelogger(allbaro,'PT3b-DAM','C:/Users/Alex/Desktop/samoa/WATERSHED_ANALYSIS/FAGAALU/MasterDataFiles/Fagaalu3b-Master.csv')
#PThoboA = PT_Hobo(allbaro,'PT1-LBJ','C:/Users/Alex/Desktop/samoa/WATERSHED_ANALYSIS/FAGAALU/MasterDataFiles/Fagaalu1a-Master.csv',12)
#PThoboB= PT_Hobo(allbaro,'PT1-LBJ','C:/Users/Alex/Desktop/samoa/WATERSHED_ANALYSIS/FAGAALU/MasterDataFiles/Fagaalu1b-Master.csv',4)
#PThobo = PThoboA.append(PThoboB)

def TS3000(XL,sheet='DAM-TS3K'):
    print 'loading : '+sheet+'...'
    TS3K = XL.parse(sheet,header=0,parse_cols='A,F',index_col=0,parse_dates=True)
    TS3K.columns=['NTU']
    return TS3K

##TS = TS3000()

def YSI(XL,sheet='LBJ-YSI'):
    print 'loading : '+sheet+'...'
    YSI = XL.parse(sheet,header=4,parse_cols='A:H',parse_dates=[['Date','Time']],index_col=['Date_Time'])
    YSI=YSI.resample('5Min')
    return YSI
    
def OBS(XL,sheet='LBJ-OBS'):
    print 'loading : '+sheet+'...'
    OBS=XL.parse(sheet,header=4,parse_cols='A:L',parse_dates=True,index_col=0)
    return OBS

def loadTSS(TSSXL,sheet='ALL_MASTER'):
    print 'loading TSS...'
    def my_parser(x,y):
        try:
            y = str(int(y))
            while len(y)!=4:
                y = '0'+y
            hour=y[:-2]
            minute=y[-2:]
            time=dt.time(int(hour),int(minute))
            parsed=dt.datetime.combine(x,time)
#            print parsed
        except:
            parsed = pd.to_datetime(np.nan)
        return parsed
            
    TSS= TSSXL.parse(sheet,header=0,parse_dates=[['Date','Time']],date_parser=my_parser,index_col=['Date_Time'])
    return TSS

#TSS = loadTSS()
#datadir = 'C:/Users/Alex/Desktop/'### samoa/
#TSS = loadTSS(datadir+'samoa/WATERSHED_ANALYSIS/TSS/TSS_grab_samples.xls','ALL_MASTER')

def loadTSS2(TSS,sheet='ALL_MASTER'):
    print 'loading TSS...'
    #col_names = ['Date','Time','Location','Sample#','Date Analyzed','Time Analyzed','NTU','Filter Wt mg','mL sample filtered','Wet Filter wt (mg)','Dry Start','Dry Finish','Dry Time','Dried Filter wt (mg)','mg sample','L sample','TSS (mg/L)']
    #my_parser= lambda x,y: dt.datetime.strptime(x+y,"%m/%d/%Y%H%M")
    def my_parser(x,y):
        y = str(int(y))
        while len(y)!=4:
            y = '0'+y
        hour=y[:-2]
        minute=y[-2:]
        time=dt.time(int(hour),int(minute))
        parsed=dt.datetime.combine(x,time)
        #print parsed
        return parsed
    TSS = pd.ExcelFile(path).parse(sheet,header=0,parse_dates=[['Date','Time']],date_parser=my_parser,index_col=['Date_Time'],na_values=['9999'])
    TSS=TSS.drop(TSS.columns[15:],1)
    return TSS

def loadNUTES1(NUTESXL,sheet='by Date'):
    print 'loading NUTES...'
    def my_parser(x,y):
        try:
            y = str(int(y))
            while len(y)!=4:
                y = '0'+y
            hour=y[:-2]
            minute=y[-2:]
            time=dt.time(int(hour),int(minute))
            parsed=dt.datetime.combine(x,time)
#            print parsed
        except:
            parsed = pd.NaT
        return parsed
    NUTES = NUTESXL.parse(sheet,skiprows=5,header=0,parse_cols='A:Q',parse_dates=[['Date','Time']],date_parser=my_parser,index_col=['Date_Time'],na_values=['NS'])
    return NUTES

   
def loadNUTES1mg(NUTESXL,sheet='by_Location'):
    print 'loading NUTES...'
    col_names=['Lab sample #','Date','Time','Location','#','mL','NH4 uM','NO3 uM','PO4 uM','TDN uM','TDP uM']
    def my_parser(x,y):
        y = str(int(y))
        hour=y[:-2]
        minute=y[-2:]
        time=dt.time(int(hour),int(minute))
        parsed=dt.datetime.combine(x,time)
        #print parsed
        return parsed
    Nutes = NUTESXL.parse(sheet,skiprows=1,header=1,parse_cols='A:Q',parse_dates=[['Date','Time']],date_parser=my_parser,index_col=['Date_Time'],names=col_names,na_values=['NS'])
    Nutes['NH4 mg/L']=Nutes['NH4 uM']*(10.0**-6.0)*14.0067*1000.0
    Nutes['NO3 mg/L']=Nutes['NO3 uM']*(10.0**-6.0)*14.0067*1000.0
    Nutes['NH4+NO3 mg/L']=Nutes['NH4 mg/L']+Nutes['NO3 mg/L']
    Nutes['TDN mg/L']=Nutes['TDN uM']*(10.0**-6.0)*14.0067*1000.0
    Nutes['PO4 mg/L']=Nutes['PO4 uM']*(10.0**-6.0)*30.97376*1000.0
    Nutes['TDP mg/L']=Nutes['TDP uM']*(10.0**-6.0)*30.97376*1000.0
    return Nutes 

def loadNUTES2and3(NUTES2XL,NUTES2infoXL):
    def my_parser(x,y):
            y = str(int(y))
            hour=y[:-2]
            minute=y[-2:]
            time=dt.time(int(hour),int(minute))
            parsed=dt.datetime.combine(x,time)
            #print parsed
            return parsed
    ## Sheet of sample data from Lisa Thurn
    NUTES2p = NUTES2XL.parse('P',index_col=['Sample'],parse_cols='A:B')
    NUTES2n = NUTES2XL.parse('N',index_col=['Sample'],parse_cols='A:C')
    NUTES2= NUTES2n.join(NUTES2p) ## there are more N samples than P samples
    ## Sheet of sample metadata submitted to Lisa Thurn, referenced by 'sample' (ie 1.2)
    NUTES2info = NUTES2infoXL.parse('info',parse_cols='A:K',parse_dates=[['DATE','TIME']],date_parser=my_parser,index_col=['Sample'])
    ## Join metadata and data
    NUTES2=NUTES2.join(NUTES2info)
    
    NUTES2=NUTES2[NUTES2['DATE_TIME']!=pd.NaT] ## drop ones without valid timestamps
    NUTES2['Sample']=NUTES2.index ## put 'Sample' in DataFrame as a column
    NUTES2.index=NUTES2['DATE_TIME'] ## reindex with the DATE_TIME instead of 'Sample' number
    return NUTES2
