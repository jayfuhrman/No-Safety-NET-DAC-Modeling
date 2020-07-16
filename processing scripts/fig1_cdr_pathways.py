# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 11:02:46 2019

@author: VEST
"""


def plot_fig1(x,y,fontsize,CI):
    import matplotlib.pyplot as plt
    import seaborn as sns; sns.set()
    import pandas as pd
    

    alpha=(1-CI)/2
   
    
    plt.style.use('seaborn-white')
    plt.style.use('seaborn-paper')
    

    fig, ax = plt.subplots(figsize=(x,y))
    
    all_nets = pd.read_csv('all_nets.csv')
    print(len(all_nets.T))
    n_allnets = len(all_nets.T)
    for column in all_nets.drop('year',axis=1):
        plt.plot(all_nets['year'],all_nets[column],color='grey',label='',alpha=0.25,linewidth=1)
    
    
    
    #plt.annotate('Total CDR', xy=(2050,2),  xycoords='data',
    #            xytext=(2064,21), textcoords='data',fontsize=fontsize,
    #            )
    plt.arrow(2003.8,-49,8,0,linewidth=1,color='grey',alpha=1,length_includes_head=True)
    
    df = pd.read_csv('AF.csv')
    df = df.astype('float64') 
    n_af = len(df.T)-1
    print(len(df.T))
    df = df.interpolate()
    #for column in df.drop('year', axis=1):
    #    line3 = plt.plot(df['year'], df[column]/1000,'-', color='forestgreen', alpha=0.5)
    df = df.set_index('year')
    central = -df.median(axis=1)/1000
    central = central.rolling(10).mean()
    line3 = central.plot(color = 'darkolivegreen',alpha=1,label='Afforestation (n='+str(n_af)+')',linewidth=3)
    ub = df.quantile(1-alpha,axis=1)/1000 #upper bound
    lb = df.quantile(alpha,axis=1)/1000 #lower bound
    ub = ub.rolling(5).mean()
    lb = lb.rolling(5).mean()
    #plt.fill_between(lb.index,-lb,-ub,color='darkolivegreen',alpha = 0.65)
    
    df = pd.read_csv('BECCS.csv')
    df = df.astype('float64') 
    df = df.interpolate()
    
    print(len(df.T))
    n_beccs = len(df.T)-1
    #for column in df.drop('year', axis=1):
    #    line2 = plt.plot(df['year'], df[column]/1000,'-', color='chartreuse', alpha=0.25)
    df = df.set_index('year')
    central = -df.median(axis=1)/1000
    central = central.rolling(5).mean()
    line2 = central.plot(color = 'chartreuse',alpha=1,label='BECCS (n='+str(n_beccs)+')',linewidth=3)
    ub = df.quantile(1-alpha,axis=1)/1000 #upper bound
    lb = df.quantile(alpha,axis=1)/1000 #lower bound
    ub = ub.rolling(5).mean()
    lb = lb.rolling(5).mean()
    #plt.fill_between(lb.index,-lb,-ub,color='chartreuse',alpha = 0.65)
    
    df = pd.read_csv('DAC.csv')
    df = df.astype('float64') 
    df = df.interpolate()
    
    
    #for column in df.drop('year', axis=1):
    #    line1 = plt.plot(df['year'], df[column]/1000,'-', color='mediumslateblue', alpha=1)
    df = df.set_index('year')
    print(len(df.T))
    n_dac = len(df.T)-1
    df=df.fillna(0)
    df = df.loc[:, (df != 0).any(axis=0)] #because there are so few scenarios reporting DAC, we drop the relatively large proportion for which it is never deployed because it is assumed unavailable.
    central = -df.median(axis=1)/1000
    line1 = central.plot(color = 'slateblue',alpha=1,label='Direct Air Capture (n='+str(n_dac)+')',linewidth=3)    
    ub = df.quantile(1-alpha,axis=1)/1000 #upper bound
    lb = df.quantile(alpha,axis=1)/1000 #lower bound
    ub = ub.rolling(5).mean()
    lb = lb.rolling(5).mean()
    #plt.fill_between(lb.index,-lb,-ub,color='slateblue',alpha = 0.5)
    
    
    

    df = all_nets
    df = df.interpolate()
    df = df.set_index('year')
    central = df.median(axis=1)
    central = -df.median(axis=1)/1000
    central = central.rolling(5).mean()
    line3 = central.plot(color = 'grey',alpha=1,label='',linewidth=3)
    ub = df.quantile(1-alpha,axis=1) #upper bound
    lb = df.quantile(alpha,axis=1) #lower bound
    ub = ub.rolling(5).mean()
    lb = lb.rolling(5).mean()
    plt.fill_between(lb.index,lb,ub,color='grey',alpha = 0.5,label='Total Negative Emissions (n='+str(n_allnets)+')')
    
    
    
    
    
        
    plt.ylabel('GtCO$_2$ yr$^{- 1}$',fontsize=fontsize)
    positive_emissions_technology = pd.read_csv('Global_Carbon_Budget_2018.csv')
    positive_emissions_technology = positive_emissions_technology.set_index('Year')
    
    positive_emissions_technology = positive_emissions_technology*44/12
    
    positive_emissions_technology['land-use change emissions'].plot(ax=ax,color = 'red',alpha=0.75,linestyle='dashed',label='')
    positive_emissions_technology = positive_emissions_technology.sum(axis=1)
    positive_emissions_technology.plot(ax=ax,color = 'red',alpha=0.75,label='')
    
    plt.arrow(2018,5,0,36,head_length=1,head_width=1,linewidth=2,color='grey',length_includes_head=True)
    plt.arrow(2018,41,0,-36,head_length=1,head_width=1,linewidth=2,color='grey',length_includes_head=True)
    
    plt.arrow(2018,0,0,4.75,head_length=1,head_width=1,linewidth=2,color='grey',length_includes_head=True)
    plt.arrow(2018,4.75,0,-4.75,head_length=1,head_width=1,linewidth=2,color='grey',length_includes_head=True)
    
    
    plt.annotate('Fossil Fuel + Industry', xy=(2019,20),  xycoords='data',fontsize=fontsize
                #xytext=(2047,20), textcoords='data',fontsize='xx-large',
                #arrowprops=dict(facecolor='grey', shrink=0.05),
                #horizontalalignment='right', verticalalignment='top',
                )
    
    plt.annotate('Land Use Change', xy=(2018.5,2),  xycoords='data',
                xytext=(2019,2), textcoords='data',fontsize=fontsize,
                #arrowprops=dict(facecolor='grey', shrink=0.05),
                #horizontalalignment='right', verticalalignment='top',
                )
    
    #plt.annotate('Increased negative emissions \ncapacity enabled by DAC', xy=(2087,-35),  xycoords='data',
    #            xytext=(2070,-30), textcoords='data',fontsize=fontsize,
    #            arrowprops=dict(facecolor='grey', shrink=0.05),
    #            horizontalalignment='right', verticalalignment='top',
    #            )
    
    
    plt.axhline(color='k')
    
    plt.xlabel('')
    #plt.legend([line1[0],line2[0],line3[0]], ('Direct Air Capture','BECCS','Afforestation'),loc='upper right')
    plt.xlim(2000,2100)
    plt.ylim(-55,43)
    plt.tick_params(axis='both',labelsize=fontsize)
    
    plt.legend(fontsize=fontsize,loc=3)
    plt.savefig('Figures/cdr_pathways_fig1_REVISED.png',dpi = 1000)
    plt.show()


dac = plot_fig1(8,8,18,0.68)

#af = af.rolling(10).mean()
#plt.plot(af)

#%%
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import pandas as pd


x=3
y=8

plt.style.use('seaborn-white')
plt.style.use('seaborn-paper')

AF = pd.read_csv('AF.csv')
BECCS = pd.read_csv('BECCS.csv')
DAC = pd.read_csv('DAC.csv')
all_nets = pd.read_csv('all_nets.csv')

df1=AF
df2=BECCS
df3=DAC
df4=all_nets

df1 = df1.drop('Unnamed: 0',axis=1)
df2 = df2.drop('Unnamed: 0',axis=1)
df3 = df3.drop('Unnamed: 0',axis=1)


