import re
from tg import expose

__author__ = 'Marek'


def get_class_that_defined_method(method):
    method_name = method.__name__
    # if method.__self__:
    #     classes = [method.__self__.__class__]
    # else:
    #unbound method
    classes = [method.im_class]
    while classes:
        c = classes.pop()
        if method_name in c.__dict__:
            return c
        else:
            classes = list(c.__bases__) + classes
    return None


class classdec:
    def __init__(self):
        print('classdec created')

    def __call__(self, func):
        print('classdec decorating')
        return func


def something(func, *args, **kwargs):
    tmp = repr(func)
    res = re.findall(r'<function ([a0-z9_.]+) .+>', tmp)[0]
    print(tmp, res)
    path = "%s.%s.%s" % (func.__module__, func.__class__.__name__, func.__name__)
    print(path)
    return expose(path)(func)


class Sandbox:
    @something
    def do(self):
        print("I am doing")


sandbox = Sandbox()
sandbox.do()
print('\n')
sandbox.do()