from tg import request, predicates
from trine.lib.utils import exposeForThisName
from trine.lib.base import BaseController
from trine.model import DBSession, Tag, Fund, TagGroup

__author__ = 'Marek'


class FundController(BaseController):
    allow_only = predicates.not_anonymous()

    def __init__(self, db:DBSession):
        super().__init__()
        self.db = db

    @exposeForThisName
    def index(self):
        tempargs = {
            'page': 'index',
            'tags': self.db.query(Tag).order_by(Tag.type.desc(), Tag.name).filter(Tag._user == request.identity["user"]),
            'funds': self.db.query(Fund).order_by(Fund.date.desc()).filter(Fund._user == request.identity["user"]),
            'tagGroups': self.db.query(TagGroup).join(TagGroup.tags).order_by(Tag.type.desc()).filter(TagGroup._user == request.identity["user"])
        }
        return tempargs

    @exposeForThisName
    def fundByTag(self):
        return {'tags': self.db.query(Tag).filter(Tag._user == request.identity["user"]).order_by(Tag.type.desc(), Tag.name)}