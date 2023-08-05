# hybridmethods

A library for the creation of hybrid methods. Methods that can be called as either class methods or instance methods.

## Usage

```py
from hybridmethods import cl, hybridmethod, instance


class Test1:
    @hybridmethod
    def method(this):
        if instance(this):  # Run when called as instance method
            pass
        else:  # Run when called as class method
            pass
    

class Test2:
    @cl.assmethod
    def method(cls):
        pass

    @method.instance
    def _(self):
        pass
```
