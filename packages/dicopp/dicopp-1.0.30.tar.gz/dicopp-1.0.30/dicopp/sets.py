
from gi.repository import Gtk

from . import limit
from . import log
from . import stor2
from . import nick
from . import hubs
from . import search
from . import daem
from . import com

class entries(Gtk.Entry):
	def __init__(self,bf):
		Gtk.Entry.__init__(self,buffer=bf,hexpand=True)
		#when write quick, hexpand only at first
def dial(t,win,f,data):
	d=Gtk.Dialog(title=t,transient_for=win)
	d.set_modal(True)
	d.connect("response",f,data)
	if win.is_maximized():
		d.maximize()
	else:
		dim=win.get_default_size()
		d.set_default_size(dim.width,dim.height)
	return d
def ini(b,win):
	d=dial("Settings",win,reset,win)
	d.add_button("_OK",Gtk.ResponseType.NONE)
	box=d.get_content_area()
	bx=Gtk.Box()
	bx.set_orientation(Gtk.Orientation.VERTICAL)
	bx.append(limit.confs())
	bx.append(log.confs())
	bx.append(stor2.confs())
	bx.append(hubs.confs())
	bx.append(search.confs(d))
	bx.append(daem.confs())
	bx.append(com.confs())
	box.append(Gtk.ScrolledWindow(child=bx,vexpand=True))
	d.show()
def reset(d,r,w):
	limit.reset(w)
	log.reset()
	stor2.ini()
	wasreset=nick.ini(True)
	hubs.reset()
	search.reset()
	if not wasreset:
		daem.reset()
	d.destroy()#at X can be omitted

def entry(txt,buf):
	bx=Gtk.Box()
	lb=Gtk.Label()
	lb.set_halign(Gtk.Align.START)
	lb.set_text(txt)
	bx.append(lb)
	en=Gtk.Entry.new_with_buffer(buf)
	en.set_hexpand(True)
	bx.append(en)
	return bx
