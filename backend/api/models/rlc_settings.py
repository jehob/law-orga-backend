#  law&orga - record and organization management software for refugee law clinics
#  Copyright (C) 2019  Dominik Walser
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

from backend.api.models import Rlc, Language


class RlcSettings(models.Model):
    rlc = models.ForeignKey(
        Rlc, related_name="rlc_settings", on_delete=models.CASCADE, null=False
    )

    user_record_pool = models.BooleanField(default=False, null=False)
    language_settings = models.ForeignKey(
        Language, related_name="rlc_language", on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return "rlc settings for rlc: " + str(self.rlc) + "; "
