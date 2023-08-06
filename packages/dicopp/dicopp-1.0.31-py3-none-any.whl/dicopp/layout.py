
from gi.repository import Gtk

from . import sets
from . import hubs
from . import hubson
from . import users
from . import usersloc
from . import flist
from . import search
from . import details
from . import dload
from . import com

def show(w):
	bx=Gtk.Box()
	bx.set_orientation(Gtk.Orientation.VERTICAL)
	b=Gtk.Button.new_with_label(chr(0x2699))
	b.connect('clicked', sets.ini, w)
	box=Gtk.Box()
	box.append(b)
	pags=Gtk.Notebook()#scrollable=True is Bus error here,use Tab to select and left right
	e=Gtk.Entry(hexpand=True)
	e.set_placeholder_text('Search...')
	e.connect('activate',search.send,pags)
	box.append(e)
	bx.append(box)
	pags.append_page(hubs.show(),hubs.label)
	pags.append_page(hubson.show(pags),Gtk.Label(label="Hubs"))
	pags.append_page(users.show(pags,w),Gtk.Label(label=users.intro))
	pags.append_page(usersloc.show(pags),Gtk.Label(label="Users"))
	pags.append_page(flist.show(),Gtk.Label(label="FileList"))
	pags.append_page(search.show(),Gtk.Label(label="Search"))
	pags.append_page(details.show(),Gtk.Label(label="Details"))
	pags.append_page(dload.show(),Gtk.Label(label="Downloads"))
	pags.append_page(com.show(),Gtk.Label(label="Command"))
	pags.connect("switch-page",sw,None)
	bx.append(pags)
	w.set_child(bx)

def sw(notebook,page,page_num,d):
	if page==hubson.page:
		hubson.set()
	elif page==usersloc.page:
		usersloc.set()
	elif page==search.page:
		search.set()
	elif page==dload.page:
		dload.set()