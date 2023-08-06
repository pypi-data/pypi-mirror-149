*****************
Installing Pebble
*****************

Installing from PyPI
====================

Packages for Pebble are published on the `Python Package Index`_ under
the name ``incenp.pebble``. To install the latest version from PyPI:

.. _Python Package Index: https://pypi.org/project/incenp.pebble/

.. code-block:: console

   $ pip install -U incenp.pebble


Installing from source
======================

You may download a release tarball from the `homepage`_ or from the
`release page`_, and then proceed to a manual installation:

.. _homepage: https://incenp.org/dvlpt/pebble.html
.. _release page: https://git.incenp.org/damien/pebble/releases

.. code-block:: console

   $ tar zxf incenp.pebble-1.0.0.tar.gz
   $ cd incenp.pebble-1.0.0
   $ python setup.py build
   $ python setup.py install

You may also clone the repository:

.. code-block:: console

   $ git clone https://git.incenp.org/damien/pebble.git

and then proceed as above.


Dependencies
============

Pebble requires the following Python dependencies to work:

* `sjcl <https://github.com/berlincode/sjcl>`_
* `requests <http://python-requests.org/>`_
* `click <https://palletsprojects.com/p/click/>`_
* `click-shell <https://github.com/clarkperkins/click-shell>`_

If you install Pebble from the Python Package Index with `pip` as
described above, those dependencies should be automatically installed if
they are not already available on your system.


Testing the installation
========================

Once installed, Pebble may be invoked from the command line by calling
the ``pbl`` program. You can check whether it has been installed
correctly by running the following command:

.. code-block:: console

   $ pbl --version
   pbl (Pebble 1.0.0)
   Copyright © 2018–2021 Damien Goutte-Gattat

   This program is released under the GNU General Public License.
   See the COPYING file or <http://www.gnu.org/licenses/gpl.html>.
