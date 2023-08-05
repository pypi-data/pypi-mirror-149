.. _majerti: http://majerti.fr
.. _readthedocs: http://quicklogging.readthedocs.io/en/latest/
.. _github: https://github.com/majerteam/quicklogging
.. _travis-ci: https://travis-ci.org/majerteam/quicklogging/
.. _stringimporter: https://github.com/majerteam/stringimporter

Documentation for quicklogging
================================

Resources
-------------

* doc: |docs| - read the doc on readthedocs_ (github rst is broken)
* source code: on github_
* package: |package| 
* ci tests: |citests|


What is quicklogging
---------------------

*quicklogging* is a Python :py:mod:`logging` wrapper to 

    * remove a bit of logging boilerplate,
    * redirect print output.

``quicklogging`` transparently provides a logger with a name relevant 
to the code at hand: 

.. important:: 

    The name of the logger is the name of the module making the call.


For instance, if you log from ``project/models/chair.py``, your logger will be named ``project.models.chair``.

This is a very important feature:

*Advantage #1 of this naming scheme* 

        the *configuration* of the :py:class:`logging.Logger` s and handlers is much 
        easier —muting, changing verbosity for a particular piece of code etc

*Advantage #2*

        we can provide a :py:func:`quicklogging.catch_prints` and a :py:func:`quicklogging.warn_prints`  functionality to catch calls 
        to print() from specific modules (typically: the module you're editing).

Licence, original authors
---------------------------

* MIT (see file ``LICENCE`` ).
* authors: majerti_ - Feth AREZKI

Requirements
--------------

Python versions
................

I tested 3.5 to 3.10 without annoyances.

Cannot test, but should work because I don't know of API changes:

* Python 2.7: *testing* NOT ok (Python 2.7 doesn't have :py:class:`importlib.abc.SourceLoader`
 
Libs required
.................

None ! unless you're running the tests (then you need stringimporter_).
.
So I've got this easy badge: |requirements|.


Doc contents
-------------

(if toctree is not displayed, then build the docs with sphinx or read them on readthedocs : |docs|.

.. toctree::
   :numbered:
   :maxdepth: 2

   user_guide
   task_oriented
   source_doc
   logging_survival

   
.. |package| image:: https://badge.fury.io/py/quicklogging.svg
        :target: https://badge.fury.io/py/quicklogging

.. |docs| image:: https://readthedocs.org/projects/quicklogging/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://quicklogging.readthedocs.io/en/latest/?badge=latest

.. |requirements| image:: https://requires.io/github/majerteam/quicklogging/requirements.svg?branch=master
     :target: https://requires.io/github/majerteam/quicklogging/requirements/?branch=master
     :alt: Requirements Status

.. |citests| image:: https://github.com/majerteam/quicklogging/actions/workflows/python-package.yml/badge.svg
    :alt: Tests status with github actions
    :target: https://github.com/majerteam/quicklogging/actions/workflows/python-package.yml

