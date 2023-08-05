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
UNDEFINED = object()

# ** Metadata
__all__ = ("hybridmethod", "classmethod", "instance")
__version__ = "0.1.0"


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


class classmethod:  # noqa: A001
    # Regarding the usage of flake8-builtins
    # https://www.gnu.org/licenses/gpl-faq.html#GPLOutput
    # https://www.gnu.org/licenses/gpl-faq.html#WhatCaseIsOutputGPL=
    """A drop in replacement for the `@classmethod` decorator.

    This decorator replaces the built-in `@classmethod` decorator, extending it to allow
    a class method to have different behavior when called as an instance method.

    ### Usage
    ```py
    class Test:
        @classmethod
        def method(cls):
            pass

        @method.instance
        def _(self):
            pass
    ```
    """

    def __init__(self, _classmethod, _instancemethod=UNDEFINED, _doc=None):
        """Initialize the wrapper.

        ### Parameters
            - _classmethod
                - The class method
            - _instancemethod = None
                - The instance method implementation
            - _doc = None
                - Method documentation
        """
        # Magic Variables
        self.__isabstractmethod__ = bool(
            getattr(_classmethod, "__isabstractmethod", False),
        )
        self.__doc__ = _doc

        # Method Implementations
        self._classmethod = _classmethod
        self._instancemethod = _instancemethod

    def __get__(self, instance, cls):
        """Handle the method to call."""
        if instance is None:
            return self._classmethod.__get__(cls, None)
        else:
            if self._instancemethod is UNDEFINED:
                # Throw an error if instance definition not implemented but called.
                raise NotImplementedError(
                    "Instance method has not been defined yet.",
                )
            return self._instancemethod.__get__(instance, cls)

    def instance(self, _instancemethod):
        """Set a given method as the instance method definition."""
        self._instancemethod = _instancemethod
        return type(self)(self._classmethod, _instancemethod, self.__doc__)


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
