import numpy as np
from matplotlib import pyplot as plt
from sklearn.manifold import TSNE
from hiphive import StructureContainer


def get_partial_fit_matrix(sc, tags, n_rows):
    M_list, tag_list = [], []
    for tag in tags:
        structure_inds = [i for i, fs in enumerate(sc) if fs.user_tag == tag]
        M, _ = sc.get_fit_data(structure_inds)
        M_list.append(M[:n_rows, :])
        tag_list.extend([tag] * n_rows)
    return np.vstack(M_list), tag_list


# parameters
n_rows = 300
perplexity = 30
learning_rate = 50
n_iter = 2000

# read data
sc = StructureContainer.read('structure_container')
unique_tags = set(fs.user_tag for fs in sc)
M, tags = get_partial_fit_matrix(sc, unique_tags, n_rows)


# t-SNE transformation
tsne = TSNE(perplexity=perplexity, n_iter=n_iter, learning_rate=learning_rate,
            verbose=1)
XY_tsne = tsne.fit_transform(M)


# plot
ms = 100
alpha = 0.25
fs = 14

for unique_tag in unique_tags:
    indices = [tag == unique_tag for tag in tags]
    plt.scatter(XY_tsne[indices, 0], XY_tsne[indices, 1], ms, alpha=alpha,
                label=unique_tag)

legend = plt.legend(fontsize=fs)
for lh in legend.legendHandles:
    lh.set_alpha(1)

plt.tight_layout()
plt.savefig('Ti_tsne_analysis.svg')
