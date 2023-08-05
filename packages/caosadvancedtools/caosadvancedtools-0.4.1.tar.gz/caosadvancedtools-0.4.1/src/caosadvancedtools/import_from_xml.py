#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2020 IndiScale GmbH, Henrik tom Wörden
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
"""
This file allows to import a dataset stored in a xml representation and
corresponding files.

The export should have been done with export_related.py
"""
import argparse
import os
from tempfile import NamedTemporaryFile

import caosdb as db
from caosdb.apiutils import apply_to_ids
from caosadvancedtools.models.data_model import DataModel


def create_dummy_file(text="Please ask the administrator for this file."):
    tmpfile = NamedTemporaryFile(delete=False)
    tmpfile.close()
    with open(tmpfile.name, "w") as tm:
        tm.write(text)

    return tmpfile.name


def import_xml(filename, rerun=False, interactive=True):
    """
    filename: path to the xml file with the data to be inserted
    rerun: boolean; if true, files are not inserted as paths would conflict.
    """
    cont = db.Container()
    with open(filename) as fi:
        cont = cont.from_xml(fi.read())

    tmpfile = create_dummy_file()
    model = []

    files = {}

    # add files to files list and properties and record types to model

    for el in cont:
        if isinstance(el, db.File):
            el._checksum = None
            target = os.path.join("downloads", el.path[1:])

            if os.path.exists(target):
                el.file = target
            else:
                el.file = tmpfile
            files[el.path] = el

        if (isinstance(el, db.Property) or isinstance(el, db.RecordType)):
            model.append(el)

    # remove entities of the model from the container

    for el in model+list(files.values()):
        cont.remove(el)

    id_mapping = {}

    for el in model+list(files.values()):
        id_mapping[el.id] = el

    # insert/update the model
    datamodel = DataModel()
    datamodel.extend(model)
    datamodel.sync_data_model(noquestion=not interactive)

    # insert files

    if not rerun:
        for _, el in enumerate(files.values()):
            r = el.insert(unique=False)
    else:
        for _, el in enumerate(files.values()):
            el.id = None
            el.retrieve()

    def replace_by_new(old):
        if old in id_mapping:
            return id_mapping[old].id
        else:
            return old

    # set the ids of already inserted entities in the container
    apply_to_ids(cont, replace_by_new)

    cont.insert(unique=False)


def defineParser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", help='file to be imported')
    parser.add_argument("--rerun", help='if this script is run at least a'
                        ' second time and files are already inserted',
                        action="store_true")

    return parser


if __name__ == "__main__":
    parser = defineParser()
    args = parser.parse_args()

    import_xml(args.file, args.rerun)
