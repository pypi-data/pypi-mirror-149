from . import users
from . import hubs
from . import search
from . import overrides

class detail():
	def __init__(self,a,b,c,d):
		self.nick=a
		self.hub=b
		self.fslots=c
		self.fname=d

def create(r,free):
	return detail(r["Nick"],r["Hub URL"],free,r[search.ext_fn])

def update(r,free,lst,it,col):
	ar=lst.get_value(it,col)
	ar.append(create(r,free))
	lst.set_value(it,col,ar)

from gi.repository import Gtk

from enum import IntEnum
class COLUMNS(IntEnum):
	NICK=0
	HUB=1
	FSLOTS=2
	FNAME=3

list=Gtk.ListStore(str,str,str,str)
sort=Gtk.TreeModelSort.new_with_model(list)

def show():
	scroll=Gtk.ScrolledWindow()
	scroll.set_vexpand(True)
	tree=hubs.TreeView(sort)
	hubs.col(tree,'Nick',COLUMNS.NICK,clk)
	hubs.col(tree,'Hub URL',COLUMNS.HUB,clk)
	hubs.col(tree,'Free Slots',COLUMNS.FSLOTS,clk)
	hubs.col(tree,'Name',COLUMNS.FNAME,clk)
	tree.connect("row-activated",clkrow,sort)
	tree.set_activate_on_single_click(True)
	scroll.set_child(tree)
	bx=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
	b=Gtk.Button.new_with_label(chr(0x1F50D))
	b.connect('clicked', srch, tree)
	bx.append(scroll)
	bx.append(b)
	return bx
def clk(b,ix):
	hubs.clk_univ(sort,ix)
def clkrow(tree,path,column,model):
	it=model.get_iter(path)
	users.ldload(model.get_value(it,COLUMNS.HUB),model.get_value(it,COLUMNS.NICK))

def set(ar):
	list.clear()
	for x in ar:
		overrides.append(list,[x.nick,x.hub,x.fslots,x.fname])

def srch(b,tree):
	s=tree.get_selection()
	d=s.get_selected()#iter free is in the bindings
	if d[1]:
		search.start(d[0].get_value(d[1],COLUMNS.FNAME))
