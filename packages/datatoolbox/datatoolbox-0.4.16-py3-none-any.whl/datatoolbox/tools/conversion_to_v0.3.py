#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 15:47:58 2020

@author: ageiges
"""

import datatoolbox as dt
#%%
inventory = dt.find(source='IAMC')


replacementDict = {#'Capacity': 'Electricity|capacity',
                   'Capacity|Electricity' : 'Electricity|capacity',
                   'Heat_output_'   : 'Heat_output|',
                   'Losses_' : 'Losses|' ,
                   'Final_energy_demand_by_fuel|': 'Final_Energy|Total|',
                   'Final_energy' :'Final_Energy',
                   'Secondary_energy' : 'Secondary_Energy',
                   'Emissions|KyotoGHG' : 'Emissions|KYOTOGHG_AR4',
                   'Emissions|KYOTOGHG' : 'Emissions|KYOTOGHG',
                   'Emission|KYOTO_GHG_AR4' : 'Emissions|KYOTOGHG_AR4',
                   'Emissions|Kyoto Gases|AR5-GWP100' : 'Emissions|KYOTOGHG_AR5',
                   'Emissions|KYOTOGHGAR4' : 'Emissions|KYOTOGHG_AR4',
                   'Emissions_KYOTOGHGAR4' : 'Emissions|KYOTOGHG_AR4',
                   'Emissions|Kyoto Gases|AR4-GWP10' : 'Emissions|KYOTOGHG_AR4',
                   'Emissions|KYOTOGHG_AR40' : 'Emissions|KYOTOGHG_AR4',
                   'Emissions_KYOTOGHG_AR4' : 'Emissions|KYOTOGHG_AR4',
                   'Emissions|Kyoto_Gases' : 'Emissions|KYOTOGHG',
                   'Emissions|Fuel|CO2' : 'Emissions|CO2|Fuel',
                   'Emissions|Fuel_CO2' : 'Emissions|CO2|Fuel',
                   'Exports_' : 'Exports|',
                   'population_total' : 'Population',
                   'population' : 'Population',
                   'gdp_ppp' : 'GDP|PPP',
                   'gdp_pp'  : 'GDP|PPP',
                   'GDP_PPP'  : 'GDP|PPP',
                   'GDP_MER'  : 'GDP|MER',
                   'Emissions_CH4' : 'Emissions|CH4',
                   'Emissions_CO2' : 'Emissions|CO2',
                   'Emissions_CO2_energy' : 'Emissions|CO2|Energy',
                   'Emissions|CO2_energy' : 'Emissions|CO2|Energy',
                   'Emissions|HFCS' : 'Emissions|HFCs',
                   'Emissions|PFCS' : 'Emissions|PFCs',
                   'Electricity_output'  : 'Electricity_generation',
                   'Electricity_output ' : 'Electricity_generation',
                   'Elect_Capacity'     : 'Electricity|capacity',  
                   'Electrical_capacity' : 'Electricity|capacity',
                   'Electrical|capacity' : 'Electricity|capacity',
                   'Electricity|capacity ': 'Electricity|capacity',
                   'Electricity_generation' : 'Electricity|generation',
                   'Electricity_genertation ' : 'Electricity|generation', 
                   'Elect_Generation' : 'Electricity|generation',
                   'Electricity_and_heat_generation' : 'Electricity&Heat|generation',
                   'Price_' : 'Price|',
                   'Primary_Energy_': 'Primary_Energy|',
                   'Primary_energy' : 'Primary_Energy',
                   'Production_' : 'Production|',
                   'Stock_changes_'  :'Stock_changes|'  ,
                   'Transfers_' : 'Transfers|',
                   'Total_PE_supply_' : 'Total_PE_supply|',
                   'Total_consumption_' : 'Total_consumption|',
                   'Emissions_er_capita' : 'Emissions_per_capita'}

for string, newString in replacementDict.items():
    mask = inventory.entity.str.contains(string)
    inventory.loc[mask, 'entity'] = inventory.loc[mask, 'entity'].apply(lambda x: x.replace(string,newString))
#%%
entityList = ['Electricity|generation|',
              'Electricity|capacity|',
              'Electricity&Heat|generation|',
              'Emissions|KYOTOGHG_AR4|',
              'Emissions|KYOTOGHG_AR5|',
              'Emissions|KYOTOGHG|',
              'Emissions|BC|',
              'Emissions|CO2|',
              'Emissions|CH4|',
              'Emissions|NH3|',
              'Emissions|N2O|',
              'Emissions|NF3|',
              'Emissions|NOx|',
              'Emissions|HFCs|',
              'Emissions|OC|',
              'Emissions|SF6|',
              'Emissions|PFCs|',
              'Emissions|VOC|',
              'Exports|',
              'Final_Energy|',
              'Investment|',
              'GDP|PPP|constant|',
              'GDP|PPP|current|',
              'GDP|MER|',
              'Heat_output|',
              'Secondary_Energy|',
              'Stock_changes|' ,
              'Transfers|',
              'Total_consumption|',
              'Population|',
              'Primary_Energy|',
              'Price|',
              'Production|']

inventory.category = None
for entity in entityList:
    mask = inventory.entity.str.startswith(entity)
    
    inventory.loc[mask, 'category'] = inventory.loc[mask, 'category'] + inventory.loc[mask, 'entity'].apply(lambda x: x.replace(entity,'')) 
    inventory.loc[mask, 'entity'] = entity[:-1]

#%%
entityList = list(inventory.entity.unique())
entityList.sort()
print(entityList)
print(len(entityList))


#%% ISSUES ??
if False:
    """
    'Total_consumption' : 'Final_energy'
    'Total_PE_supply'   : 'Primary_energy'
    'Primary_Energy_supply' : 'Primary_energy'
    'Production_'        : "?"
    'Transfers_'         : '?'
    'Stock_changes_'     
    Losses_
    'Energy_Demand'
    """
    
    #%%
dt.find(entity='Primary_Energy').source.unique()
#%%
dt.find(source='IEA_WEB_2019').entity.unique()
