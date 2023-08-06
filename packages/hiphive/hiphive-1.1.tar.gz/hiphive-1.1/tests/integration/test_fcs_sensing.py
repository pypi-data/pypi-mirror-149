import numpy as np

from ase.build import bulk
from hiphive import ClusterSpace, ForceConstantPotential
from hiphive.utilities import extract_parameters


def test_fcs_sensing():
    tols = [1e-12, 1e-10]
    methods = ['numpy', 'scipy']

    cutoffs = [5.0, 4.0]
    prim = bulk('Al', a=4.05)
    dim = 4

    ideal = prim.repeat(dim)

    cs = ClusterSpace(prim, cutoffs)
    parameters = np.random.random(cs.n_dofs)
    fcp = ForceConstantPotential(cs, parameters)
    fcs = fcp.get_force_constants(ideal)
    for tol, method in zip(tols, methods):
        fitted_parameters = extract_parameters(fcs, cs, lstsq_method=method)
        assert np.linalg.norm(fitted_parameters - parameters) < tol
