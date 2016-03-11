# A newer, shinier implementation of pipeline
# that supports the changes made to ariadne's execution model (it's luigi time!)

import os
import sys
import tools
import deftools
import luigi


class Pipeline:
    def __init__(self, def_filename):
        toks=deftools.parse_file(def_filename)