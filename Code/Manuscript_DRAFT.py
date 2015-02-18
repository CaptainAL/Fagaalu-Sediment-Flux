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

def add_figure_caption(caption):
    cap = document.add_paragraph("Figure "+str(len(document.inline_shapes))+". "+caption)
    cap.paragraph_style = 'caption'
    return
    
def dataframe_to_table(df=pd.DataFrame(),caption=''):
    table = document.add_table(rows=1, cols=len(df.columns[1:])) #df.columns[0] is the index from reset_index()  method above
    ## Merge all cells in top row and add caption text
    table_caption = table.rows[0].cells[0].merge(table.rows[0].cells[len(df.columns[1:])-1])
    table_caption.text = caption
    ## Add  header
    header_row = table.add_row().cells
    col_count =0 ## counter  to iterate over columns
    for col in  header_row:
        col.text = df.columns[1:][col_count] #df.columns[0] is the index
        col_count+=1
    ## Add data by  iterating over the DataFrame rows, then using a dictionary of DataFrame column labels to extract data
    col_labels = dict(zip(range(len(landcover.columns[1:])),landcover.columns[1:].tolist())) ## create dictionary where '1  to  n' is key for DataFrame columns
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
    return table
###################################################################################################################################################################    
    
    
##  Create Document
document = Document()

#### TITLE
title_title = document.add_heading('TITLE:',level=1)
title_title.paragraph_format.space_before = 0
title = document.add_heading('Contributions of human activities to suspended sediment yield during storm events from a steep, small, tropical watershed',level=1)
title.paragraph_format.space_before = 0
#### ABSTRACT
abstract_title = document.add_heading('ABSTRACT',level=2)
abstract_title.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
abstract = document.add_paragraph('Abstract text goes here....')
#### INTRODUCTION
introduction_title = document.add_heading('Introduction',level=2)
introduction = document.add_paragraph('Introduction text goes here....')
introduction.first_line_indent = Inches(-0.4)
#### STUDY AREA
study_area_title = document.add_heading('Study Area',level=2)
study_area = document.add_paragraph('Study Area text goes here....')
document.add_picture(maindir+'Figures/Maps/FagaaluInstruments land only map.tif',width=Inches(6))
add_figure_caption("Faga'alu and Nu'uuli watersheds showing upper (undisturbed) and lower (human-disturbed) subwatersheds.")

## Land Use/Land cover Table
## Prepare LULC Data
landcoverXL = pd.ExcelFile(datadir+'/LandCover/Watershed_Stats.xlsx')
landcover = landcoverXL.parse('Fagaalu')
landcover = landcover[['Subwatershed','Cumulative Area km2','%','% High Intensity Developed','% Developed Open Space',
                       '% Grassland (agriculture)','% Forest','% Scrub/ Shrub','% Bare Land']]
## Format Table data                       
for column in landcover.columns:
    try:
        if column.startswith('%')==True:
            landcover[column] = landcover[column]*100.
            landcover[column] = landcover[column].round(1)
        else:
            landcover[column] = landcover[column].round(2)
    except:
        pass
landcover = landcover[landcover['Subwatershed'].isin(['FOREST(UPPER)','QUARRY','VILLAGE(TOTAL)','Fagaalu Stream'])==True].reset_index()
## Create table and Caption
dataframe_to_table(df=landcover,caption="Table "+str(len(document.tables)+1)+". Land use categories in Fag'alu and Nu'uuli watersheds CITATION")

## Quarry description
quarry_text = document.add_paragraph('Quarry description text goes here...')
## Quarry figure
document.add_picture(maindir+'Figures/Maps/Quarry before and after.tif',width=Inches(6))
add_figure_caption("Photos of the open-pit aggregate quarry in Faga'alu in 2012 (Top) and 2014 (Bottom). Photo: Messina")

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
fig_filename = figdir+"Q/Water Discharge Ratings for VILLAGE (LBJ)"
plotQratingLBJ(show=False,log=False,save=True,filename=fig_filename)
document.add_picture(fig_filename+'.png',width=Inches(6))
add_figure_caption("Stage-Discharge relationships for stream gaging site at VILLAGE.")
## DAM stage-discharge rating
fig_filename = figdir+"Q/Water Discharge Ratings for FOREST (DAM)"
plotQratingDAM(show=False,log=False,save=True,filename=fig_filename)
document.add_picture(fig_filename+'.png',width=Inches(6))
add_figure_caption("Stage-Discharge relationships for stream gaging site at FOREST.")

#### Suspended Sediment Concentration
document.add_heading('Suspended Sediment Concentration',level=4)
## SSC boxplots
fig_filename = figdir+'SSC/Grab sample boxplots'
plotSSCboxplots(storm_samples_only=True,withR2=False,show=False,save=True,filename=fig_filename)
document.add_picture(fig_filename+'.png',width=Inches(6))
add_figure_caption("Boxplots of Suspended Sediment Concentration (SSC) at FOREST, QUARRY, and VILLAGE during storm periods.")
## Water Discharve vs Sediment Concentration
fig_filename = figdir+'SSC/Water discharge vs Sediment concentration'
plotQvsC(include_nonstorm_samples=True,ms=6,show=False,log=False,save=True,filename=fig_filename)
document.add_picture(fig_filename+'.png',width=Inches(6))
add_figure_caption("Water Discharge vs Suspended Sediment concentration at FOREST, QUARRY, and VILLAGE during baseflow and stormflow.")

#### Turbidity
document.add_heading('Turbidity', level=4)

## LBJ and DAM YSI T-SSC rating curves
fig_filename = figdir+'T/T-SSC rating LBJ and DAM YSI'
plotYSI_compare_ratings(DAM_YSI,DAM_SRC,LBJ_YSI,Use_All_SSC=False,show=False,save=True,filename=fig_filename)
document.add_picture(fig_filename+'.png',width=Inches(6))
add_figure_caption("Turbidity-Suspended Sediment Concentration relationships for the YSI turbidimeter deployed at VILLAGE ("+str(LBJ_YSI.dropna().index[0])+"-"+str(LBJ_YSI.dropna().index[-1])+") and at FOREST ("+str(DAM_YSI.dropna().index[0])+"-"+str(DAM_YSI.dropna().index[-1])+").")

## LBJ OBSa T-SSC rating curve
fig_filename = figdir+'T/T-SSC rating LJB OBSa'
OBSa_compare_ratings(df=LBJ_OBSa,df_SRC=LBJ_SRC,SSC_loc='LBJ',Use_All_SSC=False,show=False,save=True,filename=fig_filename)  
document.add_picture(fig_filename+'.png',width=Inches(6))
add_figure_caption("Turbidity-Suspended Sediment Concentration relationships for the OBS500 turbidimeter deployed at VILLAGE ("+str(LBJ_OBSa.dropna().index[0])+"-"+str(LBJ_OBSa.dropna().index[-1])+").")

## LBJ OBSa T-SSC rating curve
fig_filename = figdir+'T/T-SSC rating LJB OBSb'
OBSb_compare_ratings(df=LBJ_OBSb,df_SRC=LBJ_SRC,SSC_loc='LBJ',Use_All_SSC=False,show=False,save=True,filename=fig_filename)  
document.add_picture(fig_filename+'.png',width=Inches(6))
add_figure_caption("Turbidity-Suspended Sediment Concentration relationships for the OBS500 turbidimeter deployed at VILLAGE ("+str(LBJ_OBSb.dropna().index[0])+"-"+str(LBJ_OBSb.dropna().index[-1])+").")

## Synthetic Rating Curves
fig_filename = figdir+'T/Synthetic Rating Curves' ## define file name to find the png file from other script
Synthetic_Rating_Curves(param='SS_Mean',show=False,save=True,filename=fig_filename)## generate figure from separate script and save to file
document.add_picture(fig_filename+'.png',width=Inches(6)) ## add pic from filename defined above
add_figure_caption("Synthetic Rating  Curves for Turbidimeters deployed at FOREST, QUARRY, VILLAGE, Nuuuli1 and Nuuuli2")

#### Storm Events
document.add_heading('Storm Events',level=3)

#### Comparing SSY from disturbed and undisturbed subwatersheds
document.add_heading('Comparing SSY from disturbed and undisturbed subwatersheds',level=3)

#### Disturbance Ratio 
document.add_heading('Disturbance Ratio', level=3)

#### Comparing predictors of SSY
document.add_heading('Comparing predictors of SSY',level=3)

#### Fitting sediment curves
document.add_heading('Fitting sediment curves',level=3)

#### Comparing human impact on SSY from Faga’alu watershed
document.add_heading("Comparing human impact on SSY from Faga'alu watershed",level=3)

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








