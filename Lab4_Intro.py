#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 08:16:17 2019

@author: Esteban
"""

import pandas as pd
import numpy as np
#%%
#precios = '/Users/Esteban/Desktop/MyST_Python/precios_historicos_eurusd.csv'
#calendario = '/Users/Esteban/Desktop/MyST_Python/calendario_economico.csv'
precios = '/Users/preci/Documents/iteso/semestre 9/labs trading/Lab4/MyST-Lab5-EquipoX/precios_historicos_eurusd.csv'
calendario = '/Users/preci/Documents/iteso/semestre 9/labs trading/Lab4/MyST-Lab5-EquipoX/calendario_economico.csv'

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
ce_df['timestamp'] = pd.to_datetime(ce_df['timestamp'])
ce_df.index = ce_df['timestamp'] ; ce_df = ce_df.drop("timestamp",axis=1)
ce_df.head()

#%%
Control = pd.DataFrame()
Autos = pd.DataFrame()
for i in range(len(ce_df)):
    f = ce_df.index[i]
    if ce_df['Name'][i] == "Retail Sales Control Group":
        f=ce_df.index[i]
        Control[d] = ce_df.iloc[i]
    elif ce_df['Name'][i] == "Retail Sales ex Autos (MoM)":
        f=cal_ec.index[i]
        Autos[d] = cal_ec.iloc[i]
        
Autos = Autos.T
Control = Control.T