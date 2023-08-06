import numpy as np
from ase.build import bulk
from hiphive import ClusterSpace
from hiphive.cluster_space_data import ClusterSpaceData


def test_cs_data_values():
    """ Test that ClusterSpaceData correctly gathers the correct data """

    cutoffs = [7, 5]
    prim = bulk('Ti', 'hcp')
    cs = ClusterSpace(prim, cutoffs)
    cs_data = ClusterSpaceData(cs)
    print(cs_data)

    # check cutoff-matrix
    assert cs_data._cutoff_matrix[0, 0] == 7.0
    assert cs_data._cutoff_matrix[0, 1] == 5.0
    assert cs_data._cutoff_matrix[1, 1] == 5.0
    assert np.isnan(cs_data._cutoff_matrix[1, 0])

    # check padding of cutoff matrix
    cm_pad = cs_data._cutoff_matrix_padded
    assert cm_pad.shape == (3, 2)
    assert np.all([cm_pad[0, i] is None for i in range(2)])
    print(cm_pad[1:, :])
    cs_data._cutoff_matrix

    # check cluster counts
    cluster_count_target = np.array([[2, 2], [80, 40], [0, 52]])
    assert np.allclose(cs_data._cluster_counts, cluster_count_target)

    # check orbit counts
    orbit_count_target = np.array([[1, 1], [10, 4], [0, 6]])
    assert np.allclose(cs_data._orbit_counts, orbit_count_target)

    # check eigentensor counts
    eigentensor_count_target = np.array([[2, 1], [44, 34], [0, 62]])
    assert np.allclose(cs_data._eigentensor_counts, eigentensor_count_target)

    # check ndofs by order
    ndofs = {2: 44, 3: 79}
    for order, ndof in ndofs.items():
        assert cs_data.ndofs_by_order[order] == ndof


def test_cs_data_functions():
    """ Test ClusterSpaceData functions """

    cutoffs = [7, 5]
    prim = bulk('Ti', 'hcp')
    cs = ClusterSpace(prim, cutoffs)
    cs_data = ClusterSpaceData(cs)

    # test to_list
    for row in cs_data.to_list():
        assert 'order' in row.keys()
        assert 'nbody' in row.keys()
        assert 'cluster_counts' in row.keys()
        assert 'orbit_counts' in row.keys()
        assert 'eigentensor_counts' in row.keys()

    # test to_dataframe
    df = cs_data.to_dataframe()
    assert 'order' in df
    assert 'nbody' in df
    assert 'cluster_counts' in df
    assert 'orbit_counts' in df
    assert 'eigentensor_counts' in df

    # test str
    assert isinstance(cs_data.__str__(), str)
