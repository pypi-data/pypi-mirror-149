import numpy as np
from ase.build import fcc100
from hiphive import ClusterSpace, enforce_rotational_sum_rules, StructureContainer
from hiphive.core.rotational_constraints import get_rotational_constraint_matrix
from trainstation import Optimizer
from hiphive.utilities import prepare_structure
from ase.calculators.emt import EMT


def test_rotational_sum_rules():
    np.random.seed(42)

    # make dummy model
    prim = fcc100('Al', (1, 1, 1), vacuum=10, a=4.0)
    prim.pbc = True
    cs = ClusterSpace(prim, [3.9])

    atoms_ideal = prim.repeat((5, 5, 1))
    atoms = atoms_ideal.copy()
    atoms.rattle(0.05, seed=100)
    atoms = prepare_structure(atoms, atoms_ideal, calc=EMT())
    sc = StructureContainer(cs)
    sc.add_structure(atoms)

    A, y = sc.get_fit_data()
    opt = Optimizer((A, y), train_size=1.0)
    opt.train()
    parameters = opt.parameters

    # get constraint matrix and check before and after
    Ac = get_rotational_constraint_matrix(cs)
    error1 = np.linalg.norm(np.dot(Ac, parameters))
    new_parameters = enforce_rotational_sum_rules(cs, parameters)
    error2 = np.linalg.norm(np.dot(Ac, new_parameters))

    assert error1 > 0.1
    assert error2 < 1e-5
