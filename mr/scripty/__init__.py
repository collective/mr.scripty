# -*- coding: utf-8 -*-
"""Recipe scripty"""

import types


class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options, debug=False):
        self.buildout, self.name, self.options = buildout, name, options
        self._debug = debug

        for function, body in options.items():
            if function in ['recipe']:
                continue
            if function == function.upper():
                # it's a constant
                setattr(self, function, body)
                continue
            newbody = 'def ' + function + '(self):\n'
            indent = True
            for line in body.split('\n'):
                if line.startswith("..."):
                    line = line[4:]
                if indent:
                    newbody += "  "
                newbody += line + '\n'
                if line.startswith('"""'):
                    indent = not indent

            namespace = {}
            exec(newbody, globals(), namespace)
            my_function = namespace[function]
            f = types.MethodType(my_function, self)
            setattr(self, function, f)
            if function == 'install':
                pass

        for function, body in options.items():
            if function in ['recipe', 'install', 'update']:
                continue
            if function.startswith('_'):
                continue
            if function == function.upper():
                continue
            f = getattr(self, function)
            # LazyStrings don't work for $ substitions
            # result = _LazyString(f)
            result = f()
            if function in ['init']:
                continue
            if result is None:
                result = ''
            else:
                result = str(result)

            self.options[function] = result

    def install(self):
        """Installer"""
        # XXX Implement recipe functionality here

        # Return files that were created by the recipe. The buildout
        # will remove all returned files upon reinstall.
        return tuple()

    def update(self):
        """Updater"""
        pass


class Debug(Recipe):

    def __init__(self, buildout, name, options):
        Recipe.__init__(self, buildout, name, options, debug=True)


class LazyString(str):

    def __init__(self, func, name, debug):
        self.func = func
        self.name = name
        self.debug = debug

    def __new__(cls, func, *args):
        return str.__new__(cls, "This is not the string you are looking for")

    @property
    def value(self):
        if not hasattr(self, '__evaluated__'):
            self.__evaluated__ = str(self.func())
            if self.debug:
                print("DEBUG: %s=%s" % (self.name, self.__evaluated__))
        return self.__evaluated__

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


class _LazyString(str):
    """Class for strings created by a function call.

    The proxy implementation attempts to be as complete as possible,
    so that the lazy objects should mostly work as expected, for
    example for sorting.  Shamelessly stolen from speaklater, but
    changed to make it subclass str due to buildout instance check
    """
    # __slots__ = ('_func', '_args', '_kwargs')

    def __new__(cls, func, *args):
        return str.__new__(cls, "This is not the string you are looking for")

    def __init__(self, func, *args, **kwargs):
        self._func = func
        self._args = args
        self._kwargs = kwargs

    value = property(lambda x: x._func(*x._args, **x._kwargs))

    def __contains__(self, key):
        return key in self.value

    def __nonzero__(self):
        return bool(self.value)

    def __dir__(self):
        return dir(unicode)

    def __iter__(self):
        return iter(self.value)

    def __len__(self):
        return len(self.value)

    def __str__(self):
        return str(self.value)

    def __int__(self):
        return int(self.value)

    def __unicode__(self):
        return unicode(self.value)

    def __add__(self, other):
        return self.value + other

    def __radd__(self, other):
        return other + self.value

    def __mod__(self, other):
        return self.value % other

    def __rmod__(self, other):
        return other % self.value

    def __mul__(self, other):
        return self.value * other

    def __rmul__(self, other):
        return other * self.value

    def __lt__(self, other):
        return self.value < other

    def __le__(self, other):
        return self.value <= other

    def __eq__(self, other):
        return self.value == other

    def __ne__(self, other):
        return self.value != other

    def __gt__(self, other):
        return self.value > other

    def __ge__(self, other):
        return self.value >= other

    def __getattr__(self, name):
        if name == '__members__':
            return self.__dir__()
        return getattr(self.value, name)

    def __getstate__(self):
        return self._func, self._args

    def __setstate__(self, tup):
        self._func, self._args = tup

    def __getitem__(self, key):
        return self.value[key]

    def __copy__(self):
        return self

    def __repr__(self):
        try:
            return 'l' + repr(self.value)
        except Exception:
            return '<%s broken>' % self.__class__.__name__
