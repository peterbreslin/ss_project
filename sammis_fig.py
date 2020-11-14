"""
Contact:
--------
pbreslin@tcd.ie

------------
Last Update:
------------
2020 November 10

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
    """ Loads the solar stats catalogue,
        reorganises the dataframe and fixes some entries,
        then creates GOES flux vs SRS sunspot group area plot
        (SAMMIS paper figure / Fig. 6 from HELCATS paper) """

    # Defining the path for the dataframe
    dataframe = 'C:/Users/Peter/py_projects/solar_stats/cdaw_cme_flare_ar_smart_database.p'

    # Importing the dataframe
    df = pd.read_pickle(dataframe)

    # Looking at some flare props, particularly the outlier
    dfs = df[['srs_hale', 'srs_area', 'flare_goes_class']]

    # Removing the rows containing any NaN values
    dfs = dfs.dropna(how='any')

    # Reo-rganising the indicies
    dfs = dfs.reset_index()

    # Splitting goes_class column into 2 so as to separate the class from the flux value
    goes_split = dfs.flare_goes_class.str.extract('([a-zA-Z]+)([^a-zA-Z]+)', expand=True)
    goes_split.columns = ["goes_class", "goes_flux"]

    # Adding these new columns into dfs
    dfs['goes_class'] = goes_split['goes_class']
    dfs['goes_flux'] = goes_split['goes_flux']

    # Going to replace each incorrect value of 7,4 with 7.4
    dfs['goes_flux'] = dfs['goes_flux'].replace(['7,4'], '7.4')

    # Converting string flux values to a float
    dfs['goes_flux'] = dfs['goes_flux'].astype(float)

    # Now multiplying the flux values by the relevant power for its GOES class
    dfs.loc[dfs.goes_class == 'A', 'goes_flux'] *= 1e-8
    dfs.loc[dfs.goes_class == 'B', 'goes_flux'] *= 1e-7
    dfs.loc[dfs.goes_class == 'C', 'goes_flux'] *= 1e-6
    dfs.loc[dfs.goes_class == 'M', 'goes_flux'] *= 1e-5
    dfs.loc[dfs.goes_class == 'X', 'goes_flux'] *= 1e-4

    # Need to group Beta and BETA together, etc.
    dfs["srs_hale"].replace({"ALPHA": "1", "Alpha": "1",
                             "BETA": "2", "Beta": "2",
                             "BETA-GAMMA": "3", "Beta-Gamma": "3",
                             "BETA-DELTA": "4", "Beta-Delta": "4",
                             "BETA-GAMMA-DELTA": "5", "Beta-Gamma-Delta": "5",
                             "GAMMA-DELTA": "6", "Gamma-Delta": "6", }, inplace=True)

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

