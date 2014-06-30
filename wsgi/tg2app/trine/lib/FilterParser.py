import re
from trine.model.Mapper import TagMapper

__author__ = 'Marek'

class Parser:
    '''
        condition separator: and
        [not] xxx, zzz                  -- transaction must contains all mentioned tags (and some more)
        [not] any xxx, zzz              -- transaction must contains any of mentioned tags
        has [not] property              -- check if property is filled
        property [<|<=|>|>=|=|!=|regexp] value    -- @Note: see magic methods __eq__ ...
        property since reldate [until reldate] -- from specific date to now or specified date after "to"

        examples:
            grocery, beers and not ,account and amount < -20 and date since -5 days until next week and has not description
            return -    [   {  'tags': {'operator': 'contains'
                                        'names': ['grocery', 'beers'],
                                        'not': True,
                                        'null': False}},
                        {   'tags': {   'operator': 'any',
                                        'names': ['account'],
                                        'not': False,
                                        'null': True}},
                        {   'property': {   'name': 'amount',
                                            'operator': '<',
                                            'value': '-20'}},
                        {   'date': {   'property': 'date',
                                        'since': '-5 days until next week',
                                        'until': 'now'}},
    '''

    pass

def parse(value:str):
    if not value:
        return {}

    value = re.sub(r'\s+', ' ', value);
    conditions = value.split(' and ')

    result = []
    for condition in conditions:
        res = re.match(r'^has (not )?([\w]+)$', condition)
        if res:
            result.append({'has':{
                'not': res.group(1) is not None,
                'property': res.group(2)
            }})
            continue

        res = re.match(r'^([\w]+)\s*(<|<=|>|>=|=|!=|regexp)\s*(.+)$', condition)
        if res:
            result.append({'property':{
                'name': res.group(1),
                'operator': res.group(2),
                'value': res.group(3)
            }})
            continue

        # re.match(r'([\w]+) since (.+)(?= until (.+))', 'date since +5 days until 5 x').groups()
        res = re.match(r'^([\w]+) since (.+)(?= until (.+))$|^([\w]+) since (.+)$', condition)
        if res:
            prop, sinceRelDate, untilRelDate, prop2, sinceRelDate2 = res.groups()
            if prop2:
                prop = prop2
                sinceRelDate = sinceRelDate2
                untilRelDate = 'now'

            result.append({'date':{
                'property': prop,
                'since': sinceRelDate,
                'until': untilRelDate
            }})
            continue

        res = re.match(r'^(not )?(any )?(.+)$', condition)
        if res:
            result.append({'tags': {
                    'not': res.group(1) is not None,
                    'operator': 'any' if not res.group(2) is None else 'contains',
                    'names': TagMapper.getTagNamesListFromString(res.group(3)),
                    'null': re.match(r'^,.+', res.group(3)) is not None,
            }})
            continue

    return result
