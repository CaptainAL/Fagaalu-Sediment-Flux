# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 12:30:36 2015

@author: Alex
"""
## PEarson and Spearman Coefficient tables with LOWER watershed

def Pearson_r_Table(subset='pre',pvalue=0.05):
    storms_data = compile_storms_data(subset)
    Upper = storms_data[['Pstorms','EI','Qsumupper','Qmaxupper','Supper','Supper_PE']].dropna()
    Lower = storms_data[['Pstorms','EI','Qsumlower','Qmaxlower','Slower']].dropna()
    Total = storms_data[['Pstorms','EI','Qsumtotal','Qmaxtotal','Stotal','Stotal_PE']].dropna()
    ## Psum vs. Ssum
    if pearson_r(Upper['Pstorms'],Upper['Supper'])[1] < pvalue:
        Upper_Psum_Ssum_Pearson_r = '%.2f'%pearson_r(Upper['Pstorms'],Upper['Supper'])[0]
    if pearson_r(Lower['Pstorms'],Lower['Slower'])[1] < pvalue:
        Lower_Psum_Ssum_Pearson_r = '%.2f'%pearson_r(Lower['Pstorms'],Lower['Slower'])[0]
    if pearson_r(Total['Pstorms'],Total['Stotal'])[1] < pvalue:
        Total_Psum_Ssum_Pearson_r = '%.2f'%pearson_r(Total['Pstorms'],Total['Stotal'])[0]      
    ## EI vs. Ssum
    if pearson_r(Upper['EI'],Upper['Supper'])[1] < pvalue:
        Upper_EI_Ssum_Pearson_r = '%.2f'%pearson_r(Upper['EI'],Upper['Supper'])[0]
    elif pearson_r(Upper['EI'],Upper['Supper'])[1] >= pvalue:
        Upper_EI_Ssum_Pearson_r = ' ' 
    if pearson_r(Lower['EI'],Lower['Slower'])[1] < pvalue:
        Lower_EI_Ssum_Pearson_r = '%.2f'%pearson_r(Lower['EI'],Lower['Slower'])[0]
    elif pearson_r(Lower['EI'],Lower['Slower'])[1] >= pvalue:
        Lower_EI_Ssum_Pearson_r = ' ' 
    if pearson_r(Total['EI'],Total['Stotal'])[1] < pvalue:
        Total_EI_Ssum_Pearson_r = '%.2f'%pearson_r(Total['EI'],Total['Stotal'])[0]
    elif pearson_r(Total['EI'],Total['Stotal'])[1] >= pvalue:
        Total_EI_Ssum_Pearson_r = ' ' 
    ## Qsum vs. Ssum
    if pearson_r(Upper['Qsumupper'],Upper['Supper'])[1] < pvalue:
        Upper_Qsum_Ssum_Pearson_r = '%.2f'%pearson_r(Upper['Qsumupper'],Upper['Supper'])[0]
    if pearson_r(Lower['Qsumlower'],Lower['Slower'])[1] < pvalue:
        Lower_Qsum_Ssum_Pearson_r = '%.2f'%pearson_r(Lower['Qsumlower'],Lower['Slower'])[0]
    elif pearson_r(Lower['Qsumlower'],Lower['Slower'])[1]>=pvalue:
        Lower_Qsum_Ssum_Pearson_r = ' '
    if pearson_r(Total['Qsumtotal'],Total['Stotal'])[1] < pvalue:
        Total_Qsum_Ssum_Pearson_r = '%.2f'%pearson_r(Total['Qsumtotal'],Total['Stotal'])[0]
    elif pearson_r(Total['Qsumtotal'],Total['Stotal'])[1] >= pvalue:
        Total_Qsum_Ssum_Pearson_r =' '
    ## Qmaxvs. Ssum
    if pearson_r(Upper['Qmaxupper'],Upper['Supper'])[1] < pvalue:
        Upper_Qmax_Ssum_Pearson_r = '%.2f'%pearson_r(Upper['Qmaxupper'],Upper['Supper'])[0]
    if pearson_r(Lower['Qmaxlower'],Lower['Slower'])[1] < pvalue:
        Lower_Qmax_Ssum_Pearson_r = '%.2f'%pearson_r(Lower['Qmaxlower'],Lower['Slower'])[0]
    if pearson_r(Total['Qmaxtotal'],Total['Stotal'])[1] < pvalue:
        Total_Qmax_Ssum_Pearson_r = '%.2f'%pearson_r(Total['Qmaxtotal'],Total['Stotal'])[0]
    ## Put data together, and put in table
    table_data_dict = {'FOREST':[Upper_Psum_Ssum_Pearson_r,Upper_EI_Ssum_Pearson_r,Upper_Qsum_Ssum_Pearson_r,Upper_Qmax_Ssum_Pearson_r],
    'VILLAGE-FOREST':[Lower_Psum_Ssum_Pearson_r,Lower_EI_Ssum_Pearson_r,Lower_Qsum_Ssum_Pearson_r,Lower_Qmax_Ssum_Pearson_r],
    'VILLAGE':[Total_Psum_Ssum_Pearson_r,Total_EI_Ssum_Pearson_r,Total_Qsum_Ssum_Pearson_r,Total_Qmax_Ssum_Pearson_r]} ## Put data in a dictionary to convert to DataFrame
    summary =pd.DataFrame(table_data_dict,index=['Precip','EI','Qsum','Qmax'])[['FOREST','VILLAGE-FOREST','VILLAGE']]
    summary['']= summary.index
    summary = summary[['','FOREST','VILLAGE-FOREST','VILLAGE']]
    return summary
#Pearson_r_Table(pvalue=0.05)

def plotPearsonTable(pvalue=0.05,show=False):
    nrows, ncols = 3,4
    hcell, wcell=0.3,1
    hpad, wpad = 1,1
    fig = plt.figure(figsize=(ncols*wcell+wpad,nrows*hcell+hpad)) 
    pearson = fig.add_subplot(111)
    pearson.patch.set_visible(False), pearson.axis('off')
    pearson.xaxis.set_visible(False), pearson.yaxis.set_visible(False) 
  
    ALLStorms = compile_Storms_data()
    Upper = ALLStorms[['Pstorms','EI','Qsumupper','Qmaxupper','Supper','Supper_PE']].dropna()
    Lower = ALLStorms[['Pstorms','EI','Qsumlower','Qmaxlower','Slower']].dropna()
    Total = ALLStorms[['Pstorms','EI','Qsumtotal','Qmaxtotal','Stotal','Stotal_PE']].dropna()
    
    ## Psum vs. Ssum
    if pearson_r(Upper['Pstorms'],Upper['Supper'])[1] < pvalue:
        Upper_Psum_Ssum_Pearson_r = '%.2f'%pearson_r(Upper['Pstorms'],Upper['Supper'])[0]
        
    if pearson_r(Lower['Pstorms'],Lower['Slower'])[1] < pvalue:
        Lower_Psum_Ssum_Pearson_r = '%.2f'%pearson_r(Lower['Pstorms'],Lower['Slower'])[0]
        
    if pearson_r(Total['Pstorms'],Total['Stotal'])[1] < pvalue:
        Total_Psum_Ssum_Pearson_r = '%.2f'%pearson_r(Total['Pstorms'],Total['Stotal'])[0]
        
    ## EI vs. Ssum
    if pearson_r(Upper['EI'],Upper['Supper'])[1] < pvalue:
        Upper_EI_Ssum_Pearson_r = '%.2f'%pearson_r(Upper['EI'],Upper['Supper'])[0]
    elif pearson_r(Upper['EI'],Upper['Supper'])[1] >= pvalue:
        Upper_EI_Ssum_Pearson_r = ' ' 
        
    if pearson_r(Lower['EI'],Lower['Slower'])[1] < pvalue:
        Lower_EI_Ssum_Pearson_r = '%.2f'%pearson_r(Lower['EI'],Lower['Slower'])[0]
    elif pearson_r(Lower['EI'],Lower['Slower'])[1] >= pvalue:
        Lower_EI_Ssum_Pearson_r = ' ' 
        
    if pearson_r(Total['EI'],Total['Stotal'])[1] < pvalue:
        Total_EI_Ssum_Pearson_r = '%.2f'%pearson_r(Total['EI'],Total['Stotal'])[0]
    elif pearson_r(Total['EI'],Total['Stotal'])[1] >= pvalue:
        Total_EI_Ssum_Pearson_r = ' ' 
        
    ## Qsum vs. Ssum
    if pearson_r(Upper['Qsumupper'],Upper['Supper'])[1] < pvalue:
        Upper_Qsum_Ssum_Pearson_r = '%.2f'%pearson_r(Upper['Qsumupper'],Upper['Supper'])[0]
        
    if pearson_r(Lower['Qsumlower'],Lower['Slower'])[1] < pvalue:
        Lower_Qsum_Ssum_Pearson_r = '%.2f'%pearson_r(Lower['Qsumlower'],Lower['Slower'])[0]
    elif pearson_r(Lower['Qsumlower'],Lower['Slower'])[1]>=pvalue:
        Lower_Qsum_Ssum_Pearson_r = ' '
        
    if pearson_r(Total['Qsumtotal'],Total['Stotal'])[1] < pvalue:
        Total_Qsum_Ssum_Pearson_r = '%.2f'%pearson_r(Total['Qsumtotal'],Total['Stotal'])[0]
    elif pearson_r(Total['Qsumtotal'],Total['Stotal'])[1] >= pvalue:
        Total_Qsum_Ssum_Pearson_r =' '
        
    ## Qmaxvs. Ssum
    if pearson_r(Upper['Qmaxupper'],Upper['Supper'])[1] < pvalue:
        Upper_Qmax_Ssum_Pearson_r = '%.2f'%pearson_r(Upper['Qmaxupper'],Upper['Supper'])[0]
        
    if pearson_r(Lower['Qmaxlower'],Lower['Slower'])[1] < pvalue:
        Lower_Qmax_Ssum_Pearson_r = '%.2f'%pearson_r(Lower['Qmaxlower'],Lower['Slower'])[0]
        
    if pearson_r(Total['Qmaxtotal'],Total['Stotal'])[1] < pvalue:
        Total_Qmax_Ssum_Pearson_r = '%.2f'%pearson_r(Total['Qmaxtotal'],Total['Stotal'])[0]
        
    ## Put data together, and put in table
    PsumS = [Upper_Psum_Ssum_Pearson_r,Lower_Psum_Ssum_Pearson_r,Total_Psum_Ssum_Pearson_r]
    EIS = [Upper_EI_Ssum_Pearson_r,Lower_EI_Ssum_Pearson_r,Total_EI_Ssum_Pearson_r]
    QsumS = [Upper_Qsum_Ssum_Pearson_r,Lower_Qsum_Ssum_Pearson_r,Total_Qsum_Ssum_Pearson_r]
    QmaxS = [Upper_Qmax_Ssum_Pearson_r,Lower_Qmax_Ssum_Pearson_r,Total_Qmax_Ssum_Pearson_r]
    pearson.table(cellText = [PsumS,EIS,QsumS,QmaxS],rowLabels=['Psum','EI','Qsum','Qmax'],colLabels=['FOREST','FOR-VIL','VILLAGE'],loc='center left')
    plt.suptitle("Pearson's coefficients for each variable\n as compared to SSY (Mg), p<"+str(pvalue),fontsize=12)  
    show_plot(show)
    return
#plotPearsonTable(pvalue=0.05,show=True)

def Spearman_r_Table(pvalue=0.05):
    ALLStorms = compile_Storms_data()
    Upper = ALLStorms[['Pstorms','EI','Qsumupper','Qmaxupper','Supper','Supper_PE']].dropna()
    Lower = ALLStorms[['Pstorms','EI','Qsumlower','Qmaxlower','Slower']].dropna()
    Total = ALLStorms[['Pstorms','EI','Qsumtotal','Qmaxtotal','Stotal','Stotal_PE']].dropna()
    ## Psum vs. Ssum
    if spearman_r(Upper['Pstorms'],Upper['Supper'])[1] < pvalue:
        Upper_Psum_Ssum_Spearman_r = '%.2f'%spearman_r(Upper['Pstorms'],Upper['Supper'])[0]
    if spearman_r(Lower['Pstorms'],Lower['Slower'])[1] < pvalue:
        Lower_Psum_Ssum_Spearman_r = '%.2f'%spearman_r(Lower['Pstorms'],Lower['Slower'])[0]
    if spearman_r(Total['Pstorms'],Total['Stotal'])[1] < pvalue:
        Total_Psum_Ssum_Spearman_r = '%.2f'%spearman_r(Total['Pstorms'],Total['Stotal'])[0]      
    ## EI vs. Ssum
    if spearman_r(Upper['EI'],Upper['Supper'])[1] < pvalue:
        Upper_EI_Ssum_Spearman_r = '%.2f'%spearman_r(Upper['EI'],Upper['Supper'])[0]
    elif spearman_r(Upper['EI'],Upper['Supper'])[1] >= pvalue:
        Upper_EI_Ssum_Spearman_r = ' ' 
    if spearman_r(Lower['EI'],Lower['Slower'])[1] < pvalue:
        Lower_EI_Ssum_Spearman_r = '%.2f'%spearman_r(Lower['EI'],Lower['Slower'])[0]
    elif spearman_r(Lower['EI'],Lower['Slower'])[1] >= pvalue:
        Lower_EI_Ssum_Spearman_r = ' ' 
    if spearman_r(Total['EI'],Total['Stotal'])[1] < pvalue:
        Total_EI_Ssum_Spearman_r = '%.2f'%spearman_r(Total['EI'],Total['Stotal'])[0]
    elif spearman_r(Total['EI'],Total['Stotal'])[1] >= pvalue:
        Total_EI_Ssum_Spearman_r = ' ' 
    ## Qsum vs. Ssum
    if spearman_r(Upper['Qsumupper'],Upper['Supper'])[1] < pvalue:
        Upper_Qsum_Ssum_Spearman_r = '%.2f'%spearman_r(Upper['Qsumupper'],Upper['Supper'])[0]
    if spearman_r(Lower['Qsumlower'],Lower['Slower'])[1] < pvalue:
        Lower_Qsum_Ssum_Spearman_r = '%.2f'%spearman_r(Lower['Qsumlower'],Lower['Slower'])[0]
    elif spearman_r(Lower['Qsumlower'],Lower['Slower'])[1]>=pvalue:
        Lower_Qsum_Ssum_Spearman_r = ' '
    if spearman_r(Total['Qsumtotal'],Total['Stotal'])[1] < pvalue:
        Total_Qsum_Ssum_Spearman_r = '%.2f'%spearman_r(Total['Qsumtotal'],Total['Stotal'])[0]
    elif spearman_r(Total['Qsumtotal'],Total['Stotal'])[1] >= pvalue:
        Total_Qsum_Ssum_Spearman_r =' '
    ## Qmaxvs. Ssum
    if spearman_r(Upper['Qmaxupper'],Upper['Supper'])[1] < pvalue:
        Upper_Qmax_Ssum_Spearman_r = '%.2f'%spearman_r(Upper['Qmaxupper'],Upper['Supper'])[0]
    if spearman_r(Lower['Qmaxlower'],Lower['Slower'])[1] < pvalue:
        Lower_Qmax_Ssum_Spearman_r = '%.2f'%spearman_r(Lower['Qmaxlower'],Lower['Slower'])[0]
    if spearman_r(Total['Qmaxtotal'],Total['Stotal'])[1] < pvalue:
        Total_Qmax_Ssum_Spearman_r = '%.2f'%spearman_r(Total['Qmaxtotal'],Total['Stotal'])[0]
    ## Put data together, and put in table
    table_data_dict = {'FOREST':[Upper_Psum_Ssum_Spearman_r,Upper_EI_Ssum_Spearman_r,Upper_Qsum_Ssum_Spearman_r,Upper_Qmax_Ssum_Spearman_r],
    'VILLAGE-FOREST':[Lower_Psum_Ssum_Spearman_r,Lower_EI_Ssum_Spearman_r,Lower_Qsum_Ssum_Spearman_r,Lower_Qmax_Ssum_Spearman_r],
    'VILLAGE':[Total_Psum_Ssum_Spearman_r,Total_EI_Ssum_Spearman_r,Total_Qsum_Ssum_Spearman_r,Total_Qmax_Ssum_Spearman_r]} ## Put data in a dictionary to convert to DataFrame
    summary =pd.DataFrame(table_data_dict,index=['Precip','EI','Qsum','Qmax'])[['FOREST','VILLAGE-FOREST','VILLAGE']]
    summary['']= summary.index
    summary = summary[['','FOREST','VILLAGE-FOREST','VILLAGE']]
    return summary
#Spearman_r_Table(pvalue=0.05)

def plotSpearmanTable(pvalue=0.05,show=False):
    nrows, ncols = 3,4
    hcell, wcell=0.3,1
    hpad, wpad = 1,1
    fig = plt.figure(figsize=(ncols*wcell+wpad,nrows*hcell+hpad)) 
    spearman = fig.add_subplot(111)
    spearman.patch.set_visible(False), spearman.axis('off')
    spearman.xaxis.set_visible(False), spearman.yaxis.set_visible(False) 
    
    ALLStorms = compile_Storms_data()
    Upper = ALLStorms[['Supper','Supper_PE','Qsumupper','Qmaxupper','Pstorms','EI']].dropna()
    Lower = ALLStorms[['Slower','Qsumlower','Qmaxlower','Pstorms','EI']].dropna()
    Total = ALLStorms[['Stotal','Stotal_PE','Qsumtotal','Qmaxtotal','Pstorms','EI']].dropna()

    ## Psum vs. Ssum
    if spearman_r(Upper['Pstorms'],Upper['Supper'])[1] < pvalue:
        Upper_Psum_Ssum_Spearman_r = '%.2f'%spearman_r(Upper['Pstorms'],Upper['Supper'])[0]
        
    if spearman_r(Lower['Pstorms'],Lower['Slower'])[1] < pvalue:
        Lower_Psum_Ssum_Spearman_r = '%.2f'%spearman_r(Lower['Pstorms'],Lower['Slower'])[0]
    elif spearman_r(Lower['Pstorms'],Lower['Slower'])[1] >= pvalue:
        Lower_Psum_Ssum_Spearman_r = ' '
        
    if spearman_r(Total['Pstorms'],Total['Stotal'])[1] < pvalue:
        Total_Psum_Ssum_Spearman_r = '%.2f'%spearman_r(Total['Pstorms'],Total['Stotal'])[0]
        
    ## EI vs. Ssum
    if spearman_r(Upper['EI'],Upper['Supper'])[1] < pvalue:
        Upper_EI_Ssum_Spearman_r = '%.2f'%spearman_r(Upper['EI'],Upper['Supper'])[0]
    elif spearman_r(Upper['EI'],Upper['Supper'])[1] >= pvalue:
        Upper_EI_Ssum_Spearman_r = ' ' 
        
    if spearman_r(Lower['EI'],Lower['Slower'])[1] < pvalue:
        Lower_EI_Ssum_Spearman_r = '%.2f'%spearman_r(Lower['EI'],Lower['Slower'])[0]
    elif spearman_r(Lower['EI'],Lower['Slower'])[1] >= pvalue:
        Lower_EI_Ssum_Spearman_r = ' ' 
        
    if spearman_r(Total['EI'],Total['Stotal'])[1] < pvalue:
        Total_EI_Ssum_Spearman_r = '%.2f'%spearman_r(Total['EI'],Total['Stotal'])[0]
    elif spearman_r(Total['EI'],Total['Stotal'])[1] >= pvalue:
        Total_EI_Ssum_Spearman_r = ' ' 
        
    ## Qsum vs. Ssum
    if spearman_r(Upper['Qsumupper'],Upper['Supper'])[1] < pvalue:
        Upper_Qsum_Ssum_Spearman_r = '%.2f'%spearman_r(Upper['Qsumupper'],Upper['Supper'])[0]
        
    if spearman_r(Lower['Qsumlower'],Lower['Slower'])[1] < pvalue:
        Lower_Qsum_Ssum_Spearman_r = '%.2f'%spearman_r(Lower['Qsumlower'],Lower['Slower'])[0]
    elif spearman_r(Lower['Qsumlower'],Lower['Slower'])[1]>=pvalue:
        Lower_Qsum_Ssum_Spearman_r = ' '
        
    if spearman_r(Total['Qsumtotal'],Total['Stotal'])[1] < pvalue:
        Total_Qsum_Ssum_Spearman_r = '%.2f'%spearman_r(Total['Qsumtotal'],Total['Stotal'])[0]
    elif spearman_r(Total['Qsumtotal'],Total['Stotal'])[1] >= pvalue:
        Total_Qsum_Ssum_Spearman_r =' '
        
    ## Qmaxvs. Ssum
    if spearman_r(Upper['Qmaxupper'],Upper['Supper'])[1] < pvalue:
        Upper_Qmax_Ssum_Spearman_r = '%.2f'%spearman_r(Upper['Qmaxupper'],Upper['Supper'])[0]
        
    if spearman_r(Lower['Qmaxlower'],Lower['Slower'])[1] < pvalue:
        Lower_Qmax_Ssum_Spearman_r = '%.2f'%spearman_r(Lower['Qmaxlower'],Lower['Slower'])[0]
        
    if spearman_r(Total['Qmaxtotal'],Total['Stotal'])[1] < pvalue:
        Total_Qmax_Ssum_Spearman_r = '%.2f'%spearman_r(Total['Qmaxtotal'],Total['Stotal'])[0]
        
        
    ## Put data together, and put in table
    PsumS = [Upper_Psum_Ssum_Spearman_r,Lower_Psum_Ssum_Spearman_r,Total_Psum_Ssum_Spearman_r]
    EIS = [Upper_EI_Ssum_Spearman_r,Lower_EI_Ssum_Spearman_r,Total_EI_Ssum_Spearman_r]
    QsumS = [Upper_Qsum_Ssum_Spearman_r,Lower_Qsum_Ssum_Spearman_r,Total_Qsum_Ssum_Spearman_r]
    QmaxS = [Upper_Qmax_Ssum_Spearman_r,Lower_Qmax_Ssum_Spearman_r,Total_Qmax_Ssum_Spearman_r]
    spearman.table(cellText = [PsumS,EIS,QsumS,QmaxS],rowLabels=['Psum','EI','Qsum','Qmax'],colLabels=['FOREST','FOR-VIL','VILLAGE'],loc='center left')
    plt.suptitle("Spearman's coefficients for each variable\n as compared to SSY (Mg), p<"+str(pvalue),fontsize=12)  
    plt.draw()
    if show==True:
        plt.show()
    return
#plotSpearmanTable(pvalue=0.05,show=True)
    
def plotCoeffTable(show=False,norm=False):
    if norm==True:
        ALLStorms=NormalizeSSYbyCatchmentArea(compile_Storms_data())
        Upper = powerfunction(ALLStorms['Qmaxupper'],ALLStorms['Supper'])
        Total = powerfunction(ALLStorms['Qmaxtotal'],ALLStorms['Stotal'])    
        
        Up = ['%.2f'%Upper['a'],'%.2f'%Upper['b'],'%.2f'%Upper['r2'],'%.2f'%Upper['pearson'],'%.2f'%Upper['spearman'],'%.2f'%Upper['rmse']]
        Tot = ['%.2f'%Total['a'],'%.2f'%Total['b'],'%.2f'%Total['r2'],'%.2f'%Total['pearson'],'%.2f'%Total['spearman'],'%.2f'%Total['rmse']]
        
        nrows, ncols = 2,6
        hcell, wcell=0.3,1
        hpad, wpad = 1,1
        fig = plt.figure(figsize=(ncols*wcell+wpad,nrows*hcell+hpad)) 
        coeff = fig.add_subplot(111)
        coeff.patch.set_visible(False), coeff.axis('off')
        coeff.xaxis.set_visible(False), coeff.yaxis.set_visible(False) 
        coeff.table(cellText = [Up,Tot],rowLabels=['Upper','Total'],colLabels=[r'$\alpha$',r'$\beta$',r'$r^2$',"Pearson's","Spearman's",'RMSE'],loc='center left',fontsize=14)
   
    elif norm==False:
        ALLStorms = compile_Storms_data()
        Upper = powerfunction(ALLStorms['Qmaxupper'],ALLStorms['Supper'])
        Lower = powerfunction(ALLStorms['Qmaxlower'],ALLStorms['Slower'])    
        Total = powerfunction(ALLStorms['Qmaxtotal'],ALLStorms['Stotal'])
        
        Up = ['%.2f'%Upper['a'],'%.2f'%Upper['b'],'%.2f'%Upper['r2'],'%.2f'%Upper['pearson'],'%.2f'%Upper['spearman'],'%.2f'%Upper['rmse']]
        Low = ['%.2f'%Lower['a'],'%.2f'%Lower['b'],'%.2f'%Lower['r2'],'%.2f'%Lower['pearson'],'%.2f'%Lower['spearman'],'%.2f'%Lower['rmse']]
        Tot = ['%.2f'%Total['a'],'%.2f'%Total['b'],'%.2f'%Total['r2'],'%.2f'%Total['pearson'],'%.2f'%Total['spearman'],'%.2f'%Total['rmse']]    
    
        nrows, ncols = 3,6
        hcell, wcell=0.3,1
        hpad, wpad = 1,1
        fig = plt.figure(figsize=(ncols*wcell+wpad,nrows*hcell+hpad)) 
        coeff = fig.add_subplot(111)
        coeff.patch.set_visible(False), coeff.axis('off')
        coeff.xaxis.set_visible(False), coeff.yaxis.set_visible(False) 
        coeff.table(cellText = [Up,Low,Tot],rowLabels=['Upper','Lower','Total'],colLabels=[r'$\alpha$',r'$\beta$',r'$r^2$',"Pearson's","Spearman's",'RMSE'],loc='center left',fontsize=14)
    
    plt.suptitle("Model parameters for POWER law Qmax-SSYev model: "+r'$SSY_{ev} = \alpha Q^\beta$',fontsize=14)
    plt.draw()
    if show==True:
        plt.show()
    return
#plotCoeffTable(show=True,norm=False)