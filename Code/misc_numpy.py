import numpy as np
from matplotlib import pyplot as plot
from pandas import DataFrame

#### Line-fitting
## Polynomial linefit: this function fits and plots a
## polynomial line of order n to a x,y scatter plot and returns the equation 
def Polyfit(x, y, order=1, color='k--',lab='label',Xvals=10,subplot=plot):
    df=DataFrame({'x':x.values,'y':y.values},index=x.index)
    df = df.dropna()
    print df
    PolyCoeffs = np.polyfit(df['x'], df['y'], order) ## calculates polynomial coeffs
    PolyEq = np.poly1d(PolyCoeffs) ## turns the coeffs into an equation
    #print PolyEq
    PolyXvals = np.linspace(min(x), max(x)+Xvals) ## creates x-values for trendline
    #print PolyXvals
    Polyplot = subplot.plot(PolyXvals, PolyEq(PolyXvals),color,label=lab) ## plots the trendline
    return Polyplot

def PolyEq(x, y, order=1):
    try:
        df=DataFrame({'x':x,'y':y},index=x.index)
        df = df.dropna()
        PolyCoeffs = np.polyfit(df['x'], df['y'], order) ## calculates polynomial coeffs
        PolyEq = np.poly1d(PolyCoeffs) ## turns the coeffs into an equation
    except:
        print 'No regression equation possible'
        PolyEq = np.poly1d([0])
    return PolyEq
