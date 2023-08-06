from typing import *

class ConstantError(RuntimeError):
    def __init__(self, nam):
        self.nam = nam

    def __str__(self):
        return f'Cannot change value of \'{self.nam}\': \'{self.nam}\' is immutable'

class Constant:
    def __setattr__(self, __name: str, __value: Any):
        if __name in self.__dict__:
            raise ConstantError(__name)
        else:
            self.__dict__[__name] = __value