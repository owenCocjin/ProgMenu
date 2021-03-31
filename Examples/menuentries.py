##
## Author:	Owen Cocjin
## Version:	1.2
## Date:	2021.03.30
## Description:	Example menuentries file
## Notes:
##    - Added 'strict' flags
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

def strictFunc():
	'''This flag MUST be called if PARSER is strict'''
	print("You have to call me!")
	return True

def strictArgFunc(x):
	'''This takes an arg and is strict'''
	print(f"You've given me {x}!")
	return x

def recurseFunc(x, y):
	'''This reads arguments from other flags!'''
	print(f"Arg is '{x}' and noarg is '{y}'!")
	return x, y

#Menu Entries
EntryFlag("noarg", ['n', "noarg"], noargFunc)
EntryArg("arg", ['a', "arg"], argFunc)
EntryKeyarg("kwarg", ['k', "kwarg"], kwargFunc)
EntryFlag("strictflag", ['s', "strict"], strictFunc, strict=False)
EntryArg("strictarg", ['r', "sarg", "strictarg"], strictArgFunc, strict=False)
EntryFlag("recurse", ['c', "recurse"], recurseFunc, recurse=["arg", "noarg"])
