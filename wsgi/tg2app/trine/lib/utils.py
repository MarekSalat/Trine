from datetime import datetime, timedelta
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


class RelativeDatetime:

    @staticmethod
    def date2str():
        raise NotImplemented()

    @staticmethod
    def str2date(value: str) -> datetime:
        """
        :param value: date | now | {num} (second|minute|hour|day|week|month|year | seconds|minutes|hours|days|weeks|months|years)
        :return: datetime
        """
        date = datetime.utcnow()

        if value == "now":
            return date

        try:
            date = datetime.strptime(value, "%d. %m. %Y.  %H:%M").date()
            return date
        except ValueError:
            pass

        try:
            (num, key) = value.split(" ")
            num = float(num)
            key = re.sub(r's$', '', key.lower())
            key += "s"

            param = dict()
            param[key] = num
            date = date + timedelta(**param)

        except ValueError:
            pass

        return date