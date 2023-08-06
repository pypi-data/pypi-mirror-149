import numpy as np

from ase.build import fcc100
from ase.calculators.emt import EMT
from ase.optimize import BFGS

from hiphive.cutoffs import BaseClusterFilter
from hiphive import ClusterSpace, StructureContainer
from trainstation import CrossValidationEstimator
from hiphive.structure_generation import generate_rattled_structures
from hiphive.utilities import prepare_structures


class SurfaceFilter(BaseClusterFilter):

    def setup(self, atoms):
        self.atoms = atoms
        dist_tol = 1e-5
        z_pos = atoms.positions[:, 2]
        z_max = np.max(z_pos)
        z_min = np.min(z_pos)

        top_layer = np.where(z_pos + dist_tol > z_max)[0].tolist()
        bot_layer = np.where(z_pos - dist_tol < z_min)[0].tolist()
        self.surface_indices = top_layer + bot_layer

    def __call__(self, cluster):
        order = len(cluster)
        if order <= 2:
            return True
        else:
            return any(c in self.surface_indices for c in cluster)


def evaluate_cs(cs, structures):
    sc = StructureContainer(cs)
    for x in structures:
        sc.add_structure(x)
    cve = CrossValidationEstimator(sc.get_fit_data(), n_splits=10)
    cve.validate()
    print(cve)
    return cve.summary


# setup atoms and filter
atoms = fcc100('Ni', (6, 6, 6), a=4.05, vacuum=20, orthogonal=True)
atoms.pbc = True
calc = EMT()

# relax structure
atoms.set_calculator(calc)
dyn = BFGS(atoms)
converged = dyn.run(fmax=0.0001, steps=1000)

# setup cluster filter
sf = SurfaceFilter()

# build clusterspace
cutoffs1 = [6.0]
cutoffs2 = [6.0, 3.0, 3.0]
cs1 = ClusterSpace(atoms, cutoffs1, cluster_filter=None)
cs2 = ClusterSpace(atoms, cutoffs2, cluster_filter=None)
cs2_sf = ClusterSpace(atoms, cutoffs2, cluster_filter=sf)

print('Degrees of freedom second order                :', cs1.n_dofs)
print('Degrees of freedom fourth order                :', cs2.n_dofs)
print('Degrees of freedom fourth order with filter    :', cs2_sf.n_dofs)

# testing
structures = generate_rattled_structures(atoms, n_structures=25, rattle_std=0.03)
structures = prepare_structures(structures, atoms, calc)

# second order only
cve1 = evaluate_cs(cs1, structures)
cve2 = evaluate_cs(cs2, structures)
cve2_sf = evaluate_cs(cs2_sf, structures)
