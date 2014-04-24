from datetime import datetime
import re
from formencode import validators
from sqlalchemy import or_, func
from tg import request, predicates, expose, redirect, validate
from tg.flash import flash
from trine.lib.utils import exposeForThisName, RelativeDatetime
from trine.lib.base import BaseController
from trine.model import DBSession, Tag, Fund, TagGroup, User

__author__ = 'Marek'


class FundController(BaseController):
    allow_only = predicates.not_anonymous()

    def __init__(self, db:DBSession):
        super().__init__()
        self.db = db

    @exposeForThisName
    def index(self):
        user = request.identity["user"]

        balanceQuery = self.db.query(func.sum(Fund.amount).label("balance")).with_parent(user).\
                                filter(Fund.date <= datetime.utcnow())

        balances = dict()
        for tag in self.db.query(Tag).with_parent(user).filter(Tag.type == Tag.TYPE_INCOME):
            balances[tag.name] = balanceQuery.filter(
                Fund.incomeTagGroup.has( TagGroup.tags.any(Tag.name == tag.name) )
            ).first()[0]

        tempargs = {
            'page': 'index',
            'tags': user.tags,
            'tagGroups': user.tagGroups,
            'funds': self.db.query(Fund).with_parent(user).order_by(Fund.date.desc()),
            'totalBalance': balanceQuery.first()[0],
            'balances': balances,
            'totalIncomes' : balanceQuery.filter(Fund.amount > 0).first()[0],
            'totalExpenses': balanceQuery.filter(Fund.amount < 0).first()[0],
        }
        return tempargs

    @exposeForThisName
    def fundByTag(self):
        user = request.identity["user"]
        return {'tags': self.db.query(Tag).with_parent(user).order_by(Tag.type.desc(), Tag.name)}

    @expose()
    @validate(validators={"amount":validators.Number, "foreign-currency-amount":validators.Number})
    def add_fund(self, **values):
        values["validation_status"] = request.validation
        flash(values["validation_status"])

        user = request.identity["user"]

        fund = Fund(_user=user)
        fund.amount = float(values["amount"])
        fund.date = RelativeDatetime.str2date(values["datetime"])

        if values["foreign-currency-amount"]:
            fund.foreignCurrencyAmount = float(values["foreign-currency-amount"])
            fund.foreignCurrency = "EUR"

        incomeTags = self.getTagNamesListFromString(values["income-tags"])
        if incomeTags:
            fund.incomeTagGroup = self.getTagGroupOrCreateFromTagNames(incomeTags, user, Tag.TYPE_INCOME)

        expenseTags =  self.getTagNamesListFromString(values["expense-tags"])
        if expenseTags:
            fund.expenseTagGroup = self.getTagGroupOrCreateFromTagNames(expenseTags, user, Tag.TYPE_EXPENSE)

        self.db.add(fund)
        self.db.flush()

        redirect("/fund")

    def getTagNamesListFromString(self, tagname: str) ->list:
        tags = tagname
        tags = re.sub(r'\s+', ' ', tags);
        tags = re.sub(r' ?, ?', ',', tags);
        tags = re.sub(r',+', ',', tags);   # ",,,,,," => ","
        tags = re.sub(r',$', '', tags);    # delete last comma if exist
        tags = re.sub(r'^,', '', tags);     # delete first comma if exist

        if re.match(r"^\s*$",tags):
            return []

        return tags.split(",")


    def getTagGroupOrCreateFromTagNames(self, tagNames:list, user:User, type) -> TagGroup:
        if not tagNames:
            return None

        groups = self.getGroupsFromTagNames(tagNames, user)
        if not groups:
            groups = [self.createNewGroupFromTagNames(tagNames, user, type)]

        # @TODO: display warning, because there should be only one group
        return groups[0]


    def getGroupsFromTagNames(self, tagNames:list, user:User) -> list:
        if not tagNames:
            return []

        # @TODO: there should be different solution how to get group directly from sql
        groups = DBSession.query(TagGroup).with_parent(user).\
            filter(TagGroup.tags.any(Tag.name.in_(tagNames))).\
            filter(~TagGroup.tags.any(~Tag.name.in_(tagNames))).\
            group_by(TagGroup.id)
            # having(func.count(TagGroup.tags) == len(tags))

        groups = [group for group in groups if len(group.tags) == len(tagNames) ]
        return groups

    def createNewGroupFromTagNames(self, tagNames:list, user:User, type) -> TagGroup:
        tags = self.db.query(Tag).with_parent(user).filter(or_(*[Tag.name == name for name in tagNames])).all()

        fetchedTagNames = [tag.name for tag in tags]
        notExistingTagNames = list(set(tagNames) - set(fetchedTagNames))

        for name in notExistingTagNames:
            tag = Tag(_user=user, name=name, type=type)
            tags.append(tag)

        return TagGroup(_user=user, tags=tags)
