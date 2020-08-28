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
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

from backend.api.errors import CustomError
from backend.recordmanagement.models import *
from backend.recordmanagement.serializers import (
    EncryptedRecordDocumentDeletionRequestSerializer,
)
from backend.static import error_codes, permissions
from backend.api.models import Notification


class EncryptedRecordDocumentDeletionRequestViewSet(viewsets.ModelViewSet):
    serializer_class = EncryptedRecordDocumentDeletionRequestSerializer

    def get_queryset(self) -> QuerySet:
        if self.request.user.is_superuser:
            return EncryptedRecordDocumentDeletionRequest.objects.all()
        else:
            return EncryptedRecordDocumentDeletionRequest.objects.filter(
                document__record__from_rlc=self.request.user.rlc
            )

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        try:
            document: EncryptedRecordDocument = EncryptedRecordDocument.objects.get(
                pk=request.data["document_id"]
            )
        except Exception as e:
            raise CustomError(error_codes.ERROR__API__ID_NOT_FOUND)

        if not document.record.user_has_permission(request.user):
            raise CustomError(error_codes.ERROR__API__PERMISSION__INSUFFICIENT)

        if (
            EncryptedRecordDocumentDeletionRequest.objects.filter(
                request_from=request.user, document=document
            ).count()
            > 0
        ):
            raise CustomError(error_codes.ERROR__API__ALREADY_REQUESTED)

        deletion_request: (
            EncryptedRecordDocumentDeletionRequest
        ) = EncryptedRecordDocumentDeletionRequest(
            document=document, request_from=request.user
        )
        deletion_request.explanation = request.data.get("explanation", "")
        deletion_request.save()

        return Response(status=201)

    def list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        if (
            not request.user.has_permission(
                permissions.PERMISSION_PROCESS_RECORD_DOCUMENT_DELETION_REQUESTS,
                for_rlc=request.user.rlc,
            )
            and not request.user.is_superuser
        ):
            raise CustomError(error_codes.ERROR__API__PERMISSION__INSUFFICIENT)

        return Response(
            EncryptedRecordDocumentDeletionRequestSerializer(
                self.get_queryset(), many=True
            ).data
        )
