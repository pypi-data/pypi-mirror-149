from typing import *

class Case:
    def __init__(self, tpe: type, fun: function):
        self.type = tpe
        self.callback = fun

    def check(self, obj):
        if isinstance(obj, self.type):
            self.callback()

def switch(obj: object, cases: List[Case]):
    for case in cases:
        case.check(obj)