# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 06:47:52 2015

@author: Alex
"""

#### Import FIELD NOTEBOOK Data
#from notebook import FieldNotes
def FieldNotes(sheet,headerrow,Book):
    print 'Opening field notes...'
    def my_parser(x,y):
        y = str(int(y))
        hour=y[:-2]
        minute=y[-2:]
        time=dt.time(int(hour),int(minute))
        parsed=dt.datetime.combine(x,time)
        #print parsed
        return parsed
    notebook_file = pd.ExcelFile(Book)
    notebook = notebook_file.parse(sheet,header=headerrow,parse_dates=[['Date','Time']],date_parser=my_parser,index_col=['Date_Time'])
    return notebook


### Check tipping bucket at RG1 (Timu1) against non-recording (World's Best)
fieldbookdata = datadir+'FieldNotebook-dataonly.xlsx'
Timu1fieldnotes = FieldNotes('Timu-F1notes',3,fieldbookdata)

Timu1mmcheck = Timu1fieldnotes.ix[:,'mm':'to 0.1'] ##take the records from the manual gage and if it was emptied to zero
Timu1mmcheck['mm true'] = Timu1mmcheck['mm']-Timu1mmcheck['to 0.1'].shift(1)

Timu1mmcheck['end']=Timu1mmcheck.index## add a column for time
Timu1mmcheck['start']=Timu1mmcheck['end'].shift(1) ## take the time and shift it down so you have a start and stop time: When the gauge was emptied to zero, it was the start of the next interval
Timu1mmcheck=Timu1mmcheck.truncate(before = Timu1mmcheck.index[5])

Timu1mmcheck['Timu1 mm sum']=StormSums(Timu1mmcheck,Precip['Timu1'])['sum'] ## from 1/20/12 onward. Timu1 QC data begins 1/21/12
Timu1mmcheck['WorldsBest - Timu1'] = Timu1mmcheck['Timu1 mm sum']-Timu1mmcheck['mm']



### Check PT against reference staff gage at LBJ
LBJfieldnotes = FieldNotes('LBJstage',1,fieldbookdata)
LBJfieldnotesStage = pd.DataFrame(LBJfieldnotes['RefGageHeight(cm)'].resample('5Min',how='first').dropna(),columns=['RefGageHeight(cm)'])
LBJfieldnotesStage =LBJfieldnotesStage.shift(0)
LBJfieldnotesStage['Uncorrected_stage']=PT1['Uncorrected_stage']
LBJfieldnotesStage['GH-Uncorrected_stage']=LBJfieldnotesStage['RefGageHeight(cm)']-LBJfieldnotesStage['Uncorrected_stage']
LBJfieldnotesStage['Corrected_stage']=PT1['stage']
LBJfieldnotesStage['GH-Corrected_stage']=LBJfieldnotesStage['RefGageHeight(cm)']-LBJfieldnotesStage['Corrected_stage']

PT1['GH Correction']=LBJfieldnotesStage['GH-Uncorrected_stage']
PT1['GH Correction Int']= PT1['GH Correction'].interpolate()
PT1['stage_corrected_RefGage'] = PT1['Uncorrected_stage']+PT1['GH Correction Int']

def compare_PT_Ref():
    fig, (uncorr, corr) = plt.subplots(2,1,sharex=True,sharey=True)
    LBJfieldnotesStage['GH-Uncorrected_stage'].plot(ax=uncorr,ls='None',marker='.',c='r',label='All Gage Height Readings (uncorrected)')
    LBJfieldnotesStage['GH-Uncorrected_stage'][LBJfieldnotesStage['Uncorrected_stage']<LBJ_storm_threshold].plot(ax=uncorr,ls='None',marker='.',c='b',label='Baseflow Gage Height Readings (uncorrected)')
    uncorr.legend(loc='best'), uncorr.set_title('Uncorrected PT stage')
    LBJfieldnotesStage['GH-Corrected_stage'].plot(ax=corr, ls='None',marker='.',c='r',label='All Gage Height Readings (corrected)')
    LBJfieldnotesStage['GH-Corrected_stage'][LBJfieldnotesStage['Corrected_stage']<LBJ_storm_threshold].plot(ax=corr,ls='None',marker='.',c='b',label='Baseflow Gage Height Readings (corrected)')
    corr.legend(loc='best'), corr.set_title('Corrected PT stage')
    return