from sprox.formbase import EditableForm, AddRecordForm
from sprox.providerselector import ProviderTypeSelector
from sqlalchemy.orm import subqueryload
from tg import RestController, request, expose, response, predicates, abort
from tgext.crud.decorators import register_validators, registered_validate

from trine.lib.base import BaseController
from trine.lib.provider import TrineProvider
from trine.model import Transaction, Tag, TagGroup


__author__ = 'Marek'


class ApiController(BaseController):
    apiKeys = ["quick-key", "7923fd82-400a-4c0b-b9ef-df40998a5f00"]
    supportedVersions = ['v1']

    def __init__(self, session):
        super().__init__()
        self.apiControllers = dict(
            transaction=TransactionApiRestController(session),
            tag=TagRestController(session),
            taggroup=TagGroupApiRestController(session)
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


class ApiCrudRestController(BaseController, RestController):
    allow_only = predicates.not_anonymous()
    omit_fields = ['user', '_user_id']
    model = None

    def __init__(self, session):
        super().__init__()
        self.session = session
        self.provider = ProviderTypeSelector().get_selector(self.model).get_provider(self.model, hint=session)

        # if not hasattr(self, 'new_form'):
        # class EditForm(EditableForm):
        #         __entity__ = self.model
        #         __omit_fields__ = self.omit_fields
        #
        #     self.edit_form = EditForm(session)
        #
        # register_validators(self, 'post', self.new_form)
        #
        # if not hasattr(self, 'edit_form'):
        #     class NewForm(AddRecordForm):
        #         __entity__ = self.model
        #         __omit_fields__ = self.omit_fields
        #
        #     self.new_form = NewForm(session)
        #
        # register_validators(self, 'put', self.edit_form)

    def _dictify(self, value):
        if self.omit_fields is False:
            return value

        def _dictify(entity):
            if hasattr(entity, '__json__'):
                return entity.__json__()
            else:
                return self.provider.dictify(entity, omit_fields=self.omit_fields)

        if isinstance(value, list):
            # return a generator, we don't want to consume the whole query
            return (_dictify(entity) for entity in value)
        else:
            return _dictify(value)

    def _before(self, *args, **kw):
        pass
        # if request.response_type != 'application/json':
        # abort(406, 'Only JSON requests are supported')

    def _prepare_query(self, model=None, limit=False, **kw):
        if not model:
            model = self.model
        query = self.session.query(model).with_parent(request.identity["user"])
        if limit:
            query = query.limit(limit)
        return query

    @expose('json')
    def get_all(self, **kw):
        entities = self._prepare_query(**kw).all()

        if entities is None:
            abort(404, 'Not found')

        return {'value_list': self._dictify(entities)}

    @expose('json')
    def get_one(self, id, **kw):
        entity = self._prepare_query(**kw).filter(self.model.id == id).first()

        if entity is None:
            abort(404, 'Not found')

        return {'value': self._dictify(entity)}

    @expose('json')
    @registered_validate()
    def post(self, **kw):
        # if request.response_type != 'application/json':
        # abort(406, 'Only JSON requests are supported')

        if request.validation['errors']:
            return "There was an error"

        entity = self.model(**request.json_body)
        entity._user_id = request.identity["user"].id
        self.session.add(entity)
        self.session.flush()

        return self.get_one(entity.id, **kw)

    @expose('json')
    @registered_validate()
    def put(self, id, **kw):
        # if request.response_type != 'application/json':
        # abort(406, 'Only JSON requests are supported')

        entity = self._prepare_query(**kw).filter(self.model.id == id).first()

        if not entity:
            response.status_code = 404
            return {'error': 'no exists'}

        for key, value in request.json_body.items():
            setattr(entity, key, value)

        self.session.flush()

        return self.get_one(id, **kw)

    @expose('json')
    def post_delete(self, id, **kw):
        self._prepare_query(**kw).filter(self.model.id == id).delete()


class TransactionApiRestController(ApiCrudRestController):
    model = Transaction

    def __init__(self, session):
        super().__init__(session)
        self.omit_fields += ['incomeTagGroup_id', 'expenseTagGroup_id', "groups", "transactions"]
        self.provider = TrineProvider()

    def _prepare_query(self, model=None, limit=False, **kw):
        if not model:
            model = self.model

        query = self.session.query(model).options(
            subqueryload(Transaction.incomeTagGroup).subqueryload(TagGroup.tags),
            subqueryload(Transaction.expenseTagGroup).subqueryload(TagGroup.tags)
        ).with_parent(request.identity["user"])

        if limit:
            query = query.limit(limit)

        return query


class TagGroupApiRestController(ApiCrudRestController):
    model = TagGroup

    def __init__(self, session):
        super().__init__(session)
        self.omit_fields += ['expenses', 'incomes']


class TagRestController(ApiCrudRestController):
    model = Tag
