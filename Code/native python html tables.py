# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 14:00:34 2015

@author: Alex
"""
## tried this, ended up using R htmlTables

## HTML.py tables
import pypandoc
import HTML
table_data = [lab,lbj_ysi,lbj_obs_2013,lbj_obs_2014,qua_obs,dam_ts3k,dam_ysi]
header = [r'$\beta$',r'$r^2$',"Pearson's","Spearman's",'RMSE']
htmlcode = HTML.table(table_data, attribs={'bgcolor': 'yellow'})
print htmlcode