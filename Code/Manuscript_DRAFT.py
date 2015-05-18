# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 10:50:00 2015

@author: Alex
"""
plt.ioff()
plt.close('all')
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
    
def dataframe_to_table(df=pd.DataFrame(),table_num=str(len(document.tables)+1),caption='',fontsize=11):
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
    table.style.font.size = Pt(fontsize)
    table.autofit
    #table.num = str(len(document.tables)+1)
    return table
    
def add_equation(eq_table):
    t = document.add_table(rows=len(eq_table.rows),cols=len(eq_table.columns))
    t.rows[0].cells[1].text = eq_table.rows[0].cells[1].text
    t.rows[0].cells[2].text = eq_table.rows[0].cells[2].text   
    if len(eq_table.rows)>1:
        t.rows[1].cells[0].merge(t.rows[1].cells[2]).text = eq_table.rows[1].cells[0].text
    t.style = 'TableGrid'   
    t.autofit
    return t
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

### Storm Sediment Discharge Table
## Prepare table data
S_Diff_table, LOWER_percent_of_TOTAL_SSY, TOTAL_percent_of_TOTAL_SSY = S_storm_diff_table() ## function to create table data
S_Diff_table.table_num = str(tab_count())

S_Diff_table_quarry, QUARRY_percent_of_TOTAL_SSY, VILLAGE_percent_of_TOTAL_SSY, QUA_VIL_percent_of_TOTAL_SSY = S_storm_diff_table_quarry()
S_Diff_table_quarry.table_num = str(tab_count())

Annual_SSY_tables.table_num = str(tab_count())

### Storm Q and SSY summary table
Q_S_Diff_summary_table = Q_S_storm_diff_summary_table()
Q_S_Diff_summary_table.table_num = str(tab_count())

### Model statistics table
SSYEV_models_stats = ALLRatings_table()
SSYEV_models_stats.table_num = str(tab_count())

#### FIGURES ########################################################################################################################################################
figure_count=0
def fig_count():
    global figure_count
    figure_count+=1
    return str(figure_count)
## INTRODUCTION
#### Study Area Map
Study_Area_map = {'filename':maindir+'Figures/Maps/FagaaluInstruments land only map.tif', 'fig_num':str(fig_count())}
## Quarry_picture
Quarry_picture = {'filename':maindir+'Figures/Maps/Quarry before and after.tif','fig_num':str(fig_count())}

## METHODS
####  Stage-Discharge Rating Curves
## DAM_StageDischarge
DAM_StageDischarge = {'filename':figdir+"Q/Water Discharge Ratings for FG1 (DAM)",'fig_num':str(fig_count())}
plotQratingDAM(ms=8,show=False,log=False,save=True,filename=DAM_StageDischarge['filename'])

## LBJ_StageDischarge
LBJ_StageDischarge = {'filename':figdir+"Q/Water Discharge Ratings for FG3 (LBJ)",'fig_num':str(fig_count())}
plotQratingLBJ(ms=8,show=False,log=False,save=True,filename=LBJ_StageDischarge['filename'])

####  T-SSC Rating Curves
T_SSC_Rating_Curves = {'filename':figdir+'T/T-SSC rating curves','fig_num':str(fig_count())}
plot_all_T_SSC(Use_All_SSC=False,storm_samples_only=True,show=False,save=True,filename=T_SSC_Rating_Curves['filename'])

## RESULTS
## Discharge time series
Q_timeseries =  {'filename':figdir+"Q/Q time series 2012-2014",'fig_num':str(fig_count())}
QYears(log=False,show=False,save=True,filename=Q_timeseries['filename'])

#### Storms
Example_Storm = {'filename':figdir+'storm_figures/Example_Storm','fig_num':str(fig_count())}
plot_storm_individually(LBJ_storm_threshold,LBJ_StormIntervals.loc[63],show=False,save=True,filename=Example_Storm['filename']) 

####  SSC
## SSC Boxplots
SSC_Boxplots= {'filename':figdir+'SSC/Grab sample boxplots baseflow and stormflow','fig_num':str(fig_count())}
plotSSCboxplots(subset=['Pre-baseflow','Pre-storm'],withR2=False,log=True,show=False,save=True,filename=SSC_Boxplots['filename'])

## Discharge vs Sediment Concentration
Discharge_Concentration = {'filename':figdir+'SSC/Water discharge vs Sediment concentration','fig_num':str(fig_count())}
plotQvsC(subset='pre',storm_samples_only=False,ms=5,show=False,log=False,save=True,filename=Discharge_Concentration['filename'])

#### SSY models
SSY_models_ALL = {'filename':figdir+'SSY/SSY Models ALL pre-mitigation','fig_num':str(fig_count())}
ALLStorms_ALLRatings = plotALLStorms_ALLRatings(subset='pre',ms=4,norm=True,log=True,show=False,save=True,filename=SSY_models_ALL['filename'])

###### EQUATIONS ############################################################################################################################################
equation_count=0
def eq_count():
    global equation_count
    equation_count+=1
    return str(equation_count)
    
Equations = Document(maindir+'/Manuscript/Equations.docx').tables
## SSYev = Q*SSC 
SSYEV_eq = Equations[0].table
SSYEV_eq.eq_num = eq_count()
## DR = SSY/SSYPRE
DR_eq = Equations[1].table
DR_eq.eq_num = eq_count()
## predict_SSYev = aXb
predict_SSYEV_eq = Equations[2].table
predict_SSYEV_eq.eq_num = eq_count()
## PE = sqrt(sum(Error^2+Error^2))
PE_eq = Equations[3].table
PE_eq.eq_num = eq_count()
############################################################################################################################################
#### Appendix
table_count,figure_count,equation_count=0, 0, 0
### Storm Water Discharge Table
Q_Diff_table = Q_storm_diff_table() ## function to create table data
Q_Diff_table.table_num =str(tab_count())

## Cross-Sections
#LBJ
LBJ_Cross_Section = {'filename':figdir+'Q/LBJ_Cross_Section','fig_num':str(fig_count())}
Mannings(datadir+'Q/Cross_Section_Surveys/LBJ_cross_section.xlsx','LBJ_m',Slope=0.016,Manning_n='Jarrett',k=.06/.08,stage_start=1.4,show=False,save=True,filename=LBJ_Cross_Section['filename'])
#DAM
DAM_Cross_Section = {'filename':figdir+'Q/DAM_Cross_Section','fig_num':str(fig_count())}
Mannings(datadir+'Q/Cross_Section_Surveys/DAM_cross_section.xlsx','DAM_m',Slope=0.016,Manning_n='Jarrett',k=.04/.07,stage_start=.46,show=False,save=True,filename=DAM_Cross_Section['filename'])

## Synthetic Rating Curves
Synthetic_Rating_Curve = {'filename':figdir+'T/Synthetic Rating Curves Fagaalu','fig_num':str(fig_count())} ## define file name to find the png file from other script
Synthetic_Rating_Curves_Fagaalu(param='SS_Mean',show=False,save=True,filename=Synthetic_Rating_Curve['filename'])## generate figure from separate script and save to file


############################################################################################################################################
#### TITLE
title_title = document.add_heading('TITLE:',level=1)
title_title.paragraph_format.space_before = 0
title = document.add_heading('Contributions of human activities to suspended sediment yield during storm events from a steep, small, tropical watershed',level=1)
title.paragraph_format.space_before = 0
## subscript/superscript words
document.add_paragraph("SSYEV, m3, km2, SSYUPPER, SSYLOWER, SSYTOTAL, SSYPRE, alpha, Beta, plus-minus, a, b")

## AUTHORS
document.add_heading('Authors:',level=3)
document.add_paragraph("Messina, A.M.a*, Biggs, T.W.a")
document.add_paragraph("a San Diego State University, Department of Geography, San Diego, CA 92182, amessina@rohan.sdsu.edu, +1-619-594-5437, tbiggs@mail.sdsu.edu, +1-619-594-0902")

#### ABSTRACT
abstract_title = document.add_heading('ABSTRACT',level=2)
abstract_title.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
abstract = document.add_paragraph("Anthropogenic watershed disturbance by agriculture, deforestation, roads, and urbanization can alter the timing, composition, and mass of sediment loads to adjacent coral reefs, causing enhanced sediment stress on corals near the outlets of impacted watersheds like Faga'alu, American Samoa. To quantify the increase in sediment loading to the adjacent priority coral reef experiencing sedimentation stress, suspended-sediment yield (SSY) from undisturbed and human-disturbed portions of a small, steep, tropical watershed was measured during baseflow and storm events of varying magnitude. Data on precipitation, discharge, turbidity, and suspended-sediment concentration (SSC) were collected over three field campaigns and continuous monitoring from January 2012 to March 2014, which included 88 storm events. A combination of paired- and nested-watershed study designs using sediment budget, disturbance ratio, and sediment rating curve methodologies was used to quantify the contribution of human-disturbed areas to total SSY. SSC during base- and stormflows was significantly higher downstream of an open-pit aggregate quarry, indicating the quarry is a key sediment source requiring sediment discharge mitigation. Comparison of event-wise SSY from the upper, undisturbed watershed, and the lower, human-disturbed watershed showed the Lower watershed accounted for more than 80% of total SSY on average, and human activities have increased total sediment loading to the coast by approximately 200%. Four storm characteristics were tested as predictors of event SSY using Pearson's and Spearman's correlation coefficients. Similar to mountainous watersheds in semi-arid and temperate watersheds, SSY from both the undisturbed and disturbed watersheds had the highest correlation with event maximum discharge, Qmax (Pearson's R=0.88 and 0.86 respectively), and were best fit by a power law relationship. The resulting model of event-SSY from Faga'alu is being incorporated as part of a larger project investigating relationships and interactions between terrigenous sediment, water circulation over the reef, and the spatial distribution of sediment accumulation under various conditions in a linked watershed and fringing-reef embayment.")

#### KEYWORDS
document.add_heading('Keywords:',level=3)
document.add_paragraph("Sediment yield, Mountainous catchments, Land use, Storm events, coastal sediment deposition, American Samoa")

#### INTRODUCTION
introduction_title = document.add_heading('Introduction',level=2)

## What's the problem? Where is the problem? How is it being addressed?
document.add_paragraph("Human activities including deforestation, agriculture, roads, mining, and urbanization alter the timing, composition, and amount of sediment loads to downstream ecosystems, such as coral reefs. Increased sediment loads can stress corals near the outlets of impacted watersheds by decreasing light for photosynthesis and increasing sediment accuulation rates (Syvitski et al., 2005; West and van Woesik, 2001; Fabricius et al. 2005). Anthropogenic sediment disturbance can be particularly high in the humid tropics, which are characterized by high rainfall, extreme weather events, steep slopes, erodible soils, and naturally dense vegetation, where land clearing alters the fraction of exposed soil more than in sparsely-vegetated regions. Such environments characterize many volcanic islands in the south Pacific, which also contain many coral reefs impacted by sediment. ")

terms ="     =  3   )    "

# More on sediment budgets and their role in solving sed mgmt problems (Reid and Dunne, others on sed budgets)
document.add_paragraph("A sediment budget quantifies sediment as it moves from key sources to its eventual exit from a watershed (Rapp 1960), and is a useful means of characterizing watershed response to land use change and management interventions (Walling, 1995). Researchers and land managers are interested in linking land use changes and mitigation strategies to changes in sediment yields at the watershed outlet and subsequent coral health impacts. Walling (1999) has used the concept of the sediment budget to show that sediment yield from watersheds can be insensitive to both land use change and erosion management due to high sediment storage capacity on hillslopes and in the channel. Sediment yield from disturbed areas can be large but may not be important compared to naturally high yields from undisturbed areas. Walling (2008) argues sediment control strategies should be based on a a holistic understanding of the sediment dynamics of the particular watershed. While a full description of all sediment production and transport processes are of scientific interest,the sediment budget needs to be simplified to be used as a management tool (Slaymaker 2003). Most management applications require only that the order of magnitude or the relative importance of process rates be known, so Reid and Dunne (1996) argue a management-focused sediment budget can be developed quickly in situations where the management problem is clearly defined and the management area can be divided into homogenous sub-units.")


# Insert a topic sentence here (this is too detailed for a first sentence….
document.add_paragraph("Several studies have found that a large proportion of the watershed's sediment yield can originate from relatively small, disturbed areas. In the Pacific Northwest, several studies found most road-generated sediment can originate from a relatively small fraction of the road network (Wemple et al., 1996; Henderson and Toews, 2001; Megahan et al., 2001), and heavily used roads could generate 130 times as much sediment as abandoned roads (Reid and Dunne 1984). Similarly, in a disturbed watershed on Molokai, Stock et al. (2010) found that less than 5% of the land produces most of the sediment, and only 1% produces approx. 50% of the sediment (Risk, 2014), suggesting that management should focus on identifying, quantifying, and mediating erosion hotspots.") 


document.add_paragraph("Knowledge of fluvial suspended sediment yield (SSY) on most Pacific volcanic islands remains limited due to the challenges of in situ monitoring, and existing sediment yield models are not well-calibrated to the climatic, topographic, and geologic conditions found on steep, tropical islands (Calhoun and Fletcher, 1999). Developing models that predict SSY from small, mountainous catchments is a significant contribution for establishing baselines for change-detection, and can also further improve models applied at the regional scale (Duvert et al., 2012).") 

document.add_paragraph("Traditional approaches to quantifying human impact on sediment yield, including comparison of total annual yields (Fahey et al., 2003) and sediment rating curves (Asselman, 2000; Walling, 1977), are complicated by interannual variability and hysteresis in the discharge-concentration relationship. As an alternative, other studies (Basher et al., 2011; Duvert et al., 2012) have compared total SSY generated by storm events of the same magnitude to detect human impacts and develop empirical models. SSY generated by individual storm events (SSYEV) may correlate with various precipitation and discharge variables ("+'"storm metrics"'+"), such as total precipitation, the Erosivity Index, total discharge, or maximum event discharge, but the best correlation has consistently been found with maximum event discharge. Several researchers have hypothesized that the maximum event discharge integrates the whole hydrological response of a watershed, making it a good predictor variable of SSYEV in diverse environments (Duvert et al., 2012; Rankl, 2004). High correlation between SSYEV and maximum event discharge has been found in semi-arid, temperate, and sub-humid watersheds in Wyoming (Rankl, 2004), Mexico, Italy, France (Duvert et al., 2012), and New Zealand (Basher et al., 2011; Hicks, 1990), but this approach has not been attempted for steep, tropical watersheds on volcanic islands.")

document.add_paragraph("The anthropogenic impact on SSY may vary by storm magnitude, as documented in Pacific Northwest forests (Lewis et al., 2001). As storm magnitude increases, water yield and/or SSY from natural areas may increase relative to human-disturbed areas, diminishing anthropogenic impact relative to the natural baseline. While large storms account for most SSY in natural conditions, human-disturbed areas may show the most significant disturbance for smaller storms (Lewis et al., 2001). It is hypothesized that the disturbance ratio (DR) is highest for small storms, when background SSY from the undisturbed forest is low and erodible sediment from disturbed surfaces is the dominant source. For large storms, it is hypothesized mass movements and bank erosion contribute to naturally high SSY from the undisturbed watershed, reducing the DR for large events.") 

document.add_paragraph("This study uses in situ measurements of precipitation, stream discharge, turbidity (T) and suspended sediment concentration (SSC) to 1) quantify sediment yield from key areas of a human-disturbed watershed in the south Pacific and 2) to develop an empirical model of storm-generated sediment yield to a priority coral reef. Turbidity is used to estimate continuous suspended sediment concentration by developing a turbidity-suspended sediment concentration relationship (T-SSC). The T-SSC relationship is unique to each region, or even each stream, and can be influenced by water color, dissolved solids and organic matter, temperature, and the shape, size, and composition of sediment particles. T has proved to be a robust surrogate measure of SSC in streams (Gippel 1995) and is widely used for monitoring remote watersheds where sediment yield is dominated by flashy storm events and monitoring resources are limited (Lewis 1996). The questions addressed include: How much has human disturbance increased sediment yield to the coast?  What human activities dominate the anthropogenic contribution to the sediment budget?  How do sediment contributions from human-disturbed areas and undisturbed areas vary with storm size? Which storm metric is the best predictor of storm event suspended sediment yield (SSYEV): total precipitation, Erosivity Index, total discharge, or maximum event discharge? ")

#### STUDY AREA
study_area_title = document.add_heading('Study Area',level=2)
document.add_paragraph("The study watershed, Faga'alu, drains an area of 1.86km2 on Tutuila (14S, 170W), the largest island in the Territory of American Samoa (140 km2). Most of Tutuila is composed of steep, heavily forested mountains.  The mean slope of Faga'alu watershed is 0.53 m/m and total relief is 653m. Faga'alu Stream discharges to an adjacent reef that Aeby et al. (2006) identified as being highly degraded by sediment. Faga'alu watershed was identified by local environmental management agencies in the Land-Based Sources of Pollution working group of the American Samoa Coral Reef Advisory Group (CRAG) as a heavily impacted watershed, and in 2012 was selected by the US Coral Reef Task Force (USCRTF) as a Priority Watershed for conservation and remediation efforts.")

## Study Area map
if 'Study_Area_map' in locals():
    document.add_picture(Study_Area_map['filename'],width=Inches(6))
    add_figure_caption(Study_Area_map['fig_num'],"Faga'alu watershed showing the Uupper (undisturbed) and Lower (human-disturbed) subwatersheds.")
    
# Climate
document.add_heading('Climate',level=3)
document.add_paragraph("Precipitation is caused by several mechanisms including cyclones and tropical depressions, isolated thunderstorms, and orographic uplifting of trade-wind squalls over the high (300-600 m), mountainous ridge that runs the length of the island. Unlike many other Pacific Islands, the mountainous ridge runs parallel to the predominant wind direction, and does not cause a significant windward/leeward rainfall gradient. Average annual specific discharge (m3 yr-1 km-2) shows little spatial variation across the island, irrespective of location or orientation (Dames & Moore, 1981). Precipitation varies orographically from an average 2,380 mm/yr at the shoreline to 6,350 mm/yr at high elevation, averaging 3,800 mm/yr over the island from 1903 to 1973 (Eyre, 1994; Izuka, 2005). In Faga'alu watershed, rainfall records show average annual precipitation is 6,350 mm at Matafao Mtn. (653m m.a.s.l), 5,280mm at Matafao Reservoir (249 m m.a.s.l.) and about 3,800mm on the coastal plain (Craig, 2009; Dames & Moore, 1981; Tonkin & Taylor International Ltd., 1989; Wong, 1996, Perrault, 2010). Potential evapotranspiration follows the opposite trend, with annual mean PET varying from 890mm at high elevation to 1,150 mm at sea level (Izuka, 2005). Tropical cyclones are erratic but occurred on average every 1-13 years from 1981-2014 (Craig, 2009) and bring intense rainfall, flooding, landslides, and high sediment yield events (Buchanan-Banks, 1979).")

document.add_paragraph("There are two subtle rainfall seasons: a drier winter season, from June through September and a wetter summer season, from October through May (Izuka, 2005). During the drier winter season, the island is influenced by the southeast Trades and relatively stronger, predominantly East to Southeast winds, lower temperatures, lower humidity and lower total rainfall. During the wetter summer season the Inter-Tropical Convergence Zone (ITCZ) moves over the island, causing light to moderate Northerly winds, higher temperatures, higher humidity, and higher total rainfall. While total rainfall is lower in the drier Tradewind season, large rainfall events are still observed. Analysis of mean monthly rainfall data from USGS rain gauges and  Parameter-elevation Relationships on Independent Slopes Model (PRISM) Climate Group (Daly et al., 2006) for the period 1971-2000 showed 75% of precipitation occurred in the wet seaons, October-May, and 25% occurred in the dry season, June-September (Perrault, 2010). Analysis of 212 peak discharges at 11 continuous-record gaging sites up to 1990 showed 65% of annual peak flows occurred during the wet season and 35% of peak flows occurred during the drier Tradewind season (Wong, 1996).")
# Land Use
document.add_heading('Land Use',level=3)
document.add_paragraph("Faga'alu watershed can be divided into two subwatersheds: 1) an upper subwatershed characterized by large areas of undisturbed, steeply-sloping, heavily forested hillsides (UPPER), and 2) a lower subwatershed wtih similarly steep forested topography and relatively small flat areas that are urbanized or densely settled (LOWER) (Figure "+Study_Area_map['fig_num']+"). This settlement pattern is typical for volcanic islands with steep topography in the South Pacific. Land use in the village includes agriculture, roads, and urbanization (Table 1). Faga'alu watershed includes two unique anthropogenic features not found in "+'"typical"'+" watersheds in American Samoa: 1) an open aggregate quarry, upstream of FG2 in Figure "+Study_Area_map['fig_num']+"), and 2) a large impervious area associated with a hospital, adjacent FG3 in Figure "+Study_Area_map['fig_num']+". To separate these key features, the LOWER subwatershed can be further divided into a LOWER_QUARRY subwatershed, draining areas between FG1 and FG2, and a LOWER_VILLAGE subwatershed, draining areas between FG2 and FG3. Three water impoundment structures were built in the UPPER subwatershed for drinking water supply and hydropower but only the highest, Matafao Reservoir, was ever connected to the municipal water system and has since fallen out of use (Tonkin & Taylor International Ltd., 1989)(Figure "+Study_Area_map['fig_num']+"). The dams have accumulated a significant amount of sediment and we assume they are not currently retaining fine suspended sediment. A full description of stream impoundments is in the Appendix.")

## Land Use/Land cover Table
if 'landcover_table' in locals():
    dataframe_to_table(df=landcover_table,table_num=landcover_table.table_num,caption="Land use categories in Faga'alu subwatersheds (NOAA Ocean Service and Coastal Services Center, 2010)",fontsize=9)
document.add_paragraph("")
document.add_paragraph("The predominant land cover is undisturbed forest on the steep hillsides ("+"%.1f"%landcover_table.ix[5]['% Forest']+"%). Natural landsliding in undisturbed forest can contribute large amounts of sediment during storm events (Buchanan-Banks, 1979; Calhoun and Fletcher, 1999). Compared to other watersheds on Tutuila, a relatively large portion of Faga'alu watershed is urbanized ("+"%.1f"%landcover_table.ix[5]['% High Intensity Developed']+"% "+'"High Intensity Developed"'+" in Table "+landcover_table.table_num+"), due to large areas of impervious surface associated with the hospital and the numerous residences and businesses. A small portion of the watershed ("+"%.1f"%landcover_table.ix[5]['% Developed Open Space']+"%) is developed open space, which includes landscaped lawns and parks. In addition to some small, household gardens there are several small agricultural areas growing banana and taro on the steep hillsides. A land cover map (2.5m resolution) classified the agricultural plots as "+'"Grassland"'+" due to the high fractional grass cover in the plots (Table "+landcover_table.table_num+") (NOAA Ocean Service and Coastal Services Center, 2010). These plots are currently receiving technical assistance from the Natural Resource Conservation Service (NRCS) to mitigate erosion.")

## Quarry description
document.add_paragraph("An open-pit aggregate quarry, covering 1.6ha ("+"%.1f"%landcover_table.ix[1]['% Bare Land']+"% of LOWER_QUARRY subwatershed) accounts for the majority of the "+"%.1f"%landcover_table.ix[5]['% Bare Land']+"% of Faga'alu watershed classified as Bare Land (Table "+landcover_table.table_num+"). The quarry has been in continuous operation since the 1960's by advancing into the steep hillside to quarry the underlying basalt formation (Latinis 1996). The overburden soil and weathered rock was either piled up on-site where it was eroded by storms, or was manually rinsed from crushed aggregate. With few sediment runoff controls in place, the sediment was discharged directly to the stream. In 2011 the quarry operators installed some sediment runoff management practices such as silt fences and settling ponds (Horsley-Witten, 2011) but they were unmaintained and inadequate to control the large amount of sediment mobilized during storm events (Horsley-Witten, 2012a). In 2013 additional control structures were installed to route the groundwater seep directly from the blast face into the stream, to prevent it from eroding sediment from the haul road into the stream. Crushed rock was also distributed over the haul road and landings to decrease erodible sediment, and some large piles of overburden were naturally overgrown by vegetation (Figure "+Quarry_picture['fig_num']+"). Longitudinal sampling of Faga'alu stream during baseflow conditions in 2011 showed significantly increased turbidity downstream of the quarry (FG2) and of a new bridge construction site on the village road approximately 200 m downstream of FG2 (Curtis et al., 2011). Construction of the bridge was completed in March 2012 and no longer increases turbidity. There are several small footpaths and unpaved driveways in the village, but most unpaved roads are stabilized with compacted gravel and do not appear to be a major contributor of sediment (Horsley-Witten, 2012b).")

## Quarry picture
if 'Quarry_picture' in locals():
    document.add_picture(Quarry_picture['filename'],width=Inches(6))
    add_figure_caption(Quarry_picture['fig_num'],"Photos of the open aggregate quarry in Faga'alu in 2012 (Top) and 2014 (Bottom). Photo: Messina")

#### METHODS
methods_title = document.add_heading('Methods',level=2)
document.add_paragraph("A nested-watershed approach was used to quantify the contribution of undisturbed and human-disturbed areas to the SSY to Faga'alu Bay during baseflow and during storm events of varying magnitude (SSYEV). The sediment load was calculated for each of three sampling points on the Faga'alu mainsteam (F1, F2, and F3) that drain key land covers suspected of having different SSY, including undisturbed forest, quarry, and village.  While steep, mountainous watersheds can discharge large amounts of bedload (Milliman and Syvitski, 1992), this research is focused on sediment size fractions that can be transported in suspension in the marine environment to settle on corals, and this is generally restricted to silt and clay fractions (<16um) (Asselman, 2000).")

document.add_paragraph("SSY generated by individual storm events (SSYEV) can be used to assess the contribution of individual subwatersheds to total SSY (Zimmermann et al., 2012), compare the responses of different watersheds to "+'"storm metrics"'+" (Basher et al., 2011; Duvert et al., 2012; Fahey et al., 2003; Hicks, 1990),  and determine changes in SSY from the same watershed over time (Bonta, 2000). SSYEV is calculated by integrating continuous estimates of suspended sediment yield, calculated from measured or modeled water discharge (Q) and measured or modeled suspended sediment concentration (SSC) (Duvert et al., 2012):")
add_equation(SSYEV_eq) ## Equation
### Comparing SSY from disturbed and undisturbed subwatersheds
document.add_heading('Quantifying SSY from disturbed and undisturbed subwatersheds',level=3)
document.add_paragraph("A main objective for this study was to determine how much human disturbance has increased total SSY to Faga'alu Bay (SSYTOTAL). Two approaches were used to determine relative contributions to SSY at the outlet that originates from undisturbed and human-disturbed areas: comparing individual event and average percent contributions of different subwatersheds to the total sediment load, and the Disturbance Ratio (DR). SSY from the upper subwatershed (SSYFG1) was measured at FG1, SSY at the outlet was measured at FG3 (SSYFG3), and SSY from the LOWER subwatershed (SSYLOWER) was calculated by subtracting SSYFG1 from SSYFG3 (SSYLOWER=SSYFG3-SSYFG1) (Figure "+Study_Area_map['fig_num']+"). Where SSYEV data at FG2 were also available, the contributions from the quarry subwatershed LOWER_QSUB (SSYLOWER_QSUB  = SSY_FG2-SSY_FG1) and village subwatershed LOWER_VILSUB (SSYLOWER_VILSUB =SSY_FG3-SSY_FG2) subwatersheds could be determined.  The percent contributions of each subwatershed were calculated for each storm event and averaged to determine the relative contributions from the UPPER and LOWER subwatersheds to total SSY. ") 

document.add_paragraph("The disturbance ratio (DR) is the ratio of specific SSYEV (sSSY tons/km2) from the total human-disturbed watershed under current conditions (SSYTOTAL), to SSY under pre-disturbance conditions:")
add_equation(DR_eq) ## Equation
document.add_paragraph("It is assumed that the whole watershed was originally covered in forest, with sSSY of forest in the LOWER subwatershed being equal to sSSY from the undisturbed UPPER subwatershed. The sSSY from the UPPER, undisturbed subwatershed can also be used to estimate SSY from the undisturbed forest portions which make up the majority of the LOWER subwatershed, and then estimate SSY from small human-disturbed areas by subtracting from SSYLOWER. sSSY estimated for the disturbed portions of the LOWER subwatershed can then be used to calculate a DR for these specific disturbed areas.")

### Predicting event suspended sediment yield (SSYEV)
document.add_heading("Predicting event suspended sediment yield (SSYEV)",level=3)
document.add_paragraph("SSYEV may be correlated with precipitation or discharge variables, so four "+'"storm metrics"'+" were tested: total event precipitation (Psum), event rainfall erosivity (EI30) (Hicks, 1990), total event water discharge (Qsum), and peak event water discharge (Qmax) (Duvert et al., 2012; Rodrigues et al., 2013). SSYEV and the discharge metrics (Qsum and Qmax) were normalized by watershed area, which gives the specific SSYEV (sSSYEV).")

document.add_paragraph("The relationship between SSYEV and storm metrics may be a linear function, but is most often best fit by a watershed-specific power law function of the form:")
add_equation(predict_SSYEV_eq) ## Equation

document.add_paragraph("In addition to the power function (Eq "+predict_SSYEV_eq.eq_num+"), the correlation between storm metrics and SSYEV was quantified using both parametric (Pearson) and non-parametric (Spearman) correlation coefficients.")

### Data Collection
document.add_heading('Data Collection',level=3)
document.add_paragraph("Data on precipitation, water discharge, suspended sediment concentration and turbidity were collected during three field campaigns: January-March, 2012, February-July 2013, and January-March 2014.")
# But your dataset goes beyond just these three periods b/c the instruments were left in the field…a figure may help to show deployment and data gathering period.

document.add_heading('Precipitation',level=4)
document.add_paragraph("Precipitation (P) was measured at three locations in Faga'alu watershed using two Rainwise RAINEW tipping-bucket rain gages (RG1 and RG2) and a Vantage Pro Weather Station (Wx)(Figure "+Study_Area_map['fig_num']+"). Data at RG2 was only recorded January-March, 2012, to determine a relationship between elevation and precipitation. Precipitation at 15 min intervals from Wx was used to fill any data gaps in precipitation recorded at RG1.The total event precipitation (Psum) and event rainfall erosivity (EI30) were calculated using data from RG1, with data gaps filled by data from Wx.")

## Water Discharge
document.add_heading('Water Discharge',level=4)
document.add_paragraph("Water discharge (Q) in Faga'alu Stream was calculated from 15 min interval stream stage measurements, using a stage-discharge rating curve calibrated to manual Q measurements made under baseflow and stormflow conditions. Stream stage was measured with non-vented pressure transducers (PT) (Solinst Levelogger or Onset HOBO Water Level Logger) installed in stilling wells at two locations in Faga'alu: FG1 and FG3. Stream gaging sites were chosen to take advantage of an existing control structure (FG1) and a stabilized stream cross section (FG3). Barometric pressure data collected at Wx were used to calculate stage from the pressure data recorded by the PT's. Data gaps in barometric pressure were filled by data from stations at Pago Pago Harbor (NSTP6) and NOAA Climate Observatory at Tula (TULA). Priority was given to the station closest to the watershed with valid barometric pressure data. Barometric data were highly correlated and the source data made little (<1cm) difference in the resulting water level.")

document.add_paragraph("Discharge (Q) was measured in the field by the area-velocity method (AV) using a Marsh-McBirney flowmeter to measure flow velocity, and simultaneous channel surveys to measure cross-sectional area (Harrelson et al., 1994; Turnipseed and Sauer, 2010). Q measurements were made at FG1 and FG3, and linear, log-linear, and nonlinear rating curves were tested for best fit. Measurements could not be made at high stages at FG1 and FG3 for safety reasons, and peak stages were higher than the highest manual stage-Q measurements. The stream cross-section at FG3 is a channelized rectangular channel with stabilized rip-rap banks and bed (Appendix Figure "+LBJ_Cross_Section['fig_num']+"), so the stage-discharge rating at FG3 was extrapolated using Manning's equation by calibrating Manning's n to the manual AV measurements.  The flow control structure at FG1 is a masonry ogee spillway crest of a defunct stream capture. The structure is a rectangular channel 43 cm deep, then transitions abruptly to gently sloping banks, causing an abrupt change in the stage-Q relationship (Appendix Figure "+DAM_Cross_Section['fig_num']+"). The flow control structure at FG1 did not meet the assumptions for modeling Q with Manning's equation so the rating was modeled with HEC-RAS and calibrated to the manual AV measurements (Brunner, 2010).  Water discharge at FG2 was the product of the specific water discharge from FG1 (Qm3/0.9km2) and the watershed area draining to FG2 (1.17km2). This assumes that.  Discharge may be higher from the quarry surface, which represents xx% of the LOWER_QSUB subwatershed, so sediment loads at the quarry are a conservative, lower bound estimate.")

DAM_Stormflow_conditions = DAM[DAM['stage']==DAM_storm_threshold.round(0)]['Q'][0]
LBJ_Stormflow_conditions = LBJ[LBJ['stage']==LBJ_storm_threshold.round(0)]['Q'][0]

document.add_paragraph("At FG1, stage recorded by the PT varied from "+"%.0f"%DAM['stage'].min()+" to "+"%.0f"%DAM['stage'].max()+"cm, while manual discharge measurements (n= "+"%.0f"%len(DAMstageDischarge)+") covered stages from "+"%.0f"%DAMstageDischarge['stage(cm)'].min()+" to "+"%.0f"%DAMstageDischarge['stage(cm)'].max()+"cm. Since the highest recorded stage ("+"%.0f"%DAM['stage'].max()+"cm) was higher than the highest stage with measured Q ("+"%.0f"%DAMstageDischarge['stage(cm)'].max()+"cm), and there was a distinct change in channel geometry above 43 cm (Appendix Figure "+DAM_Cross_Section['fig_num']+") the rating could not be extrapolated by mathematical methods like a power law (CITATION??). The flow structure did not meet the assumptions for using Manning's equation to predict flow so the HEC-RAS model was used. The surveyed geometry of the upstream channel and flow structure at FG1 was input to HEC-RAS, and the HEC-RAS model was calibrated to the manual Q measurements (Figure "+DAM_StageDischarge['fig_num']+"). While a power function fit measured Q better than HEC-RAS for low flow, HEC-RAS fit better at high Q, above the storm threshold (Figure "+DAM_StageDischarge['fig_num']+").The RMSE for the HEC-RAS model and Q measurements was "+"%.0f"%DAM_HEC_rmse+" %, which was used to calculate the total Probable Error.")

document.add_paragraph("At FG3, recorded stage varied from "+"%.0f"%LBJ['stage'].min()+" to "+"%.0f"%LBJ['stage'].max()+"cm. Manual discharge measurements (n= "+"%.0f"%len(LBJstageDischarge)+") were made from "+"%.0f"%LBJstageDischarge['Q-AV(L/sec)'].min()+" to "+"%.0f"%LBJstageDischarge['Q-AV(L/sec)'].max()+" L/sec, covering a range of stages from "+"%.0f"%LBJstageDischarge['stage(cm)'].min()+" to "+"%.0f"%LBJstageDischarge['stage(cm)'].max()+"cm. The highest recorded stage was much higher than the highest stage with measured Q so the rating could not be extrapolated by mathematical methods. The rating at FG3 was extrapolated using Manning's equation and surveyed stream geometry. Manning's n parameter was calibrated using the manual Q measurements (Figure "+LBJ_StageDischarge['fig_num']+"). The RMSE for Mannings modeled Q and Q measurements was "+"%.0f"%LBJ_Man_rmse+" (L/sec), which is used to calculate the total Probable Error. The RMSE for the AV measurements (FG1 and FG3)  from the DUET/WQ look-up table (Harmel et al., 2006) was "+"%.1f"%AV_Q_measurement_RMSE+" %.")

## Storm Events
document.add_heading('Storm Events',level=4)
document.add_paragraph("Storm events can be defined by precipitation (Hicks, 1990) or discharge parameters (Duvert et al., 2012), and the method used to separate storm events on the hydrograph can significantly influence the analysis of SSYEV (Gellis, 2013). Complex graphical or rule-based techniques for hydrograph separation may be implemented (Dunne and Leopold, 1978; Perrault, 2010), but for this research the simple stage height threshold rule was used due to the flashy hydrologic response, low baseflow discharge, and short duration of recession curves between events (Fahey et al., 2003; Lewis et al., 2001). A storm event was defined as the period of time when stream stage height exceeds a given threshold. Complex storm events occurred when subsequent rain fell before the stream stage fell below the storm threshold. These events were separated manually into individual storms for analysis, but required the discretion of the analyst (Duvert, 2012).  Where Q peaks were separated by at least a two hour period and Q was nearly at baseflow, complex storm events were separated into individual storm events.")

## Suspended Sediment Yield
document.add_heading('Suspended Sediment Concentration and Turbidity',level=4)
document.add_paragraph("Stream water samples were collected by grab or "+'"dip"'+" sampling with 500mL HDPE bottles at FG1, FG2, and FG3. At FG2, water samples were also collected at 30 min intervals by an ISCO 3700 Autosampler triggered by a stage height sensor. Samples were analyzed for suspended sediment concentration (SSC) on-island using gravimetric methods (Gray et al., 2000). Water samples were vacuum filtered on pre-weighed 47mm diameter, 0.7um Millipore AP40 glass fiber filters, oven dried at 100C for one hour, cooled and weighed to determine SSC (mg/L).")
def No_All_samples(location):
    No_samples = len(SSC_dict['Pre-ALL'][SSC_dict['Pre-ALL']['Location'].isin([location])])
    return No_samples
## Mean and Max SSC  numbers
def Mean_and_Max_SSC(ssc,location):
    mean =  int(ssc[ssc['Location'].isin([location])]['SSC (mg/L)'].mean())
    maximum = int(ssc[ssc['Location'].isin([location])]['SSC (mg/L)'].max())
    return "{:,}".format(mean), "{:,}".format(maximum)
Mean_SSC_FG1, Max_SSC_FG1  = Mean_and_Max_SSC(SSC_dict['Pre-ALL'],'DAM')
Mean_SSC_FG2, Max_SSC_FG2 = Mean_and_Max_SSC(SSC_dict['Pre-ALL'],'DT')
Mean_SSC_FG3, Max_SSC_FG3 = Mean_and_Max_SSC(SSC_dict['Pre-ALL'],'LBJ')
Max_SSC_FG3_Event = "{:%m/%d/%Y}".format(SSC_dict['Pre-ALL'][SSC_dict['Pre-ALL']['Location'].isin(['LBJ'])]['SSC (mg/L)'].idxmax())
Max_SSC_FG3_Q = "{:,}".format(int(LBJ['Q'][SSC_dict['Pre-ALL'][SSC_dict['Pre-ALL']['Location'].isin(['LBJ'])]['SSC (mg/L)'].idxmax()]))
Max_SSC_FG1_Event = "{:%m/%d/%Y}".format(SSC_dict['Pre-ALL'][SSC_dict['Pre-ALL']['Location'].isin(['DAM'])]['SSC (mg/L)'].idxmax())
Max_SSC_FG1_Q = "{:,}".format(int(DAM['Q'][SSC_dict['Pre-ALL'][SSC_dict['Pre-ALL']['Location'].isin(['DAM'])]['SSC (mg/L)'].idxmax()]))

document.add_paragraph("From January 6, 2012, to October 1, 2014, "+str(len(SSC_dict['Pre-ALL']))+" water samples were collected at 12 sites in Faga'alu and analyzed for SSC. Three sites were the focus of this analysis: 1) FG1 (n="+"%.0f"%No_All_samples('DAM')+"), 2) FG2 (n="+"%.0f"%No_All_samples('DT')+" grab samples, n="+"%.0f"%No_All_samples('R2')+" from the Autosampler), and 3) FG3 (n="+"%.0f"%No_All_samples('LBJ')+"). ")

document.add_paragraph("SSC at 15 min intervals was estimate d from 1) 15 min interval turbidity (T) data and a T-SSC relationship calibrated to stream water samples collected over a range of Q and SSC (FG1 and FG3), and 2) linear interpolation of SSC from grab (FG1, FG2, FG3) and autosamples (FG2) , which could only be calculated if more than three samples were collected during the storm event, and if they adequately captured the SSC dynamics of the storm event. SSC was assumed to be zero at the beginning and end of each storm if no grab sample data was available (Lewis 2001). The T-SSC relationship is unique to each region, or even each stream and storm event, and can be influenced by water color, dissolved solids and organic matter, temperature, and the shape, size, and composition of sediment. However, T has proved to be a robust surrogate measure of SSC in streams (Gippel 1995) and is most accurate when a unique T-SSC relationship is developed for each instrument separately using in situ grab samples under storm conditions (Lewis 1996).")

document.add_paragraph("Turbidity (T) was measured at FG1 and FG3 using three types of turbidimeters: 1) a Greenspan TS3000 (TS), 2) a YSI 600OMS with 6136 turbidity probe (YSI), and 3) a CampbellSci OBS500 (OBS). All turbidimeters were permanently installed in protective PVC housings near the streambed where the turbidity probe would be submerged at all flow conditions, and oriented downstream. Despite regular maintenance, debris fouling during storm and baseflows was common and caused data loss during several storm events. Storm events with incomplete or invalid T data were not used in the analysis. A three-point calibration was performed on the YSI turbidimeter with YSI turbidity standards (0, 126, and 1000 NTU) at the beginning of each field season and approximately every 3-6 months during data collection.  Turbidity measured with 100 and 1000 NTU standards differed by less than 10% (4-8%) during each recalibration. The TS turbidimeter at FG1 was vandalized and removed from service before recalibration. All turbidimeters were regularly cleaned following storms to ensure proper operation.")

document.add_paragraph("At FG3, the YSI turbidimeter recorded T (NTU) at 5 min intervals from January 30, 2012, to February 20, 2012, and at 15 min intervals from February 27, 2012 to May 23, 2012, when it was damaged during a large storm. The YSI turbidimeter was replaced with an OBS which recorded Backscatter (BS) and Sidescatter (SS, comparable to NTU) at 5 min intervals from March 7, 2013, to July 15, 2014. Both BS and SS were analyzed to determine which showed the best relationship with SSC. No data was recorded from August 2013-January 2014 due to wiper clogging with sediment. A new OBS was installed at FG3 from January, 2014, to August, 2014. To correct for some periods of high noise observed in the BS and SS data recorded by the OBS in 2013, the new OBS was programmed to make 100 BS and SS measurements every 15Min, and record Median, Mean, STD, Min, and Max BS and SS. All BS and SS parameters were analyzed to determine which showed the best relationship with SSC.")

document.add_paragraph("At FG1, a TS turbidimeter recorded T (NTU) at 5 min intervals from January 2012-July 2012, when it was vandalized and destroyed. The YSI turbidimeter previously deployed at FG3 in 2012 was repaired and redeployed at FG1 and recorded T (NTU) at 5 min intervals from June 2013 to October 2013, and January 2014 to August 2014. Turbidity data was resampled to 15 min intervals to compare with SSC samples for the T-SSC relationship, and corresponding to Q for calculating suspended sediment yield (SSY) (Equation "+SSYEV_eq.eq_num+").")

document.add_paragraph("A unique T-SSC relationship was developed for each turbidimeter at each location using 15 min interval T data and SSC samples from storm periods only. A "+'"synthetic"'+" T-SSC relationship (SRC) was also developed by placing the turbidimeter in a black tub with water, and sampling T and SSC as sediment was added, but results from the SRC's were not comparable to T-SSC relationships developed under actual storm conditions and were not used in further analyses.")

## Measurement Uncertainty
document.add_heading('Measurement Uncertainty',level=3)
document.add_paragraph("Uncertainty in SSYEV estimates arises from both measurement and model errors, including models of stage-discharge (stage-Q) and turbidity-suspended sediment concentration (T-SSC) (Harmel et al., 2006). The Root Mean Square Error (RMSE) method estimates the "+'"most probable value"'+" of the cumulative or combined error by propagating the error from each measurement and modeling procedure to the final SSYEV estimate (Topping, 1972). The resulting cumulative probable error (PE) is the square root of the sum of the squares of the maximum values of the separate errors:")
add_equation(PE_eq) ## Equation
document.add_paragraph("Error from manual water discharge measurements using the Area-Velocity method, from continuous discharge measurment in a natural channel, from grab sampling and autosampling SSC during stormflows, and from lab procedures are considered "+'"measurement errors"'+" and were estimated using lookup tables from the DUET-H/WQ software tool (Harmel et al., 2006). These measurement errors (RMSE) were combined with the modeling errors (RMSE) from the stage-Q and T-SSC relationships to calculate PE for each storm event, to add a statistical measure of uncertainty to SSYEV (plus-minus tons). The effect of uncertain SSYEV estimates may complicate conclusions about contributions from subwatersheds, anthropogenic impacts, and SSYEV-Storm Metric relationships. This is common in sediment yield studies where successful models estimate SSY with plus-minus 50-100% accuracy (Duvert et al., 2012). Preliminary data and field observations suggested the difference in SSYEV from the upper and lower subwatersheds is significantly larger than the ranges of uncertainty in the SSY estimates.")

#### RESULTS ####
results_title = document.add_heading('Results',level=2)
## Field data collection
document.add_heading('Field Data Collection',level=3)

#### Precipitation
document.add_heading('Precipitation',level=4)
percent_of_annual_mean_P = (PrecipFilled[start2012:stop2012].sum() + PrecipFilled[start2013:stop2013].sum() +PrecipFilled[start2014:dt.datetime(2014,12,31)].sum())/(3*3800) *100
document.add_paragraph("Annual precipitation measured at RG1 (gaps filled with data from Wx) was "+"%.0f"%PrecipFilled[start2012:stop2012].sum()+"mm, "+"%.0f"%PrecipFilled[start2013:stop2013].sum()+"mm, and "+"%.0f"%PrecipFilled[start2014:stop2014].sum()+" in 2012, 2013, and 2014 respectively. These annual rainfall amounts are approximately "+"%.0f"%percent_of_annual_mean_P+"% of long-term rainfall data (=3,800mm) from the PRISM Climate Group (Craig, 2009). Comparison of rain gauge data showed no orographic relationship between RG1 and Wx, or RG1 and RG2, so precipitation was assumed to be homogenous over the watershed for all analyses. Rain gauges could only be placed as high as ~300m (RG2), though the highest point in the watershed is ~600m. Long-term rain gage records show a strong precipitation gradient with increasing elevation, with average precipitation of 3,000-4,000mm on the lowlands, increasing to more than 6,350mm at the high elevations (>400 m.a.s.l.) around the harbor (Craig, 2009; Dames & Moore, 1981; Wong, 1996). Rainfall data measured at higher elevations would be useful to determine a more robust orographic rainfall relationship. For this analysis, however, precipitation is only used as a predictive storm metric, and the absolute values of total rainfall in each subwatershed are not as important.")

#### Water Discharge
document.add_heading('Water Discharge',level=4)


## DAM stage-discharge rating
if 'DAM_StageDischarge' in locals():
    document.add_picture(DAM_StageDischarge['filename']+'.png',width=Inches(6))
    add_figure_caption(DAM_StageDischarge['fig_num'],"Stage-Discharge relationships for stream gaging site at FG1 for (a) the full range of observed stage and (b) the range of stages with AV measurements of Q. "+'"Channel Top"'+" refers to the point where the rectangular channel transitions to a sloped bank and cross-sectional area increases much more rapidly with stage. A power-law relationship is also displayed to illustrate the potential error that could result if inappropriate methods are used.")



## LBJ stage-discharge rating
if 'LBJ_StageDischarge' in locals():
    document.add_picture(LBJ_StageDischarge['filename']+'.png',width=Inches(6))
    add_figure_caption(LBJ_StageDischarge['fig_num'],"Stage-Discharge relationships for stream gaging site at FG3 for (a) the full range of observed stage and (b) the range of stages with AV measurements of Q.")
    
document.add_paragraph("Discharge at both FG1 and FG3 was characterized by periods of low but perennial baseflow (FG1: "+"%.0f"%DAM['Q'].min()+"-"+"%.0f"%DAM_Stormflow_conditions+" L/sec; FG3: "+"%.0f"%LBJ['Q'].min()+"-"+"%.0f"%LBJ_Stormflow_conditions+" L/sec), punctuated by short, flashy hydrograph peaks (FG1: max "+"%.0f"%DAM['Q'].max()+" L/sec, FG3: max "+"%.0f"%LBJ['Q'].max()+" L/sec) (Figure "+Q_timeseries['fig_num']+").")

if 'Q_timeseries' in locals():
    document.add_picture(Q_timeseries['filename']+'.png',width=Inches(6))
    add_figure_caption(Q_timeseries['fig_num'],"Time series of water discharge (Q), calculated from measured stage and the stage-discharge rating curves.")

#### Storm Events
document.add_heading('Storm Events',level=4)
No_of_Storm_Intervals = len(LBJ_StormIntervals[LBJ_StormIntervals['start']<Mitigation])
No_of_Storm_Intervals_DAM_Q = len(SedFluxStorms_DAM[SedFluxStorms_DAM['Qstart']<Mitigation]['Qsum'].dropna())
No_of_Storm_Intervals_LBJ_Q = len(SedFluxStorms_LBJ[SedFluxStorms_LBJ['Qstart']<Mitigation]['Qsum'].dropna())
No_of_Storm_Intervals_DAM_S = len(SedFluxStorms_DAM[SedFluxStorms_DAM['Sstart']<Mitigation]['Ssum'].dropna())
No_of_Storm_Intervals_LBJ_S = len(SedFluxStorms_LBJ[SedFluxStorms_LBJ['Sstart']<Mitigation]['Ssum'].dropna())
No_of_Storm_Intervals_QUA_S = S_Diff_table_quarry['Storm#'].max()
max_storm_duration = LBJ_StormIntervals['duration (hrs)'].max()/24

document.add_paragraph("Using the stage threshold method and manual separation of complex storm events, "+"%.0f"%No_of_Storm_Intervals+" storm events were identified from Q data at FG3 from January, 2012, to July 2014. Valid Q data was recorded during "+"%.0f"%No_of_Storm_Intervals_DAM_Q+" events at FG1, and "+"%.0f"%No_of_Storm_Intervals_LBJ_Q+" events at FG3 (Appendix, Table "+Q_Diff_table.table_num+"). Valid SSC data from T and Interpolated Grab samples was recorded during "+"%.0f"%No_of_Storm_Intervals_DAM_S+" events at FG1, and "+"%.0f"%No_of_Storm_Intervals_LBJ_S+" events at FG3. Of those storms, "+"%.0f"%S_Diff_table['Storm#'][S_Diff_table['Storm#']!=''].astype(float).max()+" events had valid P and SSY data for both the FG1 and FG3 to calculate and compare SSY from the UPPER and LOWER subwatersheds. Valid SSY data from interpolated grab samples was collected at FG2 for "+No_of_Storm_Intervals_QUA_S+" storms to compare with SSY from FG1 and FG3 directly. Storm event durations ranged from "+"%.0f"%LBJ_StormIntervals['duration (hrs)'].min()+" hours to "+"%.0f"%max_storm_duration+" days, with mean duration of "+"%.0f"%LBJ_StormIntervals['duration (hrs)'].mean()+" hours.") 

document.add_paragraph("Most storm events showed a typical pattern, where a short period of intense rainfall caused a rapid increase in SSC downstream of the quarry (FG2) while SSC remained low at the forest site (FG1), indicating sheetwash of sediment from the quarry into the stream (Figure "+Example_Storm['fig_num']+"). Highest event SSC was typically observed at FG2, with slightly lower and later peak SSC observed at FG3. SSC at FG1 typically increased more slowly, remained much lower, and peaked later than the downstream sites (FG2 and FG3). Though peak SSC was highest at FG2, the total SSY was highest at FG3 due to the addition of storm runoff from the increased cumulative area draining to FG3. Storm flow at FG3 includes both storm runoff and sediment from disturbed areas of the quarry and village, and the undisturbed forest on the steep hillsides in the lower watershed. Complex storm events occurred when a subsequent period of rainfall followed before Q and SSC fell back to baseflow levels. Several complex events were identified and separated into individual storm events.")

if 'Example_Storm' in locals():
    document.add_picture(Example_Storm['filename']+'.png',width=Inches(6))
    add_figure_caption(Example_Storm['fig_num'],"Example of storm event ("+"{:%m/%d/%Y}".format(LBJ_StormIntervals.loc[63]['start'])+"). SSY at FG1 and FG3 calculated from SSC modeled from T, and SSY at FG2 from SSC samples collected by the Autosampler.")
    

#### Suspended Sediment Concentration
document.add_heading('Suspended Sediment Concentration',level=4)
document.add_heading("Mean and maximum SSC of grab and autosamples collected during baseflow and stormflow were lowest at the FG1 site (u="+Mean_SSC_FG1+" mg/L, max="+Max_SSC_FG1+" mg/L), highest at FG2 ("+Mean_SSC_FG2+" mg/L and "+Max_SSC_FG2+") and in between at the downstream FG3 site ("+Mean_SSC_FG3+" mg/L and "+Max_SSC_FG3+" mg/L). The maximum SSC values at FG2 and FG3 were sampled during the same event ("+Max_SSC_FG3_Event+"), during fairly low discharge (Q_FG3="+Max_SSC_FG3_Q+" L/sec)(Figure "+Discharge_Concentration['fig_num']+"). The maximum SSC value for the upstream site () was sampled on "+Max_SSC_FG1_Event+" at high discharge (Q_FG1= "+Max_SSC_FG1_Q+" L/sec). Anecdotal and field observations reported higher than normal SSC upstream of the quarry during the 2013 field season, possibly due to landsliding from large storms (G. Poysky, pers. comm.).")


def Mean_storm_SSC(location):    
    Mean_storm_samples  = SSC_dict['Pre-storm'][SSC_dict['Pre-storm']['Location'].isin([location])]['SSC (mg/L)'].mean()
    return "%.0f"%Mean_storm_samples 
def No_storm_samples(location):
    No_storm = len(SSC_dict['Pre-storm'][SSC_dict['Pre-storm']['Location'].isin([location])])
    return "%.0f"%No_storm
def Percent_storm_samples(location):
    storm_samples = len(SSC_dict['Pre-storm'][SSC_dict['Pre-storm']['Location'].isin([location])])
    all_samples = len(SSC_dict['Pre-ALL'][SSC_dict['Pre-ALL']['Location'].isin([location])]) 
    percent_storm = storm_samples/all_samples *100
    return "%.0f"%percent_storm
Percent_storm_FG1 = Percent_storm_samples('DAM')
Percent_storm_FG2 = Percent_storm_samples('DT')
Percent_storm_FG3 = Percent_storm_samples('LBJ')

def Mean_baseflow_SSC(location):    
    Mean_baseflow_samples  = SSC_dict['Pre-baseflow'][SSC_dict['Pre-baseflow']['Location'].isin([location])]['SSC (mg/L)'].mean()
    return "%.0f"%Mean_baseflow_samples 
def No_baseflow_samples(location):
    No_baseflow = len(SSC_dict['Pre-baseflow'][SSC_dict['Pre-baseflow']['Location'].isin([location])])
    return "%.0f"%No_baseflow
def Percent_baseflow_samples(location):
    baseflow_samples = len(SSC_dict['Pre-baseflow'][SSC_dict['Pre-baseflow']['Location'].isin([location])])
    all_samples = len(SSC_dict['Pre-ALL'][SSC_dict['Pre-ALL']['Location'].isin([location])]) 
    percent_baseflow = baseflow_samples/all_samples *100
    return "%.0f"%percent_baseflow
Percent_baseflow_FG1 = Percent_baseflow_samples('DAM')
Percent_baseflow_FG2 = Percent_baseflow_samples('DT')
Percent_baseflow_FG3 = Percent_baseflow_samples('LBJ')

document.add_paragraph("At FG1,  "+Percent_storm_FG1+"% of grab samples (n="+No_storm_samples('DAM')+") were taken during stormflow conditions (Q_FG1>"+"%.0f"%DAM_Stormflow_conditions+" L/sec), with mean SSC of "+Mean_storm_SSC('DAM')+" mg/L (Figure "+SSC_Boxplots['fig_num']+"), and "+Percent_baseflow_FG1+"% of grab samples (n="+No_baseflow_samples('DAM')+") were taken during baseflow conditions with a mean SSC of "+Mean_baseflow_SSC('DAM')+" mg/L (Figure "+SSC_Boxplots['fig_num']+"(a)). At FG2, "+Percent_storm_FG2 +"% of grab samples (n="+No_storm_samples('DT')+") were taken during stormflow conditions (Q_FG1>"+"%.0f"%DAM_Stormflow_conditions+" L/sec), with mean SSC of "+Mean_storm_SSC('DT')+" mg/L, and "+Percent_baseflow_FG2 +"% of grab samples (n="+No_baseflow_samples('DT')+") were taken during baseflow conditions, with mean SSC of "+Mean_baseflow_SSC('DT')+" mg/L. At FG3, "+Percent_storm_FG3+"% of samples (n="+No_storm_samples('LBJ')+") were taken during stormflow conditions (Q_FG3>"+"%.0f"%LBJ_Stormflow_conditions+" L/sec), with mean SSC of "+Mean_storm_SSC('LBJ')+" mg/L, and "+Percent_baseflow_FG3+"% of samples (n="+No_baseflow_samples('LBJ')+") were taken during baseflow conditions, with mean SSC of "+Mean_baseflow_SSC('LBJ')+" mg/L. This pattern of SSC values suggests that little sediment is contributed from the forest upstream of FG1, then there is a large input of sediment between FG1 and FG2, and then SSC is diluted by addition of stormflow with lower SSC between FG2 and FG3.")

## SSC boxplots
# Stormflow
if 'SSC_Boxplots' in locals():
    document.add_picture(SSC_Boxplots['filename']+'.png',width=Inches(6))
    add_figure_caption(SSC_Boxplots['fig_num'],"Boxplots of Suspended Sediment Concentration (SSC) from grab samples only (no Autosampler) at FG1, FG2, and FG3 during  (a) baseflow and (b) stormflow.")
 
## Water Discharge vs Sediment Concentration
document.add_paragraph("The highest SSC values were observed just downstream of the quarry (FG2), mainly during discharges that fell below the storm threshold. The high SSC during discharges classified as baseflow was caused by 1) washing of quarry surfaces during regular maintenance activities at the quarry and 2) rainfall events that did not result in a significant rise in the water level in the stream, but generated runoff from the quarry that had high SSC. Given the close proximity of the quarry to the stream, SSC downstream of the quarry can be highly influenced by mining activity like rock extraction, crushing or hauling operations. During 2012 a common practice for removing fine sediment from crushed aggregate was to rinse it with water pumped from the stream. In the absence of retention structures the fine sediment was discharged directly into the stream, causing high SSC during interstorm periods with low Q. During periods with high pre-storm SSC, sheetwash erosion in the quarry during storm events causes higher SSY than during baseflow periods, but instantaneous SSC values during stormflows are sometimes lower due to dilution by water discharged from surrounding forest areas.   During periods with low pre-storm SSC, SSC increased during the storm (Figure "+Example_Storm['fig_num']+"). Riverine discharge of fine sediment by rinsing from aggregate was discontinued in 2013, corresponding with a lack of high SSC grab samples during low discharges (Figure "+Discharge_Concentration['fig_num']+"). Currently, waste sediment is piled on-site and severe erosion of these changing stockpiles causes high SSC during storm events.")

## Discharge Concentration
if 'Discharge_Concentration' in locals():
    document.add_picture(Discharge_Concentration['filename']+'.png',width=Inches(6))
    add_figure_caption(Discharge_Concentration['fig_num'],"Water Discharge vs Suspended Sediment Concentration at FG1, FG2, and FG3 during baseflow and stormflow periods. Samples from Autosampler are included with grab samples at FG2.")

document.add_paragraph("SSC varied widely for a given discharge at all three sites (FG1, FG2, FG3) due to significant hysteresis observed during storm periods. At FG2 and FG3, additional variability in the Q-SSC relationship was due to the changing sediment availability associated with quarrying operations and construction in the village. At FG1, variability of SSC samples during stormflows from year to year was assumed to be caused by randomly occurring landslides caused by large storms.")


#### Turbidity
document.add_heading('Turbidity-SSC relationships', level=4)
document.add_paragraph("The T-SSC relationships under actual storm conditions all showed acceptable r2 values ("+"%.2f"%LBJ_YSI_rating.r2+"-"+"%.2f"%DAM_YSI_rating.r2+"), so the SRC's were not used to model SSC from T data. The T-SSC relationship varied among sampling sites and sensors. Lower scatter was achieved by using grab samples collected during stormflows only. It is assumed that the color, particle sizes, and composition of sediment changes during stormflows when sediment from the quarry, which is lighter in color and finer, is present. For the TS deployed at FG1, the r2 value was fairly high ("+"%.2f"%DAM_TS3K_rating.r2+") but the ranges of T and SSC values used to develop the relationship were considered too small (0-"+"%.0f"%T_SSC_DAM_TS3K[1]['T-NTU'].max()+" NTU) compared to the maximum observed during the deployment period ("+"%.0f"%DAM_TS3K['NTU'].max()+") to develop a robust relationship for higher T values. Instead, the T-SSC relationship developed for the YSI turbidimeter installed at FG3 (Figure "+T_SSC_Rating_Curves['fig_num']+") was used to convert T data from the TS to SSC at FG1. For the YSI 600OMS turbidimeter, more scatter was observed in the T-SSC relationship at FG3 than at FG1 (Figure "+T_SSC_Rating_Curves['fig_num']+"), but this could be attributed to the higher number and wider range of values sampled, as well the contribution of multiple sediment sources sampled at FG3.") 
#The RMSE was xx mg/L and relative RMSE was xx% for the T-SSC relationship of the YSI.
#LBJ_YSI_rating.rmse
#DAM_YSI_rating.rmse

## LBJ and DAM YSI T-SSC rating curves
if 'T_SSC_Rating_Curves' in locals():
    document.add_picture(T_SSC_Rating_Curves['filename']+'.png',width=Inches(6))
    add_figure_caption(T_SSC_Rating_Curves['fig_num'],"Turbidity-Suspended Sediment Concentration relationships for a) the YSI turbidimeter deployed at FG3 ("+"{:%m/%d/%Y}".format(LBJ_YSI.dropna().index[0])+"-"+"{:%m/%d/%Y}".format(LBJ_YSI.dropna().index[-1])+") and the same YSI turbidimeter deployed at FG1 ("+"{:%m/%d/%Y}".format(DAM_YSI.dropna().index[0])+"-"+"{:%m/%d/%Y}".format(DAM_YSI.dropna().index[-1])+"). b) OBS500 turbidimeter deployed at FG3 ("+"{:%m/%d/%Y}".format(LBJ_OBSa.dropna().index[0])+"-"+"{:%m/%d/%Y}".format(LBJ_OBSa.dropna().index[-1])+") and c) OBS500 turbidimeter deployed at FG3 ("+"{:%m/%d/%Y}".format(LBJ_OBSb.dropna().index[0])+"-"+"{:%m/%d/%Y}".format(LBJ_OBSb.dropna().index[-1])+". ")
    
document.add_paragraph("The CampbellSci OBS500 measures both backscatter(BS) and sidescatter (SS), and both the BS-SSC and SS-SSC relationships at FG3 showed high R2 values (Figure "+T_SSC_Rating_Curves['fig_num']+" and Figure "+T_SSC_Rating_Curves['fig_num']+"). Mean SS was used since it is measured the same as NTU measured by the YSI turbidimeter (Anderson 2005).") 

#### Probable Error Estimates
document.add_heading('Probable Error estimates for SSY',level=3)
document.add_paragraph("Probable Error (%) was calculated by equation "+PE_eq.eq_num +" to estimate the uncertainty in SSYEV resulting from measurement and model errors (Harmel et al., 2006). The RMSE for each selected T-SSC relationship was computed and used in the estimate of Probable Error. The RMSE for the T-SSC relationship was "+"%.0f"%DAM_YSI_rating.rmse+", "+"%.0f"%LBJ_YSI_rating.rmse+", "+"%.0f"%LBJ_OBSa_rating.rmse+", "+"%.0f"%LBJ_OBSb_rating.rmse+" mg/L for the YSI at FG1, YSI at FG3, CampbellSci OBS500 at FG3 (2013), and CampbellSci OBS500 at FG3 (2014), respectively. The RMSE for YSI at FG1 was also used for the TS at FG1 since the same T-SSC relationship was used.")

#### Comparing SSY from disturbed and undisturbed subwatersheds
document.add_heading('Comparing SSY from disturbed and undisturbed subwatersheds',level=3)
document.add_paragraph("A main objective for this study was to determine how much human disturbance has increased Total SSY to Faga'alu Bay (SSYTOTAL). SSY from the UPPER subwatershed (SSYUPPER) was measured at FG1, SSYTOTAL was measured at FG3, and SSY from the LOWER subwatershed (SSYLOWER) was calculated by subtracting SSYUPPER from SSYTOTAL (SSYLOWER = SSYFG3 - SSYFG1) (Table "+S_Diff_table.table_num+").")

## Storm Sediment Table
if 'S_Diff_table' in locals():
    dataframe_to_table(df=S_Diff_table,table_num=S_Diff_table.table_num,caption="Sediment yield from subwatersheds in Faga'alu",fontsize=9)
document.add_paragraph('')

Percent_Upper_S_2 = S_Diff_table['% UPPER']['Total/Avg:']
Percent_Lower_S = S_Diff_table['% LOWER']['Total/Avg:']
S_Diff_table_percents = S_Diff_table[S_Diff_table['% UPPER']!='-']
Percent_Upper_S_min, Percent_Upper_S_max =  "%0.1f"%S_Diff_table_percents['% UPPER'].astype(float).min(), "%.0f"%S_Diff_table_percents['% UPPER'].astype(float).max()
Percent_Lower_S_min, Percent_Lower_S_max =  "%.0f"%S_Diff_table_percents['% LOWER'].astype(float).min(), "%.0f"%S_Diff_table_percents['% LOWER'].astype(float).max()

Area_UPPER, Area_LOWER = landcover_table.ix[0]['Area km2'], landcover_table.ix[3]['Area km2']
SSY_UPPER_2, sSSY_UPPER_2 = S_Diff_table['UPPER tons']['Total/Avg:'], S_Diff_table['UPPER tons']['Tons/km2'] 
SSY_LOWER_2, sSSY_LOWER_2 = S_Diff_table['LOWER tons']['Total/Avg:'], S_Diff_table['LOWER tons']['Tons/km2']
SSY_TOTAL_2, sSSY_TOTAL_2 = S_Diff_table['TOTAL tons']['Total/Avg:'], S_Diff_table['TOTAL tons']['Tons/km2']
P_measured_2, P_measured_2_perc_ann = S_Diff_table['Precip (mm)']['Total/Avg:'], "%.0f"%(float(S_Diff_table['Precip (mm)']['Total/Avg:'])/4000 *100)
disturbed_area_LOWER = Area_LOWER * float(S_Diff_table['LOWER tons']['fraction disturbed (%)'])/100


document.add_paragraph("The UPPER and LOWER subwatersheds are similar in size ("+"%0.2f"%Area_UPPER+" km2 and "+"%0.2f"%Area_LOWER+" km2) but SSYUPPER accounted for an average of just"+Percent_Upper_S_2+"% and SSYLOWER for "+Percent_Lower_S+"% at the outlet (Table "+S_Diff_table.table_num+"). SSY from the UPPER and LOWER subwatersheds for the measured storms was "+SSY_UPPER_2+" and "+SSY_LOWER_2+" tons, respectively, and corresponding sSSY was "+sSSY_UPPER_2+" and "+sSSY_LOWER_2+" tons/km2, respectively. The DR estimated from sSSY_UPPER and the sSSY_LOWER suggests sSSY has been increased by "+S_Diff_table['LOWER tons']['DR']+"x in the LOWER subwatershed, and "+S_Diff_table['TOTAL tons']['DR']+"x for the TOTAL watershed.")

#document.add_paragraph("The DR for specific water discharge (Q) was also calculated to determine if observed changes in SSY were attributable to errors in quantifying Q, and if urbanization and agriculture has affected the total water discharge from the watershed. The DR for water discharge was "+DR_Q+", suggesting that specific water discharge from the subwatersheds is the same, which is expected since they are similar sizes. Urbanization has likely increased water discharge, since the relatively large amounts of impervious surface in the village area increase runoff. However, the village area occupies a small percentage ("+"%.1f"%landcover_table.ix[2]['% High Intensity Developed']+"%) of the LOWER subwatershed area in comparison to the forest area ("+"%.1f"%landcover_table.ix[2]['% Forest']+") (Table "+landcover_table.table_num+"), and the relatively small increase in Q could be within the acceptable measurement error for quantifying Q.")  

document.add_paragraph("The measured sSSY from the undisturbed UPPER watershed (="+sSSY_UPPER_2+" tons/km2) was used to estimate SSY from undisturbed areas in the LOWER subwatershed ("+S_Diff_table['LOWER tons']['SSY from forested areas (tons)']+" tons), and SSY from the disturbed areas could be determined by subtracting from SSYLOWER ("+S_Diff_table['LOWER tons']['SSY from disturbed areas (tons)']+" tons). For the measured storms (Table "+S_Diff_table.table_num+"), roughly "+S_Diff_table['LOWER tons']['% SSY from disturbed areas']+"% of SSY from the LOWER subwatershed is from disturbed areas, despite the disturbed areas only accounting for "+S_Diff_table['LOWER tons']['fraction disturbed (%)']+"% of the subwatershed area ("+"%0.3f"%disturbed_area_LOWER+" km2). Similarly, despite only "+S_Diff_table['TOTAL tons']['fraction disturbed (%)']+"% of the TOTAL watershed being disturbed, SSY from disturbed areas accounts for "+S_Diff_table['TOTAL tons']['% SSY from disturbed areas']+"% of the SSY from the TOTAL watershed. Estimated sSSY from disturbed areas in the LOWER subwatershed is "+S_Diff_table['LOWER tons']['sSSY from disturbed areas (tons/km2)']+" tons/km2, suggesting human disturbance has increased sSSY by "+S_Diff_table['LOWER tons']['DR for sSSY from disturbed areas']+"x over undisturbed, forest conditions.")

## Comparing QUARRY and VILLAGE separately
Percent_UPPER_S_3 = S_Diff_table_quarry['% UPPER']['Total/Avg:']
Percent_QUARRY_S = S_Diff_table_quarry['% LOWER_QUARRY']['Total/Avg:']
Percent_VILLAGE_S = S_Diff_table_quarry['% LOWER_VILLAGE']['Total/Avg:']

SSY_UPPER_3, sSSY_UPPER_3 = S_Diff_table_quarry['UPPER tons']['Total/Avg:'], S_Diff_table_quarry['UPPER tons']['Tons/km2'] 
SSY_LOWER_QUARRY, sSSY_LOWER_QUARRY = S_Diff_table_quarry['LOWER_QUARRY tons']['Total/Avg:'], S_Diff_table_quarry['LOWER_QUARRY tons']['Tons/km2']
SSY_LOWER_VILLAGE, sSSY_LOWER_VILLAGE = S_Diff_table_quarry['LOWER_VILLAGE tons']['Total/Avg:'], S_Diff_table_quarry['LOWER_VILLAGE tons']['Tons/km2']
SSY_TOTAL_3, sSSY_TOTAL_3 = S_Diff_table_quarry['TOTAL tons']['Total/Avg:'], S_Diff_table_quarry['TOTAL tons']['Tons/km2']
P_measured_3, P_measured_3_perc_ann = S_Diff_table_quarry['Precip (mm)']['Total/Avg:'], "%.0f"%(float(S_Diff_table_quarry['Precip (mm)']['Total/Avg:'])/4000 *100)

Area_UPPER, Area_LOWER_QUARRY, Area_LOWER_VILLAGE = landcover_table.ix[0]['Area km2'], landcover_table.ix[1]['Area km2'], landcover_table.ix[2]['Area km2']
disturbed_area_LOWER_QUARRY = Area_LOWER_QUARRY * float(S_Diff_table_quarry['LOWER_QUARRY tons']['fraction disturbed (%)'])/100
disturbed_area_LOWER_VILLAGE = Area_LOWER_VILLAGE * float(S_Diff_table_quarry['LOWER_VILLAGE tons']['fraction disturbed (%)'])/100

document.add_paragraph("SSYEV data measured at FG2 was available for "+No_of_Storm_Intervals_QUA_S+" of the storms, so SSYEV from the LOWER subwatershed including the quarry (SSYLOWER_QUARRY) and the village areas below the quarry (SSYLOWER_VILLAGE) could be calculated to determine the relative sediment contribution from these sources (Table "+S_Diff_table_quarry.table_num+").")

if 'S_Diff_table_quarry' in locals():
    dataframe_to_table(df=S_Diff_table_quarry,table_num=S_Diff_table_quarry.table_num,caption="Sediment yield from subwatersheds in Faga'alu",fontsize=9)
#document.add_paragraph("Storm on 2/3/12 has a potential outlier at DT at beginning of storm, which makes the SSYquarry huge! Storm at 2/5/12 doesn't have adequate SSC samples for quarry and its a multipeaked event so the SSY doesn't fall back to low levels like the LBJ and DAM T data suggest it should. Storm 3/6/13 looks like may have missed the second peak but the data looks comparable between sites. Storm 4/16/13 doesn't have alot of points but maybe they're adequate? Storm 4/23/13 looks good. Storm 4/30/13 has inadequate SSC data for all locations after the first peak; can maybe change the storm interval? Storm 6/5/13 has inadequate SSC data for all locations for the first peak, decent data for LBJ and DT for second peak but not for DAM; can maybe change the storm interval? Storm 2/14/14 looks good. Storm 2/20/14 looks good. Storm 2/21/14 looks good. Storm 2/27/14 looks kinda shitty. So good storms are: 3/6/13, 4/16/13? 4/23/13, 4/30/13?, 6/5/13?, 2/14/14, 2/20/14, 2/21/14") 

document.add_paragraph("SSY at FG3 was "+SSY_TOTAL_3+" tons, averaging "+Percent_UPPER_S_3+"% from the UPPER subwatershed, "+Percent_QUARRY_S+"% from LOWER_QUARRY subwatershed, and "+Percent_VILLAGE_S+"% from the LOWER_VILLAGE subwatershed (Table "+S_Diff_table_quarry.table_num+"). sSSY from the UPPER, LOWER_QUARRY, and LOWER_VILLAGE subwatersheds and TOTAL watershed was "+sSSY_UPPER_3+", "+sSSY_LOWER_QUARRY+", "+sSSY_LOWER_VILLAGE+", and "+sSSY_TOTAL_3+", respectively. sSSY from LOWER_QUARRY and LOWER_VILLAGE was "+S_Diff_table_quarry['LOWER_QUARRY tons']['DR']+" and "+S_Diff_table_quarry['LOWER_VILLAGE tons']['DR']+" times higher, respectively, than sSSY from UPPER subwatershed, suggesting human disturbance has significantly increased SSY over natural levels, particularly at the quarry. sSSY from the TOTAL watershed was "+S_Diff_table_quarry['TOTAL tons']['DR']+" times higher than the UPPER subwatershed, similar to the larger range of storms in Table "+S_Diff_table.table_num+", where specific SSY was "+S_Diff_table['TOTAL tons']['DR']+" times higher.")

document.add_paragraph("SSY from undisturbed areas in the LOWER_QUARRY and LOWER_VILLAGE subwatersheds was: "+S_Diff_table_quarry['LOWER_QUARRY tons']['SSY from forested areas (tons)']+" and "+S_Diff_table_quarry['LOWER_VILLAGE tons']['SSY from forested areas (tons)']+" tons, respectively. SSY from the "+"%0.3f"%disturbed_area_LOWER_QUARRY+" km2 and "+"%0.3f"%disturbed_area_LOWER_VILLAGE+" km2 of disturbed areas in the LOWER_QUARRY and LOWER_VILLAGE subwatersheds was "+S_Diff_table_quarry['LOWER_QUARRY tons']['SSY from disturbed areas (tons)']+" and "+S_Diff_table_quarry['LOWER_VILLAGE tons']['SSY from disturbed areas (tons)']+" tons, respectively. SSY from the disturbed areas accounted for "+S_Diff_table_quarry['LOWER_QUARRY tons']['% SSY from disturbed areas']+"% and "+S_Diff_table_quarry['LOWER_VILLAGE tons']['% SSY from disturbed areas']+"% of total SSY from those watersheds, respectively. sSSY from disturbed areas in the UPPER, LOWER_QUARRY, and LOWER_VILLAGE subwatersheds was "+S_Diff_table_quarry['UPPER tons']['sSSY from disturbed areas (tons/km2)']+", "+S_Diff_table_quarry['LOWER_QUARRY tons']['sSSY from disturbed areas (tons/km2)']+", and "+S_Diff_table_quarry['LOWER_VILLAGE tons']['sSSY from disturbed areas (tons/km2)']+", respectively, suggesting that disturbed areas increase sSSY over forested conditions by "+S_Diff_table_quarry['LOWER_QUARRY tons']['DR for sSSY from disturbed areas']+"x and "+S_Diff_table_quarry['LOWER_VILLAGE tons']['DR for sSSY from disturbed areas']+"x in the LOWER_QUARRY and LOWER_VILLAGE subwatersheds, respectively. Bare land area in the LOWER_QUARRY subwatershed clearly increases sSSY significantly, and contributes the majority of SSY from disturbed areas in Faga'alu watershed. Human disturbance in the LOWER_VILLAGE subwatershed also increases SSY above natural levels but the magnitude of disturbance is much lower than the quarry.")

document.add_paragraph("A very small fraction of the watershed accounts for the majority of the sediment load. Roughly "+S_Diff_table_quarry['LOWER_QUARRY tons']['% SSY from disturbed areas']+"% and "+S_Diff_table_quarry['LOWER_VILLAGE tons']['% SSY from disturbed areas']+"% of SSY from the LOWER_QUARRY and LOWER_VILLAGE subwatersheds, respectively, is from disturbed areas, despite the disturbed areas only accounting for "+S_Diff_table_quarry['LOWER_QUARRY tons']['fraction disturbed (%)']+"% and "+S_Diff_table_quarry['LOWER_VILLAGE tons']['fraction disturbed (%)']+"% of the subwatershed area, respectively. Similarly, despite only "+S_Diff_table_quarry['TOTAL tons']['fraction disturbed (%)']+"% of the TOTAL watershed being disturbed, SSY from disturbed areas accounts for "+S_Diff_table_quarry.ix['% SSY from disturbed areas']['TOTAL tons']+"% of the SSY from the TOTAL watershed.")

## Summary Q, S, and DR table
#if 'Q_S_Diff_summary_table' in locals():
#    dataframe_to_table(df=Q_S_Diff_summary_table,table_num=Q_S_Diff_summary_table.table_num,caption="Total Q and SSY",fontsize=11)
#    
    
#### Fitting SSY models
document.add_heading('Predicting SSYEV from storm metrics',level=3)
document.add_paragraph("sSSYEV from the UPPER and TOTAL watersheds correlated with each of the four storm metrics (Figure "+SSY_models_ALL['fig_num']+"). Significant scatter was observed for all models, which reflects the changing sediment availability and natural variability in the watershed response for different storm events. In all models, sSSYEV from the TOTAL watershed was higher than the UPPER subwatershed for the full range of measured storms with the exception of a few events that are considered outliers. These events could be attributed to measurement error but are likely related to landsliding events in the UPPER subwatershed and the increased sediment supply for that specific event. Storm sequence and antecedent conditions may also play a role. While the climate on Tutuila is tropical, without strong seasonality, periods of low rainfall can persist for several weeks, altering the water and sediment dynamics in the subsequent storm events.")

if 'SSY_models_ALL' in locals():
    document.add_picture(SSY_models_ALL['filename']+'.png',width=Inches(6))
    add_figure_caption(SSY_models_ALL['fig_num'],"SSY rating curves for predictors. Each point represents a different storm event.")
## Power law models from ALLStorms_ALLRatings 
PS_upper,PS_total,EI_upper,EI_total, QsumS_upper,QsumS_total,QmaxS_upper,QmaxS_total=ALLStorms_ALLRatings

document.add_paragraph("Pearson and Spearman correlation coefficients were fairly similar, meaning the relationships were mostly linear in log-log space. The exception was Qmax for the UPPER subwatershed (Pearson's: "+"%.2f"%QmaxS_upper.pearson+" vs. Spearman's: "+"%.2f"%QmaxS_upper.spearman+"). Only EI30 had a higher Pearson's correlation coefficient than Spearman's, but both were low (Pearson's: "+"%.2f"%EI_total.pearson+" vs. Spearman's: "+"%.2f"%EI_total.spearman+").")

document.add_paragraph("Precipitation metrics (Psum and EI30) showed lower correlation coefficients with SSYEV compared to the discharge metrics (Qsum and Qmax) over the full range of storm sizes. SSYEV is calculated from measured Q so it is expected that discharge metrics are more closely correlated, and has been observed in other studies (Rankl, Duvert etc.). EI30 was the least correlated with SSYEV of the storm metrics. No statistically significant correlations (p<0.01) were found between SSY and EI30 for the UPPER subwatershed using Pearson's or Spearman's coefficients, and the statistically significant correlations between SSY and EI30 for the total watershed were the lowest of all storm metrics. ")

# Pearson's and Spearman's correlation coeffs and r2 and RMSE
#document.add_paragraph("Pearson's correlation coefficients...")
if 'SSYEV_models_stats' in locals():
    dataframe_to_table(df=SSYEV_models_stats,table_num=SSYEV_models_stats.table_num,caption="Model statistics")

## Comparing precipitation vs discharge correlations
document.add_paragraph("Discharge metrics showed much higher correlation coefficients than the precipitation metrics in the UPPER subwatershed, but had similar coefficients in the LOWER watershed. This suggests that sediment production processes are more related to discharge processes in the UPPER subwatershed, and more related to precipitation processes in the LOWER subwatershed, influencing the correlation coefficients for the TOTAL watershed. SSY from the LOWER subwatershed is hypothesized to be mostly generated by surface erosion at the quarry, dirt roads, and agricultural plots, whereas SSY from the UPPER subwatershed is hypothesized to be mainly from channel processes and mass wasting. Mass wasting can contribute large pulses of sediment during large precipitation events, which can be deposited near or in the streams and entrained at high discharges during later events. Given the high correlation coefficients for Qmax in both subwatersheds, Qmax may be a promising predictor that integrates both precipitation and discharge processes.")
## Best SSYEV model
document.add_paragraph("The best model fit according to the coefficient of determination (r2) and RMSE was found with Qmax for both UPPER and TOTAL watersheds. The model fit for Qsum for the UPPER subwatershed was equally high but the Qmax model has the highest r2 for both watersheds, the lowest RMSE, and the highest correlation coefficients. Therefore Qmax was selected as the best predictor of SSYEV for both the UPPER and TOTAL watersheds in Faga'alu.")  
## reword^

## Storm size
document.add_paragraph("In the LOWER subwatershed the higher Qmax-SSYEV relationship is attributed to the additional sediment yields from human-disturbed areas in the quarry and village. If Qmax-SSYEV models converge at higher Qmax values, it indicates diminishing human disturbance for large storms. It was hypothesized that for large storms, SSYEV from the Upper watershed may become the dominant source of total SSY to Faga'alu Bay, however, the results based on all of the models are unclear. Since correlation coefficients and model fits indicated EI30 was a poor predictor, it is ignored. The Psum-SSYEV models indicate that for larger storm events the SSY contributions from the Upper and Lower watersheds are more similar. Conversely, the Qsum- and Qmax-SSYEV models show no change in relative contributions of SSY over the range of storm sizes (Figure "+SSY_models_ALL['fig_num']+").  In that case, the discharge models (Qsum and Qmax) support the conclusion that human disturbance does not diminish with storm size, while the Psum model supports the conclusion that it does diminsh with storm size. ")


document.add_paragraph("Other studies have documented one to several order of magnitude increases in SSY from small disturbances in small, mountainous watersheds. On Molokai, Stock et al. (2010) found that less than 5% of the land produces most of the sediment, and of that 5%, only 1% produces ~50% of the sediment (Risk, 2014). In three basins on St.John with varying levels of development, Ramos-Scharron et al (2005) found unpaved roads increased sediment delivery rates by 3-6 times for Lameshur Bay, 5-9 times for Fish Bay, and  4-8 times for Cinnamon Bay. Disturbances at larger scales have had similar increases in total SSY to coral environments. The development of the Great Barrier Reef (GBR) catchment since European settlement (ca.1830) led to increases in SSY by an estimated factor of 5.5 (Kroon et al.,2012).")

document.add_paragraph("Annual estimates of SSY and sSSY are most commonly used to compare watersheds, however, a continuous annual time-series of SSY was not possible at the study site due to the discontinuous field sampling trips. However, a continuous discharge record for 2014 at FG1 could be used to estimate annual SSY from storm events, using the Qmax-SSY relationships. For storms with no Qmax data at FG3, Qmax was predicted from a linear regression between Qmax at FG1 and Qmax at FG3 for the study period. For storms with no SSC data, SSYUPPER and SSYTOTAL were predicted using the Qmax-SSY relationships developed above (Table "+Annual_SSY_tables.table_num+"). Continuous Q and Precip data showed that "+P_2014+" mm of precipitation fell during storms identified by the stage threshold method, representing "+P_2014_perc_ann+"% of annual Precip measured in 2014 (="+"%.0f"%PrecipFilled[start2014:stop2014].sum()+"). This implies that "+"%.0f"%(100-float(P_2014_perc_ann))+"% of Precip did not cause a rise in streamflow high enough to exceed the defined storm threshold, and considering most SSY is discharged during few, relatively large events, it is assumed it does not affect annual SSY estimates (Stock and Tribble, 2009).")

def times(x,factor,round_to):
    return int(int(round(int(factor*float(x))/float(round_to)))* float(round_to))
## Annual SSY and sSSY from Table 2 (UPPER and LOWER)
# from Table 2
annual_SSY_UPPER_2, annual_sSSY_UPPER_2 = "%.0f"%times(SSY_UPPER_2,2,10)+"-"+"%.0f"%times(SSY_UPPER_2,3,10), "%.0f"%times(sSSY_UPPER_2,2,10)+"-"+"%.0f"%times(sSSY_UPPER_2,3,10)
annual_SSY_LOWER_2, annual_sSSY_LOWER_2 = "%.0f"%times(SSY_LOWER_2,3,10)+"-"+"%.0f"%times(SSY_LOWER_2,3,10), "%.0f"%times(sSSY_LOWER_2,2,10)+"-"+"%.0f"%times(sSSY_LOWER_2,3,10)
annual_SSY_TOTAL_2, annual_sSSY_TOTAL_2 ="%.0f"%times(SSY_TOTAL_2,3,10)+"-"+"%.0f"%times(SSY_TOTAL_2,3,10), "%.0f"%times(sSSY_TOTAL_2,2,10)+"-"+"%.0f"%times(sSSY_TOTAL_2,3,10)

document.add_paragraph("SSY from the UPPER and LOWER subwatersheds was "+SSY_UPPER_2+" and "+SSY_LOWER_2+" tons, respectively and sSSY from the UPPER and LOWER subwatersheds was "+sSSY_UPPER_2+" and "+sSSY_LOWER_2+" tons/km2, respectively for the storms with turbidity measurements (Table "+S_Diff_table.table_num+"), which had a total precipitation of "+P_measured_2+" mm. Annual storm precipitation is roughly 2-3 times the precipitation measured during these storms, so annual SSY and sSSY are estimated to be roughly 2-3 times the measured SSY and sSSY: "+annual_SSY_UPPER_2+" tons/year, and  "+annual_sSSY_UPPER_2+" tons/km2/year for the UPPER subwatershed, and "+annual_SSY_LOWER_2+" tons/year, and "+annual_sSSY_LOWER_2+" tons/km2/year for the UPPER subwatershed. SSY and sSSY from the TOTAL watershed was "+SSY_TOTAL_2+" tons and "+sSSY_TOTAL_2+" tons/km2, respectively, so annual SSY and sSSY are estimated to be "+annual_SSY_TOTAL_2+" tons/year, and  "+annual_sSSY_TOTAL_2+" tons/km2/year.") 

## Annual SSY and sSSY from Table 3 (UPPER and LOWER_QUARRY, LOWER_VILLAGE)
# from Table 3
annual_SSY_UPPER_3, annual_sSSY_UPPER_3 = "%.0f"%times(SSY_UPPER_3,4,10)+"-"+"%.0f"%times(SSY_UPPER_3,5,10), "%.0f"%times(sSSY_UPPER_3,4,10)+"-"+"%.0f"%times(sSSY_UPPER_3,5,10)
annual_SSY_LOWER_3, annual_sSSY_LOWER_3 = "%.0f"%times(float(SSY_LOWER_QUARRY)+float(SSY_LOWER_VILLAGE),4,10)+"-"+"%.0f"%times(float(SSY_LOWER_QUARRY)+float(SSY_LOWER_VILLAGE),5,10), "%.0f"%times((float(SSY_LOWER_QUARRY)+float(SSY_LOWER_VILLAGE))/0.88,4,10)+"-"+"%.0f"%times((float(SSY_LOWER_QUARRY)+float(SSY_LOWER_VILLAGE))/0.88,5,10)

annual_SSY_LOWER_QUARRY_3, annual_sSSY_LOWER_QUARRY_3 = "%.0f"%times(SSY_LOWER_QUARRY,4,10)+"-"+"%.0f"%times(SSY_LOWER_QUARRY,5,10), "%.0f"%times(sSSY_LOWER_QUARRY,4,10)+"-"+"%.0f"%times(sSSY_LOWER_QUARRY,5,10)
annual_SSY_LOWER_VILLAGE_3, annual_sSSY_LOWER_VILLAGE_3 = "%.0f"%times(SSY_LOWER_VILLAGE,4,10)+"-"+"%.0f"%times(SSY_LOWER_VILLAGE,5,10), "%.0f"%times(sSSY_LOWER_VILLAGE,4,10)+"-"+"%.0f"%times(sSSY_LOWER_VILLAGE,5,10)
annual_SSY_TOTAL_3, annual_sSSY_TOTAL_3 ="%.0f"%times(SSY_TOTAL_3,4,10)+"-"+"%.0f"%times(SSY_TOTAL_3,5,10), "%.0f"%times(sSSY_TOTAL_3,4,10)+"-"+"%.0f"%times(sSSY_TOTAL_3,5,10)

LOWER_QUARRY_disturbed_fraction = S_Diff_table_quarry['LOWER_QUARRY tons']['fraction disturbed (%)']
sSSY_disturbed_LOWER_QUARRY_3 = S_Diff_table_quarry['LOWER_QUARRY tons']['sSSY from disturbed areas (tons/km2)']
annual_sSSY_disturbed_LOWER_QUARRY_3 = "%.0f"%times(S_Diff_table_quarry['LOWER_QUARRY tons']['sSSY from disturbed areas (tons/km2)'],4,100)+"-"+"%.0f"%times(S_Diff_table_quarry['LOWER_QUARRY tons']['sSSY from disturbed areas (tons/km2)'],5,100)

#For the storms totaling "+P_measured_3+" mm of precipitation measured in , 

document.add_paragraph("SSY from the UPPER, LOWER_QUARRY, and LOWER_VILLAGE subwatersheds was "+SSY_UPPER_3+", "+SSY_LOWER_QUARRY+", and "+SSY_LOWER_VILLAGE+" tons, respectively, and sSSY from the UPPER, LOWER_QUARRY, and LOWER_VILLAGE subwatersheds was "+sSSY_UPPER_3+", "+sSSY_LOWER_QUARRY+", and "+sSSY_LOWER_VILLAGE+" tons/km2, respectively for the storms which had grab samples of SSC at FG2 (Table "+S_Diff_table_quarry.table_num+"), which had a total "+P_measured_3+" mm of precipitation. Annual storm precipitation is 3,800 mm, or roughly 4-5 times the precipitation measured for these storms, so annual SSY and sSSY are estimated to be roughly 4-5 times the measured SSY and sSSY, assuming that the sediment yield per mm of precipitation is constant over the year. Annual SSY from the UPPER, LOWER_QUARRY, and LOWER_VILLAGE subwatersheds was estimated to be "+annual_SSY_UPPER_3+", "+annual_SSY_LOWER_QUARRY_3+", and "+annual_SSY_LOWER_VILLAGE_3+" tons/year, respectively. Annual sSSY from the UPPER, LOWER_QUARRY, and LOWER_VILLAGE subwatersheds was estimated to be "+annual_sSSY_UPPER_3+", "+annual_sSSY_LOWER_QUARRY_3+", and "+annual_sSSY_LOWER_VILLAGE_3+" tons/km2/year, respectively. SSY and sSSY from the TOTAL watershed was "+SSY_TOTAL_3+" tons and "+sSSY_TOTAL_3+" tons/km2, respectively, so annual SSY and sSSY are estimated to be "+annual_SSY_TOTAL_3+" tons/year, and "+annual_sSSY_TOTAL_3+" tons/km2/year. sSSY from the disturbed fraction ("+LOWER_QUARRY_disturbed_fraction+"%) of the LOWER_QUARRY subwatershed ("+"%0.2f"%Area_LOWER_QUARRY+" km2) was "+sSSY_disturbed_LOWER_QUARRY_3+" tons/km2 for the "+P_measured_3+" mm of precipitation during the measured storms (roughly 12-15% of annual precipitation). Annual sSSY from the disturbed quarry was approximately "+annual_sSSY_disturbed_LOWER_QUARRY_3+" tons/km2/year. The quarry surfaces are comprised of haul roads, piles of overburden, and steep rock faces, which can be described as a mix of unpaved roads and cut-slopes. Ramos-Scharron and McDonald (2007) measured sSSY of 570-580,000 tons/km2/yr from unpaved roads with slopes from  2-21%, and sSSY of 2,000-17,000 tons/km2/yr from cutslopes. Other literature measured sSSY from cutslopes varying from 10-105,000 tons/km2/yr. The sSSY ranges measured in this study are well within the ranges found in the literature.")

## Annual SSY and sSSY from full range of measured storms
P_FG1_all_storms, P_FG1_percent_annual = SedFluxStorms_DAM[['Ssum','Psum']].dropna()['Psum'].sum(), SedFluxStorms_DAM[['Ssum','Psum']].dropna()['Psum'].sum()/4000 * 100
annual_SSY_UPPER_ALL = SedFluxStorms_DAM[['Ssum','Psum']].dropna()['Ssum'].sum() + ((1-P_FG1_percent_annual/100) * SedFluxStorms_DAM[['Ssum','Psum']].dropna()['Ssum'].sum())
annual_sSSY_UPPER_ALL = annual_SSY_UPPER_ALL/0.90

P_FG3_all_storms, P_FG3_percent_annual = SedFluxStorms_LBJ[['Ssum','Psum']].dropna()['Psum'].sum(), SedFluxStorms_LBJ[['Ssum','Psum']].dropna()['Psum'].sum()/4000 * 100
annual_SSY_TOTAL_ALL = SedFluxStorms_LBJ[['Ssum','Psum']].dropna()['Ssum'].sum() + ((1-P_FG3_percent_annual/100) * SedFluxStorms_LBJ[['Ssum','Psum']].dropna()['Ssum'].sum())
annual_sSSY_TOTAL_ALL =annual_SSY_TOTAL_ALL/1.78

document.add_paragraph("Tables 2 and 3 include only storms with SSY data at both FG1 and FG3 (Table 2), and at FG1, FG2 and FG3 (Table 3). Using all SSY data measured at FG1 (SSYUPPER), SSY for "+"%.0f"%P_FG1_percent_annual+"% of annual precipitation ("+"%0.f"%P_FG1_all_storms+" mm) of precipitation (~4,000 mm) were measured. Storm data for Table 2 and 3 Annual SSY from the UPPER subwatershed was estimated from Table 2 and Table 3 to be "+annual_SSY_UPPER_2+" tons/yr and "+annual_SSY_UPPER_3+" tons/yr, respectively.  Using all SSY data measured at FG1 (SSYUPPER), SSY for "+"%.0f"%P_FG3_percent_annual+"% of annual precipitation ("+"%0.f"%P_FG3_all_storms+" mm) of precipitation (~4,000 mm) were measured. Annual SSY from the UPPER subwatershed was estimated from Table 2 and Table 3 to be "+annual_SSY_TOTAL_2+" and "+annual_SSY_TOTAL_3+", respectively")  

if 'Annual_SSY_tables' in locals():
    dataframe_to_table(df=Annual_SSY_tables()[0],table_num=Annual_SSY_tables.table_num,caption="Annual SSY estimates")
    dataframe_to_table(df=Annual_SSY_tables()[1],table_num='',caption="Annual sSSY estimates")

### DISCUSSION
document.add_heading('Discussion',level=2)

## Methods for quantifying human impact
document.add_heading('Methods for quantifying human impact',level=3)
document.add_heading("In contrast to other methods like traditional sediment rating curve or the traditional sediment budget, event-wise correlation of SSY and storm metrics was advantageous in small watersheds with hysteresis in Q-SSC relationship. ")


## Assessing alpha and Beta model parameters
document.add_heading('Interpreting slope and intercept of the Qmax-SSY relationship',level=3)
ratings_table = ALLRatings_table()
alpha_upper, beta_upper = ratings_table['alpha'].loc['Qmax_upper'], ratings_table['Beta'].loc['Qmax_upper']
alpha_total, beta_total = ratings_table['alpha'].loc['Qmax_total'], ratings_table['Beta'].loc['Qmax_total']

document.add_paragraph("Several researchers have attempted to explain the difference in alpha (intercept) and Beta (slope) coefficients according to watershed characteristics. A traditional sediment rating curve (Q-SSC) is considered a 'black box' model, and the alpha and Beta coefficients have no physical meaning. However, some physical interpretation has been ascribed to them, with the alpha coefficient representing erosion severity, and the Beta coefficient representing the erosive power of the river. High alpha values suggest high availability of easily eroded sediment sources in the watershed, and high Beta values suggest that a small change in stream discharge leads to a large increase in sediment load due to the erosive power of the river or the extent that new sediment sources become available as discharge increases (Asselman, 2000). Similar analysis has been done on event-based sediment yield curves (Qmax-SSYEV models). Rankl (2004) found that Beta coefficients were not statistically different between watersheds, and he assumed that the Beta exponent was a function of rainfall intensity on hillslopes. Rankl (2004) hypothesized that variability in alpha (the intercept) was a function of sediment availability and erodibility in watersheds, but Duvert et al. (2012) argued that alpha values are also dependent on the regression fitting method, arguing that, for instance, the Nonlinear method results in a model fit to higher SSY values at lower discharge compared to Linear methods.")

document.add_paragraph("Duvert (2012) compiled Qmax-SSY results from twenty-eight watersheds (0.45-1,538km2) and found Beta coefficients (slope in the log-log plots) that ranged from 1.06-2.45, and alpha coefficients (intercepts in the log-log plots) that ranged from 25-5039. The alpha coefficients for the Qmax-SSYEV models in Faga'alu were "+alpha_upper+" and "+alpha_total+", and Beta coefficients were " +beta_upper+" and "+beta_total+" in the UPPER and TOTAL Faga'alu watersheds, respectively. The Beta coefficient values are very consistent with the watersheds presented in Duvert 2012, but the alpha coefficient values are an order of magnitude lower than the lowest values in Duvert (2012). This suggests that sediment availability is relatively low in Faga'alu, likely due to the dense forest cover over the majority of the watershed.")

document.add_paragraph("Duvert et al. (2012) also found low correlation coefficients with 5 min rainfall intensity for 8 watersheds in France and Mexico. Rodrigues et al. (2013) hypothesized that EI30 is poorly correlated with SSY due to the effect of previous events on antecedent moisture conditions and in-channel sediment storage. Similar to other studies (Duvert et al., 2012; Rodrigues, Basher, Fahey, Rankl CITATION) the highest correlations were observed for discharge metrics, particularly Qmax which had the highest overall correlation with a Spearman correlation coefficient of "+"%.2f"%QmaxS_upper.spearman+" for the Upper watershed and "+"%.2f"%QmaxS_total.spearman+" for the Total watershed.")

## compare sSSY and SSC with other watersheds
document.add_heading('Comparing sSSY and mean/max SSC in other small Pacific Island watersheds',level=3)

document.add_paragraph("Sediment yield is generally controlled by climate and geology, with human disturbance playing an increasing role in the 20th century. Sediment yields in tropical Southeast Asia range from 10,000 tons/km2/yr in the tectonically active, steeply sloped island of Papua New Guinea to ~10 tons/km2/yr in the granitic Malaysian Peninsula (Douglas 1996).")

document.add_paragraph("In similar watersheds in Kauai and Molokai, Stock and Tribble (2009) found the Hanalei samples had an average SSC of 63 mg/L, with a maximum value of 2,750 mg/l (at an instantaneous flow of 14,100 cfs); the Kawela samples had an average SSC of 3,490 mg/L, with a maximum value of 54,000 mg/l (at an instantaneous flow of 1,614 l/sec).")

document.add_paragraph("Ramos-Scharron and McDonald (2007) measured sSSY of 570-580,000 tons/km2/yr from unpaved roads with slopes from  2-21%, and sSSY of 2,000-17,000 tons/km2/yr from cutslopes. Other literature measured sSSY from cutslopes varying from 10-105,000 tons/km2/yr. The sSSY ranges measured in this study are well within the ranges found in the literature.")

document.add_paragraph("Data in Milliman and Syvitski (1992) suggests there is unusually high average sSSY for watersheds (10-100,000 km2) on high-standing, South Pacific Islands on the order of 1,000-3,000 tons/km2/year, however, they acknowledge the role of sediment erodibility and effects of geology, vegetation cover and human activity. Given the high vegetation cover and lack of human activity in the UPPER subwatershed, it is assumed that specific SSY should be several orders of magnitude lower than watersheds presented in Milliman and Syvitski (1992). Models to estimate sSSY from basin area and maximum elevation in Oceania for the UPPER subwatershed (Milliman and Syvitski, 1992) predict 13 tons/km2/year for watersheds 500-1,000m and 68 tons/km2/year for max elevations of 1,000-3,000 m. SSY and sSSY from the UPPER subwatershed is higher than predicted by Milliman and Syvitski's (1992) model but it is also a smaller watershed than they included in their analysis, and high scatter above their model is observed for smaller watersheds in their Figures 5e and 6e. In Hanalei watershed, a larger watershed (54 km2) which has similarly steep relief and high rainfall (2,000-11,000 mm), Calhoun and Fletcher (1999) and  Stock and Tribble (2010) estimated sSSY was 140 plus-minus55 tons/km2/year and 525 tons/km2/yr, respectively. In Kawela watershed (14 km2), a similaryly disturbed, sub-humid watershed (500-3,000 mm precipitation) on Molokai, Stock and Tribble estimated sSSY was 459 tons/km2/yr. In comparison to these larger watersheds, the sSSY from the UPPER watershed Faga'alu is an order of magnitude lower, but it is similar in the LOWER subwatershed where human disturbance has significantly increased SSY.")

## compare with other kinds of disturbance
document.add_heading('Comparison with other kinds  of sediment disturbance', level=3)
document.add_paragraph("In contrast to other land disturbances like fire, logging, or urbanization where sediment disturbance decreases over time, the disturbance from mining is persistently high. Disturbance magnitudes are similar to the construction phase of urbanization (Wolman), or high-traffic unpaved roads (Reid and Dunne), but persist or even increase over time.") 

document.add_paragraph("Mining activity has been a major contributor of sediment in other watersheds, (refs) including volcanic islands with steep topography and high rainfall (Fly River, etc).  ...Urbanization and mining increase sediment yield in stable terrain by tow to three orders of magnitudes in catchments of several km2 but yields from construction sites can exceed those from the most unstable tectonically active natural envrionments of SE Asia (Douglas 1996). ")
## Is the 3.8x increase big or small compared with others?

## How does the yield from the quarry differ from other studies (e.g. Wolman 1967, but also look up others)?  




#document.add_paragraph("Stock and Tribble (2009): Given a saprolite bulk density of 1.2 t/m3, the average annual suspended load at Hanalei represents a basin-wide lowering rate of 0.44 mm/a, and that of Kawela a rate of 0.33 mm/a. For soil bulk densities of 0.95 t/m3, Hanalei basin surface lowering is 0.56 mm/a, and that of Kawela basin is 0.42. Bedrock densities of 3.0 t/m3 result in Hanalei lowering rates of 0.18 mm/a, and Kawela lowering rates of 0.13 mm/a")


#### CONCLUSION
conclusion_title=document.add_heading('Conclusion',level=2)
conclusion_text = document.add_paragraph("Human disturbance has increased sediment yield to Faga'alu Bay by "+S_Diff_table['TOTAL tons']['DR']+"x over pre-disturbance levels. The human-disturbed subwatershed accounted for the majority (85%) of total sediment yield, and the quarry was shown to be the most significant sediment source in the watershed, contributing about half of total SSY to the Bay. The relative contribution from the human-disturbed watershed was hypothesized to diminish with increasing storm size but the results from precipitation metrics and discharge metrics were contradictory. The Psum-SSYEV model showed that the relative contribution of SSYEV from the human-disturbed watershed decreases with storm size, but the Qmax-SSYEV model shows no change in relative contributions over increasing storm size.")

conclusion_text = document.add_paragraph("Qmax was the best predictor of SSY. The slopes of the Qmax-SSYEV relationships were comparable with other studies, but the alpha coefficients were an order of magnitude lower than other semi-arid to semi-humid waterhseds in the literature, suggesting that sediment availability is relatively low in the heavily forested Faga'alu watershed.")
#Also on volcanic rock, not uplifted sedimetns.  Rw to mention that.  Other literature suggests that SSY is a function of rock type?


## Introduce the post-mitigation work
document.add_paragraph("Management has responded to data on sediment loading in Faga'alu. In August 2012, preliminary results of the significant SSYEV contributions from the quarry and its impact on coral reef health in the Bay were communicated to US Federal and local environmental management and conservation groups including the Faga'alu village community, NOAA Coral Reef Conservation Program, American Samoa Environmental Protection Agency, and the American Samoa Coral Reef Advisory Group. In February 2013, Faga'alu watershed was designated by the US Coral Reef Task Force as a Priority Watershed Restoration site, with the main objective to reduce sediment yields to the adjacent coral reefs. These groups developed a sediment management plan for the quarry operators and village residents. The sediment runoff management plan for the quarry was implemented in October 1, 2014, and completed in December 2014. Storm monitoring is currently in progress and results documenting the successful reduction of sediment yields to the Bay will be presented in a forthcoming paper. This work provides an example of a successful environmental management project which could only be accomplished by the effective partnerships between community groups, local industries, educational institutions, and government regulatory and funding agencies.")


#### Appendix 1
document.add_page_break()
document.add_heading('APPENDIX 1. Channel cross sections',level=2)

if 'LBJ_Cross_Section' in locals():
    document.add_picture(LBJ_Cross_Section['filename']+'.png',width=Inches(6))
    add_figure_caption(LBJ_Cross_Section['fig_num'],"Stream cross-section at FG1")
if 'DAM_Cross_Section' in locals():  
    document.add_picture(DAM_Cross_Section['filename']+'.png',width=Inches(6))
    add_figure_caption(DAM_Cross_Section['fig_num'],"Stream cross-section at FG3")
    
#### Appendix 2
document.add_page_break()
document.add_heading("APPENDIX 2. Dams in Faga'alu watershed",level=2)

## Fagaalu Reservoir Infrastructure
document.add_paragraph("Faga'alu, like many watersheds on Pacific high islands, is characterized by large areas of undisturbed, steeply-sloped, forested hillsides in the upper watershed, and relatively little flat area in the lower watershed that is urbanized or densely settled (Figure 1). Faga'alu is a narrow, V-shaped watershed covering approximately 2.48 km2 from Mt. Matafao, the highest point on Tutuila (653 m), to its' outlet at the Pacific Ocean. Small tributaries from the hillsides feed a single perennial stream which runs the length of the watershed (~3 km), and drains an area of 1.86 km2. Several small ephemeral streams drain the lower portions of the watershed (0.63km2) directly to the ocean.")

document.add_paragraph("Faga'alu stream was dammed at 4 locations above the village: 1) Matafao Dam (elevation 244 m) near the base of Mt. Matafao, draining 0.20 km2, 2) Vaitanoa Dam at Virgin Falls (elevation 140 m), draining an additional 0.44 km2, 3) a small unnamed dam below Vaitanoa Dam at elevation 100m, and 4) Lower Faga'alu Dam (elevation 48 m), immediately upstream of a large waterfall 30 m upstream of the quarry, draining an additional 0.26 km2 (Tonkin & Taylor International Ltd. 1989). A 2012 aerial LiDAR survey (Photo Science, Inc.) indicates the drainage area at the Lower Faga'alu Dam is 0.90 km2. A small stream capture/reservoir (~35 m3) is also present on a side tributary that joins Faga'alu stream on the south bank, opposite the quarry. It is connected to a ~6 cm diameter pipe but it is unknown when or by whom it was built, its initial capacity, or if it is still conveying water. During all site visits water was overtopping this small structure through the spillway crest, suggesting it is fed by a perennial stream.")

document.add_paragraph("Matafao Dam was constructed in 1917 for water supply to the Pago Pago Navy base, impounding a reservoir with initial capacity of 1.7 million gallons (6,400 m3) and piping the flow out of the watershed to a hydropower and water filtration plant in Fagatogo. In the early 1940's the Navy replaced the original cement tube pipeline and hydropower house with cast iron pipe but it is unknown when the scheme fell out of use (Tonkin & Taylor International Ltd. 1989; URS Company 1978). Remote sensing and a site visit on 6/21/13 confirmed the reservoir is still filling to the spillway crest with water and routing some flow to the Fagatogo site, though the amount is much less than the 10 in. diameter pipes conveyance capacity and the flow rate variability is unknown. A previous site visit on 2/21/13 by American Samoa Power Authority (ASPA) found the reservoir empty of water but filled with an estimated 3-5 meters of fine sediment (Kearns 2013). Interviews with local maintenance staff and historical photos confirmed the Matafao Reservoir was actively maintained and cleaned of sediment until the early 70's.")

document.add_paragraph("The Vaitanoa (Virgin Falls) Dam, was built in 1964 to provide drinking water but the pipe was not completed as of 10/19/89, and a stockpile of some 40 (8 ft length) 8 in. diameter asbestos-cement pipes was found on the streambanks. Local quarry staff recall the pipes were removed from the site some time in the 1990's. The Vaitanoa Reservoir had a design volume of 4.5 million gallons (17,000m3), but is assumed to be full of sediment since the drainage valves were never opened and the reservoir was overtopping the spillway as of 10/18/89 (Tonkin & Taylor International Ltd. 1989). A low masonry weir was also constructed downstream of the Vaitanoa Dam, but not connected to any piping.") 

document.add_paragraph("The Lower Faga'alu Dam was constructed in 1966/67 just above the Samoa Maritime, Ltd. Quarry, as a source of water for the LBJ Medical Centre. It is unknown when this dam went out of use but in 1989 the 8 in. conveyance pipe was badly leaking and presumed out of service. The 8 in. pipe disappears below the floor of the Samoa Maritime quarry and it is unknown if it is still conveying water or has plugged with sediment. The derelict filtration plant at the entrance to the quarry was disconnected prior to 1989 (Tonkin & Taylor International Ltd. 1989). The original capacity was 0.03 million gallons (114 m3) but is now full of coarse sediment up to the spillway crest. No reports were found indicating this structure was ever emptied of sediment.") 

#### Appendix 3
document.add_page_break()
document.add_heading("APPENDIX 3. Water discharge during storm events",level=2)

## Storm Water Discharge
if 'Q_Diff_table' in locals():
    dataframe_to_table(df=Q_Diff_table,table_num=Q_Diff_table.table_num,caption="Water discharge from subwatersheds in Faga'alu",fontsize=9)
## 

#### Appendix 4
document.add_page_break()
document.add_heading("APPENDIX 4. Synthetic rating curves for turbidimeters in Faga'alu",level=2)

## Synthetic Rating Curves Fagaalu
if 'Synthetic_Rating_Curve' in locals():
    document.add_picture(Synthetic_Rating_Curve['filename']+'.png',width=Inches(6)) ## add pic from filename defined above
    add_figure_caption(Synthetic_Rating_Curve['fig_num'],"Synthetic Rating Curves for (a) OBS turbidimeter deployed at FG3 and (b) YSI deployed at FG1.")
    
   
## Save Document
document.save(maindir+'Manuscript/DRAFT-Fagaalu_Sediment_Yield_2015.docx')

## Clean up any open figures
plt.close('all')








