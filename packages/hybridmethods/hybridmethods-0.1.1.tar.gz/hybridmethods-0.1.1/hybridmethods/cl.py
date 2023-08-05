# Encoding: UTF-8
"""."""
UNDEFINED = object()


class assmethod:  # noqa: A001
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
