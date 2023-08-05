#!/usr/bin/env python3

# This is taken from the file manage_header.py
# in a CaosDB management repository. The file manage_header.py
# is not released yet, but creating a library might be useful.
# A. Schlemmer, 04/2019

# ** header v3.0
# This file is a part of the CaosDB Project.

# Copyright (C) 2018 Research Group Biomedical Physics,
# Max-Planck-Institute for Dynamics and Self-Organization Göttingen

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# ** end header
# Tool to manage yaml header in markdown document
# A. Schlemmer, 01/2019
# D. Hornung 2019-02
# T. Fitschen 2019-02

import argparse
import glob
import os
import re

import yaml


class NoValidHeader(Exception):
    def __init__(self, filename, *args, **kwargs):
        self.filename = filename
        msg = ("Header missing in {}\nFix this with the modify subcommand "
               "using -f option".format(filename))
        super().__init__(msg, *args, **kwargs)


class MetadataFileMissing(Exception):

    def __init__(self, filename, *args, **kwargs):
        self.filename = filename
        msg = "Metadata file README.md missing in " + filename
        super().__init__(msg, *args, **kwargs)


class ParseErrorsInHeader(Exception):
    def __init__(self, filename, reason, *args, **kwargs):
        self.filename = filename
        self.reason = reason
        msg = "Invalid header in {}. Reason: {}".format(filename, reason)
        super().__init__(msg, *args, **kwargs)


TEMPLATEHEADER = """
---
responsible:
description:
...

"""


def get_header(filename, add_header=False):
    """Open an md file identified by filename and read out the yaml
header.

filename can also be a folder. In this case folder/README.md will be used for
getting the header.

If a header is found a tuple is returned: (first yaml header line index, last+1
yaml header line index, header)

Otherwise, if `add_header` is True, a header is added and the function is called
again.

The header is normalized in the following way:

- If the value to a key is a string, a list with that string as only element is
  returned.

From https://pandoc.org/MANUAL.html:

A YAML metadata block is a valid YAML object, delimited by a line of three
hyphens (---) at the top and a line of three hyphens (---) or three dots (...)
at the bottom. A YAML metadata block may occur anywhere in the document, but if
it is not at the beginning, it must be preceded by a blank line.

    """

    if os.path.isdir(filename):
        filename = os.path.join(filename, "README.md")
        if not os.path.exists(filename):
            filename = filename[:-9]
            filename = os.path.join(filename, "readme.md")
            if not os.path.exists(filename):
                raise MetadataFileMissing(filename)

    with open(filename) as f:
        textlines = f.readlines()

    state = 0
    found_0 = -1
    found_1 = -1
    found_2 = -1
    for i, line in enumerate(textlines):
        if len(line) == 1 and state in {-1, 0}:
            found_0 = i
            state = 0
            continue
        if line.rstrip() == "---" and state == 0:
            found_1 = i+1
            state = 1
            continue
        if (line.rstrip() == "..." or line.rstrip() == "---") and state == 1:
            found_2 = i
            state = 2
            break
        # Else: reset state to -1, unless it is 1 (in this case, leave it
        # untouched
        if state == 1:
            pass
        else:
            state = -1

    # If a header section was found:
    if state == 2:
        headerlines = []
        for line in textlines[found_1:found_2]:
            line = line.replace("\t", "  ")
            line = line.rstrip()
            headerlines.append(line)
        # try:
        try:
            yaml_part = yaml.load("\n".join(headerlines), Loader=yaml.BaseLoader)
        except yaml.scanner.ScannerError as e:
            raise ParseErrorsInHeader(filename, e)
        # except yaml.error.MarkedYAMLError as e:
        #     raise NoValidHeader(filename)
        if not isinstance(yaml_part, dict):
            raise NoValidHeader(filename)
        return (found_1, found_2, clean_header(yaml_part))

    if not add_header:
        raise NoValidHeader(filename)
    else:
        print("Adding header in: {fn}".format(fn=filename))
        add_header(filename)
        return get_header(filename)


def save_header(filename, header_data):
    """
    Save a header identified by the tuple header_data to the file
    identified by filename.

    filename can also be a folder. In this case folder/README.md will
    be used for getting the header.
    """

    if os.path.isdir(filename):
        filename = os.path.join(filename, "README.md")

    with open(filename) as f:
        textlines = f.readlines()

    while textlines[header_data[0]] != "...\n":
        del textlines[header_data[0]]

    data = header_data[2]
    data = {key: val if len(val) > 1 else val[0] for key, val in data.items()}
    textlines.insert(header_data[0],
                     yaml.dump(data,
                               default_flow_style=False,
                               allow_unicode=True))

    with open(filename, "w") as f:
        f.writelines(textlines)


def add_header(filename, header_dict=None):
    """
    Add a header to an md file.

    If the file does not exist it will be created.

    If header_dict is a dictionary and not None the header
    will be created based on the keys and values of that dictionary.
    """

    if os.path.isdir(filename):
        filename = os.path.join(filename, "README.md")

    if os.path.exists(filename):
        with open(filename) as f:
            textlines = f.readlines()
    else:
        textlines = ""

    if header_dict is None:
        localheader = TEMPLATEHEADER
    else:
        localheader = "---\n" + yaml.dump(header_dict,
                                          default_flow_style=False,
                                          allow_unicode=True) + "...\n"

    with open(filename, "w") as f:
        f.write(localheader)
        f.writelines(textlines)


def clean_header(header):
    # Fill empty fields with empty string
    for k, v in header.items():
        if v == "null":
            header[k] = ""
        if v is None:
            header[k] = ""

    for k, v in header.items():
        # Plain string is put into list
        if isinstance(v, str):
            header[k] = [v]

    return header


def kw_present(header, kw):
    """
    Check whether keywords are present in the header.
    """
    return kw in header and header[kw] is not None and len(header[kw]) > 0
