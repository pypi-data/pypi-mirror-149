
from . import stor2
from . import nick

import os.path

a='''<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<DCPlusPlus>
	<Settings>
		<Nick type="string">'''
b='''</Nick>
		<ConfigVersion type="string">2.3.0</ConfigVersion>
		<Slots type="int">3</Slots>
		<TotalDownload type="int64">0</TotalDownload>
		<TotalUpload type="int64">0</TotalUpload>
	</Settings>
	<Share />
</DCPlusPlus>'''

def ini():
	f=stor2.get_file()
	if os.path.isfile(f)==False:
		d=os.path.dirname(f)
		import pathlib
		pathlib.Path(d).mkdir(exist_ok=True)#parents=True
		#
		import xml.etree.ElementTree as ET
		s=a+nick.name.get_text()+b
		e=ET.fromstring(s)
		t = ET.ElementTree(element=e)
		t.write(f)
