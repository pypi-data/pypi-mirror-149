
def append(list,values):
	values,columns=list._convert_row(values)
	try:
		list.insert_with_values(-1,columns,values)
	except AttributeError:#support gtk-4.0
		list.insert_with_valuesv(-1,columns,values)
