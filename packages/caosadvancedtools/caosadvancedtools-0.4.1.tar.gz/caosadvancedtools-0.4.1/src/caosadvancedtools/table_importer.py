#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (C) 2020 Henrik tom Wörden
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

"""
This module allows to read table files like tsv and xls. They are converted to
a Pandas DataFrame and checked whether they comply with the rules provided.
For example, a list of column names that have to exist can be provided.

This module also implements some converters that can be applied to cell
entries.

Those converters can also be used to apply checks on the entries.
"""

import logging
import pathlib
from datetime import datetime

import caosdb as db
import numpy as np
import pandas as pd
from xlrd import XLRDError

from caosadvancedtools.utils import check_win_path

from .datainconsistency import DataInconsistencyError
from .suppressKnown import SuppressKnown

logger = logging.getLogger(__name__)


def assure_name_format(name):
    """
    checks whether a string can be interpreted as 'LastName, FirstName'
    """
    name = str(name)

    if len(name.split(",")) != 2:
        raise ValueError("The field value should be 'LastName, FirstName'. "
                         "The supplied value was '{}'.".format(name))

    return name


def check_reference_field(ent_id, recordtype):
    if 1 != db.execute_query("COUNT {} WITH id={}".format(
            recordtype,
            ent_id),
            unique=True):
        raise ValueError(
            "No {} with the supplied id={} exists. \n"
            "Please supply a valid ID.".format(
                recordtype,
                ent_id
            ))

    return ent_id


def yes_no_converter(val):
    """
    converts a string to True or False if possible.

    Allowed filed values are yes and no.
    """

    if str(val).lower() == "yes":
        return True
    elif str(val).lower() == "no":
        return False
    else:
        raise ValueError(
            "Field should be 'Yes' or 'No', but is '{}'.".format(val))


def datetime_converter(val, fmt="%Y-%m-%d %H:%M:%S"):
    """ if the value is already a datetime, it is returned otherwise it
    converts it using format string
    """

    if isinstance(val, datetime):
        return val
    else:
        return datetime.strptime(val, fmt)


def date_converter(val, fmt="%Y-%m-%d"):
    """ if the value is already a datetime, it is returned otherwise it
    converts it using format string
    """

    if val is None:
        return None
    else:
        return datetime_converter(val, fmt=fmt).date()


def incomplete_date_converter(val, fmts={"%Y-%m-%d": "%Y-%m-%d",
                                         "%Y-%m": "%Y-%m", "%Y": "%Y"}):
    """ if the value is already a datetime, it is returned otherwise it
    converts it using format string

    Parameters
    ----------
    val : str
        Candidate value for one of the possible date formats.
    fmts : dict, optional
        Dictionary containing the possible (incomplete) date formats:
        keys are the formats into which the input value is tried to be
        converted, values are the possible input formats.
    """

    for to, fro in fmts.items():
        try:
            date = datetime.strptime(val, fro)

            return date.strftime(to)

        except ValueError:
            pass
    raise RuntimeError(
        "Value {} could not be converted with any format string".format(
            val))


def win_path_list_converter(val):
    """
    checks whether the value looks like a list of windows paths and converts
    it to posix paths
    """

    if pd.isnull(val):
        return []
    paths = val.split(",")

    return [win_path_converter(p) for p in paths]


def win_path_converter(val):
    """
    checks whether the value looks like a windows path and converts it to posix
    """

    if val == "":
        return val

    if not check_win_path(val):
        raise ValueError(
            "Field should be a Windows path, but is\n'{}'.".format(val))
    path = pathlib.PureWindowsPath(val)

    return path.as_posix()


def string_in_list(val, options, ignore_case=True):
    """Return the given value if it is contained in options, raise an
    error otherwise.

    Parameters
    ----------
    val : str
        String value to be checked.
    options : list<str>
        List of possible values that val may obtain
    ignore_case : bool, optional
        Specify whether the comparison of val and the possible options
        should ignor capitalization. Default is True.

    Returns
    -------
    val : str
       The original value if it is contained in options

    Raises
    ------
    ValueError
       If val is not contained in options.
    """

    if ignore_case:
        val = val.lower()
        options = [o.lower() for o in options]

    if val not in options:
        raise ValueError(
            "Field value is '{}', but it should be one of the following "
            "values:  {}.".format(val, ", ".join(
                ["'{}'".format(o) for o in options])))

    return val


class TableImporter():
    """Abstract base class for importing data from tables.
    """

    def __init__(self, converters, obligatory_columns=None, unique_keys=None,
                 datatypes=None):
        """
        Parameters
        ----------
        converters : dict
          Dict with column names as keys and converter functions as values. This dict also defines
          what columns are required to exist throught the existing keys. The converter functions are
          applied to the cell values. They should also check for ValueErrors, such that a separate
          value check is not necessary.

        obligatory_columns : list, optional
          List of column names, each listed column must not have missing values.

        unique_keys : list, optional
          List of column names that in combination must be unique: each row has a unique
          combination of values in those columns.

        datatypes : dict, optional
          Dict with column names as keys and datatypes as values.  All non-null values will be
          checked whether they have the provided datatype.  This dict also defines what columns are
          required to exist throught the existing keys.

        """

        if converters is None:
            converters = {}

        if datatypes is None:
            datatypes = {}

        self.sup = SuppressKnown()
        self.required_columns = list(converters.keys())+list(datatypes.keys())
        self.obligatory_columns = ([]
                                   if obligatory_columns is None
                                   else obligatory_columns)
        self.unique_keys = [] if unique_keys is None else unique_keys
        self.converters = converters
        self.datatypes = datatypes

    def read_file(self, filename, **kwargs):
        raise NotImplementedError()

    def check_columns(self, df, filename=None):
        """Check whether all required columns exist.

        Required columns are columns for which converters are defined.

        Raises
        ------
        DataInconsistencyError

        """

        for col in self.required_columns:
            if col not in df.columns:
                errmsg = "Column '{}' missing in ".format(col)
                errmsg += ("\n{}.\n".format(filename) if filename
                           else "the file.")
                errmsg += "Stopping to treat this file..."
                logger.warning(
                    errmsg,
                    extra={'identifier': str(filename),
                           'category': "inconsistency"})
                raise DataInconsistencyError(errmsg)

    def check_unique(self, df, filename=None):
        """Check whether value combinations that shall be unique for each row are unique.

        If a second row is found, that uses the same combination of values as a
        previous one, the second one is removed.

        """
        df = df.copy()
        uniques = []

        for unique_columns in self.unique_keys:
            subtable = df[list(unique_columns)]

            for index, row in subtable.iterrows():
                element = tuple(row)

                if element in uniques:
                    errmsg = (
                        "The {}. row contains the values '{}'.\nThis value "
                        "combination should be unique, but was used in a previous "
                        "row in\n").format(index+1, element)
                    errmsg += "{}.".format(filename) if filename else "the file."
                    errmsg += "\nThis row will be ignored!"

                    logger.warning(errmsg, extra={'identifier': filename,
                                                  'category': "inconsistency"})
                    df = df.drop(index)
                else:
                    uniques.append(element)

        return df

    def check_datatype(self, df, filename=None, strict=False):
        """Check for each column whether non-null fields have the correct datatype.

        .. note::

          If columns are integer, but should be float, this method converts the respective columns
          in place.

        Parameters
        ----------

        strict: boolean, optional
          If False (the default), try to convert columns, otherwise raise an error.

        """
        for key, datatype in self.datatypes.items():
            # Check for castable numeric types first: We unconditionally cast int to the default
            # float, because CaosDB does not have different sizes anyway.
            col_dtype = df.dtypes[key]
            if not strict and not np.issubdtype(col_dtype, datatype):
                issub = np.issubdtype
                #  These special cases should be fine.
                if issub(col_dtype, np.integer) and issub(datatype, np.floating):
                    df[key] = df[key].astype(datatype)

            # Now check each element
            for idx, val in df.loc[
                    pd.notnull(df.loc[:, key]), key].iteritems():

                if not isinstance(val, datatype):
                    msg = (
                        "In row no. {rn} and column '{c}' of file '{fi}' the "
                        "datatype was {was} but it should be "
                        "{expected}".format(rn=idx, c=key, fi=filename,
                                            was=str(type(val)).strip("<>"),
                                            expected=str(datatype).strip("<>"))
                    )
                    logger.warning(msg, extra={'identifier': filename,
                                               'category': "inconsistency"})
                    raise DataInconsistencyError(msg)

    def check_missing(self, df, filename=None):
        """
        Check in each row whether obligatory fields are empty or null.

        Rows that have missing values are removed.

        Returns
        -------
        out : pandas.DataFrame
          The input DataFrame with incomplete rows removed.
        """
        df = df.copy()

        for index, row in df.iterrows():
            # if none of the relevant information is given, skip

            if np.array([pd.isnull(row.loc[key]) for key in
                         self.obligatory_columns]).all():

                df = df.drop(index)

                continue

            # if any of the relevant information is missing, report it

            i = 0
            okay = True

            while okay and i < len(self.obligatory_columns):
                key = self.obligatory_columns[i]
                i += 1

                if pd.isnull(row.loc[key]):
                    errmsg = (
                        "Required information is missing ({}) in {}. row"
                        " (without header) of "
                        "file:\n{}".format(key, index+1, filename))

                    logger.warning(errmsg, extra={'identifier': filename,
                                                  'category': "inconsistency"})
                    df = df.drop(index)

                    okay = False

        return df

    def check_dataframe(self, df, filename=None, strict=False):
        """Check if the dataframe conforms to the restrictions.

        Checked restrictions are: Columns, data types, uniqueness requirements.

        Parameters
        ----------

        df: pandas.DataFrame
          The dataframe to be checked.

        filename: string, optional
          The file name, only used for output in case of problems.

        strict: boolean, optional
          If False (the default), try to convert columns, otherwise raise an error.
        """
        self.check_columns(df, filename=filename)
        df = self.check_missing(df, filename=filename)
        self.check_datatype(df, filename=filename, strict=strict)

        if len(self.unique_keys) > 0:
            df = self.check_unique(df, filename=filename)

        return df


class XLSImporter(TableImporter):
    def read_file(self, filename, **kwargs):
        return self.read_xls(filename=filename, **kwargs)

    def read_xls(self, filename, **kwargs):
        """Convert an xls file into a Pandas DataFrame.

        The converters of the XLSImporter object are used.

        Raises: DataInconsistencyError
        """
        try:
            xls_file = pd.io.excel.ExcelFile(filename)
        except (XLRDError, ValueError) as e:
            logger.warning(
                "Cannot read \n{}.\nError:{}".format(filename,
                                                     str(e)),
                extra={'identifier': str(filename),
                       'category': "inconsistency"})
            raise DataInconsistencyError(*e.args)

        if len(xls_file.sheet_names) > 1:
            # Multiple sheets is the default now. Only show in debug
            logger.debug(
                "Excel file {} contains multiple sheets. "
                "All but the first are being ignored.".format(filename))

        try:
            df = xls_file.parse(converters=self.converters, **kwargs)
        except Exception as e:
            logger.warning(
                "Cannot parse {}.\n{}".format(filename, e),
                extra={'identifier': str(filename),
                       'category': "inconsistency"})
            raise DataInconsistencyError(*e.args)

        df = self.check_dataframe(df, filename)

        return df


class CSVImporter(TableImporter):
    def read_file(self, filename, sep=",", **kwargs):
        try:
            df = pd.read_csv(filename, sep=sep, converters=self.converters,
                             **kwargs)
        except ValueError as ve:
            logger.warning(
                "Cannot parse {}.\n{}".format(filename, ve),
                extra={'identifier': str(filename),
                       'category': "inconsistency"})
            raise DataInconsistencyError(*ve.args)

        df = self.check_dataframe(df, filename)

        return df


class TSVImporter(TableImporter):
    def read_file(self, filename, **kwargs):
        try:
            df = pd.read_csv(filename, sep="\t", converters=self.converters,
                             **kwargs)
        except ValueError as ve:
            logger.warning(
                "Cannot parse {}.\n{}".format(filename, ve),
                extra={'identifier': str(filename),
                       'category': "inconsistency"})
            raise DataInconsistencyError(*ve.args)

        df = self.check_dataframe(df, filename)

        return df
