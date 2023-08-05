#!/usr/bin/env python3

# This file is a part of the CaosDB Project.
#
# Copyright (C) 2020,2021 IndiScale GmbH <www.indiscale.com>
# Copyright (C) 2020 Daniel Hornung <d.hornung@indiscale.com>
# Copyright (C) 2021 Henrik tom Wörden <h.tomwoerden@indiscale.com>
# Copyright (C) 2021 Alexander Kreft
# Copyright (C) 2021 Laboratory for Fluid Physics and Biocomplexity,
# Max-Planck-Insitute für Dynamik und Selbstorganisation <www.lfpn.ds.mpg.de>
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

"""A CFood for hdf5 files


This module allows to parse hdf5 files and reproduce their structure in form
of Records that reference each other.

hdf5 files are composed of groups and datasets. Both of which can have
attributes. Groups and datasets are mapped to Records and attributes to
Properties.
"""

import re
from copy import deepcopy

import caosdb as db
import h5py
import numpy as np
from caosadvancedtools.cfood import fileguide
from caosdb.common.datatype import is_reference
from caosdb.common.utils import uuid

from ..cfood import (AbstractFileCFood, assure_has_description,
                     assure_has_parent, assure_has_property,
                     assure_property_is)
from ..structure_mapping import (EntityMapping, collect_existing_structure,
                                 update_structure)


def h5_attr_to_property(val):
    """ returns the value and datatype of a CaosDB Property for the given value


    1d arrays are converted to lists
    If no suitable Property can be created (None, None) is returned.

    2d and higher dimensionality arrays are being ignored.
    """

    if isinstance(val, str):
        return val, db.TEXT
    elif isinstance(val, complex):
        return val, db.TEXT
    else:
        if not hasattr(val, 'dtype'):
            raise NotImplementedError("Code assumes only str are missing the"
                                      "dtype attribute")

        if issubclass(val.dtype.type, np.floating):
            dtype = db.DOUBLE
        elif issubclass(val.dtype.type, np.integer):
            dtype = db.INTEGER
        elif val.dtype.kind in ['S', 'U']:
            dtype = db.TEXT
            val = val.astype(str)
        elif val.dtype.kind == 'O':
            if not np.all([isinstance(el, str) for el in val]):
                raise NotImplementedError("Cannot convert arbitrary objects")
            dtype = db.TEXT
            val = val.astype(str)
        else:
            raise NotImplementedError("Unknown dtype used")

        if isinstance(val, np.ndarray):
            if val.ndim > 1:
                return None, None
        # The tolist method is on both numpy.ndarray and numpy.generic
        # and properly converts scalars (including 0-dimensional
        # numpy.ndarray) to Python scalars and 1D arrays to lists of
        # Python scalars.
        if val.ndim != 0:
            dtype = db.LIST(dtype)
        val = val.tolist()

        # TODO this can eventually be removed

        if(hasattr(val, 'ndim')):
            if not isinstance(val, np.ndarray) and val.ndim != 0:
                print(val, val.ndim)
                raise Exception(
                    "Implementation assumes that only np.arrays have ndim.")

        return val, dtype


class H5CFood(AbstractFileCFood):
    """ H5CFood which consumes a HDF5 file.

    The structure is mapped onto an equivalent structure of interconnected
    Records.

    Attributes
    ----------
    h5file : h5py.File, default None
        Name of the hdf5-file to read
    """

    # to be overwritten by subclasses

    def __init__(self, *args, **kwargs):
        """CFood which consumes HDF5 files."""
        super().__init__(*args, **kwargs)
        self.h5file = None
        self.identifiable_root = None
        self.root_name = "root"
        self.hdf5Container = db.Container()
        self.em = EntityMapping()

    def collect_information(self):
        self.h5file = h5py.File(fileguide.access(self.crawled_path), 'r')

    @staticmethod
    def get_re():
        """Return a regular expression string to match *.h5, *.nc, *.hdf, *.hdf5."""
        extensions = [
            "h5",
            "nc",
            "hdf",
            "hdf5",
        ]

        return AbstractFileCFood.re_from_extensions(extensions)

    def create_identifiables(self):
        """Create identifiables out of groups in the HDF5 file.

        This method will call is_identifiable(h5path, h5object) and create_identifiable(h5path,
        h5object) on each HDF5 object to decide and actually create the identifiables.
        """
        # manually create the identifiable root element: self.identifiable_root
        self.structure = self.create_structure(self.h5file,
                                               special_treatment=self.special_treatment,
                                               root_name=self.root_name)

    def update_identifiables(self):
        """Check if the identifiables need to be updated.

        In that case also add the updated entities to the list of updateables.

        This method will iterate over the groups and datasets governed by this CFood's identifiables
        and call ``update_object(path, h5object)`` on each object.

        """

        self.structure._cuid = "root element"
        self.em.add(self.structure, self.identifiable_root)
        collect_existing_structure(self.structure, self.identifiable_root,
                                   self.em)
        self.to_be_inserted = db.Container()
        self.insert_missing_structure(self.structure)

        # TODO this is a workaround due to the fact that the caosdb library
        # changes the objects in the Container if it is inserted. The graph
        # structure is flattened. I.e. references to other entity objects are
        # replaced with their IDs. However this code depends on this graph.
        tmp_copy = deepcopy(self.to_be_inserted)
        tmp_copy.insert()

        for e1, e2 in zip(tmp_copy, self.to_be_inserted):
            e2.id = e1.id
        # End workaround

        # self.update_structure(self.structure)
        update_structure(self.em, self.to_be_updated, self.structure)

    def special_treatment(self, key, value, dtype):
        """define special treatment of attributes

        to be overwritten by child classes.

        key: attribute name
        value: attribute value
        """

        return key, value, dtype

    @classmethod
    def create_structure(cls, h5obj, create_recordTypes=False, collection=None,
                         special_treatment=None, root_name="root"):
        """Create Records and Record types from a given hdf5-object for all
        items in the tree. Attributes are added as properties, the
        values only if the dimension < 2.

        Parameters
        ----------
        h5obj : h5py.File
                a hdf5-file object

        root_name : name that is used instead of '/'
                    Type of the root Record (the Record corresponding to
                    the root node in the HDF5 file)

        Returns
        -------
        rec : db.Container
            Contains the Record Types, Records and Properties for the
            input-tree

        """

        if collection is None:
            collection = []

        if special_treatment is None:
            def special_treatment(x, y, z): return x, y, z

        if h5obj.name == "/":
            name_without_path = root_name
        else:
            name_without_path = h5obj.name.split("/")[-1]

        if create_recordTypes:
            rec = db.RecordType(name=name_without_path)
        else:
            rec = db.Record().add_parent(name=name_without_path)
        collection.append(rec)

        if isinstance(h5obj, h5py.Group):
            for subgroup in h5obj.keys():
                subgroup_name = h5obj[subgroup].name.split("/")[-1]

                sub = H5CFood.create_structure(h5obj[subgroup],
                                               create_recordTypes=create_recordTypes,
                                               collection=collection,
                                               special_treatment=special_treatment)

                if create_recordTypes:
                    rec.add_property(subgroup_name)
                else:
                    rec.add_property(subgroup_name, value=sub)

        for key, val in h5obj.attrs.items():
            # ignored

            if key in ["REFERENCE_LIST", "DIMENSION_LIST", "NAME", "CLASS"]:
                continue

            val, dtype = h5_attr_to_property(val)

            if val is None and dtype is None:
                continue

            if create_recordTypes and key.lower() not in ['description']:
                treated_k, _, treated_dtype = special_treatment(
                    key, val, dtype)

                if treated_k is not None:
                    prop = db.Property(name=treated_k, datatype=treated_dtype)
                    collection.append(prop)
                    rec.add_property(name=treated_k)
            else:
                treated_k, treated_v, treated_dtype = special_treatment(
                    key, val, dtype)

                if treated_k is not None:
                    rec.add_property(name=treated_k, value=treated_v,
                                     datatype=treated_dtype)

        return rec

    def insert_missing_structure(self, target_structure: db.Record):
        if target_structure._cuid not in self.em.to_existing:
            self.to_be_inserted.append(target_structure)

        for prop in target_structure.get_properties():
            if prop.is_reference(server_retrieval=True):
                self.insert_missing_structure(prop.value)
