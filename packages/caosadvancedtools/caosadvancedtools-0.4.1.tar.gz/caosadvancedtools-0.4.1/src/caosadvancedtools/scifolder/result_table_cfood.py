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

import re

import caosdb as db
import pandas as pd
from caosadvancedtools.cfood import (AbstractFileCFood, assure_has_description,
                                     assure_has_parent, assure_has_property,
                                     assure_object_is_in_list, get_entity)
from caosadvancedtools.read_md_header import get_header

from ..cfood import assure_property_is, fileguide
from .experiment_cfood import ExperimentCFood
from .generic_pattern import date_pattern, date_suffix_pattern, project_pattern
from .utils import parse_responsibles, reference_records_corresponding_to_files
from .withreadme import DATAMODEL as dm
from .withreadme import RESULTS, REVISIONOF, SCRIPTS, WithREADME, get_glob


# TODO similarities with TableCrawler
class ResultTableCFood(AbstractFileCFood):

    # win_paths can be used to define fields that will contain windows style
    # path instead of the default unix ones. Possible fields are:
    # ["results", "revisionOf"]
    win_paths = []
    table_re = r"result_table_(?P<recordtype>.*).csv$"
    property_name_re = re.compile(r"^(?P<pname>.+?)\s*(\[\s?(?P<unit>.*?)\s?\] *)?$")

    @staticmethod
    def name_beautifier(x): return x

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.table = pd.read_csv(fileguide.access(self.crawled_path))

    @staticmethod
    def get_re():
        return (".*/ExperimentalData/"+project_pattern + date_pattern +
                date_suffix_pattern + ResultTableCFood.table_re)

    def create_identifiables(self):
        self.recs = []
        self.experiment, self.project = (
            ExperimentCFood.create_identifiable_experiment(self.match))

        for idx, row in self.table.iterrows():
            rec = db.Record()
            rec.add_parent(self.match.group("recordtype"))

            for col in self.table.columns[:2]:
                match = re.match(ResultTableCFood.property_name_re, col)

                if match.group("unit"):
                    rec.add_property(match.group("pname"), row.loc[col], unit=match.group("unit"))
                else:
                    rec.add_property(match.group("pname"), row.loc[col])
            self.identifiables.append(rec)
            self.recs.append(rec)

        self.identifiables.extend([self.project, self.experiment])

    def update_identifiables(self):
        for ii, (idx, row) in enumerate(self.table.iterrows()):
            for col in row.index:
                match = re.match(ResultTableCFood.property_name_re, col)
                assure_property_is(self.recs[ii], match.group("pname"), row.loc[col], to_be_updated=self.to_be_updated)
        assure_property_is(self.experiment, self.match.group("recordtype"),
                           self.recs, to_be_updated=self.to_be_updated,
                           datatype=db.LIST(self.match.group("recordtype")))
