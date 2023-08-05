
# Jaesub Hong (jhong@cfa.harvard.edu)

import cjson
from collections import OrderedDict

import pandas
import astropy
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm	 as cm
import matplotlib		 as mpl
from matplotlib.patches		import Circle
from matplotlib			import rc,rcParams
from mpl_toolkits.axes_grid1  import make_axes_locatable

import tabletool as tt
import numpy as np
import math

from astropy.io import fits

from scipy import optimize as opt
from scipy import ndimage

from os		import path
from functools	import wraps

from IPython	import embed

def help_rcParams():
	text=OrderedDict()
	text["figure.figsize"       ] ="changes the figure size; keeps the font size the same"
	text["figure.dpi"		    ] ="changes the figure size; keep relative size of font to figure the same"
	text["font.size"		    ] ="change the font size; keeps the figure size the same"

	text["axes.labelsize"	    ] ="Fontsize of the x and y labels"
	text["axes.titlesize"	    ] ="Fontsize of the axes title"
	text["figure.titlesize"	    ] ="Size of the figure title (Figure.suptitle())"
	text["xtick.labelsize"	    ] ="Fontsize of the tick labels"
	text["ytick.labelsize"	    ] ="Fontsize of the tick labels"
	text["legend.fontsize"	    ] ="Fontsize for legends (plt.legend(), fig.legend())"
	text["legend.title_fontsize"] ="Fontsize for legend titles, None sets to the same as the default axes."
	return text

def help_text(param):
	if param != None:
		if param == "basics":
			print("rcParams:")
			cjson.show(help_rcParams(),  notype=True)
			print("e.g., -*#rcParams:figure.figsize '12,10'")
		else:
			print("available help words: basics")
		exit()

#----------------------------------------------------------------------------------------
def read(infile, x=None, y=None, hdu=1, data=None,
		xlabel=None, ylabel=None,
		ftype=None, nopandas=True):
	if type(data).__name__ == "NoneType":
		if infile == None: 
			print("input data or file is required.")
			return None, None, None, None, None 

		if not path.isfile(infile):
			print("cannot read the file:", infile)
			return None, None, None, None, None

		data=tt.from_csv_or_fits(infile, ftype=ftype, hdu=hdu, nopandas=nopandas)

	if x == None or y == None:
		if   type(data) is pandas.core.frame.DataFrame: colnames=data.columns.values.tolist()
		elif type(data) is   astropy.table.table.Table: colnames=data.colnames
		else: print('need to know column names or provide -x and -y')

#		colnames=data.colnames
		if x == None: x=colnames[0]
		if y == None: y=colnames[1]
	
	# default label
	if xlabel == None:
		xlabel = x 
		if hasattr(data[x],'info'):
			if hasattr(data[x].info,'unit'):
				xunit=data[x].info.unit
				if xunit != None: xlabel = xlabel +' ('+str(xunit)+')'

	if ylabel == None:
		ylabel = y 
		if hasattr(data[y],'info'):
			if hasattr(data[y].info,'unit'):
				yunit=data[y].info.unit
				if yunit != None: ylabel = ylabel +' ('+str(yunit)+')'
	return data, x, y, xlabel, ylabel
	
def set_range(xdata, ydata, margin=None, xr=None, yr=None, 
		xscale='linear', yscale='linear', drawdown=None):

#	embed()
	if type(xr) is list: 
		if xr[0] == None: xr = None
	if type(yr) is list: 
		if yr[0] == None: yr = None
	
	if type(xr).__name__ == 'NoneType': xr= cjson.minmax(xdata, nonzero= xscale != 'linear')
	if type(yr).__name__ == 'NoneType': yr= cjson.minmax(ydata, nonzero= yscale != 'linear')

	if margin != None:
		if type(margin) is not list:
			xr = add_margin(xr, margin=margin, scale=xscale, drawdown=drawdown)
			yr = add_margin(yr, margin=margin, scale=yscale, drawdown=drawdown)
		elif len(margin) == 2:
			xr = add_margin(xr, margin=margin[0], scale=xscale, drawdown=drawdown)
			yr = add_margin(yr, margin=margin[1], scale=yscale, drawdown=drawdown)
		elif len(margin) == 4:
			xr = add_margin(xr, margin=margin[0:1], scale=xscale, drawdown=drawdown)
			yr = add_margin(yr, margin=margin[2:3], scale=yscale, drawdown=drawdown)

	return xr, yr

def get_log_edges(vr, nbin):
	logvr = [math.log(vr[0],10), math.log(vr[1],10)]
	logslope = logvr[1] - logvr[0]
	return [10.0**(logslope*v/nbin+logvr[0]) for v in range(0,nbin+1)]

def add_margin(prange, margin=None, scale='linear', drawdown=None):

	if   margin == None     : margin=[0.2,0.2]
	elif np.isscalar(margin): margin=[margin, margin]
	if scale == 'linear':
		diff=prange[1]-prange[0]
		prange=[prange[0]-margin[0]*diff,prange[1]+margin[1]*diff]
	else:
		if prange[0] <= 0.0:
			if drawdown == None: drawdown = 1.e-5
			prange[0]=prange[1]*drawdown

		logpr = [math.log(v,10) for v in prange]
		diff = logpr[1]-logpr[0]
		logpr=[logpr[0]-margin[0]*diff,logpr[1]+margin[1]*diff]
		prange=[10.0**v for v in logpr]

	return prange

def filter_by_range(xdata, ydata, xr, yr):
	mask = xdata >= xr[0] and xdata <= xr[1] and ydata >= yr[0] and ydata <= yr[1] 
	xdata=xdata[mask]
	ydata=ydata[mask]
#	if filter:
#		 data=data[data[x] >= xr[0]]
#		 data=data[data[x] <= xr[1]]
#		 data=data[data[y] >= yr[0]]
#		 data=data[data[y] <= yr[1]]

	return xdata, ydata

#----------------------------------------------------------------------------------------
def set_rcParams(rcParams=None, verbose=0):
	if rcParams == None: return
	for key, val in rcParams.items():
		if verbose >=2: print(key,val)
		plt.rcParams[key] = val
	
def set_fig_basics(figsize=None, dpi=None, fontsize=None, 
		legendsize=None, titlesize=None):
	# changes the figure size; keeps the font size the same
	if figsize != None: 
		plt.rcParams["figure.figsize"] = (float(figsize[0]), float(figsize[1]))

	# changes the figure size; keep relative size of font to figure the same
	if dpi != None: 
		plt.rcParams["figure.dpi"] = int(dpi)

	# change the font size; keeps the figure size the same
	if fontsize != None:
		plt.rcParams["font.size"] = float(fontsize)

	# xx-small, x-small, small, medium, large, x-large, xx-large, smaller, larger.

	if legendsize != None:
		plt.rcParams["legend.fontsize"] = legendsize

	if titlesize != None:
		plt.rcParams["axes.titlesize"] = titlesize

#----------------------------------------------------------------------------------------
def wrap(plt, xr, yr, xlabel, ylabel, title="", xscale='linear', yscale='linear', outfile=None, 
		display=True, ion=False):
	plt.xlim(xr)
	plt.ylim(yr)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.title(title)
	plt.xscale(xscale)
	plt.yscale(yscale)
	plt.tight_layout()
	if not ion: 
		if outfile != None: plt.savefig(outfile)
		else: 
			if display: plt.show()

#----------------------------------------------------------------------------------------
def prep_data_deco(func):

	@wraps(func)
	def prep_data(xdata, ydata, *args, 
			data=None, infile=None, x=None, y=None, xlabel=None, ylabel=None, 
			xr=None, yr=None, margin=None, drawdown=None, filter=False,
			xscale='linear', yscale='linear', xlog=False, ylog=False, 
			rcParams=None, figsize=None, dpi=None, 
			fontsize=None, legendsize=None, titlesize=None, verbose: int=0,
			ftype=None, hdu=1, help=None, **kwargs):

		help_text(help)

		if type(xdata).__name__ == "NoneType":
			data, x, y, xlabel, ylabel = read(infile, x=x, y=y, data=data, 
					xlabel=xlabel, ylabel=ylabel, ftype=ftype, hdu=hdu)
			if type(data).__name__ == "NoneType": return False

			xdata=data[x]
			ydata=data[y]

		if xscale == None: 
			xscale = 'log' if xlog else 'linear'
		if yscale == None: 
			yscale = 'log' if ylog else 'linear'

		xr, yr =  set_range(xdata, ydata, xr=xr, yr=yr, 
				margin=margin, drawdown=drawdown,
				xscale=xscale, yscale=yscale)

		if filter:
			xdata, ydata = filter_by_range(xdata, ydata, xr, yr)

		set_rcParams(rcParams, verbose=verbose)
		set_fig_basics(figsize=figsize, dpi=dpi, fontsize=fontsize, 
				legendsize=legendsize, titlesize=titlesize)

		return func(xdata, ydata, *args, 
			data=data, xlabel=xlabel, ylabel=ylabel, 
			xr=xr, yr=yr, xscale=xscale, yscale=yscale, 
			verbose=verbose, help=None, **kwargs)

	return prep_data

#----------------------------------------------------------------------------------------
@prep_data_deco
def plot1d(xdata, ydata, data=None, 
		xr=None, yr=None, 
		outfile=None, 
		xscale='linear', yscale='linear',
		xlabel=None, ylabel=None, 
		marker='.', linestyle='None', color=None,
		help=None, hold=False, verbose: int= 0):
	"""Plot 1-D from input table
	"""

	def show(ion=True):
		if ion: plt.ion()
		plt.plot(xdata, ydata,
				color=color,
				marker=marker, linestyle=linestyle)

		wrap(plt, xr, yr, xlabel, ylabel, 
				xscale=xscale, yscale=yscale, outfile=outfile, ion=ion)

	show(ion=False)
	if hold: embed()

	return plt

@prep_data_deco
def dplot(xdata, ydata, data=None, 
		xr=None, yr=None, 
		outfile=None, 
		xscale=None, yscale=None,
		xlabel=None, ylabel=None, title=None,
		binx=None, biny=None, nbinx=100, nbiny=100, nbin=None, binsize=None,
		zlog=False, zmin=0, cmap='Blues', aspect='auto',
		interpolation=None, display=True,
		help=None, hold=False, verbose:int= 0):
	""" 2-d density plot 
	"""

	if binsize != None:  binx,  biny = binsize, binsize
	if nbin    != None: nbinx, nbiny = nbin,    nbin

	if binx==None:  binx = (xr[1]-xr[0])/nbinx
	else:          nbinx = int((xr[1]-xr[0])/binx)

	if biny==None:  biny = (yr[1]-yr[0])/nbiny
	else:          nbiny = int((yr[1]-yr[0])/biny)

	xedges, yedges = nbinx, nbiny

	if xscale == 'log': xedges = get_log_edges(xr, nbinx)
	if yscale == 'log': yedges = get_log_edges(yr, nbiny)

	bins = [xedges, yedges]

	# to get zmax
	heatmap, *_ = np.histogram2d(xdata, ydata, bins=bins)
	zmax=np.max(heatmap.T)

	def show(ion=True):

		if ion: plt.ion()
		if not zlog:
			image, xedges, yedges, qmesh = plt.hist2d(xdata, ydata, bins=bins, cmap=cmap)
		else:
			# log, with negative
			zmin_= 0.5 if zmin == 0 else zmin

			image, xedges, yedges, qmesh = plt.hist2d(xdata, ydata, 
					norm=colors.LogNorm(vmin=zmin_, vmax=zmax),
					bins=bins,  cmap=cmap)
		plt.colorbar()

		wrap(plt, xr, yr, xlabel, ylabel, title=title,
				xscale=xscale, yscale=yscale, outfile=outfile, ion=ion, display=display)
		return image

	image = show(ion=False)
	if hold: embed()

	return image

