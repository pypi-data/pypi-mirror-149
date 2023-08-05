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
from itertools import chain

import caosdb as db
import pandas as pd
from caosadvancedtools.cfood import assure_object_is_in_list, fileguide
from caosadvancedtools.utils import (find_records_that_reference_ids,
                                     read_field_as_list,
                                     return_field_or_property,
                                     string_to_person)

logger = logging.getLogger("caosadvancedtools")


def parse_responsibles(header):
    """
    Extract the responsible person(s) from the yaml header.

    If field responsible is a list every entry from that list will be added as
    a person.
    Currently only the format <Firstname> <Lastname> <*> is supported.
    If it is a simple string, it is added as the only person.
    """
    people = []

    for person in read_field_as_list(header["responsible"]):
        people.append(string_to_person(person))

    return people


def get_files_referenced_by_field(globs, prefix="", final_glob=None):
    """
    returns all file entities at paths described by given globs

    This function assumes that the supplied globs is a list of
    filenames, directories or globs.

    prefix should be the path of the crawled file to supply a context for
    relative paths.
    """
    referenced_files = []
    globs = [g for g in globs if g is not None]

    for glob in globs:
        # TODO extract glob manipulation

        if final_glob is not None and not glob.endswith(final_glob):
            glob += final_glob

        if not glob.startswith("/"):
            glob = os.path.normpath(os.path.join(prefix, glob))
        else:
            glob = os.path.normpath(glob)

        query_string = "FIND file which is stored at {}".format(glob)
        logger.debug(query_string)

        el = db.execute_query(query_string)

        referenced_files.append(el)

    return referenced_files


def is_filename_allowed(path, recordtype):
    if recordtype.lower() == "experiment":
        if "ExperimentalData" in path:
            return True
    elif recordtype.lower() == "analysis":
        if "DataAnalysis" in path:
            return True
    elif recordtype.lower() == "publication":
        if "Publication" in path:
            return True
    elif recordtype.lower() == "simulation":
        if "Simulation" in path:
            return True

    return False


def get_entity_ids_from_include_file(prefix, file_path):
    """reads version ids from  include file """

    if not file_path.startswith("/"):
        file_path = os.path.normpath(os.path.join(prefix, file_path))
    else:
        file_path = os.path.normpath(file_path)
    df = pd.read_csv(fileguide.access(file_path), sep="\t", comment="#")

    if "ID" not in df.columns:
        raise ValueError("Include file must have an ID column")

    return list(df.ID)


def reference_records_corresponding_to_files(record, recordtypes, globs, path,
                                             to_be_updated, property_name):
    # TODO this function needs to be refactored:
    # the treatement of keys like 'results' should be separated from searching
    # entities (see setting of globs and includes below).

    for recordtype in recordtypes:

        directly_named_files = list(chain(*get_files_referenced_by_field(
            globs,
            prefix=os.path.dirname(path))))

        files_in_folders = list(chain(*get_files_referenced_by_field(
            globs,
            prefix=os.path.dirname(path),
            final_glob="/**")))
        files = [f for f in directly_named_files + files_in_folders if
                 is_filename_allowed(f.path, recordtype=recordtype)]
        logger.debug("Referenced files:\n" + str(files))
        entities = find_records_that_reference_ids(
            list(set([
                fi.id for fi in files])),
            rt=recordtype)
        logger.debug("Referencing entities:\n" + str(entities))

        if len(entities) == 0:
            continue
        else:
            assure_object_is_in_list(entities,
                                     record,
                                     property_name,
                                     to_be_updated,
                                     datatype=db.LIST(db.REFERENCE))


def create_files_list(df, ftype):
    files = []

    for indx, src in df.loc[ftype,
                            pd.notnull(df.loc[ftype])].iteritems():
        desc = df.loc[ftype+" description", indx]

        if pd.notnull(desc):
            files.append({'file': src, 'description': desc})
        else:
            files.append(src)

    return files


def add_value_list(header, df, name):
    if name in df.index:
        header[name] = list(df.loc[name, pd.notnull(df.loc[name])])


def get_xls_header(filepath):
    """
    This function reads an xlsx file and creates a dictionary analogue to the
    one created by the yaml headers in README.md files read with the get_header
    function of caosdb-advancedtools.
    As xlsx files lack the hierarchical structure, the information that can be
    provided is less complex. See the possibility to use the xlsx files as a
    less powerfull version for people who are not comfortable with the
    README.md files.

    The xlsx file has a defined set of rows. In each row a list of entries can
    be given. This structure is converted to a dictionary with a fix structure.
    """

    header = {}

    df = pd.read_excel(filepath, index_col=0, header=None)
    add_value_list(header, df, "responsible")
    add_value_list(header, df, "description")
    assert len(header["description"]) <= 1

    for ftype in ["sources", "scripts", "results", "sourceCode", "binaries"]:
        if ftype not in df.index:
            continue
        files = create_files_list(df, ftype)

        if len(files) > 0:
            header[ftype] = files

    add_value_list(header, df, "revisionOf")
    # there should be only one revision of

    if "revisionOf" in header:
        if len(header["revisionOf"]) > 0:
            header["revisionOf"] = header["revisionOf"][0]
    add_value_list(header, df, "tags")

    return header
