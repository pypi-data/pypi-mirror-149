=======================
python-crfsuite-openmp
=======================

.. image:: https://travis-ci.org/bratao/python-crfsuite.svg?branch=master
    :target: https://travis-ci.org/bratao/python-crfsuite

.. image:: https://img.shields.io/pypi/v/python-crfsuite-openmp.svg?style=flat-square
    :target: https://pypi.python.org/pypi/python-crfsuite-openmp
    :alt: pypi Version


python-crfsuite-open is fork of python-crfsuite with OpenMP support enabled, a (Even more) FAST sequential tagger

ChangeLog
============
* 1.0.1 - Heavly penalize Unseen transitions
* 1.0.0 - OpenMP support. Utilize all CPU cores during training

Installation
============

Using ``pip``::

    pip install python-crfsuite-openmp



Usage
=====

See docs_ and an example_.

.. _docs: http://python-crfsuite.rtfd.org/
.. _example: https://github.com/scrapinghub/python-crfsuite/blob/master/examples/CoNLL%202002.ipynb

See Also
========

sklearn-crfsuite_ is a python-crfsuite wrapper which provides
API similar to scikit-learn.

.. _sklearn-crfsuite: https://github.com/TeamHG-Memex/sklearn-crfsuite

Contributing
============

* Source code: https://github.com/scrapinghub/python-crfsuite
* Issue tracker: https://github.com/scrapinghub/python-crfsuite/issues

Feel free to submit ideas, bugs reports, pull requests or regular patches.

In order to run tests, install Cython_ (> 0.24.1)  and tox_, then type

::

    ./update_cpp.sh; tox

from the source checkout.

Please don't commit generated cpp files in the same commit as other files.

.. _Cython: http://cython.org/
.. _tox: http://tox.testrun.org

Authors and Contributors
========================

Original authors are Terry Peng <pengtaoo@gmail.com> and
Mikhail Korobov <kmike84@gmail.com>. Many other people contributed;
some of them can be found at github Contributors_ page.

Bundled CRFSuite_ C/C++ library is by Naoaki Okazaki & contributors.

.. _Contributors: https://github.com/scrapinghub/python-crfsuite/graphs/contributors

License
=======

python-crfsuite-openmp is licensed under MIT license.
CRFsuite_ library is licensed under BSD license.

.. _CRFsuite: https://github.com/chokkan/crfsuite

