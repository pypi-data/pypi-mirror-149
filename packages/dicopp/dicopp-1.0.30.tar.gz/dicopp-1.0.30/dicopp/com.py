from gi.repository import Gtk,Gdk,GLib

import shlex

from . import reqs
from . import sets

mems=[]
pos=0
text=Gtk.TextView(editable=False,wrap_mode=Gtk.WrapMode.WORD_CHAR)
#CheckButton is Bus error here
verbose=Gtk.EntryBuffer()

def show():
	bx=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
	scroll=Gtk.ScrolledWindow(vexpand=True,child=text)
	bx.append(scroll)
	global entry
	entry=Gtk.Entry(hexpand=True,placeholder_text='Command Name0 Value0 ... NameN ValueN')
	global controller
	controller=Gtk.EventControllerKey()
	controller.connect("key-pressed",eve,entry)
	entry.add_controller(controller)
	entry.connect("activate",send,None)
	bx.append(entry)
	return bx
def send(e,d):
	t=e.get_text()
	mem(t)
	n=shlex.split(t)
	c=n[0]
	del n[0]
	d={}
	m=len(n)&(-2)
	for i in range(0,m,2):
		d[n[i]]=n[i+1]
	r=reqs.reque_simple(c,d)
	if not 'result' in r:
		r='Error'
	addtext(r)
	e.get_buffer().delete_text(0,-1)
def addtext(r):
	b=text.get_buffer()
	it=b.get_end_iter()
	b.insert(it,str(r)+'\r\n',-1)
	GLib.idle_add(delay,text)
def delay(t):#this will be after row wrap
	b=t.get_buffer()
	it=b.get_end_iter()
	t.scroll_to_iter(it,0,False,0,0)
	return False
def mem(s):
	if len(mems)>4:
		del mems[0]
	mems.append(s)
	global pos
	pos=len(mems)
def eve(controller,keyval,keycode,state,entry):
	global pos
	if keyval==Gdk.KEY_Up:
		if pos>0:
			pos-=1
			entry.get_buffer().set_text(mems[pos],-1)
			return True
	elif keyval==Gdk.KEY_Down:
		x=len(mems)
		if pos<x:
			pos+=1
			if pos==x:
				entry.get_buffer().delete_text(0,-1)
				return True
			else:
				entry.get_buffer().set_text(mems[pos],-1)
				return True
	return False
def close():
	entry.remove_controller(controller)

def post(r):
	if verbose.get_text():
		addtext(r)

def confs():
	return sets.entry("Verbose (blank=False)",verbose)
def store(d):
	d['verbose']='1' if verbose.get_text() else ''
def restore(d):
	verbose.set_text(d['verbose'],-1)
