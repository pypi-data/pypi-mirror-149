
from gi.repository import Gtk

from . import nick

passive=Gtk.EntryBuffer()
def store(d):
	d['passive']='1' if passive.get_text() else ''
def restore(d):
	passive.set_text(d['passive'],-1)

def ini(se):
	z='IncomingConnections'
	if passive.get_text():
		return nick.see(se,z,'int',"3")
	s = se.find(z)
	if s==None:
		return False
	se.remove(s)
	return True
