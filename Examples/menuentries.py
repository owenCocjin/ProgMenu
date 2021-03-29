from progmenu import EntryFlag, EntryArg, EntryKeyarg
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

#Menu Entries
EntryFlag("noarg", ['n', "noarg"], noargFunc)
EntryArg("arg", ['a', "arg"], argFunc)
EntryKeyarg("kwarg", ['k', "kwarg"], kwargFunc)
