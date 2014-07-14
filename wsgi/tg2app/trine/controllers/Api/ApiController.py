from sprox.formbase import EditableForm, AddRecordForm
from sprox.providerselector import ProviderTypeSelector
from sqlalchemy.orm import subqueryload
from tg import RestController, request, expose, response, predicates, abort, validate
from tgext.crud.decorators import register_validators, registered_validate

from trine.lib.base import BaseController
from trine.lib.provider import TrineProvider
from trine.model import Transaction, Tag, TagGroup, User, DBSession as db


__author__ = 'Marek'


class ApiController(BaseController):
    """
        /api/v1/{api-key}/{model}[/{guid}]

        headers: {'Accept': 'application/json', 'Content-Type': 'application/json'}
    """

    apiKeys = ["quick-key", "7923fd82-400a-4c0b-b9ef-df40998a5f00"]
    supportedVersions = ['v1']

    def __init__(self):
        super().__init__()
        self.apiControllers = dict(
            transaction=TransactionApiRestController(),
            tag=TagRestController(),
            taggroup=TagGroupApiRestController(),
            user=UserRestController()
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

    def __init__(self):
        super().__init__()
        self.provider = ProviderTypeSelector().get_selector(self.model).get_provider(self.model, hint=db)

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

    def _prepare_query(self):
        return db.query(self.model).with_parent(request.identity["user"])

    def _filter_query(self, query, limit=0, offset=0, order_by="", pagesize=10, page=0, filter="", **kw):
        if limit:
            query = query.limit(limit)

        if limit and offset:
            query = query.offset(offset)

        if order_by:
            for col in [col.split("|") for col in order_by.split(";")]:
                field_name = col[0]
                if not hasattr(self.model, field_name):
                    continue
                field = getattr(self.model, field_name)
                if len(col) == 2:
                    strategy = col[1].lower()
                    if strategy == "asc":
                        field = field.asc()
                    if strategy == "desc":
                        field = field.desc()
                query = query.order_by(field)

        # TODO: pagesize=10&page=1
        # TODO: filter={ field: { $gt: value1, $lt: value2 } }

        return query

    @expose('json')
    def get_all(self, **kw):
        """
            model?limit=5
            model?limit=5&offset=2
            model?order_by=amount
            model?order_by=date|desc;amount|desc
            model?pagesize=10&page=1

        :param kw:
        :return:
        """
        query = self._prepare_query(**kw)
        filtered_query = self._filter_query(query, **kw)

        entities = filtered_query.all()

        if entities is None:
            abort(404, 'Not found')

        return {'value_list': self._dictify(entities), 'total_entries': query.count(), 'entries': filtered_query.count()}

    @expose('json')
    def get_one(self, id, **kw):
        entity = self._prepare_query(**kw).filter(self.model.id == id).first()

        if entity is None:
            abort(404, 'Not found')

        return {'value': self._dictify(entity)}

    @expose('json')
    # @registered_validate()
    def post(self, **kw):
        # if request.response_type != 'application/json':
        # abort(406, 'Only JSON requests are supported')

        if request.validation['errors']:
            return "There was an error"

        entity = self.model(**request.json_body)
        entity._user_id = request.identity["user"].id
        db.add(entity)
        db.flush()

        return self.get_one(entity.id, **kw)

    @expose('json')
    # @registered_validate()
    def put(self, id, **kw):
        # if request.response_type != 'application/json':
        # abort(406, 'Only JSON requests are supported')

        entity = self._prepare_query(**kw).filter(self.model.id == id).first()

        if not entity:
            response.status_code = 404
            return {'error': 'no exists'}

        for key, value in request.json_body.items():
            setattr(entity, key, value)

        db.flush()

        return self.get_one(id, **kw)

    @expose('json')
    def post_delete(self, id, **kw):
        self._prepare_query(**kw).filter(self.model.id == id).delete()


class TransactionApiRestController(ApiCrudRestController):
    model = Transaction

    def __init__(self):
        self.omit_fields += ['incomeTagGroup_id', 'expenseTagGroup_id', "groups"]
        self.provider = TrineProvider()

    def _prepare_query(self, **kw):
        return db.query(Transaction).options(
            subqueryload(Transaction.incomeTagGroup).subqueryload(TagGroup.tags),
            subqueryload(Transaction.expenseTagGroup).subqueryload(TagGroup.tags)
        ).with_parent(request.identity["user"])

    @expose(inherit=True)
    def post(self, as_transfer=False, **kw):
        # TODO: validation
        transaction = request.json

        for field, tag_type in [('incomeTagGroup', Tag.TYPE_INCOME), ('expenseTagGroup', Tag.TYPE_EXPENSE)]:
            if field not in transaction or not isinstance(transaction[field], list):
                continue
            transaction[field] = TagGroup.new_with_these_tags(
                Tag.new_from_name_list(transaction[field], request.identity["user"], tag_type))

        entity = self.model(**transaction)
        entity._user_id = request.identity["user"].id

        if as_transfer:
            entity.incomeTagGroup = entity.expenseTagGroup = None
            source, target = Transaction.new_transfer(entity,
                                                      transaction['incomeTagGroup'],
                                                      transaction['expenseTagGroup'])
            return {'value_list': self._dictify([source, target]), 'entries': 2}

        db.add(entity)
        db.flush()

        return self.get_one(entity.id, **kw)

    @expose(inherit=True)
    def put(self, id, **kw):
        entity = self._prepare_query(**kw).filter(self.model.id == id).first()

        if not entity:
            response.status_code = 404
            return {'error': 'no exists'}

        transaction_changes = request.json_body

        for field, tag_type in [('incomeTagGroup', Tag.TYPE_INCOME), ('expenseTagGroup', Tag.TYPE_EXPENSE)]:
            if field not in transaction_changes or not isinstance(transaction_changes[field], list):
                continue
            transaction_changes[field] = TagGroup.new_with_these_tags(
                Tag.new_from_name_list(transaction_changes[field], request.identity["user"], tag_type))

        for key, value in transaction_changes.items():
            if not hasattr(entity, key):
                continue
            setattr(entity, key, value)

        db.flush()

        return self.get_one(id, **kw)


class TagGroupApiRestController(ApiCrudRestController):
    model = TagGroup

    def __init__(self):
        super().__init__()
        self.omit_fields += ['expenses', 'incomes']
        self.provider = TrineProvider()


class TagRestController(ApiCrudRestController):
    model = Tag


class UserRestController(ApiCrudRestController):
    model = User

    def _prepare_query(self):
        return db.query(self.model).filter(self.model.id == request.identity["user"].id)

    def __init__(self):
        super().__init__()
        self.omit_fields = ['expenses', 'incomes', 'groups', 'transactions', "_password", "password", "tagGroups", "tags"]

    @expose(inherit=True)
    def get_all(self, **kw):
        return self.get_one(request.identity["user"].id, **kw)

    def post(self, **kw):
        pass

    def post_delete(self, id, **kw):
        pass
