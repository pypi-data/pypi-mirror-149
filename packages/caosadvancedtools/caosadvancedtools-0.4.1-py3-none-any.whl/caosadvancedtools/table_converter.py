#!/usr/bin/env python
# encoding: utf-8
#
# ** header v3.0
# This file is a part of the CaosDB Project.
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
#
# ** end header
import argparse
import re
import sys

import caosdb as db
import pandas as pd


def from_tsv(filename, recordtype):
    """ parses a tsv file to a list of records """
    df = pd.read_csv(filename, sep="\t")

    return from_table(df, recordtype)


def to_tsv(filename, container):
    df = to_table(container)
    df.to_csv(filename, sep="\t", index=False)


def generate_property_name(prop):
    if prop.unit is None:
        return prop.name
    else:
        return "{} [{}]".format(prop.name, prop.unit)


def to_table(container):
    """ creates a table from the records in a container """

    if len(container) == 0:
        raise ValueError("Container is empty")
    properties = set()

    for rec in container:
        properties.update([generate_property_name(p)
                           for p in container[0].get_properties()])
    df = pd.DataFrame(columns=list(properties))
    rts = set([p.name for p in container[0].parents])

    for ii, rec in enumerate(container):
        if set([p.name for p in rec.parents]) != rts:
            raise ValueError("Parents differ")

        for p in rec.get_properties():

            df.loc[ii, generate_property_name(p)] = p.value

    return df


def from_table(spreadsheet, recordtype):
    """ parses a pandas DataFrame to a list of records """
    records = db.Container()

    for idx, row in spreadsheet.iterrows():
        rec = db.Record()
        rec.add_parent(name=recordtype)

        for key, value in row.iteritems():
            if key.lower() == "description":
                rec.description = value
                continue

            if (pd.notnull(value) and
                    (not isinstance(value, str) or value.strip() != "")):
                regexp = r"(.*)\[(.*)\].*"
                match = re.match(regexp, key)

                if match is not None:
                    pname = match.group(1).strip()
                    unit = match.group(2).strip()
                    rec.add_property(name=pname, value=value, unit=unit)
                else:
                    rec.add_property(name=key, value=value)
        records.append(rec)

    return records


if __name__ == "__main__":

    p = argparse.ArgumentParser()
    p.add_argument("-f", "--filename", help="The excel filename")
    p.add_argument("--auth-token")
    arg = p.parse_args(sys.argv[1:])

    db.configure_connection(auth_token=arg.auth_token)

    recordtype = "Experiment"

    from_tsv(arg.filename, recordtype)
