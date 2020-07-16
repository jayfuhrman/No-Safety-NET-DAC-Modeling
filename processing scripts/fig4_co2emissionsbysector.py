#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 13:57:25 2020

@author: jgf5fz
"""
import initialize
exec(open('initialize.py').read())


fontsize = 16

col = 'sector'
query = 'co2_emisssions_no_bio_combined_aggregated'
bau = pd.read_csv('bau_net_emiss.csv')
bau = bau.set_index('year')

import matplotlib as mpl
mpl.rcParams.update(mpl.rcParamsDefault)
plt.style.use('seaborn-paper')
plt.style.use('seaborn-white')
#from matplotlib.ticker import FormatStrFormatter

title_dict = {
        '5':'b: Low overshoot, DAC available',
        '7':'c: High overshoot, DAC available',
        '13':'a: Low overshoot, no DAC',
        '9':'Low overshoot, high-cost DAC',
        '11':'High overshoot, high-cost DAC'
            
            
        }


#initial aggregation
aggregation_dict = {
        
        'airCO2':'direct air capture',
        'process heat dac':'direct air capture',
    
        'industrial feedstocks':'industry',
        
        'cement':'industry',
        'industrial energy use':'industry',
        'process heat cement':'industry',
        'N fertilizer':'industry',
        
        'H2 central production':'industry',
        'H2 forecourt production':'industry',
        
        
        'comm cooling':'buildings',
        'comm heating':'buildings',
        'comm others':'buildings',
        'resid cooling':'buildings',
        'resid heating':'buildings',
        'resid others':'buildings',
        
        'csp_backup':'electricity',
        'backup_electricity':'electricity',
        'elec_coal (IGCC CCS)':'electricity',
        'elec_coal (conv pul CCS)':'electricity',
        'elec_gas (CC CCS)':'electricity',
        'elec_refined liquids (CC CCS)':'electricity',
        'electricity':'electricity',
        

        'delivered biomass':'other energy transform',
        'delivered gas':'other energy transform',
        'district heat':'other energy transform',
        'refined liquids enduse':'other energy transform',
        'refined liquids industrial':'other energy transform',
        'gas pipeline':'other energy transform',
        'gas processing':'other energy transform',
        'wholesale gas':'other energy transform',
        
        'elec_biomass (IGCC CCS)':'bioelectricity',
        'elec_biomass (conv CCS)':'bioelectricity',
        
    
        
        'refining':'refining',
        
        'trn_aviation_intl':'transportation',
        'trn_freight':'transportation',
        'trn_freight_road':'transportation',
        'trn_pass':'transportation',
        'trn_pass_road':'transportation',
        'trn_pass_road_LDV':'transportation',
        'trn_pass_road_LDV_2W':'transportation',
        'trn_pass_road_LDV_4W':'transportation',
        'trn_pass_road_bus':'transportation',
        'trn_shipping_intl':'transportation',
        
        'unconventional oil production':'other energy transform',
        'All LandLeaf':'land use change'
        }

neg_col_names = {'industry':'industrial biofeedstocks',
                 'refining':'bioliquids refining'
                 } 

pos_col_names = {'industrial feedstocks':'industry',
                 'refining':'other energy transform',
                 #'unconventional oil production':'industry'
                 }

legend_colors_dict = {
        'direct air capture':'indigo',
        'industrial biofeedstocks':'mediumspringgreen',
        'bioliquids refining':'limegreen',
        'bioelectricity':'lawngreen',
        
        'buildings':'darkred',
        'electricity':'firebrick',
        'industry':'indianred',
        'other energy transform':'lightcoral',
        'transportation':'rosybrown',
        'unconventional oil production':'pink',
        'land use change':'darkolivegreen'
        }

def fix_legend(ax0,ax1):        
    h0,l0 = ax0.get_legend_handles_labels()
    h1,l1 = ax1.get_legend_handles_labels()
        
    #l0.reverse()
    #h0.reverse()
    l = l0
    h = h0
    for i in range(len(l1)):
        if l1[i] not in l:
            l.append(l1[i])
            h.append(h1[i])
    return h,l


str_cols = ['scenario',col,'Units']
years = set_years(2010,2100)


folder = [query]
create_folders(folder,fig_dir)

def plot_co2_emissions(n,ax,axn):
    fossil = pd.read_csv(scratchpath+'/exe_'+n+'/queryout_CO2_emissions_by_sector_no_bio_global.csv',skiprows=1)
    luc = pd.read_csv(scratchpath+'/exe_'+n+'/queryout_LUC_emissions_by_region_global.csv',skiprows=1)
    str_cols = ['scenario','LandLeaf','Units']
    luc[str_cols] = luc[str_cols].astype(str)
    scenario_name = get_scenario_name(luc)
    luc = df_plotting_prep(luc,years,scenario_name,'LandLeaf',True)
    str_cols = ['scenario',col,'Units']
    fossil[str_cols] = fossil[str_cols].astype(str)
    scenario_name = get_scenario_name(fossil)
    fossil = df_plotting_prep(fossil,years,scenario_name,col,True)
    
    df = pd.concat([fossil,luc],axis=1) #merges energy+industry and luc emissions together
    df = df/1000*44/12 # convert MtC to GtCO2
    df = df.rename(columns = aggregation_dict)
    df = df.groupby(by=df.columns,axis=1).sum()
    df.index = df.index.astype(int)
    
    net_emiss = df.sum(axis=1).to_frame()
    net_emiss.index=net_emiss.index.astype(int)
    
    

    df.to_csv(scratchpath+'/exe_'+n+'emissions.csv')
    dfneg = df.copy(deep=True)
    dfpos = df.copy(deep=True)
        
    dfneg[dfneg>0] = np.nan
    dfneg[dfneg==0] = np.nan
    dfneg = dfneg.dropna(how='all',axis =1)
    dfneg = dfneg.rename(columns = neg_col_names) #rename some remaining columns for clarity
    dfneg = dfneg.groupby(by=dfneg.columns,axis=1).sum()
    
    
    #print(dfneg)
    column_names = list(dfneg.columns)
    to_end = ['direct air capture','industrial biofeedstocks','bioelectricity','bioliquids refining','land use change'] #here, we specify the columns which we want to move to the end of the dataframe for plotting order
    for i in to_end:
        if i in column_names:
            #print(i)
            column_names.append(i)
            column_names.remove(i)
        #column_names = column_names
    dfneg = dfneg[column_names[::-1]]# reorders columns in the actual dataframe
    
    
    
    dfpos[dfpos<0] = np.nan
    dfpos[dfpos==0] = np.nan
    dfpos = dfpos.dropna(how='all',axis =1)
    dfpos = dfpos.rename(columns = pos_col_names) #rename some columns for clarity
    dfpos = dfpos.groupby(by=dfpos.columns,axis=1).sum() #aggregates columns with the same name
    
    
    column_names = list(dfpos.columns)
    to_end = ['land use change'] #here, we specify the columns which we want to move to the end of the dataframe for plotting order
    for i in to_end:
        if i in column_names:

            column_names.insert(0,column_names.pop(column_names.index(i)))
        
    dfpos = dfpos[column_names]
    

    
    if not dfneg.empty:
        #fig, (ax0,ax1) = plt.subplots(nrows=2,ncols=1,sharex=True,figsize=(11,8.5))
        
        #creating custom colorpalattes for stacked bar plots
        pos_columns = list(dfpos.columns)
        pos_colors = []
        for i in range(len(pos_columns)):
            pos_colors.append(legend_colors_dict[pos_columns[i]])        
        neg_colors=[]
        neg_columns = list(dfneg.columns)
        for i in range(len(neg_columns)):
            neg_colors.append(legend_colors_dict[neg_columns[i]])
        
        
        
        grosspos = dfpos.plot.bar(ax=ax,stacked=True,color=pos_colors,width=0.85)
        grossneg = dfneg.plot.bar(ax=axn,stacked=True,color=neg_colors,width=0.85)
        
        
        #sets ylims for equal scaling between charts
        ymin0, ymax0 = ax.get_ylim()
        ymin1, ymax1 = axn.get_ylim()
        #ylim_new = max(abs(ymax0),abs(ymin1))
        ylim_new = 47
        ax.set_ylim(-ylim_new-5,ylim_new+5)
        axn.set_ylim(-ylim_new-5,ylim_new+5)
        ax.get_legend().remove()
        axn.get_legend().remove()
        
        ax.axhline(color='k',linewidth=0.5)
        
        ax.tick_params(axis='both',labelsize=fontsize,direction='out',which='both',length=6)
        axn.tick_params(axis='both',labelsize=fontsize,direction='out',which='both',length=6)
        
        ax.plot(net_emiss.values,color='k',linewidth = 2,label='net CO$_2$ emissions')
        axn.plot(net_emiss.values,color='k',linewidth = 2)
        

def plot_ref_emissions(ax):
        reference_scenario = '../gcam_reference_scenario'
        fossil = pd.read_csv(reference_scenario+'/queryout_CO2_emissions_by_sector_no_bio_global.csv',skiprows=1)
        luc = pd.read_csv(reference_scenario+'/queryout_LUC_emissions_by_region_global.csv',skiprows=1)
        fossil = df_plotting_prep(fossil,years,'referencenoDAC',col,True)
        luc = df_plotting_prep(luc,years,'referencenoDAC','LandLeaf',True)
        df = pd.concat([fossil,luc],axis=1)
        df = df.sum(axis=1)
        df = df/1000*44/12
        df.index = df.index.astype(int)
        label_name='no climate policy'
        
        line2, = ax.plot(df.values,color='tomato',linestyle='-',label=label_name,linewidth = 2)
        
        ax.annotate('',xy=(5,51.08),xytext=(4.9,51.08-(51.08-48.27)/10),arrowprops=dict(arrowstyle='simple',color='tomato',linewidth=2))











fig = plt.figure(figsize=(11,10))
ax0 = plt.subplot(2,2,1) #upper left
ax1 = plt.subplot(2,2,3) #lower left
ax2 = plt.subplot(2,2,4) #lower right


ax0n = ax0.twinx()
ax1n = ax1.twinx()
ax2n = ax2.twinx()

ax0n.set_yticks([])
ax1n.set_yticks([])
ax2n.set_yticks([])

ax2.set_yticks([])
ax0.set_xticks([])



plot_co2_emissions('13',ax0,ax0n)
ax0.set_title('a: Low overshoot, no DAC',loc='left',fontsize=fontsize)


plot_co2_emissions('5',ax1,ax1n)
ax1.set_title('b: Low overshoot, DAC available',loc='left',fontsize=fontsize)


plot_co2_emissions('7',ax2,ax2n)
ax2.set_title('c: High overshoot, DAC available',loc='left',fontsize=fontsize)


ax0.set_ylabel('GtCO$_2$ yr$^{-1}$',fontsize=fontsize)
ax1.set_ylabel('GtCO$_2$ yr$^{-1}$',fontsize=fontsize)

plot_ref_emissions(ax0)
plot_ref_emissions(ax1)
plot_ref_emissions(ax2)

ax1.set_xlabel('')
ax2.set_xlabel('')

#here, we explicitly cast the order we want the legend in to avoid duplicates and ensure we get everything from all subplots in the legend
legend_order=['no climate policy','transportation','other energy transform','industry','electricity','buildings',
              'land use change','bioliquids refining','bioelectricity','industrial biofeedstocks','direct air capture','net CO$_2$ emissions']
idx = []
h1,l1 = ax1.get_legend_handles_labels()
h1n,l1n = ax1n.get_legend_handles_labels()
h0,l0 = ax0n.get_legend_handles_labels()

labels = l1+l1n+l0
handles = h1+h1n+h0

for i in range(len(legend_order)):
    index=labels.index(legend_order[i])
    idx.append(index)

h = []
l = []

for i in range(len(idx)):
    h.append(handles[idx[i]])
    l.append(labels[idx[i]])



plt.figlegend(h,l,bbox_to_anchor=(0.82,0.89),fontsize=fontsize)

plt.subplots_adjust(wspace=0.05,hspace=0.12)


path = 'DAC_paper/final_figs/fig4_chart.pdf'
plt.savefig(path,bbox_inches='tight',dpi=resolution)

plt.show()