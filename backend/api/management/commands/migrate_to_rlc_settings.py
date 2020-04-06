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

from django.conf import settings
from django.core.management.base import BaseCommand

from backend.api.models import RlcSettings
from backend.api.management.commands._migrators import OneTimeGenerators


class Command(BaseCommand):
    help = 'add rlc settings for all rlcs with default values'

    def handle(self, *args, **options):
        RlcSettings.objects.all().delete()
        OneTimeGenerators.generate_rlc_settings_for_rlc()