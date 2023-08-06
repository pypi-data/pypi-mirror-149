

""""""# start delvewheel patch
def _delvewheel_init_patch_0_0_22():
    import os
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'CFML.libs'))
    if sys.version_info[:2] >= (3, 8):
        conda_workaround = os.path.exists(os.path.join(sys.base_prefix, 'conda-meta')) and (sys.version_info[:3] < (3, 8, 13) or (3, 9, 0) <= sys.version_info[:3] < (3, 9, 9))
        if conda_workaround:
            # backup the state of the environment variable CONDA_DLL_SEARCH_MODIFICATION_ENABLE
            conda_dll_search_modification_enable = os.environ.get('CONDA_DLL_SEARCH_MODIFICATION_ENABLE')
            os.environ['CONDA_DLL_SEARCH_MODIFICATION_ENABLE'] = '1'
        os.add_dll_directory(libs_dir)
        if conda_workaround:
            # restore the state of the environment variable CONDA_DLL_SEARCH_MODIFICATION_ENABLE
            if conda_dll_search_modification_enable is None:
                os.environ.pop('CONDA_DLL_SEARCH_MODIFICATION_ENABLE', None)
            else:
                os.environ['CONDA_DLL_SEARCH_MODIFICATION_ENABLE'] = conda_dll_search_modification_enable
    else:
        from ctypes import WinDLL
        with open(os.path.join(libs_dir, '.load-order-CFML-0.0.2')) as file:
            load_order = file.read().split()
        for lib in load_order:
            WinDLL(os.path.join(libs_dir, lib))


_delvewheel_init_patch_0_0_22()
del _delvewheel_init_patch_0_0_22
# end delvewheel patch

# **************************************************************************
#
# CrysFML API
#
# @file      Src/__init__.py
# @brief     __init__ for API module
#
# @homepage  https://code.ill.fr/scientific-software/crysfml
# @license   GNU LGPL (see LICENSE)
# @copyright Institut Laue Langevin 2020-now
# @authors   Scientific Computing Group at ILL (see AUTHORS)
#
# **************************************************************************

# Try to import fortran binding
try:
    import CFML_api.crysfml_api
except ImportError as e:
    raise ImportError(str(e) + "\n\n=> Fortran binding could not be found. It may not be properly compiled, or it may be linked with another Python interpreter")

from CFML_api.FortranBindedClass import FortranBindedClass
from CFML_api.API_Atom_TypeDef import AtomList
from CFML_api.API_Atom_TypeDef import Atom
from CFML_api.API_Crystal_Metrics import Cell, k_to_cart_vector, k_to_cart_unitary_vector, betas_from_biso
from CFML_api.API_Crystallographic_Symmetry import SpaceGroup, multiplicity_pos, occupancy_site
from CFML_api.API_Diffraction_Patterns import DiffractionPattern
from CFML_api.API_IO_Formats import CIFFile, JobInfo
from CFML_api.API_Reflections_Utilities import ReflectionList, Reflection
from CFML_api.PowderPatternSimulation import PowderPatternSimulationConditions
from CFML_api.PowderPatternSimulation import PowderPatternSimulationSource
from CFML_api.API_Error_Messages import ErrorMessages

API_version = 0.2
