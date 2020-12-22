from progmenu import menu
from menuentries import *
PARSE=menu.parse(True)
vprint=menu.verboseSetup(menu.findFlag(['v', "verbose"]))
print(f"PARSE: {PARSE}")
