import numpy as np
from hiphive import ClusterSpace
from hiphive.force_constant_model import ForceConstantModel
from hiphive.core.tensors import rotation_to_cart_coord, rotate_tensor
from ase.build import bulk


def test_eigentensor_symmetry():
    # parameters
    a0 = 4.0
    cutoffs = [4.1, 4.1, 4.1]
    size = 3

    # structure lists
    primitive_structures = []
    for crystal in ['sc', 'bcc', 'fcc', 'hcp', 'diamond']:
        primitive_structures.append(bulk('Ta', crystal, a=a0))
    for crystal in ['rocksalt', 'wurtzite']:
        primitive_structures.append(bulk('NaCl', crystal, a=a0))

    # run tests
    for prim in primitive_structures:

        # setup
        supercell = prim.repeat(size)
        cs = ClusterSpace(prim, cutoffs)
        fcm = ForceConstantModel(supercell, cs)
        fcm.parameters = np.random.random(cs.n_dofs)
        fcs = fcm.get_force_constants()

        # test cluster space eigentensors
        for orbit in cs.orbits:
            for ri, pi in orbit.eigensymmetries:
                R_scaled = cs.rotation_matrices[ri]
                R = rotation_to_cart_coord(R_scaled, cs.primitive_structure.cell)
                R_inv = np.linalg.inv(R)
                perm = cs.permutations[pi]
                for et in orbit.eigentensors:
                    assert np.allclose(rotate_tensor(et, R_inv).transpose(perm), et)

        # test force constants
        for orbit in fcm.orbits:
            of = orbit.orientation_families[0]
            for cluster_ind in of.cluster_indices:
                cluster = fcm.cluster_list[cluster_ind]
                fc = fcs[cluster]
                for ri, pi in orbit.eigensymmetries:
                    R_scaled = cs.rotation_matrices[ri]
                    perm = cs.permutations[pi]
                    R = rotation_to_cart_coord(R_scaled, cs.primitive_structure.cell)
                    R_inv = np.linalg.inv(R)
                    assert np.allclose(rotate_tensor(fc, R_inv).transpose(perm), fc)
