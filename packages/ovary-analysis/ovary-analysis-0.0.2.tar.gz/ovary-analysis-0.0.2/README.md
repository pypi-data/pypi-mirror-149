# ovary-analysis

Image processing pipeline for ultrasound images of ovaries.

# Installation
First, clone the repository

`git clone git@git.bsse.ethz.ch:iber/ovary-analysis.git`

Then, cd to the directory you cloned the repository into

`cd ovary-analysis`

Create a new python environment for the ovary-analysis package. If you are using anaconda, you can do the following

`conda create -n ovary-analysis python=3.7`

Activate your new environment

`conda activate ovary-analysis`

Install the ovary-analysis package with with. If you are just using the package, install using:

`pip install .`

If you want to install for development, use the pip editable mode:

`pip install -e .`

# Developer tools
We use black and flake8 for formatting assistance. To install them, run the following from the repository directory

`pip install -r requirements-dev.txt`

Finally, install the pre-commit hooks.

`pre-commit install`