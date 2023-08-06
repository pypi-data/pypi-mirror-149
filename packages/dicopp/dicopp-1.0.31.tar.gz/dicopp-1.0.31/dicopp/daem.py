
from gi.repository import Gtk
import subprocess
import shlex
import psutil

data=Gtk.EntryBuffer()#text=''

from . import sets
from . import hubscon
from . import reqs

name='eiskaltdcpp-daemon'
instobj=None

def confs():
	global keep
	keep=data.get_text()
	return sets.entry("Daemon parameters",data)
def store(d):
	d['daemon_args']=data.get_text()
def restore(d):
	data.set_text(d['daemon_args'],-1)
def reset():
	if keep!=data.get_text():
		dclose()
		restart()

def restart():
	open()
	hubscon.recon()

def runs():
	for proc in psutil.process_iter():
		try:#/y/x proc.name() = x
			if name==proc.name():
				return proc
		except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
			pass
	return None
def dopen():
	global absent
	absent=runs()==None
	if absent:
		open()
def dclose():
	close(True)
def open():
	seq=shlex.split(data.get_text())
	args=[name]
	for s in seq:
		args.append(s)
	global instobj
	instobj=subprocess.Popen(args)#otherwise, cannot make it works
def close(inter):
	if absent:
		instobj.terminate()
		instobj.wait()
	elif inter:
		if instobj:
			instobj.terminate()
			instobj.wait()
		else:
			p=psutil.Process(runs().pid)
			reqs.req("daemon.stop")
			p.wait()
#-11 (SIGSEGV)
#			instobj.communicate() is same
#			terminate is SIGTERM, SIGINT or daemon.stop is same
#apport is catching first two tries
