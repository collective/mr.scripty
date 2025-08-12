Mr.Scripty
==========

|pyversions| |dependabot| |meta| |tests|

.. |pyversions| image:: https://img.shields.io/badge/python-3.9%2B-blue.svg?style=flat
    :target: https://www.python.org/downloads/

.. |dependabot| image:: https://github.com/collective/mr.scripty/actions/workflows/dependabot/dependabot-updates/badge.svg
    :target: https://github.com/collective/mr.scripty/actions/workflows/dependabot/dependabot-updates

.. |meta| image:: https://github.com/collective/mr.scripty/actions/workflows/meta.yml/badge.svg
    :target: https://github.com/collective/mr.scripty/actions/workflows/meta.yml

.. |tests| image:: https://github.com/collective/mr.scripty/actions/workflows/test-matrix.yml/badge.svg
    :target: https://github.com/collective/mr.scripty/actions/workflows/test-matrix.yml


A quick way to build recipes by using python directly inside zc.buildout

.. contents::


Supported options
=================

The recipe supports any number of options, which are Python functions.  Since
the ini parser used with buildout doesn't preserve initial whitespace each
line of your method should start with a `...` followed by the whitespace as
per normal python.  They will look like this::

  [myscripts]
  recipe = mr.scripty
  MAX = 10
  function1 =
    ... x = range(1,int(self.MAX))
    ... return ' '.join(x)

  [myrecipe]
  recipe = something.recipe
  argument = ${myscripts:function1}


The return value will be stored as a value in the buildout parts options which
is available for replacement in other buildout parts. What is returned is
always converted to a string.


Functions vs Constants
----------------------

Options all in upper case are treated as string constants and added to the
Recipe instance as an attribute. All other options will be treated as python
functions.

As each option is a Python function or variable, it needs to possess an acceptable
function identifier (see
http://docs.python.org/reference/lexical_analysis.html#grammar-token-identifier).
For instance, typical buildout options with hyphens (such as
`environment-vars`) will be invalid.

Since these functions are actually methods `self` is an available local variable
which refers to the recipe instance. `self.options`, `self.buildout` and
`self.name` are available.

Any option beginning with `_` is not evaluated so can be used as a
private function.

Init, Install and Update
------------------------

There are three special functions which are evaluated regardless if they
are called from another recipe and whose value isn't stored.

``init``: Init is called every time the recipe is loaded. This function allows you
to reduce the need for
multiple functions that may do similar jobs, remove the need for a dummy
option in order to execute arbitrary code (and other uses), like so::

    [myscripts]
    recipe = mr.scripty
    init =
        ... import math
        ... self.options['pi'] = str(math.pi)
        ... self.options['e'] = str(math.e)
        ... self.options['sqrt_two'] = str(math.sqrt(2))

After running buildout, the options ``pi``, ``e``, and ``sqrt_two`` will all
be available for use against the ``myscripts`` section like so:
``${myscripts:sqrt_two}``. See the example regarding `Offsetting port
numbers`_ for more information.


``install`` is called if the arguments (functions or constants) have changed
since the last run or if it's never run before.

``update`` is called each time (but after init)

These can be
used as quick in-place replacement for creating a real recipe and have the
same semantics as detailed in
http://www.buildout.org/en/latest/docs/tutorial.html?highlight=update#writing-recipes.


Bugs and Repo
=============

- Code repository: https://github.com/collective/mr.scripty
- Questions and comments to https://github.com/collective/mr.scripty
- Report bugs at https://github.com/collective/mr.scripty

Examples
========

`See Examples <mr/scripty/README.rst>`_.
