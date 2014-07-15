# -*- coding: utf-8 -*-
"""
Auth* related model.

This is where the models used by the authentication stack are defined.

It's perfectly fine to re-use this definition in the trine application,
though.

"""
import os
from datetime import datetime
from hashlib import sha256

from trine.utils.uuidType import UuidColumn
from trine.utils.AutoRepr import AutoRepr
from trine.utils.uuidType import id_column


__all__ = ['User', 'UserGroup', 'Permission']

from sqlalchemy import Table, ForeignKey, Column, String, TIMESTAMP
from sqlalchemy.types import Unicode
from sqlalchemy.orm import relation, synonym

from trine.model import DeclarativeBase, metadata, DBSession

# This is the association table for the many-to-many relationship between
# groups and permissions.
group_permission_table = Table('groups_permissions', metadata,
    Column('group_id',      UuidColumn(), ForeignKey('UserGroup.id',  onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
    Column('permission_id', UuidColumn(), ForeignKey('Permission.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
)

# This is the association table for the many-to-many relationship between
# groups and members - this is, the memberships.
user_group_table = Table('users_groups', metadata,
    Column('user_id',  UuidColumn(), ForeignKey('User.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
    Column('group_id', UuidColumn(), ForeignKey('UserGroup.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
)


class UserGroup(DeclarativeBase, AutoRepr):
    """
    Group definition

    Only the ``group_name`` column is required.

    """

    __tablename__ = 'UserGroup'

    id = id_column()
    name = Column(Unicode(16), unique=True, nullable=False)
    display_name = Column(Unicode(255))
    created = Column(TIMESTAMP, default=datetime.now)
    users = relation('User', secondary=user_group_table, backref='groups')

    def __unicode__(self):
        return self.group_name


class User(DeclarativeBase, AutoRepr):
    """
    User definition.

    This is the user definition used by :mod:`repoze.who`, which requires at
    least the ``user_name`` column.

    """
    __tablename__ = 'User'

    id = id_column()
    name = Column(Unicode(255), unique=True, nullable=False)
    email = Column(Unicode(255), unique=True, nullable=False)
    display_name = Column(Unicode(255))
    _password = Column('password', Unicode(128))
    created = Column(TIMESTAMP, default=datetime.now)

    defaultCurrency = Column(String(3))
    defaultTimezone = Column(String(3), default='UTC', nullable=True)

    def __unicode__(self):
        return self.display_name or self.name

    class __sprox__(object):
        hide_fields = ['tags', 'transactions', 'tagGroups']

    @property
    def permissions(self):
        """Return a set with all permissions granted to the user."""
        perms = set()
        for g in self.groups:
            perms = perms | set(g.permissions)
        return perms

    @classmethod
    def by_email_address(cls, email):
        """Return the user object whose email address is ``email``."""
        return DBSession.query(cls).filter_by(email=email).first()

    @classmethod
    def by_user_name(cls, username):
        """Return the user object whose user name is ``username``."""
        return DBSession.query(cls).filter_by(name=username).first()

    @classmethod
    def _hash_password(cls, password):
        salt = sha256()
        salt.update(os.urandom(60))
        salt = salt.hexdigest()

        hash = sha256()
        # Make sure password is a str because we cannot hash unicode objects
        hash.update((password + salt).encode('utf-8'))
        hash = hash.hexdigest()

        password = salt + hash

        return password

    def _set_password(self, password):
        """Hash ``password`` on the fly and store its hashed version."""
        self._password = self._hash_password(password)

    def _get_password(self):
        """Return the hashed version of the password."""
        return self._password

    password = synonym('_password', descriptor=property(_get_password,
                                                        _set_password))

    def validate_password(self, password):
        """
        Check the password against existing credentials.

        :param password: the password that was provided by the user to
            try and authenticate. This is the clear text version that we will
            need to match against the hashed one in the database.
        :type password: unicode object.
        :return: Whether the password is valid.
        :rtype: bool

        """
        hash = sha256()
        hash.update((password + self.password[:64]).encode('utf-8'))
        return self.password[64:] == hash.hexdigest()


class Permission(DeclarativeBase, AutoRepr):
    """
    Permission definition.

    Only the ``permission_name`` column is required.

    """

    __tablename__ = 'Permission'

    id = id_column()
    name = Column(Unicode(63), unique=True, nullable=False)
    description = Column(Unicode(255))

    groups = relation(UserGroup, secondary=group_permission_table,
                      backref='permissions')

    def __unicode__(self):
        return self.name
