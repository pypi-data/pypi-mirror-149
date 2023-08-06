import numpy as np
from ase.io import read
from hiphive import ForceConstants


def compute_array_relative_error(array1, array2):
    """ Computes relative error between two arrays """
    return 100.0 * np.linalg.norm(array1 - array2) / np.linalg.norm(array2)


def compute_relative_errors(fcs1, fcs2):
    """ Return relative fc difference in percentage for second and third order """
    fc2_array1 = fcs1.get_fc_array(order=2)
    fc2_array2 = fcs2.get_fc_array(order=2)
    fc2_error = compute_array_relative_error(fc2_array1, fc2_array2)
    if 3 in fcs1.orders and 3 in fcs2.orders:
        fc3_array1 = fcs1.get_fc_array(order=3)
        fc3_array2 = fcs2.get_fc_array(order=3)
        fc3_error = compute_array_relative_error(fc3_array1, fc3_array2)
    else:
        fc3_error = None
    return fc2_error, fc3_error


# Read phono3py fcs
atoms = read('phono3py_calculation/SPOSCAR')
fcs2_phono3py = ForceConstants.read_phonopy(atoms, 'phono3py_calculation/fc2.hdf5')
fcs3_phono3py = ForceConstants.read_phono3py(atoms, 'phono3py_calculation/fc3.hdf5')
fcs_phono3py = fcs2_phono3py + fcs3_phono3py
omega_phonopy = fcs_phono3py.compute_gamma_frequencies()

# Read hiphive fcs
fcs_model2 = ForceConstants.read('model2.fcs')
omega_model2 = fcs_model2.compute_gamma_frequencies()

fcs_model3 = ForceConstants.read('model3.fcs')
omega_model3 = fcs_model3.compute_gamma_frequencies()

fcs_model4 = ForceConstants.read('model4.fcs')
omega_model4 = fcs_model4.compute_gamma_frequencies()


# Compare fcs
fc2_model2_error, _ = compute_relative_errors(fcs_model2, fcs_phono3py)
omega_model2_error = compute_array_relative_error(omega_phonopy, omega_model2)
print('Model 2: FC2 error        {:.4f} %'.format(fc2_model2_error))
print('Model 2: Frequency error  {:.4f} %'.format(omega_model2_error))

print('')

fc2_model3_error, fc3_model3_error = compute_relative_errors(fcs_model3, fcs_phono3py)
omega_model3_error = compute_array_relative_error(omega_phonopy, omega_model3)
print('Model 3: FC2 error        {:.4f} %'.format(fc2_model3_error))
print('Model 3: FC3 error        {:.4f} %'.format(fc3_model3_error))
print('Model 3: Frequency error  {:.4f} %'.format(omega_model3_error))

print('')


fc2_model4_error, fc3_model4_error = compute_relative_errors(fcs_model4, fcs_phono3py)
omega_model4_error = compute_array_relative_error(omega_phonopy, omega_model4)
print('Model 4: FC2 error        {:.4f} %'.format(fc2_model4_error))
print('Model 4: FC3 error        {:.4f} %'.format(fc3_model4_error))
print('Model 4: Frequency error  {:.4f} %'.format(omega_model4_error))
