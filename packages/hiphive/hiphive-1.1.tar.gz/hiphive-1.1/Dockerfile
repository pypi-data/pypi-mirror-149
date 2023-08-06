# Base image
FROM continuumio/miniconda3

# Base packages
# git is used in hiphive-testing and included here to avoid two near identical images
RUN \
  apt-get update -qy && \
  apt-get upgrade -qy && \
  apt-get install -qy \
    git \
    graphviz \
    pandoc \
    python3-pip \
    zip

RUN \
  conda install -c conda-forge phono3py=2.0.0

RUN \
  pip3 install --upgrade \
    pip \
  && \
  pip3 install --upgrade \
    coverage \
    flake8 \
    nbmake \
    pytest \
    setuptools_scm \
    twine \
    xdoctest

# Packages needed for hiphive
# (The version limit on numpy is dictated by numba.)
RUN \
  pip3 install \
    h5py \
    numba>=0.55 \
    'numpy<1.22' \
    sympy>=1.1 \
  && \
  pip3 install \
    ase \
    scikit-learn \
    scipy>=1.0.0 \
    spglib

# Packages for building documentation
RUN \
  pip3 install --upgrade \
    sphinx_autodoc_typehints \
    sphinx-rtd-theme \
    sphinx_sitemap \
    sphinxcontrib-bibtex \
    cloud_sptheme \
    nbsphinx \
  && \
  pip3 install --upgrade \
    jinja2==3.0.3


# Packages for running examples
RUN \
  pip3 install \
    pandas \
    phonopy

CMD /bin/bash
