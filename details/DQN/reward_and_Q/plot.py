"""
Take the data in the results folder and plot it so we can stop using stupid
Excel.
"""

import glob
import os
import csv
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np



def movingaverage(y, window_size):
    """
    Moving average function from:
    http://stackoverflow.com/questions/11352047/finding-moving-average-from-data-points-in-python
    """
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(y, window, 'same')


def readable_output(filename):
    readable = ''
    # Example:
    # learn_data-1000-1000-32-10000.csv
    f_parts = filename.split('-')

    if f_parts[0] == 'learn_data':
        readable += 'distance: '
    else:
        readable += 'loss: '

    readable += f_parts[1] + ', ' + f_parts[2] + ' | '
    readable += f_parts[3] + ' | '
    readable += f_parts[4].split('.')[0]

    return readable


def plot_file(filename, type='loss'):
    with open(f, 'r') as csvfile:
        reader = csv.reader(csvfile)
        # Turn our column into an array.
        y = []
        for row in reader:
            if type == 'loss':
                y.append(float(row[0]))
            else:
                y.append(float(row[1]))
        y = y[:10000]
        # Running tests will be empty.
        if len(y) == 0:
            return


        # Get the moving average so the graph isn't so crazy.
        if type == 'loss':
            window = 10
        else:
            window = 10
        y_av = movingaverage(y, window)

        # Use our moving average to get some metrics.
        arr = np.array(y_av)
        if type == 'loss':
            print("%f\t%f\n" % (arr.min(), arr.mean()))
        else:
            print("%f\t%f\n" % (arr.max(), arr.mean()))

        # Plot it.
        plt.clf()  # Clear.
        plt.title(f)
        # The -50 removes an artificial drop at the end caused by the moving
        # average.
        if type == 'loss':
            plt.plot(y_av[:-50])
            plt.ylabel('Smoothed Loss')

        plt.savefig(f + '.png', bbox_inches='tight')


if __name__ == "__main__":
    # Get our loss result files.
    os.chdir("./")

    for f in glob.glob("loss*.csv"):
        plot_file(f, 'loss')
