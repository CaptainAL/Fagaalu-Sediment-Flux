# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 09:25:20 2014

@author: Alex
"""

#### Calculate Discharge and Save to file

#### STAGE TO DISCHARGE ####
order=1
powerlaw = False
from stage2discharge_ratingcurve import AV_rating_curve, Mannings_rect, Weir_rect, Weir_vnotch, Flume
## Q = a(stage)**b
def power(x,a,b):
    y = a*(x**b)
    return y

### Area Velocity and Mannings from in situ measurments
## stage2discharge_ratingcurve.AV_rating_curve(location,stage_data,trapezoid=False,Slope=0.01,Mannings_n=0.03,width=4.9276)
## Returns DataFrame of Stage (cm) and Discharge (L/sec) calc. from AV measurements with time index

#### LBJ (3 rating curves: AV measurements, A measurment * Mannings V, Area of Rectangular section * Mannings V)
Slope = 0.0161 # m/m
Mannings_n=0.050 # Mountain stream rocky bed and rivers with variable sections and veg along banks (Dunne 1978)
LBJstageDischarge = AV_rating_curve('LBJ',stage_data,True,Slope,Mannings_n).dropna() #DataFrame with Q from AV measurements, Q from measured A with Manning-predicted V, stage, and Q from Manning's and assumed rectangular channel A
LBJstageDischarge = LBJstageDischarge.truncate(before=datetime.datetime(2012,3,20)) # throw out measurements when I didn't know how to use the flow meter very well
LBJstageDischargeLog = LBJstageDischarge.apply(np.log10) #log-transformed version

## LBJ: Q Models 
LBJ_AV= pd.ols(y=LBJstageDischarge['Q-AV(L/sec)'],x=LBJstageDischarge['stage(cm)'],intercept=True) 
LBJ_AVLog= pd.ols(y=LBJstageDischargeLog['Q-AV(L/sec)'],x=LBJstageDischargeLog['stage(cm)'],intercept=True) #linear fit to log-transformed stage and Q
LBJ_AManningV = pd.ols(y=LBJstageDischarge['Q-AManningV(L/sec)'],x=LBJstageDischarge['stage(cm)'],intercept=True)
LBJ_AManningVLog = pd.ols(y=LBJstageDischargeLog['Q-AManningV(L/sec)'],x=LBJstageDischargeLog['stage(cm)'],intercept=True)
LBJ_Mannings = pd.ols(y=LBJstageDischarge['Q-Mannings(L/sec)'],x=LBJstageDischarge['stage(cm)'],intercept=True) ## Rectangular channel
LBJ_ManningsLog = pd.ols(y=LBJstageDischargeLog['Q-Mannings(L/sec)'],x=LBJstageDischargeLog['stage(cm)'],intercept=True) ## Rectangular channel

#### LBJ: Q from OrangePeel method 
from notebook import OrangePeel
orangepeel = OrangePeel('OrangePeel',1,datadir+'samoa/WATERSHED_ANALYSIS/FAGAALU/Discharge/Fagaalu-StageDischarge.xlsx')
orangepeel=orangepeel.append(pd.DataFrame({'stage cm':0,'L/sec':0},index=[pd.NaT]))

#### LBJ: Q directly from MANNING'S EQUATION:  Q = CrossSectionalArea * 1.0/n * R^(2/3) * S^(1/2)
#width = 4.9276 ## meters   
#LBJ['Q-ManningsRect']=(LBJ['stage']/100*width) * (((LBJ['stage']/100*width)/((2*LBJ['stage']/100)+width)**(2.0/3.0)) * (Slope**0.5))/Mannings_n
#LBJ['Q-ManningsRect']=LBJ['Q-ManningsRect']*1000 ##m3/s to L/s
###using rating curve from Mannings Rect
#LBJ['Q-ManningsRect']=LBJ_AVratingcurve_ManningsRect(LBJ['stage']) ## Calculate Q from A-Mannings rating

#### DAM(3 rating curves: AV measurements, WinFlume, HEC-RAS
DAMstageDischarge = AV_rating_curve('Dam',stage_data) ### Returns DataFrame of Stage and Discharge calc. from AV measurements with time index
#### DAM: Q from WinFlume equation
def D_Flume(stage):
    K1 = 252.5
    K2 = 0.02236
    u = 1.639
    Q = K1*(stage/25.4 + K2)**u ##ft to cm
    return Q
DAMstageDischarge['D_Flume(L/sec)'] = DAMstageDischarge['stage(cm)'].apply(lambda x: D_Flume(x)) ## runs the Flume equation on x (stage)
DAMstageDischargeLog=DAMstageDischarge.apply(np.log10) #log-transformed version

## HEC-RAS Model of the DAM structure: Documents/HEC/FagaaluDam.prj
DAM_HECstageDischarge = pd.DataFrame(np.array([[0,0],[19.0,15.0],[23.0,60],[31.0,203.0],[34.0,261],[61.0,10000.0],[99.0,3000.0]]),columns=['stage(cm)','Q(L/sec)']) ##rating curve from HEC-RAS FagaaluDAM.prj

## DAM: Q Models
DAM_AV = pd.ols(y=DAMstageDischarge['Q-AV(L/sec)'],x=DAMstageDischarge['stage(cm)'],intercept=True) 
DAM_AVLog = pd.ols(y=DAMstageDischargeLog['Q-AV(L/sec)'],x=DAMstageDischargeLog['stage(cm)'],intercept=True) 
DAM_D_Flume = pd.ols(y=DAMstageDischarge['D_Flume(L/sec)'],x=DAMstageDischarge['stage(cm)'],intercept=True) 
DAM_HEC = pd.ols(y=DAM_HECstageDischarge['Q(L/sec)'],x=DAM_HECstageDischarge['stage(cm)'],intercept=True) 

#h = float(stage)/30.48
#Qflume=479.5 * m.pow((h - 0.006),1.508)
#def D_Flume(stage,angle=150,notchHeight=47):
#    if float(stage)<=notchHeight:
#        Q = 479.5*((stage/30.48)-.006)**1.508 ### Flume equation up to flume height (=47cm)
#    elif float(stage)>notchHeight:
#        theta = angle
#        H = float(stage) - notchHeight #cm
#        H = H/30.48 #cm to feet
#        Cd = 0.6072-(0.000874*theta)+(0.0000061*(theta**2)) ## from LMNO engineering and Chin, 2006
#        k = 0.0144902648-(0.00033955535*theta)+(0.00000329819003*(theta**2))-(0.0000000106215442*(theta**3))
#        a = math.tan(math.radians(theta)/2.0)
#        b = (H + k)**2.5
#        VnotchQ = 4.28*Cd*a*b
#        VnotchQ = VnotchQ * 0.028316846593389  ## cfs to m^3/s from unitconverterpro.com
#        Q = VnotchQ * 1000 ##Q (L/sec)
#        Q = VnotchQ + 479.5*((notchHeight/30.48)-.006)**1.508 ## Accounts for the flume part
#    else:
#        pass
#    return Q