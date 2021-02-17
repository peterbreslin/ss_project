"""
Contact:
--------
pbreslin@tcd.ie

------------
Last Update:
------------
2020 November 16

Description:
------------
Code used to create plot of CME speed vs SMART total magnetic flux, with the flare GOES flux in the z-dimension

"""

# Packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

def main():
    """ Loads the custom solar stats catalogue,
        plots CME speed vs SMART total flux,
        add the flare GOES flux as a colour dimension """

    # =================================================================================================================

    # Defining the path for the dataframe
    dataframe = 'C:/Users/Peter/py_projects/solar_stats/custom_df.p'

    # Importing the dataframe
    df = pd.read_pickle(dataframe)

    # Making a new df for the columns I want
    dfs = df[['cme_speed', 'goes_flux', 'smart_total_flux']]

    # Removing the rows containing any NaN values
    dfs = dfs.dropna(how='any')

    #Reindexing
    dfs = dfs.reset_index(drop=True)

    # PROBLEM: smart_total_flux is not in a float format ---> must convert this
    dfs['smart_total_flux'] = dfs['smart_total_flux'].astype(float)

    # Creating a custom colormap
    cmap = mpl.colors.ListedColormap(['lightseagreen', 'darkmagenta', 'mediumblue', 'darkgreen', 'darkorange'])
    bounds = [-8, -7, -6, -5, -4, -3]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    # Plotting
    fig = plt.figure(figsize=[14, 10])
    s = plt.scatter(x=dfs['smart_total_flux'], y=dfs['cme_speed'], c=np.log10(dfs['goes_flux']),
                    alpha=0.5, cmap=cmap, norm=norm)
    plt.title('CME Speed vs SMART Total Magnetic Flux', fontsize=18)
    plt.xlabel("Total Flux [Mx]", fontsize=16)
    plt.ylabel("CME speed [kms$^{-1}$]", fontsize=16)
    plt.xscale("log")
    plt.yscale("log", base=np.e)

    # Colour bar
    cbar = fig.colorbar(s)
    cbar.set_label('log10 GOES Flux\n[Wm$^{-2}$]', fontsize=14, rotation=0, labelpad=50, y=0.55)
    plt.yticks(ticks=[100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 3000],
               labels=[r'100', r'2', r'3', r'4', r'5', r'6', r'7', r'8', r'9', r'1000', r'3000'],
               fontsize=14)
    plt.xticks(ticks=[1e21, 1e22, 1e23],
               labels=[r'10$^{21}$', r'10$^{22}$', r'10$^{23}$'],
               fontsize=14)

    #plt.savefig('smart_tot_flux.png', dpi=300, bbox_inches="tight", pad_inches=1)
    fig.show()

    # =================================================================================================================


if __name__ == '__main__':
        main()