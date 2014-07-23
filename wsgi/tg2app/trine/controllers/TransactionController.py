from datetime import datetime
from formencode import validators
from sqlalchemy import or_, func, and_
from tg import request, predicates, expose, redirect, validate
from tg.flash import flash
from trine.lib import FilterParser
from trine.lib.utils import exposeForThisName, RelativeDatetime
from trine.lib.base import BaseController
from trine.model import DBSession as db, Tag, Transaction, TagGroup

__author__ = 'Marek'


class TransactionController(BaseController):
    allow_only = predicates.not_anonymous()

    @exposeForThisName
    def index(self):
        user = request.identity["user"]
        return {
            'page': 'index',
            'tags': user.tags,
            'tagGroups': user.tagGroups,
            'transactions': db.query(Transaction).with_parent(user)
                .filter(Transaction.date <= datetime.utcnow())
                .order_by(Transaction.date.desc(), Transaction.amount.desc())
                .limit(36),
            'balances': Transaction.get_balances_per_tag(user, Tag.TYPE_INCOME).all(),
            'totalBalance': Transaction.get_balance(user).scalar(),
            'totalIncomes': Transaction.get_total_incomes(user).scalar(),
            'totalExpenses': Transaction.get_total_expenses(user).scalar(),
        }

    @exposeForThisName
    def transactionByTag(self):
        user = request.identity["user"]
        return {'tags': db.query(Tag).with_parent(user).order_by(Tag.type.desc(), Tag.name)}

    @expose()
    @validate(validators={"amount": validators.Number, "foreign-currency-amount": validators.Number})
    def add_transaction(self, **values):
        values["validation_status"] = request.validation
        flash(values["validation_status"])

        user = request.identity["user"]

        transaction = Transaction(user=user)
        transaction.amount = float(values["amount"])
        transaction.date = RelativeDatetime.str2date(values["datetime"])

        if values["foreign-currency-amount"]:
            transaction.foreignCurrencyAmount = float(values["foreign-currency-amount"])
            transaction.foreignCurrency = "EUR"

        income_tags_names = Tag.get_names_from_str(values["income-tags"])
        if income_tags_names:
            transaction.incomeTagGroup = Tag.new_from_name_list(income_tags_names)

        expense_tags_names = Tag.get_names_from_str(values["expense-tags"])
        if expense_tags_names:
            transaction.expenseTagGroup = Tag.new_from_name_list(income_tags_names)

        db.add(transaction)
        db.flush()

        redirect("/transaction")

    @exposeForThisName
    def filter(self, query=''):

        parsedQuery = FilterParser.parse(query)

        user = request.identity["user"]

        dbQuery = self.db.query(Transaction).with_parent(user)

        # contains
        if query:
            for condition in parsedQuery:
                for condName, values in condition.items():
                    if condName == 'tags':
                        ops_ = {'contains': and_, 'any': or_}
                        op_ = ops_[values['operator']]

                        tags = Tag.by_names(values['names'], user)

                        tagConditions = {Tag.TYPE_INCOME: [], Tag.TYPE_EXPENSE: []}
                        tagFields = {Tag.TYPE_INCOME: Transaction.incomeTagGroup,
                                     Tag.TYPE_EXPENSE: Transaction.expenseTagGroup}

                        for tag in tags:
                            if values['not']:
                                tagConditions[tag.type].append(~TagGroup.tags.any(Tag.id == tag.id))
                            else:
                                tagConditions[tag.type].append(TagGroup.tags.any(Tag.id == tag.id))

                        for type, condition in tagConditions.items():
                            if condition:
                                op = op_(*condition)
                                if values['null']:
                                    op = op_(or_(op, Transaction.incomeTagGroup == None,
                                                 Transaction.expenseTagGroup == None))
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
        # dbQuery = dbQuery.filter(Transaction.incomeTagGroup.has(TagGroup.tags.any(Tag.name.in_(tags))))

        queryGroups = {
            'mindate': db.query(func.min(dbQuery.subquery().columns.date)).scalar(),
            'maxdate': db.query(func.max(dbQuery.subquery().columns.date)).scalar(),
        }
        queryGroups['diffdate'] = queryGroups['maxdate'] - queryGroups['mindate'] if queryGroups[
            'maxdate'] else datetime.utcnow() - datetime.utcnow()
        days = queryGroups['diffdate'].days
        queryGroups['days'] = days + 1
        queryGroups['weeks'] = days // 7 + 1
        queryGroups['months'] = days // 30 + 1
        queryGroups['explanations'] = parsedQuery

        return {
            'query': query,
            'transactions': dbQuery.order_by(Transaction.date.desc(), Transaction.amount.desc()),
            'balance': Transaction.get_balance(user).scalar(),
            'incomes': Transaction.get_total_incomes(user).scalar(),
            'expenses': Transaction.get_total_expenses(user).scalar(),
            'queryGroups': queryGroups
        }

