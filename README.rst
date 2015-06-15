*Jasmine* integration for *unittest*
====================================

This package allows you to run `Jasmine <http://jasmine.github.io/>`_ unit
tests fully integrated with the *Python* standard module *unittest*.

The main use case is to run *JavaScript* tests for Python server APIs.


Quick start
-----------

To use this module, please follow these steps:

1. Add ``unittest-jasmine`` to the ``tests_require`` parameter to
   ``setuptools.setup()``.
2. Change or add the ``test_loader`` argument to ``setuptools.setup()`` to
   ``'unittest_jasmine.SetuptoolsLoader'``.
3. Add your *Jasmine* specs to your test package, and make sure the file names
   end with ``spec.js``.

If your project uses *npm* to manage dependencies, those will be automatically
updated when the tests are run using ``npm install``.


Advanced options
----------------

Pass additional options to *unittest-jasmine* by modifying the ``test_suite``
parameter to ``setuptools.setup()``; append the character ``'|'`` and then
the options separated by ``';'``::

    setuptools.setup(
        . . .
        test_suite='tests|option1=value1;option2={"flag":true}',
        . . .
    )

The value part of an option may be either *JSON* or a simple string. Anything
that is not parsable as *JSON* is treated as a simple string. A simple string
is treated as a *JSON* string.

The following options are recognised by *unittest-jasmine*:

lifecycle
    A module receiving notifications about the lifecycle of suites and tests.
    See `I need to run Python code before each test or suite`_ for more
    information.

spec_regex
    A regular expression used to find the spec files in the test directory.

test_directory
    The directory that contains the spec files. This must be an absolute path.

Any option not in this list will be passed on to the *Jasmine* ``loadConfig``
method.


Common tasks
------------


My *Jasmine* specs are not located in the same directory as my *Python* tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Override the default path to the spec files by setting the option
``test_directory``. This must be the absolute path to the directory containing
the spec files.


My *Jasmine* spec files do not end with ``spec.js``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Override the regular expression used to filter spec files from the test
directory by setting the option ``spec_regex``. This is used as a regular
expression to filter the files to include.

An example value is::

    setuptools.setup(
        . . .
        test_suite='tests|spec_regex=.*?-test\\.js',
        . . .
    )


I need to run *Python* code before each test or suite
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Set the option ``lifecycle`` to specify a module with functions handling the
setup and teardown of tests and suites.

The functions ``suite_setup``, ``suite_teardown``, ``test_setup`` and
``test_teardown``, if defined, will be called with the suite or test as
parameter. The functions will be called as instance methods of the respective
suites and tests.

You may copy templates for these functions from
``.../unittest_jasmine/_setuptools.py``.

An example value is::

    setuptools.setup(
        . . .
        test_suite='tests|lifecycle=test._jasmine_lifecycle',
        . . .
    )


I need to load *Jasmine* helper files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Set the option ``helper`` to a *JSON* encoded list of strings. The strings are
interpreted by *Jasmine* as paths to helper files, relative to the directory
containing the spec files; they must not be absolute paths.


I have specs written in *CoffeeScript*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To enable running tests written in *CoffeeScript*, first modify the option
``spec_regex`` to ensure that it also includes ``.coffee`` files, and then make
sure that one of your *Jasmine* helper files contains the expression
``require("coffee-script/register")``. An example value is::

    setuptools.setup(
        . . .
        test_suite='tests|spec_regex=.*?spec\\.(js|coffee);helpers=["cs.js"]',
        . . .
    )
