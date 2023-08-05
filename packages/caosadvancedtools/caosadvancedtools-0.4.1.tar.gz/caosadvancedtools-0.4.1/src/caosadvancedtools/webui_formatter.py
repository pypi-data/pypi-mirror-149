# encoding: utf-8
#
# Copyright (C) 2019, 2020 IndiScale GmbH <info@indiscale.com>
# Copyright (C) 2020 Timm Fitschen <t.fitschen@indiscale.com>
# Copyright (C) 2019, 2020 Henrik tom Wörden <h.tomwoerden@indiscale.com>
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
import logging

from .serverside.helper import wrap_bootstrap_alert


class WebUI_Formatter(logging.Formatter):
    """ allows to make logging to be nicely displayed in the WebUI

    You can enable this as follows:
    logger = logging.getLogger("<LoggerName>")
    formatter = WebUI_Formatter(full_file="path/to/file")
    handler = logging.Handler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    """

    def __init__(self, *args, full_file=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_elements = 100
        self.counter = 0
        self.full_file = full_file

    def format(self, record):
        """ Return the HTML formatted log record for display on a website.

        This essentially wraps the text formatted by the parent class in html.

        Parameters
        ----------

        record :

        Raises
        ------
        RuntimeError
            If the log level of the record is not supported. Supported log
            levels include logging.DEBUG, logging.INFO, logging.WARNING,
            logging.ERROR, and logging.CRITICAL.

        Returns
        -------
        str
            The formatted log record.

        """
        msg = super().format(record)
        self.counter += 1

        if self.counter == self.max_elements:
            return wrap_bootstrap_alert(
                "<b>Warning:</b> Due to the large number of messages, the "
                "output is stopped here. You can see the full log "
                " <a href='{}'>here</a>.".format(self.full_file),
                kind="warning")

        if self.counter > self.max_elements:
            return ""

        text = msg.replace("\n", r"</br>")
        text = text.replace("\t", r"&nbsp;"*4)

        if record.levelno == logging.DEBUG:
            return wrap_bootstrap_alert(msg, kind="info")
        elif record.levelno == logging.INFO:
            return wrap_bootstrap_alert("<b>Info:</b> " + text, kind="info")
        elif record.levelno == logging.WARNING:
            return wrap_bootstrap_alert("<b>Warning:</b> " + text,
                                        kind="warning")
        elif record.levelno == logging.ERROR:
            return wrap_bootstrap_alert("<b>ERROR:</b> " + text, kind="danger")
        elif record.levelno == logging.CRITICAL:
            return wrap_bootstrap_alert("<b>CRITICAL ERROR:</b> " + text,
                                        kind="danger")
        else:
            raise Exception("unknown level")
