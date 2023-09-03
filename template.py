#!/usr/bin/python3
#
#This template is used for single-file scripts.
#It's much cleaner to have all your entries in a dedicated module where you'd just import that module into main, but for quick scripts this will work
#

#Make sure you have the lib installed in this directory, or have a symlink in this directory that points to the ProgMenu
from progmenu import MENU,EntryArg,EntryFlag,EntryPositional

#Do whatever you need in this main!
def main():
	pass



#Add your entry functions here if you're using any
def helpFunc():
	print("""main.py
This is a template. Make sure to change this help page!
  -h; --help; Prints this page""")
	return True

#Add your entries here
EntryFlag("help",['h',"help"],helpFunc)



#This gets called when you run this script
if __name__=="__main__":
	PARSER=MENU.parse(True,strict=True)
	main()