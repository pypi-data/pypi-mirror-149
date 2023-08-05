#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 11 14:36:50 2021

@author: ageiges
"""

import datatoolbox as dt

dt.find(variable ='Final_Energy|Transport|H', source= 'IEA_WEB_2020').index

total = dt.getTable('Final_Energy|Transport|Total__Historic__IEA_WEB_2020')

tables = dict()
for fuel_type in ['Biofuel_waste', 'Electricity']:
    tables[fuel_type] = dt.getTable('Final_Energy|Transport|{}__Historic__IEA_WEB_2020'.format(fuel_type))
    
low_emission_fuel_share = (tables['Biofuel_waste'] + tables['Biofuel_waste']) / total
low_emission_fuel_share  = low_emission_fuel_share.convert('%')
low_emission_fuel_share.meta['source'] = 'CAT calculations based one IEA WEB 2020'
low_emission_fuel_share.loc[['World'],:].to_excel('low_emission_fuel_share_CAT_2021.xlsx')
