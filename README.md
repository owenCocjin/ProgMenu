# ProgMenu

> A lil library to help with cmd line flags and stuff

> YES I KNOW ONE EXISTS I WROTE THIS THEN LEARNED ABOUT argparse

## Installation

- Clone it and use it like any other library (?)

## Usage

> Add this code to the main file to test if it's working:

```
from progMenu import printFAA
printFAA()
```

> the `printFAA` function prints all the passed flags, assigned, and args

- A *flag* is: -f or --flag
- An *assigned* is a flag with an associated arg: `-s 12` or `--seed=12`
- An *arg* is pretty much anything else: `$ cmd -s <arg> <lonelyArg>`
