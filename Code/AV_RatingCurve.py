# -*- coding: utf-8 -*-
"""
Created on Fri Aug 29 09:12:05 2014

@author: Alex
"""
import os

def AV_RatingCurve(path,location,stage_data,slope=.01,Mannings_n=.033,trapezoid=True):
    Filelist = os.listdir(path)
    
    S = slope
    n = Mannings_n
    
    ## iterate over files in directory to get Flow.txt file
    for f in Filelist:
        ## Select Flow.txt file
        if f.endswith('Flow.txt')==True and f.startswith(location)==True:
            print 'file selected for analysis: '+f
            ## Open File, create blank parameters
            Flowfile = open(path+f)
            Qdf = pd.DataFrame() ## empty dataframe to append calculated Q
             
            df = pd.DataFrame(columns=['dist','depth','flow']) ## empty dataframe for Flowmeter data
            for line in Flowfile:
                split = line.strip('\n')
                split = split.split('\t')
                print split
                # Test if data is number
                try:
                    a= float(split[0])
                    isfloat=True
                except ValueError:
                    isfloat=False            
                ## Determine DateTime of AV measurment
                if split[0]==location:
                    date, time = split[1].split('/'),split[2]
                    if len(time)==3:
                        time = '0'+time
                    DateTime = dt.datetime(int(date[2]),int(date[0]),int(date[1]),int(time[0:2]),int(time[2:]))
                    print DateTime
                ## Append data
                elif isfloat==True:
                    df=df.append(pd.DataFrame({'dist':split[0],'depth':split[1],'flow':split[2]},index=[DateTime]))
                elif split[0]=='Location' or split[0]=='Field Measurements' or split[0]=='Dist(S to N)(ft)' or split[0]=='Dist(ft)':
                    pass
                
                
                ## At the end of that AV measurment, calculate Q
                elif split[0]=='-':
                    print 'calculating Q for '+str(DateTime)
                    df = df.astype('float')
                    if trapezoid==True:
                        ## Depth/flow measurements are made at the midpoint of the trapezoid, dimensions of the trapezoid have to be determined
                        valbelow = df['dist'].shift(-1).sub(df['dist'],fill_value=0) ##Distance below - Distance = the width to the right
                        valabove = df['dist'].sub(df['dist'].shift(1),fill_value=0) ## Distance above - Distance = the width to the left
                        df['width']=(valbelow.add(valabove)/2)*12*2.54 ## 2nd mark - first; then convert to cm
                        df['b1']=(df['depth'].add(df['depth'].shift(1),fill_value=0))/2 ## gives average of Depth Above and depth
                        df['b2']=(df['depth'].add(df['depth'].shift(-1),fill_value=0))/2 ## gives average of Depth Below and depth
                        df['trapezoidal-area']=.5*(df['b1']+df['b2'])*df['width'] ## Formula for area of a trapezoid = 1/2 * (B1+B2) * h; h is width of the interval and B1 and B2 are the depths at the midpoints between depth/flow measurements
                        df['trapezoidal-area']=df['trapezoidal-area']/10000 ##cm2 to m2
                        df['Q-Area']=df['trapezoidal-area']*df['flow'] *1000 ## m2 x m/sec x 1000 = L/sec
                        AV_Q = df['Q-Area'].sum()
                        Area = df['trapezoidal-area'].sum()
                        V = df['flow'].mean()
                        
                        ## Wetted perimeter doesn't use midpoints between depth/flow measurments
                        df['WP']=  ((df['depth'].sub(df['depth'].shift(1),fill_value=0))**2 + (df['dist'].sub(df['dist'].shift(1),fill_value=0)*12*2.54)**2)**0.5 ## WP = SQRT((Dnext-D)^2 + Width^2)
                        df['WP']=(df['WP']*(df['b1']>0))/100 ## cm to m; and only take WP values where the depth to the left is not zero
            
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
                        df['Q-Area']=df['rectangular-area']*df['flow']
                        
                        AV_Q = df['Q-Area'].sum()
                        Area = df['rectangular-area'].sum()
                        V = df['flow'].mean()
                        ManningV = np.nan
                    
                    try:
                        stage = stage_data[location].ix[DateTime] ## Get Stage data
                    except:
                        stage =np.nan
                    Qdf = Qdf.append(pd.DataFrame({'stage(cm)':stage,'Q(L/s)':AV_Q,'ManningQ(L/s)':ManningQ,'Area(m2)':Area,'V(m/s)':V,'ManningV(m/s)':ManningV},index=[DateTime]))
                    print str(DateTime)+': stage='+'%.2f'%stage+' Q= '+'%.2f'%AV_Q+' ManningQ= '+'%.2f'%ManningQ
                    ## Create new df for next measurement
                    df = pd.DataFrame(columns=['dist','depth','flow'])
                    
    return Qdf                

    
