=================================
ACT DR6 Multifrequency Likelihood
=================================

An external likelihood using `cobaya <https://github.com/CobayaSampler/cobaya>`_.

.. image:: https://img.shields.io/github/actions/workflow/status/ACTCollaboration/act_dr6_mflike/testing.yml?branch=master
   :target: https://github.com/ACTCollaboration/act_dr6_mflike/actions
   :alt: GitHub Workflow Status

Installing the code
-------------------

If you do not plan to dig into the code or to play with the ``yaml`` files, you can simply install the
code directly from this repository

.. code:: shell

    $ pip install git+https://github.com/ACTCollaboration/act_dr6_mflike.git

Otherwise, you first need to clone this repository to some location

.. code:: shell

    $ git clone https://github.com/ACTCollaboration/act_dr6_mflike.git /where/to/clone

Then you can install the ``act_dr6_mflike`` likelihood and its dependencies *via*

.. code:: shell

    $ pip install -e /where/to/clone

Installing ACT DR6 data
-----------------------

Preliminary simulated data can be found at `NERSC
<https://portal.nersc.gov/cfs/sobs/users/xgarrido/act_dr6_sim>`_. You can download them by yourself
but you can also use the ``cobaya-install`` binary and let it do the installation job. For instance,
if you do the next command

.. code:: shell

    $ cobaya-install /where/to/clone/examples/act_dr6_example.yaml -p /where/to/put/packages

data and code such as `CAMB <https://github.com/cmbant/CAMB>`_ will be downloaded and installed
within the ``/where/to/put/packages`` directory. For more details, you can have a look to ``cobaya``
`documentation <https://cobaya.readthedocs.io/en/latest/installation_cosmo.html>`_.

Running/testing the code
------------------------

You can test the ``act_dr6_mflike`` likelihood by doing

.. code:: shell

    $ cobaya-run /where/to/clone/examples/act_dr6_example.yaml -p /where/to/put/packages

which should run a MCMC sampler for a simulated file (*i.e.* ``act_simu_sacc_000000.fits`` in the
``act_dr6_example.yaml`` file) using the combination of TT, TE and EE spectra (*i.e.*
``polarizations: ['TT', 'TE', 'ET', 'EE']``). The results will be stored in the ``chains/mcmc``
directory.
