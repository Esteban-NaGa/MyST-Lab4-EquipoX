#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 08:16:17 2019

@author: Esteban
"""

import pandas as pd
#import numpy as np
#import datetime as datetime
#%%
precios = '/Users/Esteban/Desktop/MyST_Python/precios_historicos_eurusd.csv'
calendario = '/Users/Esteban/Desktop/MyST_Python/calendario_economico.csv'
#precios = '/Users/preci/Documents/iteso/semestre 9/labs trading/Lab4/MyST-Lab5-EquipoX/precios_historicos_eurusd.csv'
#calendario = '/Users/preci/Documents/iteso/semestre 9/labs trading/Lab4/MyST-Lab5-EquipoX/calendario_economico.csv'

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
Autos = Autos.reset_index(drop=True)
Control = Control.reset_index(drop=True) 
#%%
Autos['Volatility']=Autos['Volatility'].astype(object).astype(int)
Autos.iloc[:,5:9]=Autos.iloc[:,5:9].astype(object).astype(float)

Control['Volatility']=Control['Volatility'].astype(object).astype(int)
Control.iloc[:,5:9]=Control.iloc[:,5:9].astype(object).astype(float)
#%%
def escenario(d):
    d["escenario"]=d["actual"]
    for i in range(len(d)): 
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
Autos_esce = escenario(Autos)
Control_esce = escenario(Control)
df_indicadores_esce = pd.concat([Autos, Control])
#%% match de nuestros indicadores con el precio
comparacion_autos = precios_df[precios_df.timestamp.isin(Autos.timestamp)]
comparacion_control = precios_df[precios_df.timestamp.isin(Control.timestamp)]
#%%
## comprehension de listas para data frames
autoscom = [precios_df.iloc[i-6:i+7] for i in comparacion_autos.index]
controlcom = [precios_df.iloc[i-6:i+7] for i in comparacion_autos.index]
#%%
Autos_esce['direccion'] = Autos['actual']
Autos_esce['pips alcistas'] = Autos['actual']
Autos_esce['pips bajistas'] = Autos['actual']
Autos_esce['volatilidad'] = Autos['actual']

Control_esce['direccion'] = Control['actual']
Control_esce['pips alcistas'] = Control['actual']
Control_esce['pips bajistas'] = Control['actual']
Control_esce['volatilidad'] = Control['actual']
#%%
def df_final(df, periodos):
    
     for i in range(len(df)):
        df['direccion'][i] = periodos[i]["close"].iloc[-1] - periodos[i]["open"].iloc[6]
        df['pips alcistas'][i] = periodos[i]["high"].iloc[6:-1].max() - periodos[i]["open"].iloc[0]
        df['pips bajistas'][i] = periodos[i]["open"].iloc[0] - periodos[i]["low"].iloc[6:-1].min()
        df['volatilidad'][i] = periodos[i]["high"].max()-periodos[i]["low"].min()
        return df
#%%
Final_autos = df_final(Autos_esce, autoscom)
Final_control = df_final(Control_esce, controlcom)
