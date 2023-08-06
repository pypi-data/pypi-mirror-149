from gi.repository import Gtk

from . import search
from . import sets
from . import overrides

list=Gtk.ListStore(str)

def store(d):
	add()
	a=[]
	for x in list:
		a.append(list.get_value(x.iter,0))
	d['search_extensions']=a
def restore(d):
	for x in d['search_extensions']:
		ad([x])
	search.extensions.set_text(d['search_extensions'][0],-1)
def confs(en,win):
	bx=Gtk.Box()
	b=Gtk.Button.new_with_label("Change")
	b.connect('clicked', sel, win)
	bx.append(en)
	bx.append(b)
	return bx

def ad(x):
	overrides.append(list,x)
def add():
	c=search.extensions.get_text()
	for x in list:
		if c==list.get_value(x.iter,0):
			return
	ad([c])

def sel(b,win):
	add()
	tree=Gtk.TreeView.new_with_model(list)
	renderer = Gtk.CellRendererText()
	column = Gtk.TreeViewColumn()
	column.pack_start(renderer,True)
	column.add_attribute(renderer, "text", 0)
	tree.append_column(column)
	d=sets.dial("Extensions",win,reset,tree)
	d.add_button("_Set",Gtk.ResponseType.YES)
	d.add_button("_Delete",Gtk.ResponseType.NO)
	scroll=Gtk.ScrolledWindow(hexpand=True,vexpand=True)
	scroll.set_child(tree)
	d.get_content_area().append(scroll)
	d.show()

def reset(d,r,t):
	if r!=Gtk.ResponseType.DELETE_EVENT:
		x=t.get_selection()
		s=x.get_selected()
		if s[1]:
			if r==Gtk.ResponseType.YES:
				s[0].move_after(s[1],None)
				search.extensions.set_text(s[0].get_value(s[1],0),-1)
				d.destroy()
			elif r==Gtk.ResponseType.NO:
				s[0].remove(s[1])