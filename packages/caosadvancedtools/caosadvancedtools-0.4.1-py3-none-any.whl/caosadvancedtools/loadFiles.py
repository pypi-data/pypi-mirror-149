#!/usr/bin/env python
# encoding: utf-8
#
# ** header v3.0
# This file is a part of the CaosDB Project.
#
# Copyright (C) 2018 Research Group Biomedical Physics,
# Max-Planck-Institute for Dynamics and Self-Organization Göttingen
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

import argparse
import logging
import math
import sys
from argparse import ArgumentParser

import caosdb as db

logger = logging.getLogger(__name__)
timeout_fallback = 20


def convert_size(size):
    if (size == 0):
        return '0B'
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size, 1000)))
    p = math.pow(1000, i)
    s = round(size / p, 2)

    return '%s %s' % (s, size_name[i])


def loadpath(path, include, exclude, prefix, dryrun, forceAllowSymlinks):

    if dryrun:
        logger.info("Performin a dryrun!")
        files = db.Container().retrieve(
            unique=False,
            raise_exception_on_error=True,
            flags={"InsertFilesInDir": ("-p " + prefix + " " if prefix else "")
                   + ("-e " + exclude + " " if exclude else "")
                   + ("-i " + include + " " if include else "")
                   + ("--force-allow-symlinks " if forceAllowSymlinks else "")
                   + path})
    else:
        # new files (inserting them using the insertFilesInDir feature of
        # the server, which inserts files via symlinks)
        files = db.Container().insert(
            unique=False,
            raise_exception_on_error=True,
            flags={"InsertFilesInDir": ("-p " + prefix + " " if prefix else "")
                   + ("-e " + exclude + " " if exclude else "")
                   + ("-i " + include + " " if include else "")
                   + ("--force-allow-symlinks " if forceAllowSymlinks else "")
                   + path})

    totalsize = 0  # collecting total size of all new files

    for f in files:
        totalsize += f.size

    logger.info("Made in total {} new files with a combined size of {} "
                "accessible.".format(len(files), convert_size(totalsize)))

    return


def main(argv=None):
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    # Setup argument parser
    parser = ArgumentParser()
    parser.add_argument("-i", "--include", dest="include",
                        help="""
only include paths matching this regex pattern.
Note: The provided directory tree is traversed from its root. I.e. a pattern
like "/some/path/*.readme" will lead to no loading when called on "/some" as the
re does not match "/some". If you want to match some file, make sure the parent
directories are matched. E.g. -i "(/some|/some/path|.*readme).
exclude is given preference over include.
                        """,
                        metavar="RE")
    parser.add_argument("-e", "--exclude", dest="exclude",
                        help="exclude paths matching this regex pattern.",
                        metavar="RE")
    parser.add_argument("-p", "--prefix", dest="prefix",
                        help="store files with this prefix into the server's"
                        " file system.")
    parser.add_argument("-d", "--dry-run", dest="dryrun", action="store_true",
                        help="Just simulate the insertion of the files.")
    parser.add_argument('-t', '--timeout', dest="timeout",
                        help="timeout in seconds for the database requests. "
                        "0 means no timeout. [defaults to the global "
                        "setting, else to {timeout_fallback}s: "
                        "%(default)s]".format(
                            timeout_fallback=timeout_fallback),
                        metavar="TIMEOUT",
                        default=db.get_config().get("Connection", "timeout",
                                                    fallback=timeout_fallback))
    parser.add_argument(dest="path",
                        help="path to folder with source file(s) "
                        "[default: %(default)s]", metavar="path")
    parser.add_argument("--force-allow-symlinks", dest="forceAllowSymlinks",
                        help="Force the processing of symlinks. By default, "
                        "the server will ignore symlinks in the inserted "
                        "directory tree.", action="store_true")
    args = parser.parse_args()

    con = db.get_connection()
    con.timeout = float(args.timeout)
    con._login()

    loadpath(
        path=args.path,
        include=args.include,
        exclude=args.exclude,
        prefix=args.prefix,
        dryrun=args.dryrun,

        forceAllowSymlinks=args.forceAllowSymlinks,
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
