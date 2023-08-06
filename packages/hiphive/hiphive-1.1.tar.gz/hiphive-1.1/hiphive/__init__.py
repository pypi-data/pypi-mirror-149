"""
hiPhive module.
"""

from .cluster_space import ClusterSpace
from .structure_container import StructureContainer
from .force_constant_potential import ForceConstantPotential
from .force_constants import ForceConstants
from .core.config import config
from .core.rotational_constraints import enforce_rotational_sum_rules

__project__ = 'hiPhive'
__description__ = 'High-order force constants for the masses'
__authors__ = ['Fredrik Eriksson',
               'Erik Fransson',
               'Paul Erhart']
__copyright__ = '2022'
__license__ = 'MIT License'
__credits__ = ['Fredrik Eriksson',
               'Erik Fransson',
               'Paul Erhart']
__version__ = '1.1'
__all__ = ['ClusterSpace',
           'StructureContainer',
           'ForceConstantPotential',
           'ForceConstants',
           'config',
           'enforce_rotational_sum_rules']
__maintainer__ = 'The hiPhive developers team'
__maintainer_email__ = 'hiphive@materialsmodeling.org'
__status__ = 'Stable'
__url__ = 'http://hiphive.materialsmodeling.org/'
