=================================
ACT DR6 Multifrequency Likelihood
=================================

An external likelihood using `cobaya <https://github.com/CobayaSampler/cobaya>`_.

.. image:: https://img.shields.io/pypi/v/act_dr6_mflike.svg?style=flat
   :target: https://pypi.python.org/pypi/act_dr6_mflike
.. image:: https://github.com/ACTCollaboration/act_dr6_mflike/actions/workflows/testing.yml/badge.svg
   :target: https://github.com/ACTCollaboration/act_dr6_mflike/actions
   :alt: GitHub Workflow Status

Installing the code
-------------------

If you do not plan to dig into the code, you can simply install the
code with the following command

.. code:: shell

    python -m pip install act_dr6_mflike [--user]

Otherwise, you first need to clone this repository to some location

.. code:: shell

    git clone https://github.com/ACTCollaboration/act_dr6_mflike.git /where/to/clone

Then you can install the ``act_dr6_mflike`` likelihood and its dependencies *via*

.. code:: shell

    python -m pip install -e /where/to/clone

Installing ACT DR6 data
-----------------------

To install ACT D6 data, the easiest way is to use the ``cobaya-install`` binary and 
let it do the installation job. For instance, if you do the next command

.. code:: shell

    cobaya-install /where/to/clone/examples/act_dr6_example.yaml -p /where/to/put/packages

data and code such as `CAMB <https://github.com/cmbant/CAMB>`_ will be downloaded and installed
within the ``/where/to/put/packages`` directory. For more details, you can have a look to ``cobaya``
`documentation <https://cobaya.readthedocs.io/en/latest/installation_cosmo.html>`_.

Running/testing the code
------------------------

You can test the ``act_dr6_mflike`` likelihood by doing

.. code:: shell

    cobaya-run /where/to/clone/examples/act_dr6_example.yaml -p /where/to/put/packages

which should run a MCMC sampler for ACT DR6 official data file (*i.e.* ``dr6_data.fits`` in the
``act_dr6_example.yaml`` file) using the combination of TT, TE and EE spectra (*i.e.*
``polarizations: ['TT', 'TE', 'ET', 'EE']``). The results will be stored in the ``chains/mcmc``
directory.
