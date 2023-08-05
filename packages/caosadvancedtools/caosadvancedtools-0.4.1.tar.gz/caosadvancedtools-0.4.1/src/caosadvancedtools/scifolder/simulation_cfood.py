#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (C) 2019 Henrik tom Wörden
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
                                     assure_has_property,
                                     assure_object_is_in_list, get_entity)
from caosadvancedtools.read_md_header import get_header

from .generic_pattern import full_pattern
from .utils import (get_files_referenced_by_field, parse_responsibles,
                    reference_records_corresponding_to_files)
from .withreadme import DATAMODEL as dm
from .withreadme import (RESULTS, REVISIONOF, SCRIPTS, SOURCES, WithREADME,
                         get_glob)


class SimulationCFood(AbstractFileCFood, WithREADME):
    # win_paths can be used to define fields that will contain windows style
    # path instead of the default unix ones. Possible fields are:
    # ["results", "sources", "scripts", "revisionOf"]
    win_paths = []

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        WithREADME.__init__(self)

    def collect_information(self):
        self.find_referenced_files([RESULTS, SOURCES, SCRIPTS])

    @staticmethod
    def get_re():
        return ".*/SimulationData/" + full_pattern

    def create_identifiables(self):
        # create the project identifiable
        self.project = db.Record(name=self.match.group("project_identifier"))
        self.project.add_parent(name="Project")
        self.identifiables.append(self.project)

        self.simulation = db.Record()
        # import IPython
        # IPython.embed()
        self.simulation.add_parent(name="Simulation")
        self.simulation.add_property(
            name="date", value=self.match.group("date"))

        self.simulation.add_property(name="Project", value=self.project)

        if self.match.group("suffix") is not None:
            self.simulation.add_property(
                name="identifier", value=self.match.group("suffix"))
        else:
            # TODO empty string causes an error in search
            self.simulation.add_property(name="identifier",
                                              value="empty_identifier")
        self.identifiables.append(self.simulation)
        self.people = parse_responsibles(self.header)
        self.identifiables.extend(self.people)

    def update_identifiables(self):
        assure_has_property(self.simulation, "description",
                            self.header["description"][0],
                            to_be_updated=self.to_be_updated)

        # TODO why is here no db.LIST("Person") possible?

        assure_object_is_in_list(self.people, self.simulation,
                                 "responsible",
                                 self.to_be_updated,
                                 datatype=db.LIST(db.REFERENCE))

        if SOURCES.key in self.header:                         # pylint: disable=unsupported-membership-test
            reference_records_corresponding_to_files(
                    record=self.simulation,
                    recordtypes=["Experiment", "Publication", "Simulation",
                                 "Analysis"],
                    globs=get_glob(self.header[SOURCES.key]),  # pylint: disable=unsubscriptable-object
                    property_name=dm.sources,
                    path=self.crawled_path,
                    to_be_updated=self.to_be_updated)
        self.reference_files_from_header(record=self.simulation)

        if REVISIONOF.key in self.header:                      # pylint: disable=unsupported-membership-test
            reference_records_corresponding_to_files(
                record=self.simulation,
                recordtypes=[dm.Software],                     # pylint: disable=no-member
                property_name=dm.revisionOf,
                globs=get_glob(self.header[dm.revisionOf]),    # pylint: disable=unsubscriptable-object
                path=self.crawled_path,
                to_be_updated=self.to_be_updated)
