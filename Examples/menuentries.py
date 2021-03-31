##
## Author:	Owen Cocjin
## Version:	1.3
## Date:	2021.03.31
## Description:	Example menuentries file
## Notes:
##    - Added recurse examples
from progmenu import EntryFlag, EntryArg, EntryKeyArg
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

def argcurseFunc(arg, rec):
	'''This takes an arg AND recurse'''
	print(f"Your arg is '{arg}' and the recurse is '{rec}'")
	return arg

#Menu Entries
EntryFlag("noarg", ['n', "noarg"], noargFunc)
EntryArg("arg", ['a', "arg"], argFunc)
EntryKeyArg("kwarg", ['k', "kwarg"], kwargFunc)
EntryFlag("strictflag", ['s', "strict"], strictFunc, strict=False)
EntryArg("strictarg", ['r', "sarg", "strictarg"], strictArgFunc, strict=False)
EntryFlag("recurse", ['c', "recurse"], recurseFunc, recurse=["arg", "noarg"])
EntryArg("argcurse", ['z', "argcurse"], argcurseFunc, recurse=["recurse"])
