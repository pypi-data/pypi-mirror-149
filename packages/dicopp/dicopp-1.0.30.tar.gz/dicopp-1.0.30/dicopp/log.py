
from gi.repository import Gtk

from . import sets

import subprocess

file=Gtk.EntryBuffer()#text=''
end=Gtk.EntryBuffer()#text=''
f=None

def confs():
	f=Gtk.Frame(label="Log file")
	g=Gtk.Grid()
	lb=Gtk.Label(halign=Gtk.Align.START,label="Location")
	g.attach(lb,0,0,1,1)
	en=sets.entries(file)
	g.attach(en,1,0,1,1)
	lb=Gtk.Label(halign=Gtk.Align.START,label="External command when closing")
	g.attach(lb,0,1,1,1)
	en=sets.entries(end)
	g.attach(en,1,1,1,1)
	f.set_child(g)
	return f
def store(d):
	d['log_file']=finish()
	d['log_end']=end.get_text()
def restore(d):
	file.set_text(d['log_file'],-1)
	end.set_text(d['log_end'],-1)

def ini():
	log=file.get_text()
	if len(log)>0:
		global f
		f=open(log,"w")

def add(obj):
	if f:
		f.write(obj.__str__()+"\n")
		f.flush()

def finish():
	global f
	if f:
		txt=end.get_text()
		if txt:
			z=subprocess.run(txt,capture_output=True,text=True)
			f.write(z.stdout)
		f.close()
		f=None
	return file.get_text()

def reset():
	d=finish()
	if len(d)>0:
		global f
		f=open(d,"a")
