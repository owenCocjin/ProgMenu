##
## Author:	Owen Cocjin
## Version:	0.1
## Date:	2022.03.05
## Description:    Holds error classes
## Notes:
##  - Generslly, errors should only be called when the programmer makes an error, not the user of the app

class StrictIfEntryError(Exception):
	def __init__(self,message=f"Error with a strictif entry!"):
		super().__init__(message)
