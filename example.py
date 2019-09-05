#!/usr/bin/python3

from menu import *
import menuEntries
menu=Menu()  #Set a Menu object
menu.parse(True)  #Run any valid flags that are passed
Menu.setVerbose(menu.findFlag(['v', "verbose"]))

print("Hello, World!")
vprint(f"Flags:  \t{menu.getFlags()}")
vprint(f"Assigned:\t{menu.getAssigned()}")
vprint(f"Args:    \t{menu.getArgs()}")
