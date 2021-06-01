Release Notes
=============

v0.2.0 (June 1, 2021):
-------

Improvements:
  - update ``pywnb`` and ``hdmf`` dependencies to use the newest versions and improve version matching constraint to be compatible with future bug fixes and minor releases

Fixes:
  - replace deprecated sphinx call to ``add_stylesheet`` with ``add_css_file`` (`ref <https://github.com/sphinx-doc/sphinx/issues/7747>`_)


v0.1.1 (April 23, 2021):
-------

Hotfix release.

Fixes:
  - constrain ``hdmf`` dependency to version 2.4.0 until the just-released 2.5.0 can be tested
  - update documentation to indicate how to install ``ndx-nirs`` from PyPI
  - constrain wheel to be python 3 only


v0.1.0 (April 22, 2021):
-------

Initial release version of the extension which includes support for several standard NIRS datatypes.
