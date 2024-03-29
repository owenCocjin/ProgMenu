#!/usr/bin/python3
## Author:	Owen Cocjin
## Version:	5
## Date:	2022.03.05
## Description:	Holds MenuEntry and subclasses
## Notes:
##  - Requires verbose to be setup BEFORE parsing.
## Updates:
##  - Added StrictIf
from .errors import *

class MenuEntry():
	'''Menu entry class.
name: Entry's name. This is how it will be referenced through the PARSER dictionary.
labels: The flags that will trigger this entry.
	- NOTE: If multiple entries have the same flags, all will trigger!
function: The function that will run when this entry is triggered. If you just want to determine if the flag is caught, use: 'lambda: True' (without quotes).
mode: The mode the entry should be in (see below).
	Mode status:
		- 0=flags (No arguments will be accepted. Must return True)
		- 1=assigned (Exactly 1 positional argument is expected)
		- 2=flags&assigned (Exactly 1 keyword argument is expected)
		- 3=positional (Refers to args list for argument)
strict: If True, the strict entry's flag MUST be called when parsed strictly.
recurse: A list of entry names who's outputs are used as arguments to the Entry.
	- NOTE: The recurse outputs are passed last, and are passed in the same order as the list is in.
	'''
	all_entries=[]  #Class-wide list of all menu entries
	flags=[]
	args=[]
	keyargs=[]
	positionals=[]

	def __init__(self, name, labels, function, mode=0, strict=False, recurse=None, default=None, strictif=None):
		'''name=Entry name
		labels=Flags used to address entry
		function=Function called by entry
		mode=Mode of entry (see above)
		strict=Mandatory flag if MENU.parser has strict set to True
		recurse=A list of other flag names who's output will be used in this entry
		strictif=List of MenuEntries that if not called, make this entry strict
			Ex: EntryFlag("ip",['i',"ip"],lambda i:i,default="0.0.0.0",strictif=["server"])  #If server entry was NOT called, this becomes strict
		alt=Name of alt entry who's value to grab
		'''
		self.name=name
		self.labels=labels  #Labels being a list of the flags/args
		self.function=function
		self.mode=mode
		self.strict=strict
		self.recurse=recurse
		self.vrecurse=None  #Values of recurse
		self.default=default
		self.beenrun=False  #Tells parser if already been executed
		self.strictif=strictif
		# self.alt=alt
		MenuEntry.all_entries.append(self)

	def __str__(self):
		return f"{self.name}"

	def __call__(self, *args, **kwargs):
		return self.function(*args, **kwargs)

	@classmethod
	def help(cls):
		'''Returns a list of entry names and their labels.'''
		toRet={}
		for e in cls.all_entries:
			toRet[e.getName()]=e.getLabels()
		return toRet
	@classmethod
	def addEntry(cls, new):
		'''Add an entry to the class-wide list'''
		MenuEntry.all_entries.append(new)
	@classmethod
	def removeEntry(cls, e):
		'''Removes an entry by name.
		Returns True if entry was found/deleted, False otherwise.'''
		for i in range(len(MenuEntry.all_entries)):
			if MenuEntry.all_entries[i].getName()==e:
				del MenuEntry.all_entries[i]
				return True
		return False
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

	def strictIfLabelList(self):
		'''Get a list of all strictIf labels'''
		toret=[]
		menu=None
		if not self.strictif:
			return None
		for n in self.strictif:
			menu=self.sgetMenuEntry(n)
			if not menu:
				raise StrictIfEntryError(f"Entry \"{n}\" doesn't exist!")
			toret+=menu.getLabels()
		return toret

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
	def getStrict(self):
		return self.strict
	def setStrict(self, new):
		self.strict=new
	def getRecurse(self):
		return self.recurse
	def setRecurse(self, new):
		self.recurse=new
	def getVRecurse(self):
		return self.vrecurse
	def setVRecurse(self, new):
		self.vrecurse=new
	def getDefault(self):
		return self.default
	def setDefault(self, new):
		self.default=new
	def getBeenRun(self):
		return self.beenrun
	def setBeenRun(self, new):
		self.beenrun=new
	def getStrictIf(self):
		return self.strictif
	def setStrictIf(self,new):
		self.strictif=new

class MenuEntryExecute(MenuEntry):
	'''Menu Entry with executable qualities'''
	def __init__(self, name, labels, function, mode=0, *, strict=False, recurse=None, default=None, strictif=None):
		MenuEntry.__init__(self, name, labels, function, mode, strict=strict, recurse=recurse, default=default, strictif=strictif)
		self.value=None

	def getValue(self):
		return self.value
	def setValue(self, new):
		self.value=new

	def execute(self):
		'''Runs self.function with self.value only'''
		return self.function(self.value)

class EntryFlag(MenuEntry):
	'''MenuEntry with default mode 0'''
	def __init__(self, name, labels, function, *, strict=False, recurse=None, default=None, strictif=None):
		MenuEntry.__init__(self, name, labels, function, strict=strict, recurse=recurse, default=default, strictif=strictif)
		MenuEntry.flags.append(self)
		self.mode=0

	def execute(self):
		if self.recurse!=None:
			return self.function(*self.vrecurse)
		else:
			return self.function()

class EntryArg(MenuEntryExecute):
	'''MenuEntryExecute with default mode 1'''
	def __init__(self, name, labels, function, *, strict=False, recurse=None, default=None, strictif=None):
		MenuEntryExecute.__init__(self, name, labels, function, 1, strict=strict, recurse=recurse, default=default, strictif=strictif)
		MenuEntry.args.append(self)
		self.value=None

	def execute(self):
		'''Return None if self.value is None'''
		if self.value==None:
			return None
		if self.recurse!=None:
			return self.function(*self.vrecurse, self.value)
		else:
			return self.function(self.value)

class EntryKeyArg(MenuEntryExecute):
	'''MenuEntryExecute with default mode 2'''
	def __init__(self, name, labels, function, *, strict=False, recurse=None, default=None, strictif=None):
		MenuEntryExecute.__init__(self, name, labels, function, 2, strict=strict, recurse=recurse, default=default, strictif=strictif)
		MenuEntry.keyargs.append(self)
		self.value=[]  #Uses a list because otherwise None would always be passed

	def setValue(self, v):
		'''Sets value'''
		self.value.append(v)

	def execute(self):
		'''Runs self.function'''
		if self.recurse!=None:
			return self.function(*self.vrecurse, *self.value)
		else:
			return self.function(*self.value)

class EntryPositional(MenuEntryExecute):
	'''MenuEntryExecute with default mode 3'''
	def __init__(self,name,position,function,*,strict=False,recurse=None,default=None,strictif=None,alt:str=None):
		MenuEntryExecute.__init__(self,name,[name],function,3,strict=strict,recurse=recurse,default=default,strictif=strictif)
		MenuEntry.positionals.append(self)
		self.position=position
		self.value=None  #This will be reset during parsing

		self.strict=strict
		self.alt=alt  #Alternate entry to stuff into this value
	def execute(self):
		'''Runs self.function'''
		if self.recurse!=None:
			return self.function(*self.vrecurse,self.value)
		else:
			return self.function(self.value)

	def getAlt(self):
		return self.alt
	def setAlt(self,new):
		self.alt=new
