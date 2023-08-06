import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

import matplotlib.pyplot as plt
import numpy as np

import CFML_api

# Create list from string
print("========\nCreate atom_list from string")
dat = [
'loop_                     ',
'_atom_site_label          ',
'_atom_site_fract_x        ',
'_atom_site_fract_y        ',
'_atom_site_fract_z        ',
'_atom_site_U_iso_or_equiv ',
'Sr 0.00000 0.00000 0.25000 0.00608',
'Ti 0.50000 0.00000 0.00000 0.00507',
'O1 0.00000 0.50000 0.25000 0.01646',
'O2 0.75000 0.25000 0.00000 0.02026']
atom_list = CFML_api.AtomList(dat)
atom_list.print_description()

# Switch atoms
atom1 = atom_list[0]
atom2 = atom_list[1]
atom_list[0]=atom2
atom_list[1]=atom1
print("========\nSwitched atom list")
atom_list.print_description()

# Modify atom position
atom = atom_list[0]
atom.xyz=np.asarray([0.2, 0.3, 0.4])
atom_list[0] = atom
print("========\nModify 1st atom position")
atom_list.print_description()

# Modify atom with string
atom = atom_list[0]
atom.from_string('ATOM C C 0.0 0.0 0.0 0.2 0.5')
atom_list[0] = atom
print("========\nModified 1st atom")
atom_list.print_description()

# Create atom from string
# ATOM   label    Chem/Scatt    x(s_x)   y(s_y)   z(s_z)   B_iso(s_b)    Occ(s_o)   mom  charge # String_with_info
atom2 = CFML_api.Atom('ATOM C C 0.2(0.1) 0.4(0.3) 0.5(0.4) 0.2 0.5(0.1)  3  4 #info')
print("========\nAtom created from string")
print(atom2)

# Replace atom
print("========\nReplace 4th atom in atom list")
atom_list[3] = atom2
atom_list.print_description()
