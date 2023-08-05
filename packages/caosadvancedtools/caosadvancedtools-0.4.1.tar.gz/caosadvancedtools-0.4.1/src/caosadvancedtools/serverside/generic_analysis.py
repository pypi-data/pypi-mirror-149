# encoding: utf-8
#
# Copyright (C) 2021 Alexander Schlemmer <alexander.schlemmer@ds.mpg.de>
# Copyright (C) 2021 IndiScale GmbH <info@indiscale.com>
# Copyright (C) 2021 Henrik tom Wörden <h.tomwoerden@indiscale.com>
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
# See: https://gitlab.indiscale.com/caosdb/src/caosdb-advanced-user-tools/-/issues/55

# This source file is work in progress and currently untested.


"""
Variante I: Python module implementiert eine 'main' function, die einen Record
als Argument entgegennimmt und diesen um z.B. 'results' ergänzt und updated.

Variante II: Ein skript erhält eine ID als Argument (z.B. auf der command line)
und updated das Objekt selbstständig.

Idealfall: Idempotenz; I.e. es ist egal, ob das Skript schon aufgerufen wurde.
Ein weiterer Aufruf führt ggf. zu einem Update (aber nur bei Änderungen von
z.B. Parametern)

Das aufgerufene Skript kann beliebige Eigenschaften benutzen und erstellen.
ABER wenn die Standardeigenschaften (InputDataSet, etc) verwendet werden, kann
der Record leicht erzeugt werden.



      "Analyze"       "Perform Anlysis"
   Knopf an Record     Form im WebUI
   im WebUI
         |               |
         |               |
         v               v
     Winzskript, dass einen
     DataAnalysis-Stub erzeugt
          |
          |
          v
    execute_script Routine -->  AnalysisSkript
    erhält den Stub und ggf.    Nutzt Funktionen um Updates durchzuführen falls
    den Pythonmodulenamen       notwendig, Email
         ^
         |
         |
    Cronjob findet outdated
    DataAnalysis


Analyseskript macht update:
    - flexibel welche Änderungen vorgenommen werden (z.B. mehrere Records)
    - spezielle Funktionen sollten verwendet werden
    - Logging und informieren muss im Skript passieren
    - Skript kann mit subprocess aufgerufen werden (alternative unvollständige
      DataAnalysis einfügen)


# Features
    - Emailversand bei Insert oder Update
    - Kurze Info: "Create XY Analysis" kann vmtl automatisch erzeugt werden
    - Debug Info: müsste optional/bei Fehler zur Verfügung stehen.
    - Skript/Software version sollte gespeichert werden


Outlook: the part of the called scripts that interact with LinkAhead might in
future be replaced by the Crawler. The working directory would be copied to the
file server and then crawled.
"""

import argparse
import importlib
import logging
import os
import sys

import caosdb as db
from caosdb.utils.server_side_scripting import run_server_side_script

logger = logging.getLogger(__name__)


def check_referenced_script(record: db.Record):
    """ return the name of a referenced script

    If the supplied record does not have an appropriate Property warings are
    logged.
    """

    if record.get_property("scripts") is None:
        logger.warning("The follwing changed Record is missing the 'scripts' "
                       "Property:\n{}".format(str(record)))

        return

    script_prop = record.get_property("scripts")

    if not db.apiutils.is_reference(script_prop):
        logger.warning("The 'scripts' Property of the following Record should "
                       "reference a File:\n{}".format(str(record)))

        return

    script = db.execute_query("FIND ENTITY WITH id={}".format(
        script_prop.value[0] if isinstance(script_prop.value, list)
        else script_prop.value), unique=True)

    if (not isinstance(script, db.File)):
        logger.warning("The 'scripts' Property of the Record {} should "
                       "reference a File. Entity {} is not a File".format(
                           record.id, script_prop.value))

        return

    script_name = os.path.basename(script.path)

    return script_name


def call_script(script_name: str, record_id: int):
    ret = run_server_side_script(script_name, record_id)

    if ret.code != 0:
        logger.error("Script failed!")
        logger.debug(ret.stdout)
        logger.error(ret.stderr)
    else:
        logger.debug(ret.stdout)
        logger.error(ret.stderr)


def run(dataAnalysisRecord: db.Record):
    """run a data analysis script.

    There are two options:
    1. A python script installed as a pip package.
    2. A generic script that can be executed on the command line.

    Using a python package:
    It should be located in package plugin and implement at least
    a main function that takes a DataAnalysisRecord as a single argument.
    The script may perform changes to the Record and insert and update
    Entities.

    Using a generic script:
    The only argument that is supplied to the script is the ID of the
    dataAnalysisRecord. Apart from the different Argument everything that is
    said for the python package holds here.
    """

    if dataAnalysisRecord.get_property("scripts") is not None:
        script_name = check_referenced_script(dataAnalysisRecord)
        logger.debug(
            "Found 'scripts'. Call script '{}' in separate process".format(
                script_name)
            )
        call_script(script_name, dataAnalysisRecord.id)
        logger.debug(
            "Script '{}' done.\n-----------------------------------".format(
                script_name))

    if dataAnalysisRecord.get_property("Software") is not None:
        mod = dataAnalysisRecord.get_property("Software").value
        logger.debug(
            "Found 'Software'. Call '{}' as Python module".format(
                mod)
            )
        m = importlib.import_module(mod)

        m.main(dataAnalysisRecord)
        logger.debug(
            "'main' function of  Python module '{}' done"
            ".\n-----------------------------------".format(mod))


def _parse_arguments():
    """ Parses the command line arguments.  """
    parser = argparse.ArgumentParser(description='__doc__')
    parser.add_argument("--module", help="An id an input dataset.")
    parser.add_argument("--inputset", help="An id an input dataset.")
    parser.add_argument("--parameterset", help="An id of a parameter record.")

    return parser.parse_args()


def main():
    """ This is for testing only. """
    args = _parse_arguments()

    dataAnalysisRecord = db.Record()
    dataAnalysisRecord.add_property(name="InputDataSet", value=args.entity)
    dataAnalysisRecord.add_property(name="ParameterSet", value=args.parameter)
    dataAnalysisRecord.add_property(name="Software", value=args.module)

    dataAnalysisRecord.insert()
    run(dataAnalysisRecord)


if __name__ == "__main__":
    sys.exit(main())
