# Overview

## Writing documentation and user guides

We use [Sphinx](https://www.sphinx-doc.org/en/master/), and a few add-ons, most importantly [nbsphinx](https://nbsphinx.readthedocs.io/) so we can write using markdown and Jupyter notebooks, stored as ipynbs (which are not executed), or py:percent scripts or [quarto](https://quarto.org/) markdown (which are executed). The latter being the preferred option.

This also covers how to document separate infrastructure repositories whose documentation is pulled in.

## Organisation

The documentation mainly lives in the docs/source folder. 
Documentation for any infrastructure with it's own repository lives in the repository, so we can keep the documentation near the code.
This is the "relevant" high-level folder structure for this repository:

```
├── docs                      <- Documentation folder.
│   ├── build                 <- Placeholder for built docs.
│   ├── source                <- Documentation scripts.
│   │   ├── index.rst         <- Main file.
│   │   ├── contributing.rst  <- How to docs.
│   │   └── etc.
│   └── etc.                  <- Other necessary files.
│
└── etc.
```

## Serving documentation locally

It can be helpful to build and serve the documentation locally in order to QA any changes. To do so:

1. Clone `git@github.com:cmagovuk/selene-core.git`.
2. Activate the py39 conda environment
   `conda activate py39`
3. Navigate to the docs directory (the one with the Makefile), install requirements, pull submodules and build the html
   `cd selene-core/docs`
   `make requirements`
   `make html`
5. Staying in the same directory, build and run the docker image which serves the documentation
   `make serve`