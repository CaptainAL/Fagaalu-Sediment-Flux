import datetime

def DayofWeek(timeobject):
    weekday = date.weekday()
    daysofWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    Day = daysofWeek[weekday]
    return Day
def Sunday(timeobject):
    weekday = timeobject.weekday()
    if weekday == 6:
        return True
    elif weekday !=6:
        return False
#### Rounding time
def RoundTo15(time): ## This function takes a time object and rounds up/down to nearest 15 minute interval
    countup = 0 ## Try Rounding Up
    OGtime = time ## hang on to the original time
    while time.minute!= 00 and time.minute!= 15 and time.minute!= 30 and time.minute!= 45:
        time = time + datetime.timedelta(0,0,0,0,1) #add a minute
        countup+=1
        roundup = time
        #print time
    countdown = 0 ## Try Rounding Down
    time = OGtime
    while time.minute!= 00 and time.minute!= 15 and time.minute!= 30 and time.minute!= 45:
        time = time - datetime.timedelta(0,0,0,0,1) #add a minute
        countdown+=1
        rounddown = time
        #print time
    ## Pick which (up or down) is smallest and take that time as the minutes
    if countup < countdown:
        time = roundup
    elif countup> countdown:
        time = rounddown
    return time
def RoundTo5(time): ## This function takes a time object and rounds up/down to nearest 5 minute interval
    countup = 0 ## Try Rounding Up
    OGtime = time ## hang on to the original time
    while time.minute % 5!=0:
        time = time + datetime.timedelta(0,0,0,0,1) #add a minute
        countup+=1
        roundup = time
        #print time
    countdown = 0 ## Try Rounding Down
    time = OGtime
    while time.minute % 5!=0:
        time = time - datetime.timedelta(0,0,0,0,1) #add a minute
        countdown+=1
        rounddown = time
        #print time
    ## Pick which (up or down) is smallest and take that time as the minutes
    if countup < countdown:
        time = roundup
    elif countup> countdown:
        time = rounddown
    return time

## Average (Turbidity) data from 5min to 15min (to match PT's and Discharge data)
def Average15min(turbiditylist):
    avgList = []
    avgData = []
    for line in turbiditylist:
        #print line
        time = line[0]
        if len(line[1].split(','))==2:
            NTU = line[1].split(',')[1]
        else:
            NTU= line[1]
        if time.minute % 15 != 0:
            avgData.append(NTU) ## NTU is second value in tuple: (Time, Temp,NTU)
            #print time, NTU
        if time.minute % 15 == 0:
            avgData.append(NTU)
            total = 0
            for data in avgData:
                total = total+float(data)          
            average = (total/3)
            avgList.append((time,average))
            #print time,avgData,total,average
            avgData = [] ## reset list for next 3 values
    return avgList

def DefIntegral(StartTime,EndTime,Dictionary,DataListLocation,timestep=15):
    DeltaTime = EndTime - StartTime
    #print 'Start: '+str(StartTime)+' End: '+str(EndTime)+' Time Interval= '+str(DeltaTime)
    #### Generate list of times
    TimeList = []
    time = StartTime
    while time<=EndTime:
        TimeList.append(time)
        time = time + datetime.timedelta(0,0,0,0,timestep)
    #### Total over time interval
    Total = 0
    for time in TimeList:
        Data = Dictionary[time].split(',')[DataListLocation]
        if Data == 'NaN':
            print str(time)+' Data= NaN!'
            raise
        if Data <= 0:
            Data = 0
        if Data != 'NaN':
            Total = Total + float(Data)
        #print str(time)+' Data: '+Data+' Total= '+str(Total)
    #print StartTime,EndTime,Total
    average = Total/len(TimeList)
    print 'Average = '+str(average)
    return {'Total':Total,'DeltaTime':DeltaTime}

def InterpolateData(time,dataframe,interval=15):
    Timeprev = time - datetime.timedelta(0,0,0,0,int(interval))
    Timeafter = time + datetime.timedelta(0,0,0,0,int(interval))
    dataprev = dataframe[location].ix[Timeprev]
    dataafter = dataframe[location].ix[Timeafter]
    interpolated = (float(dataprev) + float(dataafter))/2
    return interpolated

### I think I broke this, it should be similar to aggregate_daily but just use aggregate (below)
def aggregate_hourly(datalist, listlocation = 0):
    print 'Aggregating hourly...'
    import datetime
    def generate_dates(start_date, end_date):
        dates = []
        td = datetime.timedelta(hours=1)
        current_date = start_date
        while current_date <= end_date:
            #print current_date
            dates.append((current_date,0))
            current_date += td
        return dates

    start_date = datetime.datetime(2012,1,3,0)
    end_date = datetime.datetime(2013, 3, 20,0)
    dateslist = generate_dates(start_date, end_date)
    datesdict = dict(dateslist)

    listloc = listlocation ## For lists with multiple values
    hourlist = []
    for i in sorted(datadict):
        print key.hour
        #year,month,day,hour = i[0],i[1],i[2],i[3]
        #print str(month)+' '+str(day)
        hourlydata = 0.0 ## New day, new value
        
        if listloc !=0:
            try:
                for key in datadict:
                    if key == i:
                        hourlydata = hourlydata + float(datadict[key].split(',')[listloc]) ##  pick value
                        print str(month)+' '+str(day)+' '+str(value)+' '+str(dailydata)
            except:
                pass
        else:
            try:
                for key in datadict:
                    if key == i:
                        hourlydata = hourlydata + float(datadict[key]) ##  pick value
                        print str(month)+' '+str(day)+' '+str(value)+' '+str(dailydata)
            except:
                pass
        try:
            #print str(month)+' '+str(day)+' '+str(dailydata)
            hourlist.append((datetime.datetime(year,month,day,hour),str(hourlydata)))
        except:
            pass

    return hourlist

def aggregate_daily(datalist,listlocation=0):
    print 'Aggregating daily...'
    yearmonthday=[]
    years = [2012,2013]
    monthrange = range(1,13)
    dayrange = range(1,32)
    for year in years:
        for month in monthrange:
            for day in dayrange:
                yearmonthday.append((year,month,day)) ##tuple of every month,day combination

    datadict = dict(datalist)
    data = datadict.iteritems()
    listloc = listlocation
    daylist = []
    for i in yearmonthday:
        year,month,day = i[0],i[1],i[2]
        #print str(month)+' '+str(day)
        dailydata = 0.0 ## New day, new value
        if listloc != 0:
            try:
                for key,value in data:
                    if key.year and key.month == month and key.day == day:
                        dailydata = dailydata + float(value.split(',')[listloc])
                        #print str(month)+' '+str(day)+' '+str(value)+' '+str(dailydata)
            except:
                pass
        try:
            for key,value in data:
                if key.year and key.month == month and key.day == day:
                    dailydata = dailydata + float(value)
                    #print str(month)+' '+str(day)+' '+str(value)+' '+str(dailydata)
        except:
            pass
        try:
            #print str(month)+' '+str(day)+' '+str(dailydata)
            daylist.append((datetime.datetime(year,month,day),str(dailydata)))
        except:
            pass

    return daylist

def aggregate_monthly(datalist,listlocation=0):
    print 'Aggregating monthly...'
    yearmonths = []
    years = [2012,2013]
    months = range(1,13)
    for year in years:
        for month in months:
            yearmonths.append((year,month))
    datadict = dict(datalist)
    listloc = listlocation
    #print 'listlocation '+str(listlocation)
    monthlist = []
    for i in yearmonths:
        year,month = i[0],i[1]
        #print str(month)
        monthlydata = 0.0 ## New day, new value
        if listloc!=0:
            try:
                for key,value in datadict.iteritems():
                    if key.year == year and key.month == month:
                        datavalue = value.split(',')[listloc]
                        if datavalue == 'NaN' or datavalue == 'nan' or float(datavalue)<0.0:
                            datavalue = 0.0
                        elif datavalue != 'NaN':
                            monthlydata = monthlydata + float(datavalue)                        
                        #print str(month)+' '+str(datavalue)+' '+str(monthlydata)
            except:
                pass
        try:
            for key,value in datadict.iteritems():
                if key.year==year and key.month == month:
                    monthlydata = monthlydata + float(value)
                    #print str(month)+' '+str(value)+' '+str(monthlydata)
        except:
            pass
        try:
            #print str(year)+' '+str(month)+' '+str(monthlydata)
            monthlist.append((datetime.datetime(year,month,1),str(monthlydata)))
        except:
            raise

    return monthlist


def aggregate(datalist,listlocation=1,start_date=datetime.datetime(2012,1,6,0),end_date=datetime.datetime(2013, 3, 20,0),hourstep=1,timestep=15):
    print 'Aggregating by '+str(hourstep)+' hours'
    ## Create empty list 
    def generate_dates(start_date, end_date):
        dates = []
        td = datetime.timedelta(hours=hourstep)
        current_date = start_date
        while current_date <= end_date:
            #print current_date
            dates.append((current_date,'NaN'))
            current_date += td
        return dates
    dateslist = generate_dates(start_date, end_date)

    listlocation = 0 ## default to grab first data column after the time; for lists with multiple values
    intervaldatalist = []

    t1 = dateslist[0][0] ## first start time is start of list
    count = 0
    datadict = dict(datalist)
    for d in dateslist: ## run through the list of empty containers
        count+=1 ## count up one to get the next one in the list
        try:
            timeint = t1
            t2 = dateslist[count][0] ## gets time of next item in list
            #print t1 ## start time
            # Data over an interval starts with data from starttime and does not include the data from the end time
            # This is consequent of HOBO logger data processing. Any events are assigned to the beginning of the interval
            intervaldata = 0.0 # reset the data for the interval
            while timeint < t2 and timeint < end_date: ## data for t2 is for events occurring after t2
                try:
                    data = datadict[timeint]#.split(',')[listlocation]
                    intervaldata = intervaldata + float(data)
                    timeint = timeint+datetime.timedelta(minutes=timestep)
                except KeyError:
                    #print 'no data for ' +str(timeint)
                    intervaldata = float('NaN')
                    timeint = timeint+datetime.timedelta(minutes=timestep)
                    pass
                except:
                    timeint = timeint+datetime.timedelta(minutes=timestep)
                    raise
            intervaldatalist.append((t1,intervaldata))
            t1 = t2 ## set new time start
        except IndexError: ## For when it hits the last element of the dateslist and it can't get t2
            pass
    return intervaldatalist
