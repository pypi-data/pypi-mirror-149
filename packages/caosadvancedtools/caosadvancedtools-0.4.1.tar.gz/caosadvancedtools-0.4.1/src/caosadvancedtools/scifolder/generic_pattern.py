#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (C) 2020 IndiScale GmbH <info@indiscale.com>
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

""" this module contains regular expressions neeeded for the standard file
structure """


project_pattern = (r"(?P<project_identifier>"
                   r"(?P<project_year>\d{4})_?(?P<project_name>((?!/).)*))/")
date_pattern = r"(?P<date>\d{2,4}[-_]\d{1,2}[-_]\d{1,2})"
date_suffix_pattern = r"(_(?P<suffix>(((?!/).)*)))?/"
readme_pattern = r"(readme.md|README.md|readme.xlsx|README.xlsx)$"

full_pattern = (project_pattern + date_pattern + date_suffix_pattern
                # TODO: Additional level are not allowed according to the
                # specification. This should be removed or enabled via a
                # configuration
                + "(.*)"
                + readme_pattern)
