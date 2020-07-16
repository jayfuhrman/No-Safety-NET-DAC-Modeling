#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 12:58:06 2020

@author: jgf5fz
"""
exec(open('initialize.py').read())

path = 'DAC_paper/final_figs/fig7_chart.pdf'
exe_ns = ns.astype(str) #creates string list of exe_n numbers to iterate through
exe_ns = list(exe_ns) #creates string list of exe_n numbers to iterate through

fontsize=12
resolution=1000

import matplotlib as mpl
mpl.rcParams.update(mpl.rcParamsDefault)
#folder = [query]
#create_folders(folder,fig_dir)
years = set_years(2010,2100)
#scratchpath = '/scratch/jgf5fz'
plt.style.use('seaborn-white')
plt.style.use('seaborn-paper')

fuel_dict = {
        'a oil':'oil',
        'a oil CCS':'oil CCS',
        'b natural gas':'natural gas',
        'b natural gas CCS':'natural gas CCS',
        'c coal':'coal',
        'c coal CCS':'coal CCS',
        'd biomass':'biomass',
        'd biomass CCS':'biomass CCS',
        'e nuclear':'nuclear',
        'f hydro':'renewables',
        'g wind':'renewables',
        'h solar':'renewables',
        'i geothermal':'renewables',
        'j traditional biomass':'biomass',
        }

dac_dict={'elect_td_ind':'dac electricity','process heat dac':'DAC process heat'}

legend_colors_dict={
        'oil':'saddlebrown',
        'oil CCS':'tan',
        'coal':'black',
        'coal CCS':'dimgray',
        'natural gas':'silver',
        'natural gas CCS':'lavender',
        'biomass':'limegreen',
        'biomass CCS':'lawngreen',
        'nuclear':'yellow',
        'renewables':'skyblue',
        'DAC process heat':'indigo'
        }

from cycler import cycler
c = plt.get_cmap('tab20').colors
plt.rcParams['axes.prop_cycle']=cycler(color=c)
def plot_energy(ax,n):
    n = str(n)
    col = 'fuel'
    query = 'energy_consumption'
    #fig, (ax0) = plt.subplots(nrows=1,ncols=1,figsize=(8,8)
    years = set_years(2010,2100)
    
    primary_energy = pd.read_csv(scratchpath+'/exe_'+n+'/queryout_primary_energy_consumption_with_CCS_by_region_direct_equivalent_global.csv',skiprows=1)
    df = primary_energy
    
    final_energy = pd.read_csv(scratchpath+'/exe_'+n+'/queryout_final_energy_consumption_by_sector_and_fuel_global.csv',skiprows=1)
    
    str_cols = ['scenario',col]
    df[str_cols] = df[str_cols].astype(str)
    scenario_name = get_scenario_name(df)
    df = df_plotting_prep(df,years,scenario_name,col,True)
    df = df.rename(columns = fuel_dict)
    df = df.groupby(by=df.columns,axis=1).sum()
    
    
    
    
    df = df[['natural gas CCS','natural gas','oil CCS','oil','coal CCS','coal','nuclear','renewables','biomass','biomass CCS']]
    
        
    df.index = df.index.astype(int)
    
    #adds dac process heat from final energy query to top of bars
    df1 = final_energy
    str_cols = ['scenario','input']
    df1[str_cols] = df1[str_cols].astype(str)
    df1 = df_plotting_prep(df1,years,scenario_name,'input',True)
    if 'process heat dac' in df1:
        df1 = df1['process heat dac'].astype(float)
        df1.index = df1.index.astype(int)
        df = pd.concat([df,df1],axis=1)
        df['natural gas CCS'] = df['natural gas CCS'] - df['process heat dac'] #subtract out dac process heat from natty gas CCS to avoid double counting
        #df['natural gas'] = df['natural gas'] - df['process heat dac']
        df = df.rename(columns={'process heat dac':'DAC process heat'})
    
    columns = list(df.columns)
    colors = []
    for i in range(len(columns)):
        colors.append(legend_colors_dict[columns[i]])
    new_label_order = ['biomass CCS','biomass','renewables','nuclear','coal','coal CCS','oil','oil CCS','natural gas','natural gas CCS']
    new_idx = []
    
    h,l = ax.get_legend_handles_labels()
    for i in range(len(new_label_order)):
        label = new_label_order[i]
        if label in l:
            old_idx = l.index(label)
            new_idx.append(old_idx)
    
    h = [h[i] for i in new_idx]
    l = [l[i] for i in new_idx]    
    
    
    
    df.plot.bar(ax=ax,stacked=True,color=colors,width=0.8,legend=None)
    df.to_csv(n+'energy.csv')
    
    col = 'input'
    
    

        
    h0,l0 = ax.get_legend_handles_labels()  
    l = l0
    h = h0
    for i in range(len(l0)):
        if l0[i] not in l:
            l.append(l0[i])
            h.append(h0[i])

    
    ax.tick_params(axis='both',labelsize=fontsize,direction='out',which='both',length=6)
    #plt.figlegend(reversed(h),reversed(l),fontsize=fontsize,bbox_to_anchor=(1.65,0.95))
    ax.set_ylabel('EJ-yr$^{-1}$',fontsize=fontsize)
    ax.tick_params(labelsize=fontsize)
    ax.set_ylim(0,1500)
    ax.axvline(2.5,color='darkred',linestyle='--')
    
#%%
def get_dac_energy(n):
    n = str(n)
    dac_energy = pd.read_csv(scratchpath+'/exe_'+n+'/queryout_inputs_by_tech_global.csv',skiprows=1)
    str_cols = ['technology','input']
    dac_energy[str_cols] = dac_energy[str_cols].astype(str)
    dropcols = ['scenario','region','sector','subsector']
    dac_energy=dac_energy.drop(dropcols,axis=1)
    if 'dac' in dac_energy.technology.values:
        dac_energy=dac_energy.loc[dac_energy['technology']=='dac']
        dac_energy=dac_energy.loc[dac_energy['Units']=='EJ']
        dac_energy = dac_energy.drop('technology',axis=1)
        dac_energy = dac_energy.drop('Units',axis=1)
        dac_energy = dac_energy.drop('Unnamed: 28',axis=1)
        
        dac_energy = dac_energy.set_index('input')
        
    else:
        dac_energy=0
        print(n+' has no dac')
    
    return(dac_energy)


def plot_diff_energy(ax,n1,n2):#n1 should be dac case
    #fig,ax0  = plt.subplots(nrows=1,ncols=1,figsize=(8,8))
    df = get_diff('queryout_primary_energy_consumption_with_CCS_by_region_direct_equivalent_global','fuel',n1,n2)
    print([k for k in fuel_dict])
    df = df[[k for k in fuel_dict]]
    df = df.rename(columns = fuel_dict)
    df = df.groupby(by=df.columns,axis=1).sum()


    df1 = df
    col_order = ['renewables','oil CCS','nuclear','biomass CCS','biomass','oil','coal','coal CCS','natural gas','natural gas CCS']
    col_order.reverse()
    df = df[col_order] 
    columns = list(df.columns)
        

    colors = []
    for i in range(len(columns)):
        colors.append(legend_colors_dict[columns[i]])    
    
    
    df.to_csv('diff_energy.csv')
    df.plot.bar(ax=ax,stacked=True,color=colors,width=0.85)
    df = df.sum(axis=1)
    ax.plot(df.values,color='#E57200',linestyle = '-',label='net difference',linewidth=2)
    ax.axhline(color='k')
    
    
    
    dac1 = get_dac_energy(n1)
    dac2 = get_dac_energy(n2)
    
    diff_dac = dac1-dac2
    diff_dac = diff_dac.drop('1990',axis=1)
    diff_dac = diff_dac.drop('2005',axis=1)
    diff_dac=diff_dac.T
    #diff_dac.drop([1990])
    #diff_dac.drop(0)
    
    diff_dac=diff_dac.rename(columns=dac_dict)
    diff_dac=diff_dac.drop('dac electricity',axis=1)
    print(diff_dac)
    #
    columns = list(diff_dac.columns)
        
        
    colors = []
    for i in range(len(columns)):
        colors.append(legend_colors_dict[columns[i]])    
    
    diff_dac.plot(ax=ax,stacked=True,color=colors,linewidth=2)
    diff_dac.to_csv('diff_dac_energy.csv')
    ax.tick_params(axis='both',labelsize=fontsize,direction='out',which='both',length=6)
    #ax.tick_params(axis='xaxis',rotation=90)
    ax.get_legend().remove()
    #plt.axhline(color='k')
    #plt.ylim(-200,500)
    
    #plt.legend(fontsize=fontsize,ncol=1,bbox_to_anchor=(1.5,1))
    #plt.title('Differences in energy demand: no DAC vs low-cost HT DAC')
    ax.set_ylabel('$\Delta$ EJ-yr$^{-1}$',fontsize=fontsize)
    ax.axvline(2.5,color='darkred',linestyle='--')#ax.set_xticks(rotation=90)


    
    
    
#%%
    
plt.figure(figsize=(8.5,8.5))
ax0 = plt.subplot(2,2,1) #upper left
ax1 = plt.subplot(2,2,2) #upper right
ax2 = plt.subplot(2,2,3) #lower left

ax0.set_title('a: low overshoot, DAC available',fontsize=fontsize,loc='left')
plot_energy(ax0,5)
ax0.set_xlabel('')

ax1.set_title('b: high overshoot, DAC available',fontsize=fontsize,loc='left')
plot_energy(ax1,7)
ax1.set_yticks([])
ax1.set_ylabel('')
ax1.set_xlabel('')

ax2.set_title('c: $\Delta$ energy demand, DAC vs no DAC',fontsize=fontsize,loc='left')
plot_diff_energy(ax2,5,13)
ax2.set_xlabel('')




plt.subplots_adjust(wspace=0.05,hspace=0.3)


plt.xticks(rotation=90)


legend_order = ['net difference','DAC process heat','biomass CCS','biomass','renewables','nuclear','coal','coal CCS','oil','oil CCS','natural gas','natural gas CCS']

h,l = fix_legend(ax2,legend_order)

hi,li = ax1.get_legend_handles_labels()#replace line legend with box legend
idx = li.index('DAC process heat')
l[l.index('DAC process heat')] = li[idx]
h[l.index('DAC process heat')] = hi[idx]

leg=ax2.legend(h,l,bbox_to_anchor=(1.75,1),fontsize=fontsize)

plt.savefig(path,bbox_inches='tight',dpi=resolution)
plt.show()    
    