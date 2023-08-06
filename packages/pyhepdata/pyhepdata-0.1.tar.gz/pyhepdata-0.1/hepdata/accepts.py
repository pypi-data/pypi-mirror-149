"""Module that defines a decorator that type-checks arguments 
and casts if possible

Copyright 2019 Christian Holm Christensen
"""
from functools import wraps


# --------------------------------------------------------------------
def accepts(**decls):
    """Decorator to ensure arguments for methods.  

    This decorate tries to coerce the arguments to proper types and
    only fails if it cannot. Optional values are handled correctly as
    are keyword arguments.

    Usage
    -----
    
         class Foo:
              @accepts(arg1=type,arg2=types,...)
              def func(self,arg1,arg2,...):

    Test case
    ---------
        test_accepts

    """
    def decorator(func):
        # Get list of function argument names so we can
        # find the appropriate name of an non-keyword argument.
        # Note, we ignore the first argument which is always
        # self or cls for methods
        code  = func.__code__
        names = code.co_varnames[1:code.co_argcount]

        # Check that arguments to function and those given to the
        # declarator match exactly
        diff = set(names)-set(decls.keys())
        assert len(diff) == 0, \
            "Arguments to function {}: {}\n"\
            "and decorator accept: {}\n"\
            "does not match exactly: {}\n"\
            .format(func, list(names),list(decls.keys()),diff)
        
        @wraps(func)
        def wrap(self,*args,**kwargs):
            # We will build the final argument list here 
            newargs = {}
            
            # Loop over the declared names for the decorator.
            # This list _must_ match the method arguments 
            for name, types in decls.items():
                # We assume no value for each argument 
                val = None

                try:
                    # See if we got an argument 
                    val = args[names.index(name)]
                except (ValueError, IndexError):
                    # If not, see if it was given as a keyword
                    # argument
                    val = kwargs.get(name)
                    # If it was, remove it from the list of keyword
                    # arguments to avoid duplicate arguments.
                    if name in kwargs:
                        del kwargs[name]

                # If we didn't find a value, go on to next argument 
                if val is None:
                    continue

                # If the list of acceptable types is None, then we
                # accept all types
                if types is None:
                    newargs[name] = val
                    continue

                # If types is not a list or tuple, make it into a list
                if type(types) not in [list,tuple]:
                    types = [types]

                # Possibly converted value will go here 
                newval = None
                
                # Now check if the value is already of one of the
                # appropriate types
                for t in types:
                    if isinstance(val,t):
                        newval = val
                        break

                # If the argument wasn't of one of the appropriate
                # types, see if we can convert it to a valid type.
                if newval is None:
                    for t in types:
                        try:
                            # Try to convert the value 
                            newval = t(val)
                            break
                        except:
                            pass

                # If we didn't get a new value, then we have a problem
                # and we raise an exception.
                if newval is None:
                    valid = ",".join([t.__name__ for t in types])
                    raise TypeError('Argument {} is {}, but must be {}'
                                    .format(name,type(val).__name__,valid))

                # Store the (possibly converted) value in the
                # dictionary of arguments.
                newargs[name] = newval

            # Call the method 
            return func(self,**newargs, **kwargs)
        return wrap
    return decorator

# --------------------------------------------------------------------
#
# EOF
#
