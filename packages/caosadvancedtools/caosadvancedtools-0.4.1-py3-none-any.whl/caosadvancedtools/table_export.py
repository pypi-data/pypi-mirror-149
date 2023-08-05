#!/usr/bin/env python3
# encoding: utf-8
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2020 Indiscale GmbH <info@indiscale.com>
# Copyright (C) 2020 Florian Sprecklelsen <f.spreckelsen@indiscale.com>
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
"""Collect optional and mandatory data from CaosDB records and prepare
them for an export as a table, e.g., for the export to metadata
repositories.

"""
import json
import logging

import caosdb as db

FIND_FUNCTION = "find_func"
QUERY = "query"

logger = logging.getLogger(__name__)


class TableExportError(db.CaosDBException):
    """Error that is raised in case of failing export, e.g., because of
    missing mandatory entries.

    """


class BaseTableExporter(object):
    """Base exporter class from which all actual implementations
    inherit. It contains the basic structure with a dictionary for
    optional and mandatory keys, and the error handling. The actual
    logic for finding the values to the entries has to be implemented
    elsewhere. The final results are stored in the `info` dict.

    """

    def __init__(self, export_dict, record=None,
                 raise_error_if_missing=False):
        """Initialize the exporter.

        Parameters
        ----------
        export_dict : dict or string
            dictionary with the names of the entries to be exported as
            keys. The values are again dictionaries specifying whether
            the entries are optional, which function or query should
            be used to find the value for the corresponding entry and
            possible error explanations if values are missing. Can be
            either a dict or a string specifying the path of a json
            file containing that dict. See Notes for further details.
        record : Record or None, optional
            record which is inserted into possible queries. Must be
            given if there are queries in export_dict. Default is None.
        raise_error_if_missing : bool, optional
            specify whether an error is raised if mandatory entries
            are missing or whether an error message is forwarded to a
            logger. Default is False.

        Notes
        -----
            The entries of the export_dict are themselves dictionaries
            of the form
            ```
            {"entry_to_be_exported: {
                "optional": True/False
                "find_func": name of member function
                "query": query string
                "selector": selector for the query
                "error": error explanation
                }
            }
            ```
            All entries are optional; `query` and `find_func` are
            mutually exclusive and an error will be raised if both are
            provided. The indivdual entries mean:

            - optional: True or False, if not present, the entry is
              assumed to be mandatory.
            - find_func: name of the member function that returns the
              value for this entry. Must not exist together with
              `query`
            - query: Query string for finding the value for this
              entry. If this is given, a record must be given to the
              constructor of this class. The query is then executed as
              `db.execute_query(query.format(record.id). unique=True)`
              so it must return a unique result from which the value
              can be extracted via
              `query_result.get_property_values(selector)`.
            - selector: only relevant if query is given. This is usesd
              as a selector in a call to `get_property_values` on the
              result of the query. If no selector is given, it is
              guessed from the second word of the query string (as in
              `SELECT something FROM something else`).
            - error: only relevant for mandatory entries. If the entry
              is missing, an explanatory string can be provided here
              that is used for a more verbose error output.

        """
        self.missing = []

        if isinstance(export_dict, dict):
            self.export_dict = export_dict
        else:
            try:
                with open(export_dict) as tmp:
                    self.export_dict = json.load(tmp)
            except BaseException:
                raise ValueError(
                    "export_dict must be either a dictionary"
                    " or the path to a json file.")
        self.record = record
        self._check_sanity_of_export_dict()
        self.raise_error_if_missing = raise_error_if_missing
        self.info = {}

    def collect_information(self):
        """Use the items of `export_dict` to collect the information for the
        export.

        """

        for e, d in self.export_dict.items():
            if QUERY in d:
                # TODO: How do we make this more general? There might
                # be queries that don't need the record or work with
                # the name instead of the id.
                q = d[QUERY].format(self.record.id)
                try:
                    val = db.execute_query(
                        q, unique=True).get_property_values(d["selector"])

                    if len(val) == 1:
                        val = val[0]
                except Exception as exc:
                    # invalid query
                    logger.debug(exc)
                    errmssg = "Empty or invalid query '{}' for entry {}".format(
                        q, e)
                    raise TableExportError(errmssg)

                if val is not None:
                    self.info[e] = val
                else:
                    self._append_missing(e, d)
            elif FIND_FUNCTION in d:
                find_fun = getattr(self, d[FIND_FUNCTION])
                try:
                    self.info[e] = find_fun()
                except Exception as exc:
                    self._append_missing(e, d)
                    logger.debug(exc)
            # last resort: check if record has e as property:
            else:
                try:
                    self.info[e] = self.record.get_property(e).value
                except AttributeError as exc:
                    # either record is None, or get_property(e) returns None
                    logger.debug(exc)
                    errmssg = "No find function or query were specified for entry "
                    errmssg += e

                    if self.record is not None:
                        errmssg += ", nor does record {} have a property of that name".format(
                            self.record.id)
                    errmssg += "."
                    raise TableExportError(errmssg)

        if self.missing:
            errmssg = "The following mandatory entries are missing:\n"

            for e in self.missing:
                if "error" in self.export_dict[e]:
                    errmssg += e + \
                        ":\t{}\n".format(self.export_dict[e]["error"])
                else:
                    errmssg += e + '\n'

            if self.raise_error_if_missing:
                raise TableExportError(errmssg)
            else:
                logger.error(errmssg)

    def prepare_csv_export(self, delimiter=',', print_header=False,
                           skip_empty_optionals=False):
        """Return the values in self.info as a single-line string, separated
        by the delimiter. If header is true, a header line with the
        names of the entries, separated by the same delimiter is
        added. Header and body are separated by a newline character.

        Parameters
        ----------
        delimiter : string, optional
            symbol that separates two consecutive entries, e.g. ','
            for .csv or '\t' for .tsv. Default is ','.
        print_header : bool, optional
            specify whether a header line with all entry names
            separated by the delimiter precedes the body. Default is
            False.
        skip_empty_optionals : bool, True
            if this is true, optional entries without value will be
            skipped in the output string. Otherwise an empty field
            will be attached. Default is False.

        Raises
        ------
        TableExportError:
            if mandatory entries are missing a value

        Returns
        -------
        string:
            a single string, either only the body line, or header and
            body separated by a newline character if header is True.

        """
        body = ""

        if print_header:
            header = ""

        for e, d in self.export_dict.items():
            if e in self.info:
                body += str(self.info[e]) + delimiter

                if print_header:
                    header += str(e) + delimiter
            else:
                if not ("optional" in d and d["optional"]):
                    raise TableExportError(
                        "Mandatory entry " + e +
                        " has no value that could be exported to .csv.")

                if not skip_empty_optionals:
                    body += delimiter

                    if print_header:
                        header += str(e) + delimiter
        # return and remove final delimiter

        if body.endswith(delimiter):
            body = body[:-len(delimiter)]

        if print_header and header.endswith(delimiter):
            header = header[:-len(delimiter)]

        if print_header:
            return header + '\n' + body

        return body

    def _check_sanity_of_export_dict(self):
        """Check whether all entries of the dictionary with the entries to be
        exported are valid.

        """

        for e, d in self.export_dict.items():
            # values should be exported either by query or by function

            if QUERY in d and FIND_FUNCTION in d:
                raise TableExportError(
                    "For entry " + e +
                    ", both a query and a function are given for finding "
                    "the value to be exported. Please spcify either a"
                    " function or a query, not both."
                )
            # check find function if present

            if FIND_FUNCTION in d:
                if not hasattr(self, d[FIND_FUNCTION]):
                    raise TableExportError(
                        "Find function " + d[FIND_FUNCTION] +
                        " was specified for entry " + e +
                        " but no such function could be found."
                    )
                elif not callable(getattr(self, d[FIND_FUNCTION])):
                    raise TableExportError(
                        "Find function " + d[FIND_FUNCTION] +
                        " was given for entry " + e + " but is not callable."
                    )

            elif QUERY in d:
                # query but no record is given

                if self.record is None:
                    raise TableExportError(
                        "A query for entry " + e +
                        " was specified but no record is given."
                    )
                else:
                    if "selector" not in d:
                        d["selector"] = d[QUERY].strip().split(" ")[1]
            # guess find function and insert if existing
            else:
                possible_name = self._guess_find_function(e)

                if hasattr(self, possible_name) and callable(getattr(self, possible_name)):
                    d[FIND_FUNCTION] = possible_name

    def _append_missing(self, e, d):
        """append e to missing if e is mandatory"""

        if not ("optional" in d and d["optional"]):
            self.missing.append(e)

    def _guess_find_function(self, e):
        """guess find function name as 'find_' + e"""

        return "find_{}".format(e)
