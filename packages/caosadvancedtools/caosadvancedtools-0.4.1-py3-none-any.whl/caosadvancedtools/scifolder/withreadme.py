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


import logging
import os
from dataclasses import dataclass

import caosdb as db
from caosadvancedtools.cfood import (assure_has_description, assure_has_parent,
                                     assure_object_is_in_list, fileguide)
from caosadvancedtools.read_md_header import get_header as get_md_header
from caosadvancedtools.table_importer import (win_path_converter,
                                              win_path_list_converter)
from caosadvancedtools.utils import return_field_or_property

from .utils import (get_entity_ids_from_include_file,
                    get_files_referenced_by_field, get_xls_header)

LOGGER = logging.getLogger("withreadme")
LOGGER.setLevel(level=logging.ERROR)


@dataclass
class DataModel(object):
    results: str = "results"
    scripts: str = "scripts"
    sources: str = "sources"
    date: str = "date"
    Project: str = "Project"
    Analysis: str = "Analysis"
    identifier: str = "identifier"
    responsible: str = "responsible"
    revisionOf: str = "revisionOf"
    Experiment: str = "Experiment"
    Publication: str = "Publication"
    Simulation: str = "Simulation"
    Analysis: str = "Analysis"
    revisionOf: str = "revisionOf"
    binaries: str = "binaries"
    sourcecode: str = "sourceCode"
    description: str = "description"


DATAMODEL = DataModel()
dm = DATAMODEL


class HeaderField(object):
    def __init__(self, key, model):
        self.key = key
        self.model = model


RESULTS = HeaderField("results", dm.results)
SCRIPTS = HeaderField("scripts", dm.scripts)
SOURCES = HeaderField("sources", dm.sources)
FILE = HeaderField("file", None)
INCLUDE = HeaderField("include", None)
REVISIONOF = HeaderField("revisionOf", dm.revisionOf)
BINARIES = HeaderField("binaries", dm.binaries)
SOURCECODE = HeaderField("sourceCode", dm.sourcecode)
DESCRIPTION = HeaderField("description", dm.description)
RECORDTYPE = HeaderField("recordtype", None)


def get_glob(field):
    """ takes a field which must be a list of globs or dicts.

    if it is a dict, it must have either an include or a file key"""
    globs = []

    if not isinstance(field, list):
        field = [field]

    for value in field:

        if isinstance(value, dict) and INCLUDE.key in value:
            continue

        globs.append(return_field_or_property(value, FILE.key))

    return globs


def get_description(value):
    if isinstance(value, dict) and DESCRIPTION.key in value:
        return value[DESCRIPTION.key]
    else:
        return None


def get_rt(value):
    if isinstance(value, dict) and RECORDTYPE.key in value:
        return value[RECORDTYPE.key]
    else:
        return None


class WithREADME(object):
    def __init__(self):
        self._header = None
        self.ref_files = {}

    @property
    def header(self):
        if self._header is None:
            if self.crawled_path.lower().endswith(".md"):  # pylint: disable=no-member
                self._header = get_md_header(
                    fileguide.access(self.crawled_path))   # pylint: disable=no-member
            elif self.crawled_path.lower().endswith(".xlsx"):  # pylint: disable=no-member
                self._header = get_xls_header(
                    fileguide.access(self.crawled_path))       # pylint: disable=no-member
            else:
                raise RuntimeError("Readme format not recognized.")
            self.convert_win_paths()

        return self._header

    def find_referenced_files(self, fields):
        """ iterates over given fields in the header and searches for files

        if the field contains a glob. The file entities are attached"""

        for field in fields:

            if field.key not in self.header:
                continue

            globs = get_glob(self.header[field.key])
            files = get_files_referenced_by_field(
                globs, prefix=os.path.dirname(self.crawled_path))  # pylint: disable=no-member

            description = [get_description(val) for val in
                           self.header[field.key]]
            recordtype = [get_rt(val) for val in self.header[field.key]]
            self.ref_files[field.model] = [
                (f, d, r) for f, d, r in zip(files, description, recordtype)]
            # flatten returned list of file lists
            flat_list = [f.path for sublist in files
                         for f in sublist]

            if len(flat_list) == 0:
                LOGGER.warn("ATTENTION: the field {} does not reference any "
                            "known files".format(field.key))

            self.attached_filenames.extend(flat_list)  # pylint: disable=no-member

    def convert_path(self, el):
        """ converts the path in el to unix type

        el can be a dict of a string. If el is dict it must have a file key

        returns: same type as el
        """

        if isinstance(el, dict):
            if INCLUDE.key in el:
                el[INCLUDE.key] = win_path_converter(el[INCLUDE.key])

                return el

            if FILE.key not in el:
                raise ValueError("field should have a 'file' attribute")
            el[FILE.key] = win_path_converter(el[FILE.key])

            return el
        else:
            return win_path_converter(el)

    def convert_win_paths(self):
        for field in self.win_paths:  # pylint: disable=no-member
            if field in self.header:

                if isinstance(self.header[field], list):
                    self.header[field] = [
                        self.convert_path(el) for el in self.header[field]]
                else:
                    self.header[field] = self.convert_path(self.header[field])

    def reference_files_from_header(self, record):
        """adds properties that reference the files collected in ref_files

        ref_files is expected to be a list of (files, description, recordtype)
        tuples, where files is the list of file entities, description the description
        that shall be added to each and recordtype the recordtype that the
        files shall get as parent. files may be an empty list and description
        and recordtype may be None.

        The files will be grouped according to the keys used in ref_files and
        the record types. The record types take precedence.
        """
        references = {}

        for prop_name, ref_tuple in self.ref_files.items():
            generic_references = []

            for files, description, recordtype in ref_tuple:
                if len(files) == 0:
                    continue

                if description is not None:
                    for fi in files:
                        assure_has_description(fi, description, force=True)

                if recordtype is None:
                    generic_references.extend(files)
                else:
                    for fi in files:
                        # fix parent
                        assure_has_parent(fi, recordtype, force=True,
                                          unique=False)

                    if recordtype not in references:
                        references[recordtype] = []
                    references[recordtype].extend(files)

            if len(generic_references) > 0:
                assure_object_is_in_list(
                    generic_references,
                    record,
                    prop_name,
                    to_be_updated=self.to_be_updated,
                    datatype=db.LIST(db.REFERENCE),
                )

        for ref_type in references.keys():
            assure_object_is_in_list(
                references[ref_type],
                record,
                ref_type,
                to_be_updated=self.to_be_updated,  # pylint: disable=no-member
            )

    def reference_included_records(self, record, fields, to_be_updated):
        """ iterates over given fields in the header and searches for files

        if the field contains a glob. The file entities are attached"""

        for field in fields:

            if field.key not in self.header:  # pylint: disable=no-member
                continue
            included = []

            for item in self.header[field.key]:  # pylint: disable=no-member
                if INCLUDE.key in item:
                    try:
                        included.extend(
                            get_entity_ids_from_include_file(
                                os.path.dirname(self.crawled_path),  # pylint: disable=no-member
                                item[INCLUDE.key]))
                    except ValueError:
                        al = logging.getLogger("caosadvancedtools")
                        al.warning("The include file cannot be read. Please "
                                   "make sure, it contains an 'ID' column."
                                   " The file is ignored."
                                   "\n{}".format(item[INCLUDE.key]))

            assure_object_is_in_list(included,
                                     record,
                                     field.model,
                                     to_be_updated,
                                     datatype=db.LIST(db.REFERENCE))
