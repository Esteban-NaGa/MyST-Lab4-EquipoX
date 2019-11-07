#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 08:16:17 2019

@author: Esteban
"""

import pandas as pd

#%%
precios = '/Users/Esteban/Desktop/MyST_Python/precios_historicos_eurusd.csv'
calendario = '/Users/Esteban/Desktop/MyST_Python/calendario_economico.csv'

#%%
precios_df = pd.read_csv(precios,
                        header=0,
                        sep=',',
                        parse_dates=False,
                        skip_blank_lines=True)
precios_df.head()

#%%
ce_df = pd.read_csv(calendario,
                        header=0,
                        sep=',',
                        parse_dates=False,
                        skip_blank_lines=True)
ce_df.head()

#%%
