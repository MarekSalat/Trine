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
        permission_admin = model.Permission()
        permission_admin.name = 'all'
        permission_admin.description = 'This permission give an all possible permission'

        permission_trine = model.Permission()
        permission_trine.name = 'trine'
        permission_trine.description = 'This permission give a basic user right to add, edit, delete transactions,tag groups, tags and own credentials'

        user_group_admins = model.UserGroup()
        user_group_admins.name = 'admins'
        user_group_admins.display_name = 'Admins group'
        user_group_admins.permissions = [permission_admin, permission_trine]

        user_group_trine = model.UserGroup()
        user_group_trine.name = 'trine user'
        user_group_trine.display_name = 'Trine users group'
        user_group_admins.permissions = [permission_trine]

        user_admin = model.User()
        user_admin.name = 'mareks'
        user_admin.display_name = 'Marek Salát'
        user_admin.email = 'mareks@trine.com'
        user_admin.password = 'mareks'
        user_admin.defaultCurrency = "CZK"
        user_admin.groups = [user_group_admins]

        user_trine = model.User()
        user_trine.name = 'mareks2'
        user_trine.display_name = 'Example basic user'
        user_trine.email = 'mareks2@trine.com'
        user_trine.password = 'mareks2'
        user_trine.defaultCurrency = "EUR"
        user_trine.groups = [user_group_trine]

        for user in [user_admin, user_trine]:
            grocery = Tag(name="grocery", user=user)
            beers = Tag(name="beers", user=user)
            home = Tag(name="home", user=user)
            traveling = Tag(name="traveling", user=user)
            bus = Tag(name="bus", user=user)
            train = Tag(name="train", user=user)

            cash = Tag(name="cash", type=Tag.TYPE_INCOME, user=user)
            account = Tag(name="account", type=Tag.TYPE_INCOME, user=user)
            salary = Tag(name="salary", type=Tag.TYPE_INCOME, user=user)

            transactions = []

            group_cash = TagGroup(tags=[cash], user=user)
            group_account = TagGroup(tags=[account], user=user)
            group_account_salary = TagGroup(tags=[account, salary], user=user)

            transactions.append(Transaction(
                amount=500,
                incomeTagGroup=group_cash,
                user=user
            ))

            transactions.append(Transaction(
                amount=5000,
                foreignCurrencyAmount=5000 / 28,
                foreignCurrency="EUR",
                incomeTagGroup=group_account_salary,
                user=user
            ))

            source, target = Transaction.new_transfer(Transaction(
                amount=-500,
				foreignCurrencyAmount=0,
                user=user
            ), group_account, group_cash)
            transactions.append(source)
            transactions.append(target)

            transactions.append(Transaction(
                amount=-50,
                incomeTagGroup=group_cash,
                expenseTagGroup=TagGroup(tags=[grocery, beers], user=user),
                user=user
            ))

            transactions.append(Transaction(
                amount=-150,
                incomeTagGroup=group_account,
                expenseTagGroup=TagGroup(tags=[traveling, bus], user=user),
                user=user
            ))

            group_traveling_train = TagGroup(tags=[traveling, train], user=user)
            transactions.append(Transaction(
                amount=-200,
                incomeTagGroup=group_cash,
                expenseTagGroup=group_traveling_train,
                user=user
            ))

            transactions.append(Transaction(
                amount=-128,
                incomeTagGroup=group_account,
                expenseTagGroup=group_traveling_train,
                user=user
            ))

            transactions.append(Transaction(
                amount=-42,
                incomeTagGroup=group_account,
                expenseTagGroup=TagGroup(tags=[grocery, home, beers], user=user),
                user=user
            ))

            model.DBSession.add_all(transactions)
            model.DBSession.flush()

        alchtransaction.commit()
    except IntegrityError:
        print('Warning, there was a problem adding your auth data, it may have already been added:')
        import traceback

        print(traceback.format_exc())
        alchtransaction.abort()
        print('Continuing with bootstrapping...')

        # <websetup.bootstrap.after.auth>
