#!/usr/bin/python3

from menu import *
import menuEntries
menu=Menu()  #Set a Menu object
blacklist=['w']
whitelist=menuEntries.a
menu.parse(True)
#[i() for i in menu.parse(True) if i]
#[i() for i in menu.parse(toFind=blacklist) if i ]  #Runs any function associated with any flag
Menu.setVerbose(menu.findFlag(['v', "verbose"]))
