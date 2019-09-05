#!/usr/bin/python3
from menu import MenuEntry

'''---------------+
|    FUNCTIONS    |
+---------------'''
def fFunc():
    '''No args are needed, as this is just for a flag'''
    print("'f' Flag called!")

def wFunc():
    print("'w' Flag called!")

def rFunc():
    print("'r' Flag called!")

'''-------------+
|    ENTRIES    |
+-------------'''
f=MenuEntry(['f', "frack"], fFunc, 0)
w=MenuEntry(['w'], wFunc, 1)
r=MenuEntry(['r'], rFunc, 0)

a=[f, w, r]
