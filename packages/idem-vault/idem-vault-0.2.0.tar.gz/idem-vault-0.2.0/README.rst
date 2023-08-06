==========
Idem-vault
==========

.. image:: https://img.shields.io/badge/made%20with-pop-teal
   :alt: Made with pop, a Python implementation of Plugin Oriented Programming
   :target: https://pop.readthedocs.io/

.. image:: https://img.shields.io/badge/made%20with-python-yellow
   :alt: Made with Python
   :target: https://www.python.org/

About
=====

      An Idem plugin to manage resources of HashiCorp's Vault.

What is POP?
------------

This project is built with `pop <https://pop.readthedocs.io/>`__, a Python-based
implementation of *Plugin Oriented Programming (POP)*. POP seeks to bring
together concepts and wisdom from the history of computing in new ways to solve
modern computing problems.

For more information:

* `Intro to Plugin Oriented Programming (POP) <https://pop-book.readthedocs.io/en/latest/>`__
* `pop-awesome <https://gitlab.com/saltstack/pop/pop-awesome>`__
* `pop-create <https://gitlab.com/saltstack/pop/pop-create/>`__

Getting Started
===============

Prerequisites
-------------

* Python 3.7+
* git *(if installing from source, or contributing to the project)*

Installation
------------

.. note::

   If wanting to contribute to the project, and setup your local development
   environment, see the ``CONTRIBUTING.rst`` document in the source repository
   for this project.

If wanting to use ``idem-vault``, you can do so by either
installing from PyPI or from source.

Install from PyPI
+++++++++++++++++

.. code-block:: bash

    pip install idem-vault

Install from source
+++++++++++++++++++

.. code-block:: bash

   # clone repo
   git clone git@<your-project-path>/idem-vault.git
   cd idem-vault

   # Setup venv
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e .

Usage
=====

The first step is to setup the credential to Vault. Similarly to other Idem plugins, this is done via the `acct` tool.
Create a credential.yaml file like following:

.. code-block:: sls

    vault:
      default:
        address: http://127.0.0.1:8200
        token: Sb6lasdfsdf3ysfMNsdfd11

Encrypt the the credential file:

.. code:: bash

    acct encrypt credentials.yaml

output::

    -A9ZkiCSOjWYG_lbGmmkVh4jKLFDyOFH4e4S1HNtNwI=

Add the output token and the generated fernet file path to your environment:

.. code:: bash

    export ACCT_KEY="-A9ZkiCSOjWYG_lbGmmkVh4jKLFDyOFH4e4S1HNtNwI="
    export ACCT_FILE=$PWD/credentials.yaml.fernet

You are ready to use idem-vault to manage your Vault resources!!!

Roadmap
=======
Current Supported Resources states:
kv_v2.secret

Acknowledgements
================

* `Img Shields <https://shields.io>`__ for making repository badges easy.
