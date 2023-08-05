#!/usr/bin/env python3
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
#
# ** end header
#
import argparse
import os

import caosdb as db
from caosdb.apiutils import retrieve_entities_with_ids

from export_related import export


def get_dm():
    rts = set([(r.id, r.name) for r
               in db.execute_query("SELECT name FROM RECORDTYPE")])

    if None in rts:
        rts.remove(None)
    ps = set([(r.id, r.name) for r
              in db.execute_query("SELECT name FROM PROPERTY")])

    if None in ps:
        ps.remove(None)

    return rts, ps


def get_parser():
    p = argparse.ArgumentParser()
    p.add_argument("-s", "--store", help="directory where the datamodel shall "
                   "be stored")
    p.add_argument("-c", "--compare", help="directory where the datamodel that"
                   " shall be compared is stored")
    p.add_argument("-x", "--xml", action="store_true",
                   help="store xml as well")

    return p


def store(directory, xml=False):
    rts, ps = get_dm()

    os.makedirs(directory, exist_ok=True)
    with open(os.path.join(directory, "recordtypes.txt"), "w") as fi:
        fi.write(",".join([el[1] for el in rts]))
    with open(os.path.join(directory, "properties.txt"), "w") as fi:
        fi.write(",".join([el[1] for el in ps]))

    if xml:
        cont = retrieve_entities_with_ids(
            [el[0] for el in rts]+[el[0] for el in ps])

        export(cont, directory)


def load_dm(directory):
    with open(os.path.join(directory, "recordtypes.txt"), "r") as fi:
        text = fi.read()
        rts = [el.strip() for el in text.split(",")]
    with open(os.path.join(directory, "properties.txt"), "r") as fi:
        text = fi.read()
        ps = [el.strip() for el in text.split(",")]

    return rts, ps


def lower(li):
    return [el.lower() for el in li]


def compare(directory):
    rts, ps = get_dm()
    stored_rts, stored_ps = load_dm(directory)

    print("Comparing...")

    for r in rts:
        if r.lower() not in lower(stored_rts):
            print("{} is missing in the stored recordtypes".format(r))

    for p in ps:
        if p.lower() not in lower(stored_ps):
            print("{} is missing in the stored properties".format(p))

    for r in stored_rts:
        if r.lower() not in lower(rts):
            print("{} is missing in the existing recordtypes".format(r))

    for p in stored_ps:
        if p.lower() not in lower(ps):
            print("{} is missing in the existing properties".format(p))


if __name__ == "__main__":
    p = get_parser()
    args = p.parse_args()

    if args.store:
        store(args.store, xml=args.xml)

    if args.compare:
        compare(args.compare)
