#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  2 13:35:51 2020

@author: jgf5fz
"""
#scratchpath = '/scratch/jgf5fz'
fontsize=10
years = set_years(2010,2100)
legend_colors_dict_lw = {
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



aggregation_dict_lw={
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
def water_plotter(ax,n,query,nets_only,fontsize,ymax):
        
    #fig = plt.figure(figsize=(8,8))
    
    luc = pd.read_csv(scratchpath+'/exe_'+n+'/queryout_LUC_emissions_by_region_global.csv',skiprows=1)
    #luc1=luc
    
    water = pd.read_csv(scratchpath+'/exe_'+n+'/queryout_'+query+'_global.csv',skiprows=1)
    df = water
    col = 'sector'
    str_cols = ['scenario',col]
    df[str_cols] = df[str_cols].astype(str)
    scenario_name = get_scenario_name(df)
    df = df_plotting_prep(df,years,scenario_name,col,True)
    df = df.rename(columns = aggregation_dict_lw)
    df = df.groupby(by=df.columns,axis=1).sum()
    df.index=df.index.astype(int)
    
    col = 'LandLeaf'
    str_cols = ['scenario',col]
    luc[str_cols] = luc[str_cols].astype(str)
    luc = df_plotting_prep(luc,years,scenario_name,col,False)
    luc.columns=['AF']
    #luc = luc.groupby(by=df.columns,axis=1).sum()
    luc.index=luc.index.astype(int)
    luc['AF']=luc['AF']/1000 #convert to GtC
    luc['AF']=luc['AF']*-1765 #convert to km3 H2O b
    luc['AF'][2010]=0
    luc['AF'][2015]=0
    luc['AF'][2020]=0
    luc= luc.rename(columns = {'AF':'Afforestation'})
    column_names = list(df.columns)
    
    #print(column_names)
    if query == 'biophysical_water_demand_by_crop_type':
        df = pd.concat([df,luc],axis=1)
    #print(df)
        column_names = list(df.columns)
        to_end = ['bioelectricity CCS','bioenergy crop irrigation','direct air capture','Afforestation'] #here, we specify the columns which we want to move to the end of the dataframe for plotting order
    

    to_end = ['food crop','meat and dairy','non-food crop','municipal water','industry','electricity','bioelectricity CCS','bioenergy crop cultivation','direct air capture']
    
    if nets_only == True:
        to_end = ['bioelectricity CCS','bioenergy crop cultivation','direct air capture']
        
        
    if query =='water_withdrawals_by_sector' or query == 'water_consumption_by_sector':
        column_names = list(df.columns)
        for i in to_end:
            if i in column_names:
                column_names.append(i)
                column_names.remove(i)
            else:
                to_end.remove(i)
        #print(to_end,column_names)
        df = df[to_end]
    
    
    
    h,l = ax.get_legend_handles_labels()
    
    columns = list(df.columns)
    
    
    colors = []
    for i in range(len(columns)):
        colors.append(legend_colors_dict_lw[columns[i]])    
    
    df.plot.bar(ax=ax,stacked=True,color=colors,width=0.85)
    h,l = ax.get_legend_handles_labels()       
    
    ax.legend(reversed(h),reversed(l),bbox_to_anchor=(1.02,1),fontsize=fontsize)
    ax.set_ylabel('km$^3$-yr$^{-1}$',fontsize=fontsize)
    ax.set_ylim(0,ymax)
    #ax2.xaxis.set_ticklabels([])
    df.to_csv(n+'watercons.csv')
    #plt.title(title_dict[n],loc='left',fontsize=fontsize)
    ax.tick_params(axis='both',labelsize=fontsize,direction='out',which='both',length=6)




def water_df_prep(n,query,year):    
    n = str(n)
    luc = pd.read_csv(scratchpath+'/exe_'+n+'/queryout_LUC_emissions_by_region_global.csv',skiprows=1)
    #luc1=luc
    
    water = pd.read_csv(scratchpath+'/exe_'+n+'/queryout_'+query+'_global.csv',skiprows=1)
    df = water
    col = 'sector'
    str_cols = ['scenario',col]
    df[str_cols] = df[str_cols].astype(str)
    scenario_name = get_scenario_name(df)
    df = df_plotting_prep(df,years,scenario_name,col,True)
    df = df.rename(columns = aggregation_dict_lw)
    df = df.groupby(by=df.columns,axis=1).sum()
    df.index=df.index.astype(int)
    
    col = 'LandLeaf'
    str_cols = ['scenario',col]
    luc[str_cols] = luc[str_cols].astype(str)
    luc = df_plotting_prep(luc,years,scenario_name,col,False)
    luc.columns=['AF']
    #luc = luc.groupby(by=df.columns,axis=1).sum()
    luc.index=luc.index.astype(int)
    luc['AF']=luc['AF']/1000 #convert to GtC
    luc['AF']=luc['AF']*-1765 #convert to km3 H2O b
    luc['AF'][2010]=0
    luc['AF'][2015]=0
    luc['AF'][2020]=0
    luc= luc.rename(columns = {'AF':'afforestation'})
    column_names = list(df.columns)
    df = df.rename(columns = aggregation_dict_lw)
    to_end = ['bioelectricity CCS','bioenergy crop irrigation','direct air capture']
    if query == 'biophysical_water_demand_by_crop_type':
        df = pd.concat([df,luc],axis=1)
    #print(df)
        column_names = list(df.columns)
        to_end = ['bioelectricity CCS','bioenergy crop cultivation','direct air capture','afforestation'] #here, we specify the columns which we want to move to the end of the dataframe for plotting order
    
    for i in to_end:
        if i in column_names:
    
            column_names.append(i)
            column_names.remove(i)
    
    df = df[column_names]
    if query =='water_withdrawals_by_sector' or query == 'water_consumption_by_sector':
        column_names = list(df.columns)
        for i in to_end:
            if i not in column_names:
                to_end.remove(i)
    df = df.loc[year]
    return df


def fix_colors(df,legend_dict):
    column_names = list(df.columns)
    colors = []
    for i in range(len(column_names)):
        colors.append(legend_dict[column_names[i]])
    return colors

#fontsize=24
#fig = plt.figure(figsize=(8,8))
#ax1 = plt.subplot(1,1,1)    

def plot_diff_water(n1,n2,ax):
    df1= water_df_prep(n1,'biophysical_water_demand_by_crop_type',2050)
    df2= water_df_prep(n2,'biophysical_water_demand_by_crop_type',2050)
    df = df1-df2
    df = df.to_frame()
    df = df.T
    df = df.rename(columns=aggregation_dict_lw)
    df = df.groupby(by=df.columns,axis=1).sum()
    
    et = df.rename(index={2050:'biophysical'})
    
    df1= water_df_prep(n1,'water_withdrawals_by_sector',2050)
    df2= water_df_prep(n2,'water_withdrawals_by_sector',2050)
    if 'direct air capture' not in df2.index:
        df2['direct air capture']=0
    df = df1-df2
    df = df.to_frame()
    df = df.T
    df = df.rename(columns=aggregation_dict_lw)
    df = df.groupby(by=df.columns,axis=1).sum()
    
    w = df.rename(index={2050:'withdrawals'})
    
    
    df1= water_df_prep(n1,'water_consumption_by_sector',2050)
    df2= water_df_prep(n2,'water_consumption_by_sector',2050)
    if 'direct air capture' not in df2.index:
        df2['direct air capture']=0
    df = df1-df2
    df = df.to_frame()
    df = df.T
    df = df.rename(columns=aggregation_dict_lw)
    df = df.groupby(by=df.columns,axis=1).sum()
    
    c = df.rename(index={2050:'consumption'})
    
    
    #diff_c = c.sum(axis=1)
    #plt.axhline(diff_c.values)
    #diff_w = w.sum(axis=1)
    #plt.axhline(diff_w.values)
    
    df = pd.concat([et,w,c])
    df = df.fillna(0)
    print(df)
    categories = ['afforestation','direct air capture','food crop','non-food crop','meat and dairy','bioelectricity CCS','bioenergy crop cultivation','electricity','industry','municipal water']
    #manually set columns so that negative emissions are closest to the y axis to allow direct visual comparison
    df = df[categories]
    colors = fix_colors(df,legend_colors_dict_lw)
    df.to_csv('diff_water.csv')
    df.plot.bar(ax=ax,stacked=True,color=colors,width=0.7)
    
    ax.axhline(color='k')
    #ax.legend()
    ax.set_ylabel('$\Delta$ km$^3$-yr$^{-1}$',fontsize=fontsize)
    #plt.legend(bbox_to_anchor=(1.15,0.95),fontsize=fontsize)
    #ax.set_title('c: $\Delta$ water use in 2050, DAC vs no DAC',loc='left',fontsize=fontsize)
    ax.tick_params(axis='both',labelsize=fontsize,direction='out',which='both',length=6,labelrotation=360)
    ax.set_ylim(-1100,550)
    

#%%
col = 'sector'
neg_col_names = {'industry':'industrial biofeedstocks',
                 'refining':'bioliquids refining'
                 } 

pos_col_names = {'industrial feedstocks':'industry',
                 'refining':'other energy transform',
                 #'unconventional oil production':'industry'
                 }

aggregation_dict_emis = {
        
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

legend_colors_dict_emis = {
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

def get_aggregated_emissions(n):
    fossil = pd.read_csv(scratchpath+'/exe_'+n+'/queryout_CO2_emissions_by_sector_no_bio_global.csv',skiprows=1)
    luc = pd.read_csv(scratchpath+'/exe_'+n+'/queryout_LUC_emissions_by_region_global.csv',skiprows=1)
    str_cols = ['scenario','LandLeaf','Units']
    luc[str_cols] = luc[str_cols].astype(str)
    scenario_name = get_scenario_name(luc)
    luc = df_plotting_prep(luc,years,scenario_name,'LandLeaf',True)
    str_cols = ['scenario','sector','Units']
    fossil[str_cols] = fossil[str_cols].astype(str)
    scenario_name = get_scenario_name(fossil)
    fossil = df_plotting_prep(fossil,years,scenario_name,col,True)
    
    df = pd.concat([fossil,luc],axis=1) #merges energy+industry and luc emissions together
    df = df/1000*44/12 # convert MtC to GtCO2
    
    df = df.rename(columns = aggregation_dict_emis)
    df = df.groupby(by=df.columns,axis=1).sum()
    df.index = df.index.astype(int)
    
    dfneg = df.copy(deep=True)
    dfpos = df.copy(deep=True)
        
    dfneg[dfneg>0] = np.nan
    dfneg[dfneg==0] = np.nan
    dfneg = dfneg.dropna(how='all',axis =1)
    dfneg = dfneg.rename(columns = neg_col_names) #rename some remaining columns for clarity
    dfneg = dfneg.groupby(by=dfneg.columns,axis=1).sum()
    
    dfpos[dfpos<0] = np.nan
    dfpos[dfpos==0] = np.nan
    dfpos = dfpos.dropna(how='all',axis =1)
    dfpos = dfpos.rename(columns = pos_col_names) #rename some columns for clarity
    dfpos = dfpos.groupby(by=dfpos.columns,axis=1).sum() #aggregates columns with the same name

    return df,dfneg,dfpos

def subtraction_prep(df):
    """if a sector doesn't show up in the query because it is not deployed, 
    we don't want to end up with Nan when we try to subtract from scenarios in which it is deployed
    therefore we add a column of all zeros if sector doesn't appear in the dataframe"""
    
    if 'direct air capture' not in df.columns:
        df['direct air capture']=0
    if 'industrial biofeedstocks' not in df.columns:
        df['industrial biofeedstocks']=0
    return df
      

def get_diff_emiss(df1,df2):
    df1 = subtraction_prep(df1)
    df2 = subtraction_prep(df2)
    #print(df2)
    return df1-df2



    

def get_spot_year(df,year):
    df = df.loc[[year]]
    return df

def plot_diff_emissions(n1,n2,ax):
    df1,dfneg1,dfpos1 =  get_aggregated_emissions(n1) 
    df2,dfneg2,dfpos2 =  get_aggregated_emissions(n2)
    
    diff_neg_emiss = get_diff_emiss(dfneg1,dfneg2)
    diff_mitigation = get_diff_emiss(dfpos1,dfpos2)
    
    
    df = get_spot_year(diff_neg_emiss,2050)
    df1 = get_spot_year(diff_mitigation,2050)
    
    
    colors = fix_colors(df1,legend_colors_dict_emis)
    
    
    
    
    #df.plot.bar(stacked=True,color=fix_colors(df))
    #df1.plot.bar(stacked=True,color=fix_colors(df1))
    df = df.rename(index={2050:'$\Delta$ NETs'})
    df1 = df1.rename(index={2050:'$\Delta$ abatement'})
    
    df = pd.concat([df,df1])
    #fig = plt.figure(figsize=(8,8))
    df.to_csv('fig6emiss.csv') 
    df = df.plot.bar(stacked=True,color=fix_colors(df,legend_colors_dict_emis),fontsize=fontsize,ax=ax)
    ax.axhline(color='k')
    #plt.legend(fontsize=fontsize,bbox_to_anchor=(1.35,0.8))
    ax.set_ylabel('$\Delta$ GtCO$_2$-yr$^{-1}$',fontsize=fontsize)
    ax.yaxis.set_label_position('right')
    plt.xticks(rotation=360)
    ax.set_yticks(np.arange(-10,20,5))
    ax.yaxis.tick_right()
    ax.yaxis.set_ticks_position('both')
    
    ax.tick_params(axis='both',direction='out',length=6,labelsize=fontsize)







resolution=1000


#fontsize=16

plt.figure(figsize=(8.5,8.5))
ax0 = plt.subplot(2,2,1) #upper left
ax1 = plt.subplot(2,2,2) #upper right
ax2 = plt.subplot(2,2,3) #lower left
ax3 = plt.subplot(2,2,4) #lower right





water_plotter(ax0,'5','water_consumption_by_sector',True,fontsize,325)
water_plotter(ax1,'7','water_consumption_by_sector',True,fontsize,325)
#water_plotter(ax2,'5','water_withdrawals_by_sector',True,fontsize,650)
#water_plotter(ax3,'7','water_withdrawals_by_sector',True,fontsize,650)
plot_diff_water(5,13,ax2)
plot_diff_emissions('13','5',ax3)








ax1.set_yticks([])
ax1.set_ylabel('')

ax3.yaxis.tick_right()

ax0.set_xlabel('')
ax1.set_xlabel('')
ax2.set_xlabel('')
ax3.set_xlabel('')
ax0.get_legend().remove()
ax1.get_legend().remove()
ax2.get_legend().remove()
ax3.get_legend().remove()


ax0.set_title('a: NETs water consumption, low overshoot',fontsize=fontsize,loc='left')
ax1.set_title('b: NETs water consumption, high overshoot',fontsize=fontsize,loc='left')
ax2.set_title('c: $\Delta$ 2050 water use, DAC vs no DAC',fontsize=fontsize,loc='left')
ax3.set_title('d: $\Delta$ 2050 CO$_2$ emissions, DAC vs no DAC',fontsize=fontsize,loc='left')

legend_order=['direct air capture','bioenergy crop cultivation','bioelectricity CCS','afforestation',
              'food crop','non-food crop','meat and dairy',
              'electricity','industry','municipal water']

    
h,l=fix_legend(ax2,legend_order)    

leg=ax2.legend(h,l,bbox_to_anchor=(0.85,-0.125),fontsize=fontsize,title='Water use (a-c)')
leg.get_title().set_fontsize(fontsize)


emiss_legend=['direct air capture','bioelectricity','bioliquids refining','industrial biofeedstocks','land use change',
              'buildings','electricity','industry','other energy transform','transportation']
h,l = fix_legend(ax3,emiss_legend)

leg1 = ax3.legend(h,l,fontsize=fontsize,bbox_to_anchor=(0.85,-0.125),title='CO$_2$ emissions (d)')
leg1.get_title().set_fontsize(fontsize)

plt.subplots_adjust(wspace=0.05,hspace=0.275)
path = 'DAC_paper/final_figs/fig6_chart.pdf'

plt.savefig(path,bbox_inches='tight',dpi=resolution)
plt.show()
