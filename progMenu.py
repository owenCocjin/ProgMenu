#!/usr/bin/python3
'''
## Author:	Owen Cocjin
## Version:	2.9
## Date:	21/12/19
## Description:	Process cmd line arguments & holds common variables
## Notes:


Uncomment and copy this into the main file:
	>
	from menu import *
	menu=ProgMenu()  #Set a ProgMenu object
	vprint.setVerbose(menu.findFlag(['v', "verbose"]))  #Set verbosity setting
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
	menu=ProgMenu()  #Set a ProgMenu object
	PARSER=menu.parse(True)  #Run any valid flags that are passed and save them
	vprint.setVerbose(menu.findFlag(['v', "verbose"]))  #Set verbosity setting
	<
'''
import sys  #Required!
#--------User's imports--------#
#import user-required libraries

'''-------------------+
|        SETUP        |
+-------------------'''
class vprint():
    '''Verbose printing.'''
    VERBOSE=False
    def __init__(self, *args, **kwargs):
        if vprint.VERBOSE:
            print(*args, **kwargs)

    @classmethod
    def getVerbose(cls):
        '''Return current VERBOSE value (True means will print).'''
        return cls.VERBOSE

    @classmethod
    def setVerbose(cls, new):
        '''Set VERBOSE value (True means will print).
Common code used to enable -v option(ensure menu was imported from progMenu!):
    vprint.setVerbose(menu.findFlag(['v', "verbose"]))'''
        cls.VERBOSE=True if new else False

class ProgMenu():
	menuEntries=[]  #Class-wide list of all menu entries

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

					try:
						#If the next arg is NOT a flag, add it
						if menu_args[i+1][0]!='-':
							self.assigned[n[-1]]=menu_args[i+1]
					except:
						pass

			else:
				#counts as an argument
				self.args.append(n)

	def __str__(self):
		return f"flags:\t\t{self.flags}\nassigned:\t{self.assigned}\nargs:\t\t{self.args}"

	@classmethod
	def listNames(cls):
		'''Returns a list of names of entries in order of creation.'''
		return [i.getName() for i in ProgMenu.menuEntries]

	@classmethod
	def printEntries(cls):
		'''Prints entries'''
		[print(i) for i in ProgMenu.menuEntries]

	@classmethod
	def getMenuEntries(cls):
		return ProgMenu.menuEntries

	@classmethod
	def sgetMenuEntry(cls, e):
		'''Return specific menu entry <e=name>'''
		for i in cls.menuEntries:
			if i.getName()==e:
				return i
		return False

	@classmethod
	def getEntryNames(cls):
		return [i.getName() for i in ProgMenu.menuEntries]

#Parse
	def parse(self, p=False, *, toFind=None, dontFind=None):
		'''Returns a dict of <function name:returns> while also running the function.
		- if p is True, run all called flags and return dict, else just return a list of valid flags
		- toFind is of type "list", containing names of menu entries to find.
		- dontFind is of type "list", containing names of menu entries to avoid'''

		#Create a dict of <entries:return values>
		toReturn={}
		for e in ProgMenu.menuEntries:
			toReturn[e.getName()]=None

		#Make sure toFind is populated with entry names
		if not toFind:
			toFind=[i.getName() for i in ProgMenu.menuEntries]

		def parseEntry(e):
			'''Checks if e (of type MenuEntry) was set. Run it if it is found'''
			if e.getFlg()==0:
				if any(i in self.flags for i in e.getLabels()):
					return e()

			elif e.getFlg()==1:
				for i in self.assigned:
					if i in e.getLabels():
						return e(self.assigned[i])

			elif e.getFlg()==2:
				if any(i in self.args for i in e.getLabels()):
					return e()

			elif e.getFlg()==3:
				for i in self.assigned:
					if i in e.getLabels():
						return e(self.assigned[i])

				if any(i in self.flags for i in e.getLabels()):
					return e()

			return None

		#If dontFind has something, loop through toFind and remove anything
		#that doesn't match with dontFind to toReturn
		if dontFind:
			#Loop through toFind, if there's a match with dontFind, don't run it
			for i in dontFind:
				toFind.remove(i)

		#Loop through toReturn and compare with toFind
		for r in toReturn:
			#Check if p is set and run the flag if it is
			if p and r in toFind:
				ret=parseEntry(self.sgetMenuEntry(r))
			elif not p:  #Don't run command, but check if flag was called
				flg=self.sgetMenuEntry(r).getFlg()
				print(f"[|X]: r: {r}")
				print(f"[|X]: flg: {flg}")
				if flg==0:  #Search in flags
					ret=True if r in self.flags else False
				elif flg==1:  #Search in assigned
					ret=True if r in self.assigned else False
				elif flg==2:  #Search in args
					ret=True if r in self.args else False
				elif flg==3:  #Search in flags & assigned
					ret=True if r in self.flags or r in self.assigned else False

			toReturn[r]=ret

		return toReturn


#Flags
	def findFlag(self, toFind):
		'''Returns True if any arg is a flag.
		toFind is of type "list" OR a MenuEntry object'''
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
		'''Get a specific value (or at least the first one it finds if it's a list)'''
		try:
			#If spec is a list, test if any of the passed values were flagged
			if type(spec)==list:
				for i in self.assigned:
					if i in spec:
						return self.assigned[i]
			else:
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
	- 2=args
	- 3=flags&assigned

	When setting an entry as 1, this means the function is expecting an argument (Namely whatever is passed as arg to the flag).
	The argument is retrieved through the assigned list in Menu.'''
	entryBlacklist=[]
	entryWhitelist=[]

	def __init__(self, name, labels, function, flg=0):
		self.name=name
		self.labels=labels  #Labels being a list of the flags/args
		self.function=function
		self.flg=flg
		ProgMenu.menuEntries.append(self)

	def __str__(self):
		return f"{self.name}\t{self.labels}\t{self.function}"

	def __call__(self, *args, **kwargs):
		return self.function(*args, **kwargs)

	def run(self, *args, **kwargs):
		return self.function(*args, **kwargs)

	@classmethod
	def getBlacklist(cls):
		return cls.entryBlacklist
	def getWhitelist(cls):
		return cls.entryWhitelist
	def addBlacklist(cls, new):
		cls.entryBlacklist.append(new)
	def addWhitelist(cls, new):
		cls.entryWhitelist.append(new)

	def getName(self):
		return self.name
	def setName(self, new):
		self.name=new

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

#Define certain variables & functions
def printFAA():
	print(menu.getFlags())
	print(menu.getAssigned())
	print(menu.getArgs())

menu=ProgMenu()
