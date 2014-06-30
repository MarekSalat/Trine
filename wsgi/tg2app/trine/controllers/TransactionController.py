from datetime import datetime
from formencode import validators
from sqlalchemy import or_, func, and_
from tg import request, predicates, expose, redirect, validate
from tg.flash import flash
from trine.lib import FilterParser
from trine.lib.utils import exposeForThisName, RelativeDatetime
from trine.lib.base import BaseController
from trine.model import DBSession, Tag, Transaction, TagGroup
from trine.model.Mapper import TagGroupMapper, TagMapper

__author__ = 'Marek'


class TransactionController(BaseController):
    allow_only = predicates.not_anonymous()

    def __init__(self, db:DBSession):
        super().__init__()
        self.db = db

    @exposeForThisName
    def index(self):
        user = request.identity["user"]

        transactionQuery = self.db.query(Transaction).with_parent(user)

        balanceQuery = self.db.query(func.sum(Transaction.amount)).with_parent(user).\
                                filter(Transaction.date <= datetime.utcnow())

        balances = dict()
        for tag in self.db.query(Tag).with_parent(user).filter(Tag.type == Tag.TYPE_INCOME):
            balances[tag.name] = balanceQuery.filter(
                Transaction.incomeTagGroup.has( TagGroup.tags.any(Tag.name == tag.name) )
            ).scalar()

        tempargs = {
            'page': 'index',
            'tags': user.tags,
            'tagGroups': user.tagGroups,
            'transactions': transactionQuery.order_by(Transaction.date.desc(), Transaction.amount.desc()).limit(36),
            'balances': balances,
            'totalBalance':  self.getBalance(transactionQuery),
            'totalIncomes' : self.getBalance(transactionQuery.filter(Transaction.amount > 0)),
            'totalExpenses': self.getBalance(transactionQuery.filter(Transaction.amount < 0)),
        }
        return tempargs

    @exposeForThisName
    def transactionByTag(self):
        user = request.identity["user"]
        return {'tags': self.db.query(Tag).with_parent(user).order_by(Tag.type.desc(), Tag.name)}

    @expose()
    @validate(validators={"amount":validators.Number, "foreign-currency-amount":validators.Number})
    def add_transaction(self, **values):
        values["validation_status"] = request.validation
        flash(values["validation_status"])

        user = request.identity["user"]

        transaction = Transaction(_user=user)
        transaction.amount = float(values["amount"])
        transaction.date = RelativeDatetime.str2date(values["datetime"])

        if values["foreign-currency-amount"]:
            transaction.foreignCurrencyAmount = float(values["foreign-currency-amount"])
            transaction.foreignCurrency = "EUR"

        tgMapper = TagGroupMapper(self.db)
        incomeTags = TagMapper.getTagNamesListFromString(values["income-tags"])
        if incomeTags:
            transaction.incomeTagGroup = tgMapper.getTagGroupOrCreateFromTagNames(incomeTags, user, Tag.TYPE_INCOME)

        expenseTags =  TagMapper.getTagNamesListFromString(values["expense-tags"])
        if expenseTags:
            transaction.expenseTagGroup = tgMapper.getTagGroupOrCreateFromTagNames(expenseTags, user, Tag.TYPE_EXPENSE)

        self.db.add(transaction)
        self.db.flush()

        redirect("/transaction")

    @exposeForThisName
    def filter(self, query=''):

        parsedQuery = FilterParser.parse(query)

        tgMapper = TagGroupMapper(self.db)
        user = request.identity["user"]

        dbQuery = self.db.query(Transaction).with_parent(user)

        # contains
        if query:
            for condition in parsedQuery:
                for condName, values in condition.items():
                    if condName == 'tags':
                        ops_ = {'contains': and_, 'any': or_}
                        op_ = ops_[values['operator']]

                        tags = tgMapper.findTagByNames(values['names'], user)

                        tagConditions  = {Tag.TYPE_INCOME:[], Tag.TYPE_EXPENSE: []}
                        tagFields = {Tag.TYPE_INCOME:Transaction.incomeTagGroup, Tag.TYPE_EXPENSE: Transaction.expenseTagGroup}

                        for tag in tags:
                            if values['not']:
                                tagConditions[tag.type].append( ~TagGroup.tags.any(Tag.id == tag.id ) )
                            else:
                                tagConditions[tag.type].append( TagGroup.tags.any(Tag.id == tag.id) )

                        for type, condition in tagConditions.items():
                            if condition:
                                op = op_(*condition)
                                if values['null']:
                                    op = op_(or_(op, Transaction.incomeTagGroup == None, Transaction.expenseTagGroup == None))
                                dbQuery = dbQuery.filter(tagFields[type].has(op))

                    if condName == 'property':
                        # TODO: regexp
                        operators = {'<': '__lt__', '<=': '__le__',
                                     '>': '__gt__', '>=': '__ge__',
                                     '=': '__eq__', '!=': '__ne__'}
                        property = getattr(Transaction, (values['name']))

                        dbQuery = dbQuery.filter(getattr(property, operators[values['operator']])(values['value']))


                    if condName == 'has':
                        property = getattr(Transaction, (values['property']))
                        if values['not']:
                            dbQuery = dbQuery.filter(property == None)
                        else:
                            dbQuery = dbQuery.filter(property != None)

                    # TODO: date support
                    if condName == 'date':
                        pass

        # in
        # if query:
        #     dbQuery = dbQuery.filter(Transaction.incomeTagGroup.has(TagGroup.tags.any(Tag.name.in_(tags))))

        queryGroups = {
            'mindate': self.db.query(func.min(dbQuery.subquery().columns.date)).scalar(),
            'maxdate': self.db.query(func.max(dbQuery.subquery().columns.date)).scalar(),
        }
        queryGroups['diffdate'] = queryGroups['maxdate'] - queryGroups['mindate'] if queryGroups['maxdate'] else datetime.utcnow()-datetime.utcnow()
        days = queryGroups['diffdate'].days
        queryGroups['days'] = days + 1
        queryGroups['weeks'] = days//7 + 1
        queryGroups['months'] = days//30 + 1
        queryGroups['explanations'] = parsedQuery

        return {
            'query': query,
            'transactions': dbQuery.order_by(Transaction.date.desc(), Transaction.amount.desc()),
            'balance': self.getBalance(dbQuery),
            'incomes': self.getBalance(dbQuery.filter(Transaction.amount > 0)),
            'expenses':self.getBalance(dbQuery.filter(Transaction.amount < 0)),
            'queryGroups': queryGroups
        }

    def getBalance(self, query):
            return self.getBalanceQuery(query).scalar()

    def getBalanceQuery(self, query):
        return self.db.query(func.sum(
            query.filter(Transaction.transferKey == None ).subquery().columns.amount
        ))

