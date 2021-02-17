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
Code used to create plot of CME speed vs flare GOES flux, with the CME width in the z-dimension

"""

# Packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

def main():
    """ Loads the custom solar stats catalogue,
        plots CME speed vs flare GOES flux,
        add the CME width as a colour dimension """

    # =================================================================================================================

    # Defining the path for the dataframe
    dataframe = 'C:/Users/Peter/py_projects/solar_stats/custom_df.p'

    # Importing the dataframe
    df = pd.read_pickle(dataframe)

    # Making a new df for the columns I want
    dfs = df[['cme_speed', 'goes_flux', 'cme_width']]

    # Removing the rows containing any NaN values
    dfs = dfs.dropna(how='any')

    #Reindexing
    dfs = dfs.reset_index(drop=True)

    # Creating a custom colormap
    cmap = mpl.colors.ListedColormap(['lightseagreen', 'darkmagenta', 'mediumblue', 'darkorange'])
    bounds = [0, 90, 180, 270, 360]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    # GOES Flux
    fig = plt.figure(figsize=[14, 10], facecolor='white')
    s = plt.scatter(x=np.log10(dfs['goes_flux']), y=dfs['cme_speed'], c=dfs['cme_width'],
                    alpha=0.5, cmap=cmap, norm=norm)
    plt.title('CME Speed vs GOES Flux', fontsize=18)
    plt.xlabel("log10 GOES Flux [Wm$^{-2}$]", fontsize=16)
    plt.ylabel("log10 CME speed [kms$^{-1}$]", fontsize=16)
    plt.xlim(-8.5, -1.5)
    plt.yscale("log", base=10)

    cbar = fig.colorbar(s)
    cbar.set_label(r'$\theta$[$^{\circ}$]', fontsize=16, rotation=0, labelpad=30, y=0.55)

    plt.yticks(ticks=[100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 3000],
               labels=[r'100', r'2', r'3', r'4', r'5', r'6', r'7', r'8', r'9', r'1000', r'3000'], fontsize=14)

    #plt.savefig('speed_gflux_width.png', dpi=300, bbox_inches="tight", pad_inches=1)

    fig.show()

    # =================================================================================================================


if __name__ == '__main__':
        main()