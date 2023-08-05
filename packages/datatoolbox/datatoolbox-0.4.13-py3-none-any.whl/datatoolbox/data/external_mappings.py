#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 13:16:08 2021

@author: ageiges
"""


mapping= dict()

#%% CD LINKS
mapping['CDLINKS_2021'] = dict()
mapping['CDLINKS_2021']['region']= {
             'World' : 'World',
             'OECD90 and EU (and EU candidate) countries' : 'R5_OECD',
             'Countries from the Reforming Ecomonies of the Former Soviet Union' : 'R5_REF',
             'Asian countries except Japan' : 'R5_ASIA',
             'Countries of the Middle East and Africa' : 'R5_MID',
             'Latin American countries' : 'R5_LAM',
             'Federative Republic of Brazil' : 'BRA',
             "People's Repulic of China" : 'CHN',
             'European Union (28 member countries)': 'EU28',
             'Republic of India' : 'IDN', 
             'State of Japan' : 'JPN',
             'Russian Federation' :'RUS', 
             'United States of America': 'USA'}


#%% ENGAGE
mapping['ENGAGE_2021'] = dict()
mapping['ENGAGE_2021']['region']= {
            'Asia (R5)':  'R5_ASIA',
            'China (R10)': 'R10_China',
            'European Union and Western Europe (R10)' : 'R10_EUROPE',
            'Latin America (R10)' : 'R10_LAM',
            'Latin America (R5)' : 'R5_LAM',
            'Middle East & Africa (R5)' : 'R5_MAF',
            'Middle East (R10)' : 'R10_MIDEAST',
            'North America (R10)' : 'R10_NAMERICA',
            'OECD & EU (R5)' : 'R10_EU_OECD',
            'Other (R10)' : 'R10_OTHER',
            'Other (R5)' :'R5_OTHER',
            'Other Asian countries (R10)' : 'R10_ASIA',
            'Pacific OECD (R10)' : 'R10_PACIFIC_OECD',
            'Reforming Economies (R10)': 'R10_REF',
            'Reforming Economies (R5)' : 'R5_REF',
            'South Asia (R10)' : 'R10_SOUTH_ASIA',
            'Sub-Saharan Africa (R10)' : 'R10_SUB_AFIRICA',
            'World' : 'World'}


#%% IPCC_AR5
mapping['IPCC_AR5'] = dict()
mapping['IPCC_AR5']['region'] ={
            'ASIA': 'R5_ASIA',
            'LAM': 'R5_LAM',
            'MAF': 'R5_MAF',
            'OECD90': 'R5_OECD90',
            'REF': 'R5_REF',
            'World': 'World'}

#%% IPCC_SR15
mapping['IPCC_SR15_2019'] = dict()
mapping['IPCC_SR15_2019']['region'] = {
            'World' : 'World',
            'R5ROWO' : 'R5_ROWO',
            'R5ASIA' : 'R5_ASIA',
            'R5LAM' : 'R5_LAM',
            'R5MAF' : 'R5_MAF',
            'R5OECD90+EU' : 'R5_OECD',
            'R5REF' : 'R5_REF'
            }




#%% NGFS 
mapping['NGFS_2021'] = dict()
mapping['NGFS_2021']['region']= {
             'World' : 'World',
             'OECD90 and EU (and EU candidate) countries' : 'R5_OECD',
             'Countries from the Reforming Ecomonies of the Former Soviet Union' : 'R5_REF',
             'Asian countries except Japan' : 'R5_ASIA',
             'Countries of the Middle East and Africa' : 'R5_MID',
             'Latin American countries' : 'R5_LAM'}

