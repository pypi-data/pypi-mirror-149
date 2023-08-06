import numpy as np
from ase.build import bulk
from hiphive.calculators.zbl import ZBLCalculator, zbl_energy, zbl_force


def test_zbl_energy():
    Z1 = 20
    Z2 = 7
    r_ij = np.array([0.5, 1.5, 5.5])
    E_target = np.array([3.55213849e+02, 7.66068060e+00, 2.28682878e-03])

    E_returned = zbl_energy(Z1, Z2, r_ij)
    assert np.allclose(E_target, E_returned)


def test_zbl_force():
    Z1 = 11
    Z2 = 18
    r_ij = np.array([0.65, 1.85, 5.2])
    F_target = np.array([1.03953423e+03, 9.51917619e+00, 7.31075639e-03])

    F_returned = zbl_force(Z1, Z2, r_ij)
    assert np.allclose(F_target, F_returned)


def test_calculator():
    atoms = bulk('NaCl', 'rocksalt', a=4.0).repeat((2, 1, 1))
    atoms[0].position += [0.1, 0.2, -0.3]
    atoms[3].position += [0.3, -0.2, 0]
    cutoff = 6.0

    calc = ZBLCalculator(cutoff, skin=0.3)
    atoms.calc = calc
    E = atoms.get_potential_energy()
    F = atoms.get_forces()

    E_target = 43.61676531264573
    F_target = np.array([[-0.3251631, -9.6241141,  6.26106724],
                         [1.85429746, -0.97504613, -7.70976377],
                         [2.72169881, -2.31647017, -1.14115497],
                         [-4.25083317, 12.9156304,  2.58985151]])

    assert np.allclose(E, E_target)
    assert np.allclose(F, F_target)


def test_numerical_forces():
    atoms = bulk('NaCl', 'rocksalt', a=4.0).repeat((2, 1, 1))
    atoms[0].position += [0.1, 0.2, -0.3]
    atoms[3].position += [0.3, -0.2, 0]
    cutoff = 6.0

    calc = ZBLCalculator(cutoff)
    atoms.calc = calc
    f_target = atoms.get_forces()[0][0]  # target first atoms force in x-direction

    # small finite displacement
    dx = 0.001

    atoms1 = atoms.copy()
    atoms1.positions[0] += [dx, 0, 0]
    atoms1.calc = calc
    E1 = atoms1.get_potential_energy()

    atoms2 = atoms.copy()
    atoms2.positions[0] += [-dx, 0, 0]
    atoms2.calc = calc
    E2 = atoms2.get_potential_energy()

    # calc numerical force
    f_numerical = -(E1-E2)/(2*dx)

    assert abs(f_target-f_numerical) < 1e-5
