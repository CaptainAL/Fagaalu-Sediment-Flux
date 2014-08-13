import datetime as dt
from misc_time import *
from pandas import DataFrame,read_csv,ExcelFile

def raingauge(XL,sheet='',shift=0):
    print 'loading precip: '+sheet+'...'
    my_parser= lambda x: dt.datetime.strptime(x,"%m/%d/%Y %H:%M")
    gauge = XL.parse(sheet,header=1,index_col=0,parse_cols='B,C',parse_dates=True)#,date_parser=my_parser)
    gauge= gauge.shift(shift)
    gauge = gauge*.254 ##hundredths to mm
    gauge.columns=['Events']
    return gauge       

#### Add Precip from Timu1 to a subplot
def AddTimu1(FigureNum,SubPlot,Precip):
    PrecipSeries = Precip.dropna()
    ###### Timu1
    Yax1 = FigureNum.add_axes(SubPlot.get_position(), frameon=False, sharex=SubPlot)
    Precip = PrecipSeries.plot(x_compat=True,label='Precip',color='b',linestyle='steps-post',lw=.4) 
    #### Format Secondary Y axis
    Yax1.set_ylabel('Precipitation(mm/15min)')
    Yax1.set_ylim(0,90)
    Yax1.yaxis.set_ticks_position('right')
    Yax1.yaxis.set_label_position('right')
    #Yax1.set_xlim(PrecipSeries.index[0],PrecipSeries.index[-1]) ##First and last timestamp
    Yax1.xaxis.set_visible(False)
    Yax1.yaxis.label.set_color(Precip.lines[0].get_color())
    Yax1.tick_params(axis='y',colors=Precip.lines[0].get_color())
    Yax1.grid(False)
    return Precip


#### Add Precip from Timu1 to a subplot
def AddTimu1Hourly(FigureNum,SubPlot,Precip):
    PrecipSeries = Precip.dropna()
    ###### Timu1
    Yax1 = FigureNum.add_axes(SubPlot.get_position(), frameon=False, sharex=SubPlot)
    Precip = PrecipSeries.plot(x_compat=True,label='Hourly Precip',color='b',linestyle='steps-post',lw=.4) 
    #### Format Secondary Y axis
    Yax1.set_ylabel('Precipitation(mm/hr)')
    Yax1.set_ylim(0,90)
    Yax1.yaxis.set_ticks_position('right')
    Yax1.yaxis.set_label_position('right')
    Yax1.set_xlim(PrecipSeries.index[0],PrecipSeries.index[-1]) ##First and last timestamp
    Yax1.xaxis.set_visible(False)
    Yax1.yaxis.label.set_color(Precip.lines[0].get_color())
    tkw=dict(size=4,width=1.5)
    Yax1.tick_params(axis='y',colors=Precip.lines[0].get_color(),**tkw)
    return Precip

#### Add Precip from Timu1 to a subplot
def AddTimu1Daily(FigureNum,SubPlot,PrecipSeries):
    PrecipSeries.dropna()
    ###### Timu1
    Yax1 = FigureNum.add_axes(SubPlot.get_position(), frameon=False, sharex=SubPlot)
    Precip = PrecipSeries.plot(x_compat=True,label='Daily Precip',color='b',linestyle='steps-post',lw=.4) 
    #### Format Secondary Y axis
    Yax1.set_ylabel('Precipitation(mm/day)')
    Yax1.set_ylim(0,200)
    Yax1.yaxis.set_ticks_position('right')
    Yax1.yaxis.set_label_position('right')
    Yax1.set_xlim(PrecipSeries.index[0],PrecipSeries.index[-1]) ##First and last timestamp
    Yax1.xaxis.set_visible(False)
    Yax1.yaxis.label.set_color(Precip.lines[0].get_color())
    tkw=dict(size=4,width=1.5)
    Yax1.tick_params(axis='y',colors=Precip.lines[0].get_color(),**tkw)
    return Precip

def AddTimu1Monthly(FigureNum,SubPlot,PrecipSeries):
    PrecipSeries.dropna()
    ###### Timu1
    Yax1 = FigureNum.add_axes(SubPlot.get_position(), frameon=False, sharex=SubPlot)
    Precip = PrecipSeries.plot(x_compat=True,label='Monthly Precip',color='b',linestyle='steps-post',lw=.4) 
    #### Format Secondary Y axis
    Yax1.set_ylabel('Precipitation(mm/month)')
    Yax1.set_ylim(0,500)
    Yax1.yaxis.set_ticks_position('right')
    Yax1.yaxis.set_label_position('right')
    Yax1.set_xlim(PrecipSeries.index[0],PrecipSeries.index[-1]) ##First and last timestamp
    Yax1.xaxis.set_visible(False)
    Yax1.yaxis.label.set_color(Precip.lines[0].get_color())
    tkw=dict(size=4,width=1.5)
    Yax1.tick_params(axis='y',colors=Precip.lines[0].get_color(),**tkw)
    return Precip
