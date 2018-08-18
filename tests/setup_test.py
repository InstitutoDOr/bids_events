import inspect
import sys
import os

# Preparing test environment
abspath = os.path.abspath((inspect.stack()[-1])[1])
dname = os.path.dirname(abspath)
os.chdir(dname)

sys.path.insert(0, r'..' + os.sep + '..')
