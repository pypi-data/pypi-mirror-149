#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 11 14:10:15 2021

@author: ageiges
"""

import datatoolbox as dt
import matplotlib.pyplot as plt

re_generation = dt.getTable('Electricity_generation|Renewables__historic__IEA_WEB_2020')
total_generation = dt.getTable('Electricity_generation|Total__historic__IEA_WEB_2020')

re_share = (re_generation / total_generation).convert('%')

print(re_share)
'World' in re_share.index

re_share.loc[['World'],list(range(1990,2016,5)) + [2017, 2018,2019]].to_excel('re_share.xlsx')
re_share.meta['source'] = 'CAT calculations based one IEA WEB 2020'
re_share.loc[['World'],:].to_excel('renewables_share_CAT_2020.xlsx')

#%% solar share
new_re_generation = dt.getTable('Electricity_generation|Solar_wind_other__historic__IEA_WEB_2020')
total_generation = dt.getTable('Electricity_generation|Total__historic__IEA_WEB_2020')

new_re_share = (new_re_generation / total_generation).convert('%')

plt.clf()
plt.plot(re_share.loc['World',:], label = 'All renewables')
plt.plot(new_re_share.loc['World',:], label = 'New renewables')
plt.legend()
plt.ylabel('Share in power generation [%]')