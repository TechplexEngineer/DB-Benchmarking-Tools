#!/usr/bin/env python

###
# Code to calculate statictics from dump file
# B.Bourque 7/8/2015
###

import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
from datetime import datetime, timedelta

# This function expects the data in [filename] to be tab separated.
# Col1 is the unix timestamp and col2 is the database transactions per second
def genstats(filename, start, end, plot=False, print_dates=False):
	
	data =  np.loadtxt(filename, delimiter='\t')

	st = data[:,0][0] # get the first timestamp, col 0 row 0
	st = datetime.fromtimestamp(st)


	# x values
	dates=[(datetime.fromtimestamp(ts) - timedelta(hours=st.hour, minutes=st.minute, seconds=st.second)) for ts in data[:,0]]

	# if end is not a positive number, then end is the length of the data
	if end < 0:
		end = len(data)-1

	# If start is negative, then its 0
	if start < 0:
		start = 0

	print "start\t\t:", start
	print "start_date\t:", dates[start]
	print "end\t\t:", end
	print "end_date\t:", dates[end]
	print "elasped\t\t:", (dates[end]-dates[start])
	print "avg\t\t:", np.average(data[start:end,1])

	print "{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format(start,end,dates[start],dates[end],(dates[end]-dates[start]),np.average(data[start:end,1]))

	if plot:
		if print_dates:
			plt.plot(dates[start:end], data[start:end,1], 'b-o')
		else:
			plt.plot(data[start:end,1], 'b-o')
		plt.ylabel('TPS')
		plt.xlabel('Time')
		plt.title("TPS "+filename)

		plt.minorticks_on()
		plt.grid()
		if print_dates:
			ax=plt.gca()
			xfmt = md.DateFormatter('%H:%M:%S')
			ax.xaxis.set_major_formatter(xfmt)

		plt.show()


if __name__ == "__main__":
	print "Test Routine"

	genstats("testdata.txt", 0, -1, plot=True, print_dates=True)

	genstats("testdata.txt", 0, -1, plot=True, print_dates=False)

	genstats("testdata.txt", 0, -1, plot=False, print_dates=True)