#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  2 13:08:01 2020

@author: jgf5fz
"""
exec(open('initialize.py').read())

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

resolution=1000
fontsize=24

def fix_legend(ax,legend_order):
    idx = []
    h1,l1 = ax.get_legend_handles_labels()
    for i in range(len(legend_order)):
        index=l1.index(legend_order[i])
        idx.append(index)

    h = []
    l = []
    
    for i in range(len(idx)):
        h.append(h1[idx[i]])
        l.append(l1[idx[i]])
    return h,l



years = set_years(2010,2100)

def plot_diff_land(filename,n1,n2):

    fig,ax0 = plt.subplots(nrows=1,ncols=1,figsize=(8,4))
    df = get_diff('queryout_land_allocation_by_crop_global','LandLeaf',n1,n2)
    df = df.rename(columns = aggregation_dict)
    df = df.groupby(by=df.columns,axis=1).sum()
    df = df/1000
    
    columns = list(df.columns)
        
        
    colors = []
    for i in range(len(columns)):
        colors.append(legend_colors_dict[columns[i]])
    df.to_csv('fig5diffland.csv')
    df.plot.bar(ax=ax0,stacked=True,color=colors,width=0.85)
    plt.tick_params(axis='both',labelsize=fontsize,direction='out',which='both',length=6)
    ax0.axhline(color='k')
    plt.ylabel(r'$\Delta$ Mkm$^2$',fontsize=fontsize)
    h,l=fix_legend(ax0,['pasture','other arable land','non-food crop','grassland/shrubland','food crop','bioenergy crop cultivation','forest'])
    plt.legend(h,l,fontsize=fontsize,bbox_to_anchor=(1,1.1))
    ax0.set_xlabel('')
    ax0.set_ylim(-1.55,1.55)
    ax0.annotate('b:',xy=(-0.18,1.03),xycoords='axes fraction',fontsize=fontsize)
    plt.title('$\Delta$ land use, low overshoot',loc='left',fontsize=fontsize)
    plt.savefig('DAC_paper/final_figs/fig5_chart.pdf',dpi=resolution,bbox_inches='tight')
    
    
    plt.show()

plot_diff_land('diffland',5,13)