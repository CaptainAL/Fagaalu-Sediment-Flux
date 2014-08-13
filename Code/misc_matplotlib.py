from matplotlib import collections as collections
from matplotlib.dates import WeekdayLocator, HourLocator, date2num, DateFormatter
from matplotlib import pyplot as plt
from pandas import DataFrame, to_datetime, date_range
import datetime

def Sundays(subplot,PT1):
    timespan = date_range(PT1.index[0],PT1.index[-1],freq='D',normalize=True)
    daylist = [date2num(time.to_datetime()) for time in timespan.tolist()]
#    dayofweek_bool = [int(datetime.date.weekday(time.to_datetime()))>5 for time in timespan]
    dayofweek_bool = [time.weekday()>5 for time in timespan]
    collection = collections.BrokenBarHCollection.span_where(daylist, ymin=0, ymax=80000, where=dayofweek_bool, facecolor='b', alpha='.05')
    subplot.add_collection(collection)
    return collection

#### Graphing functions
def ShadeSunday(subplot,timespan):
    timelist = [date2num(date) for date in timespan]
    dayofweek_bool = [int(datetime.date.weekday(time.to_datetime()))>5 for time in timespan]
    collection = collections.BrokenBarHCollection.span_where(timelist, ymin=0, ymax=80000, where=dayofweek_bool, facecolor='b', alpha='.05')
    subplot.add_collection(collection)
    return collection

def SundayShade(subplot,Data):
    times = PT1.iterrows()
    timelist = [date2num(index) for (index,value) in times]
    Sundays = [datetime.date.weekday(index.to_datetime()) for (index,value) in times]
    collection = collections.BrokenBarHCollection.span_where(times, ymin=0, ymax=80000, where=Sundays>5, facecolor='r', alpha='.07')
    subplot.add_collection(collection)

def FormatXdate(Subplot):
    days = WeekdayLocator(byweekday=None,interval=1,tz=None)
    hours = HourLocator(byhour=None, interval=6,tz=None)
    Subplot.xaxis.set_major_locator(days)
    Subplot.xaxis.set_minor_locator(hours)
    Subplot.xaxis.set_major_formatter(DateFormatter('%a %b-%d'))
    Subplot.xaxis.set_minor_formatter(DateFormatter('%H:%M'))
    plt.setp(Subplot.get_xticklabels(), rotation='vertical', fontsize=9)

def LegendWithPrecip(Subplot):
    handles, labels = Subplot.get_legend_handles_labels()
    try:
        Precip_plot == True
        handles.append(Precip_plot)
        labels.append('Precip')
        plt.legend(handles,labels)
    except:
        plt.legend(handles,labels)

def labelPoints(subplot,labels,xvals,yvals):
    for label, x, y in zip(labels,xvals,yvals):
        subplot.annotate(
            label, 
            xy = (x, y), xytext = (-15, -15),
            textcoords = 'offset points', ha = 'left', va = 'bottom',
            arrowprops = dict(arrowstyle = '-', connectionstyle = 'arc3,rad=0'),fontsize=7) ##bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
def colorBar(series,labels=[]):
    cbar = plt.colorbar(series,orientation='vertical',shrink=.5)
    cbar.ax.set_yticks(dt.date2num(labels))
    cbar.ax.set_yticklabels(labels)
    cbar.ax.xaxis.set_major_locator(mpl.ticker.MaxNLocator(nbins=3))
##sundays = WeekdayLocator(SUNDAY)        # major ticks on the mondays
##alldays = DayLocator()
##auto = AutoDateLocator()
##hours = HourLocator()
##stage.xaxis.set_major_locator(alldays)
##stage.xaxis.set_major_formatter(DateFormatter('%b %d'))
##stage.xaxis.set_minor_locator(hours)
##stage.xaxis.set_minor_formatter(DateFormatter('%H:%M'))

