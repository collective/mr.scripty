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


The return value will be stored as a value in the buildout parts options which
is available for replacement in other buildout parts. What is returned is
always converted to a string.

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

As each option is a Python function, it needs to possess an acceptable
function identifier (see
http://docs.python.org/reference/lexical_analysis.html#grammar-token-identifier).
For instance, typical buildout options with hyphens (such as
`environment-vars`) will be invalid.

Options all in upper case are treated as string constants and added to the
Recipe instance as an attribute.

These functions are actually instance methods of the instance of the scripty
recipe.  Methods are evaluated during the initialization of the Recipe
instance, i.e.  after the cfg is read but before any `install` or 'update`
recipe methods have been called.  Method names of `install`, `update` are
treated specially and not evaluated during initialization but rather during
the install and update phases of building this recipe instance.  These can be
used as quick in-place replacement for creating a real recipe and have the
same semantics as detailed in http://pypi.python.org/pypi/zc.buildout#id3. In
addition any option beginning with `_` is not evaluated so can be used as a
private method. Since these are methods `self` is an available local variable
which refers to the recipe instance. `self.options`, `self.buildout` and
`self.name` are also available.

Example usage
=============

Tranforming Varnish backends for HAProxy
----------------------------------------

Let's say you want to transform a ``varnish:backends`` value to what can
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
    ...   ...    host, dest = line.strip().split(':')
    ...   ...    host = host.split('.')[0]
    ...   ...    res += "acl {} url_sub VirtualHostRoot/{}\\n".format(host, dest)
    ...   ... return res
    ... repeat =
    ...   ... opt_repeatx = int('10')
    ...   ... fun_repeatx = self.repeatx()
    ...   ... return '\\n'.join(["this is line %s"%i for i in range(1,opt_repeatx+1)])
    ... repeatx = return '10'
    ...
    ... [echobackends]
    ... recipe = mr.scripty
    ... install = print(self.buildout['scripty']['backends']); return []
    ...
    ... [echorepeat]
    ... recipe = mr.scripty
    ... install =
    ...   ... script = self.buildout['scripty']
    ...   ... print(script['repeat'])
    ...   ... return []
    ... """)

Running the buildout gives us::

    >>> print(system(buildout))
    Installing scripty.
    Installing echobackends.
    acl host url_sub VirtualHostRoot/255.255.255.1
    acl host2 url_sub VirtualHostRoot/125.125.125.1
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
    this is line 10...

From this example you'll notice several things. Options that are part of a
`mr.scripty` part are turned into methods of the part instance and can call
each other. In addition, each method can be called from other buildout recipes
by accessing the option via ``${part:method}`` or in code via
``self.buildout[part][method]``.

Offsetting port numbers
-----------------------

The following example will make all the values of ports_base available with an
offset added to each one.  This example demonstrates the special ``init``
option, which enables you to run a special function where the result
is not stored against the part within buildout::

    [ports_base]
    instance1=8101
    instance2=8102

    [ports]
    recipe = mr.scripty
    OFFSET = 1000
    init =
        ... for key,value in self.buildout['ports_base'].items():
        ...     self.options[key] = str(int(value)+int(self.OFFSET))

So, the usage of ``init`` enables us to create options against the ``[ports]``
section using arbitrary code.  In the example above, this will result in all
of the options under ``[ports_base]`` being processed to add the ``OFFSET``
value to the port.  The end result is that other sections of buildout can now
reference ``${ports:instance1}`` and ``${ports:instance2}``, which will have
values of 9101 and 9102 respectively.

Different download links for certain architectures
--------------------------------------------------

This example usage shows how to alter download links for third-party libraries
based upon whether the host platform is 32 or 64-bit. Note that the example
uses Python 2.6 or later::

    [buildout]
    parts =
        ...
        download

    [scripty]
    recipe = mr.scripty
    DOWNLOAD_URL_64 = http://site.com/64bit.tgz
    DOWNLOAD_URL_32 = http://site.com/32bit.tgz
    download_url =
        ... import platform
        ... is_64bit = any(['64' in x for x in platform.architecture()])
        ... return is_64bit and self.DOWNLOAD_URL_64 or self.DOWNLOAD_URL_32

    [download]
    recipe = hexagonit.recipe.download
    url = ${scripty:download_url}

Checking existence of directories
---------------------------------

This example tests the existence of a list of directories and selects
the first one that can be found on the system.  In this particular example,
we look through a list of potential JDK directories, as the location will
differ across Linux distributions, in order to install an egg that depends
on having a Java SDK install available::

    [buildout]
    parts =
        ...
        jpype

    [scripty]
    recipe = mr.scripty
    JAVA_PATHS =
        /usr/lib/jvm/java-6-openjdk
        /etc/alternatives/java_sdk
        ${buildout:directory}
    java =
        ... import os
        ... paths = self.JAVA_PATHS.split('\n')
        ... exists = [os.path.exists(path) for path in paths]
        ... return paths[exists.index(True)]

    [java-env]
    JAVA_HOME = ${scripty:java}

    [jpype]
    recipe = zc.recipe.egg:custom
    egg = JPype
    find-links =
        http://aarnet.dl.sourceforge.net/project/jpype/JPype/0.5.4/JPype-0.5.4.1.zip
    environment = java-env
