import numpy as np
from ase.build import bulk
from hiphive import ClusterSpace, StructureContainer
from hiphive.core.translational_constraints import get_translational_constraint_matrix
from trainstation import Optimizer
from hiphive.utilities import prepare_structure
from ase.calculators.emt import EMT


def test_translational_sum_rules_with_constraint_matrix():
    np.random.seed(42)

    # make dummy model
    prim = bulk('Al', 'fcc', a=4.0)
    cs = ClusterSpace(prim, [6.0], acoustic_sum_rules=False)

    atoms_ideal = prim.repeat(5)
    atoms = atoms_ideal.copy()
    atoms.rattle(0.05, seed=100)
    atoms = prepare_structure(atoms, atoms_ideal, calc=EMT())
    sc = StructureContainer(cs)
    sc.add_structure(atoms)

    A, y = sc.get_fit_data()
    opt = Optimizer((A, y), train_size=1.0)
    opt.train()
    parameters = opt.parameters

    # get constraint matrix and compute error
    Ac = get_translational_constraint_matrix(cs).to_array()
    error = np.linalg.norm(np.dot(Ac, parameters))

    assert error > 0.01
