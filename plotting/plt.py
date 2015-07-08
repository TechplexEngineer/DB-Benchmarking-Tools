#!/usr/bin/env python

###
# Code to calculate a series of statistics from dump file
# B.Bourque 7/8/2015
###

from genstats import genstats


def genmystats(filename, skip, end, hr=False,):
	
	print "Calculating stats for: {0}".format(filename)
	# Whole Range
	genstats(filename, start=0, end=-1, numpts=-1, plot=False, print_dates=False, human_readable=hr)
	# Skip starting data
	genstats(filename, start=skip, end=-1, numpts=-1, plot=False, print_dates=False, human_readable=hr)
	# Skip the starting and ending data
	genstats(filename, start=skip, end=end, numpts=-1, plot=False, print_dates=False, human_readable=hr)
	# Skip the starting data and show 2hrs data
	genstats(filename, start=skip, end=-1, numpts=7100, plot=False, print_dates=False, human_readable=hr)
	# Skip the starting data and ending. show 1hr data
	genstats(filename, start=skip, end=-1, numpts=3550, plot=False, print_dates=False, human_readable=hr)
	# First 500 data points
	genstats(filename, start=0, end=-1, numpts=500, plot=False, print_dates=False, human_readable=hr)
	# First 1000 data points
	genstats(filename, start=0, end=-1, numpts=1000, plot=False, print_dates=False, human_readable=hr)
	# First 1500 data points
	genstats(filename, start=0, end=-1, numpts=1500, plot=False, print_dates=False, human_readable=hr)
	# First 1000 good data points
	genstats(filename, start=skip, end=-1, numpts=1000, plot=False, print_dates=False, human_readable=hr)
	# First 500 good data points
	genstats(filename, start=skip, end=-1, numpts=500, plot=False, print_dates=False, human_readable=hr)
	# First 250 good data points
	genstats(filename, start=skip, end=-1, numpts=250, plot=False, print_dates=False, human_readable=hr)


genmystats(filename="5_1200vusers.txt", skip=100, end=150000, hr=False)
genmystats(filename="5_1200vusers.txt", skip=33700, end=150000, hr=False)

# genmystats(filename="10_1200vusers.txt", skip=100, end=14000, hr=False)


# genstats("5_1200vusers.txt", start=0, end=-1, numpts=-1, plot=True, print_dates=False, human_readable=False)