# encoding: utf-8
#
# Copyright (C) 2020 IndiScale GmbH <info@indiscale.com>
# Copyright (C) 2020 Henrik tom Wörden <h.tomwoerden@indiscale.com>
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
#
from __future__ import absolute_import

import logging
import os
import sys
import tempfile
from datetime import datetime

from ..webui_formatter import WebUI_Formatter
from .helper import get_shared_filename


def configure_server_side_logging(loggername="caosadvancedtools"):
    """
    Set logging up to save one plain debugging log file, one plain info log
    file (for users) and a stdout stream with messages wrapped in html elements

    returns the path to the file with debugging output
    """
    logger = logging.getLogger(loggername)
    logger.setLevel(level=logging.DEBUG)

    filename, filepath = get_shared_filename("log.txt")

    # this is a log file with INFO level for the user
    user_file_handler = logging.FileHandler(filename=filepath)
    user_file_handler.setLevel(logging.INFO)
    logger.addHandler(user_file_handler)

    # The output shall be printed in the webui. Thus wrap it in html elements.
    formatter = WebUI_Formatter(full_file="/Shared/{}".format(filename))
    web_handler = logging.StreamHandler(stream=sys.stdout)
    web_handler.setFormatter(formatter)
    web_handler.setLevel(logging.INFO)
    logger.addHandler(web_handler)

    # one log file with debug level output
    debug_file = os.path.join(tempfile.gettempdir(),
                              "{}_{}.log".format(__name__,
                                                 datetime.now().isoformat()))
    debug_handler = logging.FileHandler(filename=debug_file)
    debug_handler.setLevel(logging.DEBUG)
    logger.addHandler(debug_handler)

    return debug_file
