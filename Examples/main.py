from progmenu import menu
from menuentries import *
#If you use verbose printing and menu entries, make sure you initialize verbose first!
#Otherwise it will throw errors when parsing strictly!
vprint=menu.verboseSetup(['v', "verbose"])
PARSE=menu.parse(True, strict=True)
print(menu)
print(f"PARSE: {PARSE}")
vprint("This is verbose printing!")
