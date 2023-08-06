"""
Make sure that the Progress works
"""

import time
import logging
import tempfile
from io import StringIO
from hiphive.input_output.logging_tools import set_config, Progress, logger
from ase.build import bulk
from hiphive import ClusterSpace


def test_logging():
    # Test Progress
    # --------------
    n_iters = 100
    seconds = 4

    # without continuous
    bar = Progress(n_iters)
    for i in range(n_iters):
        bar.tick()
    bar.close()

    # with continuous
    set_config(continuous=True)
    bar = Progress(n_iters)
    for i in range(n_iters):
        time.sleep(seconds/n_iters)
        bar.tick()
    bar.close()

    # Test logger
    # --------------
    atoms = bulk('Al')
    cutoffs = [4.0]

    # Log ClusterSpace output to StringIO stream
    for handler in logger.handlers:
        logger.removeHandler(handler)

    stream = StringIO()
    stream_handler = logging.StreamHandler(stream)
    logger.addHandler(stream_handler)

    ClusterSpace(atoms, cutoffs)
    stream_handler.flush()
    lines1 = stream.getvalue().split('\n')[:-1]  # remove last blank line

    # Log ClusterSpace output to file
    for handler in logger.handlers:
        logger.removeHandler(handler)

    logfile = tempfile.NamedTemporaryFile(mode='w+', encoding='utf-8')
    set_config(filename=logfile.name)

    ClusterSpace(atoms, cutoffs)
    logfile.seek(0)
    lines2 = [line.replace('\n', '') for line in logfile.readlines()]

    # assert lines1 (from stringIO stream) and lines (from file stream) are equal
    assert len(lines1) == len(lines2)
    for l1, l2 in zip(lines1, lines2):
        assert l1 == l2
