#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 09:10:13 2020

@author: ageiges
"""

import datatoolbox as dt

for source in dt.inventory().source.unique():
    try:
        IDList = list(dt.findExact(source= source).index)
        dt.util.zipExport(IDList, source + '.zip')
    except:
        print('source {} was not exported'.format(source))