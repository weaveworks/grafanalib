===============
Release process
===============

* Pick a new version number (e.g. ``X.Y.Z``)
* Update `CHANGELOG <../CHANGELOG.rst>`_ with that number
* Update `setup.py <../setup.py>`_ with that number
* Tag the repo with ``vX.Y.Z``
* Upload to PyPI:

      .. code-block:: console

         $ rm -rf dist
         $ python setup.py sdist bdist_wheel
         $ twine upload dist/*
