==============
setuptools-npm
==============

Plugin for setuptools to run npm commands.

-----
Usage
-----

This command provides `npm_install` and `npm_run` commands.

Run `python setup.py npm_install --help` or `python setup.py npm_run --help`
for available options.

`npm_not_skipped` is a helper function that can be used as predicate for
distutils subcommand. It evaluates to `True` if env variable `SKIP_NPM`
is not defined. This variable is exclusive to this helper function and
is not evaluated in `npm_install` and `npm_run` commands themselves.

-------
Example
-------

Let's say you have defined `build` command in `package.json` and you'd like
to run `npm clean-install` and `npm run build` each time you run `setup.py build`.
You'd configure your project like this:

.. code-block::

   # pyproject.toml
   [build-system]
   requires = ["setuptools", "setuptools-npm"]
   build-backend = "setuptools.build_meta"

.. code-block::

   # setup.py
   from distutils.command.build import build
   from setuptools import setup
   from setuptools_npm import npm_not_skipped

   class custom_build(build):
       sub_commands = [
           ('npm_install', npm_not_skipped),
           ('npm_run', npm_not_skipped),
       ] + build.sub_commands

   setup(cmdclass={'build': custom_build, 'sdist': custom_sdist})

.. code-block::

   # setup.cfg
   [npm_run]
   script = build
