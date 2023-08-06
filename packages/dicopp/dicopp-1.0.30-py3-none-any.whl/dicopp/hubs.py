
from gi.repository import Gtk,GLib

import xml.etree.ElementTree as ET
import urllib.request
import math
import threading

listdef=lambda:Gtk.ListStore(str,int,str,str)

from . import base
from . import hubscon
from . import sets
from . import overrides

addr=Gtk.EntryBuffer(text='https://www.te-home.net/?do=hublist&get=hublist.xml')
file=Gtk.EntryBuffer()
lim=Gtk.EntryBuffer(text='200')
labelA="Searching..."
labelB="HubList"
label=Gtk.Label()

list=listdef()
sort=Gtk.TreeModelSort.new_with_model(list)

from enum import IntEnum
class COLUMNS(IntEnum):
	ADDRESS=0
	USERS=1
	COUNTRY=2
	SHARED=3
def treedef(lst,act,clkrow,data):
	tree=TreeView(lst)
	col(tree,'Address',COLUMNS.ADDRESS,act)
	col(tree,'Users',COLUMNS.USERS,act)
	col(tree,'Country',COLUMNS.COUNTRY,act)
	col(tree,'Shared',COLUMNS.SHARED,act)
	tree.connect("row-activated",clkrow,data)
	tree.set_activate_on_single_click(True)
	return tree
def col(tr,tx,ix,act):
	renderer = Gtk.CellRendererText()
	column = Gtk.TreeViewColumn()
	column.set_title(tx)
	column.set_resizable(True)
	column.pack_start(renderer,True)
	column.add_attribute(renderer, "text", ix)
	tr.append_column(column,act,ix)

class TreeView(Gtk.TreeView):
	def __init__(self,model):
		Gtk.TreeView.__init__(self)
		self.set_model(model)
		#self.set_headers_clickable(True)is default
	def append_column(self,col,fn,ix):
		col.connect('clicked',fn,ix)
		col.set_clickable(True)
		Gtk.TreeView.append_column(self,col)

def confs():
	f=Gtk.Frame(label="Hub List")
	g=Gtk.Grid()
	lb=Gtk.Label(halign=Gtk.Align.START,label="File address")
	g.attach(lb,0,0,1,1)
	en=sets.entries(addr)
	g.attach(en,1,0,1,1)
	lb=Gtk.Label(halign=Gtk.Align.START,label="File fallback location")
	g.attach(lb,0,1,1,1)
	g.attach(sets.entries(file),1,1,1,1)
	lb=Gtk.Label(halign=Gtk.Align.START,label="Maximum number of entries")
	g.attach(lb,0,2,1,1)
	en=sets.entries(lim)
	g.attach(en,1,2,1,1)
	f.set_child(g)
	return f
def store(d):
	d['hub_file']=addr.get_text()
	d['hub_file_fallback']=file.get_text()
	d['hub_limit']=lim.get_text()
def restore(d):
	addr.set_text(d['hub_file'],-1)
	file.set_text(d['hub_file_fallback'],-1)
	lim.set_text(d['hub_limit'],-1)

def reset():
	list.clear()
	ini()

def clk_univ(lst,ix):
	n=lst.get_sort_column_id()
	if n[1]!=Gtk.SortType.ASCENDING:
		lst.set_sort_column_id(ix,Gtk.SortType.ASCENDING)
	else:
		lst.set_sort_column_id(ix,Gtk.SortType.DESCENDING)
def clk(b,ix):
	clk_univ(sort,ix)
def show():
	wn=Gtk.ScrolledWindow()
	wn.set_vexpand(True)
	tree=treedef(sort,clk,hubscon.add,sort)
	wn.set_child(tree)
	return wn

def ini():
	label.set_text(labelA)
	global async_th
	async_th = threading.Thread(target=ini_async)
	async_th.start()
def ini_async():
	try:
		urlresult=urllib.request.urlopen(addr.get_text())
	except Exception:
		print("urlopen exception")
		urlresult=None
	GLib.idle_add(ini_main,(urlresult,threading.current_thread()))
def ini_main(mixt):
	urlresult,th=mixt
	if async_th==th:
		try:
			label.set_text(labelB)
			tree = ET.ElementTree(file=urlresult)
			root = tree.getroot()
		except Exception:
			print("hubs list error")
			if file.get_text():
				tree = ET.parse(file.get_text())
				root = tree.getroot()
			else:
				#if the module has never been imported before (== not present in sys.modules), then it is loaded and added to sys.modules.
				from . import hublist
				root = ET.fromstring(hublist.a)
		ini_result(root)
	return False
def ini_result(root):
	try:
		hbs=root.find("Hubs").findall("Hub")
	except Exception:
		return
	mx=min(int(lim.get_text()),len(hbs))
	for i in range(mx):
		attrs=hbs[i].attrib
		if ('Secure' in attrs) and (attrs['Secure']):
			huburl=attrs['Secure']
		elif 'Address' in attrs:
			huburl=attrs['Address']
		else:
			continue
		if ('Users' in attrs) and ('Country' in attrs) and ('Shared' in attrs):
			overrides.append(list,[huburl,int(attrs['Users']),attrs['Country'],convert_size(int(attrs['Shared']))])

def convert_size(size_bytes):
	if size_bytes == 0:
		return "0 B"
	size_name = ("B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB")
	i = math.floor(math.log(size_bytes, 1024))
	p = pow(1024, i)
	s = math.floor(size_bytes / p * 100)/100 # trunc for positiv/negativ
	return "%s %s" % (s, size_name[i])
