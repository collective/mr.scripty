
Transforming Varnish backends for HAProxy
-----------------------------------------

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
    acl myhost url_sub VirtualHostRoot/255.255.255.1
    acl myhost2 url_sub VirtualHostRoot/125.125.125.1
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
