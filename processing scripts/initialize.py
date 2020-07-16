#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 12:13:02 2019

@author: jgf5fz
"""

from datetime import date
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os





scratchpath = '/scratch/jgf5fz'
fig_dir = 'DAC_paper'

ns = np.arange(18)
exe_ns = ns.astype(str) #creates string list of exe_n numbers to iterate through
exe_ns = list(exe_ns)

todays_date = str(date.today())
print(todays_date)

er = os.listdir(scratchpath+'/errors') #if run is listed in errors directory (i.e., did not solve), add to list of errors to skip plotting 

errors = [] + er #append errors list to runs we don't care about (e.g., have NETs available but no climate policy to induce their use)
errors = list(map(str,errors))


#exe_ns = ['5']


plt.style.use('seaborn-paper')
plt.style.use('seaborn-colorblind')


def create_folders(folder_list,fig_dir):
    """creates the directories to organize results plots into"""
    for folder in folder_list:
        if not(os.path.isdir(fig_dir+'/'+folder)):
            os.mkdir(fig_dir+'/'+folder)


   
##################




for e in errors:
    if e in exe_ns:
        exe_ns.remove(e)



print(exe_ns)
resolution = 500

######################

def get_scenario_name(df):
    scenario_name = df['scenario'][0]
    scenario_name = scenario_name[:-29]
    if not scenario_name=='':
        if scenario_name[-1] == ',':
            scenario_name = scenario_name[:-1]
    
    return scenario_name

def df_plotting_prep(df,years,scenario_name,col,single_scenario):

    if single_scenario == False:
        df = df[years]
        col = df.index.values.astype(int)[0]
        df = df.T
        df = df.reset_index()
        df = df.rename(index=str, columns={"index":"year",col:scenario_name})
        df['year'] = df['year'].astype('float64')
        df = df.set_index('year')
    else:
        ix = df[[col]]
        df = df[years]
        df = pd.concat([ix,df],axis=1)
        df = df.set_index(col)

        df = df.T
        df = df.reset_index()
        df = df.rename(index=str, columns={"index":"year"})
        df['year'] = df['year'].astype('float64')
        df = df.set_index('year')
        
    return df

def set_years(start_year,end_year):
    """creates a string array of years to be read as columns for the dataframe"""    
    if start_year >= 2010:
        years = np.arange(start_year,end_year+5,5).astype(str)
    elif start_year < 2010 and start_year >=1990:
        years = np.arange(2010,end_year+5,5).astype(str)
        years = np.insert(years,0,'2005')
        years = np.insert(years,0,'1990')
    else:
        years = np.arange(2010,end_year+5,5).astype(str)
        years = np.insert(years,0,'2005')
        years = np.insert(years,0,'1990')
        years = np.insert(years,0,'1985')
        years = np.insert(years,0,'1980')
        
    return years 


#print(set_years(1980,2100))





#fontsize = 'x-large'

def map_scenarios(exe_ns):
    print('')
    print('Scenario name mapping to exe_n folders:')
    ns = []
    for n in exe_ns:
        file = scratchpath+'/exe_'+n+'/queryout_co2_concentrations_global.csv'
        if os.path.exists(file):
            co2_concentrations = pd.read_csv(file,skiprows=1)

            df = co2_concentrations
        
            df[['scenario','region','CO2-concentration']] = df[['scenario','region','CO2-concentration']].astype(str)
        
            scenario_name = get_scenario_name(df)
            print(n,scenario_name)
            ns.append(n)
        else:
            print('error: file for exe_'+n+' does not exist')
    return ns
        
exe_ns = map_scenarios(exe_ns)



def label_mapper(gcam_name,scenario_dict):
    
    if gcam_name in scenario_dict:
        return scenario_dict[gcam_name]
    else:
        print(gcam_name+' not in scenario dictionary')
        return gcam_name
    
def fix_legend(ax,legend_order):
    handles,labels = ax.get_legend_handles_labels()
    idx = []
    for i in range(len(legend_order)):
        index=labels.index(legend_order[i])
        idx.append(index)
    
    
    h = []
    l = []
    
    for i in range(len(idx)):
        h.append(handles[idx[i]])
        l.append(labels[idx[i]])
    return h,l


def get_diff(query,col,n1,n2):
    n1 = str(n1)
    n2 = str(n2)
    df1 = pd.read_csv(scratchpath+'/exe_'+n1+'/'+query+'.csv',skiprows=1)
    df2 = pd.read_csv(scratchpath+'/exe_'+n2+'/'+query+'.csv',skiprows=1)
    str_cols = ['scenario',col,'Units']
    df1[str_cols] = df1[str_cols].astype(str)
    scenario_name = get_scenario_name(df1)
    df1 = df_plotting_prep(df1,years,scenario_name,col,True)
    df2[str_cols] = df2[str_cols].astype(str)
    scenario_name = get_scenario_name(df2)
    df2 = df_plotting_prep(df2,years,scenario_name,col,True)
    df = df1.subtract(df2,fill_value=0)
    df.index = df.index.astype(int)
    return df
    
    
#%%

    
    
        
    