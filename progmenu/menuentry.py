#!/usr/bin/python3
## Author:	Owen Cocjin
## Version:	4.1
## Date:	2020.12.22
## Description:	Holds MenuEntry and subclasses
## Notes:
##    - Fixed strict parsing collision with verbose
##    - Current fix requires verbose to be setup BEFORE parsing.
class MenuEntry():
	'''Menu entry class.
name: Entry's name. This is how it will be referenced through the PARSER dictionary.
labels: The flags that will trigger this entry. NOTE: If multiple entries have the same flags, all will trigger!
function: The function that will run when this entry is triggered. If you just want to determine if the flag is caught, use: 'lambda: True' (without quotes).
	Mode status:
	- 0=flags (No arguments will be accepted. Must return True)
	- 1=assigned (Exactly 1 positional argument is expected)
	- 2=flags&assigned (Exactly 1 keyword argument is expected)
	'''
	all_entries=[]  #Class-wide list of all menu entries


	def __init__(self, name, labels, function, mode=0):
		self.name=name
		self.labels=labels  #Labels being a list of the flags/args
		self.function=function
		self.mode=mode
		MenuEntry.all_entries.append(self)

	def __str__(self):
		return f"{self.name}"

	def __call__(self, *args, **kwargs):
		return self.function(*args, **kwargs)

	@classmethod
	def listNames(cls):
		'''Returns a list of names of entries in order of creation.'''
		return [i.getName() for i in MenuEntry.all_entries]

	@classmethod
	def printEntries(cls):
		'''Prints entries'''
		[print(i) for i in MenuEntry.all_entries]

	@classmethod
	def getMenuEntries(cls):
		return cls.all_entries

	@classmethod
	def sgetMenuEntry(cls, e):
		'''Return specific menu entry by name or entries labels.'''
		for i in cls.all_entries:
			if i.getName()==e or (e in i.getLabels()):
				return i
		return False

	@classmethod
	def getEntryNames(cls):
		return [i.getName() for i in MenuEntry.all_entries]

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
	def getWorkingLabel(self, menu):
		'''Returns the first found working label, None if none found'''
		for l in self.labels:
			if l in menu:
				return l
		return None

	def setFunction(self, new):
		self.function=new

	def getMode(self):
		return self.mode
	def setMode(self, new):
		self.mode=new

class MenuEntryExecute(MenuEntry):
	'''Menu Entry with executable qualities'''
	def __init__(self, name, labels, function, mode=0, value=None):
		MenuEntry.__init__(self, name, labels, function, mode)
		self.value=value

	def getValue(self):
		return self.value
	def setValue(self, new):
		self.value=new

	def execute(self):
		'''Runs self.function with self.value only'''
		return self.function(self.value)

class EntryFlag(MenuEntry):
	'''MenuEntry with default mode 0'''
	def __init__(self, name, labels, function):
		MenuEntry.__init__(self, name, labels, function)
		self.mode=0

class EntryArg(MenuEntryExecute):
	'''MenuEntry with default mode 1'''
	def __init__(self, name, labels, function, value=None):
		MenuEntryExecute.__init__(self, name, labels, function)
		self.mode=1
		self.value=value

	def execute(self):
		'''Return None if self.value is None'''
		if self.value==None:
			return None
		return self.function(self.value)

class EntryKeyarg(MenuEntryExecute):
	'''MenuEntry with default mode 2'''
	def __init__(self, name, labels, function, value=None):
		MenuEntryExecute.__init__(self, name, labels, function)
		self.mode=2
		self.value=value

	def execute(self):
		'''Runs self.function with self.value if not None'''
		if self.value!=None:
			return self.function(self.value)
		return self.function()
