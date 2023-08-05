# encoding: utf-8
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2018 Research Group Biomedical Physics,
# Max-Planck-Institute for Dynamics and Self-Organization Göttingen
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
#
from copy import deepcopy
# TODO(fspreck) for backwards compatibility with Python < 3.9 but this is
# actually
# [deprecated](https://docs.python.org/3/library/typing.html#typing.List), so
# remove this, when we drop support for old Python versions.
from typing import List

import caosdb as db
from caosdb.apiutils import compare_entities, describe_diff


CAOSDB_INTERNAL_PROPERTIES = [
    "description",
    "name",
    "unit",
]


class DataModel(dict):
    """Provides tools for managing a data model.

    When constructing a data model the CaosDB representation can easily be
    created using the classes RecordType and Propery, storing them in a
    Container and inserting it in CaoSDB. However, this has one drawback: You
    cannot simply change someting and update the container. The container will
    insist on having valid ids for all contained Entities.

    This class allows you to define your model as easily but also provides you
    with a method (`sync_data_model`) that will sync with the data model in an
    existing CaosDB instance.

    This is possible because entities, defined in this model, are identified
    with entities in CaosDB using names. I.e. a RecordType "Experiment" in this
    model will update an existing RecordType with name "Experiment" in CaosDB.
    Thus, be carefull not to change existing Entities that were created for a
    different purpose (e.g. someone else's experiment).

    DataModel inherits from dict. The keys are always the names of the
    entities. Thus you cannot have unnamed entities in your model.

    Example:

    # Create a DataModel with a RecordType and a Property, not assuming any
    # relation between the two.
    dm = DataModel([db.RecordType(name="myRecordType"),
                    db.Property(name="myProperty")])
    # Sync the DataModel with the server, so that the server state is consistent
    # with this DataModel's content.
    dm.sync_data_model()
    # Now the DataModel's IDs are the same as on the server.
    """

    def __init__(self, *args):
        if len(args) == 1 and hasattr(args[0], '__iter__'):
            super().__init__([(e.name, e) for e in args[0]])
        else:
            super().__init__(args)

    def append(self, entity: db.Entity):
        self[entity.name] = entity

    def extend(self, entities: List[db.Entity]):
        for entity in entities:
            self.append(entity)

    def sync_data_model(self, noquestion: bool = False, verbose: bool = True):
        """Synchronize this DataModel with a CaosDB instance.

        Updates existing entities from the CaosDB instance and inserts
        non-existing entities into the instance.  Note: This allows to easily
        overwrite changes that were made to an existing data model. Use this
        function with care and double check its effect.

        Raises
        ------
        TransactionError
            If one of the involved transactions fails.

        """
        all_entities = self.collect_entities()
        tmp_exist = self.get_existing_entities(all_entities)
        non_existing_entities = db.Container().extend(
            DataModel.entities_without(
                self.values(), [e.name.lower() for e in tmp_exist]))
        existing_entities = db.Container().extend(
            DataModel.entities_without(
                self.values(), [e.name.lower() for e in non_existing_entities]))
        self.sync_ids_by_name(tmp_exist)

        if len(non_existing_entities) > 0:
            if verbose:
                print("New entities:")

                for ent in non_existing_entities:
                    print(ent.name)

            if noquestion or str(input("Do you really want to insert those "
                                       "entities? [y/N] ")).lower() == "y":
                non_existing_entities.insert()
                self.sync_ids_by_name(non_existing_entities)
                if verbose:
                    print("Updated entities.")
            else:
                return
        else:
            if verbose:
                print("No new entities.")

        if len(existing_entities) > 0:
            if verbose:
                print("Inspecting changes that will be made...")
            any_change = False

            for ent in existing_entities:
                if ent.name in CAOSDB_INTERNAL_PROPERTIES:
                    # Workaround for the usage of internal properties like name
                    # in via the extern keyword:
                    ref = db.Property(name=ent.name).retrieve()
                else:
                    query = db.Query(f"FIND * with id={ent.id}")
                    ref = query.execute(unique=True)
                diff = (describe_diff(*compare_entities(ent, ref
                                                        ), name=ent.name))

                if diff != "":
                    if verbose:
                        print(diff)
                    any_change = True

            if any_change:
                if noquestion or input("Do you really want to apply the above "
                                       "changes? [y/N]") == "y":
                    existing_entities.update()
                    if verbose:
                        print("Synchronized existing entities.")
            else:
                if verbose:
                    print("No differences found. No update")
        else:
            if verbose:
                print("No existing entities updated.")

    @staticmethod
    def get_existing_entities(entities):
        """ Return a list with those entities of the supplied iterable that
        exist in the CaosDB instance.

        Args
        ----
        entities : iterable
            The entities to be retrieved.  This object will not be moidified.

        Raises
        ------
        TransactionError
            If the retrieval fails.
        """
        container = db.Container().extend(deepcopy(entities))
        valid_entities = [e for e in container.retrieve(
            sync=False, raise_exception_on_error=False) if e.is_valid()]

        return valid_entities

    @staticmethod
    def entities_without(entities, names):
        """ Return a new list with all entities which do *not* have
        certain names.

        Parameters
        ----------
        entities : iterable
            A iterable with entities.
        names : iterable of str
            Only entities which do *not* have one of these names will end up in
            the returned iterable.

        Returns
        -------
        list
            A list with entities.
        """
        newc = []

        for e in entities:
            if e.name.lower() not in names:
                newc.append(e)

        return newc

    def sync_ids_by_name(self, valid_entities):
        """Add IDs from valid_entities to the entities in this DataModel.

        "By name" means that the valid IDs (from the valid_entities) are
        assigned to the entities, their properties in this DataModel by their
        names, also parents are replaced by equally named entities in
        valid_entities.  These changes happen in place to this DataModel!

        Parameters
        ----------
        valid_entities : list of Entity
            A list (e.g. a Container) of valid entities.

        Returns
        -------
        None

        """

        for valid_e in valid_entities:
            for entity in self.values():
                if entity.name.lower() == valid_e.name.lower():
                    entity.id = valid_e.id

                # sync properties

                for prop in entity.get_properties():

                    if prop.name.lower() == valid_e.name.lower():
                        prop.id = valid_e.id

                # sync parents

                for par in entity.get_parents():
                    if par.name.lower() == valid_e.name.lower():
                        par._wrap(valid_e)

    def collect_entities(self):
        """ Collects all entities: explicitly defined RecordTypes and
        Properties and those mentioned as Properties
        """
        all_ents = {}

        for ent in self.values():
            all_ents[ent.name] = ent

            for prop in ent.get_properties():
                all_ents[prop.name] = prop

        return list(all_ents.values())
