import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

import CFML_api
import numpy as np 

cellv = np.asarray([5,5,8], dtype='float32')
angl = np.asarray([90,90,80], dtype='float32')

while True:
    a=CFML_api.Cell(cellv, angl)
    b=CFML_api.Cell(cellv, angl)
    a.angl=[90,90,90]

