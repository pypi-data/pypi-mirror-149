import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

import CFML_api

while True:
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
    
    atom_list.natoms
    atom1 = atom_list[0]
    atom2 = atom_list[1]
    atom1.xyz
    atom_list[0]=atom2
    atom_list[1]=atom1
    atom = CFML_api.Atom('ATOM C C 0.0 0.0 0.0 0.2 0.5')
    atom_new = CFML_api.Atom('ATOM C C 0.0 0.0 0.0 0.2 0.5')
    atom_list[0] = atom_new
    