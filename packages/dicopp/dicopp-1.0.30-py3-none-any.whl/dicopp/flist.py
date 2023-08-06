from gi.repository import Gtk,GObject

from time import sleep

from enum import IntEnum
class COLUMNS(IntEnum):
	NAME=0
	SIZE=1
	TTH=2
listcols="str,GObject.TYPE_INT64,str"

from . import reqs
from . import hubs
from . import overrides

name=Gtk.Label()
folder=Gtk.Label()
bx=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
list=eval("Gtk.ListStore("+listcols+")")
sort=Gtk.TreeModelSort.new_with_model(list)
sep="\\"

def cols(tree,act):
	hubs.col(tree,'Name',COLUMNS.NAME,act)
	hubs.col(tree,'Size',COLUMNS.SIZE,act)
	hubs.col(tree,'TTH',COLUMNS.TTH,act)
def show():
	scroll=Gtk.ScrolledWindow()
	scroll.set_vexpand(True)
	tree=hubs.TreeView(sort)
	cols(tree,clk)
	tree.connect("row-activated",clkrow,sort)
	tree.set_activate_on_single_click(True)
	scroll.set_child(tree)
	bx.append(name)
	bx.append(folder)
	back=Gtk.Button.new_with_label('..')
	back.connect('clicked',backing,None)
	bx.append(back)
	bx.append(scroll)
	return bx
def clk(b,ix):
	hubs.clk_univ(sort,ix)
def clkrow(tree,path,column,model):
	it=model.get_iter(path)
	fpath=folder.get_text()+model.get_value(it,COLUMNS.NAME)
	if not model.get_value(it,COLUMNS.TTH):
		fshow(name.get_text(),fpath+sep)
	else:
		reqs.requ("list.downloadfile",{"downloadto" : "","filelist" : name.get_text(),"target" : fpath})

def set(nb,nm):
	name.set_text(nm)
	z=nm.split(".")
	nb.set_tab_label_text(bx,z[0])
	reqs.req("list.closeall")
	reqs.requ("list.open",{"filelist" : nm})
	fshow(nm,'')

def backing(b,d):
	s=folder.get_text()
	if not s:
		return
	p=s.rfind(sep,0,-len(sep))
	if p!=-1:
		fshow(name.get_text(),s[:p+len(sep)])
	else:
		fshow(name.get_text(),'')
def fshow(flist,s):
	#wait phisical read,listopened was not a solution
	for i in range(0,5):
		a=reqs.reque("list.lsdir",{"directory" : s,"filelist" : flist})
		if a:
			folder.set_text(s)
			list.clear()
			for x in a:
				e=a[x]
				if "TTH" in e:
					t=e['TTH']
				else:
					t=''
				overrides.append(list,[x,int(e['Size']),t])
			break
		else:
			sleep(1)
