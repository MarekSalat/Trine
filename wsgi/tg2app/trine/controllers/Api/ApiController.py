from json import JSONEncoder
import json
from os import environ
from sprox.fillerbase import TableFiller
from sqlalchemy.orm import subqueryload
from tg import RestController, abort, request, expose, response, predicates
from tgext.crud import CrudRestController
from trine.lib.base import BaseController
from trine.model import Fund, DBSession, Tag, TagGroup

__author__ = 'Marek'


class ApiController(BaseController):
    apiKeys = ["quick-key", "7923fd82-400a-4c0b-b9ef-df40998a5f00"]
    supportedVersions = ['v1']

    def __init__(self):
        super().__init__()
        self.apiControllers = dict(
            fund=FundApiRestController(DBSession),
            tag=TagRestController(session=DBSession)
        )

    @expose()
    def _lookup(self, version, apikey, resource, *remainder):
        if not version in self.supportedVersions:
            return ApiErrorController(), ("invalidApiVersion",)
        if not apikey in self.apiKeys:
            return ApiErrorController(), ("invalidApiKey",)
        if not request.identity:
            return ApiErrorController(), ('needAuth',)
        else:
            print(request.identity)

        return self.apiControllers[resource], remainder

class ApiErrorController(BaseController):

    @expose('json')
    def needAuth(self):
        response.status = 401
        return dict()

    @expose('json')
    def invalidApiKey(self):
        status = 403
        response.status = status
        return dict(error=status, message="Invalid api key")

    @expose('json')
    def invalidApiVersion(self):
        status = 406
        response.status = status
        return dict(error=status, message="Api version is not supported")


class ApiRestController(RestController):
    allow_only = predicates.not_anonymous()

    def __init__(self, db):
        super().__init__()
        self.db = db

    def _before(self, *args, **kw):
        if request.response_type != 'application/json':
            abort(406, 'Only JSON requests are supported')


class ApiCrudRestController(CrudRestController, ApiRestController):
    def __init__(self, session, menu_items=None):
        CrudRestController.__init__(self, session, menu_items)
        ApiRestController.__init__(self, session)

    def _before(self, *args, **kw):
        ApiRestController._before(self, *args, **kw)

# ------------------

class FundApiRestController(ApiCrudRestController):
    model = Fund
    substring_filters = [Fund.description]

    class table_filler_type(TableFiller):
        __model__ = Fund
        __omit_fields__ = [Fund._user, Fund._user_id, Fund.incomeTagGroup_id, Fund.expenseTagGroup_id]
        __hide_fields__ = __omit_fields__

        # def _do_get_provider_count_and_objs(self, **kw):
        #     since = kw.pop('since', 0)
        #     limit = kw.pop('limit', None)
        #     offset = kw.pop('offset', None)
        #     order_by = kw.pop('order_by', None)
        #     desc = kw.pop('desc', False)
        #     substring_filters = kw.pop('substring_filters', [])
        #
        #     # count, objs = self.__provider__.query(self.__entity__, limit, offset, self.__limit_fields__,
        #     #                                       order_by, desc, substring_filters=substring_filters,
        #     #                                       filters=kw)
        #
        #     objs = DBSession.query(Fund).options(
        #         subqueryload(Fund.incomeTagGroup).subqueryload(TagGroup.tags),
        #         subqueryload(Fund.expenseTagGroup).subqueryload(TagGroup.tags)
        #     ).filter(Fund._user == request.identity["user"]).all()
        #
        #     count = len(objs)
        #
        #     self.__count__ = count
        #
        #     return count, objs

class TagRestController(ApiCrudRestController):
    model = Tag
    substring_filters = ['name']
    pagination = {'items_per_page': 100}

    class table_filler_type(TableFiller):
        __model__ = Tag

