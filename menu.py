#!/usr/bin/python3
'''
## Author:	Owen Cocjin
## Version:	2.6
## Date:	04/09/19
## Description:	Process cmd line arguments & holds common variables
## Notes:
##	- Changed VERBOSE from a global variable to a class var for Menu
##	- Fixed parsing settings

Uncomment and copy this into the main file:
	>
	from menu import *
	menu=Menu()  #Set a Menu object
	Menu.setVerbose(menu.findFlag(['v', "verbose"]))  #Set verbosity setting
	<

For menu entries, it's easiest to make a seperate python file (menuEntries.py)\
and fill that with Entry objects. Uncomment and copy this into menuEntries.py:
	> from menu import MenuEntry <

And this to the main file:
	> import menuEntries <

For all the functionality (i.e. verbose & entries) uncomment and copy this into
the main file
	>
	from menu import *
	import menuEntries
	menu=Menu()  #Set a Menu object
	menu.parse(True)  #Run any valid flags that are passed
	Menu.setVerbose(menu.findFlag(['v', "verbose"]))  #Set verbosity setting
	<
'''
import sys  #Required!
#--------User's imports--------#
#import usershit

'''-------------------+
|        SETUP        |
+-------------------'''
def vprint(toPrint):
	'''Only print if VERBOSE is True'''
	if Menu.VERBOSE:
		print(toPrint)
		return 0
	else:
		return 1

class Menu():
	menuEntries=[]  #Class-wide list of all menu entries
	VERBOSE=False  #Class-wide verbosity setting

	def __init__(self):
		#--------Variables--------#
		#Required!
		self.flags=[]
		self.assigned={}
		self.args=[]

		#--------Process sys.argv--------#
		#Find flags in sys.argv and save them
		menu_args=sys.argv[1:]  #Remove first arg
		for i, n in enumerate(menu_args):
			#If current arg starts with '-', it's a flag
			if n[0]=='-':
				#If current arg starts with '--', its it's own flag
				if n[1]=='-':
					if '=' in n:
						#If there is an equal sign, split it and add to assigned, args, and flags
						rec=n[2:].split('=')
						self.flags.append(rec[0])
						self.assigned[rec[0]]=rec[1]
						self.args.append(rec[1])
					else:
						#Add the whole flag
						self.flags.append(n[2:])
				else:
					#Count each individual char as a flag and add it to the list
					for j in n[1:]:
						self.flags.append(j)

					#If the next arg is NOT a flag, add it
					if menu_args[i+1][0]!='-':
						self.assigned[n[-1]]=menu_args[i+1]

			else:
				#counts as an argument
				self.args.append(n)

	def __str__(self):
		return f"flags:\t\t{self.flags}\nassigned:\t{self.assigned}\nargs:\t\t{self.args}"

#Parse
	def parse(self, p=False, *, toFind=None, dontFind=None):
		'''Returns any functions associated with a flags/assigned/args.
		Note: parse() does NOT run any entries.
		- if p is True, run all called flags, else just return a list of valid flags
		- toFind is of type "list", containing MenuEntry objects
		- dontFind is of type "list", containing strings of flags to avoid'''

		toReturn=[]

		def parseEntry(e):
			'''Checks if e (of type MenuEntry) was set. Run it if it is found'''
			if e.getFlg()==0:
				if any(i in self.flags for i in e.getLabels()):
					e()

			elif e.getFlg()==1:
				for i in self.assigned:
					if i in e.getLabels():
						e(self.assigned[i])

			elif e.getFlg()==2:
				if any(i in self.args for i in e.getLabels()):
					e()

		#Populate toFind with all menuEntries if blank
		if not toFind:
			toFind=[i for i in Menu.menuEntries]

		#If dontFind has something, loop through toFind and add anything
		#that doesn't match with dontFind to toReturn
		if dontFind:
			#Loop through toFind, if there's a match with dontFind, remove it
			for i, e in enumerate(toFind):
				if any(i in dontFind for i in e.getLabels()):
					#if any element in dontFind is in the current label, remove it
					continue
				else:
					toReturn.append(e)

		#Else if dontFind is empty, add everything in toFind
		elif not dontFind:
			[toReturn.append(i) for i in toFind]

		#Check if p is set and run all called flags if it is
		if not p:
			return toReturn
		elif p:
			[parseEntry(e) for e in toReturn]

	@classmethod
	def getEntries(cls):
		toReturn=''
		for i in Menu.menuEntries:
			toReturn+=f"{i}\n"
		return toReturn

	@classmethod
	def getMenuEntries(cls):
		return Menu.menuEntries

	@classmethod
	def setVerbose(cls, verb):
		'''Sets verbosity. This isn't in the Menu class so the user can set the verbose\
		command to be whatever through setVerbose(main.findFlag('<whatever>'))'''
		Menu.VERBOSE=True if verb else False
		return Menu.VERBOSE

#Flags
	def findFlag(self, toFind):
		'''Returns True if any arg is a flag.
		toFind is of type "list"'''
		for i in toFind:
			if i in self.flags:
				return True
		return False

	def getFlags(self):
		return self.flags

	def addFlag(self, new):
		'''Appends a new flag'''
		self.flags.append(new)

	def removeFlag(self, old):
		'''Removes the first occurence of a given flag'''
		try:
			self.flags.remove(old)
		except:
			print(f"[|X]Error: {old} flag not found!")

#Assigned
	def findAssigned(self, toFind):
		'''Returns True is any arg is assigned.
		toFind is of type "list"'''
		for i in toFind:
			if i in self.assigned:
				return True
		return False

	def getAssigned(self):
		return self.assigned

	def sgetAssigned(self, spec):
		'''Get a specific value'''
		try:
			return self.assigned[spec]
		except:
			return None

	def setAssigned(self, key, value):
		'''Adds a key:value pair to assigned.
		Can also change the value of key.'''
		self.assigned[key]=value

	def removeAssigned(self, key):
		'''Remove a key:value pair, distinguished by the key only'''
		try:
			del(self.assigned[key])
		except KeyError:
			print(f"[|X]Error: {key} assigned not found!")
		except:
			print("[|X]Error.removeAssigned(): Other error!")

#Args
	def findArg(self, toFind):
		'''Returns True is any arg is an arg.
		toFind is of type "list"'''
		for i in toFind:
			if i in self.args:
				return True
		return False

	def getArgs(self):
		return self.args

	def addArg(self, new):
		'''Adds a value to args'''
		self.args.append(new)

	def removeArg(self, old):
		'''Removes an the first occurence of an argument'''
		try:
			self.args.remove(old)
		except:
			print(f"[|X]Error: {old} arg not found!")

	def stats(self):
		'''Return the values of flags, assigned, and args'''
		return self.flags, self.assigned, self.args

	def isEmpty(self):
		'''Returns a tuple of True/False, depending on if menu vars are empty.
		Returns in order of: Flags, Assigned, Args
		- True if it is empty
		- False if it contains something'''
		isFlags=True if len(self.flags)==0 else False
		isAssigned=True if len(self.assigned)==0 else False
		isArgs=True if len(self.args)==0 else False
		return isFlags, isAssigned, isArgs

class MenuEntry():
	'''Menu entry class.
	flg status:
	- 0=flags
	- 1=assigned
	- 2=args'''
	def __init__(self, labels, function, flg=0):
		self.labels=labels  #Labels being a list of the flags/args
		self.function=function
		self.flg=flg
		Menu.menuEntries.append(self)

	def __str__(self):
		return f"{self.labels}\t{self.function}"

	def __call__(self, *args, **kwargs):
		self.function(*args, **kwargs)
		return 0

	def run(self, *args, **kwargs):
		self.function(*args, **kwargs)
		return 0

	def getLabels(self):
		return self.labels

	def addLabel(self, new):
		self.labels.append(new)

	def removeLabel(self, old):
		self.labels.remove(old)

	def setFunction(self, new):
		self.function=new

	def getFlg(self):
		return self.flg

	def setFlg(self, new):
		self.flg=new

'''----------------+
|    USER SPACE    |
+----------------'''
#User's functions

#User's Variables!
