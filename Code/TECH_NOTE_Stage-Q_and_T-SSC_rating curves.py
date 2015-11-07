# -*- coding: utf-8 -*-
"""
Created on Fri Nov 06 08:33:49 2015

@author: Alex
"""
## TECHNICAL NOTE
## Stage-Discharge and Turbidity-SSC rating curve constructions

## Based off Duvert 2010 and Duvert 2010 tech note

## Goal: document the development of stage-Q and T-SSC rating curves in Faga'alu (maybe another one for Nuuuli)


### LOAD FIELD DATA
if 'XL' not in locals():
    print 'opening MASTER_DATA excel file...'+dt.datetime.now().strftime('%H:%M:%S')
    XL = pd.ExcelFile(datadir+'MASTER_DATA_FAGAALU.xlsx')
if 'XL' in locals():
    print 'MASTER_DATA opened: '+dt.datetime.now().strftime('%H:%M:%S')    
    

#### Import WX STATION Data
#from load_from_MASTER_XL import WeatherStation
def WeatherStation(XL,sheet=''):
    print 'loading Wx: '+sheet+'...'
    ## Fagaalu Weather Station
    #my_parser= lambda x,y: dt.datetime.strptime(x+y,"%m/%d/%Y%I:%M %p")
    Wx= XL.parse(sheet,skiprows=1,header=0,parse_cols='A:AD',parse_dates=[['Date','Time']],index_col=['Date_Time'],na_values=['---'])
    Wx.columns=['TempOut', 'HiTemp', 'LowTemp', 'OutHum', 'DewPt', 'WindSpeed', 'WindDir', 'WindRun', 'HiSpeed', 'HiDir', 'WindChill', 'HeatIndex', 'THWIndex', 'Bar', 'Rain', 'RainRate', 'HeatD-D', 'CoolD-D', 'InTemp', 'InHum', 'InDew', 'InHeat', 'InEMC', 'InAirDensity', 'WindSamp', 'WindTx', 'ISSRecept', 'Arc.Int.']
    return Wx
    
if 'FP' not in locals():
    print 'Opening Weather Station data...'
    FPa = WeatherStation(XL,'FP-30min')
    Bar15Min=FPa['Bar'].resample('15Min',fill_method='pad',limit=2) ## fill the 30min Barometric intervals to 15minute, but not Precip!
    FPa = FPa.resample('15Min')
    FPa['Bar']=Bar15Min
    FPb = WeatherStation(XL,'FP-15min')
    FP = FPa.append(FPb)
    
    
#### Import BAROMETRIC Data: NDBC

##load data from NDBC NSTP6 station at DMWR, Pago Harbor
## To get more NSTP6 data either go to their website and copy and paste the historical data
## or use wundergrabber_NSTP6-REALTIME.py and copy and paste frome the .csv
def ndbc(datafile = datadir+'BARO/NSTP6/NSTP6-2012-14.xlsx'):
    print 'Loading NDBC NSTP6 barometric data...'
    try:
        ndbc_data = pd.DataFrame.from_csv(datadir+'BARO/NSTP6/NDBC_Baro.csv')
    except:
        ndbcXL = pd.ExcelFile(datafile)
        ndbc_parse = lambda yr,mo,dy,hr,mn: dt.datetime(yr,mo,dy,hr,mn)
        ndbc_data = ndbcXL.parse('NSTP6-2012-14',header=0,skiprows=1,parse_dates=[['#yr','mo','dy','hr','mn']],index_col=0,date_parser=ndbc_parse,
                             na_values=['9999','999','99','99.0'])
        ndbc_data.to_csv(datadir+'BARO/NSTP6/NDBC_Baro.csv')
    #local = pytz.timezone('US/Samoa')
    #ndbc_data.index = ndbc_data.index.tz_localize(pytz.utc).tz_convert(local)
    print 'NDBC loaded'
    return ndbc_data

NDBCbaro = ndbc(datafile = datadir+'BARO/NSTP6/NSTP6-2012-14.xlsx')
NDBCbaro = NDBCbaro['hPa'].resample('15Min')
NDBCbaro = NDBCbaro.interpolate(method='linear',limit=4)
NDBCbaro.columns=['NDBCbaro']
NDBCbaro=NDBCbaro.shift(-44) ## UTC to Samoa local  =11 hours =44x15min
NDBCbaro = NDBCbaro-.022

## Barologger at  LBJ
def barologger(XL,sheet=''):
    print 'loading Wx: '+sheet+'...'
    ## Fagaalu Weather Station
    #my_parser= lambda x,y: dt.datetime.strptime(x+y,"%m/%d/%Y%I:%M %p")
    Baro=  XL.parse(sheet,header=11,parse_cols='A,B,D',parse_dates=[['Date','Time']],index_col=['Date_Time'])
    Baro.columns= ['LEVEL']
    Baro=Baro.resample('15Min',how='mean')
    return Baro
    
BaroLogger = barologger(XL,'Fagaalu1-Barologger')
 
## Build data frame of barometric data: Make column 'baropress' with best available data
 ## Fill priority = FP,NDBC,TAFUNA,TULA (TAFUNA and TULA have been deprecated, reside in other scripts)
allbaro = pd.DataFrame(NDBCbaro/10).reindex(pd.date_range(start2012,stop2014,freq='15Min'))
allbaro['FPbaro']=FP['Bar']/10
allbaro['NDBCbaro']=NDBCbaro/10
allbaro['BaroLogger']=BaroLogger

## create a new column and fill with FP or Barologger
allbaro['Baropress']=allbaro['FPbaro'].where(allbaro['FPbaro']>0,allbaro['BaroLogger']) 
## create a new column and fill with FP or NDBC
allbaro['Baropress']=allbaro['Baropress'].where(allbaro['Baropress']>0,allbaro['NDBCbaro']) 


#### Import PT Data
# ex. PT_Levelogger(allbaro,PTname,datapath,tshift=0,zshift=0): 
#from load_from_MASTER_XL import PT_Hobo,PT_Levelogger
def PT_Hobo(allbaro,PTname,XL,sheet='',tshift=0,zshift=0): # tshift in 15Min(or whatever the timestep is), zshift in cm
    print 'loading HOBO PT: '+sheet+'...'
    PT = XL.parse(sheet,header=1,index_col=0,parse_cols='B,C',parse_dates=True)
    PT.columns=['Pressure']
    PT=PT.resample('15Min',how='mean')
    PT=PT.shift(tshift) ## shift by 3 hours (12 x 15minutes)
    PT['barodata']=allbaro['Baropress']
    PT['stage(cm)']=(PT['Pressure']-PT['barodata'])*.102*100.0 ## hPa  to cm
    #PT['stage']=PT['stage'].where(PT['stage']>0,PT['barodata']) ## filter negative values
    PT['stage(cm)']=PT['stage(cm)'].round(1)  
    PT['stage(cm)']=PT['stage(cm)']+zshift
    PT['Uncorrected_stage']=PT['stage(cm)'].round(0)
    return PT

def PT_Levelogger(allbaro,PTname,XL,sheet,tshift=0,zshift=0): # tshift in hours, zshift in cm
    print 'loading Levelogger PT: '+sheet+'...'
    PT = XL.parse(sheet,header=11,parse_cols='A,B,D',parse_dates=[['Date','Time']],index_col=['Date_Time'])
    PT.columns= ['LEVEL']
    PT=PT.resample('15Min',how='mean')
    PT['barodata']=allbaro['Baropress']
    PT=PT.shift(tshift) ## shift by 3 hours (12 x 15minutes)
    PT['stage(cm)']=(PT['LEVEL']-PT['barodata'])*.102*100.0
    #PT['stage']=PT['stage'].where(PT['stage']>0,0) ## filter negative values
    PT['stage(cm)']=PT['stage(cm)'].round(1)  
    PT['stage(cm)']=PT['stage(cm)']+zshift
    PT['Uncorrected_stage']=PT['stage(cm)'].round(0)
    return PT
    
## PT1 LBJ
# tshift in 15Min(or whatever the timestep is), zshift in cm
PT1aa = PT_Hobo(allbaro,'PT1 LBJ bridge',XL,'PT-Fagaalu1aa',tshift=12) #12 x 15min = 3hours (It says it was at GMT-8 instead of GMT-11 but the logger time was set to local anyway)
PT1ab = PT_Hobo(allbaro,'PT1 LBJ bridge',XL,'PT-Fagaalu1ab',tshift=12) #12 x 15min = 3hours (It says it was at GMT-8 instead of GMT-11 but the logger time was set to local anyway)
PT1ba = PT_Hobo(allbaro,'PT1 LBJ bridge',XL,'PT-Fagaalu1ba',tshift=4)
PT1bb = PT_Hobo(allbaro,'PT1 LBJ bridge',XL,'PT-Fagaalu1bb',tshift=4)
PT1bc = PT_Hobo(allbaro,'PT1 LBJ bridge',XL,'PT-Fagaalu1bc',tshift=4)
PT1ca = PT_Hobo(allbaro,'PT1 LBJ bridge',XL,'PT-Fagaalu1ca').truncate(after= dt.datetime(2014,9,23))
PT1cb = PT_Hobo(allbaro,'PT1 LBJ bridge',XL,'PT-Fagaalu1cb')

PT1 = pd.concat([PT1aa,PT1ab,PT1ba,PT1bb,PT1bc,PT1ca,PT1cb])

#rawPT1XL = pd.ExcelFile(datadir+'PT-Fagaalu1-raw.xlsx') 
#rawPT1=pd.DataFrame()
#for sheet_name in rawPT1XL.sheet_names:
#    #print sheet_name
#    sheet = rawPT1XL.parse(sheet_name,header=1,index_col=0,parse_cols='B,C',parse_dates=True)
#    sheet.columns=['Pressure']
#    rawPT1 = rawPT1.append(sheet)

## PT2 QUARRY
# tshift in 15Min(or whatever the timestep is), zshift in cm
PT2 = PT_Levelogger(allbaro,'PT2 Drive Thru',XL,'PT-Fagaalu2',0,-22)

## PT3 DAM
# tshift in 15Min(or whatever the timestep is), zshift in cm
PT3aa = PT_Hobo(allbaro,'PT3a Dam',XL,'PT-Fagaalu3aa',12)
PT3ab = PT_Hobo(allbaro,'PT3a Dam',XL,'PT-Fagaalu3ab',12)
PT3b = PT_Levelogger(allbaro,'PT3b Dam',XL,'PT-Fagaalu3b',0)
PT3c = PT_Levelogger(allbaro,'PT3c Dam',XL,'PT-Fagaalu3c',0)
PT3d = PT_Levelogger(allbaro,'PT3d Dam',XL,'PT-Fagaalu3d',0)
PT3e = PT_Levelogger(allbaro,'PT3e Dam',XL,'PT-Fagaalu3e',0)
PT3f = PT_Levelogger(allbaro,'PT3f Dam',XL,'PT-Fagaalu3f',0)
PT3g = PT_Levelogger(allbaro-1.5,'PT3g Dam',XL,'PT-Fagaalu3g',0)
PT3 = pd.concat([PT3aa,PT3ab,PT3b,PT3c,PT3d,PT3e,PT3f,PT3g])
PT3 = PT3[PT3>0]

PT1 = PT1.reindex(pd.date_range(start2012,stop2014,freq='15Min'))
PT2 = PT2.reindex(pd.date_range(start2012,stop2014,freq='15Min'))
PT3 = PT3.reindex(pd.date_range(start2012,stop2014,freq='15Min'))

def plot_uncorrected_stage_data(show=False):
    fig, (baro,pt1,pt3,t) = plt.subplots(4,sharex=True,sharey=False,figsize=(12,8))
    for ax in [baro,pt1,pt3]:
        ax.xaxis.set_visible(False)
    allbaro['Baropress'].plot(ax=baro,c='k',label='Barometric Pressure (kPa)')
    allbaro['Baropress'].plot(ax=t,c='k',label='Barometric Pressure (kPa)')
    baro.legend()
    ## PT1 at LBJ
    PT1list = [PT1aa,PT1ab,PT1ba,PT1bb,PT1bc,PT1c]
    count = 0
    count_dict = {1:'aa',2:'ab',3:'ba',4:'bb',5:'bc',6:'c'}
    for PT in PT1list:
        count+=1
        try:
            PT['Pressure'].plot(ax=pt1,c=np.random.rand(3,1),label='PT1'+count_dict[count])
            PT['Pressure'].plot(ax=t,c=np.random.rand(3,1),label='PT1'+count_dict[count])
        except KeyError:
            PT['LEVEL'].plot(ax=pt1,c=np.random.rand(3,1),label='PT1'+count_dict[count])
            PT['LEVEL'].plot(ax=t,c=np.random.rand(3,1),label='PT1'+count_dict[count])
    pt1.legend()
    
    ## PT3 at DAM
    PT3list = [PT3aa,PT3ab,PT3b,PT3c,PT3d,PT3e,PT3f,PT3g]
    count = 0
    count_dict = {1:'aa',2:'ab',3:'b',4:'c',5:'d',6:'e',7:'f',8:'g'}
    for PT in PT3list:
        count+=1
        try:
            PT['Pressure'].plot(ax=pt3,c=np.random.rand(3,1),label='PT3'+count_dict[count])
            PT['Pressure'].plot(ax=t,c=np.random.rand(3,1),label='PT3'+count_dict[count])
        except KeyError:
            PT['LEVEL'].plot(ax=pt3,c=np.random.rand(3,1),label='PT3'+count_dict[count])
            PT['LEVEL'].plot(ax=t,c=np.random.rand(3,1),label='PT3'+count_dict[count])
    pt3.legend()
    t.legend(ncol=2)
    
    if show==True:
        plt.tight_layout(pad=0.1)
        plt.show()
    return
#plot_uncorrected_stage_data(show=True)
    
    
    
## BAROMETRIC PRESSURE DATA FROM DIFFERENT SOURCES
## WITH PRESSURE FROM PT (MAKE SURE THEY'RE IN SYNC)
## Not sure what the difference plot is for....
def plot_barometric_pressure():   
    fig, (baro, pt, diff) = plt.subplots(3,1,sharex=True)
    ## Barometric Data
    allbaro['Baropress'].plot(ax=baro,c='k', label='Barometric Pressure (kPa)')
    allbaro['NDBCbaro'].plot(ax=baro,c='r', label='NDBC NSTP6')
    allbaro['FPbaro'].plot(ax=baro,c='g', label='Weather Station')
    ## PT Data
    PT1['Pressure'].plot(ax=baro,c='b', label='LBJ PT Pressure')
    PT1['stage(cm)'].plot(ax=pt,c='b', label='LBJ PT Stage(cm)')
    ## Difference between PT pressure and Barometric pressure at low stages
    press_diff_baseflow = PT1['Pressure'][PT1['stage(cm)']<10]-PT1['barodata']
    m.rolling_mean(press_diff_baseflow,window=96).plot(ax=diff, label='Daily Mean difference kPa (PT-Baro)') ## 96 * 15min = 24 hours
    
    baro.legend(), pt.legend(), diff.legend()
    return
#plot_barometric_pressure()

    

def correct_Stage_data(Stage_Correction_XL,location,PTdata):
    print 'Correcting stage for '+location
    def my_parser(x,y):
        try:
            y = str(int(y))
            hour=y[:-2]
            minute=y[-2:]
            time=dt.time(int(hour),int(minute))
        except:
            time=dt.time(0,0)
        parsed=dt.datetime.combine(x,time)
        #print parsed
        return parsed
    Stage_Correction = Stage_Correction_XL.parse(location,parse_dates=False)
    Correction=pd.DataFrame()
    for correction in Stage_Correction.iterrows():
        t1_date = correction[1]['T1_date']
        t1_time = correction[1]['T1_time']
        t1 = my_parser(t1_date,t1_time)
        t2_date = correction[1]['T2_date']
        t2_time = correction[1]['T2_time']
        t2 = my_parser(t2_date,t2_time)
        z = correction[1]['z']    
        print t1,t2, z
        Correction = Correction.append(pd.DataFrame({'z':z},index=pd.date_range(t1,t2,freq='15Min')))
    Correction = Correction.reindex(pd.date_range(start2012,stop2014,freq='15Min'))
    PTdata['Manual_Correction'] = Correction['z']
    PTdata['stage_corrected_Manual'] = PTdata['Uncorrected_stage']+PTdata['Manual_Correction']
    PTdata['stage(cm)']=PTdata['stage_corrected_Manual'].where(PTdata['stage_corrected_Manual']>0,PTdata['stage(cm)'])#.round(0)
    return PTdata
Stage_Correction_XL = pd.ExcelFile(datadir+'Q/StageCorrection.xlsx')    
PT1 = correct_Stage_data(Stage_Correction_XL,'LBJ',PT1)
PT3 = correct_Stage_data(Stage_Correction_XL,'DAM',PT3)


## STAGE DATA FOR PT's
#### FINAL STAGE DATA with CORRECTIONS
Fagaalu_stage_data = pd.DataFrame({'LBJ':PT1['stage(cm)'],'DT':PT2['stage(cm)'],'Dam':PT3['stage(cm)']})
Fagaalu_stage_data = Fagaalu_stage_data.reindex(pd.date_range(start2012,stop2014,freq='15Min'))


#### STAGE TO DISCHARGE ####
#from stage2discharge_ratingcurve import AV_RatingCurve#, calcQ, Mannings_rect, Weir_rect, Weir_vnotch, Flume


### Calculate Q from a single AV measurement
#fileQ = calcQ(datadir+'Q/LBJ_4-18-13.txt','LBJ',Fagaalu_stage_data,slope=Slope,Mannings_n=n,trapezoid=True)
## and save to CSV
#pd.concat(fileQ).to_csv(datadir+'Q/LBJ_4-18-13.csv')

### Area Velocity and Mannings from in situ measurments
## Returns DataFrame of Stage (cm) and Discharge (L/sec) calc. from AV measurements with time index

def Stage_Q_AV_RatingCurve(path,location,stage_data,slope=.01,Mannings_n=.033,trapezoid=True,printResults=False):
    Filelist = os.listdir(path)
    ## iterate over files in directory to get Flow.txt file
    for f in Filelist:
        ## Select Flow.txt file
        if f.endswith('Flow.txt')==True and f.startswith(location)==True:
            print 'AV measurements file selected for analysis: '+f
            ## Open File, create blank parameters
            Flowfile = open(path+f)
            Qdf = pd.DataFrame() ## empty dataframe to append calculated Q
            for line in Flowfile:
                split = line.strip('\n').split('\t')
                #print split
                # Test if data is number
                try:
                    a= float(split[0]) ## dummy test
                    isfloat=True
                except ValueError:
                    isfloat=False            
                ## Determine DateTime of AV measurment
                if split[0]==location:
                    ## Create empty dataframe
                    df = pd.DataFrame(columns=['dist','depth','flow']) ## empty dataframe for Flowmeter data
                    date, time = split[1].split('/'),split[2]
                    if len(time)==3:
                        time = '0'+time
                    DateTime = dt.datetime(int(date[2]),int(date[0]),int(date[1]),int(time[0:2]),int(time[2:]))
                    DateTime = RoundTo15(DateTime)
                    #print DateTime
                ## Append data
                elif isfloat==True:
                    df=df.append(pd.DataFrame({'dist':split[0],'depth':split[1],'flow':split[2]},index=[DateTime]))
                elif split[0]=='Location' or split[0]=='Field Measurements' or split[0]=='Dist(S to N)(ft)' or split[0]=='Dist(ft)':
                    pass
                
                ## At the end of that AV measurment, calculate Q
                elif split[0]=='-':
                    #print 'calculating Q for '+str(DateTime)
                    df = df.astype('float')
                    if trapezoid==True:
                        ## Depth/flow measurements are made at the midpoint of the trapezoid, dimensions of the trapezoid have to be determined
                        df['right']= df['dist'].shift(-1).sub(df['dist'],fill_value=0) ##Distance next - Distance = the width to the right
                        df['left'] = df['dist'].sub(df['dist'].shift(1),fill_value=0) ## Distance previous - Distance = the width to the left
                        df['right'] = df['right'].where(df['right']>0,0)
                        df['width']=((df['right'] + df['left'])/2)*12*2.54 ## 2nd mark - first; then convert to cm
                        df['b1']=(df['depth'].add(df['depth'].shift(1),fill_value=0))/2 ## gives average of Depth Above and depth
                        df['b2']=(df['depth'].add(df['depth'].shift(-1),fill_value=0))/2 ## gives average of Depth Below and depth
                        df['trapezoidal-area']=.5*(df['b1']+df['b2'])*df['width'] ## Formula for area of a trapezoid = 1/2 * (B1+B2) * h; h is width of the interval and B1 and B2 are the depths at the midpoints between depth/flow measurements
                        df['trapezoidal-area']=df['trapezoidal-area']/10000 ##cm2 to m2
                        df['AV']=df['trapezoidal-area']*df['flow'] *1000 ## m2 x m/sec x 1000 = L/sec
                        AV_Q = df['AV'].sum()
                        Area = df['trapezoidal-area'].sum()
                        V = df['flow'].mean()
                        ## Wetted perimeter doesn't use midpoints between depth/flow measurments
                        df['WP']=  ((df['depth'].sub(df['depth'].shift(1),fill_value=0))**2 + (df['dist'].sub(df['dist'].shift(1),fill_value=0)*12*2.54)**2)**0.5 ## WP = SQRT((Dnext-D)^2 + Width^2)
                        df['WP']=(df['WP']*(df['b1']>0))/100 ## cm to m; and only take WP values where the depth to the left is not zero
                        
                        WP = df['WP'].sum()
                        R = (df['trapezoidal-area'].sum())/(df['WP'].sum()) ## m2/m = m
                        ## Mannings = (1R^2/3 * S^1/2)/n
                        S = slope
                        ## Jarrett (1990) equation for n
                        ## n = 0.32*(S**0.30)*(R**-0.16)
                        if Mannings_n == 'Jarrett':
                            n = 0.32*(S**0.30)*(R**-0.16)
                        else:
                            n = Mannings_n
                        ManningV = (1*(R**(2.0/3.0))*(S**0.5))/n
                        ManningQ = ManningV * df['trapezoidal-area'].sum() * 1000 ## L/Sec
                    elif trapezoid==False:
                        df = df.set_value(len(df),'dist',df['dist'][-1]) ## add a dummy distance value
                        valbelow = df['dist'].shift(-1).sub(df['dist'],fill_value=0) ## Width is value below - dist value
                        valabove = df['dist'].sub(df['dist'].shift(1),fill_value=0)
                        df['width']=(valbelow.add(valabove)/2)*12*2.54 ## 2nd mark - first
                        df['rectangular-area']=df['depth']*(df['width'])/10000 ##cm2 to m2
                        df['AV']=df['rectangular-area']*df['flow']
                        
                        AV_Q = df['AV'].sum().round(0)
                        Area = df['rectangular-area'].sum()
                        V = df['flow'].mean()
                        ManningV = np.nan
                    try:
                        stage = stage_data[location].ix[DateTime] ## Get Stage data
                        print location+' '+str(DateTime)+' '+'Stage= '+str(stage)+' Q= '+str(AV_Q)
                    except:
                        stage =np.nan
                        print location+' '+str(DateTime)+' '+'Stage= '+str(stage)+' Q= '+str(AV_Q)
                    Qdf = Qdf.append(pd.DataFrame({'stage(cm)':stage,'Q-AV(L/sec)':round(AV_Q,0),'Q-AManningV(L/sec)':round(ManningQ,0),
                    'Area(m2)':Area,'V(m/s)':V,'ManningV(m/s)':ManningV,'WP':WP,'R':R},index=[DateTime]))
                    
                    if printResults==True:                    
                        print str(DateTime)+': stage='+'%.2f'%stage+' Q= '+'%.0f'%AV_Q+' ManningQ= '+'%.2f'%ManningQ
                        print df              
    return Qdf  
#Stage_Q_AV_RatingCurve(path,location,stage_data,slope=.01,Mannings_n=.033,trapezoid=True,printResults=False)


### Discharge using Mannings and Surveyed Cros-section
#from ManningsRatingCurve import Mannings, Mannings_Series
def Mannings_Q_from_CrossSection(Cross_section_file,sheetname,Slope,Manning_n,k=1,stage_start=.01,stage_end=None,show=False,save=False,filename=''):    
    ## Open and parse file; drop NA  
    print Cross_section_file+' '+sheetname
    print 'Slope: '+str(Slope)+' Mannings n: '+str(Manning_n)
    XL = pd.ExcelFile(Cross_section_file) 
    df = XL.parse(sheetname,header=4,parse_cols='F:H')
    df = df.dropna()
    ## Mannings Parameters S:slope, n:Mannings n
    S = Slope # m/m
    n= Manning_n
    ## empty lists
    areas, wp, r, Man_n, v, q, = [],[],[],[],[],[]
    ## Stage data
    ## one stage measurement
    if stage_end == None:
        print 'Stage: '+str(stage_start)
        stages = np.array([stage_start])
    ## start and end stage
    elif stage_start != stage_end:
        print 'Stage_start: '+str(stage_start)+' Stage_end: '+str(stage_end)
        stages = np.arange(stage_start,stage_end,.1) #m
    ## stage Series         
    elif type(stage_start)==pd.Series:
        print 'Stage Series...'
        stages = stage_start.to_list()
        
    for stage in stages:
        print 'stage: '+str(stage)
        df['y1'] = df['depth']+df['Rod Reading'].max()
        df['y2'] = stage
        df['z'] = df['y2']-df['y1']
        df['z'] = df['z'][df['z']>=0]
        
        x = df['Dist'].values
        y1 = df['y1'].values
        y2 = df['y2'].values
        
        z = y2-y1
        z= np.where(z>=0,z,0)
        Area = np.trapz(z,x)
        
        ## Wetted Perimeter
        df['dx'] = df['Dist'].sub(df['Dist'].shift(1),fill_value=0)
        df['dy'] = df['z'].sub(df['z'].shift(1),fill_value=0)
        df['wp'] = (df['dx']**2 + df['dy']**2)**0.5
        print df        
        
        WP = df['wp'].sum()
        R = (Area/WP) ## m2/m = m
        ## Jarrett (1990) equation for n
        ## n = 0.32*(S**0.30)*(R**-0.16)
        if Manning_n == 'Jarrett':
            n = 0.32*(S**0.30)*(R**-0.16)
            n= n *k
        ## Mannings = (1R^2/3 * S^1/2)/n
        ManningV = (1*(R**(2.0/3.0))*(S**0.5))/n
        ManningQ = ManningV * Area ## M3/s
        
        plt.ioff()          
        fig, ax1 = plt.subplots(1)
        ax1.plot(df['Dist'],df['y1'],'-o',c='k')
        ax1.fill_between(df['Dist'], df['y1'], stage,where = df['y1']<=stage,alpha=.5, interpolate=True)
        
        ax1.annotate('stage: '+'%.2f'%stage+'m',xy=(0,1.5+.45))
        ax1.annotate('Mannings n: '+'%.3f'%n,xy=(0,1.5+.03))
        ax1.annotate('Area: '+'%.3f'%Area+'m2',xy=(0,1.5+.25))
        ax1.annotate('WP: '+'%.2f'%WP+'m',xy=(df['Dist'].mean(),1.5+.03))
        ax1.annotate('Manning V: '+'%.2f'%ManningV+'m/s ',xy=(df['Dist'].mean(),1.5+.25))
        ax1.annotate('Manning Q: '+'%.3f'%ManningQ+'m3/s',xy=(df['Dist'].mean(),1.5+.45))
        plt.axes().set_aspect('equal')
        plt.xlim(-1,df['Dist'].max()+1),plt.ylim(-1,2 + 1.)
    
        areas.append(Area)
        wp.append(WP)
        r.append(R)
        Man_n.append(n)
        v.append(ManningV)
        q.append(ManningQ)
        show_plot(show,fig)
        savefig(save,filename) 
        plt.close('all')
        plt.ion()
    
    DF = pd.DataFrame({'stage(m)':stages,'area(m2)':areas,'wp(m)':wp,'r':r,'Man_n':Man_n,'vel(m/s)':v,'Q(m3/s)':q}) 
    return DF,df
  
    
def Mannings_Q_from_stage_data(Cross_section_file,sheetname,stage_data,Slope,Manning_n,k=1):    
    ## Open and parse file; drop NA  
    print Cross_section_file+' '+sheetname
    print 'Slope: '+str(Slope)+' Mannings n: '+str(Manning_n)
    XL = pd.ExcelFile(Cross_section_file) 
    df = XL.parse(sheetname,header=4,parse_cols='F:H')
    df = df.dropna()
    ## Mannings Parameters S:slope, n:Mannings n
    S = Slope # m/m
    n= Manning_n
    ## empty lists
    areas, wp, r, Man_n, v, q, = [],[],[],[],[],[]
    ## Stage data
    stage_data = stage_data/100 ## cm to m
    for stage in stage_data.values:
        #print 'stage: '+str(stage)
        df['y1'] = df['depth']+df['Rod Reading'].max()
        df['y2'] = stage
        df['z'] = df['y2']-df['y1']
        df['z'] = df['z'][df['z']>=0]
        x = df['Dist'].values
        y1 = df['y1'].values
        y2 = df['y2'].values
        z = y2-y1
        z= np.where(z>=0,z,0)
        Area = np.trapz(z,x)
        ## Wetted Perimeter0.01
        df['dx'] =df['Dist'].sub(df['Dist'].shift(1),fill_value=0)
        df['dy'] = df['z'].sub(df['z'].shift(1),fill_value=0)
        df['wp'] = (df['dx']**2 + df['dy']**2)**0.5
        WP = df['wp'].sum()
        R = (Area/WP) ## m2/m = m
        ## Jarrett (1990) equation for n
        ## n = 0.32*(S**0.30)*(R**-0.16)
        if Manning_n == 'Jarrett':
            n = 0.32*(S**0.30)*(R**-0.16) 
            n = n * k
        ## Mannings = (1R^2/3 * S^1/2)/n
        ManningV = (1*(R**(2.0/3.0))*(S**0.5))/n
        ManningQ = ManningV * Area ## M3/s
        ManningQ= round(ManningQ,3)
        areas.append(Area)
        wp.append(WP)
        r.append(R)
        Man_n.append(n)
        v.append(ManningV)
        q.append(ManningQ)        
    DF = pd.DataFrame({'stage(m)':stage_data.values,'area(m2)':areas,'wp(m)':wp,'r':r,'Man_n':Man_n,'vel(m/s)':v,'Q(m3/s)':q},index=stage_data.index)
    return DF
    
## Read LBJ_Man Discharge from .csv, or calculate new if needed
if 'LBJ_Man' not in locals():
    try:
        print 'Loading Mannings Q for DAM from CSV'
        LBJ_Man_reduced = pd.DataFrame.from_csv(datadir+'Q/Manning_Q_files/LBJ_Man_reduced.csv')
        LBJ_Man = pd.DataFrame.from_csv(datadir+'Q/Manning_Q_files/LBJ_Man.csv')
    except:
        print 'Calculate Mannings Q for LBJ and saving to CSV'
        LBJ_S, LBJ_n, LBJ_k = 0.016, 'Jarrett', .06/.08
        LBJ_S, LBJ_n, LBJ_k = 0.016, .067, 1
        LBJ_stage_reduced = Fagaalu_stage_data['LBJ'].dropna().round(0).drop_duplicates().order()
        LBJ_Man_reduced = Mannings_Q_from_stage_data(datadir+'Q/Cross_Section_Surveys/LBJ_cross_section.xlsx','LBJ_m',Slope=LBJ_S,Manning_n=LBJ_n,k=LBJ_k,stage_data=LBJ_stage_reduced)
        LBJ_Man_reduced.to_csv(datadir+'Q/Manning_Q_files/LBJ_Man_reduced.csv')
        LBJ_stage= Fagaalu_stage_data['LBJ']+5
        LBJ_Man= Mannings_Q_from_stage_data(datadir+'Q/Cross_Section_Surveys/LBJ_cross_section.xlsx','LBJ_m',Slope=LBJ_S,Manning_n=LBJ_n,k=LBJ_k,stage_data=LBJ_stage)
        LBJ_Man.to_csv(datadir+'Q/Manning_Q_files/LBJ_Man.csv')
        pass
    
## Read DAM_Man Discharge from .csv, or calculate new if needed
if 'DAM_Man' not in locals():
    try:
        print 'Loading Mannings Q for DAM from CSV'
        DAM_Man_reduced = pd.DataFrame.from_csv(datadir+'Q/Manning_Q_files/DAM_Man_reduced.csv')
        DAM_Man = pd.DataFrame.from_csv(datadir+'Q/Manning_Q_files/DAM_Man.csv')
    except:
        print 'Calculate Mannings Q for DAM and saving to CSV'
        DAM_S, DAM_n,  DAM_k = 0.03, 'Jarrett', .025/.06
        DAM_stage_reduced = Fagaalu_stage_data['Dam'].dropna().round(0).drop_duplicates().order()
        DAM_Man_reduced = Mannings_Q_from_stage_data(datadir+'Q/Cross_Section_Surveys/DAM_cross_section.xlsx','DAM_m',Slope=DAM_S,Manning_n=DAM_n,k=DAM_k,stage_data=DAM_stage_reduced)
        DAM_Man_reduced.to_csv(datadir+'Q/Manning_Q_files/DAM_Man_reduced.csv')
        DAM_stage = Fagaalu_stage_data['Dam']
        DAM_Man= Mannings_Q_from_stage_data(datadir+'Q/Cross_Section_Surveys/DAM_cross_section.xlsx','DAM_m',Slope=0.03,Manning_n='Jarrett',k=.025/.06,stage_data=DAM_stage)
        DAM_Man.to_csv(datadir+'Q/Manning_Q_files/DAM_Man.csv')
        pass 

#### LBJ Stage-Discharge
# (3 rating curves: AV measurements, A measurement * Mannings V, Surveyed Cross-Section and Manning's equation)

## LBJ AV measurements
## Mannings parameters for A-ManningV
Slope = 0.0161 # m/m
LBJ_n=0.067 # Mountain stream rocky bed and rivers with variable sections and veg along banks (Dunne 1978)

#DataFrame with Q from AV measurements, Q from measured A with Manning-predicted V, stage, and Q from Manning's and assumed rectangular channel
LBJstageDischarge = Stage_Q_AV_RatingCurve(datadir+'Q/Flow_Files/','LBJ',Fagaalu_stage_data,slope=Slope,Mannings_n=LBJ_n,trapezoid=True).dropna() 
LBJstageDischarge = LBJstageDischarge.truncate(before=datetime.datetime(2012,3,20)) # throw out measurements when I didn't know how to use the flowmeter 
LBJstageDischargeLog = LBJstageDischarge.apply(np.log10) #log-transformed version

## LBJ: Discharge Ratings
## Linear
LBJ_AV= pd.ols(y=LBJstageDischarge['Q-AV(L/sec)'],x=LBJstageDischarge['stage(cm)'],intercept=True) 
## Power
LBJ_AVLog= pd.ols(y=LBJstageDischargeLog['Q-AV(L/sec)'],x=LBJstageDischargeLog['stage(cm)'],intercept=True) #linear fit to log-transformed stage and Q
## Linear with Mannings and measured Area
LBJ_AManningV = pd.ols(y=LBJstageDischarge['Q-AManningV(L/sec)'],x=LBJstageDischarge['stage(cm)'],intercept=True)
## Power with Mannings and measured Area
LBJ_AManningVLog = pd.ols(y=LBJstageDischargeLog['Q-AManningV(L/sec)'],x=LBJstageDischargeLog['stage(cm)'],intercept=True)

#### DAM Stage-Discharge

## DAM AV Measurements
Slope= 0.3
DAM_n = 'Jarrett'
DAM_k = 1
## DataFrame of Stage and Discharge calc. from AV measurements with time index
DAMstageDischarge = Stage_Q_AV_RatingCurve(datadir+'Q/Flow_Files/','Dam',Fagaalu_stage_data,slope=Slope,Mannings_n=DAM_n).dropna() 
#DAMstageDischarge = DAMstageDischarge[10:]# throw out measurements when I didn't know how to use the flowmeter
DAMstageDischargeLog=DAMstageDischarge.apply(np.log10) #log-transformed version

## DAM: Discharge Ratings
## Linear
DAM_AV = pd.ols(y=DAMstageDischarge['Q-AV(L/sec)'],x=DAMstageDischarge['stage(cm)'],intercept=True) 
## Power
DAM_AVLog = pd.ols(y=DAMstageDischargeLog['Q-AV(L/sec)'],x=DAMstageDischargeLog['stage(cm)'],intercept=True) 

### HEC-RAS Model of the DAM structure: Documents/HEC/FagaaluDam.prj
def HEC_piecewise(PTdata):
    if type(PTdata)!=pd.Series:
        PTdata = pd.Series(data=PTdata)
    HEC_a1, HEC_b1 = 9.9132, -5.7184 ## from excel DAM_HEC.xlsx
    HEC_a2, HEC_b2 = 25.823, -171.15 
    HEC_a3, HEC_b3 = 98.546, -3469.4
    
    Func1=PTdata[PTdata<=11]*HEC_a1 + HEC_b1
    Func2=PTdata[(PTdata>11)&(PTdata<=45)]*HEC_a2 + HEC_b2
    Func3=PTdata[PTdata>45]*HEC_a3 + HEC_b3
    AllValues = Func1.append([Func2,Func3])
    return AllValues
DAM_HECstageDischarge= pd.DataFrame(data=range(0,150),columns=['stage(cm)'])
DAM_HECstageDischarge['Q_HEC(L/sec)'] = HEC_piecewise(DAM_HECstageDischarge['stage(cm)'])

DAMstageDischarge['Q_HEC(L/sec)']= HEC_piecewise(DAMstageDischarge['stage(cm)']).values

DAM_HEC = pd.ols(y=DAMstageDischarge['Q_HEC(L/sec)'],x=DAMstageDischarge['stage(cm)'],intercept=True) 


## This function calculates the coeff of determination (r2) for 
## a function (=Manning's rating curve) and some independent points (=AV Q measurements
def Manning_AV_r2(ManningsQ_Series,AV_Series):
    # LBJ Mannings = y predicted
    ManQ, Manstage = ManningsQ_Series['Q(m3/s)']*1000, ManningsQ_Series['stage(m)']*100
    y_predicted = pd.DataFrame({'Q_Man':ManQ.values},index=Manstage).sort()
    ## LBJ AV  = y
    AV_Q, AVstage = AV_Series['Q-AV(L/sec)'], AV_Series['stage(cm)'].apply(np.int)
    y_ = pd.DataFrame({'Q_AV':AV_Q.values},index=AVstage).sort()
    y_['Q_Man'] = y_predicted
    y_=  y_.dropna() # keep it clean
    
    y_bar = y_['Q_AV'].mean()
    y_var = (y_['Q_AV'] - y_bar)**2.
    ss_tot = y_var.sum()
    y_res = (y_['Q_AV']-y_['Q_Man'])**2.
    ss_res = y_res.sum()
    r2 = 1-(ss_res/ss_tot)
    return  r2
LBJ_Man_r2 = Manning_AV_r2(LBJ_Man_reduced,LBJstageDischarge)
DAM_Man_r2 = Manning_AV_r2(DAM_Man_reduced,DAMstageDischarge)

def Manning_AV_rmse(Man_Series,AV_Series):
    # LBJ Mannings = y predicted
    ManQ, Manstage = Man_Series['Q(m3/s)']*1000, Man_Series['stage(m)']*100
    y_predicted = pd.DataFrame({'Q_Man':ManQ.values},index=Manstage).sort()
    ## LBJ AV  = y
    AV_Q, AVstage = AV_Series['Q-AV(L/sec)'], AV_Series['stage(cm)'].apply(np.int)
    y_ = pd.DataFrame({'Q_AV':AV_Q.values},index=AVstage).sort()
    y_['Q_Man'] = y_predicted
    y_=  y_.dropna() # keep it 
    y_['Q_diff'] = y_['Q_AV'] - y_['Q_Man']
    y_['Q_diff_squared'] = (y_['Q_diff'])**2.
    y_rmse = (y_['Q_diff_squared'].sum()/len(y_))**0.5
    
    mean_observed = AV_Q.mean()
    rmse_percent = y_rmse/mean_observed *100.
    return int(y_rmse),int(mean_observed),int(rmse_percent)
LBJ_Man_rmse = Manning_AV_rmse(LBJ_Man_reduced,LBJstageDischarge)[2]
    
    
def HEC_AV_r2(HEC_Series,AV_Series):
    # LBJ Mannings = y predicted
    HEC_Q, HECstage = HEC_Series['Q_HEC(L/sec)'].round(0), HEC_Series['stage(cm)']
    y_predicted = pd.DataFrame({'Q_HEC':HEC_Q.values},index=HECstage).sort()
    ## LBJ AV  = y
    AV_Q, AVstage = AV_Series['Q-AV(L/sec)'], AV_Series['stage(cm)']
    y_ = pd.DataFrame({'Q_AV':AV_Q.values},index=AVstage).sort()
    y_['Q_Man'] = y_predicted
    y_=  y_.dropna() # keep it clean
    
    y_bar = y_['Q_AV'].mean()
    y_var = (y_['Q_AV'] - y_bar)**2.
    ss_tot = y_var.sum()
    y_res = (y_['Q_AV']-y_['Q_Man'])**2.
    ss_res = y_res.sum()
    r2 = 1-(ss_res/ss_tot)
    return  r2
DAM_HEC_r2 = HEC_AV_r2(DAM_HECstageDischarge,DAMstageDischarge)

def HEC_AV_rmse(HEC_Series,AV_Series):
    # LBJ Mannings = y predicted
    HEC_Q, HECstage = HEC_Series['Q_HEC(L/sec)'].round(0), HEC_Series['stage(cm)']
    y_predicted = pd.DataFrame({'Q_HEC':HEC_Q.values},index=HECstage).sort()
    ## LBJ AV  = y
    AV_Q, AVstage = AV_Series['Q-AV(L/sec)'], AV_Series['stage(cm)']
    y_ = pd.DataFrame({'Q_AV':AV_Q.values},index=AVstage).sort()
    y_['Q_Man'] = y_predicted
    y_=  y_.dropna() # keep it clean
    y_['Q_diff'] = y_['Q_AV'] - y_['Q_Man']
    y_['Q_diff_squared'] = (y_['Q_diff'])**2.
    y_rmse = (y_['Q_diff_squared'].sum()/len(y_))**0.5
    
    mean_observed = AV_Q.mean()
    rmse_percent = y_rmse/mean_observed *100.
    return int(y_rmse),int(mean_observed),int(rmse_percent)
DAM_HEC_rmse = HEC_AV_rmse(DAM_HECstageDischarge,DAMstageDischarge)[2]   


### Compare Discharge Ratings from different methods
def plotQratingLBJ(ms=6,show=False,log=False,save=False,filename=figdir+''): ## Rating Curves
    mpl.rc('lines',markersize=ms)
    title="Water Discharge Ratings for FG3(LBJ)"
    fig, (site_lbj, site_lbj_zoom)= plt.subplots(1,2,figsize=(8,4))
    xy = np.linspace(0,8000,8000)
    site_lbj.text(0.1,0.95,'(a)',verticalalignment='top', horizontalalignment='right',transform=site_lbj.transAxes,color='k',fontsize=10,fontweight='bold')
    site_lbj_zoom.text(0.1,0.95,'(b)',verticalalignment='top', horizontalalignment='right',transform=site_lbj_zoom.transAxes,color='k',fontsize=10,fontweight='bold')
    #LBJ AV Measurements and Rating Curve
    site_lbj.plot(LBJstageDischarge['Q-AV(L/sec)'][start2012:stop2012],LBJstageDischarge['stage(cm)'][start2012:stop2012],'o',color='k',fillstyle='none',label='AV 2012') 
    site_lbj.plot(LBJstageDischarge['Q-AV(L/sec)'][start2013:stop2013],LBJstageDischarge['stage(cm)'][start2013:stop2013],'^',color='k',fillstyle='none',label='AV 2013') 
    site_lbj.plot(LBJstageDischarge['Q-AV(L/sec)'][start2014:stop2014],LBJstageDischarge['stage(cm)'][start2014:stop2014],'s',color='k',fillstyle='none',label='AV 2014') 
    site_lbj_zoom.plot(LBJstageDischarge['Q-AV(L/sec)'][start2012:stop2012],LBJstageDischarge['stage(cm)'][start2012:stop2012],'o',color='k',fillstyle='none',label='AV 2012') 
    site_lbj_zoom.plot(LBJstageDischarge['Q-AV(L/sec)'][start2013:stop2013],LBJstageDischarge['stage(cm)'][start2013:stop2013],'^',color='k',fillstyle='none',label='AV 2013') 
    site_lbj_zoom.plot(LBJstageDischarge['Q-AV(L/sec)'][start2014:stop2014],LBJstageDischarge['stage(cm)'][start2014:stop2014],'s',color='k',fillstyle='none',label='AV 2014') 

    ## LBJ MODELS
    ## Mannings for AV measurements
    #site_lbj.plot(LBJstageDischarge['Q-AManningV(L/sec)'],LBJstageDischarge['stage(cm)'],'.',ls='None',c='grey',label='A-ManningsV')
    #site_lbj_zoom.plot(LBJstageDischarge['Q-AManningV(L/sec)'],LBJstageDischarge['stage(cm)'],'.',ls='None',c='grey',label='A-ManningsV')
    ## LBJ Power
    LBJ_AVpower = powerfunction(LBJstageDischarge['Q-AV(L/sec)'],LBJstageDischarge['stage(cm)'])    
    PowerFit(LBJstageDischarge['Q-AV(L/sec)'],LBJstageDischarge['stage(cm)'],xy,site_lbj,c='grey',ls='-',label='AV power law '+r'$r^2$'+"%.2f"%LBJ_AVpower['r2'])    
    PowerFit(LBJstageDischarge['Q-AV(L/sec)'],LBJstageDischarge['stage(cm)'],xy,site_lbj_zoom,c='grey',ls='-',label='AV power law '+r'$r^2$'+"%.2f"%LBJ_AVpower['r2'])        
    ## LBJ Mannings from stream survey
    LBJ_ManQ, LBJ_Manstage = LBJ_Man_reduced['Q(m3/s)']*1000, LBJ_Man_reduced['stage(m)']*100
    site_lbj.plot(LBJ_ManQ,LBJ_Manstage,'-',markersize=2,c='k',label='Mannings: n='+str(LBJ_n)+r'$ r^2$'+"%.2f"%LBJ_Man_r2)
    site_lbj_zoom.plot(LBJ_ManQ,LBJ_Manstage,'-',markersize=2,c='k',label='Mannings')
    ## Label point -click
    labelindex_subplot(site_lbj, LBJstageDischarge.index,LBJstageDischarge['Q-AV(L/sec)'],LBJstageDischarge['stage(cm)'])
    labelindex_subplot(site_lbj_zoom, LBJstageDischarge.index,LBJstageDischarge['Q-AV(L/sec)'],LBJstageDischarge['stage(cm)'])
    ## Label subplots    
    site_lbj.set_ylabel('Stage(cm)'),site_lbj.set_xlabel('Q(L/sec)'),site_lbj_zoom.set_xlabel('Q(L/sec)')
    ## Format subplots
    site_lbj.set_ylim(0,PT1['stage(cm)'].max()+10)#,site_lbj.set_xlim(0,LBJ_AVnonLinear(PT1['stage'].max()+10))
    site_lbj_zoom.set_ylim(0,45), site_lbj_zoom.set_xlim(0,1600)
    ## Legends
    site_lbj.legend(loc='lower right',fancybox=True)  
    ## Figure title
    #plt.suptitle(title,fontsize=16)
    fig.canvas.manager.set_window_title('Figure : '+title) 
    logaxes(log,fig)
    for ax in fig.axes:
        ax.autoscale_view(True,True,True)
    plt.tight_layout(pad=0.1)
    show_plot(show,fig)
    savefig(save,filename)
    return
#plotQratingLBJ(ms=6,show=True,log=False,save=False,filename=figdir+'')
#plotQratingLBJ(ms=6,show=True,log=True,save=False,filename=figdir+'')

### Compare Discharg Ratings from different methods
def plotQratingDAM(ms=6,show=False,log=False,save=False,filename=figdir+''): ## Rating Curves
    mpl.rc('lines',markersize=ms)
    fig, (site_dam, site_dam_zoom) = plt.subplots(1,2,figsize=(8,4))
    site_dam.text(0.95,0.95,'(a)',verticalalignment='top', horizontalalignment='right',transform=site_dam.transAxes,color='k',fontsize=10,fontweight='bold')
    site_dam_zoom.text(0.95,0.95,'(b)',verticalalignment='top', horizontalalignment='right',transform=site_dam_zoom.transAxes,color='k',fontsize=10,fontweight='bold')
    title="Discharge Ratings for FG1 (DAM)"
    xy = np.linspace(0,8000,8000)
    #DAM AV Measurements and Rating Curve
    site_dam.plot(DAMstageDischarge['Q-AV(L/sec)'][start2012:stop2012],DAMstageDischarge['stage(cm)'][start2012:stop2012],'o',color='k',fillstyle='none',label='AV 2012')
    site_dam.plot(DAMstageDischarge['Q-AV(L/sec)'][start2013:stop2013],DAMstageDischarge['stage(cm)'][start2013:stop2013],'^',color='k',fillstyle='none',label='AV 2013')
    site_dam.plot(DAMstageDischarge['Q-AV(L/sec)'][start2014:stop2014],DAMstageDischarge['stage(cm)'][start2014:stop2014],'s',color='k',fillstyle='none',label='AV 2014')
    #DAM AV Measurements and Rating Curve
    site_dam_zoom.plot(DAMstageDischarge['Q-AV(L/sec)'][start2012:stop2012],DAMstageDischarge['stage(cm)'][start2012:stop2012],'o',color='k',fillstyle='none',label='AV 2012')
    site_dam_zoom.plot(DAMstageDischarge['Q-AV(L/sec)'][start2013:stop2013],DAMstageDischarge['stage(cm)'][start2013:stop2013],'^',color='k',fillstyle='none',label='AV 2013')
    site_dam_zoom.plot(DAMstageDischarge['Q-AV(L/sec)'][start2014:stop2014],DAMstageDischarge['stage(cm)'][start2014:stop2014],'s',color='k',fillstyle='none',label='AV 2014')
    
    ### DAM Linear
    ## DAM Power    
    DAM_AVpower=powerfunction(DAMstageDischarge['Q-AV(L/sec)'],DAMstageDischarge['stage(cm)'])    
    PowerFit(DAMstageDischarge['Q-AV(L/sec)'],DAMstageDischarge['stage(cm)'],xy,site_dam,c='grey',ls='-', label='AV power law '+r'$r^2$'+"%.2f"%DAM_AVpower['r2']) ## rating from DAM_AV
    PowerFit(DAMstageDischarge['Q-AV(L/sec)'],DAMstageDischarge['stage(cm)'],xy,site_dam_zoom,c='grey',ls='-', label='AV power law '+r'$r^2$'+"%.2f"%DAM_AVpower['r2']) ## rating from DAM_AV
    #DAM HEC-RAS Model and Rating Curve
    #PowerFit(DAM_HECstageDischarge['Q_HEC(L/sec)'],DAM_HECstageDischarge['stage(cm)'],xy,site_dam,c='b',ls='--',label='DAM_HECpower '+r'$r^2$'+"%.2f"%DAM_HEC_r2) ## rating from DAM_HEC
    site_dam.plot(DAM_HECstageDischarge['Q_HEC(L/sec)'],DAM_HECstageDischarge['stage(cm)'],'-',color='k',label='HEC-RAS model '+r'$r^2$'+"%.2f"%DAM_HEC.r2)
    #PowerFit(DAM_HECstageDischarge['Q_HEC(L/sec)'],DAM_HECstageDischarge['stage(cm)'],xy,site_dam_zoom,c='b',ls='--',label='DAM_HECpower '+r'$r^2$'+"%.2f"%DAM_HEC_r2) ## rating from DAM_HEC
    site_dam_zoom.plot(DAM_HECstageDischarge['Q_HEC(L/sec)'],DAM_HECstageDischarge['stage(cm)'],'-',color='k',label='HEC-RAS model '+r'$r^2$'+"%.2f"%DAM_HEC.r2)
    ## DAM  FLUME
    
    ## DAM Mannings from stream survey
    DAM_ManQ, DAM_Manstage = DAM_Man_reduced['Q(m3/s)']*1000,DAM_Man_reduced['stage(m)']*100
    #site_dam.plot(DAM_ManQ, DAM_Manstage,'-',markersize=2,color='r',label='Mannings DAM '+r'$r^2$'+"%.2f"%DAM_Man_r2)   
    #site_dam_zoom.plot(DAM_ManQ, DAM_Manstage,'-',markersize=2,color='r',label='Mannings DAM')   
    ## Label point-click
    labelindex_subplot(site_dam, DAMstageDischarge.index,DAMstageDischarge['Q-AV(L/sec)'],DAMstageDischarge['stage(cm)'])
    labelindex_subplot(site_dam_zoom, DAMstageDischarge.index,DAMstageDischarge['Q-AV(L/sec)'],DAMstageDischarge['stage(cm)'])
    ## Storm Thresholds
    site_dam.axhline(46,ls='-.',linewidth=0.6,c='grey',label='Channel top')
    ## Label subplots    
    site_dam.set_ylabel('Stage(cm)'),site_dam.set_xlabel('Q(L/sec)'),site_dam_zoom.set_xlabel('Q(L/sec)')
    ## Format subplots
    site_dam.set_ylim(0,PT3['stage(cm)'].max()+10)#,site_dam.set_xlim(0,HEC_piecewise(PT3['stage'].max()+10).values)
    site_dam_zoom.set_ylim(0,20),site_dam_zoom.set_xlim(0,500)
    ## Legends
    site_dam.legend(loc='best',fancybox=True)    
    fig.canvas.manager.set_window_title('Figure : '+title) 
    logaxes(log,fig)
    for ax in fig.axes:
        ax.autoscale_view(True,True,True)
    plt.tight_layout(pad=0.1)
    show_plot(show,fig)
    savefig(save,filename)
    return
#plotQratingDAM(ms=6,show=True,log=False,save=False,filename=figdir+'')
#plotQratingDAM(ms=6,show=True,log=True,save=False,filename=figdir+'')

#### CALCULATE DISCHARGE
## Calculate Q for LBJ
## Stage
LBJ = DataFrame(PT1,columns=['stage(cm)']) ## Build DataFrame with all stage records for location (cm)
## Mannings
LBJ['Q-Mannings'] = LBJ_Man['Q(m3/s)']*1000
## Power Models
a,b = 10**LBJ_AVLog.beta[1], LBJ_AVLog.beta[0]# beta[1] is the intercept = log10(a), so a = 10**beta[1] # beta[0] is the slope = b
LBJ['Q-AVLog'] = a * (LBJ['stage(cm)']**b)
a,b = 10**LBJ_AManningVLog.beta[1], LBJ_AManningVLog.beta[0]
LBJ['Q-AManningVLog'] = a*(LBJ['stage(cm)']**b)

## Calculate Q for DAM
## Stage
DAM = DataFrame(PT3,columns=['stage(cm)']) ## Build DataFrame with all stage records for location
## Mannings
DAM['Q-Mannings']=DAM_Man['Q(m3/s)']*1000 ## m3/s to L/sec
## Linear Model
DAM['Q-AV']=(DAM['stage(cm)']*DAM_AV.beta[0]) + DAM_AV.beta[1] ## Calculate Q from AV rating=
## Power Model
a,b = 10**DAM_AVLog.beta[1], DAM_AVLog.beta[0]
DAM['Q-AVLog']=(a)*(DAM['stage(cm)']**b) 
## HEC-RAS Model
DAM['Q-HEC']= HEC_piecewise(DAM['stage(cm)'])



#### CHOOSE Q RATING CURVE
LBJ['Q']= LBJ['Q-Mannings']
LBJ['Q-RMSE'] = LBJ_Man_rmse
print 'LBJ Q from Mannings and Surveyed Cross Section'
DAM['Q']= DAM['Q-HEC'].round(0)
DAM['Q-RMSE'] = DAM_HEC_rmse
print 'DAM Q from HEC-RAS and Surveyed Cross Section'


#### Calculate Q for QUARRY based on specific discharge from watershed (m3/s/km2)
QUARRY = pd.DataFrame((DAM['Q']/.9)*1.17) ## Q* from DAM (m3/s/0.9km2) x Area Quarry (=1.17km2)
QUARRY['Q-RMSE'] = DAM['Q-RMSE'] ## RMSE same as for DAM
QUARRY['stage(cm)']=DAM['stage(cm)']
## Convert to 15min interval LBJ
LBJq = (LBJ*900) ## Q above is in L/sec; L/sec * 900sec/15Min = L/15Min
LBJq['stage(cm)']=PT1['stage(cm)'] ## put unaltered stage back in

## Convert to 15min interval QUARRY
QUARRYq = (QUARRY*900) ## Q above is in L/sec; L/sec * 900sec/15Min = L/15Min
QUARRYq['stage(cm)']=PT3['stage(cm)'] ## put unaltered stage back in

## Convert to 15min interval DAM
DAMq= (DAM*900)## Q above is in L/sec; L/sec * 900sec/15Min = L/15Min
DAMq['stage(cm)']=PT3['stage(cm)'] ## put unaltered stage back in


### Plot Q 
def plot_Q_by_year(log=False,show=False,save=False,filename=''):
    mpl.rc('lines',markersize=6)
    fig, (Q2012,Q2013,Q2014)=plt.subplots(3)
    letter_subplots(fig,0.1,0.95,'top','right','k',font_size=10,font_weight='bold')
    
    for ax in fig.axes:
        ax.plot_date(LBJ['Q'].index,LBJ['Q'],ls='-',marker='None',c='k',label='Q FG3')
        #ax.plot(LBJstageDischarge.index,LBJstageDischarge['Q-AV(L/sec)'],ls='None',marker='o',color='k')
        ax.plot_date(DAM['Q'].index,DAM['Q'],ls='-',marker='None',c='grey',label='Q FG1')
        #ax.plot(DAMstageDischarge.index,DAMstageDischarge['Q-AV(L/sec)'],ls='None',marker='o',color='grey')
        ax.set_ylim(0,LBJ['Q'].max()+500)  
        
    Q2012.set_xlim(start2012,stop2012),Q2013.set_xlim(start2013,stop2013),Q2014.set_xlim(start2014,stop2014)
    Q2012.legend(loc='best')
    Q2013.set_ylabel('Discharge (Q) L/sec')
    #Q2012.set_title("Discharge (Q) L/sec at the Upstream and Downstream Sites, Faga'alu")
    
    for ax in fig.axes:
        ax.locator_params(nbins=6,axis='y')
        ax.xaxis.set_major_locator(mpl.dates.MonthLocator(interval=2))
        ax.xaxis.set_major_formatter(mpl.dates.DateFormatter('%b %Y'))
        
    plt.tight_layout(pad=0.1)
    logaxes(log,fig)
    show_plot(show,fig)
    savefig(save,filename)
    return
#plot_Q_by_year(log=False,show=True,save=False,filename='')