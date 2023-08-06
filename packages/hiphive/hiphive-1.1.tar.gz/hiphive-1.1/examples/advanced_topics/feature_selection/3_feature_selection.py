"""
Feature selection

Runs in 10 minutes on an Intel Core i5-4670K CPU.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from hiphive import StructureContainer, ForceConstantPotential
from trainstation import CrossValidationEstimator


def run_cve(fit_kwargs):
    cve = CrossValidationEstimator(
        sc.get_fit_data(), n_splits=n_splits,
        train_size=train_size, test_size=test_size,
        validation_method='shuffle-split', **fit_kwargs)
    cve.validate()
    nzp = [np.count_nonzero(params) for params in cve.parameters_splits]
    row = fit_kwargs
    row['rmse'] = cve.rmse_validation
    row['rmse_std'] = np.std(cve.rmse_validation_splits)
    row['nzp'] = np.mean(nzp)
    row['nzp_std'] = np.std(nzp)
    row['parameters'] = cve.parameters_splits[0]
    return row


# parameters
n_splits = 5
train_size = 600

# load SC
sc = StructureContainer.read('structure_container')
cs = sc.cluster_space
n_rows, n_cols = sc.data_shape
test_size = n_rows - train_size

# feature selection parameters
alphas = np.logspace(-5, -2, 20)          # LASSO
lambdas = np.logspace(3, 5, 20)           # ARDR
n_feature_vals = np.arange(50, n_cols, 20)  # RFE

# indices for which fcs will be plotted
alpha_inds = [4, 15]
lambda_inds = [6, 15]
n_features_inds = [2, 10]

# LASSO
summary_list = []
for alpha in alphas:
    kwargs = dict(fit_method='lasso', alpha=alpha, max_iter=100000)
    summary_list.append(run_cve(kwargs))
df_lasso = pd.DataFrame(summary_list)

# ARDR
summary_list = []
for threshold_lambda in lambdas:
    kwargs = dict(fit_method='ardr', threshold_lambda=threshold_lambda)
    summary_list.append(run_cve(kwargs))
df_ardr = pd.DataFrame(summary_list)

# RFE
summary_list = []
for n_features in n_feature_vals:
    kwargs = dict(fit_method='rfe', n_features=n_features)
    summary_list.append(run_cve(kwargs))
df_rfe = pd.DataFrame(summary_list)

# analyze the predicted force constant models for a selection parameters
lasso_orbits = dict()
for ind in alpha_inds:
    fcp = ForceConstantPotential(cs, df_lasso.parameters[ind])
    lasso_orbits[ind] = pd.DataFrame(fcp.orbit_data)

ardr_orbits = dict()
for ind in lambda_inds:
    fcp = ForceConstantPotential(cs, df_ardr.parameters[ind])
    ardr_orbits[ind] = pd.DataFrame(fcp.orbit_data)

rfe_orbits = dict()
for ind in n_features_inds:
    fcp = ForceConstantPotential(cs, df_rfe.parameters[ind])
    rfe_orbits[ind] = pd.DataFrame(fcp.orbit_data)


# plotting feature selection
figsize = (18, 4.8)
fs = 14
ms = 8
lw = 1.5
color1 = '#1f77b4'
color2 = '#ff7f0e'
alpha = 0.5

kwargs_rmse = dict(lw=lw, ms=ms, color=color1, label='RMSE Test')
kwargs_nzp = dict(lw=lw, ms=ms, color=color2, label='N')

fig = plt.figure(figsize=figsize)
ax1 = fig.add_subplot(1, 3, 1)
ax2 = fig.add_subplot(1, 3, 2)
ax3 = fig.add_subplot(1, 3, 3)
ax1_y2 = ax1.twinx()
ax2_y2 = ax2.twinx()
ax3_y2 = ax3.twinx()

ylim1 = [0.008, 0.02]
ylim2 = [0, 1.1*n_cols]

# LASSO
ax1.semilogx(df_lasso.alpha, df_lasso.rmse, '-o', **kwargs_rmse)
ax1.fill_between(df_lasso.alpha, df_lasso.rmse - df_lasso.rmse_std,
                 df_lasso.rmse + df_lasso.rmse_std, color=color1, alpha=alpha)
ax1_y2.semilogx(df_lasso.alpha, df_lasso.nzp, '-o', **kwargs_nzp)
ax1_y2.fill_between(df_lasso.alpha, df_lasso.nzp - df_lasso.nzp_std,
                    df_lasso.nzp + df_lasso.nzp_std, color=color2, alpha=alpha)


# ardr
ax2.semilogx(df_ardr.threshold_lambda, df_ardr.rmse, '-o', **kwargs_rmse)
ax2.fill_between(df_ardr.threshold_lambda, df_ardr.rmse - df_ardr.rmse_std,
                 df_ardr.rmse + df_ardr.rmse_std, color=color1, alpha=alpha)
ax2_y2.semilogx(df_ardr.threshold_lambda, df_ardr.nzp, '-o', **kwargs_nzp)
ax2_y2.fill_between(df_ardr.threshold_lambda, df_ardr.nzp - df_ardr.nzp_std,
                    df_ardr.nzp + df_ardr.nzp_std, color=color2, alpha=alpha)

# rfe
ax3.plot(df_rfe.n_features, df_rfe.rmse, '-o', **kwargs_rmse)
ax3.fill_between(df_rfe.n_features, df_rfe.rmse - df_rfe.rmse_std,
                 df_rfe.rmse + df_rfe.rmse_std, color=color1, alpha=alpha)
ax3_y2.plot(df_rfe.n_features, df_rfe.nzp, '-o', **kwargs_nzp)

ax1.set_xlim([np.min(alphas), np.max(alphas)])
ax2.set_xlim([np.min(lambdas), np.max(lambdas)])
ax3.set_xlim([np.min(n_feature_vals), np.max(n_feature_vals)])

ax1.set_xlabel('Regularization parameter $\\alpha$', fontsize=fs)
ax2.set_xlabel(r'$\lambda$ - Threshold', fontsize=fs)
ax3.set_xlabel('Number of features', fontsize=fs)

ax1.set_title('LASSO', fontsize=fs)
ax2.set_title('automatic relevance determination', fontsize=fs)
ax3.set_title('recursive feature eliminiation', fontsize=fs)

for ax in [ax1, ax2, ax3]:
    ax.set_ylabel('RMSE validation (eV/Å)', color=color1, fontsize=fs)
    ax.set_ylim(ylim1)
    ax.tick_params(labelsize=fs)
    ax.tick_params(axis='y', labelcolor=color1)

for ax in [ax1_y2, ax2_y2, ax3_y2]:
    ax.set_ylabel('Number of non zero parameters', color=color2, fontsize=fs)
    ax.set_ylim(ylim2)
    ax.tick_params(labelsize=fs, labelcolor=color2)

plt.tight_layout()
plt.savefig('feature_selection_methods.svg')


# rmse - nzp curves
ms = 8
lw = 2.0
fig = plt.figure()
plt.plot(df_lasso.nzp, df_lasso.rmse, '-o', ms=ms, lw=lw, label='Lasso')
plt.plot(df_ardr.nzp, df_ardr.rmse, '-o', ms=ms, lw=lw, label='ARDR')
plt.plot(df_rfe.nzp, df_rfe.rmse, '-o', ms=ms, lw=lw, label='RFE')

plt.xlabel('Number of non zero parameters', fontsize=fs)
plt.ylabel('RMSE validation (eV/Å)', fontsize=fs)
plt.ylim(ylim1)
plt.legend(loc=1, fontsize=fs)
plt.gca().tick_params(labelsize=fs)
plt.tight_layout()
plt.savefig('rmse_nzp_curves.svg')


# plot resulting models
ms = 10
alpha = 0.8
ylim = [2e-3, 20]
fig = plt.figure(figsize=figsize)
ax1 = fig.add_subplot(1, 3, 1)
ax2 = fig.add_subplot(1, 3, 2)
ax3 = fig.add_subplot(1, 3, 3)

for ind, df in lasso_orbits.items():
    ax1.semilogy(df.radius, df.force_constant_norm, 'o', ms=ms, alpha=alpha,
                 label='alpha = {:.1e}'.format(alphas[ind]))

for ind, df in ardr_orbits.items():
    ax2.semilogy(df.radius, df.force_constant_norm, 'o', ms=ms, alpha=alpha,
                 label='f = {:.1e}'.format(lambdas[ind]))

for ind, df in rfe_orbits.items():
    ax3.semilogy(df.radius, df.force_constant_norm, 'o', ms=ms, alpha=alpha,
                 label='n_features = {:d}'.format(n_feature_vals[ind]))

ax1.set_title('LASSO', fontsize=fs)
ax2.set_title('automatic relevance determination', fontsize=fs)
ax3.set_title('recursive feature eliminiation', fontsize=fs)

for ax in [ax1, ax2, ax3]:
    ax.set_xlabel('Pair radius (A)', fontsize=fs)
    ax.set_ylim(ylim)
    ax.tick_params(labelsize=fs)
    ax.legend(fontsize=fs)
ax1.set_ylabel('Force constant norm (eV/A$^2$)', fontsize=fs)

plt.tight_layout()
plt.savefig('feature_selection_models.svg')
