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
from typing import Any
from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from backend.api.models import UserProfile
from backend.collab.models import EditingRoom, CollabDocument, TextDocument
from backend.collab.serializers import (
    EditingRoomSerializer,
    CollabDocumentListSerializer,
    CollabDocumentSerializer,
    TextDocumentSerializer,
)
from backend.api.errors import CustomError
from backend.static.error_codes import ERROR__API__ID_NOT_FOUND
from backend.static.middleware import get_private_key_from_request


class TextDocumentModelViewSet(viewsets.ModelViewSet):
    queryset = TextDocument.objects.all()

    def get_queryset(self) -> QuerySet:
        if self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(rlc=self.request.user.rlc)

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        doc: TextDocument = TextDocument.objects.get(pk=kwargs["pk"])
        users_private_key = get_private_key_from_request(request)
        user: UserProfile = request.user
        key: str = user.get_rlcs_aes_key(users_private_key)
        data = TextDocumentSerializer(doc).get_decrypted_data(key)
        return Response(data)

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        doc: TextDocument = TextDocument.objects.get(pk=kwargs["pk"])
        users_private_key = get_private_key_from_request(request)
        user: UserProfile = request.user
        key: str = user.get_rlcs_aes_key(users_private_key)
        doc.patch(request.data, key, user)

        return Response(TextDocumentSerializer(doc).get_decrypted_data(key))