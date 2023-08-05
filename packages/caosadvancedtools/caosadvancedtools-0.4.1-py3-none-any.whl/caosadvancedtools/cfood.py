#!/usr/bin/env python
# encoding: utf-8
#
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2018 Research Group Biomedical Physics,
# Max-Planck-Institute for Dynamics and Self-Organization Göttingen
# Copyright (C) 2019-2022 IndiScale GmbH <info@indiscale.com>
# Copyright (C) 2019,2020 Henrik tom Wörden
# Copyright (C) 2020-2022 Florian Spreckelsen <f.spreckelsen@indiscale.com>
# Copyright (C) 2021 University Medical Center Göttingen, Institute for Medical Informatics
# Copyright (C) 2021 Florian Spreckelsen <florian.spreckelsen@med.uni-goettingen.de>
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
""" Defines how something that shall be inserted into CaosDB is treated.

CaosDB can automatically be filled with Records based on some structure, a file
structure, a table or similar.
The Crawler will iterate over the respective items and test for each item
whether a CFood class exists that matches the file path, i.e. whether CFood
class wants to treat that pariticular item. If one does, it is instanciated to
treat the match. This occurs in basically three steps:
1. Create a list of identifiables, i.e. unique representation of CaosDB Records
(such as an experiment belonging to a project and a date/time).
2. The identifiables are either found in CaosDB or they are created.
3. The identifiables are update based on the date in the file structure.
"""

import logging
import re
import warnings
from abc import ABCMeta, abstractmethod
from datetime import datetime

import caosdb as db
from caosdb.common.models import Entity
from caosdb.exceptions import (BadQueryError, EmptyUniqueQueryError,
                               QueryNotUniqueError, TransactionError)

from .datamodel_problems import DataModelProblems
from .guard import global_guard as guard

ENTITIES = {}
PROPERTIES = {}
RECORDS = {}
RECORDTYPES = {}
FILES = {}

logger = logging.getLogger(__name__)


def get_entity(name):
    """ Returns the entity with a given name, preferably from a local cache.

    If the local cache does not contain the entity, retrieve it from CaosDB.
    """

    if name not in ENTITIES:
        ent = db.Entity(name=name)
        ent.retrieve()
        ENTITIES[name] = ent

    return ENTITIES[name]


def get_property(name):
    """Returns the property with a given name, preferably from a local
    cache.

    If the local cache does not contain the record type, try to
    retrieve it from CaosDB. If it does not exist, see whether it
    could be a record type used as a property.

    """

    if name not in PROPERTIES:
        try:
            prop = db.execute_query("FIND Property with name='{}'".format(
                name),
                unique=True)
        except (EmptyUniqueQueryError, QueryNotUniqueError):
            # Property might actually be a RecordTypes
            prop = get_recordtype(name)
        PROPERTIES[name] = prop

    return PROPERTIES[name]


def get_record(name):
    """Returns the record with a given name, preferably from a local cache.

    If the local cache does not contain the record, try to retrieve it
    from CaosDB.

    """

    if name not in RECORDS:
        rec = db.execute_query("FIND Record with name='{}'".format(name),
                               unique=True)
        RECORDS[name] = rec

    return RECORDS[name]


def get_recordtype(name):
    """Returns the record type with a given name, preferably from a local
    cache.

    If the local cache does not contain the record type, try to
    retrieve it from CaosDB. If it does not exist, add it to the data
    model problems

    """

    if name not in RECORDTYPES:
        try:
            rec = db.execute_query("FIND RecordType WITH name='{}'".format(name),
                                   unique=True)
        except (EmptyUniqueQueryError, QueryNotUniqueError) as e:
            DataModelProblems.add(name)
            raise e
        RECORDTYPES[name] = rec

    return RECORDTYPES[name]


class FileGuide(object):
    def access(self, path):
        """ should be replaced by a function that adds
        a prefix to paths to allow to access caosdb files locally

        This default just returns the unchanged path.
        """

        return path


fileguide = FileGuide()


class AbstractCFood(object, metaclass=ABCMeta):
    """ Abstract base class for Crawler food (CFood)."""

    def __init__(self, item):
        """A CFood has two main methods which must be customized:

    1. `create_identifiables`
        This method defines (and inserts if necessary) the identifiables which may be updated at a
        later stage.  After calling this method, the `identifiables` Container contains those
        Records which will be updated at a later time.

    2. `update_identifiables`
        This method updates the stored identifiables as necessary.
        """
        self.to_be_updated = db.Container()
        self.identifiables = db.Container()
        self.item = item
        self.attached_items = []
        self.update_flags = {}

    @abstractmethod
    def create_identifiables(self):
        """
        should set the instance variable Container with the identifiables
        """

    @abstractmethod
    def update_identifiables(self):
        """ Changes the identifiables as needed and adds changed identifiables
        to self.to_be_updated
        """

    @classmethod
    def match_item(cls, item):
        """ Matches an item found by the crawler against this class. Returns
        True if the item shall be treated by this class, i.e. if this class
        matches the item.

        Parameters
        ----------
        item : object
               iterated by the crawler

        To be overwritten by subclasses!
        """

        return True

    def collect_information(self):
        """ The CFood collects information for further processing.

        Often CFoods need information from files or even from the database in
        order to make processing decision. It is intended that this function is
        called after match. Thus match can be used without connecting to the
        database.

        To be overwritten by subclasses
        """
        pass

    def attach(self, item):
        self.attached_items.append(item)

    # TODO looking for should `attach` the files itsself. This would allow to
    # group them right away and makes it unnecessary to check matches later
    # again.
    def looking_for(self, item):
        """
        returns True if item can be added to this CFood.

        Typically a CFood exists for a file and defines how to deal with the
        file. However, sometimes additional files "belong" to a CFood. E.g. an
        experiment CFood might match against a README file but labnotes.txt
        also shall be treated by the cfood (and not a special cfood created for
        labnotes.txt)
        This function can be used to define what files shall be 'attached'.

        To be overwritten by subclasses
        """

        return False

    @staticmethod
    # move to api?
    def set_parents(entity, names):
        entity.parents.clear()

        for n in names:
            entity.add_parent(get_entity(n))

    @staticmethod
    # move to api?
    def remove_property(entity, prop):
        # TODO only do something when it is necessary?

        if isinstance(prop, db.Entity):
            name = prop.name
        else:
            name = prop

        while entity.get_property(name) is not None:
            entity.remove_property(name)

    @staticmethod
    # move to api?
    def set_property(entity, prop, value, datatype=None):
        AbstractCFood.remove_property(entity, prop)

        if datatype is not None:
            entity.add_property(prop, value, datatype=datatype)
        else:
            entity.add_property(prop, value)


def add_files(filemap):
    """add to the file cache"""
    FILES.update(filemap)


def get_entity_for_path(path):
    if path in FILES:
        return FILES[path]
    try:
        q = "FIND FILE WHICH IS STORED AT '{}'".format(path)
        logger.debug(q)
        FILES[path] = db.execute_query(q, unique=True)

        return FILES[path]
    except BadQueryError:
        path_prefix = "**"

        if not path.startswith("/"):
            path_prefix = path_prefix + "/"
        q = "FIND FILE WHICH IS STORED AT '{}{}'".format(path_prefix, path)
        logger.debug(q)

        FILES[path] = db.execute_query(q, unique=True)

        return FILES[path]


class AbstractFileCFood(AbstractCFood):
    # contains the compiled regular expression after the first execution of the
    # function match()
    _pattern = None

    def __init__(self, crawled_path, *args, **kwargs):
        """ Abstract base class for file based Crawler food (CFood).

        Parameters
        ----------
        crawled_path : The file that the crawler is currently matching. Its
                       path should match against the pattern of this class

        """
        super().__init__(*args, item=crawled_path, **kwargs)
        self._crawled_file = None
        self.crawled_path = crawled_path
        self.match = re.match(self.get_re(), crawled_path)
        self.attached_filenames = []

    @property
    def crawled_file(self):
        if self._crawled_file is None:
            self._crawled_file = get_entity_for_path(self.crawled_path)

        return self._crawled_file

    @staticmethod
    def re_from_extensions(extensions):
        """Return a regular expression which matches the given file extensions.

        Useful for inheriting classes.

        Parameters
        ----------
        extensions : iterable<str>
            An iterable with the allowed extensions.

        Returns
        -------
        out : str
            The regular expression, starting with ``.*\\.`` and ending with the EOL dollar
            character.  The actual extension will be accessible in the
            :py:attribute:`pattern group name<python:re.Pattern.groupindexe>` ``ext``.
        """

        if not extensions:
            return None

        return r".*\.(?P<ext>" + "|".join(extensions) + ")$"

    @classmethod
    def get_re(cls):
        """ Returns the regular expression used to identify files that shall be
        processed

        This function shall be implemented by subclasses.
        """
        raise NotImplementedError()

    @classmethod
    def match_item(cls, path):
        """ Matches the regular expression of this class against file names

        Parameters
        ----------
        path : str
                 The path of the file that shall be matched.
        """

        return re.match(cls.get_re(), path) is not None

    # TODO looking for should `attach` the files itsself. This would allow to
    # group them right away and makes it unnecessary to check matches later
    # again.
    def looking_for(self, crawled_file):
        """
        returns True if crawled_file can be added to this CFood.

        Typically a CFood exists for a file and defines how to deal with the
        file. However, sometimes additional files "belong" to a CFood. E.g. an
        experiment CFood might match against a README file but labnotes.txt
        also shall be treated by the cfood (and not a special cfood created for
        labnotes.txt)
        This function can be used to define what files shall be 'attached'.
        """

        # TODO rename to filenames_to_be_attached

        if crawled_file in self.attached_filenames:
            return True

        return False


def assure_object_is_in_list(obj, containing_object, property_name,
                             to_be_updated=None, datatype=None):
    """Checks whether `obj` is one of the values in the list property
    `property_name` of the supplied entity `containing_object`.

    If this is the case this function returns. Otherwise the entity is
    added to the property `property_name` and the entity
    `containing_object` is added to the supplied list to_be_updated in
    order to indicate, that the entity `containing_object` should be
    updated. If none is submitted the update will be conducted
    in-place.

    If the property is missing, it is added first and then the entity
    is added/updated.

    If obj is a list, every element is added

    """

    if datatype is None:
        datatype = db.LIST(property_name)

    if containing_object.get_property(property_name) is None:
        containing_object.add_property(property_name, value=[],
                                       datatype=datatype)
    # TODO: case where multiple times the same property exists is not treated

    list_prop = containing_object.get_property(property_name)
    if list_prop.value is None:
        list_prop.value = []
    elif not isinstance(list_prop.value, list):
        list_prop.value = [list_prop.value]
        list_prop.datatype = datatype
    current_list = list_prop.value

    if not isinstance(obj, list):
        objects = [obj]
    else:
        objects = obj

    # use ids if values are entities

    if all([isinstance(el, db.Entity) for el in objects]):
        objects = [el.id for el in objects]

    update = False

    for o in objects:
        contained = False

        for el in current_list:
            if el == o:
                contained = True

                break

        if contained:
            logger.debug("{} is in {} of entity {}".format(
                o, property_name, containing_object.id))

        else:
            logger.debug("UPDATE: Appending {} to {} of entity {}".format(
                o, property_name, containing_object.id))
            current_list.append(o)
            update = True

    if update:
        if to_be_updated is not None:
            to_be_updated.append(containing_object)
        else:
            get_ids_for_entities_with_names([containing_object])

            guard.safe_update(containing_object)


def assure_special_is(entity, value, kind, to_be_updated=None, force=False):
    """
    Checks whether `entity` has the name or description that is passed.

    If this is the case this function ends. Otherwise the entity is assigned
    a new name. The list to_be_updated is supplied, the entity is added to
    the list in order to indicate, that the entity `entity` should be updated.
    Otherwise it is directly updated
    """

    if kind not in ["name", "description"]:
        raise RuntimeError("Function cannot be used to set {}".format(kind))

    if entity.__getattribute__(kind) == value:
        return

    logger.debug("UPDATE: set {} of entity {}".format(kind, entity.id))
    entity.__setattr__(kind,  value)

    if to_be_updated is None:
        if force:
            entity.update(unique=False)
        else:
            guard.safe_update(entity, unique=False)
    else:
        to_be_updated.append(entity)


def assure_name_is(entity, name, to_be_updated=None, force=False):
    """
    Checks whether `entity` has the name that is passed.

    If this is the case this function ends. Otherwise the entity is assigned
    a new name. The list to_be_updated is supplied, the entity is added to
    the list in order to indicate, that the entity `entity` should be updated.
    Otherwise it is directly updated
    """

    assure_special_is(entity, name, "name", to_be_updated=to_be_updated,
                      force=force)


# TOOD rename to is
# switch arugments and check for old sequence
def assure_has_description(entity, description, to_be_updated=None,
                           force=False):
    """
    Checks whether `entity` has the description that is passed.

    If this is the case this function ends. Otherwise the entity is assigned
    a new description. The list to_be_updated is supplied, the entity is added to
    the list in order to indicate, that the entity `entity` should be updated.
    Otherwise it is directly updated
    """

    assure_special_is(entity, description, "description",
                      to_be_updated=to_be_updated, force=force)


def assure_has_parent(entity, parent, to_be_updated=None,
                      force=False, unique=True):
    """
    Checks whether `entity` has a parent with name `parent`.

    If this is the case this function ends. Otherwise the entity is assigned
    a new parent. The list to_be_updated is supplied, the entity is added to
    the list in order to indicate, that the entity `entity` should be updated.
    Otherwise it is directly updated
    """
    parents = entity.get_parents()
    contained = False

    for el in parents:
        if el.name.lower() == parent.lower():
            contained = True

            break

    if contained:
        logger.debug("entity {} has parent {}".format(entity.id, parent))

        return

    logger.debug("UPDATE: Adding  parent {} to entity {}".format(parent,
                                                                 entity.id))
    entity.add_parent(parent)

    if to_be_updated is None:
        get_ids_for_entities_with_names([entity])

        if force:
            entity.update(unique=unique)
        else:
            guard.safe_update(entity, unique=unique)
    else:
        to_be_updated.append(entity)


def assure_parents_are(entity, parents, to_be_updated=None,
                       force=False, unique=True):
    """
    Checks whether `entity` has the provided parents (and only those).

    If this is the case this function ends. Otherwise the entity is assigned
    the new parents and the old ones are discarded.

    Note that parent matching occurs based on names.

    If the list to_be_updated is supplied, the entity is added to
    the list in order to indicate, that the entity `entity` should be updated.
    Otherwise it is directly updated

    parents: single string or list of strings
    """

    if not isinstance(parents, list):
        parents = [parents]

    for i, e in enumerate(parents):
        if isinstance(e, db.Entity):
            if e.name is None:
                raise Exception("Entity should have name")
        else:
            parents[i] = db.Entity(name=e)

    if ([p.name.lower() for p in entity.get_parents()]
            == [p.name.lower() for p in parents]):

        logger.debug("entity {} has parents {}".format(entity.id, parents))

        return

    logger.debug("UPDATE: Adding  parent {} to entity {}".format(parents,
                                                                 entity.id))

    while len(entity.parents) > 0:
        entity.parents.pop()

    for parent in parents:
        entity.add_parent(parent)

    if to_be_updated is None:
        get_ids_for_entities_with_names([entity])

        if force:
            entity.update(unique=unique)
        else:
            guard.safe_update(entity, unique=unique)
    else:
        to_be_updated.append(entity)


def assure_has_property(entity, name, value, to_be_updated=None,
                        datatype=None, setproperty=False):
    """Checks whether `entity` has a property `name` with the value
    `value`.

    If this is the case this function ends. Otherwise the entity is
    assigned a new parent.

    Note that property matching occurs based on names.

    If the list to_be_updated is supplied, the entity is added to the
    list in order to indicate, that the entity `entity` should be
    updated. Otherwise it is directly updated

    setproperty: boolean, if True, overwrite existing properties.

    """

    if name.lower() == "description":
        warnings.warn("Do not use assure_has_property with 'description'. "
                      "Use assure_has_description.", DeprecationWarning)

        if entity.description == value:
            return
        else:
            logger.debug("UPDATE: Adding  description with value {} to "
                         "entity {}".format(value, entity.id))
            entity.description = value

            if to_be_updated is None:
                get_ids_for_entities_with_names([entity])

                guard.safe_update(entity, unique=False)

            else:
                to_be_updated.append(entity)

            return

    properties = entity.get_properties()
    possible_properties = [prop for prop in properties if prop.name.lower() ==
                           name.lower()]
    contained = False

    if setproperty and len(possible_properties) > 1:
        raise ValueError("Trying to set the property value of {} but more"
                         " than one such properties exist.".format(name))

    if isinstance(value, db.Entity):
        value = value.id

    if isinstance(value, list):
        value = [i.id if isinstance(i, db.Entity) else i for i in value]

    for el in possible_properties:
        tmp_value = el.value

        if isinstance(tmp_value, db.Entity):
            tmp_value = el.value.id

        if isinstance(tmp_value, list):
            tmp_value = [i.id if isinstance(
                i, db.Entity) else i for i in tmp_value]

        if tmp_value == value:
            contained = True

            break

        # cover special case of datetimes that are returned as strings
        # by pylib.

        if isinstance(value, datetime):

            try:
                compare_time = datetime.fromisoformat(el.value)
            except ValueError:
                # special case of wrong iso format
                # time zone
                tmp = el.value.split("+")

                if len(tmp) == 2:
                    tz_str = '+' + tmp[1][:2] + ':' + tmp[1][2:]
                else:
                    tz_str = ""
                tmp = tmp[0]
                # milli- and micrseconds
                tmp = tmp.split(".")

                if len(tmp) == 2:
                    if len(tmp[1]) < 6:
                        ms = '.' + tmp[1] + '0'*(6-len(tmp[1]))
                    else:
                        raise ValueError(
                            "invalid millisecond format in {}".format(el.value))
                else:
                    ms = ""
                tmp = tmp[0] + ms + tz_str
                compare_time = datetime.fromisoformat(tmp)

            if compare_time == value:
                contained = True

                break

    if contained:
        logger.debug("entity {} has property  {} with value {}".format(
            entity.id, name, value))

        return

    logger.debug(
        "UPDATE: Adding  property {} with value {} to entity {}".format(
            name, value, entity.id))

    if setproperty and possible_properties:
        entity.properties.remove(possible_properties[0])

    if datatype is None:
        entity.add_property(name=name, value=value)
    else:
        entity.add_property(name=name, value=value, datatype=datatype)

    if to_be_updated is None:
        get_ids_for_entities_with_names([entity])

        guard.safe_update(entity, unique=False)
    else:
        to_be_updated.append(entity)


def assure_property_is(entity, name, value, datatype=None, to_be_updated=None,
                       force=False):
    """
    Checks whether `entity` has a Property `name` with the given value.

    If this is the case this function ends. Otherwise the entity is assigned
    a new property or an existing one is updated.

    If the list to_be_updated is supplied, the entity is added to
    the list in order to indicate, that the entity `entity` should be updated.
    Otherwise it is directly updated
    """

    assure_has_property(entity, name, value, to_be_updated=to_be_updated,
                        datatype=datatype, setproperty=True)


def insert_id_based_on_name(entity):
    if entity.name is not None and (entity.id is None or entity.id < 0):
        if isinstance(entity, db.Property):
            entity.id = get_property(entity.name).id
        elif isinstance(entity, db.Record):
            entity.id = get_record(entity.name).id
        elif isinstance(entity, db.RecordType):
            entity.id = get_recordtype(entity.name).id
        else:
            # In case the type of the entity isn't specified
            entity.id = get_entity(entity.name).id


def get_ids_for_entities_with_names(entities):
    # TODO how to deal with name conflicts?

    for ent in entities:
        insert_id_based_on_name(ent)

        for prop in ent.get_properties():
            insert_id_based_on_name(prop)

        for parent in ent.get_parents():
            insert_id_based_on_name(parent)
            insert_id_based_on_name(ent)


class RowCFood(AbstractCFood):
    def __init__(self, item, unique_cols, recordtype, **kwargs):
        """
        table : pandas table
        """
        super().__init__(item, **kwargs)
        self.unique_cols = unique_cols
        self.recordtype = recordtype

    def create_identifiables(self):
        rec = db.Record()
        rec.add_parent(self.recordtype)

        for col in self.unique_cols:
            rec.add_property(col, self.item.loc[col])
        self.identifiables.append(rec)

    def update_identifiables(self):
        rec = self.identifiables[0]

        for key, value in self.item.iteritems():
            if key in self.unique_cols:
                continue
            assure_property_is(rec, key,
                               value,
                               to_be_updated=self.to_be_updated)


class CMeal():
    """
    CMeal groups equivalent items and allow their collected insertion.

    Sometimes there is no one item that can be used to trigger the creation of
    some Record. E.g. if a collection of image files shall be referenced from one
    Record that groups them, it is unclear which image should trigger the
    creation of the Record.

    CMeals are grouped based on the groups in the used regular expression. If,
    in the above example, all the images reside in one folder, all groups of
    the filename match except that for the file name should match.
    The groups that shall match
    need to be listed in the matching_groups class property. Subclasses will
    overwrite this property.

    This allows to use has_suitable_cfood in the match_item function of a CFood
    to check whether the necessary CFood was already created.
    In order to allow this all instances of a
    CFood class are tracked in the existing_instances class member.

    Subclasses must have a cls.get_re function and a match member variable
    (see AbstractFileCFood)
    """
    existing_instances = []
    matching_groups = []

    def __init__(self):
        self.item = None
        # FIXME is this only necessary, because of inconsistent use of super().__init__()?
        if "match" not in self.__dict__:
            self.match = None
        self.__class__.existing_instances.append(self)

    @staticmethod
    def get_re():
        raise NotImplementedError("Subclasses must implement this function.")

    @classmethod
    def all_groups_equal(cls, m1, m2):
        equal = True

        if m2 is None:
            return False

        for group in cls.matching_groups:
            if (group not in m1.groupdict() or
                    group not in m2.groupdict() or
                    m1.group(group) != m2.group(group)):
                equal = False

        return equal

    @classmethod
    def has_suitable_cfood(cls, item):
        """ checks whether the required cfood object already exists.

        item : the crawled item
        """
        match = re.match(cls.get_re(), item)

        for cfood in cls.existing_instances:
            if cls.all_groups_equal(match, cfood.match):
                return True

        return False

    def belongs_to_meal(self, item):
        # This is already the main item

        if item == self.item:
            return False
        match = re.match(self.get_re(), item)

        if match is None:
            return False

        return self.all_groups_equal(match, self.match)
