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
This file allows to create an xml representation of a complete dataset.
Using the given entity all related entities are collected and saved in a way
that the data can be imported in another CaosDB instance.

Files that are smaller than 1MB are saved in a downloads folder and can be
imported along with the entities themselves.
"""
import argparse
import os

import caosdb as db
from caosdb.apiutils import apply_to_ids, retrieve_entities_with_ids
from caosdb.common.datatype import get_id_of_datatype, is_reference
from lxml import etree


def get_ids_of_related_entities(entity):
    """ returns a list of ids of entities that related to the given one.

    Related means in this context, that it is kind of necessary for the
    representation of this entity: ids of properties and parents as well as the
    ids of referenced entities.
    """
    entities = []

    if isinstance(entity, int):
        entity = db.Entity(id=entity).retrieve()

    for par in entity.parents:
        entities.append(par.id)

    for prop in entity.properties:
        entities.append(prop.id)
        isref = is_reference(prop.datatype)

        if isref:
            if isinstance(prop.value, list) and len(prop.value) > 0:
                entities.extend([int(el) for el in prop.value])
            elif prop.value is not None:
                entities.append(int(prop.value))

            if prop.datatype not in [db.FILE, db.REFERENCE, db.LIST(db.FILE),
                                     db.LIST(db.REFERENCE)]:
                entities.append(get_id_of_datatype(prop.datatype))

    return entities


def recursively_collect_related(entity):
    """ collects all related entities.
    Starting from a single entity the related entities are retrieved (see
    get_ids_of_related_entities) and then the related entities of those are
    retrieved and so forth.
    This is usefull to create a collection of kind of related dataset
    """
    all_entities = db.Container()
    all_entities.append(entity)
    ids = set()
    new_ids = set([entity.id])

    while new_ids:
        ids.update(new_ids)

        for eid in list(new_ids):
            new_ids.update(get_ids_of_related_entities(eid))
        new_ids = new_ids - ids

    return retrieve_entities_with_ids(list(ids))


def invert_ids(entities):
    apply_to_ids(entities, lambda x: x*-1)


def export_related_to(rec_id, directory="."):
    if not isinstance(rec_id, int):
        raise ValueError("rec_id needs to be an integer")
    ent = db.execute_query("FIND {}".format(rec_id), unique=True)
    cont = recursively_collect_related(ent)
    export(cont, directory=directory)


def export(cont, directory="."):
    directory = os.path.abspath(directory)
    dl_dir = os.path.join(directory, "downloads")

    if not os.path.exists(dl_dir):
        os.makedirs(dl_dir)

    for el in cont:
        if isinstance(el, db.File) and el.size < 1e6:
            target = os.path.join(dl_dir, el.path[1:])
            os.makedirs(os.path.dirname(target), exist_ok=True)
            try:
                el.download(target)
                print("Downloaded:", target)
            except BaseException:
                print("Failed download of:", target)

    invert_ids(cont)

    for el in cont:
        el.version = None
    xml = etree.tounicode(cont.to_xml(
        local_serialization=True), pretty_print=True)

    with open(os.path.join(directory, "caosdb_data.xml"), "w") as fi:
        fi.write(xml)


def defineParser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '-i',
        '--id',
        type=int,
        required=True,
        help='the id of the record that shall be copied and then changed')
    parser.add_argument(
        '-d',
        '--directory',
        default=".",
        help='the directory where the xml file and the downloads are saved')

    return parser


if __name__ == "__main__":
    parser = defineParser()
    args = parser.parse_args()

    export_related_to(args.id, directory=args.directory)
