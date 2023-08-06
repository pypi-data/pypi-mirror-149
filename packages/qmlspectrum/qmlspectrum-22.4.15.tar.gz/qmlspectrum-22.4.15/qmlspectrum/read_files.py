import os
from os import listdir
from os.path import isfile, join

def read_files(path):
    files = [f for f in listdir(path) if isfile(join(path, f))]
    files = sorted(files)
    return files
