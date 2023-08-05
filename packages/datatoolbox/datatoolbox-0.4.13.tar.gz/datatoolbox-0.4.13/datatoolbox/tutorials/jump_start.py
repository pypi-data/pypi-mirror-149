#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# %%
"""
Created on Tue Mar 22 10:21:27 2022

@author: ageiges
"""

import datatoolbox as dt
import matplotlib.pyplot as plt

# %%
dt.import_new_source_from_remote('PRIMAP_2019')


# %% Inventory
"""
The inventory is a pandas dataframe containing all available tables, each in a row.
The index has the tableIDs and comes with the following colums : 
['variable', 'entity', 'category', 'pathway', 'scenario', 'model', 'source', 'source_name', 'source_year', 'unit']

All coulumns can be used for the later search requests.
"""
dt.inventory().head()


# %% Seach using patterns - findp
"""
Defauls is a shell style type of search suitable to be used for categories.
"""

dt.findp(source = 'PRIMAP_2019').head()

# %%
# One star (*) is giving all results for only the following level (speparated by "|") 
res = dt.findp(variable='Emissions|CH4*',
         source = 'IPCC_SR15') # "Emissions|KYOTOGHG_AR4|Marine" will be excluded
print('Singel star results:')
print(res.variable.unique())
# 
#Two stars (**) allows for any patter for the complete rest of the string
res = dt.findp(variable='Emissions|CH4**',
         source = 'IPCC_SR15') # "Emissions|KYOTOGHG_AR4|Marine" will be included

print('Two stars results:')
print(res.variable.unique())

# %% Results object

res
res.columns
res.index

# %% Datatable
# Data table
res = dt.findp(source = 'PRIMAP_2019')
table = dt.getTable(res.index[0])
print(table)

# %%

# %%
# Meta data
table.meta


# %% meta data


--->>> benchmarks


# %%
dt.findp(source='IEA*').source.unique()

# %% adapters
# Interfaces
res = dt.findp(source='IPCC_SR15', variable=[
    'Secondary Energy|Electricity|Coal|w/o CCS',
    'Secondary Energy|Electricity'],
         pathway = ['IMA15-LiStCh|IMAGE 3.0.1',
            'CD-LINKS_NPi2020_1000|WITCH-GLOBIOM 4.4',
            'CD-LINKS_NPi2020_400|WITCH-GLOBIOM 4.4',
            'ADVANCE_2020_1.5C-2100|MESSAGE-GLOBIOM 1.0',
            'SSP1-19|AIM/CGE 2.0',
            'SSP2-19|AIM/CGE 2.0',
            'TERL_15D_LowCarbonTransportPolicy|AIM/CGE 2.1',
            'TERL_15D_NoTransportPolicy|AIM/CGE 2.1',])


print(res)
# pyam
idf =  res.as_pyam()

# xarray
xds = res.as_xarray()
# %% new way of computing a benchmark
res = dt.findp(
    source='IPCC_SR15', 
    variable=[
        'Secondary Energy|Electricity|Coal|w/o CCS',
        'Secondary Energy|Electricity'],
    pathway = [
        'IMA15-LiStCh|IMAGE 3.0.1',
        'CD-LINKS_NPi2020_1000|WITCH-GLOBIOM 4.4',
        'CD-LINKS_NPi2020_400|WITCH-GLOBIOM 4.4',
        'ADVANCE_2020_1.5C-2100|MESSAGE-GLOBIOM 1.0',
        'SSP1-19|AIM/CGE 2.0',
        'SSP2-19|AIM/CGE 2.0',
        'TERL_15D_LowCarbonTransportPolicy|AIM/CGE 2.1',
        'TERL_15D_NoTransportPolicy|AIM/CGE 2.1']
    )

xds = res.as_xarray()
xds['Coal share'] = xds['Secondary Energy|Electricity|Coal|w/o CCS'] / xds['Secondary Energy|Electricity']
xds['Coal share'] = xds['Coal share'].pint.to('percent')

plt.plot(xds['Coal share'].time, xds['Coal share'].mean(dim= 'pathway').sel(region='World'))
xds['Coal share'].median(dim= 'pathway').sel(region='World', time=2030).item()
plt.title('Coal share')
#print(xds)

# %%
dt.conversionFactor('Mt N2O / yr', 't CO2eq /yr', context ='GWPAR4')

# %% Emission intensity of power generation
res = dt.findp(
    source='IPCC_SR15', 
    variable=[
        'Emissions|CO2|Energy|Supply|Electricity',
        'Secondary Energy|Electricity'],
    pathway = ['IMA15-LiStCh|IMAGE 3.0.1',
        'CD-LINKS_NPi2020_1000|WITCH-GLOBIOM 4.4',
        'CD-LINKS_NPi2020_400|WITCH-GLOBIOM 4.4',
        'ADVANCE_2020_1.5C-2100|MESSAGE-GLOBIOM 1.0',
        'SSP1-19|AIM/CGE 2.0',
        'SSP2-19|AIM/CGE 2.0',
        'TERL_15D_LowCarbonTransportPolicy|AIM/CGE 2.1',
        'TERL_15D_NoTransportPolicy|AIM/CGE 2.1']
    )

xds = res.as_xarray()

xds['Emission intensity'] = xds['Emissions|CO2|Energy|Supply|Electricity'] / xds['Secondary Energy|Electricity']
xds['Emission intensity'] = xds['Emission intensity'].pint.to('g CO2 /  kWh')

#plt.plot(xds['Emission intensity'].time, xds['Emission intensity'].mean(dim= 'pathway').sel(region='World'))
xds['Emission intensity'].median(dim= 'pathway').sel(region='World', time=2030).item()
#plt.title(f'Emission intensity[{xds["Emission intensity"].pint.units}]')
print(xds)


# %% plotting time series
plt.figure(1)
plt.clf()

ax = plt.subplot(1,2,1)
xds['Emission intensity'].median(dim='pathway').plot.line(ax  =ax, x='time')
ax = plt.subplot(1,2,2)
xds['Emission intensity'].mean(dim= 'pathway').sel(region='World').plot.line(ax  =ax, x='time')
plt.legend(['World'])
plt.ylabel('')

# %%
