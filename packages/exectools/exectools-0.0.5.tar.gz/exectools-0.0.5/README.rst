exectools

Using exectools
===============

.. code-block:: python

    
    # reload modules before importing

    > from exectools import _import, _from
    > _import('import foo as bar')
    > _import('foo as bar')
    > _import('from foo import bar, kaz')
    > _from('foo import bar')
    > _from('foo import bar as kaz')

    # execfile for python 3

    > from exectools import execfile
    > execfile('file.py')

    # make refresh helpers

    > from exectools import make_refresh
    > refresh_me = make_refresh(__file__)
    > refresh_me()

    # unload all modules matching regex pattern
    > from exectools import unload
    > unload('exect')

Changelog
=========

0.0.1: initial release (2021-09-24)

