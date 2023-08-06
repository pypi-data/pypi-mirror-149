from ase.build import bulk
from ase.calculators.emt import EMT

from hiphive import ClusterSpace
from hiphive.self_consistent_phonons import self_consistent_harmonic_model


def test_scp():

    # parameters
    T = 1000
    cutoffs = [4.0]
    n_structures = 5
    n_iterations = 10
    alpha = 0.5

    # atoms and calculator
    prim = bulk('Ni')
    atoms = prim.repeat(4)
    calc = EMT()

    # run scp
    cs = ClusterSpace(atoms, cutoffs)
    parameters_traj = self_consistent_harmonic_model(
            atoms, calc, cs, T, alpha, n_iterations, n_structures)

    # check the length of parameters_traj, +1 because initial model is included
    assert len(parameters_traj) == n_iterations + 1

    # check that parameters are of correct size
    for parameters in parameters_traj:
        assert len(parameters) == cs.n_dofs
