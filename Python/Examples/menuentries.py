from progmenu import MenuEntry, EntryFlag, EntryArg, EntryKeyarg
#Menu Entry functions
def noargFunc():
	'''Takes no arguments'''
	print("This takes no args!")
	return True

def argFunc(x):
	'''Normally you use this mode to get an arg from the user.
	This is ignored if no arg passed'''
	print(f"You gave me: {x}!")
	return x

def kwargFunc(x='Bad'):
	'''Like mode 1, but has a default if no arg given'''
	print(f"What I have is: {x}!")
	return x

def genericFunc():
	'''Example of using MenuEntry class'''
	print("This is an example of using MenuEntry class!")
	return 'BigValue'

#Menu Entries
noarg=EntryFlag("noarg", ['n', "noarg"], noargFunc)
arg=EntryArg("arg", ['a', "arg"], argFunc)
kwarg=EntryKeyarg("kwarg", ['k', "kwarg"], kwargFunc)
generic=MenuEntry("generic", ['g', "generic", '1'], genericFunc, mode=0)  #MenuEntry class modes can be define
