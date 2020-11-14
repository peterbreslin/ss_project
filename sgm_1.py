"""
Contact:
--------
pbreslin@tcd.ie

------------
Last Update:
------------
2020 October 30

Description:
------------
Code used to create plots of some simple statistics during the first 2 weeks of the project. Some of these plots were
included in the SGM 22/10

"""

# Packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import matplotlib as mpl

def main():
    """ Loads the solar stats catalogue,
        reorganises the dataframe and fixes some entries,
        then starts creating some plots """
    #==================================================================================================================

    # Defining the path for the dataframe
    dataframe = 'C:/Users/Peter/py_projects/solar_stats/cdaw_cme_flare_ar_smart_database.p'

    # Importing the dataframe
    df = pd.read_pickle(dataframe)

    # CME Halo Flag - reindexing to get the desired order (increasing in halo flag)
    halo_counts = df['cme_halo'].value_counts()
    halo_counts = halo_counts.reindex(index = ['I','II','III','IV'])

    # Some Pie Chart properties
    my_colours = ['cornflowerblue','lightcoral','palegreen','sandybrown']
    my_explode = (0, 0, 0, 0)
    
    # Plotting
    a = plt.figure(1)
    plt.plot(figsize=(8,8), facecolor='white', aspect='equal')
    pie = halo_counts.plot.pie(autopct='%1.1f%%', fontsize=16, label="", table=True, colors=my_colours,
                               explode=my_explode, shadow=False, wedgeprops={'linewidth':2, 'edgecolor':"white"})
    pie.set_title('CME Halo Classification', fontsize=16)
    
    # Making the table
    tab = pie.tables[0]
    tab.set_fontsize(12)
    tab.scale(1.3, 1.3)
    
    #plt.savefig('cme_halo.png', dpi=300, bbox_inches="tight", pad_inches=1)
    a.show()

    #==================================================================================================================

    """ Creating a new df to manipulate specific columns/rows """

    # Need to remove NaNs ---> only interested in the 3 columns so making a new dataframe for these
    df2 = df[["cme_speed", "smart_r_value", "smart_wlsg", 'flare_goes_class', 'smart_total_flux']]

    # Removing the rows containing any NaN values
    df2 = df2.dropna(how='any')


    """ SMART R-value """
    
    # Plotting with x-axis on a log10 scale, y-axis on a log scale
    b = plt.figure(2)
    ax2 = df2.plot.scatter(x='smart_r_value', y='cme_speed', alpha=0.5, figsize=(10,10), fontsize=12)
    ax2.set_title('CME Speed vs SMART R values', fontsize=16)
    ax2.set_xlabel("R value [Mx]", fontsize=14)
    ax2.set_ylabel("CME speed [kms$^{-1}$]", fontsize=14)
    ax2.set_xscale("log", base=10)
    ax2.set_yscale("log", base=np.e)
    
    # Scaling the log x-axis accordingly
    ax2.yaxis.set_major_formatter(ScalarFormatter())
    
    #plt.savefig('r_values.png', dpi=300, bbox_inches="tight", pad_inches=1)
    b.show()

    #==================================================================================================================

    """ SMART WLSG:
    There are a lot of zero's in the WLSG column ---> let's remove these by dropping those rows.
    Creating a boolean DataFrame by comparing all filtered column values by a scalar for NOT equality and then checking
    all the boolean Trues per row by all """

    # Removing zeros
    df3 = df2[(df2[['smart_wlsg']] != 0).all(axis=1)]
    
    # Plotting with x-axis on a log10 scale, y-axis on a log scale
    c = plt.figure(3)
    ax3 = df3.plot.scatter(x='smart_wlsg', y='cme_speed', alpha=0.5, figsize=(10,10), fontsize=12, color='indianred')
    ax3.set_title('CME Speed vs SMART WL$_{SG}$', fontsize=16)
    ax3.set_xlabel("WL$_{SG}$ [G]", fontsize=14)
    ax3.set_ylabel("CME speed [kms$^{-1}$]", fontsize=14)
    ax3.set_xscale("log", base=10)
    ax3.set_yscale("log", base=np.e)
    
    # Scaling the log x-axis accordingly
    ax3.yaxis.set_major_formatter(ScalarFormatter())
    
    #plt.savefig('wlsg.png', dpi=300, bbox_inches="tight", pad_inches=1)
    c.show()

    #==================================================================================================================

    """ GOES Flare Class:
    Need to split df2['flare_goes_class'] into two in order to separate the class form the flux value
    The pattern ([a-zA-Z]+)([^a-zA-Z]+) means match a group of letters: ([a-zA-Z]+) followed by a group 
    of non letters: ([^a-zA-Z]+) """

    # Splitting GOES class column
    goes_split = df2.flare_goes_class.str.extract('([a-zA-Z]+)([^a-zA-Z]+)', expand=True)
    goes_split.columns = ["goes_class", "goes_flux"]

    # Putting the two 'new' columns into the dataframe under new column headings
    df2['goes_class'] = goes_split['goes_class']
    df2['goes_flux'] = goes_split['goes_flux']   
    
    """ The flux is a string ---> must convert to a float BUT there are some incorrect values that we must change:
    
        df2['goes_flux'] = df2['goes_flux'].astype(float)   
    
    Running above line gives an error --> Looks like there is some data inputted incorrectly eg. 7,4 (shoud be 7.4) """
    
    # Going to replace each value of 7,4 with 7.4
    df2['goes_flux'] = df2['goes_flux'].replace(['7,4'],'7.4')
    
    # Converting string flux values to a float
    df2['goes_flux'] = df2['goes_flux'].astype(float)
    
    # Now multiplying the flux values by the relevant power for its GOES class
    df2.loc[df2.goes_class == 'A', 'goes_flux'] *= 1e-8
    df2.loc[df2.goes_class == 'B', 'goes_flux'] *= 1e-7
    df2.loc[df2.goes_class == 'C', 'goes_flux'] *= 1e-6
    df2.loc[df2.goes_class == 'M', 'goes_flux'] *= 1e-5
    df2.loc[df2.goes_class == 'X', 'goes_flux'] *= 1e-4
    
    # Logging the goes_flux column
    df2['goes_flux'] = np.log10(df2['goes_flux'])
    
    # Plotting speed vs GOES flux
    d = plt.figure(4)
    ax4 = df2.plot.scatter(x='goes_flux', y='cme_speed', alpha=0.5, figsize=(10,10), fontsize=12, color='mediumpurple')
    ax4.set_title('CME Speed vs GOES Flux', fontsize=16)
    ax4.set_xlabel("log10 GOES flux [Wm$^{-2}$]", fontsize=16)
    ax4.set_ylabel("CME speed [kms$^{-1}$]", fontsize=16)
    #ax4.set_xscale("log", base=10)
    ax4.set_yscale("log", base=np.e)
    
    ax4.set_yticks([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 3000])
    ax4.set_yticklabels([r'100', r'2', r'3', r'4', r'5', r'6', r'7', r'8', r'9', r'1000', r'3000'], fontsize=14)
    
    #plt.savefig('flux_w_outlier.png', dpi=300, bbox_inches="tight", pad_inches=1)
    d.show()

    #==================================================================================================================

    """ print(max(df2['goes_flux'])) ---> There is an outlier, let's remove this """

    # Creating a copy of the dataframe for ease
    df2_copy = df2.copy()

    # Finding it's index
    max_index = df2_copy['goes_flux'].idxmax()

    # Need to reindex the dataframe so that it's numbered correctly
    df2_copy = df2_copy.reset_index()

    # Getting the new (and correct) index
    max_index2 = df2_copy['goes_flux'].idxmax()

    # Now to remove this row
    df2_copy = df2_copy.drop(df2_copy.index[2738])

    #==================================================================================================================

    """ GOES flux Plot w/o outlier """

    # Re-plotting
    e = plt.figure(5)
    ax5 = df2_copy.plot.scatter(x='goes_flux', y='cme_speed',
                                alpha=0.5, figsize=(10,10), fontsize=12, color='mediumpurple')
    ax5.set_title('CME Speed vs GOES Flux', fontsize=16)
    ax5.set_xlabel("GOES flux [Wm$^{-2}$]", fontsize=16)
    ax5.set_ylabel("CME speed [kms$^{-1}$]", fontsize=16)
    #ax5.set_xscale("log", base=10)
    ax5.set_yscale("log", base=np.e)
    ax5.set_yticks([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 3000])
    ax5.set_yticklabels([r'100', r'2', r'3', r'4', r'5', r'6', r'7', r'8', r'9', r'1000', r'3000'],
                        fontsize=14)
    
    #plt.savefig('goes_flux.png', dpi=300, bbox_inches="tight", pad_inches=1)
    e.show()

    #==================================================================================================================

    """ SMART Total Magnetic Flux """

    # PROBLEM: smart_total_flux is not in a float format ---> must convert this
    df2_copy['smart_total_flux'] = df2_copy['smart_total_flux'].astype(float)

    # Creating a custom colormap
    cmap = mpl.colors.ListedColormap(['lightseagreen', 'darkmagenta', 'mediumblue', 'darkgreen', 'darkorange'])
    bounds = [-8, -7, -6, -5, -4, -3]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    # Plotting
    f = plt.figure(6)
    fig2 = plt.figure(figsize=[14, 10])
    sct = plt.scatter(x=df2_copy['smart_total_flux'], y=df2_copy['cme_speed'], c=df2_copy['goes_flux'],
                      alpha=0.5, cmap=cmap, norm=norm)
    plt.title('CME Speed vs SMART Total Magnetic Flux', fontsize=16)
    plt.xlabel("Total Flux [Mx]", fontsize=14)
    plt.ylabel("CME speed [kms$^{-1}$]", fontsize=14)
    # plt.ylim([20,3000])
    plt.xscale("log")
    plt.yscale("log", base=np.e)

    # Colourbar
    cbar = fig2.colorbar(sct)
    cbar.set_label('log10 GOES Flux\n[Wm$^{-2}$]', fontsize=14, rotation=0, labelpad=50, y=0.55)
    plt.yticks(ticks=[100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 3000],
               labels=[r'100', r'2', r'3', r'4', r'5', r'6', r'7', r'8', r'9', r'1000', r'3000'],
               fontsize=14)
    plt.xticks(ticks=[1e21, 1e22, 1e23],
               labels=[r'10$^{21}$', r'10$^{22}$', r'10$^{23}$'],
               fontsize=14)

    # plt.savefig('smart_total_flux.png', dpi=300, bbox_inches="tight", pad_inches=1)
    f.show()

    #==================================================================================================================

    """ GOES flare classes - Pie chart """

    # Counting how many classes and how many of each class there are
    class_counts = df2_copy['goes_class'].value_counts()
    class_counts = class_counts.reindex(index=['A', 'B', 'C', 'M', 'X'])

    # Pie chart & Table properties
    class_col = ['lightskyblue', 'darkorchid', 'royalblue', 'mediumseagreen', 'darkorange']
    my_explode = (0.7, 0.05, 0.1, 0.05, 0.6)
    # my_explode = (0,0,0,0,0)

    # Pie chart plotting
    g = plt.figure(7)
    plt.figure(figsize=(8, 8), facecolor='white')
    ax7 = plt.plot(aspect='equal')
    pie2 = class_counts.plot.pie(autopct='%1.1f%%', textprops={'color': "black"}, fontsize=16,
                                 label="", table=True, colors=class_col, explode=my_explode, shadow=False)
    pie2.set_title('GOES Flare Classes', fontsize=16)

    # Table
    tab2 = pie2.tables[0]
    tab2.set_fontsize(12)
    tab2.scale(1.3, 1.3)

    # plt.savefig('flare_classes.png', dpi=300, bbox_inches="tight", pad_inches=1)
    g.show()

    #==================================================================================================================

    """ Looking at some stats """

    # How many flares
    df_new = df.copy()
    type_ct = df_new['flare_type'].count()
    type_nan = df_new['flare_type'].isnull().sum()
    print('Flare Type: ' + str(type_ct) + ' with ' + str(type_nan) + ' NaNs')

    # How many CMEs
    cme_ct = df_new['cme_time'].count()
    cme_nan = df_new['cme_time'].isnull().sum()
    print('CME count: ' + str(cme_ct) + ' with ' + str(cme_nan) + ' NaNs')

    # SRS - hale class
    srs_hale_ct = df_new['srs_hale'].count()
    srs_hale_nan = df_new['srs_hale'].isnull().sum()
    print('SRS Hale Class: ' + str(srs_hale_ct) + ' with ' + str(srs_hale_nan) + ' NaNs')

    # SRS - observation time (total number of SRS events)
    srs_time_ct = df_new['srs_observation_time'].count()
    srs_time_nan = df_new['srs_observation_time'].isnull().sum()
    print('SRS Records: ' + str(srs_time_ct) + ' with ' + str(srs_time_nan) + ' NaNs')

    # SMART Regions
    smart_time_ct = df_new['smart_observation_time'].count()
    smart_time_nan = df_new['smart_observation_time'].isnull().sum()
    print('SMART Regions: ' + str(smart_time_ct) + ' with ' + str(smart_time_nan) + ' NaNs')

    #==================================================================================================================

    """ Looking at which database is missing flare records """

    # Making a separate dataframe for ease
    df_flares = df_new[['flare_type']]

    # Removing the rows containing any NaN values
    df_flares = df_flares.dropna(how='any')

    # Counting different types
    flare_type = df_flares.value_counts().to_dict()
    print(flare_type)

    # Checking how many flares are missing and from which database
    missing_flares = df_new[['flare_type', 'flare_goes_class']]
    missing_flares = missing_flares.dropna(how='any')
    print(missing_flares['flare_type'].value_counts().to_dict())

    #==================================================================================================================

    """ CME width and speed """

    df_speed_width = df_new[['cme_speed', 'cme_width', 'cme_halo']]
    df_speed_width = df_speed_width.dropna(how='any')

    # Replacing the non-numeric hale classes with numeric values
    df_speed_width["cme_halo"].replace({"I": "1", "II": "2", "III": "3", "IV": "4"}, inplace=True)
    df_speed_width["cme_halo"] = df_speed_width["cme_halo"].astype(float)

    # New colour scheme for the CME hale flag which will be shown as a z-dimension
    cmap2 = mpl.colors.ListedColormap(['cornflowerblue', 'lightcoral', 'palegreen', 'sandybrown'])
    bounds2 = [1, 2, 3, 4, 5]
    norm2 = mpl.colors.BoundaryNorm(bounds2, cmap2.N)

    # Plotting
    h = plt.figure(8)
    plt.figure(figsize=[16, 12])
    sct2 = plt.scatter(x=df_speed_width['cme_width'], y=df_speed_width['cme_speed'], c=df_speed_width['cme_halo'],
                       alpha=0.5,
                       cmap=cmap2, norm=norm2)
    plt.title('CME Speed vs Width', fontsize=16)
    plt.xlabel("Width [Degrees]", fontsize=14)
    plt.ylabel("CME speed [kms$^{-1}$]", fontsize=14)
    # plt.xscale("log")
    plt.yscale("log", base=np.e)
    plt.xticks(fontsize=14)
    plt.yticks(ticks=[100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 3000],
               labels=[r'100', r'2', r'3', r'4', r'5', r'6', r'7', r'8', r'9', r'1000', r'3000'],
               fontsize=14)

    # Legend
    legend1 = plt.legend(*sct2.legend_elements(), loc="lower right", title="CME Halo Flag", fontsize=14)

    # plt.savefig('cme_speed_width.png', dpi=300, bbox_inches="tight", pad_inches=1)
    h.show()

    #==================================================================================================================

    plt.show()


if __name__ == '__main__':
    main()