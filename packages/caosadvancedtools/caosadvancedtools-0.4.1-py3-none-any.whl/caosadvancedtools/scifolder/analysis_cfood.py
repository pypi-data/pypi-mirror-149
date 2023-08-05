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


class AnalysisCFood(AbstractFileCFood, WithREADME):
    _prefix = ".*/DataAnalysis/"

    # win_paths can be used to define fields that will contain windows style
    # path instead of the default unix ones. Possible fields are:
    # ["results", "sources", "scripts","revisionOf"]
    win_paths = []

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        WithREADME.__init__(self)

    def collect_information(self):
        self.find_referenced_files([RESULTS, SOURCES, SCRIPTS])

    @staticmethod
    def name_beautifier(name):
        """ a function that can be used to rename the project. I.e. if
        the project in CaosDB shall be named differently than in the folder
        structure.
        Use discouraged.
        """

        return name

    @staticmethod
    def get_re():
        return AnalysisCFood._prefix + full_pattern

    def create_identifiables(self):
        # create the project identifiable
        name = AnalysisCFood.name_beautifier(
            self.match.group("project_identifier"))
        self.project = db.Record(name=name)
        self.project.add_parent(name=dm.Project)
        self.identifiables.append(self.project)

        # create the Analysis identifiable
        self.analysis = db.Record()
        self.analysis.add_parent(name=dm.Analysis)
        self.analysis.add_property(name=dm.date, value=self.match.group("date"))

        self.analysis.add_property(name=dm.Project, value=self.project)
        self.identifiables.append(self.analysis)

        if self.match.group("suffix") is not None:
            self.analysis.add_property(name=dm.identifier,
                                       value=self.match.group("suffix"))
        else:
            # TODO empty string causes an error in search
            self.analysis.add_property(name=dm.identifier,
                                       value="empty_identifier")

        # parse people and add them to identifiables
        # TODO People are currently 'identifiable' due to ther first and last
        # names. There will be conflicts
        self.people = parse_responsibles(self.header)
        self.identifiables.extend(self.people)

    def update_identifiables(self):
        assure_has_property(self.analysis, "description",
                            self.header["description"][0],
                            to_be_updated=self.to_be_updated)
        assure_object_is_in_list(obj=self.people,
                                 containing_object=self.analysis,
                                 property_name=dm.responsible,
                                 to_be_updated=self.to_be_updated,
                                 datatype=db.LIST(db.REFERENCE)
                                 )
        self.reference_included_records(self.analysis,
                                        [RESULTS, SOURCES, SCRIPTS],
                                        to_be_updated=self.to_be_updated
                                        )

        if SOURCES.key in self.header:
            reference_records_corresponding_to_files(
                    record=self.analysis,
                    recordtypes=[dm.Experiment, dm.Publication, dm.Simulation,
                                 dm.Analysis],
                    globs=get_glob(self.header[SOURCES.key]),
                    property_name=dm.sources,
                    path=self.crawled_path,
                    to_be_updated=self.to_be_updated)

        self.reference_files_from_header(record=self.analysis)

        if REVISIONOF.key in self.header:
            reference_records_corresponding_to_files(
                record=self.analysis,
                recordtypes=[dm.Analysis],
                property_name=dm.revisionOf,
                globs=get_glob(self.header[REVISIONOF.key]),
                path=self.crawled_path,
                to_be_updated=self.to_be_updated)
