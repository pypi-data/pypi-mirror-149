import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

import matplotlib.pyplot as plt
import numpy as np

import CFML_api

# Create list from string
print("========\nCreate job_info from string")
dat = [
'Title SrTiO3',
'Npatt 1',
'Patt_1 NEUT_2THE  1.54056    1.54056    1.00      0.0        135.0',
'UVWXY        0.025  -0.00020   0.01200   0.00150  0.00465',
'STEP         0.05 ',
'Backgd       50.000']

job_info = CFML_api.JobInfo(dat)
job_info.print_description()

job_info.range_2theta = (0.0, 12.0)

job_info.print_description()

#help(CFML_api.JobInfo)
