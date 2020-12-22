from progmenu import menu
from menuentries import *
PARSE=menu.parse(True, strict=True)
vprint=menu.verboseSetup(menu.findFlag(['v', "verbose"]))
print(menu)
print(f"PARSE: {PARSE}")
