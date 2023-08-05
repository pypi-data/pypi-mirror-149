#!/usr/bin/env python3
#
# This file is a part of the CaosDB Project.
#
# Copyright (c) 2020 IndiScale GmbH
# Copyright (c) 2020 Daniel Hornung <d.hornung@indiscale.com>
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

""" Imports data from labfolder via api """

import json
import os
import time

import html2text

import caosdb as db
from labfolder.connection import configure_connection  # pylint: disable=import-error


class Importer(object):
    def __init__(self):
        self.connection = configure_connection()
        self.projects = self.connection.retrieve_projects()
        self.entries = self.connection.retrieve_entries()

    def create_project(self, project):
        dbproject = db.Record(name=project['title'])
        dbproject.add_parent(name="Project")
        dbproject.add_property(name="projectId", value=project['id'])
        # crawler.cached_find_identifiables([dbproject])

        return dbproject

    def get_entries(self, project_id):
        return [ent for ent in self.entries if ent["project_id"] == project_id]

    def treat_project(self, project):
        cont = db.Container()
        dbproject = self.create_project(project)
        cont.append(dbproject)

        for entry in self.get_entries(project["id"]):
            recs = self.create_entry(entry, dbproject)
            cont.extend(recs)

        print(cont)
        cont.insert(unique=False)
        # import IPython
        # IPython.embed()

    def import_data(self):
        for project in self.projects:
            self.treat_project(project)

    def add_property_from_data_element(self, dbrecord, element):

        if element['type'] == "DATA_ELEMENT_GROUP":
            for c in element["children"]:
                self.add_property_from_data_element(dbrecord, c)
        elif element['type'] == "SINGLE_DATA_ELEMENT":

            # if quant is not None:
            # quant = quant.strip(": ")
            # title = title+" - "+quant
            res = db.execute_query("FIND PROPERTY '{}'".format(element['title']))

            if len(res) == 0:
                p = db.Property(name=element['title'], unit=element['unit'], datatype=db.DOUBLE)
                try:
                    p.insert()
                except db.exceptions.TransactionError as e:
                    print(e)

                    return
            val = element['value']
            try:
                val = float(val)
            except (ValueError, TypeError):
                print("Value is no float!!!", val)

                return
            dbrecord.add_property(name=element['title'], value=val, unit=element['unit'])
        elif element['type'] == "DESCRIPTIVE_DATA_ELEMENT":
            res = db.execute_query("FIND PROPERTY '{}'".format(element['title']))

            if len(res) == 0:
                p = db.Property(name=element['title'], datatype=db.TEXT)
                p.insert()
            dbrecord.add_property(name=element['title'],
                                  value=element['description'])

    def create_element(self, element_id, el_type, dbrecord):
        print(element_id, el_type)

        if el_type == "IMAGE":
            el_type = "FILE"
        elif el_type == "DATA_ELEMENT":
            el_type = "DATA"

        try:
            element = self.connection.retrieve_element(element_id, el_type=el_type)
        except BaseException:
            print("Could not retrieve: ", element_id)

            return

        if el_type == "TEXT":
            dbrecord.add_property(
                name="textElement",
                value=html2text.html2text(element["content"]))
        elif el_type == "FILE":
            local_file = self.connection.download_file(element_id)
            f = db.File(name=element["file_name"],
                        path=os.path.join("labfolder", str(time.time()),
                                          element["file_name"]),
                        file=local_file)
            f.insert(unique=False)
            dbrecord.add_property(name="associatedFile", value=f)

        elif el_type == "DATA":
            for subel in element["data_elements"]:
                self.add_property_from_data_element(dbrecord=dbrecord,
                                                    element=subel)
        elif el_type == "TABLE":
            print(element)

    def create_entry(self, entry, dbproject):
        cont = db.Container()
        dbrecord = db.Record(name=entry["title"])
        dbrecord.add_parent(name="LabbookEntry")
        dbrecord.add_property(name="Project", value=dbproject)
        dbrecord.add_property(name="entryId", value=entry['id'])
        # crawler.cached_find_identifiables([dbrecord])

        # TODO resolve id
        # person = get_author_from_entry(entry)
        # dbrecord.add_property(name="responsible", value=person)

        for element in entry["elements"]:

            print(json.dumps(element, sort_keys=True, indent=4))
            self.create_element(element["id"], element["type"], dbrecord)
            # If all text field would have the class dd_text_entry the
            # following would be sufficient:
            # if 'dd_text_entry' in block['class']:
            # instead we check whether an editor field exists.

        cont.extend([dbrecord])

        return cont
