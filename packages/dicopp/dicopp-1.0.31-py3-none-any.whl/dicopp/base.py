
from . import limit
from . import log
from . import stor2
from . import hubs
from . import hubson
from . import search
from . import daem
from . import com

import json
from gi.repository import Gdk

import appdirs
import os.path
import pathlib
def get_client_dir():
	return pathlib.Path(appdirs.user_config_dir('dicopp'))
get_client_dir().mkdir(exist_ok=True)
def get_client():
	return os.path.join(get_client_dir(),'config.json')

def write(win):
	d={}
	dim=win.get_default_size()
	d['width']=dim.width
	d['height']=dim.height
	d['max']=win.is_maximized()
	d['min']=win.get_surface().get_state()&Gdk.ToplevelState.MINIMIZED
	limit.store(d)
	log.store(d)
	stor2.store(d)
	hubs.store(d)
	hubson.store(d)
	search.store(d)
	daem.store(d)
	com.store(d)
	with open(get_client(), "w") as write_file:
		json.dump(d, write_file)

def read(win):
	try:
		with open(get_client()) as f:
			d=json.load(f)
			win.set_default_size(d['width'],d['height'])
			if(d['max']):
				win.maximize()
			if(d['min']):
				win.minimize()
			limit.restore(d)
			log.restore(d)
			stor2.restore(d)
			hubs.restore(d)
			search.restore(d)
			daem.restore(d)
			com.restore(d)
			return d
	except Exception:
		return None
def read2(d):
	if d:
		hubson.restore(d)
