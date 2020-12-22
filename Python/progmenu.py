#!/usr/bin/python3
## Author:	Owen Cocjin
## Version:	3.2
## Date:	2020.12.18
## Description:	Process cmd line arguments & holds common variables
## Notes:
##    - Moved verbose to ProgMenu. It is now a function that returns a function based on given parameters
import sys  #Required!

'''-------------------+
|        SETUP        |
+-------------------'''
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
			if n[0]=='-' and len(n)>=2:
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
	def parse(self, p=False, *, strict=False):
		'''Returns a dict of <entry name:returns> while also running the entry (if p is set).
	- If p is True, run all called flags and return dict of {entry name:return value/None}.
	- If p is False, return a dict of {entry name:True/None}.
	- If strict is True, throw error if an assigned entry wasn't passed an arg, else just ignore it'''
		entries={}
		toRet={}
		for e in self.getMenuEntries():  #Set all entries to False (default)
			entries[e]=None

		#if p isn't set, loop through all entries, setting bool when specified
		for r in entries:
			curFlg=r.getFlg()
			if curFlg==0 or curFlg==2:  #Look through flags
				if any([i for i in r.getLabels() if i in self.flags]):
					if p:
						entries[r]=r()
					else:
						entries[r]=True

			if curFlg==1 or curFlg==2:  #Look through assigned
				labels=r.getLabels()
				val=None

				#Get assigned value
				for i in self.assigned:
					if i in labels:
						val=self.assigned[i]
						break
				#Strict check
				if val==None and strict and curFlg==1:
					raise AssignedError(f"No argument was given for assigned '{r.getName()}'!")

				if any([i for i in r.getLabels() if i in self.assigned]):
					if p:
						entries[r]=r(val)
					else:
						entries[r]=True

		#Get names of entries instead of entries themselves
		for i in entries:
			toRet[i.getName()]=entries[i]

		return toRet


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

#Verbose
	def verboseSetup(self, verbose, prefix=None):
		'''Used to setup verbose printing'''
		def vprint(*args, **kwargs):
			'''Verbose printing with a prefix'''
			print(prefix, end='')
			print(*args, **kwargs)
		def vprintNoPrefix(*args, **kwargs):
			'''Verbose printing without a prefix'''
			print(*args, **kwargs)

		if verbose and prefix!=None:
			return vprint
		elif verbose and not prefix:
			return vprintNoPrefix
		else:  #Returns a useless function
			return lambda *_, **a: None

class MenuEntry():
	'''Menu entry class.
name: Entry's name. This is how it will be referenced through the PARSER dictionary.
labels: The flags that will trigger this entry. NOTE: If multiple entries have the same flags, all will trigger!
function: The function that will run when this entry is triggered. If you just want to determine if the flag is caught, use: 'lambda: True' (without quotes).
	flg status:
	- 0=flags (No arguments will be accepted. Must return True)
	- 1=assigned (Exactly 1 positional argument is expected)
	- 2=flags&assigned (Exactly 1 keyword argument is expected)

	'''

	def __init__(self, name, labels, function, flg=0):
		self.name=name
		self.labels=labels  #Labels being a list of the flags/args
		self.function=function
		self.flg=flg
		ProgMenu.menuEntries.append(self)

	def __str__(self):
		return f"{self.name}"

	def __call__(self, *args, **kwargs):
		return self.function(*args, **kwargs)

	def run(self, *args, **kwargs):
		return self.function(*args, **kwargs)

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
	'''Prints all found flags, assigned, and arguments in that order'''
	print(menu.getFlags())
	print(menu.getAssigned())
	print(menu.getArgs())

menu=ProgMenu()  #Create a global ProgMenu instance

class AssignedError(Exception):
	'''An assigned entry (flg=1) was passed without an argument'''
	pass
