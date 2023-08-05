import os

# read a text file
def read_textfile(filename):
    actual_filename = os.path.expandvars(os.path.expanduser(filename))
    with open(actual_filename, "rt") as f:
        return f.read()

