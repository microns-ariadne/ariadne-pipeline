# Dummy package definition so that installs are easier.
import os

# Define a function so that ariadne can find out where 
# plugins are installed:


def get_examples_dir():
    # Basic operating theory:
    # The plugins package should be located somewhere in the python path.
    # As such, we can ask OS to expand this file's full path. 
    return os.path.abspath(".")+"/examples"
