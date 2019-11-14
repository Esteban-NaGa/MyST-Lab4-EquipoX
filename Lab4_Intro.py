#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 08:16:17 2019

@author: Esteban
"""

import pandas as pd
import numpy as np
import datetime as datetime
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
precios_df['timestamp'] = pd.to_datetime(precios_df['timestamp'])
precios_df['timestamp'] = precios_df['timestamp'].dt.tz_localize('UTC')
#precios_df.index = precios_df['timestamp'] ; precios_df = precios_df.drop('timestamp',axis=1)
precios_df.head()

#%%
ce_df['timestamp'] = pd.to_datetime(ce_df['timestamp'])
ce_df['timestamp'] = ce_df['timestamp'].dt.tz_localize('UTC')
#ce_df.index = ce_df['timestamp'] ; ce_df = ce_df.drop('timestamp',axis=1)
ce_df.head()

#%%
Control = pd.DataFrame()
Autos = pd.DataFrame()
for i in range(len(ce_df)):
    f = ce_df.index[i]
    if ce_df['Name'][i] == "Retail Sales Control Group":
        f=ce_df.index[i]
        Control[f] = ce_df.iloc[i]
    elif ce_df['Name'][i] == "Retail Sales ex Autos (MoM)":
        f=ce_df.index[i]
        Autos[f] = ce_df.iloc[i]
        
Autos = Autos.T
Control = Control.T
df_indicadores = pd.concat([Autos, Control])

#%%
#Usar np.where para encontrar el match entre precios y calendario
#%%
#A 	actual >= previous & actual >= consensus & consensus >= previous
#B 	actual >= previous & actual >= consensus & consensus < Precious
#C 	actual >= previous & actual < consensus & consensus >= previous
#D 	actual >= previous & actual < consensus & consensus < previous
def escenario(d):
    d["actual"]=d["escenario"]
    for i in range(len(d["actual"])): 
      if d["actual"][i] >= d["consensus"][i] >= d["previous"][i]:
          d["escenario"][i] = "A"
      elif d["actual"][i] >= d["consensus"][i] < d["previous"][i]:
          d["escenario"][i]= "B"
      elif d["actual"][i] < d["consensus"][i] >= d["previous"][i]:
          d["escenario"][i]= "C"
      elif d["actual"][i] < d["consensus"][i] < d["previous"][i]:
          d["escenario"][i]= "D"
          
    return d
#%%
Autos = escenario(Autos)
Control = escenario(Control)
df_indicadores = pd.concat([Autos, Control])
#%% match de nuestros indicadores con el precio
comparacion_autos = precios_df[precios_df.timestamp.isin(Autos.timestamp)]
comparacion_control = precios_df[precios_df.timestamp.isin(Control.timestamp)]

#%%
## comprehension de listas para data frames
autoscom = [precios_df.iloc[i-6:i+7] for i in comparacion_autos.index]
controlcom = [precios_df.iloc[i-6:i+7] for i in comparacion_autos.index]




