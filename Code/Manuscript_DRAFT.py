# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 10:50:00 2015

@author: Alex
"""
plt.ioff()
from docx import *
from docx.shared import Inches
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
##  Create Document
document = Document()

######## SOME TOOLS
def add_figure_caption(fig_num=str(len(document.inline_shapes)),caption=''):
    cap = document.add_paragraph("Figure "+fig_num+". "+caption)
    cap.paragraph_style = 'caption'
    return
    
def dataframe_to_table(df=pd.DataFrame(),table_num=str(len(document.tables)+1),caption=''):
    table = document.add_table(rows=1, cols=len(df.columns)) 
    ## Merge all cells in top row and add caption text
    table_caption = table.rows[0].cells[0].merge(table.rows[0].cells[len(df.columns)-1])
    table_caption.text = "Table "+table_num+". "+caption
    ## Add  header
    header_row = table.add_row().cells
    col_count =0 ## counter  to iterate over columns
    for col in  header_row:
        col.text = df.columns[col_count] #df.columns[0] is the index
        col_count+=1
    ## Add data by  iterating over the DataFrame rows, then using a dictionary of DataFrame column labels to extract data
    col_labels = dict(zip(range(len(df.columns)),df.columns.tolist())) ## create dictionary where '1  to  n' is key for DataFrame columns
    for row in df.iterrows():  ## iterate over  rows in  DataFrame
        #print row[1]
        row_cells = table.add_row().cells ## Add a row to the  table
        col_count  = 0
        for cell in row_cells: ## iterate over the columns in the row
            #print row[1][str(col_labels[col_count])]
            cell.text = str(row[1][str(col_labels[col_count])]) ## and plug in data using a dictionary to  get column labels for DataFrame
            col_count+=1
    ## Format Table Style  
    table.style = 'TableGrid'   
    table.autofit
    table.num = str(len(document.tables)+1)
    return table
###################################################################################################################################################################    



#### TABLES ########################################################################################################################################################
### Landcover_Table
table_count=0
def tab_count():
    global table_count
    table_count+=1
    return str(table_count)
# Prepare LULC Data
landcover_table = LandCover_table()
landcover_table.table_num = str(tab_count())

### Storm Water Discharge Table
Q_Diff_table = Q_storm_diff_table() ## function to create table data
Q_Diff_table.table_num = str(tab_count())

### Storm Sediment Discharge Table
## Prepare table data
S_Diff_table = S_storm_diff_table() ## function to create table data
S_Diff_table.table_num = str(tab_count())

### Storm Q and SSY summary table
Q_S_Diff_summary_table = Q_S_storm_diff_summary_table()
Q_S_Diff_summary_table.table_num = str(tab_count())

### Pearson r coefficient table
Pearson_table = Pearson_r_Table()
Pearson_table.table_num = str(tab_count())

### Pearson r coefficient table
Spearman_table = Spearman_r_Table()
Spearman_table.table_num = str(tab_count())

#### FIGURES ########################################################################################################################################################
figure_count=0
def fig_count():
    global figure_count
    figure_count+=1
    return str(figure_count)
### INTRODUCTION
## Study Area Map
Study_Area_map = {'filename':maindir+'Figures/Maps/FagaaluInstruments land only map.tif', 'fig_num':str(fig_count())}
## Quarry_picture
Quarry_picture = {'filename':maindir+'Figures/Maps/Quarry before and after.tif','fig_num':str(fig_count())}

### RESULTS
### Stage-Discharge Rating Curves
## LBJ_StageDischarge
LBJ_StageDischarge = {'filename':figdir+"Q/Water Discharge Ratings for VILLAGE (LBJ)",'fig_num':str(fig_count())}
plotQratingLBJ(show=False,log=False,save=True,filename=LBJ_StageDischarge['filename'])
## DAM_StageDischarge
DAM_StageDischarge = {'filename':figdir+"Q/Water Discharge Ratings for FOREST (DAM)",'fig_num':str(fig_count())}
plotQratingDAM(show=False,log=False,save=True,filename=DAM_StageDischarge['filename'])

### SSC
## SSC Boxplots
SSC_Boxplots = {'filename':figdir+'SSC/Grab sample boxplots','fig_num':str(fig_count())}
plotSSCboxplots(storm_samples_only=True,withR2=False,show=False,save=True,filename=SSC_Boxplots['filename'])
## Discharge vs Sediment Concentration
Discharge_Concentration = {'filename':figdir+'SSC/Water discharge vs Sediment concentration','fig_num':str(fig_count())}
plotQvsC(storm_samples_only=False,ms=6,show=False,log=False,save=True,filename=Discharge_Concentration['filename'])

### T-SSC Rating Curves
## Synthetic Rating Curves
Synthetic_Rating_Curve = {'filename':figdir+'T/Synthetic Rating Curves','fig_num':str(fig_count())} ## define file name to find the png file from other script
Synthetic_Rating_Curves(param='SS_Mean',show=False,save=True,filename=Synthetic_Rating_Curve['filename'])## generate figure from separate script and save to file
## LBJ and DAM YSI T-SSC rating curves
LBJ_and_DAM_YSI_Rating_Curve = {'filename':figdir+'T/T-SSC rating LBJ and DAM YSI','fig_num':str(fig_count())}
plotYSI_compare_ratings(DAM_YSI,DAM_SRC,LBJ_YSI,Use_All_SSC=False,show=False,save=True,filename=LBJ_and_DAM_YSI_Rating_Curve['filename'])
## LBJ OBSa T-SSC rating curve
LBJ_OBSa_Rating_Curve = {'filename':figdir+'T/T-SSC rating LJB OBSa','fig_num':str(fig_count())}
OBSa_compare_ratings(df=LBJ_OBSa,df_SRC=LBJ_SRC,SSC_loc='LBJ',Use_All_SSC=False,show=False,save=True,filename=LBJ_OBSa_Rating_Curve['filename'])  
## LBJ OBSa T-SSC rating curve
LBJ_OBSb_Rating_Curve = {'filename':figdir+'T/T-SSC rating LJB OBSb','fig_num':str(fig_count())}
OBSb_compare_ratings(df=LBJ_OBSb,df_SRC=LBJ_SRC,SSC_loc='LBJ',Use_All_SSC=False,show=False,save=True,filename=LBJ_OBSb_Rating_Curve['filename'])  

## Storms
Example_Storm = {'filename':figdir+'storm_figures/Example_Storm','fig_num':str(fig_count())}
plot_storm_individually(LBJ_storm_threshold,LBJ_StormIntervals.loc[63],show=False,save=True,filename=Example_Storm['filename']) 

## SSY models
SSY_models_ALL = {'filename':figdir+'SSY/SSY Models ALL','fig_num':str(fig_count())}
plotALLStorms_ALLRatings(subset='pre',norm=True,log=True,show=False,save=True,filename=SSY_models_ALL['filename'])

#################################################################################################################################################################
#### TITLE
title_title = document.add_heading('TITLE:',level=1)
title_title.paragraph_format.space_before = 0
title = document.add_heading('Contributions of human activities to suspended sediment yield during storm events from a steep, small, tropical watershed',level=1)
title.paragraph_format.space_before = 0
#### ABSTRACT
abstract_title = document.add_heading('ABSTRACT',level=2)
abstract_title.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
abstract = document.add_paragraph('Abstract text goes here....')
### Read in Body Text
Body_Text = Document(maindir+'/Manuscript/Body_Text.docx')
section_count = 0
Section = {'Introduction':[],'Study Area':[],'Methods':[],'Results':[],'Discussion':[],'Conclusion':[]}
for paragraph in Body_Text.paragraphs:
    if len(paragraph.text)==0:
        section_count+=1
    if section_count == 1:
        Section['Introduction'].append(paragraph)
    if section_count == 2:
        Section['Study Area'].append(paragraph)   
    if section_count == 3:
        Section['Methods'].append(paragraph)
    if section_count == 4:
        Section['Results'].append(paragraph)        
    if section_count == 5:
        Section['Discussion'].append(paragraph)        
    if section_count == 6:
        Section['Conclusion'].append(paragraph)    
#### INTRODUCTION
introduction_title = document.add_heading('Introduction',level=2)
for paragraph in Section['Introduction'][1:]:
    p = document.add_paragraph(paragraph.text)
    p.style='BodyText'
    p.paragraph_format.left_indent = 0
    p.paragraph_format.first_line_indent = Inches(.4)

#### STUDY AREA
study_area_title = document.add_heading('Study Area',level=2)
study_area = document.add_paragraph('Study Area text goes here....referring to Figure'+Study_Area_map['fig_num'])
## Study Area map
if 'Study_Area_map' in locals():
    document.add_picture(Study_Area_map['filename'],width=Inches(6))
    add_figure_caption(Study_Area_map['fig_num'],"Faga'alu watershed showing upper (undisturbed) and lower (human-disturbed) subwatersheds.")
# Climate
document.add_heading('Climate',level=3)
# Land Use
document.add_heading('Land Use',level=3)
document.add_paragraph('Land use text goes here...referring to Table '+landcover_table.table_num)
## Land Use/Land cover Table
if 'landcover_table' in locals():
    dataframe_to_table(df=landcover_table,table_num=landcover_table.table_num,caption="Land use categories in Fag'alu and Nu'uuli watersheds CITATION")

## Quarry description
quarry_text = document.add_paragraph('Quarry description text goes here...Picture is of the quarry (Figure '+Quarry_picture['fig_num']+').')
## Quarry picture
if 'Quarry_picture' in locals():
    document.add_picture(Quarry_picture['filename'],width=Inches(6))
    add_figure_caption(Quarry_picture['fig_num'],"Photos of the open-pit aggregate quarry in Faga'alu in 2012 (Top) and 2014 (Bottom). Photo: Messina")

#### METHODS
methods_title = document.add_heading('Methods',level=2)
methods = document.add_paragraph('Methods text  goes here...')

#### RESULTS ####
results_title = document.add_heading('Results',level=2)
## Field data collection
document.add_heading('Field Data  Collection',level=3)

#### Precipitation
document.add_heading('Precipitation',level=4)
precipitation_text = document.add_paragraph('Precipitation text goes here...')

#### Water Discharge
document.add_heading('Water Discharge',level=4)
## LBJ stage-discharge rating
if 'LBJ_StageDischarge' in locals():
    document.add_picture(LBJ_StageDischarge['filename']+'.png',width=Inches(6))
    add_figure_caption(LBJ_StageDischarge['fig_num'],"Stage-Discharge relationships for stream gaging site at VILLAGE.")
## DAM stage-discharge rating
if 'DAM_StageDischarge' in locals():
    document.add_picture(DAM_StageDischarge['filename']+'.png',width=Inches(6))
    add_figure_caption(DAM_StageDischarge['fig_num'],"Stage-Discharge relationships for stream gaging site at FOREST.")
## Storm Water Discharge
if 'Q_Diff_table' in locals():
    dataframe_to_table(df=Q_Diff_table,table_num=Q_Diff_table.table_num,caption="Water discharge from subwatersheds in Faga'alu")

#### Suspended Sediment Concentration
document.add_heading('Suspended Sediment Concentration',level=4)
## SSC boxplots
if 'SSC_Boxplots' in locals():
    document.add_picture(SSC_Boxplots['filename']+'.png',width=Inches(6))
    add_figure_caption(SSC_Boxplots['fig_num'],"Boxplots of Suspended Sediment Concentration (SSC) from grab samples only (no Autosampler) at FOREST, QUARRY, and VILLAGE during storm periods.")
## Water Discharge vs Sediment Concentration
if 'Discharge_Concentration' in locals():
    document.add_picture(Discharge_Concentration['filename']+'.png',width=Inches(6))
    add_figure_caption(Discharge_Concentration['fig_num'],"Water Discharge vs Suspended Sediment concentration at FOREST, QUARRY, and VILLAGE during baseflow and stormflow periods.")


#### Turbidity
document.add_heading('Turbidity', level=4)

## Synthetic Rating Curves
if 'Synthetic_Rating_Curve' in locals():
    document.add_picture(Synthetic_Rating_Curve['filename']+'.png',width=Inches(6)) ## add pic from filename defined above
    add_figure_caption(Synthetic_Rating_Curve['fig_num'],"Synthetic Rating  Curves for Turbidimeters deployed at FOREST, QUARRY, VILLAGE, Nuuuli-1 and Nuuuli-2")

## LBJ and DAM YSI T-SSC rating curves
if 'LBJ_and_DAM_YSI_Rating_Curve' in locals():
    document.add_picture(LBJ_and_DAM_YSI_Rating_Curve['filename']+'.png',width=Inches(6))
    add_figure_caption(LBJ_and_DAM_YSI_Rating_Curve['fig_num'],"Turbidity-Suspended Sediment Concentration relationships for the YSI turbidimeter deployed at VILLAGE ("+str(LBJ_YSI.dropna().index[0])+"-"+str(LBJ_YSI.dropna().index[-1])+") and at FOREST ("+str(DAM_YSI.dropna().index[0])+"-"+str(DAM_YSI.dropna().index[-1])+").")

## LBJ OBSa T-SSC rating curve
if 'LBJ_OBSa_Rating_Curve' in locals():
    document.add_picture(LBJ_OBSa_Rating_Curve['filename']+'.png',width=Inches(6))
    add_figure_caption(LBJ_OBSa_Rating_Curve['fig_num'],"Turbidity-Suspended Sediment Concentration relationships for the OBS500 turbidimeter deployed at VILLAGE ("+str(LBJ_OBSa.dropna().index[0])+"-"+str(LBJ_OBSa.dropna().index[-1])+").")

## LBJ OBSb T-SSC rating curve
if 'LBJ_OBSb_Rating_Curve' in locals():
    document.add_picture(LBJ_OBSb_Rating_Curve['filename']+'.png',width=Inches(6))
    add_figure_caption(LBJ_OBSb_Rating_Curve['fig_num'],"Turbidity-Suspended Sediment Concentration relationships for the OBS500 turbidimeter deployed at VILLAGE ("+str(LBJ_OBSb.dropna().index[0])+"-"+str(LBJ_OBSb.dropna().index[-1])+").")



#### Storm Events
document.add_heading('Storm Events',level=3)
if 'Example_Storm' in locals():
    document.add_picture(Example_Storm['filename']+'.png',width=Inches(6))
    add_figure_caption(Example_Storm['fig_num'],"Example of storm event.")

#### Comparing SSY from disturbed and undisturbed subwatersheds
document.add_heading('Comparing SSY from disturbed and undisturbed subwatersheds',level=3)
## Storm Sediment Table
document.add_paragraph("Table "+S_Diff_table.table_num+" shows that lots of...")
if 'S_Diff_table' in locals():
    dataframe_to_table(df=S_Diff_table,table_num=S_Diff_table.table_num,caption="Sediment discharge from subwatersheds in Faga'alu")
    
#### Comparing human impact on SSY from Faga’alu watershed
document.add_heading("Comparing human impact on SSY from Faga'alu watershed",level=3)
if 'Q_S_Diff_summary_table' in locals():
    dataframe_to_table(df=Q_S_Diff_summary_table,table_num=Q_S_Diff_summary_table.table_num,caption="Total Q and SSY")

SSYspec_Forest = float(Q_S_Diff_summary_table.ix['SSY* Forest'][''][:4])
SSYspec_Village = float(Q_S_Diff_summary_table.ix['SSY* Village'][''][:4])
SSYspec_change = (SSYspec_Village/SSYspec_Forest)
document.add_paragraph("Humans have increased specific SSY ~"+"%.1f"%SSYspec_change+"x")    

#### Fitting SSY models
document.add_heading('Fitting sediment curves',level=3)
if 'SSY_models_ALL' in locals():
    document.add_picture(SSY_models_ALL['filename']+'.png',width=Inches(6))
    add_figure_caption(SSY_models_ALL['fig_num'],"SSY rating curves for predictors")

#### Comparing predictors of SSY
document.add_heading('Comparing predictors of SSY',level=3)
# Pearson's correlation coeffs
document.add_paragraph("Pearson's correlation coefficients...")
if 'Pearson_table' in locals():
    dataframe_to_table(df=Pearson_table,table_num=Pearson_table.table_num,caption="Pearson correlation coefficients")
# Spearman's correlation coeffs
document.add_paragraph("Spearman's correlation coefficients...")  
if 'Spearman_table' in locals():
    dataframe_to_table(df=Spearman_table,table_num=Spearman_table.table_num,caption="Spearman correlation coefficients")
    
#### DISCUSSION
discussion_title=document.add_heading('Discussion',level=2)
discussion_text = document.add_paragraph('Discussion text goes here...')


#### CONCLUSION
conclusion_title=document.add_heading('Conclusion',level=2)
conclusion_text = document.add_paragraph('Conclusion text goes here...')


## 


## Save Document
document.save(maindir+'Manuscript/DRAFT.docx')

## Clean up any open  figures
plt.close('all')








