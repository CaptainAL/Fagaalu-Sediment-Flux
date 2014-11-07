
import os
from misc_time import *
import numpy as np
import pandas as pd
import datetime as dt

## Filelist = text file with all the field measurements
##            needs to be formatted correctly


#################################################################################################################
def AV_RatingCurve(path,location,stage_data,slope=.01,Mannings_n=.033,trapezoid=True,printResults=False):
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
                split = line.strip('\n')
                split = split.split('\t')
                #print split
                # Test if data is number
                try:
                    a= float(split[0])
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
                        
                        AV_Q = df['AV'].sum()
                        Area = df['rectangular-area'].sum()
                        V = df['flow'].mean()
                        ManningV = np.nan
                    
                    try:
                        stage = stage_data[location].ix[DateTime] ## Get Stage data
                    except:
                        stage =np.nan
                    Qdf = Qdf.append(pd.DataFrame({'stage(cm)':stage,'Q-AV(L/sec)':AV_Q,'Q-AManningV(L/sec)':ManningQ,'Area(m2)':Area,'V(m/s)':V,'ManningV(m/s)':ManningV,'WP':WP,'R':R},index=[DateTime]))
                    
                    if printResults==True:                    
                        print str(DateTime)+': stage='+'%.2f'%stage+' Q= '+'%.2f'%AV_Q+' ManningQ= '+'%.2f'%ManningQ
                        print df
                    
                    
    return Qdf 

def calcQ(filename,location,stage_data,slope=.01,Mannings_n=.033,trapezoid=True,printResults=False):
  
    S = slope
    n = Mannings_n
    
    ## iterate over files in directory to get Flow.txt file
    
    print 'file selected for analysis: '+f
    ## Open File, create blank parameters
    Flowfile = open(filename)
    Qdf = pd.DataFrame() ## empty dataframe to append calculated Q
                
    for line in Flowfile:
        split = line.strip('\n')
        split = split.split('\t')
        #print split
        # Test if data is number
        try:
            a= float(split[0])
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
                ManningV = (1*(R**(2.0/3.0))*(S**0.5))/n
                ManningQ = ManningV * df['trapezoidal-area'].sum() * 1000 ## L/Sec

            elif trapezoid==False:
                df = df.set_value(len(df),'dist',df['dist'][-1]) ## add a dummy distance value
                valbelow = df['dist'].shift(-1).sub(df['dist'],fill_value=0) ## Width is value below - dist value
                valabove = df['dist'].sub(df['dist'].shift(1),fill_value=0)
                df['width']=(valbelow.add(valabove)/2)*12*2.54 ## 2nd mark - first
                df['rectangular-area']=df['depth']*(df['width'])/10000 ##cm2 to m2
                df['AV']=df['rectangular-area']*df['flow']
                
                AV_Q = df['AV'].sum()
                Area = df['rectangular-area'].sum()
                V = df['flow'].mean()
                ManningV = np.nan
            
            try:
                stage = stage_data[location].ix[DateTime] ## Get Stage data
            except:
                stage =np.nan
            Qdf = Qdf.append(pd.DataFrame({'stage(cm)':stage,'Q-AV(L/sec)':AV_Q,'Q-AManningV(L/sec)':ManningQ,'Area(m2)':Area,'V(m/s)':V,'ManningV(m/s)':ManningV,'WP':WP,'R':R},index=[DateTime]))
            
            if printResults==True:            
                print str(DateTime)+': stage='+'%.2f'%stage+' Q= '+'%.2f'%AV_Q+' ManningQ= '+'%.2f'%ManningQ
                print df
                
                 
    return Qdf,df 
    

#################################################################################################################
#################################################################################################################


def Mannings_rect(PTdatalist,location,ManningsN,Slope,width):
    n = ManningsN
    S = Slope

    ## Get stage data from PT and calculate Manning's Q
    StageDischarge = []
    def InterpolateData(time,datadict,datalist,otherdata,interval=15):
        Timeprev = time - datetime.timedelta(0,0,0,0,int(interval))
        Timeafter = time + datetime.timedelta(0,0,0,0,int(interval))
        dataprev = datadict[Timeprev].split(',')[1]
        dataafter = datadict[Timeafter].split(',')[1]
        interpolated = (float(dataprev) + float(dataafter))/2
        datalist.append((time,str(interpolated)+','+str(otherdata)))
        return           
    for line in PTdatalist:
        try:
            #print line
            Stagetime = line[0] ## Time object from Q calculation above
            ## Round minutes off to nearest 15minutes
            Stagetime = RoundTo15(Stagetime)
            Qlocation = location
            stage = float(line[1].split(',')[1])
            Depth = stage # cm
            Width = width # cm
            Area = Depth * Width # cm^2
            #### wetted perimeter
            WP = (2*Depth) + width #cm 
            ## MANNING'S EQUATION:  Q = CrossSectionalArea * 1.486/n * R^(2/3) * S^(1/2)
            ManningsQ = Area * (1.436/n) * (Area/WP)**(2.0/3.0) * S**(1.0/2.0) ## cm^3
            ManningsQ = str(ManningsQ/1000) #L/sec
            #print str("%.1f" % Q)            
            if math.isnan(float(stage))==False and math.isnan(float(ManningsQ))==False:
                StageDischarge.append((Stagetime,str(stage)+','+str(ManningsQ)))
                #print str(Stagetime)+' '+Qlocation+' Q: '+str(ManningsQ)+' stage = '+str(stage)
        except:
            raise
    ##Qtime = datetime.datetime(2012,1,30,0,0,0)
    ##Qzero = '1'
    ##LBJzeroflow = '3.5' ## point of zero flow (cm)
    ##LBJStageDischarge.append((Qtime,LBJzeroflow+','+Qzero))
    return StageDischarge 

### TEST Manning's Portion #####
##import barom_data as b
##Fbarometric = b.Wx() #returns dictionary of Fagaalu Prime wx station 
##Tbarometric = b.Tula() #returns dictionary of TULA met station
##barometric_data = Tbarometric
##import PT_data as PT
##PT1datalist = PT.PT1_stage(barometric_data)
##n = 0.003
##S = 0.0029
##Mannings_rect(PT1datalist,'LBJ',n,S,459.3)

#################################################################################################################
#################################################################################################################


def Weir_rect(PTdatalist,crestHeight,crestwidth):
    crestH = float(crestHeight) # cm
    width = float(crestwidth) # feet
    ## Calculates Q from stage Height (Chin, 2006)
    ## for a rectangular unsuppressed weir (constricted)
    StageDischarge = []
    Hlist = []
    for line in PTdatalist:
        try:
            #print line
            Stagetime = line[0] ## Time object from Q calculation above
            ## Round minutes off to nearest 15minutes
            Stagetime = RoundTo15(Stagetime)
            stage = line[1].split(',')[1]
            if stage != 'NaN' and float(stage)>= crestH:
                H = float(stage) - crestH # cm - cm
                Hlist.append(H)
                H = H/30.48 #cm to feet
                crestH = crestH/30.48 #cm to feet
                Hratio = H/crestHeight
                a = math.pow((14.14/(8.15+Hratio)),10.0)
                b = math.pow((Hratio/(Hratio+1)),15.0)
                Cd = 1.06*(math.pow((a+b),-0.01)) ## Chin,2006
                Cw = (2.0/3.0)*(math.pow((2*9.81),0.5))*Cd
                width = width # feet
                RectWeirQ = Cw*(width-(0.1*2.0*H))*(math.pow(H,1.5)) ## cfs
                RectWeirQ = RectWeirQ * 0.028316846593389  ## cfs to m^3/s from unitconverterpro.com
                RectWeirQ = RectWeirQ * 1000 # m^3/s to L/s
                StageDischarge.append((Stagetime,str(stage)+','+str(RectWeirQ)))
            else:
                pass
        except:
            raise
    return StageDischarge ## cubic meter per second

###### TEST
##import barom_data as b
##Fbarometric = b.Wx() #returns dictionary of Fagaalu Prime wx station 
##Tbarometric = b.Tula() #returns dictionary of TULA met station
##barometric_data = Fbarometric
##import PT_data as PT
##PT2datalist = PT.PT2_stage(barometric_data)
##crestHeight = 25.8
##crestWidth = 9.0
##st = RectWeir(PT2datalist,crestHeight,crestWidth)

def Weir_vnotch(PTdatalist,angle,notchHeight):
    theta = float(angle) ## in degrees
    notchH = float(notchHeight) ## in cm
    ## Calculates Q from stage Height (Chin, 2006)
    ## for a V-notch weir, alternative Kinsvater and Shen (USBR 1997)
    StageDischarge = []
    for line in PTdatalist:
        try:
            #print line
            Stagetime = line[0] ## Time object from Q calculation above
            ## Round minutes off to nearest 15minutes
            Stagetime = RoundTo15(Stagetime)
            stage = line[1].split(',')[1]
            if stage != 'NaN' and float(stage) >= notchH:
                H = float(stage) - notchH #cm
                H = H/30.48 #cm to feet
                Cd = 0.6072-(0.000874*theta)+(0.0000061*(theta**2)) ## from LMNO engineering and Chin, 2006
                k = 0.0144902648-(0.00033955535*theta)+(0.00000329819003*(theta**2))-(0.0000000106215442*(theta**3))
                a = math.tan(math.radians(theta)/2.0)
                b = math.pow((H + k),2.5)
                VnotchQ = 4.28*Cd*a*b
                VnotchQ = VnotchQ * 0.028316846593389  ## cfs to m^3/s from unitconverterpro.com
                VnotchQ = VnotchQ * 1000
                StageDischarge.append((Stagetime,str(stage)+','+str(VnotchQ)))
            else:
                pass
        except:
            raise    
    return StageDischarge

#### TEST
##import barom_data as b
##Fbarometric = b.Wx() #returns dictionary of Fagaalu Prime wx station 
##Tbarometric = b.Tula() #returns dictionary of TULA met station
##barometric_data = Fbarometric
##import PT_data as PT
##PT2datalist = PT.PT2_stage(barometric_data)
##angle = 163.0
##notchH = 25.8
##VnotchWeir(PT2datalist,angle,notchH)



#################################################################################################################
#################################################################################################################

def Flume(PTdatalist):
    StageDischarge = []
    for line in PTdatalist:
        try:
            #print line
            Stagetime = line[0] ## Time object from Q calculation above
            ## Round minutes off to nearest 15minutes
            Stagetime = RoundTo15(Stagetime)
            stage = line[1].split(',')[1]
            if stage != 'NaN':
                h = float(stage)/30.48
                Qflume=479.5 * math.pow((h - 0.006),1.508)
                StageDischarge.append((Stagetime,str(stage)+','+str(Qflume)))
            else:
                pass
        except:
            raise
    return StageDischarge

###### TEST
##import barom_data as b
##Fbarometric = b.Wx() #returns dictionary of Fagaalu Prime wx station 
##Tbarometric = b.Tula() #returns dictionary of TULA met station
##barometric_data = Fbarometric
##import PT_data as PT
##PT3datalist = PT.PT3_stage(barometric_data)
##flume = DamFlume(PT3datalist)



###OLD code: I don't think this actually did what I wanted it to do
def AV_rating_curveOLD(location,stage_data,trap=False):
    path = datadir+'Q/'
    Filelist = os.listdir(path)
    Qtime,Qdata = [],[] ## Empty DataFrame to add data to
    for f in Filelist:
        #print f
        if f.endswith('.txt')==True and f.startswith(location)==True:
            ## Open File, create blank parameters
            Flowfile = open(path+f)
            Flabel = 'Flabel'
            Qlist = [] ## make a new list for each file/measurement to append all the Q's to
            Qsum, Flow1, Depth1, Dist1, Q, Qm3=0,0,0,0,0,0 ## create empty variables
            for line in Flowfile:
                split = line.strip('\n')
                split = split.split('\t')
                #print split
                ## Handle date time
                ## handle header: Location,Date,Time
                if split[0]==location:
                    try:
                        ## print Q from previous measurement
                        if len(Qlist)>0: ## will only calculate Q if the list is populated
                            for Q in Qlist:
                                Qsum = Qsum+Q ## Sum up Q from each stream segment
                                #print str("%.1f" % Qsum)
                            #print str(Ftime)+' '+Location+' '+str("%.1f" % Qsum)+' L/sec'
                            Qdata.append(Qsum)
                            Qtime.append(Ftime)
                        #print split
                        Date = split[1]
                        Time = split [2]
                        Name = 'Flow '+location+' '+Date+' '+Time
                        datesplit = Date.split('/')
                        Fyear = int(datesplit[2])  
                        if len(str(Fyear)) == 2:
                            Fyear = '20'+Fyear
                        Fmonth = int(datesplit[0])
                        Fday = int(datesplit[1])
                        # Must be in 24hour time, this is not amateur hour
                        if len(str(Time))==3:
                            Time = '0'+str(Time)
                        Fhour = int(Time[0:2])
                        Fminute = int(Time[2:])
                        Ftime = RoundTo15(datetime.datetime(Fyear,Fmonth,Fday,Fhour,Fminute))
                        ## RESET parameters for next measurement!!!
                        Qsum, Flow1, Depth1, Dist1, Q, Qm3=0,0,0,0,0,0
                        Qlist = []
                    except:
                        raise
                        #print 'skipped!'
                        Qsum, Flow1, Depth1, Dist1, Q, Qm3=0,0,0,0,0,0
                        Qlist = []
                        pass
                ## Get data for Distance across stream and Flow
                try: ## Make sure the line has numbers
                    Num = float(split[0])
                    Num = True
                except:
                    Num = False
                if Num == True:
                    if trapezoidal == True:
                        Dist2 = float(split[0])*12*2.54 ## Feet to cm
                        Depth2 = float(split[1]) ## Centimeters
                        Flow2 = float(split[2]) ## meters/sec
                        #print str(Dist2)+'\t'+str(Depth2)+'\t'+str(Flow2)
                        Area = (((Depth1+Depth2)/2)*(Dist2-Dist1))/10000 ## Area of Trapezoid m2
                        Velocity = (Flow1+Flow2)/2 ## Average Velocity between two measurements = center of trapezoid
                        Qm3 = Area * Velocity ## m3/sec
                        Q = Qm3 * 1000 ## L/sec
                    elif trapezoidal == False:
                        Dist2 = float(split[0])*12*2.54 ## Feet to cm
                        Depth2 = float(split[1]) ## Centimeters
                        Flow2 = float(split[2]) ## meters/sec
                        #print str(Dist2)+'\t'+str(Depth2)+'\t'+str(Flow2)
                        Area = ((Depth2)*(Dist2-Dist1))/10000 ## Area of Trapezoid m2
                        Velocity = (Flow1+Flow2)/2 ## Average Velocity between two measurements = center of trapezoid
                        Qm3 = Area * Velocity ## m3/sec
                        Q = Qm3 * 1000 ## L/sec
                    #print str("%.1f" % Q)
                    Qlist.append(Q) ## list of Q from each segment to be summed up above^
                    Flow1 = Flow2 ## set for next calculapion
                    Dist1 = Dist2 ## set for next calculation
                    Depth1 = Depth2 ## set for next calculation
            ## print Q from last measurement in the Flowfile
            if len(Qlist)>0: ## will only calculate Q if the list is populated
                for Q in Qlist:
                    Qsum = Qsum+Q ## Sum up Q from each stream segment
                    #print str("%.1f" % Qsum)
                #print str(Ftime)+' '+location+' '+str("%.1f" % Qsum)+' L/sec'
                Qdata.append(Qsum)
                Qtime.append(Ftime)

    ## Get stage data from PT's for the above Q measurements
    d= {'Q':Qdata}
    StageDischarge = pd.DataFrame(d,index=Qtime)
    StageDischarge['stage']=stage_data[location].ix[StageDischarge.index]
    return StageDischarge











