#!/usr/bin/python3
from menu import MenuEntry

'''---------------+
|    FUNCTIONS    |
+---------------'''
def fFunc():
    '''No args are needed, as this is just for a flag'''
    print("'f' Flag called!")

def wFunc(passed):
    print(f"'w' Flag called, with '{passed}' attached!")

def rFunc():
    print("'r' Flag called!")

'''-------------+
|    ENTRIES    |
+-------------'''
f=MenuEntry(['f'], fFunc, 0)
w=MenuEntry(['w', "weed"], wFunc, 1)
r=MenuEntry(['r'], rFunc, 2)
