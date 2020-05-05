===============
Release process
===============

Pre-release
-----------

* Pick a new version number (e.g. ``X.Y.Z``)
* Update `CHANGELOG <https://github.com/weaveworks/grafanalib/blob/master/CHANGELOG.rst>`_ with that number
* Update `setup.py <https://github.com/weaveworks/grafanalib/blob/master/setup.py>`_ with that number

Smoke-testing
-------------

* Run

      .. code-block:: console

         $ python setup.py install

* Check ``~/.local/bin/generate-dashboard`` for the update version.
* Try the example on `README <https://github.com/weaveworks/grafanalib/blob/master/README.rst>`_.

Releasing
---------

* Head to `<https://github.com/weaveworks/grafanalib/releases/new>`_ and create the release there.
* Wait for GitHub Actions to complete the build and release.
* Confirm on `<https://pypi.org/project/grafanalib/>`_ that the release made it there.

Follow-up
---------

* Run

      .. code-block:: console

         $ pip intall grafanalib -U

* Check if the upgrade worked and the test above still passes.
