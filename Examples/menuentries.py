##
## Author:	Owen Cocjin
## Version:	1.6
## Date:	2022.03.05
## Description:	Example menuentries file
## Notes:
##    - Added recurse examples
## Updates:
##    - Added StrictIf parameter
from progmenu import EntryFlag, EntryArg, EntryKeyArg, EntryPositional
#Menu Entry functions
def noargFunc():
	'''Takes no arguments'''
	print("NOARG: This takes no args!")
	return True

def argFunc(x):
	'''Normally you use this mode to get an arg from the user.
	This is ignored if no arg passed'''
	print(f"ARG: You gave me: {x}!")
	return x

def kwargFunc(r, x='Bad'):
	'''Like mode 1, but has a value if no arg given.
	If not called, uses default value (passed in EntryKeyArg)!'''
	print(f"KWARG: What I have is: {x}! Recurse has: {r}")
	return x

def strictFunc():
	'''This flag MUST be called if PARSER is strict'''
	print("STRICT: You have to call me!")
	return True

def strictArgFunc(x):
	'''This takes an arg and is strict'''
	print(f"STRICTARG: You've given me {x}!")
	return x

def recurseFunc(x, y):
	'''This reads arguments from other flags!'''
	print(f"RECURSE: Arg is '{x}' and noarg is '{y}'!")
	return x, y

def argcurseFunc(rec, arg):
	'''This takes an arg AND recurse.
The recurse vars are called first, then the arg var.'''
	print(f"ARGCURSE: The recurse is '{rec}' and your arg is '{arg}'")
	return arg

def helpFunc():
	print("""menu.py [-acfhknrsz] <positional>
Test out ProgMenu!
  -a; --arg=<arg>;      Takes an argument
  -c; --recurse;        Reads results from "arg" and "noarg"
  -f; --stif;           Strict if "noarg" AND "recurse" aren't called
  -h; --help;           Prints this page
  -k; --kwarg;          Argument with default value (deprecated)
  -n; --noarg;          Just a flag; Doesn't take arguments
  -r; --sarg=<arg>;     Takes an argument AND is strict
  -s; --strict;         Must be called
  -z; --argcurse=<arg>; Takes an argument and is recursed
		""")
	return True


#Menu Entries
EntryArg("argcurse", ['z', "argcurse"], argcurseFunc, recurse=["recurse"])
EntryFlag("noarg", ['n', "noarg"], noargFunc, default='Nothing')
EntryArg("arg", ['a', "arg"],argFunc)
EntryKeyArg("kwarg", ['k', "kwarg"], kwargFunc, default="default", recurse=["recurse"])
EntryFlag("recurse", ['c', "recurse"], recurseFunc, recurse=["arg", "noarg"])
EntryPositional("position",0,lambda p:not bool(print(f"POSITIONAL: This is the positional arg @ pos 0: {p}")),strict=True,alt=["alt","noarg"])
EntryPositional("position2",1,lambda p:not bool(print(f"POSITIONAL2: This is the positional arg @ pos 1: {p}")))
EntryArg("alt",['l',"alt"],lambda l: not bool(print(f"""ALT: This will skip positional arg 0, as you gave me: "{l}" """)))

#Uncomment for strict flags
# EntryFlag("strictflag", ['s', "strict"], strictFunc, strict=True)
# EntryArg("strictarg", ['r', "sarg", "strictarg"], strictArgFunc, strict=False)
# EntryArg("strictif",['f',"stif"],lambda f:f,default="Stif default",strictif=["noarg","recurse"])

#This is a keyword flag based on it's name being "help".
#This flag takes precedence over all, and will skip strict checks and immediately exit once done
EntryFlag("help",['h',"help"],helpFunc)
#Uncomment these to test invalid recurses
#EntryFlag("nested", ['d'], lambda _:True, recurse=["looped"])
#EntryFlag("looped", ['l'], lambda _:True, recurse=["toodeep"])
#EntryFlag("toodeep", ['t'], lambda _:True, recurse=["nested"])
