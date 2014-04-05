import re
from tg import expose

__author__ = 'Marek'


def exposeForThisName(func):
    module = func.__module__.replace('controllers', 'templates')
    module = re.sub(r'\.[\w]+$', '', module)
    controller = re.findall(r'<function ([\w.]+).+>', repr(func))[0]
    controller = re.sub('Controller\.', '.', controller)
    path = "%s.%s" % (module, controller)

    return expose(path)(func)