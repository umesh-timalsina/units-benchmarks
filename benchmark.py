import os
import sys
import time
import argparse

import numpy as np
from matplotlib import pyplot as plt


PKG_IMPORT = """python -c 'import {}'"""


class UnitBenchMarker:
    """Perform benchmark tests for different unit packages"""

    def plot_import_times(self, repeat=10, filename=None):
        """Plot import times for unyt vs. pint repeated over repeat times
        
        
        Parameters
        ----------
        repeat: int, default=10
            Repeat imports this number of times
        filname: str, default=None
            In not none, save the matplotlib figure to this file
        """
        x = range(0, repeat)
        unyt_times = []
        pint_times = []
        for j in range(repeat):
            start = time.perf_counter()
            os.system(PKG_IMPORT.format('unyt'))
            unyt_times.append(time.perf_counter() - start)
            start = time.perf_counter()
            os.system(PKG_IMPORT.format('pint'))
            pint_times.append(time.perf_counter() - start)

        plt.plot(x, pint_times, color='r', label='pint', marker='o')
        plt.plot(x, unyt_times, color='g', label='unyt', marker='o')
        plt.xlabel('Trail')
        plt.ylabel('Time (secs)')
        plt.legend(loc='upper left')
        
        fig = plt.gcf()
        fig.suptitle(f'Import times for unyt vs pint (repeated over {repeat} iterations)')

        self._add_tables(unyt_times, pint_times)

        if filename is not None:
            plt.savefig(filename, figsize=(10, 8))
        else:
            plt.show()
    
    def _add_tables(self, unyt_times, pint_times):
        unyt_median = round(np.median(unyt_times), 5)
        pint_median = round(np.median(pint_times), 5)
        
        unyt_mean = round(np.mean(unyt_times), 5)
        pint_mean = round(np.mean(pint_times), 5)

        unyt_std_dev = round(np.std(unyt_times), 5)
        pint_std_dev = round(np.std(pint_times), 5)

        row_labels = ['Mean', 'Median', '$\sigma$']
        col_labels = ['unyt', 'pint']
        
        plt.table(
            cellText=[[unyt_mean, pint_mean], [unyt_median, pint_median], [unyt_std_dev, pint_std_dev]],
            rowLabels=row_labels,
            colLabels=col_labels,
            colWidths = [0.2]*3,
            loc='center right',
        )


        
def parse_args():
    parser = argparse.ArgumentParser(description=UnitBenchMarker.__doc__)
    subparsers = parser.add_subparsers(help='Sub Commands')
    plot_subcommand = subparsers.add_parser('plot', description='Plot import times for pint vs unyt')
    plot_subcommand.add_argument('--repeat', default=10, type=int, help='The number of times to repeat import')
    plot_subcommand.add_argument('--filename', default=None, type=str, help='Save the import times plot to this file')
    prog_args = parser.parse_args()
    return prog_args


if __name__ == "__main__":
    args = parse_args()
    bm = UnitBenchMarker()
    if 'plot' in sys.argv:
        bm.plot_import_times(repeat=args.repeat, filename=args.filename)


