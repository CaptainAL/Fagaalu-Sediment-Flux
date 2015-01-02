import os
import datetime

#ylist = ['2008','2009','2010','2011','2012'] ##years needed
ylist = ['2012']

newpath = 'C:/TulaMetData/Daily/'

TulaPressureList = []
#print 'month'+'\t'+'day'+'\t'+'year'+'\t'+'mm precip'
for y in ylist:
    path = 'C:/TulaMetData/'+y
    files = os.listdir(path)
    for f in files: ## each f is a new DAY
        data = open(path+'/'+f,'r')
        daysplit = f.replace('.','-').split('-')
        #dayfile = open(daysplit[1]+'-'+daysplit[2]+'-'+daysplit[0]+'.csv','w')
        year = daysplit[0]
        month = daysplit[1]
        day = daysplit[2]
        #print 'year: '+year+' month '+month+' day: '+day
        dailyprecip, precipprev, precip15, pressure = 0.0,0.0,0.0,0.0
        presscount = 0
        try:
            for d in data: ## each d is a new MINUTE
                split = d.split(',')
                try:
                    num =float(split[1])
                except:
                    num = False
                    pass
                if num != False: ## Make sure the line is data #
                    #print split[1]+','+split[2]+','+split[3]+','+split[4]+','+split[5]+','+split[13]+','+split[18]
                    hour = split[4]
                    minute = split[5]
                    press = float(split[13])
                    precip = float(split[18]) ## subtract the previous Minute's precip value
                    presscount+=1
                    try:
                        if press != 9999:
                            pressure = pressure + float(press)
                    except:
                            raise
                    try:
                        if precip != 9999:
                            #print str(precip)+' - '+str(precipprev)
                            precip = precip-precipprev
                            #print precip
                            precip15=precip15+precip
                            precipprev = float(split[18])
                    except:
                            precip = 'NaN'
                            pass
                    if float(minute) == 0 or float(minute)==15 or float(minute)==30 or float(minute)==45:
                            pressure15 = pressure/presscount
                            dailyprecip = dailyprecip+precip
                            #print month+'/'+day+'/'+year+'\t'+hour+':'+str(minute)+'\t'+str(pressure15)+'\t'+str(precip15)
                            print month+'/'+day+'/'+year+'\t'+hour+':'+str(minute)+'\t'+str(pressure15)
                            Time = datetime.datetime(int(year),int(month),int(day),int(hour),int(minute))
                            TulaPressureList.append((Time,pressure15))
                            precipprev = float(split[18])
                            precip15, pressure,presscount = 0,0,0
        except:
                pass
        
        #print month+'\t'+day+'\t'+year+'\t'+str(dailyprecip)
datadict = dict(TulaPressureList)
for line in TulaPressureList:
        time = line[0]
        pressure = line[1]
        if pressure <= 990:
            try:
                Timeprev = time - datetime.timedelta(0,0,0,0,int(15))
                Timeafter = time + datetime.timedelta(0,0,0,0,int(15))
                dataprev = datadict[Timeprev]
                dataafter = datadict[Timeafter]
                pressure= (float(dataprev) + float(dataafter))/2
            except:
                pressure = 0.0
        

                                            
                
        
                

                

