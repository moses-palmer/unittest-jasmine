Release notes
=============

v1.0.2 - pkg_resources fixes
----------------------------
*  Make sure to actually include the *JavaScript* runner in the package.
*  Use ``__name__`` instead of ``__package__`` when loading runner using
   ``pkg_resources`` to work on *Python 3*.


v1.0.1 - Python 3 fixes
-----------------------
*  Corrected dynamic method addition to work with *Python 3*.
*  Allow using release maker script on *Python 3*.
*  Build a universal wheel when making a release.


v1.0 - Initial Release
----------------------
*  Initial release
