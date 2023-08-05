# This file is a part of the CaosDB Project.
#
# Copyright (C) 2021 IndiScale GmbH <info@indiscale.com>
# Copyright (C) 2021 Daniel Hornung <d.hornung@indiscale.com>
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
"""Interaction with the Bloxberg blockchain.
"""


import hashlib
import json
import secrets

import caosdb as db

from ..models.parser import parse_model_from_string
from . import swagger_client


__model_yaml = """
BloxbergCertificate:
  obligatory_properties:
    pepper:
      datatype: TEXT
    hash:
      datatype: TEXT
    proofValue:
      datatype: TEXT
    certificateJSON:
      datatype: TEXT
  recommended_properties:
    certified:
      datatype: REFERENCE
"""
__model = parse_model_from_string(__model_yaml)


class Bloxberg:
    """A Bloxberg instance can be used to obtain or verify certificates."""

    def __init__(self, connection=None):
        """A Bloxberg instance can be used to obtain or verify certificates.

Parameters
----------
connection : dict
A dict with the following keys:
  - url : The bloxberg URL. Default is "https://qa.certify.bloxberg.org"
        """
        self._create_conf(connection)
        self._api_client = swagger_client.ApiClient(configuration=self._conf)
        self._api = swagger_client.CertificateApi(self._api_client)

    def _create_conf(self, connection=None):
        """Generate a Swagger configuration object."""
        self._conf = swagger_client.Configuration()
        if connection:
            if "URL" in connection:
                self._conf.host = connection["URL"]

    def certify(self, entity):
        """Attempt to certify the given `entity` and return a certificate Record.

Parameters
----------
entity : caosdb.Entity
The entity to be certified

Returns
-------
out : caosdb.Record
A BloxbergCertificate Record with all the necessary Properties.
"""
        # Calculate hash
        pepper = str(secrets.randbits(1024))
        entity.retrieve()
        hasher = hashlib.sha256()
        hasher.update(pepper.encode(encoding="utf8"))
        hasher.update(str(entity).encode(encoding="utf8"))
        entity_hash = "0x" + hasher.hexdigest()
        print(entity_hash)
        pubkey = "0x9858eC18a269EE69ebfD7C38eb297996827DDa98"  # TODO The key of the API server?
        # Create body
        body = swagger_client.Batch(public_key=pubkey, crid=[entity_hash], crid_type="sha2-256",
                                    enable_ipfs=False)
        # Submit hash & obtain response
        result = self._api.create_bloxberg_certificate_create_bloxberg_certificate_post(body=body)
        attribute_map = result[0].attribute_map
        cert = result[0].to_dict()
        for old, new in attribute_map.items():
            if old == new:
                continue
            cert[new] = cert.pop(old)
        json_s = json.dumps(cert)
        # Generate result Record
        cert_rec = db.Record().add_parent("BloxbergCertificate")
        # Extract information and put into result
        cert_rec.add_property(property="certified", value=entity)
        cert_rec.add_property(property="pepper", value=pepper)
        cert_rec.add_property(property="hash", value=entity_hash)
        cert_rec.add_property(property="proofvalue", value=cert["proof"]["proofValue"])
        cert_rec.add_property(property="certificateJSON", value=json_s)
        # Return result
        return cert_rec

    def verify(self, certificate):
        """Attempt to verify the certificate.

A certificate passes verification if the Bloxberg instance says it is good.  Typical use cases may
also include the `validate` step to make sure that the certificate's original data exists and
contains what it claimed to contain when the certificate was created.

This method does nothing if the verification passes, else it raises an exception.

Parameters
----------
certificate : caosdb.Record
The BloxbergCertificate Record which shall be verified.

        """
        raise NotImplementedError("Bloxberg first needs to implement a verification API method.")

    @staticmethod
    def json_from_certificate(certificate, filename=None):
        """Generate a qa.certify.bloxberg.org JSON string, optionally writing it to a file.

Parameters
----------
certificate : caosdb.Record
The BloxbergCertificate Record for which the JSON is generated.

filename : str
Write the JSON to this file.
"""
        content = {}

        return content


def ensure_data_model(force=False):
    """Make sure that the data model fits our needs.

    Most importantly, this means that a suitable RecordType "BoxbergCertificate" must exist.
    """
    __model.sync_data_model(noquestion=force)


def certify_entity(entity, json_filename=None):
    """Certify the given entity and store the result in the CaosDB.

Parameters
----------
entity : caosdb.Entity
  The Entity to be certified.

json_filename : str
  If given, store the JSON here.
"""
    if isinstance(entity, int):
        entity = db.Entity(id=entity)

    blx = Bloxberg()
    print("Obtaining certificate...")
    certificate = blx.certify(entity)
    print("Certificate was successfully obtained.")
    certificate.insert()
    print("Certificate was stored in CaosDB.")

    if json_filename:
        with open(json_filename, "w") as json_file:
            json_file.write(certificate.get_property("certificateJSON").value)


def demo_run():
    """Run the core functions for demonstration purposes."""
    print("Making sure that the remote data model is up to date.")
    ensure_data_model()
    print("Data model is up to date.")
    import caosdb as db
    CertRT = db.RecordType(name="BloxbergCertificate").retrieve()
    print("Certifying the `BloxbergCertificate` RecordType...")
    json_filename = "/tmp/cert.json"
    certify_entity(CertRT, json_filename=json_filename)
    print("Certificate json file can be found here: {}".format(json_filename))
    print("You can verify the certificate here: https://certify.bloxberg.org/verify")
