from gi.repository import Gtk

from . import hubs
from . import hubscon
from . import users
from . import reqs
from . import overrides

list=hubs.listdef()
sort=Gtk.TreeModelSort.new_with_model(list)
page=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

def clk(b,ix):
	hubs.clk_univ(sort,ix)
def show(nb):
	wn=Gtk.ScrolledWindow()
	wn.set_vexpand(True)
	t=hubs.treedef(sort,clk,rowclk,nb)
	wn.set_child(t)
	page.append(wn)
	b=Gtk.Button.new_with_label("-")
	b.connect('clicked', rem, [t,nb])
	page.append(b)
	return page

def add(a):
	overrides.append(list,a)
def rem(b,gr):
	s=gr[0].get_selection()
	d=s.get_selected()#iter free is in the bindings
	if d[1]:
		hubscon.remcon(gr[1],d[0].get_value(d[1],hubs.COLUMNS.ADDRESS))
		list.remove(d[0].convert_iter_to_child_iter(d[1]))

def rowclk(tree,path,column,nb):
	model=tree.get_model()
	it=model.get_iter(path)
	adr=model.get_value(it,hubs.COLUMNS.ADDRESS)
	resp=reqs.reque("hub.getusers",{"huburl" : adr})
	users.set(nb,adr,resp.split(';'))

def store(d):
	l=[]
	for r in list:
		v=[]
		for i in hubs.COLUMNS:
			v.append(list.get_value(r.iter,i))
		l.append(v)
	d['hubs']=l
def restore(d):
	l=d['hubs']
	for r in l:
		hubscon.addcon(list,r)

def set():
	res=reqs.req("hub.listfulldesc")
	if res:
		for z in list:
			x=list.get_value(z.iter,hubs.COLUMNS.ADDRESS)
			for r in res:
				if r==x:
					list.set_value(z.iter,hubs.COLUMNS.USERS,int(res[r]["users"]))
					list.set_value(z.iter,hubs.COLUMNS.SHARED,res[r]["totalshare preformatted"])
					del res[r]
					break