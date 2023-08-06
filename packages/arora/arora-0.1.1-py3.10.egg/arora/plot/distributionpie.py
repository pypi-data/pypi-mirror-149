import matplotlib.pyplot as plt
from typing import Dict


def _pltcolor(lst):
    """
    Bent Ari gave us this code and this is based on his Bsc project
    Args:
        lst:

    Returns:

    """
    cols = []
    for num in lst:
        if num == 0:
            cols.append('fuchsia')  # Wake
        elif num == -1:
            cols.append('blue')  # N1
        elif num == -2:
            cols.append('aqua')  # N
        elif num == -3:
            cols.append('lime')  # N3
        elif num == 5:
            cols.append('orange')  # REM
        elif num == 12:
            cols.append('dodgerblue')  # N1 or N2 (both)
        elif num == -10:
            cols.append('red')
        else:
            cols.append('red')  # other
        return cols


def plot_distrib_pies(distrib_dict: Dict, sleep_stage_map: Dict, pct=False):
    """
    Bent Ari gave us this code and this is based his Bsc project
    Args:
        distrib_dict:
        sleep_stage_map:
        pct:
    """
    f, axs = plt.subplots(10, 6, figsize=(35, 35))
    for i in range(10):
        curr_primarykeys = list(distrib_dict[f'Scorer {i + 1}'].keys())
        curr_primarykeys.sort()
        for j in range(len(curr_primarykeys)):
            key = curr_primarykeys[j]
            labels = []
            sizes = []
            for x, y in distrib_dict[f'Scorer {i + 1}'][key].items():
                labels.append(x)
                sizes.append(y)
            # Plot
            cols = _pltcolor(labels)
            if pct:
                axs[i, j].pie(sizes, labels=labels, autopct='%1.1f%%', colors=cols)
            else:
                axs[i, j].pie(sizes, labels=labels, autopct=autopct_format(sizes), colors=cols)
            axs[i, j].set_title(f"Followup of {sleep_stage_map[key]}")
            axs[i, j].legend([sleep_stage_map[num] for num in labels], bbox_to_anchor=(1.05, 1), loc='upper left',
                             borderaxespad=0., prop={'size': 10})
            axs[i, j].text(0.95, 0.1, f'Switches: {sum(sizes):,}', horizontalalignment='center',
                           verticalalignment='center', transform=axs[i, j].transAxes)
