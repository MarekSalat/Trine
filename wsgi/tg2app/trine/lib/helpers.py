# -*- coding: utf-8 -*-

"""WebHelpers used in trine."""

#from webhelpers import date, feedgenerator, html, number, misc, text
import re
from datetime import datetime

from markupsafe import Markup


def current_year():
    now = datetime.now()
    return now.strftime('%Y')


def icon(icon_name, white=False):
    if white:
        return Markup('<i class="icon-%s icon-white"></i>' % icon_name)
    else:
        return Markup('<i class="icon-%s"></i>' % icon_name)


def formatDatetime(value, format='medium'):
    return value.strftime("%d. %m. %Y.  %H:%M")


def formatNumber(value):
    value = str(value)
    return re.sub(r'.0+', '', value)
