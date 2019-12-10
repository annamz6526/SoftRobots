import pickle



"""
Take the data in the results folder and plot it so we can stop using stupid
Excel.
"""

import glob
import os
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

		# Turn our column into an array.
	y = []
	with open(filename, 'rb') as file:
		y = pickle.load(file)

		# Running tests will be empty.
	if len(y) == 0:
		return


	# Get the moving average so the graph isn't so crazy.
	if type == 'loss':
		window = 1
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
		plt.ylabel('Smoothed Q')

	plt.savefig(f + '.png', bbox_inches='tight')


if __name__ == "__main__":
	# Get our loss result files.
	os.chdir("./")
	f = "Q"
	plot_file('Q.txt', 'loss')
	with open('reward.txt', 'rb') as f:
		mylist = pickle.load(f)

	print("reward")
	print(mylist)
	with open('qvalue.txt', 'rb') as f:
		mylist = pickle.load(f)

	print("qvalue")
	print(mylist)
# with open('reward.txt', 'rb') as f:
# 	mylist = pickle.load(f)

# print("reward")
# print(mylist)

# with open('qvalue.txt', 'rb') as f:
# 	mylist = pickle.load(f)

# print("qvalue")
# print(mylist)