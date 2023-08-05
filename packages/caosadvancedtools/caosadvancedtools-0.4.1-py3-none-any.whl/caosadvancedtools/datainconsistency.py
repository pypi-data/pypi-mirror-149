#!/usr/bin/env python
# encoding: utf-8
#
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2020 Indiscale GmbH <info@indiscale.com>
# Copyright (C) 2020 Henrik tom Wörden <h.tomwoerden@indiscale.com>
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

"""Implements an error to be used when there is a problem with the data to be
read. I.e. something that users of CaosDB need to fix.

"""


class DataInconsistencyError(ValueError):
    pass
