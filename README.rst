Mr.Scripty
==========
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

Init
----

The one special exception to the above is the ``init`` option, which
is not stored.  Utilising this option allows you to reduce the need for
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


Install and Update
------------------
These functions are actually instance methods of the instance of the scripty
recipe.  Methods are evaluated during the initialization of the Recipe
instance, i.e.  after the cfg is read but before any `install` or 'update`
recipe methods have been called.  Method names of `install`, `update` are
treated specially and not evaluated during initialization but rather during
the install and update phases of building this recipe instance.  These can be
used as quick in-place replacement for creating a real recipe and have the
same semantics as detailed in http://pypi.python.org/pypi/zc.buildout#id3.

- Code repository: https://github.com/collective/mr.scripty
- Questions and comments to https://github.com/collective/mr.scripty
- Report bugs at https://github.com/collective/mr.scripty

Examples
========

`Examples <http:///./mr/scripty/README.rst>`_.