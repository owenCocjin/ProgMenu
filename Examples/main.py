from progmenu import MENU
from menuentries import *
#If you use verbose printing and menu entries, make sure you initialize verbose first!
#Otherwise it will throw errors when parsing strictly!
vprint=MENU.verboseSetup(['v', "verbose"])
PARSE=MENU.parse(True, strict=True)
print(MENU)
print(f"PARSE: {PARSE}")
vprint("This is verbose printing!")
