from gi.repository import Gtk

from . import hubs
from . import reqs
from . import overrides
from . import userinfo

listdef=lambda:Gtk.ListStore(str)

list=listdef()
page=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
intro="UserList"

def show(nb,win):
	scroll=Gtk.ScrolledWindow()
	sort=Gtk.TreeModelSort.new_with_model(list)
	t=show_univ(nb,scroll,sort,clkrow)
	b=Gtk.Button.new_with_label(chr(0x24D8))
	b.connect('clicked', info, [t,nb,win])
	page.append(scroll)
	page.append(b)
	return page
def show_univ(nb,sc,srt,cl_rw):
	sc.set_vexpand(True)
	t=hubs.TreeView(srt)
	renderer = Gtk.CellRendererText()
	column = Gtk.TreeViewColumn()
	column.set_title("Name")
	column.pack_start(renderer,True)
	column.add_attribute(renderer, "text", 0)
	t.append_column(column, clk, srt)
	t.connect("row-activated",cl_rw,nb)
	t.set_activate_on_single_click(True)
	sc.set_child(t)
	return t
def clk(b,d):
	hubs.clk_univ(d,0)
def clkrow(t,p,c,b):
	m=t.get_model()
	user=m.get_value(m.get_iter(p),0)
	adr=b.get_tab_label_text(page)
	ldload(adr,user)

def ldload(adr,user):
	reqs.requ("list.download",{"huburl" : adr, "nick" : user})

def clear(nb,adr):
	list.clear()
	nb.set_tab_label_text(page,adr)
def ifclear(nb,a):
	if(nb.get_tab_label_text(page)==a):
		clear(nb,intro)

def set(nb,adr,lst):
	clear(nb,adr)
	for x in lst:
		overrides.append(list,[x])

def info(b,triple):
	s=triple[0].get_selection()
	model,iter=s.get_selected()
	if iter:
		userinfo.ini(triple[1].get_tab_label_text(page),model.get_value(iter,0),triple[2])
