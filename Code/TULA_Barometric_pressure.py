# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 06:52:00 2015

@author: Alex
"""

## THIS IS TO LOAD AND USE BAROMETRIC DATA FROM THE NOAA CLIMATE STATION AT TULA
## IT WASN'T NEEDED AFTER ADEQUATE DATA WAS FOUND FROM THE NDBC NSTP6 STATION

def Tula(datapath=datadir+'BARO/TulaStation/TulaMetData/'):
    #### Barometric Pressure from NOAA Weather Station Tula
    print 'loading TULAbaro....'
    ylist = ['2012']
    TulaPressureList = []
    #print 'month'+'\t'+'day'+'\t'+'year'+'\t'+'mm precip'
    for y in ylist:
        path = datapath+y
        files = os.listdir(path)
        for f in files: ## each f is a new DAY
            data = open(path+'/'+f,'r')
            daysplit = f.replace('.','-').split('-')
            #dayfile = open(daysplit[1]+'-'+daysplit[2]+'-'+daysplit[0]+'.csv','w')
            year, month, day = daysplit[0],daysplit[1],daysplit[2]
            #print 'year: '+year+' month '+month+' day: '+day
            dailyprecip, precipprev, precip15, pressure = 0.0,0.0,0.0,0.0
            presscount = 0
            try:
                for d in data: ## each d is a new MINUTE
                    split = d.split(',')
                    try:
                        num =float(split[1]) #will be True if split[1] is a number and the line is data
                    except:
                        num = False
                        pass
                    if num != False: ## Make sure the line is data #
                        #print split[1]+','+split[2]+','+split[3]+','+split[4]+','+split[5]+','+split[13]+','+split[18]
                        hour,minute = split[4], split[5]
                        press = split[13] #the pressure value for the Minute, need to be agg'ed to 15min.
                        precip = split[18] ## subtract the previous Minute's precip value
                        presscount+=1
                        try: ## Running total for 15 min. aggregate
                            if float(press) == False:
                                pressure = 'NaN'
                            if float(press) != 9999:
                                pressure = pressure + float(press) ## running total of pressure?
                            if float(press) == 9999:
                                pressure = pressure + 1000
                        except:
                                pressure = 'NaN'
                                pass
                                
                        try: ## Subtract previous minute's precip from current minute to get correct value
                            if float(precip) == False:
                                precip = 'NaN'
                            if precip != 9999:
                                #print str(precip)+' - '+str(precipprev)
                                precip = float(precip)-precipprev ## subtract previous minute's precip (precipprev) from current precip (precip)
                                #print precip ## this should be the correct precip value
                                precip15=precip15+float(precip) ## Running total for 15 minute aggregated rainfall
                                precipprev = split[18]
                        except:
                                precip = 'NaN'
                                pass
                        if minute == '':
                            minute = 'NaN'
                            pass
                        ## at 15 minute intervals average pressure and tally up precip
                        if float(minute) == 0 or float(minute)==15 or float(minute)==30 or float(minute)==45: ## Adjust time offset???
                                pressure15 = float(pressure)/presscount ## Get 15 minute average pressure 
                                dailyprecip = dailyprecip+float(precip) ## Aggregate daily rainfall
                                #print month+'/'+day+'/'+year+'\t'+hour+':'+str(minute)+'\t'+str(pressure15)+'\t'+str(precip15) 
                                #print month+'/'+day+'/'+year+'\t'+hour+':'+str(minute)+'\t'+str(pressure15) ## tab-separated output
                                Time = dt.datetime(int(year),int(month),int(day),int(hour),int(minute)) ## -10 so it lines up with other times
                                #print Time
                                timedelta =-dt.timedelta(hours=11)
                                Time = Time + timedelta ## time offset to get it to match Faga'alu
                                #print Time
                                TulaPressureList.append((Time,float(pressure15))) ## make list of 15 minute averaged atmospheric pressure
                                precipprev = split[18] ## reassign precip to precipprev for next loop
                                precip15,pressure,presscount = 0.0,0.0,0 ## reset variables for next loop
            except:
                    raise
            #print month+'\t'+day+'\t'+year+'\t'+str(dailyprecip)
    datadict = dict(TulaPressureList) ## Make dictionary of (Time,Pressure) tuples, RAW data
    baro = pd.Series(datadict,name='TULAbaro')
    baro_offset = (baro/10.0)+.92
    return baro_offset
    
##load data from NOAA Climate Observatory at Tula, East Tutuila
TULAbaro= pd.DataFrame(Tula(datadir+'BARO/TulaStation/TulaMetData/'),columns=['TULAbaro']) ## add TULA barometer data


## THESE LINES GO WHERE THE allbaro df is created


allbaro['TULAbaro']=TULAbaro['TULAbaro']


allbaro['Baropress']=allbaro['Baropress'].where(allbaro['Baropress']>0,allbaro['TULAbaro']) 





















