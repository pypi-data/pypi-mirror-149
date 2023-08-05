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
from caosadvancedtools.cfood import (AbstractFileCFood,
                                     assure_object_is_in_list, fileguide,
                                     get_entity)
from caosadvancedtools.read_md_header import get_header
from caosadvancedtools.utils import find_records_that_reference_ids

from .generic_pattern import date_suffix_pattern, readme_pattern
from .utils import (get_files_referenced_by_field, parse_responsibles,
                    reference_records_corresponding_to_files)
from .withreadme import DATAMODEL as dm
from .withreadme import (RESULTS, REVISIONOF, SCRIPTS, SOURCES, WithREADME,
                         get_glob)


def folder_to_type(name):
    if name == "Theses":
        return "Thesis"
    elif name == "Articles":
        return "Article"
    elif name == "Posters":
        return "Poster"
    elif name == "Presentations":
        return "Presentation"
    elif name == "Reports":
        return "Report"
    else:
        raise ValueError()


class PublicationCFood(AbstractFileCFood, WithREADME):
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
        # matches anything but "/", i.e. a folder name
        _prefix = ".*/Publications/"
        _type = r"(?P<type>Theses|Articles|Posters|Presentations|Reports)/"
        _partial_date = r"(?P<date>\d{2,4}([-_]\d{1,2}[-_]\d{1,2})?)"

        return _prefix+_type+_partial_date+date_suffix_pattern+readme_pattern

    def create_identifiables(self):
        header = get_header(fileguide.access(self.crawled_path))
        self.publication = db.Record(name=self.match.group("date")
                                     + "_"+self.match.group("suffix"))
        self.publication.add_parent(name=folder_to_type(
            self.match.group("type")))
        self.identifiables.append(self.publication)

        self.people = parse_responsibles(header)
        self.identifiables.extend(self.people)

    def update_identifiables(self):
        header = get_header(fileguide.access(self.crawled_path))
        self.publication.description = header["description"][0]

        assure_object_is_in_list(self.people, self.publication,
                                 "responsible",
                                 self.to_be_updated,
                                 datatype=db.LIST(db.REFERENCE))

        if SOURCES.key in self.header:
            reference_records_corresponding_to_files(
                    record=self.publication,
                    recordtypes=[dm.Experiment, dm.Publication, dm.Simulation,
                                 dm.Analysis],
                    globs=get_glob(self.header[SOURCES.key]),
                    property_name=dm.sources,
                    path=self.crawled_path,
                    to_be_updated=self.to_be_updated)
        self.reference_files_from_header(record=self.publication)

        if REVISIONOF.key in self.header:
            reference_records_corresponding_to_files(
                record=self.publication,
                recordtypes=[dm.Publication],
                property_name=dm.revisionOf,
                globs=get_glob(self.header[REVISIONOF.key]),
                path=self.crawled_path,
                to_be_updated=self.to_be_updated)
