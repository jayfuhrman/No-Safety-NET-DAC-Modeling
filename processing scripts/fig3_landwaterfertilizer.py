#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 10:10:47 2020

@author: jgf5fz
"""
query='fig3'
exec(open('initialize.py').read())
fontsize=12
exe_ns = ['13']
legend_colors_dict = {
        'bioenergy crop cultivation':'lawngreen',
        'bioelectricity CCS':'limegreen',
        'forest':'forestgreen',
        'food crop':'cornflowerblue',
        'non-food crop':'sienna',
        'Fodder':'darksalmon',
        'pasture':'thistle',
        'grassland':'darkseagreen',
        'non-arable land':'whitesmoke',
        'grassland/shrubland':'khaki',
        'other arable land':'cadetblue',
        'urban land':'grey',
        'electricity':'gold',
        'municipal water':'aquamarine',
        'meat and dairy':'lightcoral',
        'industry':'slategrey',
        'Fertilizer Exports':'silver',
        'direct air capture':'indigo',
        'afforestation':'forestgreen'}



aggregation_dict={
        #land and fertilizer
        'ProtectedUnmanagedPasture':'pasture',
        'UnmanagedPasture':'pasture',
        'Pasture':'pasture',
        
        'ProtectedUnmanagedForest':'forest',
        'UnmanagedForest':'forest',
        'Forest':'forest',
        
        'Tundra':'non-arable land',
        'RockIceDesert':'non-arable land',
        
        'SugarCrop':'non-food crop',
        'OilCrop':'non-food crop',
        'biomass_tree':'bioenergy crop cultivation',
        'biomass_grass':'bioenergy crop cultivation',
        'PalmFruit':'non-food crop',
        'biomass':'bioenergy crop cultivation',
        'biomassGrass':'bioenergy crop cultivation',
        'biomassTree':'bioenergy crop cultivation',
        
        'Rice':'food crop',
        'Wheat':'food crop',
        'MiscCrop':'food crop',
        'RootTuber':'food crop',
        'OtherGrain':'food crop',
        'Corn':'food crop',
        
        'FiberCrop':'non-food crop',
        
        'UrbanLand':'non-arable land',
        
        'OtherArableLand':'other arable land',
        
        'Shrubland':'grassland/shrubland',
        'ProtectedShrubland':'grassland/shrubland',
        
        'Grassland':'grassland/shrubland',
        'ProtectedGrassland':'grassland/shrubland',
        
        'FodderHerb':'non-food crop',
        'FodderGrass':'non-food crop',
        
        'Exports_fertilizer':'Fertilizer Exports',
        
        'municipal water':'municipal water',
        'ces':'direct air capture',
        #water
        'industry':'industry',
        'regional coal':'industry',
        'regional natural gas':'industry',
        'regional oil':'industry',
        'unconventional oil production':'industry',
        
        'nuclearFuelGenII':'electricity',
        'nuclearFuelGenIII':'electricity',
        'elec_biomass (conv CCS)':'bioelectricity CCS',
        'elec_coal (conv pul CCS)':'electricity',
        'elec_refined liquids':'electricity',
        'elec_gas (CC CCS)':'electricity',
        'elec_biomass (IGCC CCS)':'bioelectricity CCS',
        'elec_coal (IGCC CCS)':'electricity',
        'elec_refined liquids (CC CCS)':'electricity',
        
        'Dairy':'meat and dairy',
        'SheepGoat':'meat and dairy',
        'Pork':'meat and dairy',
        'Poultry':'meat and dairy',
        'Beef':'meat and dairy'}
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
        'low-temp-heat-dac':'dac waste heat'}

legend_colors_dict_en={
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
        'dac process heat':'darkslateblue'
        }


land_col_order = ['bioenergy crop cultivation',
                  'forest',
                  'food crop',
                  'pasture',
                  'grassland/shrubland',
                  'non-food crop',
                  'other arable land',
                  'non-arable land'] #defines the order of the land columns for plotting

    
import matplotlib as mpl
from matplotlib import gridspec
mpl.rcParams.update(mpl.rcParamsDefault)

#plt.style.use('seaborn-colorblind')
plt.style.use('seaborn-paper')
plt.style.use('seaborn-white')
for n in exe_ns:
    fig = plt.figure(figsize=(5,13))

    str_cols = ['scenario','Units']
    years = set_years(2010,2100)
    folder = [query]
    create_folders(folder,fig_dir) 
    from cycler import cycler
    c = plt.get_cmap('tab20').colors
    plt.rcParams['axes.prop_cycle']=cycler(color=c)
    

    
    
    col = 'fuel'
    #query = 'energy_consumption'


    ax0 = plt.subplot(4,1,1)
    
    #years = set_years(2010,2100)
    
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
        df['natural gas CCS'] = df['natural gas CCS'] - df['process heat dac']
        df = df.rename(columns={'process heat dac':'dac process heat'})
    #    plt.plot(df1,label='dac process heat',color='grey')
    #    plt.fill_between(years.astype(np.float),df1.values,hatch='\\',edgecolor='grey',facecolor='none')
    
    
    columns = list(df.columns)
    colors = []
    for i in range(len(columns)):
        colors.append(legend_colors_dict_en[columns[i]])
    new_label_order = ['biomass CCS','biomass','renewables','nuclear','coal','coal CCS','oil','oil CCS','natural gas','natural gas CCS']
    new_idx = []
    h,l = ax0.get_legend_handles_labels()
    for i in range(len(new_label_order)):
        label = new_label_order[i]
        if label in l:
            old_idx = l.index(label)
            new_idx.append(old_idx)
    
    h = [h[i] for i in new_idx]
    l = [l[i] for i in new_idx]    
    
    
    
    df.plot.bar(ax=ax0,stacked=True,color=colors,width=0.8,legend=None)
    
    
        
    h0,l0 = ax0.get_legend_handles_labels()  
    l = l0
    h = h0
    for i in range(len(l0)):
        if l0[i] not in l:
            l.append(l0[i])
            h.append(h0[i])

    ax0.legend(reversed(h),reversed(l),bbox_to_anchor=(1.02,1.10),fontsize=fontsize)
    ax0.set_title('a: Primary energy',loc='left',fontsize=fontsize)
    ax0.set_ylabel('EJ-yr$^{-1}$',fontsize=fontsize) 
    
    ax0.annotate('Start of climate policy',xy=(2.5,900),xytext=(4,925),fontsize=fontsize,color='darkred',
                 arrowprops=dict(arrowstyle='simple',facecolor='darkred'))
    

    
    
    #land area
    
    ax1 = plt.subplot(4,1,3)
    land_area = pd.read_csv(scratchpath+'/exe_'+n+'/queryout_land_allocation_by_crop_global.csv',skiprows=1)
    df = land_area
    col = 'LandLeaf'
    str_cols = ['scenario',col]
    df[str_cols] = df[str_cols].astype(str)
    scenario_name = get_scenario_name(df)
    df = df_plotting_prep(df,years,scenario_name,col,True)
    df = df.rename(columns = aggregation_dict)
    df = df.groupby(by=df.columns,axis=1).sum()
    df = df/1000
    
    
    
    df = df[land_col_order]
    #df.plot.area(ax=ax0,linewidth=0)
    
    land = df
    
    first_row = land.iloc[[0]].values[0]
    landprime = land.apply(lambda row: row-first_row, axis=1)
    df = landprime
    
    column_names = list(df.columns)
    to_end = land_col_order #here, we specify the columns which we want to move to the end of the dataframe for plotting order
    
    for i in to_end:
        if i in column_names:

            column_names.append(i)
            column_names.remove(i)
    
    df = df[column_names]
    
    columns = list(df.columns)
    
    colors = []
    for i in range(len(columns)):
        colors.append(legend_colors_dict[columns[i]])    
    
    
    
    df.to_csv(scratchpath+'/exe_'+n+'/tot_land.csv')    
    df.plot.bar(ax=ax1,stacked=True,color=colors,width=0.85)
    h,l = ax1.get_legend_handles_labels() 
    #diff plots treat legends differently so to get everything to show up in order on the legend we explicitly switch forest and bioenergy on the legend
    i1 = l.index('forest')
    i2 = l.index('bioenergy crop cultivation')
    l[i1],l[i2]=l[i2],l[i1]
    h[i1],h[i2]=h[i2],h[i1]
 
    ax1.legend(h,l,bbox_to_anchor=(1.02,1),fontsize=fontsize)
    ax1.xaxis.set_ticklabels([])
    ax1.set_title('c: Land use ($\Delta$ from 2010)',loc='left',fontsize=fontsize)
    ax1.set_ylabel(r'$\Delta$ Mkm$^2$',fontsize=fontsize)
    ax1.axhline(color='k')
    ##########
    
    
    #water withdrawals
        
    ax2 = plt.subplot(4,1,2)
        
    
    water_withdrawals = pd.read_csv(scratchpath+'/exe_'+n+'/queryout_water_consumption_by_sector_global.csv',skiprows=1)
    df = water_withdrawals
    col = 'sector'
    str_cols = ['scenario',col]
    df[str_cols] = df[str_cols].astype(str)
    scenario_name = get_scenario_name(df)
    df = df_plotting_prep(df,years,scenario_name,col,True)
    df = df.rename(columns = aggregation_dict)
    df = df.groupby(by=df.columns,axis=1).sum()
    
    
    column_names = list(df.columns)
    to_end = ['food crop','meat and dairy','non-food crop','electricity','industry','municipal water','bioelectricity CCS','bioenergy crop cultivation','direct air capture'] #here, we specify the columns which we want to move to the end of the dataframe for plotting order
    
    for i in to_end:
        if i in column_names:

            column_names.append(i)
            column_names.remove(i)
    
    df = df[column_names]
    
    
    
    h,l = ax2.get_legend_handles_labels()

    columns = list(df.columns)
    
    colors = []
    for i in range(len(columns)):
        colors.append(legend_colors_dict[columns[i]])    
    
    df.to_csv(scratchpath+'/exe_'+n+'/water_consumption.csv')    
    df.plot.bar(ax=ax2,stacked=True,color=colors,width=0.85)
    h,l = ax2.get_legend_handles_labels()       

    ax2.legend(reversed(h),reversed(l),bbox_to_anchor=(1.02,1),fontsize=fontsize)
    ax2.set_ylabel('km$^3$-yr$^{-1}$',fontsize=fontsize)
    
    ax2.set_title('b: Water consumption',loc='left',fontsize=fontsize)
    ax2.xaxis.set_ticklabels([])
    
    
    
    
    
    ###
    #fertilizer

    ax3 = plt.subplot(4,1,4)
    str_cols = ['scenario','Units']
    fertilizer = pd.read_csv(scratchpath+'/exe_'+n+'/queryout_fertilizer_consumption_by_crop_type_global.csv',skiprows=1)
    df = fertilizer
    df[str_cols] = df[str_cols].astype(str)
    scenario_name = get_scenario_name(df)
    df = df_plotting_prep(df,years,scenario_name,'sector',True)
    
    df = df.rename(columns = aggregation_dict)
    df = df.groupby(by=df.columns,axis=1).sum()
    df = df.drop('Fertilizer Exports',axis=1)
    df.index = df.index.astype(int)
    
    column_names = list(df.columns)
    to_end = ['food crop','non-food crop','bioenergy crop cultivation'] #here, we specify the columns which we want to move to the end of the dataframe for plotting order
    
    for i in to_end:
        if i in column_names:

            column_names.append(i)
            column_names.remove(i)
    
    df = df[column_names]

    columns = list(df.columns)     
    colors = []
    for i in range(len(columns)):
        colors.append(legend_colors_dict[columns[i]])    
    df.to_csv(scratchpath+'/exe_'+n+'/fertilizer.csv')    
    df.plot.bar(ax=ax3,stacked=True,color=colors,width=0.85)
    
    h,l = ax3.get_legend_handles_labels()
    ax3.legend(reversed(h),reversed(l),bbox_to_anchor=(1.02,1),fontsize=fontsize)
    ax3.set_ylabel('MtN-yr$^{-1}$',fontsize=fontsize)
    ax3.set_title('d: Fertilizer demand',loc='left',fontsize=fontsize)
   

    path =  fig_dir+'/'+query+'/'+query+scenario_name+'.png'

    
    ax0.xaxis.set_ticklabels([])
    ax0.set_xlabel('')
    ax1.set_xlabel('')
    ax2.set_xlabel('')
    ax3.set_xlabel('')
    
    for ax in [ax0,ax1,ax2,ax3]:
        ax.tick_params(axis='both',labelsize=fontsize,direction='out',which='both',length=6)
        ax.axvline(2.5,color='darkred',linestyle='--')
        #ax.xaxis.set_ticklabels([])
    
    path = 'DAC_paper/final_figs/fig3.pdf'
    plt.savefig(path,bbox_inches='tight',dpi=resolution)
    #print('Saved to'+path)

    #ax0.set_title(scenario_name)

    
    plt.show()