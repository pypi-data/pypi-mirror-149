dlpoly-py
=========

.. image:: https://badge.fury.io/py/dlpoly-py.svg
   :target: https://badge.fury.io/py/dlpoly-py

.. image:: https://img.shields.io/conda/vn/conda-forge/dlpoly-py.svg
   :target: https://anaconda.org/conda-forge/dlpoly-py

dlpoly-py package contains tools to read input and output for DL_POLY
it can also produce inputs and be mixed with other python packages
like ASE, MDAnalysis, MDAnse or pymatgen

install
-------

You need Python 3.6 or later to run `dlpoly-py`. You can have multiple Python
versions (2.x and 3.x) installed on the same system without problems.

To install Python 3 for different Linux flavors, macOS and Windows, packages
are available at
`https://www.python.org/getit <https://www.python.org/getit/>`_

**Using pip**

**pip** is the most popular tool for installing Python packages, and the one
included with modern versions of Python.

`dlpoly-py` can be installed with `pip`

.. code:: bash

    pip install dlpoly-py

**Note:**

Depending on your Python installation, you may need to use `pip3` instead of `pip`.

.. code:: bash

    pip3 install dlpoly-py

Depending on your configuration, you may have to run `pip` like this:

.. code:: bash

    python3 -m pip install dlpoly-py

**Using pip (GIT Support)**

`pip` currently supports cloning over `git`

.. code:: bash

    pip install git+https://gitlab.com/drFaustroll/dlpoly-py.git

For more information and examples, see the
`pip install <https://pip.pypa.io/en/stable/reference/pip_install/#id18>`_
reference.

**Using a virtual environment**

.. code:: bash

    # create virtual env
    virtualenv3 venv/dlpoly
    source venv/dlpoly/bin/activate
    pip3 install dlpoly-py

**Using conda**

**conda** is the package management tool for Anaconda Python installations.

Installing `dlpoly-py` from the `conda-forge` channel can be achieved by adding
`conda-forge` to your channels with:

.. code:: bash

    conda config --add channels conda-forge

Once the `conda-forge` channel has been enabled, `dlpoly-py` can be installed
with:

.. code:: bash

    conda install dlpoly-py

It is possible to list all of the versions of `dlpoly-py` available on your
platform with:

.. code:: bash

    conda search dlpoly-py --channel conda-forge

usage
-----

Examples can be found in https://gitlab.com/drFaustroll/dlpoly-py/-/tree/devel/examples

sime run using Ar data from above folder.


.. code:: python

   from dlpoly import DLPoly

   dlp="/home/drFaustroll/playground/dlpoly/dl-poly-alin/build-yaml/bin/DLPOLY.Z"

   dlPoly = DLPoly(control="Ar.control", config="Ar.config",
                   field="Ar.field", workdir="argon")
   dlPoly.run(executable=dlp,numProcs = 4)

   # change temperature and rerun, from previous termination
   dlPoly = DLPoly(control="Ar.control", config="argon/REVCON", destconfig="Ar.config",
                field="Ar.field", workdir="argon-T310")
   dlPoly.control.temp = 310.0
   dlPoly.run(executable=dlp,numProcs = 4)

alternatively you can set the environment variable DLP_EXE to point to DL_POLY_4 executable and remove the executable parameter from
run.

.. code:: bash

   export DLP_EXE="/home/drFaustroll/playground/dlpoly/dl-poly-alin/build-yaml/bin/DLPOLY.Z"

.. code:: python

   from dlpoly import DLPoly

   dlPoly = DLPoly(control="Ar.control", config="Ar.config",
                   field="Ar.field", workdir="argon")
   dlPoly.run(numProcs = 4)

   # change temperature and rerun, from previous termination
   dlPoly = DLPoly(control="Ar.control", config="argon/REVCON", destconfig="Ar.config",
                field="Ar.field", workdir="argon-T310")
   dlPoly.control.temp = 310.0
   dlPoly.run(numProcs = 4)



authors
-------

 - Alin M Elena, Daresbury Laboratory, UK
 - Jacob Wilkins, University of Oxford, UK

contact
-------

  - please report issues in the `gitlab tracker <https://gitlab.com/drFaustroll/dlpoly-py/-/issues>`_
  - available in the `matrix room <https://matrix.to/#/!MsDOMMiBCBkTvqGxOz:matrix.org/$-Tgf2pIJ9CD732cbG5FEawZiRy8CJlexMbgwD25vvBQ?via=matrix.org>`_

