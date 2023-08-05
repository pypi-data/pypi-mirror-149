#!/usr/bin/env python
# encoding: utf-8
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2020 Indiscale GmbH <info@indiscale.com>
# Copyright (C) 2020 Florian Sprckelsen <f.spreckelsen@indiscale.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# ** end header
"""Implements a class for finding and storing missing entities, either
record types or properties, that are missing in a data model. They can
be inserted by hand or gueesed from possible exceptions when inserting
or updating entities with missing parents and/or properties.

"""
from caosdb.exceptions import (EntityDoesNotExistError,
                               TransactionError,
                               UnqualifiedParentsError,
                               UnqualifiedPropertiesError)


class DataModelProblems(object):
    """ Collect and store missing RecordTypes and Properties."""
    missing = set()

    @staticmethod
    def add(ent):
        """Add a missing record type or property."""
        DataModelProblems.missing.add(ent)

    @staticmethod
    def _evaluate_unqualified(e):
        """Evaluate all UnqualifiedParentsErrors and
        UnqualifiedPropertiesErrors and check for possible datamodel
        problems.

        """
        # UnqualifiedParentsErrors are always possible problems:
        if isinstance(e, UnqualifiedParentsError):
            for err in e.errors:
                DataModelProblems.add(err.entity.name)
        elif isinstance(e, UnqualifiedPropertiesError):
            # Only those UnqualifiedPropertiesErrors that were caused
            # by (at least) an EntityDoesNotExistError are possible
            # datamodel problems
            for err in e.errors:
                if isinstance(err, EntityDoesNotExistError):
                    DataModelProblems.add(err.entity.name)
        # If there is at least one UnqualifiedParentsError or at least
        # one UnqualifiedPropertiesError on some level below, go
        # through the children.
        elif (e.has_error(UnqualifiedParentsError) or
              e.has_error(UnqualifiedPropertiesError)):
            for err in e.errors:
                DataModelProblems._evaluate_unqualified(err)

    @staticmethod
    def evaluate_exception(e):
        """Take a TransactionError, see whether it was caused by datamodel
        problems, and update missing parents and/or properties if this
        was the case. Afterwards, raise the exception.

        Parameters
        ----------
        e : TransactionError
            TransactionError, the children of which are checked for
            possible datamodel problems.

        """
        if not isinstance(e, TransactionError):
            raise ValueError(
                "Only TransactionErrors can be checked for datamodel problems")

        if (e.has_error(UnqualifiedParentsError) or
                e.has_error(UnqualifiedPropertiesError)):
            for err in e.errors:
                DataModelProblems._evaluate_unqualified(err)

        raise e
