# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 14:05:01 2015

@author: Alex
"""

#### LBJ Baseflow Separation
from numpy import *
import scipy as sp
from pandas import *
from rpy2.robjects.packages import importr
import rpy2.robjects as ro
import pandas.rpy.common as com

#

ro.r('x=c()')
ro.r('x[1]=22')
ro.r('x[2]=44')
print(ro.r('x'))

LBJ_Q = pd.DataFrame({'Q':LBJ['Q'].values},index = LBJ['Q'].index)

## convert to R Data Frame
hydrograph = com.convert_to_r_dataframe(LBJ_Q)
## Send to R
ro.globalenv['flowdata'] = hydrograph
## replace blanks with NA
ro.r('flowdata[flowdata==""]<-NA')
## Drop NA rows from Data Frame
ro.r('flow = flowdata[complete.cases(flowdata),]')
## run Baseflow Separation
ro.r("library(EcoHydRology)")
ro.r("base = BaseflowSeparation(flow)")
## Convert back to Pandas
flowdf = com.load_data("base")
## reindex with the original time index WITHOUT NA's (they're dropped in the R code)
flowdf = flowdf.reindex(index=LBJ_Q.dropna().index)