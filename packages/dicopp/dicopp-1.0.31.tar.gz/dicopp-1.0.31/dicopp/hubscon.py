
from gi.repository import GLib

import time

from . import hubs
from . import reqs
from . import hubson
from . import users

recons=[]
class reconnect():
	def __init__(self,adr):
		self.adr=adr

def acon(a):
	try:
		reqs.requ("hub.add",{"enc" : "", "huburl" : a})
	except Exception:
		r=reconnect(a)
		r.id=GLib.timeout_add_seconds(3,bcon,r)
		recons.append(r)
def bcon(r):
	acon(r.adr)
	recons.remove(r)
	return False

def add(tree,path,column,model):
	it=model.get_iter(path)#iter free is in the bindings
	d=[]
	for i in hubs.COLUMNS:
		d.append(model.get_value(it,i) if i!=hubs.COLUMNS.USERS else 0)
	addcon(model,d)
def addcon(model,rowlst):
	adr=rowlst[hubs.COLUMNS.ADDRESS]
	lst=hubson.list
	for z in lst:
		x=lst.get_value(z.iter,hubs.COLUMNS.ADDRESS)
		if x==adr:
			return
	acon(adr)
	hubson.add(rowlst)
def remcon(nb,a):
	reqs.requ("hub.del",{"huburl" : a})
	hclose(a)
	users.ifclear(nb,a)

def recon():
	lst=hubson.list
	for z in lst:
		x=lst.get_value(z.iter,hubs.COLUMNS.ADDRESS)
		for a in recons:
			if x==a.adr:
				return
		acon(x)

def close():
	for x in recons:
		GLib.source_remove(x.id)
def hclose(a):
	for x in recons:
		if x.adr==a:
			GLib.source_remove(x.id)
			return
