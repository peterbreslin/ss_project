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
Code to make validation histogram plots of various properties

"""

# Packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def main():
    """ Loads the custom solar stats catalogue,
        reorganises the dataframe,
        and plots various validation histogram plots (from HELCATS paper) """

    # Defining the path for the dataframe
    custom_df = 'C:/Users/Peter/py_projects/solar_stats/custom_df.p'

    # Importing the dataframe
    df = pd.read_pickle(custom_df)

    # CME data
    dfc = df[['cme_width', 'cme_angle', 'cme_speed']]

    # Putting the kinetic energy and mass in a separate df because they contain significantly less entries
    mke = df[['cme_mass', 'cme_kinetic_energy']]

    # Removing the rows containing any NaN values
    dfc = dfc.dropna(how='any')
    mke = mke.dropna(how='any')

    # Re-organising the indicies
    dfc = dfc.reset_index(drop=True)
    mke = mke.reset_index(drop=True)

    # Mass values are not floats
    mke['cme_mass'] = mke['cme_mass'].astype(float)

    #==================================================================================================================

    # SRS data
    dfs = df[['srs_no_spots', 'srs_area']]

    # Putting the GOES flux in a separate df because it contains significantly more entries
    glux = df[['goes_flux']]

    # There are some zero values in area and spot column ---> converting to NaNs and removing those rows
    dfs.srs_area = dfs.srs_area.replace({0: np.nan})

    # Removing the rows containing any NaN values
    dfs = dfs.dropna(how='any')
    glux = glux.dropna(how='any')

    # Re-organising the indicies
    dfs = dfs.reset_index(drop=True)
    glux = glux.reset_index(drop=True)

    # srs_area and srs_no_spots columns are objects --> converting to a float
    dfs['srs_area'] = dfs['srs_area'].astype(float)
    dfs['srs_no_spots'] = dfs['srs_no_spots'].astype(float)

    #==================================================================================================================

    # Plotting CME width and CME angle
    a, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5), facecolor='white', sharey=True)

    ax1.hist(dfc['cme_width'], edgecolor='white', align='mid',
             weights=np.ones(len(dfc['cme_width'])) / len(dfc['cme_width']),
             bins=30)
    ax1.yaxis.set_major_formatter(ticker.PercentFormatter(1))
    ax1.set_xlabel('CME Width [$^\circ$]')
    ax1.set_ylabel('Frequency')

    ax2.hist(dfc['cme_angle'], edgecolor='white', align='mid',
             weights=np.ones(len(dfc['cme_angle'])) / len(dfc['cme_angle']),
             bins=30)
    ax2.yaxis.set_major_formatter(ticker.PercentFormatter(1))
    ax2.yaxis.set_tick_params(labelleft=True)
    ax2.set_xlabel('CME Angle [$^{\circ}$]')

    plt.tight_layout()
    #plt.savefig('cme_hist_perc.png', dpi=300, bbox_inches="tight", pad_inches=1)
    a.show()

    #=================================================================================================================

    # Plotting CME mass and CME kinetic energy
    b, (ax3, ax4) = plt.subplots(1, 2, figsize=(15, 5), facecolor='white')

    ax3.hist(mke['cme_mass'], edgecolor='white', align='mid', bins=30, color='chocolate')
    ax3.set_yscale('log')
    ax3.set_xlabel('CME Mass [g]')
    ax3.set_ylabel('Frequency')

    ax4.hist(mke['cme_kinetic_energy'], edgecolor='white', align='mid', bins=30, color='chocolate')
    ax4.set_yscale('log')
    ax4.set_xlabel('CME KE [erg]')

    plt.tight_layout()
    #plt.savefig('cme_hist_perc2.png', dpi=300, bbox_inches="tight", pad_inches=1)
    b.show()

    #=================================================================================================================

    # Plotting number of sunspots and sunspot area
    c, (ax5, ax6) = plt.subplots(1, 2, figsize=(15, 5), facecolor='white', sharey=True)

    ax5.hist(dfs['srs_no_spots'], edgecolor='white', align='mid', color='rebeccapurple',
             weights=np.ones(len(dfs['srs_no_spots'])) / len(dfs['srs_no_spots']),
             bins=30)
    ax5.yaxis.set_major_formatter(ticker.PercentFormatter(1))
    ax5.set_xlabel('SRS Number')
    ax5.yaxis.set_tick_params(labelleft=True)

    ax6.hist(dfs['srs_area'], edgecolor='white', align='mid', color='rebeccapurple',
             weights=np.ones(len(dfs['srs_area'])) / len(dfs['srs_area']),
             bins=25)
    ax6.yaxis.set_major_formatter(ticker.PercentFormatter(1))
    ax6.set_xlabel('SRS Area [m.s.h]')
    ax6.yaxis.set_tick_params(labelleft=True)

    plt.tight_layout()
    #plt.savefig('srs_hist_perc.png', dpi=300, bbox_inches="tight", pad_inches=1)
    c.show()

    #=================================================================================================================

    # Plotting GOES flux and CME speed
    d, (ax7, ax8) = plt.subplots(1, 2, figsize=(15, 5), facecolor='white', sharey=True)

    # GOES flux
    ax7.hist(np.log10(glux['goes_flux']), edgecolor='white', align='mid', color='mediumseagreen',
             weights=np.ones(len(glux['goes_flux'])) / len(glux['goes_flux']),
             bins=30)
    ax7.yaxis.set_major_formatter(ticker.PercentFormatter(1))
    ax7.set_xlabel('GOES Flux [Wm$^{-2}$]')
    ax7.set_ylabel('Frequency')

    # CME speed
    ax8.hist(dfc['cme_speed'], edgecolor='white', align='mid', color='mediumseagreen',
             weights=np.ones(len(dfc['cme_speed'])) / len(dfc['cme_speed']),
             bins=25)
    ax8.yaxis.set_major_formatter(ticker.PercentFormatter(1))
    ax8.yaxis.set_tick_params(labelleft=True)
    ax8.set_xlabel('CME Speed [kms$^{-1}$]')

    plt.tight_layout()
    #plt.savefig('flux_speed_hist.png', dpi=300, bbox_inches="tight", pad_inches=1)
    d.show()


if __name__ == '__main__':
    main()


