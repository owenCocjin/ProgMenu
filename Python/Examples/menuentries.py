from progmenu import MenuEntry
#Menu Entry functions
def noargFunc():
	print("This takes no args!")
	return True

def argFunc(x):
	'''Normally you use this mode to get an arg from the user.
	This is ignored if no arg passed'''
	print(f"You gave me: {x}!")
	return x

def kwargFunc(x=False):
	'''Like mode 1, but has a default if no arg given.'''
	print(f"x is: {x}!")
	return x

#Menu Entries
noarg=MenuEntry("noarg", ['n', "noarg"], noargFunc, 0)
arg=MenuEntry("arg", ['a', "arg"], argFunc, 1)
kwarg=MenuEntry("kwarg", ['k', "kwarg"], kwargFunc, 2)
