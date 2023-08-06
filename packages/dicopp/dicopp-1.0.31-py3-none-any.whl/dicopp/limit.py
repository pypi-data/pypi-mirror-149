from gi.repository import GLib,Gtk

from . import reqs
from . import log
from . import sets

start=0
time=Gtk.EntryBuffer(text="0")
limit=Gtk.EntryBuffer(text='1000000000')
timer=0
def timer_get():
	return int(time.get_text())

def open(win):
	t=timer_get()
	if t>0:
		global timer
		timer=GLib.timeout_add_seconds(t*60,callba,win)

def close():
	global timer
	if timer:
		GLib.source_remove(timer)
		timer=0

def callba(win):
	res=reqs.req("show.ratio")
	upB=int(res['up_bytes'])-start
	log.add(upB)
	if upB>int(limit.get_text()):
		print("Upload limit. Window close.")
		global timer
		timer=0
		win.close()
		return False
	return True

def confs():
	f=Gtk.Frame()
	f.set_label("Close program when upload is greater than Value in bytes")
	g=Gtk.Grid()
	lb=Gtk.Label()
	lb.set_halign(Gtk.Align.START)
	lb.set_text("Interval time to verify in minutes (0=disable)")
	g.attach(lb,0,0,1,1)
	en=sets.entries(time)
	g.attach(en,1,0,1,1)
	lb=Gtk.Label()
	lb.set_halign(Gtk.Align.START)
	lb.set_text("Value")
	g.attach(lb,0,1,1,1)
	en=sets.entries(limit)
	g.attach(en,1,1,1,1)
	f.set_child(g)
	return f
def reset(w):
	close()
	open(w)

def store(d):
	d['upload_time']=int(time.get_text())
	d['upload_limit']=int(limit.get_text())

def restore(d):
	time.set_text(str(d['upload_time']),-1)
	limit.set_text(str(d['upload_limit']),-1)