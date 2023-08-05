#
# Jaesub Hong (jhong@cfa.harvard.edu)
# 2020 - 2022
#
# on-the-fly command line tool for any function without wrapper
#	input parameters can be either command line option (-, --)
#	or use commentable json files
#

__version__    = '0.2.8'
CJSON_STARTUP  = 'CJSON_STARTUP'
native         = '_cjson.native_'
# identifier for native cjson functions
# use this value for one of the function parameters

import json
import re
import sys
import math
import glob 
import hashlib      
import textwrap3	# we modify one of its routines below: len

import numpy  as np

from os		import path, makedirs, chdir, getcwd, getenv
from pathlib	import Path
from socket		import gethostname
from collections  import OrderedDict
from datetime     import datetime
from importlib    import import_module
#from IPython	import embed

#----------------------------------------------------------------------------
# test output color setting
class cc_raw: 
	""" color codes
	"""
	orange	 ="\033[38;2;190;165;0m"
	green		 ="\033[38;2;46;145;36m"
	pink		 ="\033[38;2;185;145;175m"
	red		 ="\033[38;2;230;0;0m"
#	steelblue	 ="\033[38;2;176;196;222m"
	steelblue	 ="\033[38;2;156;176;202m"
	darkgrey	 ="\033[38;2;90;90;90m"
	reset		 ="\033[38;2;160;160;160m"
	""" """

class cc_bw: 
	""" color codes
	"""
	key  =''
	type =''
	reset=''
	none =''
	hl   =''
	err  =""
	defs = ""
	""" """

class cc_dark: 
	""" color codes
	"""
	key   = cc_raw.orange
	type  = cc_raw.green
	reset = cc_raw.reset
	none  = cc_raw.darkgrey
	hl    = cc_raw.pink
	err   = cc_raw.red
	defs  = cc_raw.steelblue
	""" """

def colored(r, g, b, text):
	return f"\033[38;2;{r};{g};{b}m{text}\033[38;2;255;255;255m"

def color_scheme(mode):
	if mode == None: mode='dark'
	if mode == 'dark': return cc_dark
	else:			 return cc_bw

#----------------------------------------------------------------------------
# grab time
def timestr2stamp(tstr):

	match=re.search(r'([0-9]+)([^0-9])[0-9]+([^0-9])[0-9]+', tstr)
	if match == None: 
		try:    modtime = Path(tstr).stat().st_mtime
		except: return None
		return modtime

	date = tstr.split(' ')
	if len(date) == 1:
		time=None
		date=date[0]
	elif len(date) >=2:
		time=date[1]
		date=date[0]
	else:
		return None

	match=re.search(r'([0-9]+)([^0-9])[0-9]+([^0-9])[0-9]+', date)
	if match == None: return None

	if len(match.group(1)) <=2: yr='%y'
	else:				    yr='%Y'
	sep1 = match.group(2)
	sep2 = match.group(3)

	dformat=yr+sep1+"%m"+sep2+"%d"
	#print(dformat)
	if time == None:
		return datetime.timestamp(datetime.strptime(date,dformat))

	#print(time)
	match=re.search(r'[0-9]+([^0-9])[0-9]+([^0-9])[0-9]+', time)

	sep3 = match.group(1)
	sep4 = match.group(2)

	tformat="%H"+sep3+"%M"+sep4+"%S"
	#print(tformat)
	return datetime.timestamp(datetime.strptime(tstr,dformat+" "+tformat))

def sizestr2size(sstr):
	try:
		resize=int(sstr)
	except:
		try: resize = Path(sstr).stat().st_size
		except ValueError: resize = -1
	return resize

#----------------------------------------------------------------------------
# dict routines
def replace(inp, rep, pre='{', post='}'):
	""" parameters starting with ^ and . are used to replace variables of the same names
	"""
	text=json.dumps(inp)

	for key in rep:
		if key == '': continue
		
		# to avoid the infinite loop
		if bool(re.search(pre+key+post,rep[key])): continue

		new_text=text
		while True:
			text=new_text
			new_text=text.replace(pre+key+post,rep[key])
			if new_text == text: break
	
	out=json.loads(text, object_pairs_hook=OrderedDict)
	return out, text
	""" """

def copy(inp, verbatim=False, pre='{', post='}'):
	""" copy dictionary to another with loading and variable replacement
	
	"""
	if verbatim:
		text=json.dumps(inp)
		return json.loads(text, object_pairs_hook=OrderedDict)

	rep=OrderedDict()
	for key in inp:
		if type(inp[key]) is not str: continue
		rep[key]=inp[key]
		
	out, text=replace(inp, rep, pre=pre, post=post)
	
	return out
	""" """

def load(file, return_text=False):
	""" read json file, strip comments and do some basic math
	"""
	# not trying to create JSON dialect
	# just add a few features, which may or may not cause issues down the line
	# 	commenting, simple math, trailing ","
	# these features are ony for reading json files, not implemented for writing
	out=OrderedDict()
	try:
		jsonfile=open(file)
		text=jsonfile.read()
		jsonfile.close()
		new=list()

		for line in text.splitlines():

			# remove comments: anything after //
			mat=re.search("^(\s*)//",line)
			if bool(mat): line=''

			mat=re.search("^(.*)//",line)
			if bool(mat): 
#				print(mat.group(1).count('"'))
				if (mat.group(1).count('"') % 2) == 0:
					line=mat.group(1)

			# allow simple math: this is a dangerous slippery slope
			# goes against separation of configuration and program
			# but it's so convenient
			mat=re.search("^(.*:\s*)<([^:,]+)>(.*,.*)$",line)
			if bool(mat): 
				try:
					calc=eval(mat.group(2))
				except SyntaxError:
					print('evaluation of the expression', mat.group(2), 'failed')
					calc='"'+mat.group(2)+'"'
				line=mat.group(1)+str(calc)+mat.group(3)

			new.append(line)
		text='\n'.join(new)

		# add beginning and ending {} if missing
		if not bool(re.match('[\n\s]*[{\[]',text)): 
#			text='{\n'+text+'\n}'
			text='{'+text+'}'

		# now get rid of trailing ","
		# which causes either inconveniency or time loss in run time
		# by dealing with null keys
		text=re.sub(r',([\n\s]*)([}\]])',r'\1\2',text)

		out=json.loads(text, object_pairs_hook=OrderedDict)
	except FileNotFoundError:
		print('file not found:',file)
	except ValueError:
		print('The file',file,'failed parsing')

	if return_text: return text

	return out
	""" """

def find_diff(trg, ref):
	""" find difference of two hashes
	"""
	changes=OrderedDict()
	
	for key in trg:
		if key not in ref: changes[key]=trg[key]
		else:
			if trg[key] != ref[key]:
				changes[key]=trg[key]
	
	gone=ref.keys() - trg.keys()
	
	return copy(changes,verbatim=True), list(gone)
	""" """

def apply_diff(diff, trg, gone=None):
	""" apply hash difference to another hash
	"""
	new=copy(trg, verbatim=True)
	for key in diff: new[key] = diff[key]

	if gone != None: 
		for each in gone: del[each]

	return new
	""" """

# never used?
def inherit_par(cfg, default, keys=None):
	""" set default parameters for config dictionary
	"""
	if keys == None:
		for k in default.keys() - cfg.keys(): cfg[k] = default[k]
	else:
		for k in keys & default.keys(): cfg[k] = default[k]

	return cfg

def copy_par(cfg, pre="{=", post="}", parent=None):
	""" copy both the type and value of a parameter to another
	     "target_variable" : "{#source_variable}"
	"""
	if   pre  == False: return cfg
	elif post == False: return cfg
	elif pre  == ''   : return cfg
	elif post == ''   : return cfg

	if parent == None: parent=cfg

	for k, v in cfg.items():
		if type(v) is dict or type(v) is OrderedDict: 
			cfg[k]=copy_par(v, pre=pre, post=post, parent=parent)
			continue
		if type(v) is not str: continue	# perhaps already done
		mat=re.search("^"+pre+"(.+)"+post+"$",v)
		if bool(mat):
			if mat.group(1) in parent.keys():
				cfg[k] = parent[mat.group(1)]

	return cfg

def nested_key(cfg, key, val=None, sep=':', pop=True):
	""" simple par into a nested variable

	"""
	if val == None: val=cfg[key]

	itype=type(cfg)
	mat=re.search("^(.+)"+sep+"(.+)$",key)
#	print(key)
#	print(mat)
	if not bool(mat): 
		cfg[key] = val
		return cfg

	if key in cfg: 
		if pop: del cfg[key]
	key=mat.group(1)
	rest=mat.group(2)

	if key not in cfg.keys():
		cfg[key] = OrderedDict() if itype is dict else OrderedDict()

	cfg[key] = nested_key(cfg[key],rest,val=val, sep=sep)

	return cfg

def expand_nested(cfg, sep=":", pop=True):
	if   sep == False: return cfg
	elif sep == ''   : return cfg
	elif sep == None : return cfg

	new=copy(cfg)
	for k, v in cfg.items():
		new = nested_key(new, k,sep=sep, pop=pop)
	return new

def expand_list(cfg, pre="\*",	sep=",", pop=True):
	if   pre == False: return cfg
	elif pre == ''   : return cfg
	elif pre == None : return cfg

	new=copy(cfg)
	for k, v in cfg.items():
		if type(v) is dict or type(v) is OrderedDict: 
			new[k]=expand_list(cfg[k], pre=pre, pop=pop)
			continue

		if type(v) is not str: continue

		vals = v.split(sep)
		if len(vals) == 1: continue

		mat=re.search("^([-]*)"+pre+"(.+)$",k)
		if not bool(mat): continue
		newk = mat.group(1)+mat.group(2)
		new[newk] = vals
		if pop: del new[k]

	return new

def to_float(k, v, pre='##'):
	mat=re.search("^([-]*)"+pre+"(.+)$",k)
	if not bool(mat): return k, v

	newk = mat.group(1)+mat.group(2)

	if type(v) is str:
		try:
			return newk, float(v)
		except ValueError:
			print('warning: enforcing floats failed for:',k, v)
			return newk, v
	elif type(v) is list:
		newv = []
		for ev in v:
			if type(ev) is not str: 
				newv.append(ev)
				continue
			try:
				newv.append(float(ev))
			except ValueError:
				print('warning: enforcing floats failed for:',k, ev,'in', v)
				newv.append(ev)
		return newk, newv
	else:
		print('warning: enforcing floats failed for:',k, v)
		return newk, v

def to_numeric(k, v, pre='#'):

	mat=re.search("^([-]*)"+pre+"(.+)$",k)
	if not bool(mat): return k, v

	newk = mat.group(1)+mat.group(2)
	if type(v) is str:
		try:
			return newk, int(v)
		except ValueError:
			try:
				return newk, float(v)
			except ValueError:
				print('warning: enforcing numeric failed for:',k, v)
				return newk, v
	elif type(v) is list:
		newv=[]
		for ev in v:
			if type(ev) is not str: 
				newv.append(ev)
				continue
			try:
				newv.append(int(ev))
			except ValueError:
				try:
					newv.append(float(ev))
				except ValueError:
					print('warning: enforcing numeric failed for:',k, ev,'in', v)
					newv.append(ev)
		return newk, newv
	else:
		print('warning: enforcing numeric failed for:',k, v)
		return newk, v

def enforce_numeric(cfg, 
		pre4n="#",	# prefix for number (integer and floats)
		pre4f='##', # prefix for floats
		pop=True):
	if pre4n == False and pre4n == None or pre4n == '': return cfg

	new=copy(cfg)
	for k, v in cfg.items():
		if type(v) is dict or type(v) is OrderedDict: 
			new[k]=enforce_numeric(cfg[k], pre4n=pre4n, pre4f=pre4f, pop=pop)
			continue

		if pre4f !=None and pre4f != "":
			newk, newv = to_float(k, v, pre=pre4f)
			if k != newk:
				new[newk] = newv
				if pop: del new[k]
				continue

		newk, newv = to_numeric(k, v, pre=pre4n)
		if k == newk: continue
		new[newk] = newv
		if pop: del new[k]
		continue

	return new

def enforce_format(cfg, enforcer=None):

	if enforcer == None: return cfg
	new=copy(cfg)
	for k, v in enforcer.items():
		if k not in cfg.keys(): continue

		if type(v) is dict or type(v) is OrderedDict: 
			new[k]=enforce_format(cfg[k], enforcer[k])
			continue

		if type(cfg[k]) is list:
			try:
				if   v ==     'int': new[k] = [    int(ev) for ev in cfg[k]]
				elif v ==   'float': new[k] = [  float(ev) for ev in cfg[k]]
				elif v ==    'bool': new[k] = [   bool(ev) for ev in cfg[k]]
				elif v == 'complex': new[k] = [complex(ev) for ev in cfg[k]]
				elif v ==     'str': new[k] = [    str(ev) for ev in cfg[k]]
			except ValueError:
				print('enforcing type',v,'failed for', k+ ':', cfg[k] )
				exit()
		else:
			try:
				if   v ==     'int': new[k] =     int(cfg[k])
				elif v ==   'float': new[k] =   float(cfg[k])
				elif v ==    'bool': new[k] =    bool(cfg[k])
				elif v == 'complex': new[k] = complex(cfg[k])
				elif v ==     'str': new[k] =     str(cfg[k])
			except ValueError:
				print('enforcing type',v,'failed for', k+ ':', cfg[k] )
				exit()

	return new

def update_specific(cfg, only):
	new = copy(cfg)
	if only != None:
		for k, v in only.items():
			if k not in cfg.keys(): new[k] = only[k]
			elif type(v) is dict or type(v) is OrderedDict: 
				newv = new[k] if k in new.keys() else OrderedDict()
				for ek in v.keys() - newv.keys(): newv[ek] = v[ek]
				new[k] = newv
	return new

def routine_specific(cfg):

	routine = cfg['-main']

	new = copy(cfg)

	for k, v in cfg.items():
		if not bool(re.search('^--only for ',k)): continue

		levels = routine
		while levels !='':
			if bool(re.search('^--only for '+levels,k)): 
				new=update_specific(new, copy(cfg[k]))
			levels='.'.join(levels.split('.')[:-1])

		del new[k]
	

	return new
	
def delete_or_None(cfg, pre="\.", pop=True):
	if   pre == False: return cfg
	elif pre == ''   : return cfg
	elif pre == None : return cfg

	new=copy(cfg)
	for k, v in cfg.items():
		if type(v) is dict or type(v) is OrderedDict: 
			new[k]=delete_or_None(cfg[k], pre=pre, pop=pop)
			continue

		mat=re.search("^([-]*)"+pre+"(.+)$",k)
		if not bool(mat): continue
		newk = mat.group(1)+mat.group(2)
		if new[k]:
			# if true, yeah, delete the key
			if newk in new: del new[newk] 
		else: 
			# if false, then don't delete, but set None
			new[newk]=None
			
		if pop: del new[k]

	return new

#----------------------------------------------------------------------------
# fix column type from panda table to astropy table
# perhaps a better way to do this, but for now...

def new_ext(filename, new):
	return re.sub('\.[^\.]+$','.'+new, filename)
#----------------------------------------------------------------------------
# obsolete?
def set_par(cfg, par, default):
	""" set default parameters from config dictionary
	"""
	return cfg.get(par, default)

def get_max_str(lst):
	if not lst: return 0
	maxv = len(lst[0])   # list is not empty
	for x in lst:
		cv=len(x)
		if cv > maxv: maxv = len(x)
	return maxv

def simplify(value):
	if   value > 1099511627776:	return "{:.1f}".format(value/1099511627776)+'T'
	elif value > 1073741824:	return "{:.1f}".format(value/1073741824)+'G'
	elif value > 1048576:		return "{:.1f}".format(value/11048576)+'M'
	elif value > 1024:		return "{:.1f}".format(value/1024)+'k'
	else:					return str(value)

def show(dict, ref=None, tab=0, cc=None, full=False, 
		notype=False, hidden='-', exceptions=['-prep','-post']):
	""" show input parameters
	"""

	do=False
	if len(dict) > 0: do=True

	if do:
		keys   = dict.keys()
		types  = [type(each).__name__ for each in dict.values()]
		values = dict.values()
		strval = [str(each) for each in dict.values() 
				if type(each) is not dict and type(each) is not OrderedDict]

		maxkey   = len(max(keys,   key=len))
		maxtype  = len(max(types,  key=len))
		maxvalue = len(max(strval, key=len))
		if maxvalue > 50: maxvalue=50
	else:
		maxtype = 6
		maxvalue = 6

	doref=False
	if ref != None:
		lenref=len(ref)
		if lenref > 0: doref=True

	# nothing to do
	if not do and not doref: return

	if doref:
		reftypes   = [type(each).__name__ for each in ref.values()]
		maxreftype = len(max(reftypes, key=len))
		if not do:
			maxkey= len(max(ref.keys(), key=len))

	tab_ = ''.rjust(tab)
	nextab=tab+maxkey+maxtype+5
	if cc == None: cc=color_scheme('dark')

	if do:
		for key, typ, value in zip(keys, types, values):
			cckey =cc.key
			if key[0:1] == hidden: 
				cckey= cc.defs
				if not full: 
					if key not in exceptions: continue

			key_ = tab_+cckey+key.rjust(maxkey+1)

			if typ == 'NoneType': 
				typ_   = cc.none + typ.ljust(maxtype)
				value_ = cc.none + str(value).ljust(maxvalue)
			else:
				typ_   = cc.type  + typ.ljust(maxtype)
				value_ = cc.reset + str(value).ljust(maxvalue)

			if typ == 'dict' or typ == 'OrderedDict':
				print(key_, typ_, cc.reset)
				cref=None
				if doref:
					if key in ref.keys(): cref=ref[key]
				show(value, tab=nextab, full=full, ref=cref)
				continue

			if doref:
				if key in ref.keys():
					reftype = type(ref[key]).__name__
					if reftype == 'NoneType': 
						reftype = cc.none  + reftype.ljust(maxreftype)
						refval  = cc.none  + str(ref[key])
						feed    = cc.none + '<<'
					else:
						if reftype != typ and typ != 'NoneType':
							reftype = cc.hl   + reftype.ljust(maxreftype)
						else:
							reftype = cc.type + reftype.ljust(maxreftype)
						feed   = cc.reset + '<<'
						refval = cc.reset + str(ref[key])

					if notype: 
						print(key_, value_, feed, refval, cc.reset)
					else:      
						print(key_, typ_, value_, feed, reftype, refval, cc.reset)
			else:
				if notype: print(key_, value_, cc.reset)
				else:      print(key_, typ_,  value_, cc.reset)
	
	if doref:
		typ_   = cc.err + '?'.rjust(maxtype)
		value_ = cc.err + '?'.ljust(maxvalue)
		if do: keys = ref.keys() - dict.keys()  # why does this keep changing the order???
		else:  keys = ref.keys()
		for key in keys:
			key_ = tab_+cc.key+key.rjust(maxkey+1)
			reftype = type(ref[key]).__name__

			if reftype == 'dict' or reftype == 'OrderedDict':
				print(key, reftype, cc.reset)
				cref=None
				show(OrderedDict(), tab=nextab, full=full, ref=ref[key])
				continue

			if reftype == 'NoneType': 
				reftype = cc.none  + reftype.ljust(maxreftype)
				refval  = cc.none  + str(ref[key])
				feed    = cc.none + '<<'
			else:
				reftype = cc.hl   + reftype.ljust(maxreftype)
				feed   = cc.reset + '<<'
				refval = cc.reset + str(ref[key])
			if notype: 
				print(key_, value_, feed, refval, cc.reset)
			else:      
				print(key_, typ_, value_, feed, reftype, refval, cc.reset)


	""" """

def show_feed(args, kwargs, name, inargs=[], inkwargs=OrderedDict(), cc=None):

	if cc == None: cc=color_scheme('dark')

	print(' main:',cc.key+name+cc.reset)
	ninargs=len(inargs)
	ninkwargs=len(inkwargs)

	if len(args) >0:
		maxargs = len(max(args, key=len))

	if ninargs > 0:
		types   = [type(each).__name__ for each in inargs]
		maxtype = len(max(types, key=len))

	for i, each in enumerate(args):
		arg_ = cc.hl +each.rjust(maxargs+1)

		if i >= ninargs: 
			print(arg_,cc.reset)
			continue
		if types[i] == 'NoneType': 
			feed  = cc.none+'<<'
			type_ = cc.none+types[i].ljust(maxtype)
			inarg_= cc.none+str(inargs[i])
		else:
			feed  = cc.reset+'<<'
			type_ = cc.type+types[i].ljust(maxtype)
			inarg_= cc.reset+str(inargs[i])

		print(arg_+cc.reset,feed, type_, inarg_, cc.reset)
	
	show(kwargs, ref=inkwargs, cc=cc)

def show_diff(trg, ref, cc=None):
	""" show the difference of two hashes or dictionaries
	"""
	changes, gone =find_diff(trg, ref)

	if cc == None: cc=color_scheme('dark')
	show(changes)
	if gone != None:
		print(cc.key,gone,cc.reset)

	""" """

def show_files(fcheck, basedir=None, ofilekeys=[], cc=None, keymap=None):
	""" show files
	"""
	# color scheme
	if cc == None: cc=color_scheme('dark')
	if keymap == None: keymap={}

	maxlen=get_max_str([k for k in fcheck.keys()])+1
	if basedir != None:
		print('basedir'.rjust(maxlen)+':',basedir)
	for key, val in fcheck.items():
		if type(val) is not OrderedDict: continue
		name	 = val['name']
		absent = val['absent']
		if key[0:1] == '-': key_=keymap.get(key,key)
		else:               key_=key
		if absent:
			print(key_.rjust(maxlen)+':'.ljust(7)+cc.err+'missing'.ljust(19), name+cc.reset)
		else:
			modtime = val['modtime']
			size	  = val['size']
			color   = cc.reset
			if key == fcheck['--outfile']:
#				print(fcheck['-updated'])
				if not fcheck['-updated']: color=cc.err
				else: color=cc.key
			if type(ofilekeys).__name__ != 'NoneType':
				if key in ofilekeys: color=cc.key
			print(color+key_.rjust(maxlen)+':', \
					str(datetime.fromtimestamp(modtime))[2:19:],cc.reset+simplify(size).rjust(6),name)
	""" """

def inoutpar(par, sep='<<'):
	pars = par.split(sep)
	if len(pars) == 1: return par, par
	# inside )  outside of def
	return pars[0].strip(), pars[1].strip()

def stripkey(src, sep='<<'):
	for key in [k for k in src.keys()]:
		if sep in key: src[key.replace(' ','')] = src.pop(key)
	return src

#----------------------------------------------------------------------------
# plotting routines
def set_axes_color(axes, fcolor='black', bcolor='white'):
	for ax in axes:
		ax.set_facecolor(bcolor)
		ax.yaxis.label.set_color(fcolor)
		ax.xaxis.label.set_color(fcolor)
		ax.spines['bottom'].set_color(fcolor)
		ax.spines['top'].set_color(fcolor)
		ax.spines['left'].set_color(fcolor)
		ax.spines['right'].set_color(fcolor)
		ax.tick_params(axis='x', colors=fcolor, which='both')
		ax.tick_params(axis='y', colors=fcolor, which='both')

def minmax(data, nonzero=False):
	if nonzero: return [np.min(data[np.nonzero(data)]), np.max(data)]
	else:       return [np.min(data), np.max(data)]

def set_plot_range(rng_, scale='linear', extend=None, drawdown=None):
	rng=rng_
	if scale == 'linear':
		diff=rng[1]-rng[0]
		if extend == None:
			rng=[rng[0]-0.2*diff,rng[1]+0.2*diff]
		elif np.isscalar(extend):
			rng=[rng[0]-extend*diff,rng[1]+extend*diff]
		else:
			rng=[rng[0]-extend[0]*diff,rng[1]+extend[1]*diff]
	else:
		if extend == None:
			rng=[rng[0]*0.5, rng[1]*2]
		elif np.isscalar(extend):
			rng=[rng[0]/extend, rng[1]*extend]
		else:
			rng=[rng[0]*extend, rng[1]*extend]
		if rng[0] < 0.0:
			if drawdown == None:
				drawdown = 1.e-5
				rng[0]=rng_[1]*drawdown
	return rng

def bigger_range(xr, yr):
	return [xr[0] < yr[0] and xr[0] or yr[0], 
		  xr[1] > yr[1] and xr[1] or yr[1]] 

#-------------------------------------------------------------------
# semi-regex handling in the parameters regarding file names
def find_tag(expression, inp, tagid='', pre='{', post='}'):
	""" get tags from a parameter
	"""
	if expression == None: return ''

	# this means inp can be drived from expression itself by removing '(' and ')'
	if inp == None:
		inp=expression.replace('(','')
		inp=inp.replace(')','')
		return_inp=True
	else:
		return_inp=False

	subexpr=re.findall(expression,inp)
	if type(subexpr[0]) is tuple: subexpr = [item for t in subexpr for item in t] 

	tag=OrderedDict()

	for idx, expr in enumerate(subexpr):
		tag[pre+tagid+str(idx+1)+post]=expr
	
	if return_inp:  return tag, inp
	else: 	    return tag
	""" """

def apply_tag(inp, tags):
	""" apply tags to a parameter
	"""
	if tags == None: return inp

	out=inp
	for key in tags: out=out.replace(key,tags[key])

	return out
	""" """

def combine_tags(keys, tags, ids=None, cfg=None):
	""" get more tags from other files used in the program
	"""

	if cfg  == None: cfg=OrderedDict()
	if ids  == None: ids=[key+':' for key in keys]

	if tags == None: tags=OrderedDict()
	combined=copy(tags,verbatim=True)

	values=[]
	for ckey, cid in zip(keys, ids):
#		expre		= self.apply_tag(cfg[ckey],tags)
#		tag, value  = self.find_tag(expre, None, tagid=cid)
		expre		= apply_tag(cfg[ckey],tags)
		tag, value  = find_tag(expre, None, tagid=cid)
		values.append(value)
		for key_, tag_ in tag.items(): combined[key_]=tag_
	
	return combined, values
	""" """

#-------------------------------------------------------------------
def regex2searchable(regex, wild='*'):
	""" convert regular expression to file searchable expression
	"""
	if not bool(re.search('\(',regex)): return regex

	spexpr=regex.split('(')

	newexpr=[]
	for seg in spexpr:
		if not bool(re.search('\)', seg)): 
			newexpr.append(seg)
			continue

		newexpr.append(re.sub(r'(.*\))','*',seg))

#		print(''.join(newexpr))
	return ''.join(newexpr)
	""" """

def mixed2regexsrchable(mixed, wild='*', single='?'):
	""" convert mixed expression to file searchable and regex expression
	"""
	if not bool(re.search('\(',mixed)): 
		regex=mixed
		regex=regex.replace('.','\.')
		regex=regex.replace(wild,'.*')
		regex=regex.replace(single,'.')
		return mixed, regex

	spexpr=mixed.split('(')

	srchable=[]
	regex=[]

	for seg in spexpr:
		if not bool(re.search('\)', seg)): 
			reg = seg
			reg = seg.replace('.','\.')
			reg = reg.replace(wild,'.*')
			reg = reg.replace(single,'.')
			regex.append(reg)
			srchable.append(seg)
			continue

		srchable.append(re.sub(r'.*\)','*',seg))

		mat = re.match(r'(.*\))(.*)',seg)
		reg = mat.group(2)
		reg = reg.replace('.','\.')
		reg = reg.replace(wild,'.*')
		reg = reg.replace(single,'.')
		regex.append(mat.group(1)+reg)


	srchable=''.join(srchable)
	srchable=srchable.replace('**','*')
	regex='('.join(regex)
	return srchable, regex
	""" """

def match(key, inp, cfg=None):
	""" case match for a given parameter, and reset other parameters accordingly
	"""
	bingo=False
	request=False

	if cfg==None: return bingo, OrderedDict()
	update=copy(cfg) 

	for par, val in cfg.items():
		if not bool(re.search('=',par)): continue
		request=True

		if not bool(re.search('^'+key,par)): continue

		fields = par.split('=')

		if bool(re.search('~=',par)) and not bool(re.search(fields[1],inp)): continue
		if bool(re.search('==',par)) and fields[2] != inp: 		         continue
		if bool(re.search('!=',par)) and bool(re.search(fields[1],inp)):     continue

		bingo=True

		for spar, sval in val.items():
			if not bool(re.search('=',spar)):
				update[spar]=sval

			else:
				for spar_, sval_ in sval.items():
					if spar not in update: update[spar]=OrderedDict()
					update[spar][spar_]=sval_

	# if there is no match request, then bingo should be 1
	bingo = bingo == request

	match_only = cfg.get('-match_only', False)
	bingo      = bingo or not match_only

	return bingo, update
	""" """

#----------------------------------------------------------------------------
# filtering file selections
def pick(infile, indir=None, include=None, exclude=None, verbose=0):
	""" see if the given filename meets the requirement as an input file
	"""
	# set by "from" and/or "except" options
	if infile == "": return False

	pick=True
#	if 'from'   in cfg.keys(): pick = pick and     bool(re.search(cfg['from'], infile))
#	if 'except' in cfg.keys(): pick = pick and not bool(re.search(cfg['except'],infile))
	if include != None: pick = pick and     bool(re.search(include, infile))
	if exclude != None: pick = pick and not bool(re.search(exclude, infile))

	if not pick:
		if verbose >= 3: print('not picking',infile)
		return False

	if indir != None: infile_=Path(indir) / Path(infile)
	else:             infile_=infile

	if not path.isfile(infile_):
		if verbose >= 2: print(infile, 'does not exist.')
		return False

	return pick
	""" """

def skip_by_outfile(outfile, basedir=None, \
		fcheck=None, \
#		ftcheck=None, fscheck=None, \  # this should be used for separately
		updateonly=False, \
		after=None, before=None, \
		larger=None, smaller=None, \
		dryrun=False, clobber=False, keep=None, drop=None, 
		verbose=0):
	""" see if the given filename meets the requirement as an output file
	    depending on if the file alreay exists or when it was last modified.
	    technically this can be used for any files (e.g., input file)
	"""	
	# set by "include" and/or "exclude" options

	if outfile == None:
		if fcheck == None:
			if verbose >= 2: print('no filename is given')
			return False  # nothing to test against
		else:
			outfile = fcheck['name']

	skip=False
	#if 'include' in cfg.keys(): skip=    not bool(re.search(cfg['include'], outfile))
	#if 'exclude' in cfg.keys(): skip=skip or bool(re.search(cfg['exclude'], outfile))
	if keep != None: skip=    not bool(re.search(keep, outfile))
	if drop != None: skip=skip or bool(re.search(drop, outfile))

	if dryrun:
		if verbose >= 2: print('a dryrun requested')
		skip=True 

	# with fcheck, these tests are already done
	if fcheck != None:
		exist = not fcheck['absent']
	else:
		if basedir != None:
			outfile_ = str(Path(basedir) / Path(outfile))
		else:
			outfile_ = outfile
		exist = path.isfile(outfile_)

		if exist:
			fcheck=OrderedDict()
			fcheck['absent' ] = not exist
			fcheck['modtime'] = Path(outfile_).stat().st_mtime
			fcheck['size'   ] = Path(outfile_).stat().st_size

	# now time and size cut
	if exist:
#		if ftcheck == None: fmodtime = fcheck ['modtime']
#		else:               fmodtime = ftcheck['modtime']
#		if fscheck == None: fsize    = fcheck ['size']
#		else:               fsize    = fscheck['size']

		fmodtime = fcheck ['modtime']
		fsize    = fcheck ['size']
#		print(fmodtime, ftcheck)	

		if after  != None: 
			if fmodtime > after : exist = False
		if before != None: 
			if fmodtime < before: exist = False

		if larger != None: 
			if fsize > int(larger) : exist = False
		if smaller!= None: 
			if fsize < int(smaller): exist = False

		# updated?
		if updateonly == True:
			if '-updated' in fcheck:
				if not fcheck['-updated']:
					exist = False

	if not clobber and not skip and exist:
#		if verbose >= 2: print('file exists for', outfile)
		skip=True

	return skip
	""" """

def skip_by_file_modtime(modtime, after=None, before=None, verbose=0):
	""" 
	"""	
	if modtime == None: return False
	if after == None and before == None:
		return False
	else:
		if after != None:
			if modtime > after: return False
		if before != None:
			if modtime < before: return False

	return True
	""" """

def skip_by_file_size(size, larger=None, smaller=None, verbose=0):
	""" 
	"""	
	if size == None: return False
	if larger == None and smaller == None:
		return False
	else:
		if larger != None:
			if size > larger: return False
		if smaller != None:
			if size < smaller: return False

	return True
	""" """

#----------------------------------------------------------------------------
# iteration loop settings
def search_infile(expre, tagid='', indir=None, \
		include=None, exclude=None, \
		recursive_search=True, infile_order='sort', \
		cfg=OrderedDict(), verbose=0):
	""" make file list from wild card input file parameters
	"""
	if type(expre) is not str: return None

	c_dir=getcwd()
	if indir != None: chdir(indir)
	
	# convert regex to searchable expression
	# e.g.,  dummy_([0-9]+).fits => dummy_*.fits
	if type(expre) is not list: expre=[expre]
	
	searchable  =[]
	regex		=[]
	dirs		=[]
	isregex	=[]
	counts	=[]
	for each_ in expre:
		
		mat=re.search('^(.*)#([0-9]+)$',each_)
		if bool(mat):
			each=mat.group(1)
			count=int(mat.group(2))
		else:
			count=searchable.count(each_)
			each=each_

		dir =path.dirname(each)
		file=path.basename(each)
		if dir == '.': dir='' 
		if dir != '' : dir=dir+'/'
	
		dir_,  rdir_ =mixed2regexsrchable(dir)
		file_, rfile_=mixed2regexsrchable(file)

		dirs.append(dir_)
		searchable.append(file_)
		regex.append(rdir_+rfile_)
	
		isregex.append(file != file_)
		counts.append(count)
		
#			print(dir, file_, file != file_)
	
	files =[]
	tags	=[]
	uids	=[]
	names	=[]

	maxc=max(counts)+1
	digit=math.ceil(math.log10(maxc))

	for ori, each, indir_, isrex, count in zip(regex, searchable, dirs, isregex, counts):
		if each == '': continue
	
#		print(indir,':',indir_,':', each)
		# now search
		if indir != None:
			# not sure how to make this one line
#			print(recursive_search, each)
			if recursive_search:
				files_=glob.glob('**/'+each, recursive=recursive_search)
#				files_=glob.glob(each, recursive=recursive_search)
			else:
				files_=glob.glob(each)
		else:
			files_=glob.glob(indir_+each, recursive=recursive_search)
#			print(files_)
	
		if len(files_) == 0: continue
	
		# check if the found match with the original regular expression
		if isrex: 
			survived=[]
			tag=[]
			for found in files_:
				if not re.search(ori, found): continue
				survived.append(found)
				tag.append(find_tag(ori, found, tagid=tagid))
		else:
			survived=files_
			tag=[OrderedDict()]*len(files_)
	
		if len(survived) == 0: continue
	
		# collect any that survives
		for each in survived: 
			names.append(each)
			uids.append(count)
			if count >0: files.append(each+'#'+str(count).zfill(digit))
			else: files.append(each)
		for each in tag: tags.append(each)

	chdir(c_dir)
	
	if len(files) == 0: return None
	
	# now sorting
	files_ = files
	tags_	 = tags
	names_ = names
	uids_  = uids

	# perhaps this is obsolete since now with filecheck ....
	if infile_order != 'unsort':
		zipped = zip(files, tags, names, uids)
		sorted_= sorted(zipped, reverse= infile_order == 'reverse')
		tuples = zip(*sorted_)
		files_, tags_, names_, uids_ = [ list(tuple) for tuple in tuples]

	# filter
	files   = OrderedDict()

	for file_, tag_, name_, uid_ in zip(files_, tags_, names_, uids_):
		if pick(file_, indir=indir, include=include, exclude=exclude, verbose=verbose):
			files[file_] = OrderedDict()
			files[file_]['tag']  = tag_
			files[file_]['name'] = name_
			files[file_]['uid']  = uid_
	
	return files
	""" """

def get_outfile(outfile, infile, outdir=None, outsubdir=None, \
		mirror_indir=True, tags=None, switch_subdir=None, \
		cfg=None, verbose=0):
	""" get output file name based on input filename and other options
	"""

	if outfile == None: return None, None

	if cfg     == None: cfg=OrderedDict()
	if outdir  == None: mirror_indir = False 
	
	insubdir = path.dirname(infile)
	if outsubdir == None:
		outsubdir= insubdir
		if outsubdir != '': outsubdir=outsubdir+'/'
	
	if switch_subdir == True:
		for src, trg in switch_subdir.items():
			outsubdir=outsubdir.replace(src, trg)
	
	if tags != None: 
		outsubdir = apply_tag(outsubdir,tags)
		outfile   = apply_tag(outfile,tags)

	if mirror_indir:
		outdir  = Path(outdir) / Path(outsubdir)  
		outfile = Path(outdir) / Path(outfile)
	else:
		# usually in this case, this function is not likely needed
		if outdir == None: 
			outdir  = Path(path.dirname(outfile)) 
#			outfile = Path(outdir) / Path(path.basename(outfile))
		else:
			outfile = Path(outdir) / Path(outfile)

	return outfile, outdir
	""" """

def set_file_pars(default=OrderedDict(), \
		name="", tag=None, \
		tkeys=None, tagids=None, akeys=None, \
		fkeys=None, ifkeys=None, ofkeys=None, \
		absent=None, \
		fcheck=None, \
		cfg=None, mcfg=None, verbose=0):
	""" set both input and output filenames and other associated parameters
	"""
	
	# potentially the same for set_tasks -----------------------------------
	# grab more tags
	# this is always tied to a file for now
	if tkeys != None:
		tag, values= combine_tags(tkeys, tag, ids=tagids, cfg=mcfg)
		for tkey, value in zip(tkeys, values): mcfg[tkey]=value
		infiles[infile]['tag']=tag

	# apply all the tags if requested
	if akeys != None:
		for key in akeys: mcfg[key]=apply_tag(mcfg[key], tag)

	# apply all the tags and these are files
	if fkeys != None:
		for key in fkeys: mcfg[key]=apply_tag(mcfg[key], tag)
	if ifkeys != None:
		for key in ifkeys: mcfg[key]=apply_tag(mcfg[key], tag)
	if ofkeys != None:
		for key in ofkeys: mcfg[key]=apply_tag(mcfg[key], tag)

	# update the outfile info
	if '-outfile' in cfg:
		outfile=cfg.get('-outfile',None)
		outfile, outdir =get_outfile(outfile, name, \
						outdir	  = cfg.get('-outdir',	  None), \
						outsubdir	  = cfg.get('-outsubdir', None), \
						mirror_indir  = cfg.get('-mirror',	  True), \
						switch_subdir = cfg.get('-swapsub',	  False), \
						tags=tag, cfg=mcfg, verbose=verbose)
		mcfg['-outfile']=Path(outfile)
	
	if '-indir' in mcfg:
		mcfg['-infile' ] = Path(mcfg['-indir']) / Path(name)
	else:
		mcfg['-infile' ] = name

	# update files in a directory relative to input dir
	if ifkeys != None:
		fulldir = path.dirname(mcfg['-infile'])
		for key in ifkeys: mcfg[key]=Path(fulldir) / Path(mcfg[key])

	# update files in a directory relative to output dir
	if ofkeys != None:
		if '-outfile' in cfg:
			fulldir = path.dirname(mcfg['-outfile'])
			for key in ofkeys: mcfg[key]=Path(fulldir) / Path(mcfg[key])

	# file check 
	# review the status of these files
	if fcheck != None:
		fcres=OrderedDict()
		for key in fcheck:
			fcres[key] = OrderedDict()
			fcres[key]['absent'] = False
			fcres[key]['name']   = str(mcfg[key])
			if '-basedir' in mcfg:
				try: fcres[key]['name'] = str(Path(mcfg[key]).relative_to(mcfg['-basedir']))
				except: pass
			if not path.isfile(mcfg[key]): 
				fcres[key]['absent'] = True
				continue
			fcres[key]['modtime'] = Path(mcfg[key]).stat().st_mtime
			fcres[key]['size']    = Path(mcfg[key]).stat().st_size
			if '-latest' not in fcres:
				fcres['-latest'] = key
			else:
				if fcres[key]['modtime'] >= fcres[fcres['-latest']]['modtime']:
					fcres['-latest'] = key
		fcres['-updated'] = False
		if '-latest' in fcres:
			if   fcres['-latest'] == '-outfile':        fcres['-updated'] = True
			elif fcres['-latest'] in cfg.get('-ofilekeys',[]): fcres['-updated'] = True
#			print(fcres['-latest'],cfg.get('-ofilekeys',[]), fcres['-updated'])
		fcres['--outfile'] = '-outfile'
				
#		infiles[infile]['-fcheck'] = fcres

	# how to handle if the file does not exist fexist
	if absent != None:
		for key, val in absent.items():
			if not path.isfile(str(mcfg[key])): 
#						mcfg[key] = val +':'+str(mcfg[key])
				if '-missing' not in mcfg: mcfg['-missing']=[]
				mcfg['-missing'].append(key+' not found: '+str(mcfg[key]))
				mcfg[key] = val #+':'+str(mcfg[key])

	# rename file path relative to basedir if possible
	if '-basedir' in mcfg:
		try: mcfg['-infile'] = mcfg['-infile' ].relative_to(mcfg['-basedir'])
		except: pass
		if '-outfile' in mcfg:
			try: mcfg['-outfile'] = mcfg['-outfile'].relative_to(mcfg['-basedir'])
			except: pass
		# repeat for fkeys
		# 4 dir options for each of fkeys
		#	full indir, full out dir, some reference dir, none
		#	_indir_(*default), _outdir_, regular string, none
		# file names of fkeys, ofkeys, ifkeys can get simplified by basedir
		if fkeys != None:
			for key in fkeys: 
				try: mcfg[key] = mcfg[key].relative_to(mcfg['-basedir'])
				except: pass
		if ifkeys != None:
			for key in ifkeys: 
				try: mcfg[key] = mcfg[key].relative_to(mcfg['-basedir'])
				except: pass
		if ofkeys != None:
			for key in ofkeys: 
				try: mcfg[key] = mcfg[key].relative_to(mcfg['-basedir'])
				except: pass

	# update mcfg with proper string of filenames
	mcfg['-infile']  = str(mcfg['-infile'])
	if '-outfile' in cfg:
		mcfg['-outfile'] = str(mcfg['-outfile'])
	if ifkeys != None:
		for key in ifkeys: mcfg[key] = str(mcfg[key])
	if ofkeys != None:
		for key in ofkeys: mcfg[key] = str(mcfg[key])
		#  -----------------------------------

	return copy(mcfg, pre='{>', post='}'), fcres

	""" """

def set_files(default=OrderedDict(), \
		tkeys=None, tagids=None, akeys=None, \
		fkeys=None, ifkeys=None, ofkeys=None, \
		absent=None, fcheck=None, \
		cfg=None, verbose=0):
	""" set both input and output filenames and other associated parameters
	"""
	# if everything works, this is the only routine to be called
	
	# mkeys: keys for matching: by default, infile
	#	if _match_only is true, non-matching cases can be excluded
	#	based on 'go' parameter
	#	
	# tkeys: keys for finding tags: by default, infile
	#
	# tagids: IDs for tags coming from other than infile
	#	e.g., infile tags are {1}, {2}, {3}, ....
	#		to separate other tags, one can assign something like {r:1}, {r:2}, ...
	#		then the ID should be 'r:'.
	#		if not given, by defaults, it grabs the first letter of each of tkeys
	#		so there will be collisions if more than one of tkeys start with the same letter
	#		name the parameters so that they can avoid collision
	#		or specify the IDs explicitly
	# akeys: keys for applying tags: by defaults, outfile

	infiles = search_infile(cfg['-infile'],				\
			indir			= cfg.get('-indir',	   None),	\
			include		= cfg.get('-include',	   None),	\
			exclude		= cfg.get('-exclude',	   None),	\
			recursive_search	= cfg.get('-recursive',	   True),	\
			infile_order	= cfg.get('-infile_order', 'sort'),	\
			verbose		= verbose)

	if infiles == None: return None

	match_key = '-infile'
	if '-infile' in cfg.get('-keymap',{}): match_key=cfg['-keymap']['-infile']
#	print(match_key,'======')
	
#	from IPython import embed; embed()
	for infile in infiles:
	
		skip_job=False

		name = infiles[infile].get('name', None)
		if name == None: continue

		tag  = infiles[infile].get('tag', None)
		uid  = infiles[infile].get('uid', None)

		
		bingo, matched= match(match_key, infile, cfg=cfg)
		if not bingo: continue

		mcfg = copy(default)
		for each in matched: mcfg[each] = matched[each]

		# what might be updated
		for each in [tkeys, akeys]:
			if each == None: continue
			for k in each & cfg.keys(): mcfg[k] = cfg[k]
	
		infiles[infile]['-mcfg'], infiles[infile]['-fcheck'] =set_file_pars(default=default, \
								name=name, tag=tag, \
								tkeys=tkeys, tagids=tagids, akeys=akeys, \
								fkeys=fkeys, ifkeys=ifkeys, ofkeys=ofkeys, \
								absent=absent, \
								fcheck=fcheck, \
								cfg=cfg, mcfg=mcfg, verbose=verbose)

		### better way to collect updates
	if len(infiles) == 0: infiles=None
	
	return infiles
	""" """

def set_tasks(default=OrderedDict(), \
		tkeys=None, tagids=None, akeys=None, \
		fkeys=None, ifkeys=None, ofkeys=None, \
		absent=None, fcheck=None, \
		cfg=None, verbose=0):
	tasks = OrderedDict()

	match_key = '-iter'
	if '-iter' in cfg.get('-keymap',{}): match_key=cfg['-keymap']['-iter']

	for task in cfg['-iter']:
		# this is used only for '-iter'
		# which needs to be more generalized including 'infile'
		# for infile, set _iter to be the list of parsed infiles
		# and allow other variables to change accordingly
#		bingo, matched = match('-iter', task, cfg=cfg)
		bingo, matched = match(match_key, task, cfg=cfg)
		if task not in cfg: 
			mcfg=copy(default)
			if bingo: 
				for k in mcfg.keys() & matched.keys(): mcfg[k] = matched[k]
		else:
			mcfg=copy(cfg[task])
			if bingo: 
				for k in (default.keys() - mcfg.keys()) & matched.keys(): mcfg[k]=matched[k]
			else:
				for k in default.keys() - mcfg.keys(): mcfg[k]=default[k]

		tasks[task] = OrderedDict()
		tasks[task]['-mcfg'], tasks[task]['-fcheck'] =set_file_pars(default=default, \
								name=mcfg.get('-infile',""), tag=OrderedDict(), \
								tkeys=tkeys, tagids=tagids, akeys=akeys, \
								fkeys=fkeys, ifkeys=ifkeys, ofkeys=ofkeys, \
								absent=absent, \
								fcheck=fcheck, \
								cfg=cfg, mcfg=mcfg, verbose=verbose)
	
	return tasks

#----------------------------------------------------------------------------
# key map setting
def defaults(cfg):
	""" set default values for some of the parameters
	"""
	# any regular paramater should be rename-able

	cfg['-runprep' ] =     cfg.get('-runprep', True)
	cfg['-verbose' ] = int(cfg.get('-verbose', 1))
	cfg['-dryrun'  ] =     cfg.get('-dryrun',	 False)
	cfg['-clobber' ] =     cfg.get('-clobber', False)
	cfg['-sort'    ] =     cfg.get('-sort',	 None)
#	cfg['-help'    ] =     cfg.get('-help',	 False)
#	cfg['-Help'    ] =     cfg.get('-Help',	 False)

	# if explicitly requested "no sorting"
	if cfg['-sort'] == "None": cfg["-sort"]= None

	# when sorting is not requested but modtime or size cut is requested, then sort
	if cfg['-sort'] == None:
		if '-larger'  in cfg: cfg['-sort'] = 'size'
		if '-smaller' in cfg: cfg['-sort'] = '~size'
		if '-after'   in cfg: cfg['-sort'] = 'modtime'
		if '-before'  in cfg: cfg['-sort'] = '~modtime'

	if '-basedir' not in cfg:
		if '-indir' in cfg: 
			if '-outdir' not in cfg:
				cfg['-basedir'] = cfg['-indir']
			else: 
				try:
					simple_dir = str(Path(cfg['-outdir']).relative_to(cfg['-indir']))
					cfg['-basedir'] = cfg['-indir']
				except:
					pass
#				except ValueError:


	return cfg
	""" """

# handle input parameters
def get_func_parameters(func):
	""" check func input parameters and keyword
	    and update them with the given cfg dictionary
	""" 

	if hasattr(func,'__code__'):
		keys = func.__code__.co_varnames[:func.__code__.co_argcount][::-1]
	else: 
		return [], {}
	sorter = {j: i for i, j in enumerate(keys[::-1])} 
	if func.__defaults__ != None:
		values = func.__defaults__[::-1]
		kwargs = {i: j for i, j in zip(keys, values)}
		sorted_args = tuple(
			sorted([i for i in keys if i not in kwargs], key=sorter.get)
		)
		sorted_kwargs = {
			i: kwargs[i] for i in sorted(kwargs.keys(), key=sorter.get)
		}   
	else:
		sorted_args = keys[::-1]
		sorted_kwargs = OrderedDict()

	return sorted_args, sorted_kwargs

def set_func_parameters(sorted_args, sorted_kwargs, cfg=None):
	""" check func input parameters and keyword
	    and update them with the given cfg dictionary
	""" 
	updated_args=[]
	for par in sorted_args:
		if par in cfg: updated_args.append(cfg[par])
		else:		   updated_args.append(None)

	if sorted_kwargs != None:
		updated_kwargs=OrderedDict()
		for par in sorted_kwargs:
			if par in cfg: updated_kwargs[par]=cfg[par]
			else:		   updated_kwargs[par]=sorted_kwargs[par]

	# if you meet this, the function doesn't tell us what it needs
	# e.g., math.sin
	if updated_args == []:
		for par in cfg.get('-pars',[]):
			if par in cfg:
				updated_args.append(cfg[par])
	for par in cfg.get('-kwpars',[]):
		if par in cfg:
			updated_kwargs[par] = cfg[par]
		else:
			updated_kwargs[par] = None
	
	# only when -pars are set
	if cfg.get('-collect_kwpars',False):
		for par in cfg:
			if par in cfg.get('-exclude_kwpars',[]):      continue
			if par[0:1] == '-':		 continue
			if par in cfg.get('-pars',[]): continue
			if par not in updated_kwargs.keys():
				updated_kwargs[par] = cfg[par]

	return updated_args, updated_kwargs

def set_module_parameters(module, cfg, keys=None):
	""" set module global parameters
	""" 
	if cfg == None: return
	if keys == None:
		for key in cfg:			setattr(module, key, cfg[key])
	else:
		for key in keys & cfg.keys(): setattr(module, key, cfg[key])

def get_parameters(pars=sys.argv[1:]):
	""" from command strings, set and return parameters as a dict (cfg)
	"""
	cfg=OrderedDict()

	if type(pars) is not list: pars=[pars]

	# interactive
	if len(sys.argv) ==1: cfg['exit']=False

	cfg_fly=OrderedDict()

	# handle regular (-xxx format) parameter
	jsonpar=[]
	potential=False

#	print(pars)
	for par in pars:
#		print(par,'<<<<')
		mat=re.search("^-(.+)",par)
		if bool(mat):
			key=mat.group(1)
			matneg=re.search("^\^(.+)",key)
			if bool(matneg):
				key=matneg.group(1)
				cfg_fly[key] = False
			else:
				matneg2=re.search("^-\^(.+)",key)
				if bool(matneg2): 
					key='-'+matneg2.group(1)
					cfg_fly[key] = False
				else:
					cfg_fly[key] = True
					potential=True
		else:
			if potential:
				cfg_fly[key]=par
				potential=False
			else:
				jsonpar.append(par)

	# handle json file or json format parameter
	jsonfiles=[]
	for par in jsonpar:
		mat=re.search("^{(.+)",par)
		if bool(mat):
			cfg_=json.loads(par, object_pairs_hook=OrderedDict)
		else:
			if '--raw' in pars:
				print(load(par, return_text=True))
				exit()
			else:
				cfg_=load(par)
				jsonfiles.append(par)
#				jfile_found = True

		for key in cfg_: cfg[key]=cfg_[key]

#	now = datetime.now()
#	cfg_['_date']=now.strftime("%y%m%d_%H%M%S")
	if '--raw' in pars:
#		print(json.dumps(cfg, indent="\t"))
		print(" ".join(pars))
		exit()

	for key in cfg_fly: cfg[key]=cfg_fly[key]

	if '-python' in cfg.keys():
		for key in cfg['-python']: cfg[key] = cfg['-python'][key]

	if jsonfiles != []: cfg['-jsonfiles'] = jsonfiles

	cfg=copy(cfg)


	# load default parameters
	if '-load' in cfg.keys():
		if type(cfg['-load']) is str: cfg['-load']=cfg['-load'].split(':')
		# note: this should be reversed in order 
		for each in cfg['-load'][::-1]:
			each = path.expanduser(each)
			if not path.isfile(each): 
				print('file not found for _load:',each)
				continue
			cfg_=copy(load(each))
			for key in cfg_.keys() - cfg.keys(): cfg[key]=cfg_[key]

	startup = getenv(CJSON_STARTUP) 
	if startup != None:
		startup=startup.split(':')
		# note: this should be reversed in order 
		for each in startup[::-1]:
			each = path.expanduser(each)
			if not path.isfile(each): 
				print('file not found for', CJSON_STARTUP+':',each)
				continue
			cfg_=copy(load(each))
			for key in cfg_.keys() - cfg.keys(): cfg[key]=cfg_[key]

	if "-main" not in cfg: return cfg

	# this was done in execute: this is the right place
	cfg=defaults(cfg) 

	# expand a string value to a list, useful for cmdline or json file
	cfg = expand_list(cfg, 
			pre=cfg.get('-list_pre','\*'),
			sep=cfg.get('-list_sep',','),
			pop=cfg.get('-pop_expand_list',True))

	# enforce numeric parameter from cmdline or json file
	cfg=enforce_numeric(cfg, 
			pre4n=cfg.get('-enforce_numeric','#'),
			pre4f=cfg.get('-enforce_floats','##'),
			pop  =cfg.get('-pop_enforce_numeric',True))

	# expand a key to a nested dict or OrderedDict from cmdline or json file
	# useful for cmdline, and adding parameters to an existing dict or OrderedDict
	cfg = expand_nested(cfg, 
			sep =cfg.get('-expand_nested',':'),
			pop =cfg.get('-pop_expanded_nest',True))

	# need to repeat since there may be a new keymap from the above
	cfg=defaults(cfg) 


	cfg = routine_specific(cfg)

	# inheriting non-string parameters in both type and value
#	print('----')
#	show(cfg, full=True)
#	print('----')
	cfg = copy_par(cfg, 
			pre =cfg.get('-copy_par_pre','{='),
			post=cfg.get('-copy_par_post','}'))
#	show(cfg, full=True)
#	print('----')

	cfg = enforce_format(cfg, 
			enforcer =cfg.get('-enforce_format',None))

	# either delete variables or set them None
	cfg = delete_or_None(cfg, 
			pre =cfg.get('-del_or_none_pre','\.'))

	# key mapping
	if "-cfg<<cfg" in cfg:
		keymap = OrderedDict()
		for idx, epar in enumerate(cfg["-cfg<<cfg"]):
			tpar, spar = inoutpar(epar)
			if tpar == spar: spar = '-'+spar
			if tpar not in cfg and spar in cfg: cfg[tpar] = cfg[spar]
			if spar not in cfg and tpar in cfg: cfg[spar] = cfg[tpar]
			keymap[spar] = tpar
			keymap[tpar] = spar
		cfg['-keymap'] = keymap
	return cfg
	""" """
	
#----------------------------------------------------------------------------
# execute configuration file
def execute(cfg, previously=None):
	""" execute the main routine called in cfg
	"""
	# [-exec] : execution style, default is 'one_go' below
	# -main   : the main routine to call
	# [-type] : the main routine type
	#	    generic [default], native
	# [-prev] : smuggling the actual data output of the previous run if specified
	#	    need to be controlled

	cc = color_scheme(cfg.get('-color_scheme','dark'))

	if help_text(cfg.get('-help', False), cc=cc): return 0

	if '-main' not in cfg.keys():
		print('no _main: need the main subroutine to execute')
		if '-show' in cfg.keys(): show(cfg, full=True, cc=cc)
		return -1
	
#	if previously != None:
#		data['-prev']=previously

	if '-show' in cfg.keys():
		if type(cfg['-show']) is bool:
			show(cfg,cc=cc)
			return 0
		if cfg['-show'] == 'hidden':
			show(cfg, full=True, cc=cc)
			return 0

	show_what=cfg.get('-show','').split(',')

#	start_time_all=datetime.now()
#	print(0,'{}'.format(datetime.now() - start_time_all))

	levels  = cfg['-main'].split('.')
	module  = __import__(levels[0])
	routine = module
	for each in levels[1:]: 
		try:
			routine = getattr(routine, each)
		except AttributeError:
			routine = import_module(each, routine)

	userhelp=cfg.get('-Help',False)

	if userhelp == True:
		if routine.__doc__ == None:
			print('hmm, does not have any doc in', cfg['-main'])
#			help(routine)
		else:
			print(routine.__doc__.replace("\n\t","\n"))
#			help(routine)
		return 0

	if hasattr(routine,'__code__'):
		routine_keys = routine.__code__.co_varnames[:routine.__code__.co_argcount][::-1]
	else: routine_keys = []
	routine_args,  routine_kwargs = get_func_parameters(routine)

	if 'func' in show_what:
		show_feed(routine_args, routine_kwargs, cfg['-main'])
		return 0

	if '-native' not in cfg.keys(): 
		# search for native routines, which is set by default parameter value begin
		# a bit adhoc since we are setting the parameter to be string in the definition
		# but it will be fed with dict() or cjson() itself during runtime
		# if both (self, cfg) exist, then the first one takes the priority
#		for each in [native, native_class]: 
		for (k, v) in routine_kwargs.items():
			if v == native:
				native_key = k
				cfg['-native'] = v
				break

	cfg['-native'] = cfg.get('-native',	'')

	cfg['-pars']   = cfg.get('-pars',	routine_keys[::-1])
	default=OrderedDict()
	for each in cfg['-pars']:
		if each in cfg: default[each] = cfg[each]

	if 'default' not in locals(): default=copy(cfg)

	# set module level global parameters
	if '-global' in cfg.keys(): 
		gvar = cfg['-global']
		# doing this here for safety
		if type(gvar) is list:
			gvar=OrderedDict()
			for each in cfg['-global']:
				if each in cfg.keys():
					gvar[each] = cfg[each]
		set_module_parameters(module, gvar)


	# default variables
	# -repeat: determine if calling the routine multiple times with varing input parameters
	#	iter: variable based repeat if exists
	#	infile: file(name) based repeat 
	#		infile: input file, required
	#		outfile: output file, optional
	#		indir: input directory, optional
	#		outdir: output directory, optional
	#		outsubdir: output subdirectory, optional
	# -pars: parameters to be fed into the routine
	#	should be set by the routine if generic

	if '-repeat' not in cfg.keys(): 
		if   '-iter'   in cfg.keys(): cfg['-repeat'] = "variable"
		elif '-infile' in cfg.keys(): cfg['-repeat'] = "filename"
		else:                         cfg['-repeat'] = ""

	tkeys	  = cfg.get('-tagkeys',   None)	# grab tags from these parameters
	akeys	  = cfg.get('-appkeys',   None)	# apply tags to these parameters
	fkeys	  = cfg.get('-filekeys',  None)	# apply tags to these files
	ofkeys  = cfg.get('-ofilekeys', None)	# apply tags to these files located in a folder w.r.t. output
	ifkeys  = cfg.get('-ifilekeys', None)	# apply tags to these files located in a folder w.r.t. input
	absent  = cfg.get('-absent',    None)	# what to assign to absent files for further action
	fcheck  = cfg.get('-filecheck', [])		# check the status of these files if requested
	tckey   = cfg.get('-timekey',   None)	# apply time cut using "after" and "before" to these files
	sckey   = cfg.get('-sizekey',   None)	# apply size cut using "larger" and "smaller" to these files
	if '-infile' in cfg: stkey = cfg.get('-sortkey', "-infile")	# sort key
	else:	               stkey = None

	# force run without clobber option even if output exists for these cases
	after   = cfg.get("-after"  , None)	# when existing outputs are modified after a certain time
	before  = cfg.get("-before" , None)	# when existing outputs are modified before a certain time
	smaller = cfg.get("-smaller", None)	# when existing outputs are smaller than a certain size
	larger  = cfg.get("-larger" , None)	# when existing outputs are larger than a certain size

	if "-infile"  in cfg: fcheck.insert(0, '-infile')
	if "-outfile" in cfg: fcheck.append('-outfile')

	if stkey != None:
		if stkey not in fcheck: fcheck.append(stkey)
#	print('fcheck',fcheck)

	if after  != None: after  = timestr2stamp(after)
	if before != None: before = timestr2stamp(before)

	if tckey != None:
		after_outfile=None
		before_outfile=None
	else:
		after_outfile =after
		before_outfile=before

	if sckey != None:
		larger_outfile=None
		smaller_outfile=None
	else:
		larger_outfile=larger
		smaller_outfile=smaller

	out=None

	if cfg['-repeat'] == "":

		tasks = OrderedDict()
		tasks['main'] = OrderedDict()
		tasks['main']['-mcfg'] = cfg

	else:
		c_dir=getcwd()
		if '-basedir' in cfg: chdir(cfg['-basedir'])

		if cfg['-repeat'] == "variable":
			tasks=set_tasks(default=default, 
					akeys=akeys, tkeys=tkeys, 
					fkeys=fkeys, ifkeys=ifkeys, ofkeys=ofkeys, 
					absent=absent, fcheck=fcheck, 
					cfg=cfg, verbose=cfg['-verbose']) 
		else:
#			show(default,full=True)
#			show(cfg,full=True)
			tasks=set_files(default=default, 
					akeys=akeys, tkeys=tkeys, 
					fkeys=fkeys, ifkeys=ifkeys, ofkeys=ofkeys, 
					absent=absent, fcheck=fcheck, 
					cfg=cfg, verbose=cfg['-verbose']) 

		if tasks == None:
			if 'job' in show_what: print(cc.err+'no tasks found'+cc.reset)
#			print(routine.__doc__)
			return 0

		# sorting the tasks
		skip_sort=False
		if cfg['-sort'] != None and stkey != None:
			try:
				mat=re.match(r'([~]*)(.+)',cfg['-sort'])
			except:
				skip_sort=True

			if not skip_sort:
				sortby = mat.group(2)
				if   sortby == 'name'     : defsortval=""		# filename with path
				elif sortby == 'basename' : defsortval=""		# only by filename
				elif sortby == 'modtime'  : defsortval=datetime.timestamp(datetime.now())
				elif sortby == 'size'     : defsortval=0
				else:
					print(cc.hl+'skip sorting: no sorting method by',sortby)
					print('   available sorting methods: name, basename, modtime, size'+cc.reset)
					skip_sort=True

			if not skip_sort:
				if len(mat.group(1)) == 1: reverse = True
				else:                      reverse = False

				for task in tasks:
					cfcheck=tasks[task]['-fcheck'][stkey]
					if sortby == 'basename':
						tasks[task]['-sortval']=path.basename(cfcheck.get('name', defsortval))
					else:
						tasks[task]['-sortval']=cfcheck.get(sortby, defsortval)
				tasks = OrderedDict(sorted(tasks.items(),  \
						key=lambda x: x[1]['-sortval'], reverse=reverse))


	ntasks = len(tasks)
	if 'job' in show_what:
		print(cc.hl+'# of jobs:',ntasks,cc.reset)

	index=0
	start_time_all=datetime.now()

	# insert pre process 
	if "-prep" in cfg:
		pre=stripkey(cfg["-prep"])
		if '-autopar' not in pre: pre['-autopar'] = cfg.get('-prep:-autopar', True)
		# pre  << cfg : simple inheirt of cfg parameters
		# pre  << main: input parameters to pre-process from the main routine
		#			expect a set of list variables
		#			one of them should be set by "-key"
		#			which is the key for return variables
		# main << pre: output returns from pre-process to the main routine
		#			tuples of dicts with key set by "-key"
		#
		# if source and target variable names are different, 
		# use "trg_var << src_var", otherwise, simply use "var"
		# for main<<pre, the source variable indicates 
		# the tuple order of the main output
		# e.g., "success<<2"
		for each in ["-prep<<cfg","-prep<<main","-main<<prep"]:
			if each not in pre: pre[each]=[]
			if type(pre[each]) is str: pre[each] = [pre[each]]

		# prep input parameters for pre-process
		# input is a set of lists, and one of which is tied to key
		for epar in pre["-prep<<main"]:
			tpar, spar = inoutpar(epar)
#				pre[tpar] = [tasks[task]['-mcfg'][spar] for task in tasks]
			pre[tpar] = {task: tasks[task]['-mcfg'][spar] for task in tasks}

		# inherit some global configurations
		for idx, epar in enumerate(pre["-prep<<cfg"]):
			tpar, spar = inoutpar(epar)
#			if tpar == spar: spar = '-' +spar
			if spar in cfg: pre[tpar] = cfg[spar]

		pre_levels = pre['-main'].split('.')
		if pre_levels[0] == levels[0]: pre_module = module
		else:                          pre_module = __import__(pre_levels[0])
		pre_routine = pre_module
		for each in pre_levels[1:]: pre_routine   = getattr(pre_routine, each)

		if 'job' in show_what:
			print(cc.hl+'pre-proc:',pre_module.__name__, pre_routine.__name__,cc.reset)

		if   'input'    in show_what: show(pre, cc=cc)
		elif 'inputall' in show_what: show(pre, full=True, cc=cc)

		if cfg['-runprep']:
			pre_args, pre_kwargs = get_func_parameters(pre_routine)

			if pre['-autopar']:
				for key in set(pre_args) | set(pre_kwargs.keys()):
					if key not in pre.keys():
						var=OrderedDict()
						for task in tasks:
							mcfg=tasks[task]['-mcfg']
							if key in mcfg.keys(): var[task]=mcfg[key]
						if len(var) != 0:
							pre[key] = var
						else:
							if key in cfg.keys(): pre[key] = cfg[key]


			pre_args, pre_kwargs = set_func_parameters(pre_args, pre_kwargs, cfg=pre)
			pre_out = pre_routine(*pre_args, **pre_kwargs)

			if type(pre_out).__name__ == 'function': 
				pre_args, pre_kwargs = get_func_parameters(pre_out)
				pre_args, pre_kwargs = set_func_parameters(pre_args, pre_kwargs, cfg=pre)
				pre_out=pre_out(*sorted_args, **sorted_kwargs)

			if type(pre_out) is not tuple: pre_out = [pre_out]
#			from IPython import embed; embed()

			if 'time' in show_what: 
				runtime(start_time_all, datetime.now(), pre['-main'], jobid='pre-proc ',cc=cc)

			# wrap up output from pre-process
			# output has to be a dict with key to ensure a proper assignment 
			for idx, epar in enumerate(pre["-main<<prep"]):
				sidx = idx
				tpar, spar = inoutpar(epar)
				if tpar != spar: sidx = int(spar)
				for task in tasks:
					mcfg=tasks[task]['-mcfg']
					mcfg[tpar] = pre_out[sidx].get(task, mcfg.get(tpar, None))
#						print(tpar, mcfg[tpar], '=====')
					tasks[task]['-mcfg']=mcfg
#						if epar in mcfg: print(mcfg[epar])

		# need to update fcheck
		fups = list(set(cfg['-filecheck']) & set(pre['-main<<prep']))
		if len(fups) >0:
			# this part is very similar to a portion of set_file_pars
			# need to be pull out as a function
			# and redo after the main process
			for task in tasks:
				fcres=tasks[task]['-fcheck']
				mcfg =tasks[task]['-mcfg']
				for key in fups:
					fcres[key]['name'] = mcfg[key]
					if not path.isfile(mcfg[key]): 
						fcres[key]['absent'] = True
						continue
					fcres[key]['absent'] = False
					fcres[key]['modtime'] = Path(mcfg[key]).stat().st_mtime
					fcres[key]['size']    = Path(mcfg[key]).stat().st_size
					if '-latest' not in fcres:
						fcres['-latest'] = key
					else:
						if fcres[key]['modtime'] >= fcres[fcres['-latest']]['modtime']:
							fcres['-latest'] = key
				fcres['-updated'] = False
				if '-latest' in fcres:
					if   fcres['-latest'] == '-outfile':               fcres['-updated'] = True
					elif fcres['-latest'] in cfg.get('-ofilekeys',[]): fcres['-updated'] = True

				tasks[task]['-fcheck'] = fcres


	if "-post" in cfg:
		post=stripkey(cfg["-post"])
		# post << cfg : simple inheirt of cfg parameters
		# post << main: input parameters to post-process from the main routine, 
		#               the main routine returns tuples of variables
		#		    the post process expect a dict with key=task
		# post << pre : feed the return output from pre-process to post-process
		#		    for now, pre-process output is a dict array, and 
		#		    post-process input expectes a dict with key=task or key=-key 
		#		    set in pre-process
		for each in ["-post<<cfg","-post<<main","-post<<prep"]:
			if each not in post: post[each]=[]
			if type(post[each]) is str: post[each] = [post[each]]

	out=OrderedDict()

	for task in tasks:
		index = index+1
		mcfg = tasks[task]['-mcfg']
		
		if "-post" in cfg:
			out[task] = [None for epar in post["-post<<main"]]

		if "-cfg<<cfg" in cfg:
			for idx, epar in enumerate(cfg["-cfg<<cfg"]):
				tpar, spar = inoutpar(epar)
				# only applied to cfg<<cfg since they are the same level
				if tpar == spar: spar = '-'+spar
				if spar in mcfg: mcfg[tpar] = mcfg[spar]

#						
		maxlen=len(str(ntasks))
		jobid=str(index).rjust(maxlen)+'/'+str(ntasks)
		if 'job' in show_what:
			print(cc.hl+'job',jobid+':',cfg['-main'],cc.reset+task,cc.reset)

		if 'input' in show_what: 
			show(mcfg, cc=cc)
			continue
		if 'inputhidden' in show_what: 
			show(mcfg, full=True, cc=cc)
			continue
		if 'files' in show_what: 
			if '-fcheck' in tasks[task].keys(): 
				show_files(tasks[task]['-fcheck'], ofilekeys=ofkeys, cc=cc,
						keymap=cfg.get('-keymap',{}),
						basedir=mcfg.get('-basedir', None))

		# if this is a native routine, feed the whole thing either by class itself or cfg
		sorted_args, sorted_kwargs = set_func_parameters(routine_args, routine_kwargs, cfg=mcfg)

		if   cfg['-native'] == native      : sorted_kwargs[native_key] =  mcfg
#			elif cfg['-native'] == native_class: sorted_kwargs[native_key] =  cjson(cfg=mcfg)

		if '-fcheck' in tasks[task].keys(): 
			cur_fcheck=tasks[task]['-fcheck']
		else: 
			cur_fcheck=OrderedDict()

		# time based cut
		if tckey != None: 
			ftcheck = cur_fcheck.get(tckey, None)
			if ftcheck != None:
				if skip_by_file_modtime(ftcheck.get('modtime', None), after=after, before=before):
					if 'job' in show_what: print(cc.err+'skipping job', jobid,cc.reset)
					continue

		# size based cut
		if sckey != None: 
			fscheck = cur_fcheck.get(sckey, None)
			if fscheck != None:
				if skip_by_file_size(fscheck.get('size',None), larger=larger, smaller=smaller):
					if 'job' in show_what: print(cc.err+'skipping job', jobid,cc.reset)
					continue

		# implement clobbering with skip
		if '-outfile' in mcfg:
			if skip_by_outfile(mcfg['-outfile'], \
					basedir = mcfg.get('-basedir', None ), \
					dryrun  = mcfg.get('-dryrun' , False), \
					clobber = mcfg.get('-clobber', False), \
					keep    = mcfg.get('-keep'   , None ), \
					drop    = mcfg.get('-drop'   , None ), \
					fcheck  = cur_fcheck.get('-outfile', None), \
					after   = after_outfile, before=before_outfile, \
					larger  = larger_outfile, smaller=smaller_outfile, \
					updateonly = mcfg.get('-updateonly', False), \
					verbose = mcfg['-verbose']):
				if 'job' in show_what: print(cc.err+'skipping job', jobid,cc.reset)
				continue

		# now run
		start_time=datetime.now()
		if 'feed' in show_what:
#			print(cfg['-main'])
##			print(routine_keys)
#			print(sorted_args)
#			show(sorted_kwargs)
#			print(type(sorted_kwargs))
			show_feed(routine_args, routine_kwargs, cfg['-main'], cc=cc,
					inargs=sorted_args, inkwargs=sorted_kwargs)
			continue

		out_main=routine(*sorted_args, **sorted_kwargs)
		if type(out_main).__name__ == 'function': 
#			print(type(out_main).__name__)
			routine_args,  routine_kwargs = get_func_parameters(out_main)
			sorted_args,   sorted_kwargs  = set_func_parameters(routine_args, routine_kwargs, cfg=mcfg)
			out_main=out_main(*sorted_args, **sorted_kwargs)

		if 'output' in show_what: print(out_main)
		if type(out_main) is tuple: out[task] =  out_main
		else:                       out[task] = [out_main]
#			
		if 'time' in show_what: 
			runtime(start_time, datetime.now(), cfg['-main'], jobid='job '+jobid, cc=cc)

	# insert post process here?
	if "-post" in cfg:

		if '-autopar' not in post: post['-autopar'] = cfg.get('-post:-autopar', True)
		# wrap up output from main loop
		for idx, epar in enumerate(post["-post<<main"]):
			tpar, spar = inoutpar(epar)
			sidx = idx
			if tpar != spar: sidx = int(spar) 
			for task in tasks:
				# there could be an additional option to make this
				# simple list like this or dict array with key using "-key"
				# list 
#					post[tpar] = [out[task][sidx] for task in tasks]
				# dict with key=task
				post[tpar] = {task: out[task][sidx] for task in tasks}

		if "-prep" in cfg and "-post<<prep" in post:
			for idx, epar in enumerate(post["-post<<prep"]):
				tpar, spar = inoutpar(epar)
				sidx = idx
				if tpar != spar: sidx = int(spar)
				# list
#					src = pre_out[sidx]
#					post[tpar]=[src[k] for k in src.keys()]
				# dict with key=-key par
				post[tpar] = pre_out[sidx]

		# inherit some global configurations
		for idx, epar in enumerate(post["-post<<cfg"]):
			tpar, spar = inoutpar(epar)
#			if tpar == spar: spar = '-'+spar
			if spar in cfg: post[tpar] = cfg[spar]

		post_levels = post['-main'].split('.')
		if post_levels[0] == levels[0]: post_module = module
		else:                           post_module = __import__(post_levels[0])

		post_routine = post_module
		for each in post_levels[1:]: post_routine = getattr(post_routine, each)

		if 'job' in show_what:
			print(cc.hl+'post-proc:',post_module.__name__, post_routine.__name__,cc.reset)

		if   'input'    in show_what: show(post, cc=cc)
		elif 'inputall' in show_what: show(post, full=True, cc=cc)
		else:
			post_args, post_kwargs = get_func_parameters(post_routine)
			if post['-autopar']:
				for key in set(post_args) | set(post_kwargs.keys()):
					if key not in post.keys():
						var=OrderedDict()
						for task in tasks:
							mcfg=tasks[task]['-mcfg']
							if key in mcfg.keys(): var[task]=mcfg[key]
						if len(var) != 0:
							post[key] = var
						else:
							if key in cfg.keys(): post[key] = cfg[key]

			post_args, post_kwargs = set_func_parameters(post_args, post_kwargs, cfg=post)
			post_out = post_routine(*post_args, **post_kwargs)

			if type(post_out).__name__ == 'function': 
				post_args, post_kwargs = get_func_parameters(post_out)
				post_args, post_kwargs = set_func_parameters(post_args, post_kwargs, cfg=post)
				post_out=post_out(*sorted_args, **sorted_kwargs)

#			from IPython import embed; embed()

			if 'time' in show_what: 
				runtime(start_time_all, datetime.now(), post['-main'], jobid='post-proc', cc=cc)

	end_time=datetime.now()
	if 'time' in show_what: 
		runtime(start_time_all, end_time, cfg['-main'], jobid='job '+'all'.ljust(len(jobid)), cc=cc)

	log(cfg, start_time_all, end_time)
#		print('execute: out ->', out)
#		from IPython import embed; embed()
	return out
	""" """

# execute input parameter assuming it's one run
def oneGo(pars=sys.argv[1:], previously=None):
	""" set parameters and execute
	"""
	cfg=get_parameters(pars)
	if '-exec' not in cfg.keys():
#			print('oneGo: previously',previously)
		out=execute(cfg, previously=previously)
#			print('oneGo: out',out)
		return out
	return -1
	""" """

# execute a series of run
def go(pars=sys.argv[1:]):
	""" the main function, enables a series of runs 
	"""
	if type(pars) is not list: pars=[pars]

	coms=[] # common json file set
	comc=[] # common command line
	sets=[] # json file set
	setc=[] # command line for each json
	
	if '--relay' in pars: continuous=True
	else:			    continuous=False

	if '--parse' not in pars: parse=True
	if '--parse'     in pars: parse=True
	if '-^-parse'    in pars: parse=False
	if '--^parse'    in pars: parse=False
	# check common variables
	if '--with' in pars: 
		idx=pars.index('--with')
		for par in pars[idx+1:]:
			if bool(re.search("^[^-{].*json$",par)): coms.append(par)
			else:                                    comc.append(par)
		pars=pars[0:idx]

	# run one by one
	# need to fix this for command line version
	cc=[]
	for par in pars:
		if bool(re.search("^[^-{].*json$",par)) and parse:
			sets.append(par)
			new=[]
			setc.append(new)
		else:
			try:
				new.append(par)
			except NameError:
				cc.append(par)

	if len(sets) == 0:
		out=oneGo(cc)
		return out

	out=0
	for esets, esetc in zip(sets, setc): 
		if not continuous: out=0
		out=oneGo(cc+coms+[esets]+comc+esetc, previously=out)

	return out
	""" """

#----------------------------------------------------------------------------
# obsolete
def history(cfg):
	""" make a copy of the configuration hash variable as a json file 
	"""
	# called at the end of the program
	# requires the directory name: set by _hisdir
	# the filename is automatically assigned by date_time, 
	# but can be set manually by _hisfile

	if cfg['-dryrun']: return

	if '-hisfile' not in cfg.keys(): return
	if '-hisdir'  not in cfg.keys(): return
	
	historyfile=Path(cfg['-hisdir']) / Path(cfg['-hisfile'])
	makedirs(historyfile,exist_ok=True)
	json.dump(cfg, open(historyfile,"w"))

	""" """

def log(cfg, start_time, end_time):
	""" write a log
	"""
	# called at the end of the program
	# requires the directory name: set by _hisdir
	# the filename is automatically assigned by date_time, 
	# but can be set manually by _hisfile

	if cfg['-dryrun']: return

	if '-logfile' not in cfg.keys(): return
	if not cfg.get('-save_cmdline_log', False):
		if cfg.get('-jsonfiles', None)  == None: return  
		# ignore command line tools, which usually don't have a direct json file input to parse
	
#	username = getuser()
	hostname = gethostname()

	cfg_str = json.dumps(cfg)
	hashres = hashlib.sha1(cfg_str.encode())

	loginfo = ['{}'.format(start_time)[2:19],'{}'.format(end_time - start_time),
#			'{}'.format(time)[0:19],
			'SHA1:'+hashres.hexdigest(),
			cfg['-main'], '', hostname, 
			'']
	loginfo = ' '.join(loginfo)

	logfile=path.expanduser(cfg['-logfile'])
	if path.isfile(logfile): 
		lfile = open(logfile,"a")
		lfile.write('\n'+loginfo)
	else:                    
		lfile = open(logfile,"w")
		lfile.write(loginfo)
	lfile.close()

	hisfile = cfg.get('-hisfile', None)
	if hisfile == None: return
	if hisfile == '_auto_':
		filename = start_time.strftime("%y%m%d_%H%M%S")+'_'+cfg['-main']+'.json'
		hisfile = Path(logfile).parent / Path(filename)

#	json.dump(cfg, open(hisfile,"w"))
	hfile = open(path.expanduser(hisfile),"w")
	hfile.write('//'+loginfo+'\n')
	hfile.write(cfg_str.replace(',',',\n\t'))
	hfile.close()

	""" """

def runtime(start_time, end_time, label, jobid='', cc=None):
 
	if cc == None: cc=color_scheme('dark')
	print(cc.key+jobid+':','{}'.format(end_time - start_time), 
			cc.type+'{}'.format(start_time), 
			cc.key+label, cc.reset)

#----------------------------------------------------------------------------
# extracted from Jonathaneunice/ansiwrap
# to eliminate ansi_terminate_lines, which seems to have a bug
# string_types = basestring if sys.version_info[0] == 2 else str

def ansilen(s):
	"""
	Return the length of a string as it would be without common
	ANSI control codes. The check of string type not needed for
	pure string operations, but remembering we are using this to
	monkey-patch len(), needed because textwrap code can and does
	use len() for non-string measures.
	"""
#	if isinstance(s, string_types):
	if isinstance(s, str):
		s_without_ansi = re.compile('\x1b\\[(K|.*?m)').sub('', s)
		return len(s_without_ansi)
	else:
		return len(s)

# now replace the standard len of textwrap3 
textwrap3.len = ansilen

#----------------------------------------------------------------------------
def deco_text(text, cc=None, width=80, add_indent=24):
	if cc == None: cc=color_scheme('dark')

	conv= OrderedDict()
	conv['{version}']=__version__
	conv['{tt} ' ]=cc.key
	conv['{ty} ' ]=cc.type
	conv['{df} ' ]=cc.hl
	conv[' {re}' ]=cc.reset
	conv['{hd} ' ]=cc.defs
	conv['\n\t'  ]='\n'
	conv['\t'    ]='      '
	conv['{..} ' ]=''
	for key in conv.keys(): text=re.sub(key, conv[key], text) 
	wrapped=[]
	for line in text.split('\n'): 
		wrapped.append(wrap_line(line, width=width, add_indent=add_indent))
	return "\n".join(wrapped)

def wrap_line(line, width=80, add_indent=24):

	mat=re.search('^( +)[^ ]*', line)
	if bool(mat):
		nb = len(mat.group(1))
		if nb !=0: nb+=add_indent
		indent=' '.ljust(nb)
	else: indent=''
	return "\n".join(textwrap3.wrap(line, width=width, subsequent_indent=indent))

def wrap_text(text, width=80, add_intent=24):
	wrapped=[]
	for line in text.split('\n'):
		wrapped.append(wrap_line(line))
	return "\n".join(wrapped)

def help_text(sub=None, cc=None, width=80):
	""" print out the help text
	"""

	# missing parts: 
	#	startup: startup, aliasing, native function
	#	iteration: iterative procedure and file search
	#	decoration: prep and post process
	#	logging :
	#	serial: serial run
	#
	#	omit "{" "}"
	parts = ['main',
			'overview',
			'features',
			'json',
			'pars',
			'startup',
			'iteration',
			'decoration',
			'logging',
			'sequential',
			'cmdline',
			'changes'
			]
	usage = {}
	for each in parts:
		usage[each] = deco_text(globals()['help_text_'+each](), cc=cc, width=width)

	if type(sub) is not bool:
		mat=re.search('^func:(.*)',sub)

	if sub == False: return False

	if sub == True:
		print(usage['main'])
		return True

	if sub in parts:
		print(usage[sub])
		text="try also: \n\t\t--help " + " | ".join(parts[1:])+" | all "+ "| func: | func:[function name]"
		print(deco_text(text, cc=cc, width=width, add_indent=6))
	elif bool(mat):
		if mat.group(1) == '':
			for k, v in globals().items():
				if k[0:1] == '_' : continue
				if type(v).__name__ != 'function': continue
#				print(k, type(v).__name__)
			show(globals(), hidden='_')
		else:
			functions=mat.group(1).split(',')
			for each in functions:
#			routine=__getattr__(each)
				routine=globals()[each]
				ctext=routine.__doc__
				ctext=(ctext[::-1].replace('\n','', 1))[::-1]
				print(cc.key+each,cc.reset)
				print(ctext)
	elif sub == 'all':
		for sec in usage.values(): print(sec)
	elif sub == 'readme':
		bw=color_scheme('bw')
		for each in ['main','startup','overview']: 
			print(deco_text(globals()['help_text_'+each](), cc=bw, width=width))
		text="try also: \n\t\t --help " + " | ".join(parts[1:])+" | all "+ "| func: | func:[function name]"
		print(deco_text(text, cc=bw, width=width, add_indent=6))
	else:
		print("unknown topic:", sub)
		text="try: \n\t\t --help " + " | ".join(parts[1:])+" | all "+ "| func: | func:[function name]"
		print(deco_text(text, cc=cc, width=width, add_indent=6))

	return True
	""" """

#----------------------------------------------------------------------------
def help_text_main():
	return """Usage: {tt} cjpy  json_input_file1 -options_for_file1 ... \\
			[json_input_file2 -options_for_file2 ...] \\
			[--with common_json_files -common_options ...] {re}

	Command liner for python routines using json based input parameter files. 
	Ver {version} by Jaesub Hong (jhong@cfa.harvard.edu)

		{tt} cjpy --help [overview json pars cmdline all ... func:] {re}
		{tt} cjpy [json_files ...] --Help  {re}
		{tt} cjpy --main module.routine --Help  {re}
	"""
def help_text_overview():
	return """{hd} ## An overview of the basic concept: {re}

	The cjson input parameter files can contain the name of the routine to call: e.g., {tt} "-main": "module.routine" {re}.  Keys starting with alphabets are assumed to be fed into the main routine set by {tt} "-main" {re} key.  Assume that a python script {tt} example.py {re} has

		{tt} def my_sum(name, x, y):
		     \"\"\" This is my sum. \"\"\"
		     print(name+':', x+y) {re}

	Then with a json file {tt} input.json {re},

		{tt} "-main": "example.my_sum",
		    "x": 5,
		    "y": 7, 
		 "name": "answer", {re}

	one can execute the routine {tt} my_sum {re} in a shell command prompt like 

		{tt} % cjpy input.json
		{ty} answer: 12 {re}

	In princinple, all the content in the json files can be fed as a long string in the command line or as optional parameters for individual keys with "-". So the above example is equivalent to the followings even without the json file {tt} input.json {re}.

		{tt} % cjpy --main example.my_sum -#x 5 -#y 7 -name "answer" {re} 
		{tt} % cjpy '{"-main":"example.my_sum","x":5,"y":7,"name":"answer"}' {re}

	or some combination of all three examples:

		{tt} % cjpy '{"-main":"example.my_sum","name":"answer"}' -#x 5 -#y 7 {re}
		{tt} % cjpy input.json '{"name":"answer"}' -#x 5 -#y 7 {re}

	When both json files and command line input options are available for the same key, the command line options take a priority.  Note {tt} # {re} in {tt} -#x {re} ensures it is a number but not a string.  See more details with {tt} cjpy --help cmdline {re}. Note {tt} --Help {re} (capital H) prints out the doc string of the routine.

		{tt} % cjpy input.json --Help
		{ty} This is my sum. {re}

	Calling multiple JSON files execute them in sequence.

		{tt} % cjpy input.json input.json
		{ty} answer: 12 
		answer: 12 {re}

		{tt} % cjpy input.json -#x 7 input.json -#x 6
		{ty} answer: 14 
		answer: 13 {re}

	Find out what kind of parameters are needed to call the routine using {tt} --show func {re} option.

		{tt} % cjpy --main os.path.isfile --show func
		{ty}  main: os.path.isfile
		 path {re}

	The above example shows {tt} isfile {re} expect a parameter called {tt} path {re}.

		{tt} % cjpy --main os.path.isfile -path cjson.py --show output
		{ty} True {re}

	Can check how the parameters get fed to the routine.

		{tt} % cjpy --main os.path.isfile -path cjson.py --show feed
		{ty}  main: os.path.isfile
		 path << str cjson.py {re}

		{tt} % cjpy input.json --show feed
		{ty}  main: example.my_sum
		 name << str answer 
		    x << int 5 
		    y << int 7 {re}

	Can call a routine needing no input parameters.

		{tt} % cjpy --main datetime.datetime.now --show output
		{ty} 2022-04-27 22:11:52.983532 {re}

	One can force the parameters to a function with {tt} --pars {re} option.

		{tt} % cjpy --main math.sin -#x 1.0 --pars 'x' --show output
		{ty} 0.8414709848078965 {re}
	"""
def help_text_features():
	return """{hd} ## The main objectives, features and limitation: {re}

	There are many excellent packages that handle input parameters of
	routines and link them to matching command line tools. The main purpose
	of this program is, though, to faciliate a command line call of an arbitrary
	python routine without additional wrapper script for the routine. At
	the same time, for some tasks, the input parameters themselves are part
	of the important data to keep and track.  This program encourages the use
	of an input file in JSON format for input parameters, so that the input
	parameters are available for later review, modification and rerun.  Since
	the input parameters contain the name of the main routine to call (i.e.,
	poor man's objective oriented programming), there is no need for
	additional wrapper script.  For simple routines that don't really need
	the input parameter files, a simple alias can be used for easy repetitive
	call instead of a wrapper script (try {tt} --help startup {re}). Some of
	the main features are:

	- Calling a python routine from a command line without any wrappers
	- Enable somewhat a clean separation between the routine (program) and
	  the input parameters (data).
	- Support iterative routine calling with minimal parameter setting
	- Support calling multiple routines sequentially
	- Provide flexible command line options for easy on-the-fly modification
	  of parameter changes
	- Support automatic logging of the input parameters and run condition
	  through hashing
	- Support rudimentary extension of JSON format including commenting,
	  simple math, and variable substitution.
	- Provide recursive file search function with basic regex for the cases
	  that the same routine has to deal with lots of similar-type but
	  different files.
	- Provide the check of the mod time of files to process and enable an
	  easy option to what to process and what not to process.
	- For iterative runs, pre-process and post-process routine can be called
	  to facilitate more complex iterations and the job needed to process the
	  collection of results
	- Allow an option to pass the complete set of the input parameters for
	  routines that are written specifically for cjpy
	- When the called routine returns another routine, the new routine is
	  also called.

	In regarding the data type of input parameters, cjpy provides a few tools
	to ensure proper types, but not as strict as some of other tools. The motto is
	"quickish and dirtish" is goog enough, although we don't want to go as far as 
	"quick and dirty.

	The current limitations of the program are:
	- Routines of a class: this should work in principle and it does for
	  some, but not tested as extensive as for regular routines
	- Routines with decorators or processed by function manipulators often end
	  up with unclear arguments and keyword arguments, sometimes splitted
	  over the original routine and decorators/manipulators.  In this case,
	  the user has to manually make sure what parameters are fed (in what
	  order for non-keyword parameters). Use {tt} -collect_kwpars {re} and
	  {tt} -exclude_kwpars {re} to efficently facilitate this.

	"""
def help_text_json():
	return """{hd} ## Features in setting parameters with JSON files: {re}

	In cjpy, the JSON format is used for input parameter files. There may be other more popular or capable formats, but JSON seems to be one of the most compatible formats with the python dictionary, which is versatile and easy to handle, even though it tends to be a bit verbose. 

	Unlike the standard JSON, commenting is allowed in cjpy with the c-style notation of {tt} // {re}. The outermost {tt} "{" {re} and {tt} "}" {re} can be omitted to simulate a more configuration-file like feel. String-only variables are allowed for tagging & replacing by calling the "key" in the "{key}" format: e.g., 

		{tt} "key1": "Abcdef", "key2": "{key1} & more" {re} is equivalent to
		{tt} "key1": "Abcdef", "key2": "Abcdef & more" {re} 

	Enclosures {tt} "{>" {re} and {tt} "}" {re} allow a similar subsititution, but the substitution occurs after all other variables are substituted.

		{tt} "k1": "Abcd", "k2": "{k1}!", "k3": "{k2}?" {re} is equivalent to
		{tt} "k1": "Abcd", "k2": "Abcd!", "k3": "{k1}!?" {re} 

		{tt} "k1": "Abcd", "k2": "{k1}!", "k3": "{>k2}?" {re} is equivalent to
		{tt} "k1": "Abcd", "k2": "Abcd!", "k3": "Abcd!?" {re} 

	For non-string variables, use {tt} {= {re} and {tt} } {re}: e.g.,

		{tt} "key1": [1.5, 20], "key2": "{=key1}" {re}  is equivalent to
		{tt} "key1": [1.5, 20], "key2": [1.5, 20] {re}  

	Basic math expressions in {tt} <expr> {re} are allowed: e.g., 

		{tt} "key" : <3+4*5> {re} changes to {tt} "key": 23 {re}.  

	Trailing commas are allowed: e.g., 

		{tt} "key": [1,2,3,] {re} is the same as {tt} "key": [1,2,3] {re}.

	The built-in keys like {tt} infile {re} can be used with wild cards, which automatically generate a matching file list and successively call the main routine with each file.  {tt} {1}, {2}, ... {key:1}, {key:2}, ... {re} are reserved for tagging and replacing by regex in infile and other parameters for iterations: e.g.,

		{tt} "infile": "(.*)([0-9]+).txt", "outfile": "{1}__{2}.txt" {re}

	If the {tt} infile {re} parameter encounters files named {tt} hello3000.txt, hiThere2000.txt {re} ..., the main routine will be iteratively called with 

		{tt} "infile": "hello3000.txt",   "outfile": "hello__3000.txt" {re}
		{tt} "infile": "hiThere2000.txt", "outfile": "hiThere__2000.txt" 
	     ... {re}

	These features are desirable for convenience, but semi-intentionally limited in order to keep json file mainly for input parameters without over-stepping into the programming side.  Given the rather relaxed rules for JSON in cjpy, recommend avoiding multi-line parameters, which can conflict with commenting and others. Nested variables (dictionary or hash) are ok to use.  

	Parameters with {tt} ==, ~=, != {re} in their keys can be used for a pattern matching to make exceptions through built-in cjson functions like {tt} combine_tags {re}: e.g., 

		e.g., {tt} "infile~=.txt$" : { "x-value": 90, ... } {re}. 

	What this can do is that when the parameter {tt} infile {re} meet files ending with {tt} ".txt" {re}, {tt} x-value {re} is set to 90, superceding other possible settings for {tt} x-value {re}.  
	"""
def help_text_pars():
	return """{hd} ## Parameter usage in JSON input files: {re}

	For command line parameters, add the additional prefix {tt} - {re}:i.e., {tt} "-main" {re} in a JSON file is equivalent to {tt} --main {re} as a command line option.  Parameters starting with alphabets can be potentially fed into the routine called.

		{tt} -main      {ty}  str  {df} None   {re} the main module and routine to call 
		{tt} -load      {ty}  str* {df} None   {re} load other json file: same as --with option in the command line 

		{tt} -infile    {ty}  str* {df} None   {re} regex of input files, any regex should be in (), which can be tagged as {1}, {2},...  
		{tt} -outfile   {ty}  str  {df} None   {re} output file, one can use tags in input file  

		{tt} -iter      {ty}  str* {df} None   {re} task list for iteration 
		{tt} -indir     {ty}  str  {df} None   {re} input directory root, needed for recursive search, otherwise optional 
		{tt} -outdir    {ty}  str  {df} None   {re} output directory root, needed for recursive output matching input, otherwise optional 
		{tt} -include   {ty}  str  {df} None   {re} only choose input files with matching string: regex 
		{tt} -exclude   {ty}  str  {df} None   {re} do not choose input files with matching string: regex 
		{tt} -keep      {ty}  str  {df} None   {re} only run the cases that would create output files with matching string: regex 
		{tt} -drop      {ty}  str  {df} None   {re} only skip the cases that would create output files with matching string: regex 
		{tt} -dryrun    {ty}  bool {df} false  {re} skip a certain part of run defined by user
		{tt} -clobber   {ty}  bool {df} false  {re} overwrite the existing results
		{tt} -outsubdir {ty}  str  {df} None   {re} when an additional subdirectory name is needed to be added 

		{tt} -after     {ty}  str  {df} None   {re} run only for {tt} outfile {re} (default) modified after this time 
		{tt} -before    {ty}  str  {df} None   {re} run only for {tt} outfile {re} (default) modified before this time 
		{tt} -larger    {ty}  str  {df} None   {re} run only for {tt} outfile {re} (default) larger than this size 
		{tt} -smaller   {ty}  str  {df} None   {re} run only for {tt} outfile {re} (default) smaller than this size 

		{tt} -sort      {ty}  str  {df} None   {re} Sort by {df} name, basename, modtime, or size {re}. The default changes to {df} modtime {re} if {tt} -after/-before {re} is set, or to {df} size {re} if {tt} -larger/-smaller {re} is set.

		{tt} -verbose   {ty}  int  {df} 1      {re} chatter level 

		{tt} -recursive {ty}  bool {df} true   {re} recursive input file search, requires indir 
		{tt} -mirror    {ty}  bool {df} true   {re} when input files are searched recursively, does output follow the same directory structure? required outdir 
		{tt} -swapsub   {ty}  dict {df} None   {re} when mirroring indir, if certain subdirectory names needed to be changed 
		{tt} -infile_order {ty}  str {df} sort {re} reverse, unsort: sort input files? (obsolete: use -sort) 

		{tt} -tagkeys   {ty}  str* {df} None   {re} list of file parameters to grab tags 
		{tt} -appkeys   {ty}  str* {df} None   {re} list of parameters to apply tags 
		{tt} -filekeys  {ty}  str* {df} None   {re} list of file parameters to apply tags 
		{tt} -ifilekeys {ty}  str* {df} None   {re} apply tags to these files located in a folder w.r.t. input file folder 
		{tt} -ofilekeys {ty}  str* {df} None   {re} apply tags to these files located in a folder w.r.t. output file folder 
		{tt} -filecheck {ty}  str* {df} None   {re} check the status of these files. When {df} infile and outfile {re} are given, they become the default.
		{tt} -absent    {ty}  dict {df} None   {re} what to assign to absent files for further action set by user 

		{tt} -timekey   {ty}  str  {df} -outfile {re} file key to apply time cut with {tt} after and before {re}.
		{tt} -sizekey   {ty}  str  {df} -outfile {re} file key to apply size cut with {tt} larger and  smaller {re}
		{tt} -sortkey   {ty}  str  {df} -infile  {re} file key to sort with {tt} -sort {re}

		{tt} -hisfile   {ty}  str  {df} none   {re} copy of input json file and command line option, automatically generated if set to be {df} "_auto_" {re}.
		{tt} -logfile   {ty}  str  {df} none   {re} log file 
		{tt} -save_cmdline_log {ty} bool {df} false {re} save log for cmdline tools

		{tt} -repeat    {ty}  str  {df} none   {re} will the call be made repeatly? variable, filename, "" 
		{tt} -native    {ty}  str  {df} none   {re} is the function cjson native or generic?

		{tt} -global    {ty}  str* {df} none   {re} global variables 
		{tt} -pars      {ty}  str* {df} none   {re} input parameters of the function called; must set this for invisible non-keyword parameters: e.g., decorated functions
		{tt} -kwpars    {ty}  str* {df} none   {re} input keyword parameters of the function called; set this for invisible keywords or simply set -collect_kwpars true
		{tt} -collect_kwpars {ty} bool {df} false {re} set this true to feed all the unassigned parameters starting with alphabets as keyword paramters when the routine's keyword parameters are not visible. Use {tt} --show feed {re} to check how the parameters are passed. 
		{tt} -exclude_kwpars {ty} str* {df} none {re} exclude these keyword parameters for function call

		{tt} -enforce_numeric {ty} str {df} #  {re} a prefix to specify cmdline par being a number instead of string; "" to disable it 
		{tt} -enforce_floats {ty} str {df} ##  {re} a prefix to specify cmdline par being a float instead of string; "" to disable it 
		{tt} -pop_enforce_numeric {ty} str {df} true {re} remove the original key for enforced numebrs

		{tt} -enforce_format {ty}  dict {df} none {re}  a full dict for data format enforcer, int, float, complex, bool, str

		{tt} -expand_nested   {ty} str {df} ,  {re} a separator to indicate the nested key or parameter; "" to disable it 
		{tt} -pop_expand_nest {ty} str {df} true {re} remove the original key with nested string,

		{tt} -del_or_none {ty}  str  {df} \.   {re} delete these parameters or set them None

		{tt} -list_pre    {ty}  str  {df} *    {re} a prefix to indicate a list in string variable; "" to disable it 
		{tt} -list_sep    {ty}  str  {df} ,    {re} a separator to indicate a list in string variable; "" to disable it 
		{tt} -pop_expand_list {ty} str {df} true {re} remove the original key with the list string; 

		{tt} -copy_par_pre   {ty}  str {df} {= {re} a prefix to copy a parameter for both type and value
		{tt} -copy_par_post  {ty}  str {df} }  {re} a suffix to copy a parameter for both type and value

		{tt} -prep     {ty}  dict  {df} none   {re} a routine to run before the main task, used for set iteration task input parameters
		{tt} -post     {ty}  dict  {df} none   {re} a routine to run after the main task, used for a summary process
		{tt} -runprep  {ty}  bool  {df} true   {re} run  the prep routine

		{tt} -only for module.routine {ty} dict {df} none {re} settings that only apply to a particular module.routine

		{tt} -prep<<cfg  {ty} str* (-prep) {re} a list of parameters to inherit from the input parameters to the prep process
		{tt} -prep<<main {ty} str* (-prep) {re} a list of parameters to inherit from the main routine to the prep process
		{tt} -main<<prep {ty} str* (-prep) {re} a list of parameters to inherit from the prep process to the main routine

		{tt} -cfg<<cfg   {ty} str* (-prep) {re} Essentially remap the keys in the list 

		{tt} -post<<cfg  {ty} str* (-post) {re} a list of parameters to inherit from the input parameters to the post process
		{tt} -post<<main {ty} str* (-post) {re} a list of parameters to inherit from the post process to the main routine 
		{tt} -post<<prep {ty} str* (-post) {re} a list of parameters to inherit from the post process to the prep process 
		{tt} -autopar    {ty} bool (-prep or -post) {df} true {re} inherit parameters from the main routine automatically 
	"""
def help_text_cmdline():
	return """{hd} ## Parameter usage in the command line: {re}

	All the parameters can be used either in a json file or as a command line
	option: e.g., {tt} {"infile":"filename"} {re} in the json file is equivalent to
	{tt} -infile filename {re} in the command line.  The full content in json
	can be used in the command line through json syntax albeit complex: e.g.,
	{tt} '{"key":value,... }' {re}. 

	There is no automatic type checking, but a few options to enforce numeric or
	list are available.  See below.  When there are multiple instances of a same
	key, the last assignment is used except when it is given after {tt} --with {re}
	parameter: the command line option of the same parameter is used over the same
	of the json file. 

	- Keys without any value mean a boolean variable: e.g.,

		{tt}   -key {re} in command line is equivalent to {tt} {"key": true} {re} in json
		{tt}  -^key {re} is equivalent to {tt} { "key": false} {re}
		{tt} --^key {re} is equivalent to {tt} {"-key": false} {re}
		{tt} -^-key {re} is equivalent to {tt} {"-key": false} {re}

	- Keys starting with {tt} # {re} and {tt} ## {re} will be enforced 
	  as numbers and floats, respectively: e.g.,

		{tt}   -key 1 {re}   is equivalent to {tt} {"key": "1"} {re}
		{tt}  -#key 1 {re}   is equivalent to {tt} {"key": 1} {re}
		{tt}  -#key 1.0 {re} is equivalent to {tt} {"key": 1.0} {re}
		{tt} -##key 1 {re}   is equivalent to {tt} {"key": 1.0} {re}

	  Use {tt} "-enforce_format" {re} key in JSON files which enables formatting without 
	  prefix: e.g., in a JSON file,

		{tt} "-enforce_format" : { 
		        "x" : "float",
		        "y" : "complex",
			  ...
			} {re}

	  Then, the command line option {tt} -x 1 {re} will keep {tt} x {re} as a float instead of str.


	- Keys starting with {tt} * {re} will be treated as list: e.g.,

		{tt}    -key 5,Ab,6.1 {re} is equivalent to {tt} {"key": "5,Ab,6.1"} {re} 
		{tt}   -*key 5,Ab,6.1 {re} is equivalent to {tt} {"key": ["5","Ab","6.1"]} {re} 
		{tt}  -*#key 5,Ab,6.1 {re} is equivalent to {tt} {"key": [5,"Ab",6.1]} {re} 
		{tt} -*##key 5,Ab,6.1 {re} is equivalent to {tt} {"key": [5.0,"Ab",6.1]} {re} 

	- Keys starting with {tt} : {re} will be treated as a nested dict: e.g.,

		{tt} -key1:key2 abc {re} is equivalent to {tt} {"key1": {"key2":"abc"}} {re} 

	- Keys starting with {tt} . {re} will delete the keys or explicitly set them None: e.g.,

		{tt}  -.key {re} is equivalent to {tt} {".key": true} {re}, then this key will be deleted inside python; Used to clean keys after substitution or to remove keys in the other configuration files loaded.
		{tt} -^.key {re} is equivalent to {tt} {".key": false} {re}, and this will set {tt} key = None {re} inside python; Used when needed to explicitly feed {tt} None {re} to input variables.

	Several handy command line options are:

		{tt} --Help  {ty} bool {df} false    {re} display the doc text of the user routine

		{tt} --help  {ty} bool {df} false    {re} display the main section of the help string
		{..}         {ty} str  {df} overview {re} describe the concept and overview
		{..} {..}              {df} json     {re} illustrate features of parameters set in JSON files
		{..} {..}              {df} pars     {re} list parameters used in cjpy
		{..} {..}              {df} cmdline  {re} display features of command line options
		{..} {..}              {df} all      {re} display all the help text

		{tt} --show  {ty} bool {df} false    {re} show information about the parameters and jobs
		{tt}         {ty} list {df}        {re} * {re} indicates exit without calling the routine
		{..} {..}              {df} hidden {re} * {re} show also the hidden variables
		{..} {..}              {df} func   {re} * {re} expected function's parameter
		{..} {..}              {df} input  {re} * {re} parameters prepared
		{..} {..}              {df} feed   {re} * {re} how the parameters are fed to the function
		{..} {..}              {df} output {re}   {re} output of the function
		{..} {..}              {df} job    {re}   {re} job progress
		{..} {..}              {df} files  {re}   {re} input and output file status
		{..} {..}              {df} time   {re}   {re} time
		{..} {..}        e.g., {tt} --show          {re} shows the basic input parameters and exit
		{..} {..}              {tt} --show job,time {re} shows both the job prgress and run time

		{tt} --raw   {ty} bool {df} false {re} show the input parameters in the standard JSON format
		{tt} --with  {ty} list {df} None  {re} json input files used with all other json input files.
		{tt} --relay {ty} bool {df} false {re} when multiple routines are called, their data can be sequentially passed.
		{tt} --parse {ty} bool {df} true  {re} parse *.json files instead of treating them as parameter values.
	"""
def help_text_startup():
	return """{hd} ## Startup, aliasing and native function {re}

	Install the cjpy package using pip, 

		{tt} % pip install cjpy {re}

	then assign an alias for easy use: e.g., in bash,

		{tt} % alias cjpy="python -m cjpy" {re}

	Alternatively, this program can be used without installation: simply
	place {tt} cjson.py {re} in the python path and use

		{tt} % alias cjpy="python cjson.py" {re}

	When using the script "cjpy" (or {tt} __main__,py {re} of the installation), 
	the first line of the script should point to the right place: e.g.,

		{tt} #!/usr/bin/python3 {re}

	For a common parameter configuration, assign an environmental variable
	{tt} CJSON_STARTUP {re} to a JSON file with the common paramters: e.g.,
	in bash,

		{tt} % export CJSON_STARTUP="~/my_startup.json" {re}

	The parameters in this file will be loaded.

	By default, cjpy will attempt passing parameters starting only with alphabets
	to the routine in call, but one can accept the full parameter sets
	(including {tt} -main {re}) by adding an optional parameter in your function:

		{tt} import cjpy.cjson
		def my_routine(..., cfg=cjson.native, ...):
			... {re}

	then, {tt} cfg {re}, which is an {tt} collections.OrderedDict {re}, will
	inherit all the parameters.

	One can also use cjpy inside python or ipython: e.g.,

		{tt} >>> import cjpy.cjson as cj
		>>> cfg = cj.get_parameters(['json file name','options', ...])
		>>> out = cj.execute(cfg) {re}

	"""
def help_text_iteration():
	return """{hd} ## Iterative calling and file search {re}

	A single input JSON file can set up an iterative call to a function.
	Going back to the example {tt} example.my_sum {re} (try {tt} --help
	overview {re}), now we have a new JSON file called {tt} iterations.json {re}:

		{tt} "-main": "example.my_sum",
		"x": 5,
		"y": 7,
		"name": "answer",

		"-iter": ["run A", "run B", "test C"],

		"run A" : { "x": 1,  "y": 2,  },
		"run B" : { "x": 10, "y": 20, },
		"test C": { "x": 10, },

		"-iter~=run": { "name": "ANSWER", }, {re}
	
	This example will run three cases in sequence as specified in [tt} iter {re}.

		{tt} % cjpy iterations.json 
		{ty} ANSWER: 3
		ANSWER: 30
		answer: 17 {re}

	The key {tt} -iter {re} is reserved for setting an iteraction.
	The parameters in the outside or top level will be default, and for each
	case, when a new value is given, the default value will be substituted.
	cjpy will look for parameter names in the list {tt} -iter {re}, and
	substitute variables inside.  Note {tt} "-iter~=run" {re} allows the
	variable substitution for any tasks whose name contains "run". Three such
	expressions are allowed for key matching:

		{tt} "-iter~=run" {re} for any keys containing "run"
		{tt} "-iter==run" {re} for key which is "run"
		{tt} "-iter!=run" {re} for any keys not containing "run"

	To see the progress with runs:

		{tt} % cjpy iterations.json --show job
		{ty} # of jobs: 3 
		job 1/3: example.my_sum run A 
		ANSWER: 3
		job 2/3: example.my_sum run B 
		ANSWER: 30
		job 3/3: example.my_sum test C 
		answer: 17 {re}

	Since input JSON files shouldn't be the place for programming, there is
	no features of loop using "for", "while", or "range", etc. However, when a
	main input is a file (key {tt} infile {re}), a more flexible features are
	available based on matching file parameters (name, mod time, and file size).

	Now imagine a 2nd routine in {tt} example.py":

		{tt} def show_new_name(infile, outfile):
		\"\"\" Come up with a new file name\"\"\" 
		print(infile, ">>", outfile) {re}

	which simply prints out two parameters. With {tt} onefile.json {re}:

		{tt} "-main": "example.show_new_name",
		"infile" : "input.json",
		"outfile": "input_json.txt", {re}

	Then,

		{tt} % cjpy onefile.json
		input.json >> input_json.txt {re}

	Now with {tt} manyfiles.json {re}:

		{tt} "-main": "example.show_new_name",
		"infile" : "(.*).(json)",
		"outfile": "{1}_{2}.txt", {re}

	Then,
		{tt} % cjpy manyfiles.json
		{ty} input.json >> output.txt 
		iterations.json >> iterations_json.txt
		manyfiles.json >> manyfiles_json.txt
		onefile.json >> onefile_json.txt {re}

	The same can be achieved directly in the command line.

		{tt} % cjpy --main example.show_new_name \\
			-infile '(.*).(json)' -outfile '{1}_{2}.txt' {re}
	
	The key {tt} infile {re} is reserved for simple regex based file search
	and followup iteration. The regex can be captured with tags {tt} {1}, {2}, ... {re}
	and used for other keys like {tt} outfile {re} in this example.  Since 
	both {tt} infile and outfile {re} keys are regular variables, we expect 
	the routine in call to receive them. 

	The regex for cjpy is somewhat limited. All the capturable text 
	and regex should be in {tt} ( {re} and {tt} ) {re}. The expression of {tt} '(.*).(json)' {re} 
	will be equivalent to a file search with {tt} *.json {re}.

	In addition to regex, keys such as {tt} -include, -exclude, -keep, -drop,
	-after, -before, -larger & -smaller {re} are reserved for further screening: e.g.,

		{tt} cjpy manyfiles.json -after iterations.json --timekey infile --^parse
		{ty} manyfiles.json >> manyfiles_json.txt
		onefile.json >> onefile_json.txt {re}

	This only works on the input files modified after {tt} iterations.json {re} was
	last modified.  The key {tt} --timekey {re} in the command  line is
	needed to set key {tt} -after {re} is applied to {tt} infile {re} in the
	JSON file (by default it applies to {tt} outfile {re}, but we don't
	generate any actual {tt} outfile {re} in this example).  The key {tt}
	--^parse {re} is needed since cjpy will try to attempt to parse any
	*.json files instead of using it as parameters.

	For more complex screening and the tasks needed after iteractions, use
	keys {tt} -prep & -post {re}. Try {tt} --help decoration {re}.

	"""
def help_text_decoration():
	return """{hd} ## Pre and post processes {re}

	Keys {tt} -prep & -post {re} are used to call a separate routine needed
	to run before and after the main routine, especially when the main
	routine is iterative called. As an OrderedDict, both keys can have their
	own set of variables and called. The main thing to pay attention is how
	to relay the output of these to the input and output of the main tasks. 

	The parameter pass is done through a set of dictionarys, which key is the
	task ID.  The task ID is the name in {tt} -iter {re} or the individual name 
	determined from {tt} infile {re}. The direction of the feed is set by these keys:

		{tt} prep<<cfg   {re} feed these input parameters to the prep process
		{tt} prep<<main  {re} feed these parameters that will be used in the
				main routine to the prep process
		{tt} main<<prep  {re} feed these output from the prep process to the
				main routine 

		{tt} post<<cfg   {re} feed these post parameters to the post process
		{tt} post<<main  {re} feed these outputs from the main routine to the 
				post process
		{tt} post<<prep  {re} feed these outputs from the prep process to the
				post process
		{tt} -autopar    {re} enable inheriting parameters from the main
				routine automatically 

	
	"""
def help_text_logging():
	return """{hd} ## Logging in cjpy {re}

	The automatic logging of each run and a copy of the input parameters are
	enabled through {tt} -logfile {re} and {tt} -hisfile = "_auto_" {re}.
	The log file contains the SHA1 has result of the input parameters, so
	that one can tell the same run has been run or not.

	{tt} 22-04-28 11:27:58 0:00:00.000100 \\
	SHA1:81e37f0fee49f9729aaebe684e9853544664972b example.show_new_name  meco
	 {re}
	When some of the routines are used frequently as a command line tool
	instead of tasks, the logging and copying can be disabled. In general,
	key {tt} --^parse {re} sets the auto log off, which can be set by key
	{tt} -save_cmdline_log {re}.

	"""
def help_text_sequential():
	return """{hd} ## Sequential calling in cjpy {re}

	Multiple jobs can be executed in sequence by simply listing them: e.g.,

		{tt} % cjpy job1.json job2.json ... {re}

	By default, they get executed independently, so this is equivalent to

		{tt} % cjpy job1.json 
		{tt} % cjpy job2.json
		... {re}

	The output of the one job in the first example can be fed to the input
	of the next job. This feature hasn't been tested extensively.

		{tt} % cjpy job1.json -par "a" job2.json -par "b" ... {re}

	Note in this example, {tt} par {re} is set to "a" for job1.json and "b"
	for job2.json

		{tt} % cjpy job1.json -par "a" -par "b" {re}

	In this example, {tt} par {re} is simply set to be "b".

		{tt} % cjpy job1.json job2.json --with job3.json {re}

	In this example, each job is first combined with job3.json and executed, which
	is equivalent to:
	
		{tt} % cjpy job1.json --load job3.json {re}
		{tt} % cjpy job2.json --load job3.json {re}
	"""
def help_text_changes():
	return """{hd} ## Changes {re}

	v0.2.8 2022/05
		- change the name for {tt} -main<<cfg {tt} to {re} -cfg<<cfg {re}
		  since it's essentially remapping the keys. Useful for inheriting -variables
		  to the main or renaming command line options:e.g, 
			"-cfg<<cfg": ["infile", "-recursive << R"],
		  This would make "infile" = "-infile" and "-recursive"="R" so the value of the
		  hidden variable "-infile" can be fed to the main as the parameter "infile".
		  The command line option {tt} --recursive {re} can be invoked now
		  simply by {tt} -R {re}.
		- Automatic assignment of -basedir to -indir is a bit more limited.

	v0.2.7 2022/04
		- clean separation of parameters between "vars" and "-vars"
			- now all the parameter names starting with alphabets are
			  available for user routine by default
			- for this, change {tt} help {re} to {tt} -Help {re}
		- rework keymap function, now internally generated if neccessary
		- now support functions with decorators: 
			- add {tt} -collect_kwpars {re} and {tt} -exclude_kwpars {re}
			  for easy parameter feed to the routine when the exact list of
			  input parameters of user routine is invisible or unclear
		- more features with the show function: 
			- now shows hidden variables in different colors
			- now shows the feed with unknown target parameters
		- update help text
			- add the section "Changes"

	v0.2.6 2022/04
		- simplified runtime function
		- update help text

	v0.2.0 2022/04
		- iteration loop implemented,		
		- now pip installable
		- initial release to pypi

	v0.1.0 2020/05
		- initial writing, 
		- python implementation of cjson IDL batch code

	"""
#----------------------------------------------------------------------------
if __name__ == "__main__":
	""" in bash, use this program in this way
	    alias cjpy='python cjson.py'

	    and then 
	    cjpy json_file [json_files ...] [-other parameters]

	    to run in ipython

	    import cjson as cj

		or

	    import cjpy.cjson as cj

	    cfg=cjson.get_parameters(['cjson file'])
	    out=cjson.execute(cfg)

	    or 

	    out=cjson.go('input args string')

	"""
	go()
	""" """



