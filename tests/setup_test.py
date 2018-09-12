import inspect
import sys
import os

# Inserting pack in path
dname = os.path.dirname(os.path.realpath(__file__))
pack_dir =  os.path.join( dname, '..')
sys.path.insert(0, os.path.realpath(pack_dir))