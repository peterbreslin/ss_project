"""
Contact:
--------
pbreslin@tcd.ie

------------
Last Update:
------------
2020 November 15

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

    # Reindexing
    dfs = dfs.reset_index(drop=True)

    # Converting string Hale values to a float
    dfs["srs_hale"] = dfs["srs_hale"].astype(float)

    # srs_area column is a string --> convert to a float!
    dfs["srs_area"] = dfs["srs_area"].astype(float)

    # Removing the rows that contain zeros
    dfs = dfs[(dfs[['srs_area']] != 0).all(axis=1)]

    # Re-indexing once again
    dfs = dfs.reset_index(drop=True)

    # Logging the goes_flux and srs area for plotting
    dfs['goes_flux'] = np.log10(dfs['goes_flux'])
    dfs['srs_area'] = np.log10(dfs['srs_area'])

    # Want to separate each class so that we can make each one a specific symbol
    a = dfs.loc[dfs['srs_hale'] == 1.0]     # alpha
    b = dfs.loc[dfs['srs_hale'] == 2.0]     # beta
    bg = dfs.loc[dfs['srs_hale'] == 3.0]    # beta-gamma
    bd = dfs.loc[dfs['srs_hale'] == 4.0]    # beta-delta
    bgd = dfs.loc[dfs['srs_hale'] == 5.0]   # beta-gamma-delta
    gd = dfs.loc[dfs['srs_hale'] == 6.0]    # gamma-delta

    # Setting Hale Class colours
    cmap = mpl.colors.ListedColormap(['crimson', 'darkblue', 'darkcyan', 'magenta', 'darkorange', 'black'])
    bounds = [1, 2, 3, 4, 5, 6, 7]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    # Plotting
    p1 = plt.figure(figsize=[16, 12], facecolor='white')

    s1 = plt.scatter(x=a['srs_area'], y=a['goes_flux'], c=a['srs_hale'],
                     alpha=0.8, marker='o', cmap=cmap, norm=norm, label=r'$\alpha$', s=70)
    s2 = plt.scatter(x=b['srs_area'], y=b['goes_flux'], c=b['srs_hale'],
                     alpha=0.8, marker='+', cmap=cmap, norm=norm, label=r'$\beta$', s=70)
    s3 = plt.scatter(x=bg['srs_area'], y=bg['goes_flux'], c=bg['srs_hale'],
                     alpha=0.8, marker='v', cmap=cmap, norm=norm, label=r'$\beta \gamma$', s=70)
    s4 = plt.scatter(x=bd['srs_area'], y=bd['goes_flux'], c=bd['srs_hale'],
                     alpha=0.8, marker='x', cmap=cmap, norm=norm, label=r'$\beta \delta$', s=70)
    s5 = plt.scatter(x=bgd['srs_area'], y=bgd['goes_flux'], c=bgd['srs_hale'],
                     alpha=0.8, marker='*', cmap=cmap, norm=norm, label=r'$\beta \gamma \delta$', s=70)
    s6 = plt.scatter(x=gd['srs_area'], y=gd['goes_flux'], c=gd['srs_hale'],
                     alpha=0.8, marker='s', cmap=cmap, norm=norm, label=r'$\gamma \delta$', s=70)

    plt.title('Flare GOES flux vs. SRS Sunspot Group Area', fontsize=18)
    plt.xlabel("log10 SRS Area [m.s.h]", fontsize=16)
    plt.ylabel("log10 GOES Flux [Wm$^{-2}$]", fontsize=16)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)

    # Legend
    leg = plt.legend(loc="best", title="Hale Class", fontsize=18)
    plt.setp(leg.get_title(), fontsize=18)
    leg.legendHandles[0].set_color('crimson')
    leg.legendHandles[1].set_color('darkblue')
    leg.legendHandles[2].set_color('darkcyan')
    leg.legendHandles[3].set_color('magenta')
    leg.legendHandles[4].set_color('darkorange')
    leg.legendHandles[5].set_color('black')

    #plt.savefig('flux_area_rev.png', dpi=300, bbox_inches="tight", pad_inches=1)

    p1.show()



if __name__ == '__main__':
    main()

