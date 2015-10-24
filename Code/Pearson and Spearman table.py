# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 12:48:57 2015

@author: Alex
"""

## Pearson and Spearman tables


def Pearson_Spearman_Table(subset='pre',pvalue=0.05):
    ## compile storm data
    storms_data = compile_storms_data(subset)
    Upper = storms_data[['Pstorms','EI','Qsumupper','Qmaxupper','Supper','Supper_PE']].dropna()
    Total = storms_data[['Pstorms','EI','Qsumtotal','Qmaxtotal','Stotal','Stotal_PE']].dropna()
    ## Test if the Pearson Correlation is Significant at some p value
    def test_pearson_p(df1,df2,pvalue):
        pearson_correlation = pearson_r(df1,df2)
        if pearson_correlation[1] < pvalue:
            sig = '%.2f'%pearson_correlation[0]
        elif pearson_correlation[1] > pvalue:
            sig = ' '
        return sig
            
    ## Psum vs. Ssum
    Upper_Psum_Ssum_Pearson_r = test_pearson_p(Upper['Pstorms'],Upper['Supper'])
    Total_Psum_Ssum_Pearson_r = test_pearson_p(Total['Pstorms'],Total['Stotal'])     
    ## EI vs. Ssum
    Upper_EI_Ssum_Pearson_r = test_pearson_p(Upper['EI'],Upper['Supper'])
    Total_EI_Ssum_Pearson_r = test_pearson_p(Total['EI'],Total['Stotal'])
    ## Qsum vs. Ssum
    Upper_Qsum_Ssum_Pearson_r = test_pearson_p(Upper['Qsumupper'],Upper['Supper'])
    Total_Qsum_Ssum_Pearson_r = test_pearson_p(Total['Qsumtotal'],Total['Stotal'])
    ## Qmaxvs. Ssum
    Upper_Qmax_Ssum_Pearson_r = test_pearson_p(Upper['Qmaxupper'],Upper['Supper'])
    Total_Qmax_Ssum_Pearson_r = test_pearson_p(Total['Qmaxtotal'],Total['Stotal'])
    
    ## Test if the Spearman Correlation is Significant at some p value
    def test_spearman_p(df1,df2,pvalue):
        spearman_correlation = spearman_r(df1,df2)
        if spearman_correlation[1] < pvalue:
            sig = '%.2f'%pearson_correlation[0]
        elif spearman_correlation[1] > pvalue:
            sig = ' '
        return sig
    
    ## Psum vs. Ssum
    Upper_Psum_Ssum_Spearman_r = test_spearman_p(Upper['Pstorms'],Upper['Supper'])
    Total_Psum_Ssum_Spearman_r = test_spearman_p(Total['Pstorms'],Total['Stotal'])     
    ## EI vs. Ssum
    Upper_EI_Ssum_Spearman_r = test_spearman_p(Upper['EI'],Upper['Supper'])
    Total_EI_Ssum_Spearman_r = test_spearman_p(Total['EI'],Total['Stotal'])
    ## Qsum vs. Ssum
    Upper_Qsum_Ssum_Spearman_r = test_spearman_p(Upper['Qsumupper'],Upper['Supper'])
    Total_Qsum_Ssum_Spearman_r = test_spearman_p(Total['Qsumtotal'],Total['Stotal'])
    ## Qmaxvs. Ssum
    Upper_Qmax_Ssum_Spearman_r = test_spearman_p(Upper['Qmaxupper'],Upper['Supper'])
    Total_Qmax_Ssum_Spearman_r = test_spearman_p(Total['Qmaxtotal'],Total['Stotal'])
    
    
    