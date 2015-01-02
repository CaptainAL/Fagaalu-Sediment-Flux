import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as dt
import numpy as np
import datetime
#from datetime import date
import os
import math as m
from pandas import *
from pandas import Series, DataFrame
plt.close('all')
##plt.ion()

from misc_time import * ##import my custom modules
from misc_numpy import *
from misc_matplotlib import *

#### Get Weather data for PT correction
from load_data import *

FP = Wx()

Precip['FPrain']=FP['FPrain'] ## Wx()[1] is the precip data in a Series
Precip['FPrain-30']=Precip['FPrain'].resample('30Min',how=sum)
Precip['FPhourly'] = Precip['FPrain'].resample('H',how='sum') ## label=left?? 
Precip['FPdaily'] = Precip['FPrain'].resample('D',how='sum')

allbaro= DataFrame(FP['FPbaro']) ## Wx()[0] is the barometric data in a Series
allbaro['ndbc'] = ndbc() ## ndbc() returns a Series
allbaro['TULAbaro']=Tula()
#allbaro = CombineBaroData(FPbaro,NDBCbaro,TULAbaro) ## pandas merge

PT1 = PT_Hobo_stage(allbaro,'PT1 LBJ bridge','C:/Users/Alex/Desktop/samoa/WATERSHED_ANALYSIS/FAGAALU/MasterDataFiles/Fagaalu1_MASTER.txt') ## returns Series
PT2 = PT_LevelLogger_stage(allbaro,'PT2 Drive Thru','C:/Users/Alex/Desktop/samoa/WATERSHED_ANALYSIS/FAGAALU/MasterDataFiles/Fagaalu2_MASTER.txt')
stage_data = DataFrame({'LBJ':PT1,'DT':PT2,'Dam':PT3})

### Stage to discharge: Rating Curves
order=2
from stage2discharge_ratingcurve import *
#### LBJ
### Area Velocity and Mannings from in situ measurments
LBJstageDischarge = AV_rating_curve('LBJ',stage_data) ### Returns DataFrame of Stage and Discharge calc. from AV measurements with time index
LBJstageDischarge['Q-ManningsAV'] = Mannings_file('LBJ',stage_data) ### Adds Discharge from A measurments, V from Mannings to DataFrame

