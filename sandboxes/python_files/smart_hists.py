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
Code to make validation histogram plots of some of the SMART properties

"""

# Packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def main():
    """ Loads the custom solar stats catalogue,
        reorganises the dataframe to contain the SMART properties,
        and plots various validation histogram plots (from HELCATS paper) """

    # Defining the path for the dataframe
    custom_df = 'C:/Users/Peter/py_projects/solar_stats/custom_df.p'

    # Importing the dataframe
    df = pd.read_pickle(custom_df)

    # CME data
    dfs = df[['smart_total_area', 'smart_negative_area', 'smart_positive_area', 'smart_negative_flux',
              'smart_positive_flux', 'smart_flux_fraction', 'smart_b_min', 'smart_b_max', 'smart_b_mean',
              'smart_bipole_separation', 'smart_psl_length', 'smart_r_value', 'smart_wlsg', 'smart_total_flux']]

    # Removing the rows containing any NaN values
    dfs = dfs.dropna(how='any')

    # Reindexing
    dfs = dfs.reset_index(drop=True)

    # flux values are not floats
    dfs['smart_total_flux'] = dfs['smart_total_flux'].astype(float)
    dfs['smart_positive_flux'] = dfs['smart_positive_flux'].astype(float)
    dfs['smart_negative_flux'] = dfs['smart_negative_flux'].astype(float)

    # There are some zero values in the wlsg and psl length columns (also some others but not important ones)
    psl = dfs[['smart_psl_length']]
    wlsg = dfs[['smart_wlsg']]

    # Removing the rows that contain zeros
    psl = psl[(psl[['smart_psl_length']] != 0).all(axis=1)]
    wlsg = wlsg[(wlsg[['smart_wlsg']] != 0).all(axis=1)]

    # Reindexing
    psl = psl.reset_index(drop=True)
    wlsg = wlsg.reset_index(drop=True)

    #==================================================================================================================

    # Plotting total area and flux properties
    a, (ax1, ax2), = plt.subplots(1, 2, figsize=(15, 5), facecolor='white', sharey=True)

    ax1.hist(dfs['smart_total_area'], edgecolor='white', align='mid', color='cornflowerblue',
             weights=np.ones(len(dfs['smart_total_area'])) / len(dfs['smart_total_area']),
             bins=30)
    ax1.yaxis.set_major_formatter(ticker.PercentFormatter(1))
    ax1.set_xlabel('SMART total area [m.s.h]')
    ax1.set_ylabel('Frequency')

    ax2.hist(dfs['smart_total_flux'], edgecolor='white', align='mid', color='cornflowerblue',
             weights=np.ones(len(dfs['smart_total_flux'])) / len(dfs['smart_total_flux']),
             bins=30)
    ax2.yaxis.set_major_formatter(ticker.PercentFormatter(1))
    ax2.yaxis.set_tick_params(labelleft=True)
    ax2.set_xlabel('SMART total flux [Mx]')

    plt.tight_layout()
    #plt.savefig('area_flux_hist.png', dpi=300, bbox_inches="tight", pad_inches=1)
    a.show()

    #=================================================================================================================

    # Plotting Bmin and Bmax
    b, (ax3, ax4) = plt.subplots(1, 2, figsize=(15, 5), facecolor='white', sharey=True)

    ax3.hist(dfs['smart_b_min'], edgecolor='white', align='mid', color='cornflowerblue',
             weights=np.ones(len(dfs['smart_b_min'])) / len(dfs['smart_b_min']),
             bins=30)
    ax3.yaxis.set_major_formatter(ticker.PercentFormatter(1))
    ax3.set_xlabel('SMART B$_{min}$ [G]')
    ax3.yaxis.set_tick_params(labelleft=True)

    ax4.hist(dfs['smart_b_max'], edgecolor='white', align='mid', color='cornflowerblue',
             weights=np.ones(len(dfs['smart_b_max'])) / len(dfs['smart_b_max']),
             bins=25)
    ax4.yaxis.set_major_formatter(ticker.PercentFormatter(1))
    ax4.set_xlabel('SMART B$_{max}$ [G]')
    ax4.yaxis.set_tick_params(labelleft=True)

    plt.tight_layout()
    #plt.savefig('bmin_max_hist.png', dpi=300, bbox_inches="tight", pad_inches=1)
    b.show()

    #=================================================================================================================

    # Plotting PIL length and bipole separation
    c, (ax5, ax6) = plt.subplots(1, 2, figsize=(15, 5), facecolor='white', sharey=True)

    ax5.hist(np.log10(psl['smart_psl_length']), edgecolor='white', align='mid', color='cornflowerblue',
             weights=np.ones(len(psl['smart_psl_length'])) / len(psl['smart_psl_length']),
             bins=30)
    ax5.yaxis.set_major_formatter(ticker.PercentFormatter(1))
    ax5.set_xlabel('SMART PIL length [Mm]')
    ax5.set_ylabel('Frequency')

    ax6.hist(dfs['smart_bipole_separation'], edgecolor='white', align='mid', color='cornflowerblue',
             weights=np.ones(len(dfs['smart_bipole_separation'])) / len(dfs['smart_bipole_separation']),
             bins=25)
    ax6.yaxis.set_major_formatter(ticker.PercentFormatter(1))
    ax6.yaxis.set_tick_params(labelleft=True)
    ax6.set_xlabel('SMART bipole separation [Mm]')

    plt.tight_layout()
    #plt.savefig('pil_bipole_hist.png', dpi=300, bbox_inches="tight", pad_inches=1)
    c.show()

    #=================================================================================================================

    # Plotting R value and WLSG
    d, (ax6, ax7) = plt.subplots(1, 2, figsize=(15, 5), facecolor='white', sharey=True)

    ax6.hist(np.log10(dfs['smart_r_value']), edgecolor='white', align='mid', color='cornflowerblue',
             weights=np.ones(len(dfs['smart_r_value'])) / len(dfs['smart_r_value']),
             bins=30)
    ax6.yaxis.set_major_formatter(ticker.PercentFormatter(1))
    ax6.set_xlabel('SMART R value [Mx]')
    ax6.set_ylabel('Frequency')

    ax7.hist(np.log10(wlsg['smart_wlsg']), edgecolor='white', align='mid', color='cornflowerblue',
             weights=np.ones(len(wlsg['smart_wlsg'])) / len(wlsg['smart_wlsg']),
             bins=25)
    ax7.yaxis.set_major_formatter(ticker.PercentFormatter(1))
    ax7.yaxis.set_tick_params(labelleft=True)
    ax7.set_xlabel('SMART WL$_{SG}$ [G]')

    plt.tight_layout()
    #plt.savefig('r_wlsg_hist.png', dpi=300, bbox_inches="tight", pad_inches=1)
    d.show()

    #=================================================================================================================

    # Plotting PIL and WLSG together on a log scale
    e, (ax8, ax9) = plt.subplots(1, 2, figsize=(15, 5), facecolor='white')

    ax8.hist(psl['smart_psl_length'], edgecolor='white', align='mid', bins=30, color='mediumvioletred')
    ax8.set_yscale('log')
    ax8.set_xlabel('SMART PIL length [Mm]')
    ax8.set_ylabel('Frequency')

    ax9.hist(dfs['smart_bipole_separation'], edgecolor='white', align='mid', bins=30, color='mediumvioletred')
    ax9.set_yscale('log')
    ax9.set_xlabel('SMART bipole separation [Mm]')

    plt.tight_layout()
    #plt.savefig('psl_bip_loghist.png', dpi=300, bbox_inches="tight", pad_inches=1)
    e.show()

    #=================================================================================================================


if __name__ == '__main__':
    main()


