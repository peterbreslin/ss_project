"""
Contact:
--------
pbreslin@tcd.ie

------------
Last Update:
------------
2020 November 14

Description:
------------
Code to make plot of the GOES flux vs SRS sunspot group area 
(SAMMIS paper figure / Fig. 6 from HELCATS paper) 

"""

# Packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

def main():
    """ Loads the custom solar stats catalogue,
        reorganises the dataframe,
        then creates GOES flux vs SRS sunspot group area plot
        (SAMMIS paper figure / Fig. 6 from HELCATS paper) """

    # Defining the path for the dataframe
    custom_df = 'C:/Users/Peter/py_projects/solar_stats/custom_df.p'

    # Importing the dataframe
    df = pd.read_pickle(custom_df)

    # Looking at some flare props, particularly the outlier
    dfs = df[['srs_hale', 'srs_area', 'goes_flux']]

    # Removing the rows containing any NaN values
    dfs = dfs.dropna(how='any')

    # Reo-rganising the indicies
    dfs = dfs.reset_index()

    # Converting string Hale values to a float
    dfs["srs_hale"] = dfs["srs_hale"].astype(float)

    # srs_area column is a string --> convert to a float!
    dfs["srs_area"] = dfs["srs_area"].astype(float)

    # Removing the rows that contain zeros
    dfs_nz = dfs[(dfs[['srs_area']] != 0).all(axis=1)]

    # Re-indexing once again
    dfs_nz = dfs_nz.reset_index()

    # Logging the goes_flux and srs area for plotting
    dfs_nz['goes_flux'] = np.log10(dfs_nz['goes_flux'])
    dfs_nz['srs_area'] = np.log10(dfs_nz['srs_area'])

    # Setting Hale Class colours
    cmap = mpl.colors.ListedColormap(['gold', 'crimson', 'black', 'royalblue', 'mediumseagreen', 'aqua'])
    bounds = [1, 2, 3, 4, 5, 6, 7]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    # Plotting
    a = plt.figure(figsize=[16, 12], facecolor='white')
    sct1 = plt.scatter(x=dfs_nz['srs_area'], y=dfs_nz['goes_flux'], c=dfs_nz['srs_hale'], alpha=0.8, cmap=cmap,
                       norm=norm)
    plt.title('Flare GOES flux vs. SRS Sunspot Group Area', fontsize=18)
    plt.xlabel("log10 SRS Area [m.s.h]", fontsize=14)
    plt.ylabel("log10 GOES Flux [Wm$^{-2}$]", fontsize=14)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    # Legend
    handles, labels = sct1.legend_elements()
    labels = [r'$\alpha$', r'$\beta$',
              r'$\beta - \gamma$',
              r'$\beta - \delta$',
              r'$\beta - \gamma - \delta$',
              r'$\gamma - \delta$']
    leg = plt.legend(handles, labels, loc="best", title="Hale Class", fontsize=14)
    plt.setp(leg.get_title(), fontsize=14)

    # plt.savefig('flux_srs_area.png', dpi=300, bbox_inches="tight", pad_inches=1)

    a.show()



if __name__ == '__main__':
    main()

