#!/usr/bin/env python
# encoding: utf-8
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2020 Indiscale GmbH <info@indiscale.com>
# Copyright (C) 2020 Henrik tom Wörden <h.tomwoerden@indiscale.com>
# Copyright (C) 2020 Florian Spreckelsen <f.spreckelsen@indiscale.com>
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

# TODO this is implementing a cache on client side. Should it be on
# server side?
import os
import sqlite3
from hashlib import sha256

import caosdb as db
from lxml import etree

import tempfile


def put_in_container(stuff):
    if isinstance(stuff, list):
        stuff = db.Container().extend(stuff)

    if not isinstance(stuff, db.Container):
        stuff = db.Container().append(stuff)

    return stuff


def cleanXML(xml):
    # remove transaction benchmark
    props = xml.findall('TransactionBenchmark')

    for prop in props:
        parent = prop.find("..")
        parent.remove(prop)

    return xml


def get_pretty_xml(cont):
    cont = put_in_container(cont)
    xml = cont.to_xml(local_serialization=True)
    cleanXML(xml)

    return etree.tounicode(xml, pretty_print=True)


class Cache(object):
    """
    stores identifiables (as a hash of xml) and their respective ID.

    This allows to retrieve the Record corresponding to an indentifiable
    without querying.
    """

    def __init__(self, db_file=None):
        if db_file is None:
            self.db_file = "cache.db"
        else:
            self.db_file = db_file

        if not os.path.exists(self.db_file):
            self.create_cache()

    def create_cache(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute(
            '''CREATE TABLE identifiables (digest text primary key, caosdb_id integer)''')
        conn.commit()
        conn.close()

    @staticmethod
    def hash_entity(ent):
        xml = get_pretty_xml(ent)
        digest = sha256(xml.encode("utf-8")).hexdigest()

        return digest

    def insert(self, ent_hash, ent_id):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute('''INSERT INTO identifiables VALUES (?, ?)''',
                  (ent_hash, ent_id))
        conn.commit()
        conn.close()

    def check_existing(self, ent_hash):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute('''Select  * FROM identifiables WHERE digest=?''',
                  (ent_hash,))
        res = c.fetchone()
        conn.commit()
        conn.close()

        if res is None:
            return res
        else:
            return res[1]

    def update_ids_from_cache(self, entities):
        """ sets ids of those entities that are in cache

        A list of hashes corresponding to the entities is returned
        """
        hashes = []

        for ent in entities:
            ehash = Cache.hash_entity(ent)
            hashes.append(ehash)
            eid = self.check_existing(ehash)

            if eid is not None:
                ent.id = eid

        return hashes

    def insert_list(self, hashes, entities):
        """ Insert the ids of entities into the cache

        The hashes must correspond to the entities in the list
        """

        for ehash, ent in zip(hashes, entities):
            if self.check_existing(ehash) is None:
                self.insert(ehash, ent.id)


class UpdateCache(Cache):
    """
    stores unauthorized updates

    If the Guard is set to a mode that does not allow an update, the update can
    be stored in this cache such that it can be authorized and done later.
    """

    def __init__(self, db_file=None):
        if db_file is None:
            tmppath = tempfile.gettempdir()
            tmpf = os.path.join(tmppath, "crawler_update_cache.db")
            db_file = tmpf
        super().__init__(db_file=db_file)

    @staticmethod
    def get_previous_version(cont):
        """ Retrieve the current, unchanged version of the entities that shall
        be updated, i.e. the version before the update """

        old_ones = db.Container()

        for ent in cont:
            old_ones.append(db.execute_query("FIND {}".format(ent.id),
                                             unique=True))

        return old_ones

    def insert(self, cont, run_id):
        """Insert a pending, unauthorized update


        Parameters
        ----------
        cont: Container with the records to be updated containing the desired
              version, i.e. the state after the update.

        run_id: int
                The id of the crawler run
        """
        cont = put_in_container(cont)
        old_ones = UpdateCache.get_previous_version(cont)
        new_ones = cont

        old_hash = Cache.hash_entity(old_ones)
        new_hash = Cache.hash_entity(new_ones)
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute('''INSERT INTO updates VALUES (?, ?, ?, ?, ?)''',
                  (old_hash, new_hash, str(old_ones), str(new_ones),
                   str(run_id)))
        conn.commit()
        conn.close()

    def create_cache(self):
        """ initialize the cache """
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute('''CREATE TABLE updates (olddigest text, newdigest text,
                  oldrep text, newrep  text, run_id text,
                  primary key (olddigest, newdigest, run_id))''')
        conn.commit()
        conn.close()

    def get_updates(self, run_id):
        """ returns the pending updates for a given run id

        Parameters:
        -----------
        run_id: the id of the crawler run
        """

        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute('''Select * FROM updates WHERE run_id=?''',
                  (str(run_id),))
        res = c.fetchall()
        conn.commit()
        conn.close()

        return res
