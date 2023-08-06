from gi.repository import Gtk,GLib

from . import reqs
from . import flist
from . import hubs
from . import search
from . import overrides

from enum import IntEnum
class COLUMNS(IntEnum):
	NAME=0
	PATH=1
	DOWNLOADED=2
	SIZE=3
	USERS=4
	STATUS=5

list=Gtk.ListStore(str,str,str,int,str,str)
sort=Gtk.TreeModelSort.new_with_model(list)
page=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
timer=0

def show():
	scroll=Gtk.ScrolledWindow()
	scroll.set_vexpand(True)
	tree=hubs.TreeView(sort)
	hubs.col(tree,'Name',COLUMNS.NAME,clk)
	hubs.col(tree,'Path',COLUMNS.PATH,clk)
	hubs.col(tree,'Downloaded',COLUMNS.DOWNLOADED,clk)
	hubs.col(tree,'Size',COLUMNS.SIZE,clk)
	hubs.col(tree,'Users',COLUMNS.USERS,clk)
	hubs.col(tree,'Status',COLUMNS.STATUS,clk)
	tree.connect("row-activated",clkrow,sort)
	tree.set_activate_on_single_click(True)
	scroll.set_child(tree)
	b=Gtk.Button.new_with_label("-")
	b.connect('clicked', rem, tree)
	page.append(scroll)
	page.append(b)
	return page
def clk(b,ix):
	hubs.clk_univ(sort,ix)
def clkrow(tree,path,column,model):
	it=model.get_iter(path)
	search.start(model.get_value(it,COLUMNS.NAME))

def add(m,it):
	xt=m.get_value(it,flist.COLUMNS.TTH)
	xl=m.get_value(it,flist.COLUMNS.SIZE)
	dn=m.get_value(it,flist.COLUMNS.NAME)
	m="magnet:?xt=urn:tree:tiger:"+xt+"&xl="+str(xl)+"&dn="+dn
	reqs.requ("magnet.add",{"directory" : "","magnet" : m})

def set():
	global timer
	if timer==0:
		if fresh(None):
			timer=GLib.timeout_add_seconds(10,fresh,None)
def fresh(d):
	rows=reqs.req("queue.list")
	for x in list:
		if inspect(x.iter,rows):
			list.remove(x.iter)
	if rows:
		for t in rows:
			r=rows[t]
			overrides.append(list,[r["Filename"],r["Path"],r["Downloaded"],int(r["Size Sort"]),r["Users"],r["Status"]])
		return True
	if len(list)==0:
		global timer
		timer=0
		return False
	return True
def inspect(it,rows):
	if not rows:
		return True
	told=target(list,it)
	for t in rows:
		r=rows[t]
		tnew=r["Path"]+r["Filename"]
		if told==tnew:
			list.set_value(it,COLUMNS.DOWNLOADED,r["Downloaded"])
			list.set_value(it,COLUMNS.SIZE,int(r["Size Sort"]))
			list.set_value(it,COLUMNS.USERS,r["Users"])
			list.set_value(it,COLUMNS.STATUS,r["Status"])
			del rows[t]
			return False
	return True
def close():
	if timer:
		GLib.source_remove(timer)

def target(model,iter):
	return model.get_value(iter,COLUMNS.PATH)+model.get_value(iter,COLUMNS.NAME)
def rem(b,t):
	s=t.get_selection()
	d=s.get_selected()#iter free is in the bindings
	if d[1]:#on tab focus is selecting but on force click is ugly
		tg=target(d[0],d[1])
		reqs.requ("queue.remove",{"target":tg})
		list.remove(d[0].convert_iter_to_child_iter(d[1]))
