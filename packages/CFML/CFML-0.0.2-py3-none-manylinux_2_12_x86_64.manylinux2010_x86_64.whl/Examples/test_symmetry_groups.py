import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

import CFML_api

a=CFML_api.SpaceGroup(5)
b=CFML_api.SpaceGroup(10)
print("======")
a.print_description()
print("======")
b.print_description()
print("======")
print(b.lattice_translation)
print("======")
print(a.lattice_translation)
print("======")
try:
    a.lattice_translation = [1,2,3]
except AttributeError as e:
    print(e)