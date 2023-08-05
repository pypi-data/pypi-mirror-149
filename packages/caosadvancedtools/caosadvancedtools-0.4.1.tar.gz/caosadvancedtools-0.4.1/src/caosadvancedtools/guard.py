#!/usr/bin/env python
# encoding: utf-8
#
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2020 Henrik tom Wörden
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

import caosdb as db

RETRIEVE = 0
INSERT = 1
UPDATE = 2


class ProhibitedException(Exception):
    pass


class Guard(object):

    def __init__(self, level=RETRIEVE):
        self.freshly_created = []
        self.level = level

    def safe_insert(self, obj, *args, **kwargs):
        if self.level < INSERT:
            raise ProhibitedException("not allowed")
        obj.insert(*args, **kwargs)

        if isinstance(obj, db.Container):
            self.freshly_created.extend([
                e.id for e in obj])
        else:
            self.freshly_created.append(obj.id)

    def safe_update(self, obj, *args, **kwargs):
        if isinstance(obj, db.Container):
            all_fresh = True

            for el in obj:
                if el.id not in self.freshly_created:
                    all_fresh = False

            if self.level < UPDATE and not all_fresh:
                raise ProhibitedException("not allowed")
            else:
                obj.update(*args, **kwargs)
        else:
            if self.level < UPDATE and obj.id not in self.freshly_created:
                raise ProhibitedException("not allowed")
            else:
                obj.update(*args, **kwargs)

    def set_level(self, level):
        self.level = level


global_guard = Guard()
