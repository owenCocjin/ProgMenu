#!/usr/bin/python3
## Author:	Owen Cocjin
## Version:	4.6.1
## Date:	2022.01.01
## Description:	Process cmd line arguments
## Notes:
##  - Verbose must be defined before strict parsing, otherwise parser will identify verbose flag as invalid
##  - Currently, recursed entries will call their recurses
##    This means if a sub-recurse prints anything, it will print when recursed
##  - The desired recurse depth is 2, but this can be somewhat unreliable as the sub-recurses are added to the list of non-recurses once run
##  - ProgMenu.flags list is used more so to confirm that an entry was called.
##    This means if a positional entry was "called", it will show up in both flags and assigned
## Updates:
##  - Updated isEmpty() to use boolean of lists instead of checking lengths
##  - Added a loop in parser that will remove/add args based on:
##    + Remove from args if preceding flag is an EntryFlag
##    + Remove from assigned if preceding flag is an EntryArg
##    This allows more flexibility; Ex: If the last arg is a target file name, this can be implemented without any additionaly code on the user's part.
##  - Added positional entries!
##    This allows an entry to gain it's value from the position of an unassigned arg!
##  - Removes arg from arg list if assigned to positional.
##    This avoids duplicate positionals
##  - Fixed bug that didn't catch missing positionals
import sys  #Required!
from .menuentry import MenuEntry,EntryArg,EntryFlag,EntryPositional

'''-------------------+
|        SETUP        |
+-------------------'''
class ProgMenu():
	def __init__(self):
		#--------Variables--------#
		#Required!
		self.flags=[]
		self.assigned={}
		self.args=[]
		self.verbose=None  #Entry created by self.verboseSetup()

		#--------Process sys.argv--------#
		#Find flags in sys.argv and save them
		menu_args=sys.argv[1:]  #Remove first arg
		iterator=0
		# for i, n in enumerate(menu_args):
		while iterator<len(menu_args):
			n=menu_args[iterator]
			#If current arg starts with '-', it's a flag
			if n[0]=='-' and len(n)>=2:
				#If current arg starts with '--', its it's own flag
				if n[1]=='-':
					if '=' in n:
						#If there is an equal sign, split it and add to assigned, args, and flags
						rec=n[2:].split('=')
						self.flags.append(rec[0])
						self.assigned[rec[0]]=rec[1]
						# self.args.append(rec[1])
					else:
						#Add the whole flag
						self.flags.append(n[2:])
				else:
					#Count each individual char as a flag and add it to the list
					for j in n[1:]:
						self.flags.append(j)

					try:
						#If the next arg is NOT a flag, add it as arg to this flag
						if menu_args[iterator+1][0]!='-':
							self.assigned[n[-1]]=menu_args[iterator+1]
					except:
						pass

			else:
				#If this isn't an arg for the preceding entry, it will be removed from the args list by MenuEntry.parse()
				self.args.append(n)
			iterator+=1

	def __str__(self):
		return f"flags:    {self.flags}\nassigned: {self.assigned}\nargs:     {self.args}"

#Parse
	def parse(self, p=False, *, strict=False):
		'''Returns a dict of <entry name:returns> while also running the entry (if p is set).
	- If p is True, run all called flags and return dict of {entry name:return value/None}.
	- If p is False, return a dict of {entry name:True/False}, essentially making everything a flag 0.
	- If strict is True, throws error if an assigned entry wasn't passed an arg,
		plain flag was passed an arg,
		or non-entry flag was passed.'''
		toRet={}  #Dict of {EntryName:return}
		recurse=[]  #List of entries that are recursed

		#Check for help flag first!
		helpentry=MenuEntry.sgetMenuEntry("help")
		if helpentry and self.findFlag(helpentry.getLabels()):
			helpentry.execute()
			exit(0)

		def einm(entryLabels, menuList):
			'''Returns True if any entryLabels are in the given menuList'''
			return any([True for i in entryLabels if i in menuList])
		def ftom(flag):
			'''Converts a given flag to a mode based on what's passed in command line:
				-1=Flag not found (flag isn't found in entries)
				 0=Flag only (equivalent to MenuEntry mode 0)
				 1=Assigned (equivalent to MenuEntry mode 1 or 2)'''
			if flag in self.assigned:
				return 1
			elif flag in self.flags:
				return 0
			else:
				return -1
		def throwError(txt, err=1, shouldexit=True):
			'''Prints error message and exits with error no err'''
			print(txt)

			#If "help" entry exists, print it
			help_entry=MenuEntry.sgetMenuEntry("help")
			if help_entry:
				help_entry()

			if shouldexit:
				exit(err)
		def runEntry(e):
			'''Runs entry's function and returns it's result'''
			if einm(e.getLabels(),self.flags):
				if e.getMode() in [1,2,3]:
					#Get assigned value and execute with said val
					wl=e.getWorkingLabel(self.assigned.keys())
					if wl!=None:
						e.setValue(self.assigned[wl])
					return e.execute()
				elif e.getMode() in [0, 2]:
					return e.execute()  #Execute current MenuEntry
			else:
				return e.getDefault()
		def runRecurse(e):
			'''Run all recurses in entry e and return e after execution'''
			vrecursed=[]
			for sub in [MenuEntry.sgetMenuEntry(r) for r in e.getRecurse()]:
				if sub.getRecurse():  #Recursed; Not in toRet
					sub.setVRecurse([toRet[n] for n in sub.getRecurse()])
					toRet[sub.getName()]=runEntry(sub)
					sub.setBeenRun(True)
				vrecursed.append(toRet[sub.getName()])
			#Add vrecursed to e
			e.setVRecurse(vrecursed)
			#Run e
			return runEntry(e)

	#Setup loops
		#Check for flags that were assigned an arg and unassign them
		for e in MenuEntry.all_entries:
			#Get the label in assigned
			try:
				calledlabel=set(self.assigned).intersection(e.getLabels()).pop()
				if type(e)==EntryFlag:
					del self.assigned[calledlabel]
				elif type(e)==EntryArg:
					self.args.remove(self.assigned[calledlabel])
			except (KeyError,ValueError):  #Entry not in assigned
				continue

		#Assign positional args to entries
		self.positionals=self.args.copy()  #Without copy there's an issue with
		errflag=False
		for e in MenuEntry.positionals:
			#Check if entry is positional (last to prevent false positives)
			try:
				e.value=self.positionals[e.position]
				self.assigned[e.name]=e.value
				self.flags.append(e.getLabels()[0])  #There can only be a single label because the label is the name
				self.args.remove(e.value)  #Remove from args list to avoid duplicate positionals
			except (IndexError,ValueError):  #Can't remove from self.args, meaning there's a missing arg
				errflag=True
				throwError(f"[PositionalError]: Missing positional arg '{e.name}'",shouldexit=False)
		if errflag:
			exit()

		#Strict check
		if strict:
			#Loop through all entries and check if any strict ones are missing
			strictflag=False  #Used to confirm if help was called or not
			for curentry in MenuEntry.getMenuEntries():
				if curentry.getStrict() and not any(f in self.flags for f in curentry.getLabels()):
					strictflag=True
					throwError(f"[StrictError]: Missing strict flag: '{curentry.getName()}'!", shouldexit=False)
			if strictflag:
				#Print entry help if verbose
				if self.verbose!=None and any(f in self.flags for f in self.verbose.getLabels()):
					entryhelp=MenuEntry.help()
					print("Flags:")
					for l in entryhelp:
						print(f"\t{l}: {entryhelp[l]}")
				exit(1)

			#Add verbose to entry list
			if self.verbose!=None:
				MenuEntry.addEntry(self.verbose)
			#Make a big list of labels
			allLabels=[j for i in MenuEntry.getMenuEntries() for j in i.getLabels()]
			for curFlag in self.flags:
				curEntry=MenuEntry.sgetMenuEntry(curFlag)
				#print(f"{curFlag} -> {ftom(curFlag)} -> {curEntry}")
				#If entry doesn't exist:
				if curFlag not in allLabels:
					throwError(f"[FlagError]: Invalid flag passed: '{curFlag}'!")
				#If entry is mode 0, but flag is mode 1
				elif curEntry.getMode()==0 and ftom(curFlag)!=0:
					throwError(f"[FlagError]: Flag was passed an arg: '{curFlag}' <- '{self.assigned[curFlag]}'!")
				#If entry mode is >=1, but flag is mode <=0
				elif ftom(curFlag)==0 and MenuEntry.sgetMenuEntry(curFlag).getMode()==1:
					throwError(f"[AssignedError]: Flag requires an arg: '{curFlag}'!")
				#Ignore everything else
				else:
					continue
			#Remove verbose entry from all_entries to prevent execution calls
			if self.verbose!=None:
				MenuEntry.removeEntry('verbose')

		#if p is False, loop through all entries, setting bool when specified
		if not p:
			for e in MenuEntry.getMenuEntries():
				if e.getMode()==0 and einm(e.getLabels(), self.flags)\
				or\
				e.getMode() in [1, 2, 3] and einm(e.getLabels(), self.assigned):
					toRet[e.getName()]=True
				else:
					toRet[e.getName()]=False
		#if p is True, execute entries
		elif p:
			for e in MenuEntry.getMenuEntries():
				#Add to recurse is marked as so, and skip running
				if e.getRecurse()!=None:
					recurse.append(e)
					continue
				#Process entry's function
				toRet[e.getName()]=runEntry(e)
				e.setBeenRun(True)

			#Check for any 2 layered recurses, quit if any exist
			recursenames=[c.getName() for c in recurse]
			for curse in recurse:
				for r in curse.getRecurse():
					if MenuEntry.sgetMenuEntry(r) in recurse\
					and\
					any(sub in recursenames for sub in MenuEntry.sgetMenuEntry(r).getRecurse()):
						throwError(f"[RecurseError:Pre-run]: Nested recurse '{r}' goes too deep!")
					elif r not in MenuEntry.getEntryNames():  #Calling a recurse that doesn't exist
						throwError(f"[RecurseError:Missing]: Entry '{r}' doesn't exist!")
				#It's good; Run it!
				if not curse.getBeenRun():
					toRet[curse.getName()]=runRecurse(curse)
					curse.setBeenRun(True)

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
		return bool(self.flags), bool(self.assigned), bool(self.args)

#Verbose
	def verboseSetup(self, verbose):
		'''Used to setup verbose printing. 'verbose' is a list of trigger flags'''
		def vprint(*args, **kwargs):
			print(*args, **kwargs)
		empty=lambda *_, **a: None

		#Return empty function if no verbose flags
		if not self.findFlag(verbose):
			return empty

		#Store verbose entry
		self.verbose=MenuEntry("verbose", verbose, empty, 0)
		#Remove verbose from entry list due to bugginess
		MenuEntry.removeEntry("verbose")
		#Return proper function
		return vprint
