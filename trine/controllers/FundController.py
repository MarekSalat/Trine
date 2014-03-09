from trine.lib.utils import exposeForThisName
from trine.lib.base import BaseController
from trine.model import DBSession, Tag, Fund, TagGroup

__author__ = 'Marek'


class FundController(BaseController):
    def __init__(self, db:DBSession):
        super().__init__()
        self.db = db

    @exposeForThisName
    def index(self):
        tempargs = {
            'page': 'index',
            'tags': self.db.query(Tag).order_by(Tag.type.desc(), Tag.name),
            'funds': self.db.query(Fund).order_by(Fund.date.desc()),
            'tagGroups': self.db.query(TagGroup).join(TagGroup.tags).order_by(Tag.type.desc())
        }
        return tempargs

    @exposeForThisName
    def fundByTag(self):
        return {'tags': self.db.query(Tag).order_by(Tag.type.desc(), Tag.name)}