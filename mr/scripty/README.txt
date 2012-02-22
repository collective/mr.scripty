Supported options
=================

The recipe supports any number of options, which are Python functions. As each option
is a Python function, it needs to possess an acceptable function identifier (see
http://docs.python.org/reference/lexical_analysis.html#grammar-token-identifier). For instance,
typical buildout options with hyphens (such as `environment-vars`) will be invalid.

Since the ini parser used with buildout doesn't preserve initial whitespace each line of your method should start
with a `...` followed by the whitespace as per normal python.
They will look like this ::

  [myscripts]
  recipe = mr.scripty
  MAX = 10
  function1 =
    ... x = range(1,int(self.MAX))
    ... return ' '.join(x)


The return value will be stored as a value in the buildout parts options which is available for
replacement in other buildout parts. What is returned is always converted to a string.

Options all in upper case are treated as string constants and added to the Recipe instance
as an attribute.

These functions are actually instance methods of the instance of the scripty recipe.
Methods are evaluated during the initialization of the Recipe instance, i.e.
after the cfg is read but before any `install` or 'update` recipe methods have been called.
Method names of `install`, `update` are treated specially and not evaluated during
initialization but rather during the install and update phases of building this
recipe instance.
These can be used as quick inplace replacement for creating a real recipe and have the same
semantics as detailed in http://pypi.python.org/pypi/zc.buildout#id3. In addition any option beggining
with `_` is not evaluated so can be used as a private method. Since these are methods `self` is
an available local variable which refers to the recipe instance. `self.options`, `self.buildout` and
`self.name` are also available.


Example usage
=============


Let's say you want to transform the a varnish:backends value to what can
be used inside haproxy::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = scripty echobackends echorepeat
    ...
    ... [varnish]
    ... backends =
    ... 	myhost.com:255.255.255.1
    ...     myhost2.com:125.125.125.1
    ...
    ... [scripty]
    ... recipe = mr.scripty
    ... backends =
    ...   ... res = ""
    ...   ... for line in self.buildout['varnish']['backends'].splitlines():
    ...   ...    if ':' not in line:
    ...   ...      continue
    ...   ...    host,dest = line.split(':')
    ...   ...    host = host.split('.')[0]
    ...   ...    res += "acl %s url_sub VirtualHostRoot/%s\\n" % (dest,host)
    ...   ... return res
    ... repeat =
    ...   ... opt_repeatx = int(self.options['repeatx'])
    ...   ... fun_repeatx = self.repeatx()
    ...   ... return '\\n'.join(["this is line %s"%i for i in range(1,opt_repeatx+1)])
    ... repeatx = return '10'
    ...
    ... [echobackends]
    ... recipe = mr.scripty
    ... install = print self.buildout['scripty']['backends']; return []
    ...
    ... [echorepeat]
    ... recipe = mr.scripty
    ... install =
    ...   ... script = self.buildout['scripty']
    ...   ... print script['repeat']
    ...   ... return []
    ... """)

Running the buildout gives us::

    >>> print 'start', system(buildout) 
    start...
    Installing echobackends.
    acl host url_sub VirtualHostRoot/255.255.255.1
    acl host2 url_sub VirtualHostRoot/125.125.125.1
    <BLANKLINE>
    Installing echorepeat.
    this is line 1
    this is line 2
    this is line 3
    this is line 4
    this is line 5
    this is line 6
    this is line 7
    this is line 8
    this is line 9
    this is line 10
    <BLANKLINE>

From this example you'll notice several things. Options that are part of a mr.scripty part are
turned into methods of the part instance and can call each other. In addition, each method can
be called from other buildout recipes by accessing the option via ${part:method} or in code via
self.buildout[part][method].

Another example
===============

The following example will make all the values of ports_base available with an offset added to
each one ::

    [ports_base]
    instance1=8101
    instance2=8102


    [ports]
    recipe=mr.scripty
    OFFSET = 1000
    init=
      ... for key,value in self.buildout['ports_base'].items():
      ...   self.options[key] = str(int(value)+int(self.OFFSET))
