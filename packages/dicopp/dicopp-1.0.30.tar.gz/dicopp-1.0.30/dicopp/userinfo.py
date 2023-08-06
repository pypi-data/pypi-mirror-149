
from gi.repository import Gtk

from . import sets,reqs

def ini(hub,user,win):
	r=reqs.reque("hub.getuserinfo",{"nick":user,"huburl":hub})
	if r:
		d=sets.dial(user,win,done,None)
		d.add_button("_OK",Gtk.ResponseType.NONE)
		bx=Gtk.Grid()
		bx.set_column_spacing(5)
		y=0
		for k in r:
			bx.attach(Gtk.Label(label=k,halign=Gtk.Align.START),0,y,1,1)
			y+=1
		y=0
		for v in r.values():
			bx.attach(Gtk.Label(label=v,halign=Gtk.Align.START),1,y,1,1)
			y+=1
		box=d.get_content_area()
		box.append(Gtk.ScrolledWindow(child=bx,hexpand=True,vexpand=True))
		d.show()

def done(w,r,d):
	#if r==Gtk.ResponseType.NONE:
	w.destroy()#ok with or without at X button
