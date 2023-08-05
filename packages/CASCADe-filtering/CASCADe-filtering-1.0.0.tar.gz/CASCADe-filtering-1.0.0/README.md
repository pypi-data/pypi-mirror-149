
[![pipeline status](https://gitlab.com/jbouwman/cascade-filtering/badges/main/pipeline.svg)](https://gitlab.com/jbouwman/cascade-filtering/commits/main)

#  <span style="color:#1F618D">CASCADe-filtering</span>

This package is a sub package of the <span style="color:#1F618D">CASCADe </span> package, developed within the EC Horizons 2020 project
<span style="color:#FF0000">Exoplanets A </span>. It contains functionality
to detect and flag cosmic ray hits in spectral images, and to create cleaned and filtered spectral images, which can be used for spectral extraction.

## Installing <span style="color:#1F618D">CASCADe-filtering</span>

The easiest way to install the <span style="color:#1F618D">CASCADe-filtering </span>
package is to create an Anaconda environment, download the distribution from PyPi,
and install the package in the designated Anaconda environment with the following
commands:

```bash

conda create --name cascade-filtering python=3.9 ipython
conda activate cascade-filtering
pip install CASCADe-filtering

```

This will install all code and scripts you need for the package to work.

## Installing the <span style="color:#1F618D">CASCADe-filtering</span> examples

The <span style="color:#1F618D">CASCADe-filtering </span> package comes with
several examples, demonstrating how to detect and filter cosmic hits from
spectroscopic images.  If the package is installed from PypPi, the example
jupyter notebooks and simulated data need be downloaded from the GitLab
repository. To initialize the data download one can use the following bash command
in the Anaconda environment:

```bash

setup_cascade-filtering.py

```

or alternatively from within the python interpreter:

```python

from cascade_filtering.initialize import setup_examples
setup_examples()

```

The additional downloaded data also includes examples and observational data to
try out the <span style="color:#1F618D">CASCADe </span> package, which are explained
below.

> **_NOTE:_**  The data files will be downloaded by default to a `CASCADeSTORAGE/` directory in the users home directory. If a different location is preferred, please read the section on how to set the <span style="color:#1F618D">CASCADe </span>
`CASCADE_STORAGE_PATH` environment variable first. For details in the
environment variables we refer to the documentation of the
<span style="color:#1F618D">CASCADe </span> main package.

## Installing alternatives for the <span style="color:#1F618D">CASCADe-filtering</span> package

The <span style="color:#1F618D">CASCADe-filtering </span> code can also be
downloaded from GitLab directly by either using git or pip. To download and
install with a single command using pip, type in a terminal the following command

```bash

pip install git+git://gitlab.com/jbouwman/CASCADe-filtering.git@main

```

which will download the latest version. For other releases replace the `main`
branch with one of the available releases on GitLab. Alternatively, one can first
clone the repository and then install, either using the HTTPS protocol:

```bash

git clone https://gitlab.com/jbouwman/CASCADe-filtering.git

```

or clone using SSH:

```bash

git clone git@gitlab.com:jbouwman/CASCADe-filtering.git

```

Both commands will download a copy of the files in a folder named after the
project's name. You can then navigate to the directory and start working on it
locally. After accessing the root folder in a terminal, type

```bash

pip install .

```

to install the package.

In case one is installing <span style="color:#1F618D">CASCADe-filtering </span> directly from GitLab, and one is using Anaconda,  make sure a cascade environment
is created and activated before using our package. For convenience, in the
<span style="color:#1F618D">CASCADe-filtering  </span> main package directory an
environment.yml can be found. You can use this yml file to create or update the
cascade Anaconda environment. If you not already had created an cascade environment
execute the following command:

```bash

conda env create -f environment.yml

```

In case you already have an cascade environment, you can update the necessary
packages with the following command (also use this after updating
<span style="color:#1F618D">CASCADe-filtering  </span> itself):

```bash

conda env update -f environment.yml

```

Make sure the <span style="color:#1F618D">CASCADe-filtering </span>- package is
in your path. You can either set a `PYTHONPATH` environment variable pointing to
the location of the <span style="color:#1F618D">CASCADe </span>-filtering package
on your system, or when using anaconda with the following command:

```bash

conda develop <path_to_the_CASCADe_package_on_your_system>/CASCADe-filtering

```

## Using  <span style="color:#1F618D">CASCADe-filtering </span>

The <span style="color:#1F618D">CASCADe-filtering </span> distribution comes with
several working examples and test data sets which can be found in the examples directory of the <span style="color:#1F618D">CASCADe-filtering </span> distribution
on GitLab, or have been installed locally with the commands outlined above.
The example jupyter notebooks explain and demonstrate the basic usage of the
filtering modules, and use simulated JWST/MIRI low resolution spectroscopic data
as an example how to identify and remove cosmic hits. To run the examples make
sure that the conda cascade-filtering environment can be found by the jupyter
server. This can be achieved with the following command:  

```bash

python -m ipykernel install --user --name=cascade-filtering

```

after which the notebooks can be viewed and excecuted with jupyter which can be
started with.

```bash

jupyter notebooks

```

## Documentation

The full documentation can be found online at:

```

https://jbouwman.gitlab.io/CASCADe-filtering/


```

Alternatively, the documentation can be found in the `docs`  directory of the
<span style="color:#1F618D">CASCADe-filtering </span> GitLab repository.
After cloning the git repository, the full documentation can be generated
by executing in the in the `docs` directory the following commands:

```bash

make html
make latexpdf

```

The generated HTML and PDF files will be located in the `build/html` and
`build/latex` sub-directories of the main documentation directory, respectively.

Documentation on the <span style="color:#1F618D">CASCADe </span> main
package can be found at:

```

https://jbouwman.gitlab.io/CASCADe/


```

## Acknowledgments

The <span style="color:#1F618D">CASCADe-filtering </span> code was developed by
Jeroen Bouwman, with contributions from the following collaborators:

Juergen Schreiber (MPIA)

This work was supported by the European Unions Horizon 2020 Research and
Innovation Programme, under Grant Agreement N 776403.

## Publications

https://ui.adsabs.harvard.edu/abs/2021AJ....161..284M/abstract

https://ui.adsabs.harvard.edu/abs/2021A%26A...646A.168C/abstract

https://ui.adsabs.harvard.edu/abs/2020ASPC..527..179L/abstract

https://exoplanet-talks.org/talk/271
