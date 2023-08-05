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
from __future__ import absolute_import

import argparse
import datetime
import json
import logging
import os
import subprocess
import sys
from email import message, policy, utils
from tempfile import NamedTemporaryFile

import caosdb as db


def wrap_bootstrap_alert(text, kind):
    """ Wrap a text into a Bootstrap (3.3.7) DIV.alert.

    Parameters
    ----------

    text : str
        The text body of the bootstrap alert.
    kind : str
        One of ["success", "info", "warning", "danger"]

    Returns
    -------
    alert : str
        A HTML str of a Bootstrap DIV.alert
    """

    return ('<div class="alert alert-{kind} alert-dismissible" '
            'role="alert">{text}</div>').format(kind=kind, text=text)


def print_bootstrap(text, kind, file=sys.stdout):
    """ Wrap a text into a Bootstrap (3.3.7) DIV.alert and print it to a file.

    Parameters
    ----------

    text : str
        The text body of the bootstrap alert.
    kind : str
        One of ["success", "info", "warning", "danger"]
    file : file, optional
        Print the alert to this file. Default: sys.stdout.

    Returns
    -------
    None
    """
    print(wrap_bootstrap_alert(text, kind), file=file)


def print_success(text):
    """Shortcut for print_bootstrap(text, kine="success")

    The text body is also prefixed with "<b>Success:</b> ".

    Parameters
    ----------

    text : str
        The text body of the bootstrap alert.

    Returns
    -------
    None
    """
    print_bootstrap("<b>Success:</b> " + text, kind="success")


def print_info(text):
    """Shortcut for print_bootstrap(text, kine="info")

    The text body is also prefixed with "<b>Info:</b> ".

    Parameters
    ----------

    text : str
        The text body of the bootstrap alert.

    Returns
    -------
    None
    """
    print_bootstrap("<b>Info:</b> " + text, kind="info")


def print_warning(text):
    """Shortcut for print_bootstrap(text, kine="warning")

    The text body is also prefixed with "<b>Warning:</b> ".

    Parameters
    ----------

    text : str
        The text body of the bootstrap alert.

    Returns
    -------
    None
    """
    print_bootstrap("<b>Warning:</b> " + text, kind="warning")


def print_error(text):
    """Shortcut for print_bootstrap(text, kine="danger")

    The text body is also prefixed with "<b>ERROR:</b> ".

    Parameters
    ----------

    text : str
        The text body of the bootstrap alert.

    Returns
    -------
    None
    """
    print_bootstrap("<b>ERROR:</b> " + text, kind="danger", file=sys.stderr)


class DataModelError(RuntimeError):
    """DataModelError indicates that the server-side script cannot work as
    intended due to missing data model entities or an otherwise incompatible
    data model."""

    def __init__(self, rt, info=""):
        super().__init__(
            "This script expects certain RecordTypes and Properties to exist "
            "in the data model. There is a problem with {}. {}".format(rt, info))


def recordtype_is_child_of(rt, parent):
    """Return True iff the RecordType is a child of another Entity.

    The parent Entity can be a direct or indirect parent.

    Parameters
    ----------

    rt : caosdb.Entity
        The child RecordType.
    parent : str or int
        The parent's name or id.

    Returns
    -------
    bool
        True iff `rt` is a child of `parent`
    """
    query = "COUNT RecordType {} with id={}".format(parent, rt.id)

    if db.execute_query(query) > 0:
        return True
    else:
        return False


def init_data_model(entities):
    """Return True iff all entities exist and their role and possibly their
    data type is correct.

    This implementation follows a fail-fast approach. The first entity with
    problems will raise an exception.

    Parameters
    ----------

    entities : iterable of caosdb.Entity
        The data model entities which are to be checked for existence.

    Raises
    ------
    DataModelError
        If any entity in `entities` does not exist or the role or data type is
        not matching.

    Returns
    -------
    bool
        True if all entities exist and their role and data type are matching.
    """
    try:
        for e in entities:
            local_datatype = e.datatype
            local_role = e.role
            e.retrieve()

            if local_datatype is not None and local_datatype != e.datatype:
                info = ("The remote entity has a {} data type while it should "
                        "have a {}.".format(e.datatype, local_datatype))
                raise DataModelError(e.name, info)

            if local_role is not None and local_role != e.role:
                info = ("The remote entity has is a {} while it should "
                        "be a {}.".format(e.role, local_role))
                raise DataModelError(e.name, info)
    except db.exceptions.EntityDoesNotExistError:
        raise DataModelError(e.name, "This entity does not exist.")

    return True


def get_data(filename, default=None):
    """Load data from a json file as a dict.

    Parameters
    ----------

    filename : str
        The file's path, relative or absolute.
    default : dict
        Default data, which is overridden by the data in the file, if the keys
        are defined in the file.

    Returns
    -------
    dict
        Data from the given file.
    """
    result = default.copy() if default is not None else {}
    with open(filename, 'r') as fi:
        data = json.load(fi)
    result.update(data)

    return result


def get_timestamp():
    """Return a ISO 8601 compliante timestamp (second precision)"""

    return datetime.datetime.utcnow().isoformat(timespec='seconds')


def get_argument_parser():
    """Return a argparse.ArgumentParser for typical use-cases.

    The parser expects a file name as data input ('filename') and and an
    optional auth-token ('--auth-token').

    The parser can also be augmented for other use cases.

    Returns
    -------
    argparse.ArgumentParser
    """
    p = argparse.ArgumentParser()
    # TODO: add better description. I do not know what json file is meant.
    # TODO: use a prefix for this argument? using this in another parser is
    # difficult otherwise
    p.add_argument("filename", help="The json filename")
    p.add_argument("--auth-token")

    return p


def parse_arguments(args):
    """Use the standard parser and parse the arguments.

    Call with `parse_arguments(args=sys.argv)` to parse the command line
    arguments.

    Parameters
    ----------
    args : list of str
        Arguments to parse.

    Returns
    -------
    dict
        Parsed arguments.
    """
    p = get_argument_parser()

    return p.parse_args(args)


def get_shared_filename(filename):
    """
    prefix a filename with a path to a shared resource directory


    Parameters
    ----------
    filename : str
        Filename to be prefixed; e.g. `log.txt`.

    Returns
    -------
    tuple
        (filename, filepath), where `filename` is the name that can be shared
        with users, such that they can retrieve the file from the shared
        directory. `filepath` is the path that can be used in a script to
        actually store the file; e.g. with open(filepath, 'w') as fi...
    """

    if "SHARED_DIR" not in os.environ:
        raise RuntimeError(
            "The environment variable 'SHARED_DIR' should be "
            "set. Cannot identifiy the directory for the shared resource")

    directory = os.environ["SHARED_DIR"]
    randname = os.path.basename(os.path.abspath(directory))
    filepath = os.path.abspath(os.path.join(directory, filename))
    filename = os.path.join(randname, filename)

    return filename, filepath


def send_mail(from_addr, to, subject, body, cc=None, bcc=None,
              send_mail_bin=None):
    """ Send an email via the configured send_mail client.

    The relevant options in the pycaosdb.ini are:

        [Misc]
        sendmail = ...

    Parameters
    ----------
    from_addr : str
        The sender's email address.
    to : str or list of str
        The recipient's email address.
    subject : str
        Subject of the email.
    body : str
        The mail body, i.e. the text message.
    cc : str or list of str (optional)
        Single or list of cc-recipients. Defaults to None.
    bcc : str or list of str (optional)
        Single or list of bcc-recipients. Defaults to None.
    send_mail_bin : str (optional)
        Path of sendmail client. Defaults to config["Misc"]["sendmail"].

    Raises
    ------
    subprocess.CalledProcessError
        If the sendmail client returned with a non-zero code.
    caosdb.ConfigurationException
        If the caosdb configuration has no `Misc.sendmail` configured while the
        `send_mail_bin` parameter is None.
    """

    # construct the mail
    mail = message.EmailMessage(policy=policy.SMTP)
    mail.set_content(body)
    mail["From"] = from_addr
    mail["To"] = to if isinstance(to, str) else ", ".join(to)
    mail["Subject"] = subject
    mail['Date'] = utils.formatdate(localtime=True)

    if cc is not None:
        mail["CC"] = cc if isinstance(cc, str) else ", ".join(cc)

    if bcc is not None:
        mail["BCC"] = bcc if isinstance(cc, str) else ", ".join(cc)

    # construct the call

    if send_mail_bin is not None:
        sendmail = send_mail_bin
    else:
        caosdb_config = db.configuration.get_config()

        if "Misc" not in caosdb_config or "sendmail" not in caosdb_config["Misc"]:
            err_msg = ("No sendmail executable configured. "
                       "Please configure `Misc.sendmail` "
                       "in your pycaosdb.ini.")
            raise db.ConfigurationError(err_msg)
        sendmail = caosdb_config["Misc"]["sendmail"]

    # construct sendmail command
    # options explained (from `man sendmail`):
    #   -t  Read message for recipients. To:, Cc:, and Bcc: lines will be
    #       scanned for recipient addresses. The Bcc: line will be deleted
    #       before transmission.
    #   -i  Ignore dots alone on lines by themselves in incoming messages. This
    #       should be set if you are reading data from a file.
    #   -f  Sets the name of the ''from'' person (i.e., the envelope sender of
    #       the mail). This address may also be used in the From: header if
    #       that header is missing during initial submission. The envelope
    #       sender address is used as the recipient for delivery status
    #       notifications and may also appear in a Return-Path: header. -f
    #       should only be used by ''trusted'' users (normally root, daemon,
    #       and network) or if the person you are trying to become is the same
    #       as the person you are. Otherwise, an X-Authentication-Warning
    #       header will be added to the message.
    command = [sendmail, "-t", "-i", "-f", from_addr]

    # execute and handle return code
    p = subprocess.Popen(command,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout, stderr = p.communicate(mail.as_bytes())
    return_code = p.wait()

    if return_code != 0:
        raise subprocess.CalledProcessError(return_code, command,
                                            output=stdout.decode("utf8"),
                                            stderr=stderr.decode("utf8"))


def get_file_via_download(ent, logger=logging.getLogger(__name__)):
    """ downloads the given file entity

    The typical error handling is done.
    """
    try:
        # TODO remove the following treatment of size=0 when the
        # following issue is resolved:
        # https://gitlab.com/caosdb/caosdb-server/-/issues/107

        if ent.size > 0:
            val_file = ent.download()
        else:
            ntf = NamedTemporaryFile(delete=False)
            ntf.close()
            val_file = ntf.name
    except db.ConsistencyError as e:
        logger.error("The checksum of the downloaded file with id={} did not "
                     "match.".format(ent.id))
        raise e
    except db.CaosDBException as e:
        logger.error("Cannot download the file with id={}.".format(ent.id))
        raise e

    return val_file


class NameCollector(object):
    def __init__(self):
        self.names = []

    def get_unique_savename(self, name):
        """ make names unique by attaching numbers

        This is for example use full if multiple files shall be saved into one
        directory but the names of them are not unique
        """
        orig_name = name

        if name in self.names:
            ii = self.names.count(name) + 1
            name += "_{}".format(ii)
        self.names.append(orig_name)

        return name
