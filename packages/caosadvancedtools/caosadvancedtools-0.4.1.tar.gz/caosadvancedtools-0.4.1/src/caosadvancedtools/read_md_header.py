#!/usr/bin/env python
# encoding: utf-8
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C)
# A. Schlemmer, 01/2019
# D. Hornung 2019-02
# T. Fitschen 2019-02
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

from . import pandoc_header_tools


def get_header(fn):
    return pandoc_header_tools.get_header(fn)[2]

# import os
# import re

# import caosdb as db
# import yaml

# from .cfood import AbstractCFood, get_entity
# from .utils import string_to_person

# TODO: I have an improved version of this tool in filesystemspecification.

# def _clean_header(header):
#     # Fill empty fields with empty string

#     for k, v in header.items():
#         if v == "null":
#             header[k] = ""

#         if v is None:
#             header[k] = ""

#     for k, v in header.items():
#         # Plain string is put into list

#         if type(v) == str:
#             header[k] = [v]

#     return header


# class NoValidHeader(Exception):
#     pass


# def get_header(filename):
#     """Open an md file identified by filename and read out the yaml
# header.

# filename can also be a folder. In this case folder/readme.md will be used for
# getting the header.

# If a header is found a tuple is returned: (first yaml header line index, last+1
# yaml header line index, header)

# Otherwise, if `add_header` is True, a header is added and the function is called
# again.

# The header is normalized in the following way:

# - If the value to a key is a string, a list with that string as only element is
#   returned.

# From https://pandoc.org/MANUAL.html:

# A YAML metadata block is a valid YAML object, delimited by a line of three
# hyphens (---) at the top and a line of three hyphens (---) or three dots (...)
# at the bottom. A YAML metadata block may occur anywhere in the document, but if
# it is not at the beginning, it must be preceded by a blank line.

#     """

#     if os.path.isdir(filename):
#         filename = os.path.join(filename, "readme.md")

#     with open(filename) as f:
#         textlines = f.readlines()

#     state = 0
#     found_0 = -1
#     found_1 = -1
#     found_2 = -1

#     for i, line in enumerate(textlines):
#         if len(line) == 1 and state in {-1, 0}:
#             found_0 = i
#             state = 0

#             continue

#         if line.rstrip() == "---" and state == 0:
#             found_1 = i+1
#             state = 1

#             continue

#         if line.rstrip() == "..." and state == 1:
#             found_2 = i
#             state = 2

#             break
#         # Else: reset state to -1, unless it is 1 (in this case, leave it
#         # untouched

#         if state == 1:
#             pass
#         else:
#             state = -1

#     # If a header section was found:

#     if state == 2:
#         headerlines = []

#         for l in textlines[found_1:found_2]:
#             l = l.replace("\t", "  ")
#             l = l.rstrip()
#             headerlines.append(l)
#         try:
#             yaml_part = yaml.load("\n".join(headerlines))
#         except yaml.error.MarkedYAMLError as e:
#             # print("Error in file {}:".format(filename))
#             # print(headerlines)
#             raise NoValidHeader(filename)

#         return _clean_header(yaml_part)

#     raise NoValidHeader(filename)
