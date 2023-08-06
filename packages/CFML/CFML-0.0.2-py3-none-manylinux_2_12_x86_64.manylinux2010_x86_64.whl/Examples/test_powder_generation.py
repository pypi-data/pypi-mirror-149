import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))

import CFML_api
import matplotlib.pyplot as plt

plt.figure(1)

powder_pattern = CFML_api.PowderPatternSimulator()
powder_pattern.compute("Data/SrTiO3.cfl")
plt.plot(powder_pattern.x, powder_pattern.y, label="CFL")

powder_pattern = CFML_api.PowderPatternSimulator()
powder_pattern.compute("Data/SrTiO3.cif")
plt.plot(powder_pattern.x, powder_pattern.y, label="CIF with default conditions")

plt.legend()

plt.figure(2)
simulation_conditions = CFML_api.PowderPatternSimulationConditions()
simulation_conditions.lamb = 1.54056
simulation_conditions.u_resolution = 0.0012
simulation_conditions.v_resolution = -0.0002
simulation_conditions.w_resolution = 0.012
simulation_conditions.x_resolution = 0.0015
simulation_conditions.theta_min = 1.00
simulation_conditions.theta_step = 0.1
simulation_conditions.theta_max = 180
simulation_conditions.job = CFML_api.PowderPatternSimulationSource.Neutrons
simulation_conditions.lorentzian_size = 10000.0
simulation_conditions.bkg = 200.0

powder_pattern = CFML_api.PowderPatternSimulator()
powder_pattern.compute("Data/SrTiO3.cfl", simulation_conditions)
plt.plot(powder_pattern.x, powder_pattern.y, label="CFL with given conditions")

powder_pattern = CFML_api.PowderPatternSimulator()
powder_pattern.compute("Data/SrTiO3.cif", simulation_conditions)
plt.plot(powder_pattern.x, powder_pattern.y, label="CIF with given conditions")

plt.legend()

plt.show()