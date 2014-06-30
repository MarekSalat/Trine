# -*- coding: utf-8 -*-
"""Setup the trine application"""
from __future__ import print_function
from datetime import datetime
import uuid

import transaction as alchtransaction

from trine import model
from trine.model import Tag, TagGroup, Transaction


# noinspection PyArgumentList
def bootstrap(command, conf, vars):
    """Place any commands to setup trine here"""

    # <websetup.bootstrap.before.auth
    from sqlalchemy.exc import IntegrityError

    try:
        adminUser = model.User()
        adminUser.name = 'mareks'
        adminUser.display_name = 'Marek Salát'
        adminUser.email = 'mareks@trine.com'
        adminUser.password = 'mareks'
        adminUser.defaultCurrency = "CZK"

        model.DBSession.add(adminUser)

        adminsGroup = model.UserGroup()
        adminsGroup.name = 'admins'
        adminsGroup.display_name = 'Admins group'

        adminsGroup.users.append(adminUser)

        model.DBSession.add(adminsGroup)

        adminPermission = model.Permission()
        adminPermission.name = 'all'
        adminPermission.description = 'This permission give an all possible permission'
        adminPermission.groups.append(adminsGroup)

        model.DBSession.add(adminPermission)

        basicUser = model.User()
        basicUser.name = 'mareks2'
        basicUser.display_name = 'Example basic user'
        basicUser.email = 'mareks2@trine.com'
        basicUser.password = 'mareks2'
        basicUser.defaultCurrency = "EUR"

        model.DBSession.add(basicUser)

        basicUsersGroup = model.UserGroup()
        basicUsersGroup.name = 'basicUsers'
        basicUsersGroup.display_name = 'Basic users group'

        model.DBSession.add(basicUsersGroup)

        basicUserPermission = model.Permission()
        basicUserPermission.name = 'trine'
        basicUserPermission.description = 'This permission give a basic user right to add, edit, delete transactions,tag groups, tags and own credentials'
        basicUserPermission.groups.append(basicUsersGroup)

        model.DBSession.add(basicUserPermission)

        model.DBSession.flush()

        for user in [adminUser, basicUser]:
            grocery = Tag(name="grocery", _user=user)
            beers = Tag(name="beers", _user=user)
            home = Tag(name="home", _user=user)
            traveling = Tag(name="traveling", _user=user)
            bus = Tag(name="bus", _user=user)
            train = Tag(name="train", _user=user)

            cash = Tag(name="cash", type=Tag.TYPE_INCOME, _user=user)
            account = Tag(name="account", type=Tag.TYPE_INCOME, _user=user)
            salary = Tag(name="salary", type=Tag.TYPE_INCOME, _user=user)

            transactions = []

            group_cash = TagGroup(tags=[cash], _user=user)
            group_account = TagGroup(tags=[account], _user=user)
            group_account_salary = TagGroup(tags=[account, salary], _user=user)

            transactions.append(Transaction(
                amount=500,
                incomeTagGroup=group_cash,
                _user=user
            ))

            transactions.append(Transaction(
                amount=5000,
                foreignCurrencyAmount=5000 / 28,
                foreignCurrency="EUR",
                incomeTagGroup=group_account_salary,
                _user=user
            ))

            transferKey = uuid.uuid4()
            created = datetime.utcnow()

            transactions.append(Transaction(
                amount=-500,
                incomeTagGroup=group_account,
                transferKey=transferKey,
                date=created,
                _user=user
            ))

            transactions.append(Transaction(
                amount=500,
                incomeTagGroup=group_cash,
                transferKey=transferKey,
                date=created,
                _user=user
            ))

            transactions.append(Transaction(
                amount=-50,
                incomeTagGroup=group_cash,
                expenseTagGroup=TagGroup(tags=[grocery, beers], _user=user),
                _user=user
            ))

            transactions.append(Transaction(
                amount=-150,
                incomeTagGroup=group_account,
                expenseTagGroup=TagGroup(tags=[traveling, bus], _user=user),
                _user=user
            ))

            group_traveling_train = TagGroup(tags=[traveling, train], _user=user)
            transactions.append(Transaction(
                amount=-200,
                incomeTagGroup=group_cash,
                expenseTagGroup=group_traveling_train,
                _user=user
            ))

            transactions.append(Transaction(
                amount=-128,
                incomeTagGroup=group_account,
                expenseTagGroup=group_traveling_train,
                _user=user
            ))

            transactions.append(Transaction(
                amount=-42,
                incomeTagGroup=group_account,
                expenseTagGroup=TagGroup(tags=[grocery, home, beers], _user=user),
                _user=user
            ))

            for transaction in transactions:
                model.DBSession.add(transaction)

            model.DBSession.flush()

        alchtransaction.commit()
    except IntegrityError:
        print('Warning, there was a problem adding your auth data, it may have already been added:')
        import traceback

        print(traceback.format_exc())
        alchtransaction.abort()
        print('Continuing with bootstrapping...')

    # <websetup.bootstrap.after.auth>
