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

""" Imports labfolder exports """

import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import warnings
from io import BytesIO, StringIO

import requests
import yaml
from bs4 import BeautifulSoup

import caosdb as db

RERUN = False
# crawler = Crawler()

print("""
WARNING: This is an ALPHA version. Parsing of the by labfolder exported data
might not work correctly! There might be missing elements! Check the result
carefully before inserting it.
""")


def create_project(project):
    dbproject = db.Record(name=project.attrs['data-name'])
    dbproject.add_parent(name="Project")
    dbproject.add_property(name="projectId", value=project.attrs['data-id'])
    # crawler.cached_find_identifiables([dbproject])

    return dbproject


def get_author_from_entry(entry):
    person = db.Record()
    person.add_parent(name="Person")
    resp = entry.find_all(attrs={'class': 'author_name'})

    for name in ["firstname", "lastname"]:
        person.add_property(
            name=name,
            value=resp[0].find_all(attrs={'class': 'author_'+name})[0].getText())
    # crawler.cached_find_identifiables([person])

    return person


def val_or_none(stuff):
    if len(stuff) == 0:
        return None
    else:
        return stuff[0].getText()


def add_property_from_data_element(dbrecord, element):
    unit = val_or_none(element.find_all(attrs={'class': 'element-unit'}))
    title = val_or_none(element.find_all(attrs={'class': 'element-title'}))
    quant = val_or_none(element.find_all(attrs={'class': 'element-quantity'}))
    val = val_or_none(element.find_all(attrs={'class': 'element-value'}))

    print("tit", title)
    print("qu", quant)
    if quant is not None:
        quant = quant.strip(": ")
        title = title+" - "+quant
    res = db.execute_query("FIND PROPERTY '{}'".format(title))
    if len(res) == 0:
        p = db.Property(name=title, unit=unit, datatype=db.DOUBLE)
        p.insert()
    try:
        val = float(val)
    except TypeError:
        print("Value is no float!!!", val)
        return
    dbrecord.add_property(name=title, value=val, unit=unit)


def create_file(name, filename, root):
    local_path = os.path.join(root, filename)
    local_path = os.path.normpath(local_path)
    if not os.path.exists(local_path):
        raise ValueError("FILE DOES NOT EXIST: ", local_path)
    f = db.File(path=local_path, file=local_path, name=name)
    return f


def create_entry(entry, dbproject, root):
    cont = db.Container()
    dbrecord = db.Record()
    dbrecord.add_parent(name="LabbookEntry")
    dbrecord.add_property(name="Project", value=dbproject)
    dbrecord.add_property(name="entryId", value=entry.attrs['data-id'])
    # crawler.cached_find_identifiables([dbrecord])

    person = get_author_from_entry(entry)
    dbrecord.add_property(name="responsible", value=person)

    for block in entry.find_all(attrs={'class': 'dd_entry_cell'}):
        # If all text field would have the class dd_text_entry the
        # following would be sufficient:
        # if 'dd_text_entry' in block['class']:
        # instead we check whether an editor field exists.
        editor = block.find_all(attrs={'class': 'redactor_editor'})

        if len(editor) > 0:
            dbrecord.add_property(name="textElement", value=editor[0].getText())

            continue

        download = block.find_all(
            attrs={'class': 'dd_entry_cell_file_download'})

        if len(download) > 0:
            name = ((download[0].parent).attrs['data-filename']).strip('"')
            if name == "blank.png":
                continue
            if len(download[0].find_all("img")) > 0:
                filename = download[0].find_all("img")[0].attrs['src']
            elif len(download[0].find_all("a")) > 0:
                filename = download[0].find_all("a")[0].attrs['href']
            else:
                raise ValueError("could not get filename")
            print(name)
            print(filename)
            f = create_file(name, filename, root)
            if RERUN:
                f.retrieve()
            else:
                f.insert()
            dbrecord.add_property(name="associatedFile", value=f)
            cont.append(f)

            continue

        elements = block.find_all(
            attrs={'class': 'data-element-display'})

        if len(elements) > 0:
            for el in elements:
                add_property_from_data_element(dbrecord=dbrecord, element=el)

            continue

        tables = block.find_all(
            attrs={'class': 'table-el-container'})

        if len(tables) > 0:
            name = (tables[0]).find_all(
                        attrs={'class': 'table-el-filename'}
                    )[0].getText().strip()
            f = create_file(name, name, root)
            if RERUN:
                f.retrieve()
            else:
                f.insert()
            dbrecord.add_property(name="table", value=f)
            cont.append(f)

            continue

        empty = block.find_all(
            attrs={'class': 'dd_entry_empty_element'})

        if len(tables) > 0:
            print("\n\nempty")

            continue

    cont.extend([dbrecord, person])

    return cont


def treat_project(path):
    with open(os.path.join(path, "index.html")) as fp:
        tree = BeautifulSoup(fp, features="lxml")

    cont = db.Container()
    project = tree.find_all(id="eln_project_content")

    if len(project) == 0:
        return
    else:
        project = project[0]
    dbproject = create_project(project)
    cont.append(dbproject)

    for entry in project.find_all(lambda x: x.has_attr('data-id')):
        recs = create_entry(entry, dbproject, path)
        cont.extend(recs)

    print(cont)
    cont.insert()
    # import IPython
    # IPython.embed()


def import_data(folder):
    """imports the data of a labfolder export"""

    if not os.path.exists(folder):
        raise ValueError("folder does not exist")

    projects_folder = os.path.join(folder, "projects")

    if not os.path.exists(projects_folder):
        raise ValueError("folder does not contain a projects folder")

    for root, dirs, files in os.walk(projects_folder):
        print(root, dirs, files)

        if "index.html" in files:
            treat_project(root)
