
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
#from mpl_toolkits.axes_grid1  import make_axes_locatable
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

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
	
def minmax(data, nonzero=False):
	if nonzero: 
		data=np.array(data)
		return [np.min(data[np.nonzero(data)]), np.max(data)]
	else:       return [np.min(data), np.max(data)]

def set_range(data, margin=None, 
		dr=None, # data range
		scale='linear', drawdown=None):

#	embed()
	if type(dr) is list: 
		if dr[0] == None: dr = None
	
	if type(dr).__name__ == 'NoneType': dr= minmax(data, nonzero= scale != 'linear')

	if margin != None:
		dr = add_margin(dr, margin=margin, scale=scale, drawdown=drawdown)

	return dr

def set_range_2D(xdata, ydata, margin=None, xr=None, yr=None, 
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

def val2pix(val, vr=None, pr=None):
	# value to pixel
	slope=(pr[1]-pr[0])/(vr[1]-vr[0])
	if type(val) is not list:
		return int(slope*(val-vr[1])+pr[0])
	return [int(slope*(v-vr[1])+pr[0]) for v in val]

def pix2val(pix, vr=None, pr=None):
	# pixel to value
	slope=(vr[1]-vr[0])/(pr[1]-pr[0])
	if type(pix) is not list:
		return slope*(pix-pr[0])+vr[0]
	return [slope*(p-pr[0])+vr[0] for p in pix]

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
		rect=[0,0,1,1],
		label=True, display=True, ion=False):

	if label:
		plt.xlabel(xlabel)
		plt.ylabel(ylabel)
#		print('rect',rect)
		# this needs a clean up
		plt.title(title, y=rect[3]+(rect[3]-1)*20.)

	plt.xlim(xr)
	plt.ylim(yr)
	plt.xscale(xscale)
	plt.yscale(yscale)
	plt.tight_layout(rect=rect)
	if not ion: 
		if outfile != None: plt.savefig(outfile)
		else: 
			if display: plt.show()

def colorbar(cbar, im, ax, fig, orientation=None, ticks_position=None):
	cax = ax.inset_axes(cbar) #, transform=ax.transAxes)
	fig.colorbar(im, 
			orientation=orientation,
			cax=cax)
	if ticks_position != None:
		if ticks_position == 'left' or ticks_position == 'right':
			cax.yaxis.set_ticks_position(ticks_position)
		if ticks_position == 'bottom' or ticks_position == 'top':
			cax.xaxis.set_ticks_position(ticks_position)

def colorbar_set(cbar, im, ax, fig, 
		xlabel=None, ylabel=None, title=None,
		off=None, width=None, length=None, rect=[0.,0.,1.,1.],
		orientation=None, outside=False):

	if not outside:
		if off    == None: off    = 0.03
		if width  == None: width  = 0.03
		if length == None: length = 0.5-off
		loff = 1.0-length-off
		woff = 1.0-width-off
		if orientation == 'vertical':
			if cbar == 'lower,left':
				rect=[off,off,width,length]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='right')
			elif cbar == 'upper,left':
				rect=[off,loff,width,length]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='right')
			elif cbar == 'lower,right':
				rect=[woff,off,width,length]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='left')
			elif cbar == 'upper,right':
				rect=[woff,loff,width,length]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='left')
		elif orientation == 'horizontal':
			if cbar == 'lower,left':
				rect=[off,off,length,width]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='top')
			elif cbar == 'upper,left':
				rect=[off,woff,length,width]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='bottom')
			elif cbar == 'lower,right':
				rect=[loff,off,length,width]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='top')
			elif cbar == 'upper,right':
				rect=[loff,woff,length,width]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='bottom')
	else:
		if width  == None: width  = 0.03
		if length == None: length = 0.5
		if off    == None: off    = -0.10 - width
		loff = 0.5
		woff = 1.02
		y=rect[3]+(rect[3]-1)*20.
		if orientation == 'vertical':
			if cbar == 'lower,left':
				rect=[off,0,width,length]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='left')
				ax.set_xlabel(xlabel)
				ax.set_ylabel(ylabel, loc='top')
			elif cbar == 'upper,left':
				rect=[off,loff,width,length]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='left')
				ax.set_xlabel(xlabel)
				ax.set_ylabel(ylabel, loc='bottom')
			elif cbar == 'lower,right':
				rect=[woff,0,width,length]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='right')
				ax.set_xlabel(xlabel)
				ax.set_ylabel(ylabel)
			elif cbar == 'upper,right':
				rect=[woff,loff,width,length]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='right')
				ax.set_xlabel(xlabel)
				ax.set_ylabel(ylabel)
			ax.set_title(title, y=y)
		elif orientation == 'horizontal':
			if cbar == 'lower,left':
				ax.set_xlabel(xlabel,loc='right')
				ax.set_title(title, y=y)
				rect=[0,off,length,width]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='bottom')
			elif cbar == 'upper,left':
				ax.set_xlabel(xlabel)
				ax.set_title(title, y=y, loc='right')
				rect=[0,woff,length,width]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='top')
			elif cbar == 'lower,right':
				ax.set_xlabel(xlabel, loc='left')
				ax.set_title(title,y=y)
				rect=[loff,off,length,width]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='bottom')
			elif cbar == 'upper,right':
				ax.set_xlabel(xlabel)
				ax.set_title(title, y=y, loc='left')
				rect=[loff,woff,length,width]
				colorbar(rect, im, ax, fig, 
					orientation=orientation,
					ticks_position='top')
			ax.set_ylabel(ylabel)

def despine_axes(ax, despine):
	if despine == None: despine = False
	if type(despine) is bool:
		if despine:
			ax.spines['top'].set_visible(False)
			ax.spines['right'].set_visible(False)
	else:
		for each in despine.split(','):
			ax.spines[each].set_visible(False)

#----------------------------------------------------------------------------------------
def hist2line(edges, values):
	x, y = [edges[0]], [values[0]]
	for i in range(1, len(values)):
		x.append(edges[i])
		x.append(edges[i])
		y.append(values[i-1])
		y.append(values[i])
	x.append(edges[-1])
	y.append(values[-1])
	return x, y

#----------------------------------------------------------------------------------------
def prep_data_deco(func):

	@wraps(func)
	def prep_data(xdata, ydata, *args, 
			data=None, image=None, infile=None, x=None, y=None, xlabel=None, ylabel=None, 
			xr=None, yr=None, margin=0.0, drawdown=None, filter=False,
			xscale=None, yscale=None, xlog=False, ylog=False, 
			rcParams=None, figsize=None, dpi=None, 
			clip=None,  # pixel coordinates
			fontsize=None, legendsize=None, titlesize=None, verbose: int=0,
			ftype=None, hdu=None, help=None, **kwargs):

		help_text(help)

		loaded = None

		# try loading an image
		if type(image) is bool:
			if image:
				# read image
				# assume fits image for now
				hdul=fits.open(infile)
				if hdu == None: hdu=0
#				image=np.transpose(hdul[hdu].data)
				image=hdul[hdu].data
				loaded='image'
		elif type(image).__name__ != "NoneType":
			loaded='image'

		# make sure 2-d image and clip if requested
		if loaded == "image":
			ndim = image.ndim
			if ndim == 3: 
				image = image.sum(axis=0)
			image=np.transpose(image)
			#print(image.shape)

			if type(clip) is list:
				# x and y seem to be swapped
				#image=image[clip[2]:clip[3],clip[0]:clip[1]]
				image=image[clip[0]:clip[1],clip[2]:clip[3]]

			nbinx, nbiny=image.shape
			#print(nbinx,nbiny)
			if type(clip) is not list:
				if xr == None: xr=[0,nbinx]
				if yr == None: yr=[0,nbiny]
			else:
				if xr == None: xr=[clip[0],clip[1]]
				if yr == None: yr=[clip[2],clip[3]]

		# if there is no image then try loading a table
		if type(xdata).__name__ == "NoneType" and loaded == None:
			if hdu == None: hdu=1
			data, x, y, xlabel, ylabel = read(infile, x=x, y=y, data=data, 
					xlabel=xlabel, ylabel=ylabel, ftype=ftype, hdu=hdu)
			if type(data).__name__ == "NoneType": return False

			xdata=data[x]
			ydata=data[y]
			loaded='table'

		if xscale == None: 
			xscale = 'log' if xlog else 'linear'
		if yscale == None: 
			yscale = 'log' if ylog else 'linear'

		xr, yr =  set_range_2D(xdata, ydata, xr=xr, yr=yr, 
				margin=margin, drawdown=drawdown,
				xscale=xscale, yscale=yscale)

		if filter:
			if loaded == 'table':
				xdata, ydata = filter_by_range(xdata, ydata, xr, yr)
				# need to clip the image

		set_rcParams(rcParams, verbose=verbose)
		set_fig_basics(figsize=figsize, dpi=dpi, fontsize=fontsize, 
				legendsize=legendsize, titlesize=titlesize)

		return func(xdata, ydata, *args, 
			data=data, image=image, xlabel=xlabel, ylabel=ylabel, 
			xr=xr, yr=yr, xscale=xscale, yscale=yscale, 
			margin=margin, drawdown=drawdown,
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
def dplot(xdata, ydata, image=None, data=None,
		xr=None, yr=None, zr=None,
		zmin=None, zmax=None,
		outfile=None, 
		xscale=None, yscale=None,
		xlabel=None, ylabel=None, title=None,
		binx=None, biny=None, nbinx=100, nbiny=100, nbin=None, binsize=None,
		zlog=False, cmap='Blues', aspect='auto',
		interpolation=None, display=True,
		cbar=True, cb_orientation='vertical', cb_ticks_position='right', cb_outside=False,
		cb_off=None, cb_width=None, cb_length=None,
		xhist=False, xh_height=0.15, xh_scale=None, 
		yhist=False, yh_height=0.15, yh_scale=None, 
		xslice=None, yslice=None, # data coordinateslike xr or yr (not necessarily pixels)
		halpha=0.3, hcolor="darkblue", hgap=0.04, hheight: float=0.15,
		despine=None, margin=0.0, drawdown=None,
		help=None, hold=False, verbose:int= 0):
	""" 2-d density plot 
	"""

	if type(image).__name__ == 'NoneType':
		# data points
		if binsize != None:  binx,  biny = binsize, binsize
		if nbin    != None: nbinx, nbiny = nbin,    nbin

		if binx==None:  binx = (xr[1]-xr[0])/nbinx
		else:          nbinx = int((xr[1]-xr[0])/binx)

		if biny==None:  biny = (yr[1]-yr[0])/nbiny
		else:          nbiny = int((yr[1]-yr[0])/biny)
		doimage=False
	else:
		# image input
		# assume xr, and yr is given, and probably no log scale for x and y axes?
		nbinx, nbiny = image.shape
#		ndim = image.ndim
#		if   ndim == 2: nbinx, nbiny = image.shape
#		elif ndim == 3: 
#			nbinz, nbinx, nbiny = image.shape
#			image = image.sum(axis=0)
		if zmax == None: zmax = np.max(image)
		if zmin == None: zmin = np.min(image)
		binx = (xr[1]-xr[0])/nbinx
		biny = (yr[1]-yr[0])/nbiny
		doimage=True


	xedges, yedges = nbinx, nbiny
	if xscale == 'log': xedges = get_log_edges(xr, nbinx)
	if yscale == 'log': yedges = get_log_edges(yr, nbiny)
	bins = [xedges, yedges]

	if not doimage:
		# to get zmax
		heatmap, *_ = np.histogram2d(xdata, ydata, bins=bins)
		if zmax == None: zmax=np.max(heatmap.T)
		if zmin == None: zmin=np.min(heatmap.T)
		weights = None
	else:
		if type(xedges) is not list:
			xedges_ = [ii*binx+xr[0]+binx*0.5 for ii in range(0,nbinx)]
		else:
			xedges_ = [(v+w)*0.5 for v, w in zip(xedges[:-1:], xedges[1::])]

#		xdata   = xedges_ * nbiny
		xdata   = [[v]  * nbiny for v in xedges_]
		xdata   = np.array(xdata).flatten()

		if type(xedges) is not list:
			yedges_ = [ii*binx+yr[0]+binx*0.5 for ii in range(0,nbiny)]
		else:
			yedges_ = [(v+w)*0.5 for v, w in zip(yedges[:-1:], yedges[1::])]
#		ydata   = [[v]  * nbinx for v in yedges_]
#		ydata   = np.array(ydata).flatten()
		ydata   = yedges_ * nbinx

		weights = image.flatten()

	def show(ion=True):

		nonlocal zmin,zmax
		fig, ax = plt.subplots()

		if ion: plt.ion()
		if not zlog:
			if zr != None: 
				zmin =zr[0]
				zmax =zr[1]

			image, xedges, yedges, im = ax.hist2d(xdata, ydata, bins=bins, 
					norm=colors.Normalize(vmin=zmin, vmax=zmax),
					cmap=cmap, weights=weights)
#			image, xedges, yedges, im = plt.hist2d(xdata, ydata, bins=bins, cmap=cmap)
		else:
			# log, with negative
			zmin_= 0.5 if zmin <= 0 else zmin

			if zr != None: 
				zmin =zr[0]
				zmax =zr[1]

#			norm = colors.LogNorm(vmin=zmin_, vmax=zmax)
			image, xedges, yedges, im = ax.hist2d(xdata, ydata, weights=weights,
					norm=colors.LogNorm(vmin=zmin_, vmax=zmax),
					bins=bins,  cmap=cmap)
#			cm = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)

		nonlocal cbar, despine, cb_outside, margin, xslice, yslice

		if xhist or yhist:
			if despine == None: despine=True
		despine_axes(ax, despine)

		if xhist:
			nonlocal xh_height, xh_scale
			xax= ax.inset_axes([0,1.+hgap,1,hheight] , transform=ax.transAxes, sharex=ax)
			if yslice != None:
				if type(yslice) is not list: 
					p2v=pix2val([0,1], vr=yr, pr=[0,nbiny])
					p2v=p2v[1]-p2v[0]
					yslice=[yslice,yslice+p2v]
				pix_yslice=val2pix(yslice, vr=yr, pr=[0,nbiny])
				if pix_yslice[0] == pix_yslice[1]: pix_yslice[1]=pix_yslice[1]+1
				xh = image[:,pix_yslice[0]:pix_yslice[1]].sum(axis=1)
				ax.plot([xr[0],xr[0]],yslice, marker='D', clip_on=True, color='black')
				ax.plot([xr[1],xr[1]],yslice, marker='D', clip_on=True, color='black')
				if not doimage:
					xdata_=xdata[ydata >= yslice[0] and ydata <= yslice[1]]
				else:
					xdata_=xdata
			else:
				xh = image.sum(axis=1)
				xdata_=xdata

			xl, yl = hist2line(xedges, xh)
#			xax.plot(xl, yl,
			if not doimage:
				xax.hist(xdata_, bins=xedges, histtype='stepfilled', 
						facecolor=hcolor, 
						alpha=halpha)
				xax.hist(xdata_, bins=xedges, histtype='step', 
						edgecolor=hcolor)
			else:
				xax.hist(xdata[::nbiny], bins=xedges, histtype='stepfilled', 
						facecolor=hcolor, weights=xh,
						alpha=halpha)
				xax.hist(xdata[::nbiny], bins=xedges, histtype='step', 
						weights=xh,
						edgecolor=hcolor)


			xax.set_xlim(xr)
			xax.set_xscale(xscale)
#			xax.set_xticklabels([])
			plt.setp(xax.get_xticklabels(), visible=False)
			plt.setp(xax.get_xlabel(), visible=False)

			if xh_scale == None:
				if zlog: 
					xax.set_yscale('log')
					xh_scale='log'
			else:
				xax.set_yscale(xh_scale)

#			print('margin',margin)
#			print('xh_height',xh_height)
			xh_yr =  set_range(yl, 
				margin=margin/pow(xh_height,0.3), drawdown=drawdown,
				scale=xh_scale)
			xax.set_ylim(xh_yr)

			despine_axes(xax, despine)

		if yhist:
			nonlocal yh_height, yh_scale
			if yh_height == None: yh_height=0.15
			yax= ax.inset_axes([1.+hgap,0.0,hheight,1] , transform=ax.transAxes, sharey=ax)
			yh = image.sum(axis=0)
			if xslice != None:
				if type(xslice) is not list: 
					p2v=pix2val([0,1], vr=xr, pr=[0,nbinx])
					p2v=p2v[1]-p2v[0]
					xslice=[xslice,xslice+p2v]
				pix_xslice=val2pix(xslice, vr=xr, pr=[0,nbinx])
				if pix_xslice[0] == pix_xslice[1]: pix_xslice[1]=pix_xslice[1]+1
				yh = image[pix_xslice[0]:pix_xslice[1],:].sum(axis=0)
				ax.plot(xslice,[yr[0],yr[0]], marker='D', clip_on=True, color='black')
				ax.plot(xslice,[yr[1],yr[1]], marker='D', clip_on=True, color='black')
				if not doimage:
					ydata_=ydata[xdata >= xslice[0] and xdata <= xslice[1]]
				else:
					ydata_=ydata
			else:
				yh = image.sum(axis=0)
				ydata_=ydata

			xl, yl = hist2line(yedges, yh)
#			yax.plot(xl,yl,
			if not doimage:
				yax.hist(ydata_, bins=yedges, 
						align='mid',
						orientation='horizontal',
						facecolor=hcolor,
						histtype='stepfilled',
						alpha=halpha)
				yax.hist(ydata_, bins=yedges, 
						align='mid',
						orientation='horizontal',
						edgecolor=hcolor,
						histtype='step')
			else:
				yax.hist(ydata[0:nbiny], bins=yedges, 
						weights=yh,
						align='mid',
						orientation='horizontal',
						facecolor=hcolor,
						histtype='stepfilled',
						alpha=halpha)
				yax.hist(ydata[0:nbiny], bins=yedges, 
						weights=yh,
						align='mid',
						orientation='horizontal',
						edgecolor=hcolor,
						histtype='step')

			yax.set_ylim(yr)
			yax.set_yscale(yscale)
			plt.setp(yax.get_yticklabels(), visible=False)
			if yh_scale == None:
				if zlog: 
					yax.set_xscale('log')
					yh_scale='log'
			else:
				yax.set_xscale(yh_scale)

			yh_yr =  set_range(yl, 
				margin=margin/pow(yh_height,0.3), drawdown=drawdown,
				scale=yh_scale)

			yax.set_xlim(yh_yr)
#			xax.axes.xaxis.set_visible(False)
#			xax.plot(xedges[1:], xh)
			despine_axes(yax, despine)

			if type(cbar) is bool:
				if cbar: 
					cbar='lower,left'
					cb_outside=True


		hsize=hheight+hgap
		if xhist: yhsize=0.05*hsize
		else: yhsize=0.0
		if yhist: xhsize=0.05*hsize
		else: xhsize=0.0
		rect=[0,0,1.+xhsize, 1.0+yhsize]

		if type(cbar) is bool:
			if cbar: fig.colorbar(im, pad=0.01)
		elif type(cbar) is list:
			cbar=[float(v) for v in cbar]
			colorbar(cbar, im, ax, fig, 
					orientation=cb_orientation, 
					ticks_position=cb_ticks_position)
		elif type(cbar) is str:
			colorbar_set(cbar, im, ax, fig, 
					off=cb_off, width=cb_width, length=cb_length,
					xlabel=xlabel, ylabel=ylabel, title=title, rect=rect,
					orientation=cb_orientation, outside=cb_outside)

		wrap(plt, xr, yr, xlabel, ylabel, title=title, label=not cb_outside,
				rect=rect,
				xscale=xscale, yscale=yscale, outfile=outfile, ion=ion, display=display)
		return image

	image = show(ion=False)
	if hold: embed()

	return image

