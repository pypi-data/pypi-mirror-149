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

cell.print_description()
space_group.print_description()
atom_list.print_description()

powder_pattern_simulation_conditions = CFML_api.PowderPatternSimulationConditions()

reflection_list = CFML_api.ReflectionList(
    cell, space_group, True, 0, powder_pattern_simulation_conditions.getSinThetaOverLambdaMax())
reflection_list.compute_structure_factors(space_group, atom_list)
reciprocal_cell_vol = cell.reciprocal_cell_vol

while True:
    diffraction_pattern = CFML_api.DiffractionPattern(powder_pattern_simulation_conditions, reflection_list, reciprocal_cell_vol)
    #diffraction_pattern.title
    diffraction_pattern.diff_kind
    diffraction_pattern.scat_var
    diffraction_pattern.xax_text
    diffraction_pattern.yax_text
    diffraction_pattern.instr
    diffraction_pattern.filename
    diffraction_pattern.filepath
    diffraction_pattern.xmin
    diffraction_pattern.xmax
    diffraction_pattern.ymin
    diffraction_pattern.ymax
    diffraction_pattern.scal
    diffraction_pattern.monitor
    diffraction_pattern.norm_mon
    diffraction_pattern.col_time
    diffraction_pattern.step
    diffraction_pattern.zerop
    diffraction_pattern.Tsamp
    diffraction_pattern.Tset
    diffraction_pattern.npts
    diffraction_pattern.is_ct_step
    diffraction_pattern.is_gy
    diffraction_pattern.is_gycalc
    diffraction_pattern.is_gbgr
    diffraction_pattern.is_gsigma
    diffraction_pattern.is_sig_var
    diffraction_pattern.is_al_x
    diffraction_pattern.is_al_y
    diffraction_pattern.is_al_ycalc
    diffraction_pattern.is_al_bgr
    diffraction_pattern.is_al_sigma
    diffraction_pattern.is_al_istat
    diffraction_pattern.conv
    diffraction_pattern.x
    diffraction_pattern.y
    diffraction_pattern.sigma
    diffraction_pattern.istat
    diffraction_pattern.ycalc
    diffraction_pattern.bgr
    diffraction_pattern.nd