#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (C) 2019 IndiScale GmbH <info@indiscale.com>
# Copyright (C) 2019 Henrik tom Wörden <h.tomwoerden@indiscale.com>
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

import os
from itertools import chain

import caosdb as db
from caosadvancedtools.cfood import (AbstractFileCFood, assure_has_parent,
                                     assure_has_property, assure_name_is,
                                     assure_object_is_in_list, get_entity)
from caosadvancedtools.guard import global_guard as guard
from caosadvancedtools.read_md_header import get_header

from .generic_pattern import full_pattern
from .utils import get_files_referenced_by_field, parse_responsibles
from .withreadme import BINARIES
from .withreadme import DATAMODEL as dm
from .withreadme import SOURCECODE, WithREADME


class SoftwareCFood(AbstractFileCFood, WithREADME):
    _prefix = ".*/Software/"
    # win_paths can be used to define fields that will contain windows style
    # path instead of the default unix ones. Possible fields are:
    # ["binaries", "sourceCode","revisionOf"]
    win_paths = []

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        WithREADME.__init__(self)

    def collect_information(self):
        self.find_referenced_files([BINARIES, SOURCECODE])

    @staticmethod
    def get_re():

        return SoftwareCFood._prefix + full_pattern

    def create_identifiables(self):
        # The software is a record type. Let's try to find it.
        self.software = db.execute_query(
            "FIND RecordType Software with name = {}".format(
                self.match.group("project_identifier")))

        if len(self.software) == 0:
            # Software not found insert if allowed
            self.software = db.RecordType(
                name=self.match.group("project_identifier"))
            self.software.add_parent(name="Software")
            self.software.add_property(name="alias",
                                       value=self.match.group("project_name"))
            guard.safe_insert(self.software)
        elif len(self.software) == 1:
            self.software = self.software[0]
        else:
            raise RuntimeError("Cannot identify software record type. Multiple"
                               "matches for {}".format(
                                   self.match.group("project_identifier")))

        # create the software version
        # identifiable is made from parent and date and suffix
        self.softwareversion = db.Record()
        self.softwareversion.add_parent(self.software)
        self.softwareversion.add_property("date", self.match.group("date"))

        if self.match.group("suffix"):
            self.softwareversion.add_property(
                "version", self.match.group("suffix"))

        self.identifiables.append(self.softwareversion)

        # parse people and add them to identifiables
        # TODO People are currently 'identifiable' with their first and last
        # names. There will be conflicts
        self.people = parse_responsibles(self.header)
        self.identifiables.extend(self.people)

    def update_identifiables(self):
        version_name = self.match.group("project_name")

        if self.match.group("suffix"):
            version_name += "_"+self.match.group("suffix")
        else:
            version_name += "_"+self.match.group("date")

        assure_name_is(self.softwareversion, version_name,
                       to_be_updated=self.to_be_updated)
        assure_has_property(self.softwareversion, "description",
                            self.header["description"][0],
                            to_be_updated=self.to_be_updated)
        assure_object_is_in_list(obj=self.people,
                                 containing_object=self.softwareversion,
                                 property_name="responsible",
                                 to_be_updated=self.to_be_updated,
                                 datatype=db.LIST(db.REFERENCE)
                                 )

        self.reference_files_from_header(record=self.softwareversion)
