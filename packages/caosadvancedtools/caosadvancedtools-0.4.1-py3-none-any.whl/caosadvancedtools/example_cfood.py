#!/usr/bin/env python
# encoding: utf-8
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2018 Research Group Biomedical Physics,
# Max-Planck-Institute for Dynamics and Self-Organization Göttingen
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

from .cfood import AbstractFileCFood, assure_has_property


class ExampleCFood(AbstractFileCFood):
    @classmethod
    def get_re(cls):
        return (r".*/(?P<species>[^/]+)/"
                r"(?P<date>\d{4}-\d{2}-\d{2})/README.md")

    def create_identifiables(self):
        self.experiment = db.Record()
        self.experiment.add_parent(name="Experiment")
        self.experiment.add_property(name="date",
                                     value=self.match.group('date'))
        self.identifiables.append(self.experiment)

    def update_identifiables(self):
        assure_has_property(
            self.experiment,
            "species",
            self.match.group('species'))
