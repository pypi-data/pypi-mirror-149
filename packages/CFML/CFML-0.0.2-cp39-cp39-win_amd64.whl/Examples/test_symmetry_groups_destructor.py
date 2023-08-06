import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

import CFML_api

while True:
    a=CFML_api.SpaceGroup(5)
    b=CFML_api.SpaceGroup(10)
    #a.print_description()
    a.symmetry_operators
    a.lattice_translation
    a.is_hexa
    a.space_group_number
    a.space_group_symbol
    a.hall_symbol
    a.generalized_hall_symbol
    a.crystal_system
    a.laue_class
    a.point_group
    a.extra_information
    a.space_group_setting
    a.space_group_lattice_type
    a.space_group_lattice_type_symbol
    a.number_of_lattice_points
    a.bravais
    a.centre
    a.centric
    a.inversion_centre
    a.number_of_symops
    a.multiplicity
    a.operators_minimum_number
    a.symmetry_operators
    a.symmetry_operators_as_text
    a.wyckoff_info
    a.asymetric_unit
    a.symmetry_operators[0].rotation_matrix
    a.symmetry_operators[0].translation_matrix
    a.wyckoff_info.num_orbit
    a.wyckoff_info.orbits[0].multiplicity
    a.wyckoff_info.orbits[0].site
    a.wyckoff_info.orbits[0].orbit_number
    a.wyckoff_info.orbits[0].str_orig
    a.wyckoff_info.orbits[0].str_orbit[0]