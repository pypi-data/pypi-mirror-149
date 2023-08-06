import numpy as np
import matplotlib.pyplot as plt
from hiphive import ForceConstantPotential
from helpers import get_dispersion


# parameters
temperatures = [2000, 1000, 300]
dim = 6


# read fcps
fcps = dict()
for T in temperatures:
    fcps[T] = ForceConstantPotential.read('fcps/scph_T{}.fcp'.format(T))

# collect dispersion
dispersions = dict()
for T, fcp in fcps.items():
    dispersions[T] = get_dispersion(fcp, dim)

# read parameter trajs
parameter_trajs = np.loadtxt('scph_trajs/scph_parameters_T2000')
delta_parameters = [np.linalg.norm(p-p2) for p, p2 in zip(parameter_trajs, parameter_trajs[1:])]


# setup plot
fig = plt.figure(figsize=(8, 3.5))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

# plot scph convergence
ax1.plot(parameter_trajs)
ax1.set_xlabel('SCPH iteration')
ax1.set_ylabel('Parameters')
ax1.set_xlim([0, len(parameter_trajs)])

ax2.plot(delta_parameters)
ax2.set_xlabel('SCPH iteration')
ax2.set_ylabel('$\\Delta$ Parameters')
ax2.set_xlim([0, len(parameter_trajs)])
ax2.set_ylim(bottom=0.0)

fig.tight_layout()
fig.savefig('scph_parameter_convergence.svg')

# setup plot dispersions
fig = plt.figure()
ax1 = fig.add_subplot(111)

cmap = plt.get_cmap('viridis')
colors = {T: cmap(i/(len(dispersions)-0.9)) for i, T in enumerate(temperatures)}

# plotting dispersion
for T, (qnorms, freqs) in dispersions.items():
    color = colors[T]
    for q, freq, in zip(qnorms, freqs):
        ax1.plot(q, freq, color=color)
    ax1.plot(np.nan, np.nan, color=color, label='{}K'.format(T))

ax1.set_xlabel('Wave vector $\\vec{q}$')
ax1.set_ylabel('Frequency (meV)')
ax1.legend()

# set qpts as x-ticks
qpts = [0] + [q[-1] for q in qnorms]
qpts_names = ['N', r'$\Gamma$', 'H', r'$\Gamma$']
for q in qpts:
    ax1.axvline(q, color='k', lw=0.6)
ax1.axhline(y=0.0, color='k', ls='-', lw=1.0)
ax1.set_xticks(qpts)
ax1.set_xticklabels(qpts_names)
ax1.set_xlim([qpts[0], qpts[-1]])
ax1.set_ylim([0, 20])

fig.tight_layout()
fig.savefig('scph_phonon_dispersions.svg')
