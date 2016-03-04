# datasettools -- Contains classes and functions necessary to manage, parse, and use datasets.

import DatasetDefs
import ariadnetools
import os
import sys

def parseFormatSpec(specEntry):
    x=0
    y=0
    z=0
    formattype=""
    filename=""

    for e in specEntry:
        if e[0]=="x":
            x=e[1]
        elif e[0]=="y":
            y=e[1]
        elif e[0]=="z":
            z=e[1]
        elif e[0]=="formattype":
            formattype=e[1]
        elif e[0]=="filename":
            filename=e[1]

    return x, y, z, formattype, filename
    



