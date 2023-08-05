#!/usr/bin/env python3
# encoding: utf-8
#
# ** header v3.0
# This file is a part of the CaosDB Project.
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
#
# ** end header
#

import logging
import os
import pathlib

import caosdb as db
from caosdb.exceptions import TransactionError

logger = logging.getLogger(__name__)


def set_log_level(level):
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.DEBUG)


def replace_path_prefix(path, old_prefix, new_prefix):
    """
    Replaces the prefix old_prefix in path with new_prefix.

    Raises a RuntimeError when the path does not start with old_prefix.
    """

    if not path.startswith(old_prefix):
        raise RuntimeError(
            "Path does not start with old_prefix\n{}\nvs\n{}".format(
                path,
                old_prefix))
    path = path[len(old_prefix):]

    return os.path.join(new_prefix, path)


def string_to_person(person):
    """
    Creates a Person Record from a string.

    The following formats are supported:
    - `<Firstname> <Lastname> <*>`
    - `<Lastname(s)>,<Firstname(s)>,<*>`

    The part after the name can be used for an affiliation for example.
    """

    if "," in person:
        firstname = person.split(",")[1].strip()
        lastname = person.split(",")[0].strip()
    else:
        firstname = person.split(" ")[0].strip()
        lastname = person.split(" ")[1].strip()

    pr = db.Record()
    pr.add_parent("Person")
    pr.add_property("lastname", lastname)
    pr.add_property("firstname", firstname)

    return pr


def read_field_as_list(field):
    """
    E.g. in yaml headers entries can be single values or list. To simplify the
    work with those values, this function puts single values in a list.
    """

    if isinstance(field, list):
        return field
    else:
        return [field]


def get_referenced_files(glob, prefix=None, filename=None, location=None):
    """
    queries the database for files referenced by the provided glob

    Parameters:
    glob: the glob referencing the file(s)
    prefix: the glob can be relative to some path, in that case that path needs
            to be given as prefix
    filename: the file in which the glob is given (used for error messages)
    location: the location in the file in which the glob is given (used for
              error messages)
    """

    orig_glob = glob

    if not glob.startswith("/") and prefix is not None:
        glob = os.path.join(prefix, glob)
    glob = os.path.normpath(glob)
    try:
        query_string = "FIND file which is stored at {}".format(glob)
        logger.debug(query_string)
        files = db.execute_query(query_string)
    except TransactionError:
        logger.error(
            "In {} in file \n{}\nthe expression '{}' does not "
            "allow a search for files. Please make sure "
            "it is valid.".format(
                location,
                filename,
                orig_glob
            )
        )

        return []

    if len(files) == 0:
        logger.warning(
            "In {} in file \n{}\nthe expression '{}' does not "
            "reference any known files".format(
                location,
                filename,
                orig_glob
            )
        )

    return files


def check_win_path(path, filename=None):
    """
    check whether '/' are in the path but no '\'.

    If that is the case, it is likely, that the path is not a Windows path.

    Parameters:
    path: path to be checked
    filename: if the path is located in a file, this parameter can be used to
              direct the user to the file where the path is located.
    """

    if r"\\" not in path and "/" in path:
        if filename:
            msg = "In file\n{}\nthe ".format(filename)
        else:
            msg = "The "
        msg += ("path\n{}\ndoes not look like "
                "a Windows path.".format(path))
        logger.warning(msg, extra={'identifier': str(path),
                                   'category': "inconsistency"})

        return False

    return True


def return_field_or_property(value, prop=None):
    """
    returns value itself of a property.

    Typical in yaml headers is that a field might sometimes contain a single
    value and other times a dict itself. This function either returns the
    single value or (in case of dict as value) a value of the dict.
    """

    if isinstance(value, dict) and prop in value:
        return value[prop]
    else:
        return value


def find_records_that_reference_ids(referenced_ids, rt="", step_size=50):
    """ Returns a list with ids of records that reference entities with
    supplied ids

    Sometimes a file or folder will be referenced in a README.md (e.g. in an
    Analysis) but not those files shall be referenced but the corresponding
    object  (e.g. the Experiment). Thus the ids of all Records (of a suitable
    type) are collected that reference one or more of the supplied ids.
    This is done in chunks as the ids are passed in the header of the http
    request.
    """
    record_ids = set()
    index = 0

    while index < len(referenced_ids):
        subset = referenced_ids[index:min(
            index+step_size, len(referenced_ids))]
        try:
            q_string = ("FIND Record {} which references \n".format(rt)
                        + " or which references \n".join(
                            [str(el) for el in subset]))
            exps = db.execute_query(q_string)
            record_ids.update([exp.id for exp in exps])
        except Exception as e:
            print(e)
            pass

        index += step_size

    return list(record_ids)
