"""A singleton metaclass for singletons.

Copyright 2019 Christian Holm Christensen
"""

class Singleton(type):
    """A singleton metaclass

    This class redefines what a type is if another class inherits from
    this as a metaclass.  This class then manipulates how we create
    new objects of the derived type so that we only ever have one
    instance of the derived class

    To make a class a singleton do 

    >>> class A(metaclass=Singleton):
    ...     pass 


    Test case
    ---------
    - ``test_singleton.py``

    """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = \
                super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

#
# EOF
#
