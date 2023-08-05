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

import caosdb as db
from caosadvancedtools.cfood import (AbstractFileCFood, assure_has_description,
                                     assure_has_parent, assure_has_property,
                                     assure_object_is_in_list, get_entity)
from caosadvancedtools.read_md_header import get_header

from .generic_pattern import full_pattern
from .utils import parse_responsibles, reference_records_corresponding_to_files
from .withreadme import DATAMODEL as dm
from .withreadme import RESULTS, REVISIONOF, SCRIPTS, WithREADME, get_glob


class ExperimentCFood(AbstractFileCFood, WithREADME):

    # win_paths can be used to define fields that will contain windows style
    # path instead of the default unix ones. Possible fields are:
    # ["results", "revisionOf"]
    win_paths = []

    @staticmethod
    def name_beautifier(x): return x

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        WithREADME.__init__(self)

        self.name_map = {},

    @staticmethod
    def get_re():
        return ".*/ExperimentalData/"+full_pattern

    def collect_information(self):
        self.find_referenced_files([RESULTS])

    @staticmethod
    def create_identifiable_experiment(match):
        # create the project identifiable
        name = ExperimentCFood.name_beautifier(
            match.group("project_identifier"))
        project = db.Record(name=name)
        project.add_parent(name=dm.Project)

        experiment = db.Record()
        experiment.add_parent(name=dm.Experiment)
        experiment.add_property(
            name=dm.date, value=match.group("date"))
        experiment.add_property(name=dm.Project, value=project)

        if match.group("suffix") is None:
            experiment.add_property(
                name="identifier", value="empty_identifier")
        else:
            experiment.add_property(name="identifier",
                                    value=match.group("suffix"))

        return [experiment, project]

    def create_identifiables(self):
        self.experiment, self.project = (
            ExperimentCFood.create_identifiable_experiment(self.match))

        self.identifiables.extend([self.project, self.experiment])
        self.people = parse_responsibles(self.header)
        self.identifiables.extend(self.people)

    def update_identifiables(self):
        # set description
        assure_has_property(self.experiment, "description",
                            self.header["description"][0],
                            to_be_updated=self.to_be_updated)

        # set responsible people
        assure_object_is_in_list(self.people, self.experiment, dm.responsible,
                                 to_be_updated=self.to_be_updated,
                                 datatype=db.LIST(db.REFERENCE))

        self.reference_files_from_header(record=self.experiment)

        if "revisionOf" in self.header:
            reference_records_corresponding_to_files(
                record=self.experiment,
                recordtypes=[dm.Experiment],
                globs=get_glob(self.header[REVISIONOF.key]),
                path=self.crawled_path,
                property_name=dm.revisionOf,
                to_be_updated=self.to_be_updated)
