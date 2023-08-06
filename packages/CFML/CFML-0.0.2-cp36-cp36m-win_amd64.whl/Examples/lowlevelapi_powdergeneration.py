import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

import matplotlib.pyplot as plt

import CFML_api

filename = sys.argv[1]

cif_file = CFML_api.CIFFile(filename)

cell = cif_file.cell
space_group = cif_file.space_group
atom_list = cif_file.atom_list
job_info = cif_file.job_info

# cell.print_description()
# space_group.print_description()
# atom_list.print_description()
job_info.print_description()

job_info.range_2theta=(0.0,120.0)

#print(job_info.range_2theta)

job_info.u_resolution = 0.5

#print(job_info.u_resolution)

# Friedel's pair F(h,k,l) = F(-h,-k,-l) in absence of anomalous dispersion phasing techniques
reflection_list = CFML_api.ReflectionList(cell, space_group, True, job_info)

reflection_list.compute_structure_factors(space_group, atom_list, job_info)

print(reflection_list.nref)

ref = reflection_list[0]

print(ref.hkl, ref.fcalc, ref.stl)

diffraction_pattern = CFML_api.DiffractionPattern(job_info,
                                                  reflection_list, cell.reciprocal_cell_vol)

#plt.plot(diffraction_pattern.x, diffraction_pattern.ycalc)
#plt.show()
