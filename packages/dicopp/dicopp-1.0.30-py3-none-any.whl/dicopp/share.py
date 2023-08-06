
from gi.repository import Gtk
import xml.etree.ElementTree as ET

folder=Gtk.EntryBuffer()#text=''

def store(d):
	d['share_folder']=folder.get_text()
def restore(d):
	folder.set_text(d['share_folder'],-1)
#eiskalt want only with trailing /
#this method at reread will work
#with share.add will not work without /
def ini(root):
	se = root.find("Share")
	dr="Directory"
	s = se.find(dr)
	d=folder.get_text()
	if d:
		if s==None:
			s=ET.SubElement(se,dr)
			s.set('Virtual','share')
			s.text=d
			return True
		elif d!=s.text:
			s.text=d
			return True
	elif s!=None:
		se.clear()
		return True
	return False
