#  law&orga - record and organization management software for refugee law clinics
#  Copyright (C) 2020  Dominik Walser
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>

from django.db import models
from datetime import datetime
import pytz
from django_prometheus.models import ExportModelOperationsMixin

from backend.static.encryption import RSAEncryption
from backend.api.errors import CustomError
from backend.api.models import Rlc
from backend.recordmanagement.models import OriginCountry
from backend.static import error_codes
from backend.static.date_utils import parse_date
from backend.static.encryption import AESEncryption


class EncryptedClient(ExportModelOperationsMixin("encrypted_client"), models.Model):
    from_rlc = models.ForeignKey(
        Rlc, related_name="e_client_from_rlc", on_delete=models.SET_NULL, null=True
    )
    created_on = models.DateField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now_add=True)

    birthday = models.DateField(null=True, blank=True)
    origin_country = models.ForeignKey(
        "OriginCountry", related_name="e_clients", on_delete=models.SET_NULL, null=True
    )

    # encrypted
    name = models.BinaryField(null=True)
    note = models.BinaryField(null=True)
    phone_number = models.BinaryField(null=True)

    encrypted_client_key = models.BinaryField(null=True)

    def __str__(self):
        return "e_client: " + str(self.id)

    def patch(self, client_data, clients_aes_key: str) -> [str]:
        patched = []
        for key, value in client_data.items():
            if key not in self.allowed_fields():
                raise CustomError(error_codes.ERROR__API__PARAMS_NOT_VALID)
            if key in self.ignore_fields():
                continue
            patched.append(key)
            if key == "origin_country":
                try:
                    country = OriginCountry.objects.get(pk=value)
                except Exception as e:
                    raise CustomError(
                        error_codes.ERROR__RECORD__ORIGIN_COUNTRY__NOT_FOUND
                    )
                self.origin_country = country

            else:
                to_save = ""
                if key in self.changeable_datetime_fields():
                    to_save = parse_date(value)
                elif key in self.changeable_encrypted_fields():
                    to_save = AESEncryption.encrypt(value, clients_aes_key)
                setattr(self, key, to_save)

        self.last_edited = datetime.utcnow().replace(tzinfo=pytz.utc)
        self.save()
        return patched

    @staticmethod
    def allowed_fields():
        return (
            EncryptedClient.changeable_datetime_fields()
            + EncryptedClient.changeable_encrypted_fields()
            + EncryptedClient.ignore_fields()
            + EncryptedClient.specific_changed_fields()
        )

    @staticmethod
    def changeable_datetime_fields():
        return ["birthday"]

    @staticmethod
    def ignore_fields():
        return ["id", "encrypted_client_key", "created_on", "last_edited", "from_rlc"]

    @staticmethod
    def specific_changed_fields():
        return ["origin_country"]

    @staticmethod
    def changeable_encrypted_fields():
        return ["name", "note", "phone_number"]

    def get_password(self, rlcs_private_key):
        encrypted_client_key = self.encrypted_client_key
        try:
            encrypted_client_key = encrypted_client_key.tobytes()
        except:
            pass
        return RSAEncryption.decrypt(encrypted_client_key, rlcs_private_key)
