# ProgMenu

> A lil library to help with cmd line flags and stuff (stuff being verbose printing)

***

## Installation

- Clone or download into a folder
- Move progMenu.py into the working directory of a project

OR

- Copy Python/progmenu.py to your Python path (probably /usr/lib/pythonX.X ; Check your path with `python -c "import sys; print(sys.path)"`)

<br/>

## Usage

### Testing

Run this code as a script to test if it's working:

```
from progmenu import printFAA
printFAA()
#Prints all the passed flags, assigned, and args in that order
```

- A *flag* is: `-f or --flag`
- An *assigned* is a flag with an associated arg: `-s 12` or `--seed=12`
- An *arg* is pretty much anything else: `$ cmd -s <arg> <lonelyArg>`
- <u>**NOTE:**</u> Multiple flags passed via one tick will be treated as 2 separate flags, with the last flag getting any assigns (ex. `-fh 'Hello'` is the same as `-f -h 'Hello'`)

<br/>

### Main Usage
> This is a super basic example! Checkout the Examples in the Python directory for more options

In the main file:
```
from progmenu import MENU
from menuentries import *
PARSER=MENU.parse(True)  #True means run the functions instead of just returning True/None if the entry was called.
print(f"PARSER: {PARSER}")  #Just so you can see what PARSER is. It's a dictionary of the entry names and what they returned (if called in the cmd line).
```

In another file containing the entries (in this case named `menuentries.py`):
```
from progmenu import MenuEntry
def aFunc():
	print("This is an entry function!")
	return True

#This doesn't/shouldn't be saved to a variable as this may cause collisions. When an Entry class is created it adds itself to a class-wide list!
EntryFlag("entryName", ['f', "flag"], aFunc)  #help(MenuEntry) for more details)
```

Now when you run the main file without using `f` or `flag` as a flag, nothing will happen. But if you do, it prints "This is an entry function!"

<br/>

### Verbose Printing

To use verbose printing, simply print like normal, but use the function "vprint" instead of "print" (And make sure the verbose flag was set).
To use verbose printing in other files, you MUST make sure you import vprint in each file (you don't need to set verbosity anywhere other than main), otherwise Python will complain that vprint wasn't defined.

> Currently, there is an issue where in order to politely use verbose and menu entries, you must setup verbose __BEFORE__ parsing strictly!

Ex:

#### Using main:
- In main file (main.py):
```
from progmenu import MENU
vprint=MENU.verboseSetup(['v' "verbose"]) #menu.findFlag() returns True if any passed flags were found, meaning you can hardcode verbosity with: menu.verboseSetup(True)
print("This is without verbose!")
vprint("This is WITH verbose!")
```
- Now run the file with `-v` or `--verbose`:
```
$ python ./main.py
This is without verbose!
$python ./main.py -v
This is without verbose!
This is WITH verbose!
```

#### Using external files:
> TLDR; You only need to import verbosity in the files where you're calling it literally

- In main file (main.py):
```
import verboseTest
verboseTest.testFunc()
```
- In another file (verboseTest.py):
```
from progmenu import MENU  #MENU is required to catch flags
vprint=MENU.verboseSetup(['v', "verbose"])  #menu.findFlag() returns True if any passed flags were found, meaning you can hardcode verbosity with: menu.verboseSetup(True)
def testFunc():
	'''Prints normally and with verbose'''
	print("This is a normal print from testFunc!")
	vprint("This is verbose print from testFunc!")
```
- Now when the main file is run without '-v', only the normal print will work. When it's run with '-v', both print statements will print:
```
$ python main.py
This is a normal print from testFunc!
$ python main.py -v
This is a normal print from testFunc!
This is verbose print from testFunc!
```
