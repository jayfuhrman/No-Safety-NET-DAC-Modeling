#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 15:39:49 2019

@author: jgf5fz
"""
#scratchpath = '/scratch/jgf5fz/DAC_modeling_paper_NCC_submission/hector_climate'
import initialize
exec(open('initialize.py').read())
fontsize=14
resolution = 1000
#scratchpath = '/scratch/jgf5fz/old_db/12-20'
scenario_dict_climate = {
       'land_prot_0p9_1p5_low_os_p2_co2_only_dac1_low_USA_only,d':'1.5$^o$C low overshoot',
       'land_prot_0p9_1p5_high_os_p4_co2_only_dac1_low_USA_only,d':'1.5$^o$C high overshoot',
        }


#maps label to color
color_dict={
        'No climate policy':'tomato',
        '1.5$^o$C low overshoot':'slateblue',
        '1.5$^o$C high overshoot':'cadetblue',

        }

style_dict = {
        '1.5$^o$C low overshoot':'-',
        '1.5$^o$C high overshoot':'-',
        'No climate policy':'--'}



def plot_all_climate_metrics(exe_ns,col,query,scenario_dict):
    resolution = 1000

    import matplotlib as mpl
    mpl.rcParams.update(mpl.rcParamsDefault)
    #plt.style.use('seaborn-white')
    #plt.style.use('seaborn-poster')
    
    
    
    str_cols = ['scenario',col,'Units']
    years = set_years(2000,2100)
    folder = [query]
    create_folders(folder,fig_dir)
    
    fig = plt.figure()
    fig, (ax2,ax1,ax0) = plt.subplots(nrows=3,ncols=1,sharex=True,figsize=(5.5,9))
    
    #Emissions
    col = 'sector'
    for n in exe_ns:
        fossil = pd.read_csv(scratchpath+'/exe_'+n+'/queryout_CO2_emissions_by_sector_no_bio_global.csv',skiprows=1)
        luc = pd.read_csv(scratchpath+'/exe_'+n+'/queryout_LUC_emissions_by_region_global.csv',skiprows=1)

        scenario_name = get_scenario_name(fossil)
        label_name = label_mapper(scenario_name,scenario_dict)
        
        fossil = df_plotting_prep(fossil,years,scenario_name,col,True)
        luc = df_plotting_prep(luc,years,scenario_name,'LandLeaf',True)

        df = pd.concat([fossil,luc],axis=1)
        df = df.sum(axis=1)
        
        
        df = df/1000*44/12
        df.to_csv('tot_emiss/luc_fossil_emiss'+label_name+'.csv')
        if scenario_name in scenario_dict:
            ax0.plot(df,label=label_name,color=color_dict[label_name],linestyle=style_dict[label_name])
        ax0.annotate('Net zero CO$_2$ \nEmissions',
                     xy=(1995,1.5),fontsize=fontsize)
        
        
        
        
        
    ax0.axhline(0,linestyle='-',color='k',linewidth=0.5)


    
    hist = pd.read_csv('../historical_climate_data/co2_annmean_gl.csv')
    for n in exe_ns:
        co2_concentrations = pd.read_csv(scratchpath+'/exe_'+n+'/queryout_co2_concentrations_global.csv',skiprows=1)
        df = co2_concentrations
        
        
        df[['scenario','region','CO2-concentration']] = df[['scenario','region','CO2-concentration']].astype(str)
        
        scenario_name = get_scenario_name(df)
        label_name = label_mapper(scenario_name,scenario_dict)
        #if 'BAU' in scenario_name:
        #    scenario_name = 'ref'
        
        drop_cols = ['scenario','region','CO2-concentration','Units','Unnamed: 29']
        col = df.index.values.astype(int)[0]
        df = df.drop(drop_cols,axis=1)
        
        df = df.T
        df = df.reset_index()
        df = df.rename(index=str, columns={"index":"year",col:scenario_name})
        df['year'] = df['year'].astype('float64')
        df = df.set_index('year')
        
        
        if scenario_name in scenario_dict:
            df = df.loc[df.index >= 2020.0]
            conc = df
            ax1.plot(df,color=color_dict[label_name],linestyle=style_dict[label_name])
            
    
    ax1.plot(hist['year'],hist['mean'],linestyle='-',color='grey',label='')    
    ax1.set_ylabel('ppm',fontsize=fontsize)
    ax1.set_title('b: CO$_2$ Concentration',loc='left',fontsize=fontsize)
    
    
    #temperature
    str_cols = ['scenario']
    for n in exe_ns:
        temps = pd.read_csv(scratchpath+'/exe_'+n+'/queryout_mean_temperature_global.csv',skiprows=1)
        df = temps
        df[str_cols] = df[str_cols].astype(str)
        
        
        
        
        scenario_name = get_scenario_name(df)
        label_name = label_mapper(scenario_name,scenario_dict)
        
        df = df_plotting_prep(df,years,scenario_name,'',False)
        if scenario_name in scenario_dict:
            ax2.plot(df,color=color_dict[label_name],linestyle=style_dict[label_name])
    ax2.set_ylabel('$\Delta$$^o$C',fontsize=fontsize)
    ax2.set_title('a: Global Average Temperature Anomaly',loc='left',fontsize=fontsize)
    
    ax2.axhline(1.5,linestyle='-',color='k',linewidth=0.5)
    ax2.axhline(2,linestyle='-',color='k',linewidth=0.5)
    
    
    
    ax2.annotate('Paris Target',xy=(2015,2.1),fontsize=fontsize)
    ax2.annotate('Well Below 2$^o$C',xy=(1991,1.65),fontsize=fontsize)
    
    ax2.set_xlim(1990,2100)
    ax2.set_ylim(0.5,3.5)
    

    for ax in [ax0,ax1,ax2]:
        ax.tick_params(axis='both',labelsize=fontsize,direction='out',which='both',length=6)
        #plot reference scenario
    reference_scenario = '../gcam_reference_scenario'
    
    ref_temps = pd.read_csv(reference_scenario+'/queryout_mean_temperature_global.csv',skiprows=1)
    ref_co2 = pd.read_csv(reference_scenario+'/queryout_co2_concentrations_global.csv',skiprows=1)
    #reference  temps
    df = ref_temps
    str_cols = ['scenario']
    df[str_cols] = df[str_cols].astype(str)
    scenario_name = get_scenario_name(df)
    df = df_plotting_prep(df,years,scenario_name,'',False)
    label_name='No climate policy'
    ax2.plot(df,color=color_dict[label_name],label=label_name)    
    #reference pCO2
    df = ref_co2
    str_cols = ['scenario']
    df[str_cols] = df[str_cols].astype(str)
    df = df_plotting_prep(df,years,scenario_name,'',False)
    ax1.plot(df,color=color_dict[label_name])
    #reference LUC+fossil co2 emission
    fossil = pd.read_csv(reference_scenario+'/queryout_CO2_emissions_by_sector_no_bio_global.csv',skiprows=1)
    luc = pd.read_csv(reference_scenario+'/queryout_LUC_emissions_by_region_global.csv',skiprows=1)
    scenario_name = get_scenario_name(fossil)
    fossil = df_plotting_prep(fossil,years,scenario_name,'sector',True)
    luc = df_plotting_prep(luc,years,scenario_name,'LandLeaf',True)
    df = pd.concat([fossil,luc],axis=1)
    df = df.sum(axis=1)
    df = df/1000*44/12
    ax0.plot(df,color=color_dict[label_name])    
    df.to_csv('totemiss'+scenario_name+'.csv')
    
    #historical
    hist = pd.read_csv('../historical_climate_data/global_carbon_budget.csv')
    hist['tot_anthropogenic'] = hist['fossil fuel and industry']+hist['land-use change emissions']
    ax0.plot(hist['Year'],hist['tot_anthropogenic']*44/12,label='Historical',linestyle='-',color='grey')
    h,l = ax0.get_legend_handles_labels()
    ax0.set_ylabel('GtCO$_2$ yr$^-1$',fontsize=fontsize)
    ax0.set_title('c: Fossil + LUC CO$_2$ Emissions',loc='left',fontsize=fontsize)

    str_cols = ['scenario']#here we define the columns we will need to read as strings rather than objects for dataframe slicing
    hist = pd.read_csv('../historical_climate_data/global-average-air-temperature-anomalies-5.csv')
    hist = hist.loc[hist['Type:text']=='Global annual']
    ax2.plot(hist['Year:year'],hist['NOAA Global Temp:number'],label='',linestyle='-',color='grey',alpha=.5)
    ax2.plot(hist['Year:year'],hist['HadCRUT4:number'],label='',linestyle='-',color='grey',alpha=.5)
    ax2.plot(hist['Year:year'],hist['ERA5:number'],label='',linestyle='-',color='grey',alpha=.5)
    ax2.plot(hist['Year:year'],hist['GISSTEMP:number'],label='',linestyle='-',color='grey',alpha=.5)

    #here we collect all the legend labels and handles we want an concatenate them together so the legend shows up how we want
    h0,l0 = ax0.get_legend_handles_labels()
    h2,l2 = ax2.get_legend_handles_labels()
    h = h0+h2 
    l = l0+l2
    plt.figlegend(h,l,bbox_to_anchor=(1,1.07),borderaxespad=0.01,ncol=2,fontsize=fontsize)
    
    
    fig.subplots_adjust(wspace=0.0001,hspace=0.0001)
    #path =  fig_dir+'/'+query+'/'+query+todays_date+'.png'
    fig.tight_layout()
    
    
    
    path = 'DAC_paper/final_figs/fig2.png'
    plt.savefig(path,bbox_inches='tight',dpi=resolution)
    plt.show()
    
    


df = plot_all_climate_metrics(exe_ns,'sector','fig2',scenario_dict_climate)



























