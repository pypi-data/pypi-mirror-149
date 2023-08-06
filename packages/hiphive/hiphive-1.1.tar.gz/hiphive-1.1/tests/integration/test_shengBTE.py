"""
Tests shengBTE write force constants
"""
import numpy as np
from tempfile import NamedTemporaryFile
from ase.build import bulk
from hiphive import ClusterSpace, ForceConstantPotential
from hiphive.input_output.shengBTE import write_shengBTE_fc3, read_shengBTE_fc3


def test_write_and_read_shengBTE():
    prim = bulk('Al', a=4.05)
    supercell = prim.repeat(4)

    cs = ClusterSpace(prim, [5.0, 5.0])
    params = np.random.random(cs.n_dofs)
    fcp = ForceConstantPotential(cs, params)
    fcs = fcp.get_force_constants(supercell)

    with NamedTemporaryFile('w') as f:

        # write
        write_shengBTE_fc3(f.name, fcs, prim, 1e-5)

        # read
        fcs_chk = read_shengBTE_fc3(f.name, prim, supercell, 1e-5)

        assert np.allclose(fcs.get_fc_array(order=3),
                           fcs_chk.get_fc_array(order=3),
                           atol=1e-5, rtol=0)
