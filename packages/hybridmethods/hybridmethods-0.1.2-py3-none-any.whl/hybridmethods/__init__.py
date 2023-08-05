# Encoding: UTF-8
"""Module to allow methods to be both a class method and an instance method.

This module provides a means to allow a method to have different behavior depending if
it were called as an instance method or as a class method.

### Usage
```py
from hybridmethods import *


class Test1:
    @hybridmethod
    def method(this):
        if instance(this):  # Run when called as instance method
            pass
        else:  # Run when called as class method
            pass


class Test2:
    @classmethod
    def method(cls):
        pass

    @classmethod.instance
    def _(self):
        pass
```
"""
# * Constants
# ** Metadata
__all__ = ("hybridmethod", "cl", "instance")
__version__ = "0.1.2"

# * Imports
from . import cl


# * Decorators
class hybridmethod(classmethod):
    """Transform a method into a hybrid method.

    A hybrid method allows a method to have different behavior at runtime depending if
    it were called as an instance method or a class method.

    ### Usage
    ```py
    class Test:
        @hybridmethod
        def method(this):
            if isinstance(this, type):
                pass
            else:
                pass
    ```

    NOTE: See also the `instance` helper function.
    """

    def __get__(self, instance, type_):
        """`__get__` magic method."""
        if instance is None:
            descriptor_get = super().__get__
        else:
            descriptor_get = self.__func__.__get__

        return descriptor_get(instance, type_)


# * Helper Functions
def instance(this) -> bool:
    """`@hybridmethod` helper function.

    ### Usage
    ```py
    class Test:
        @hybridmethod
        def method(this):
            if instance(this):
                pass
            else:
                pass
    ```
    """
    return not isinstance(this, type)
