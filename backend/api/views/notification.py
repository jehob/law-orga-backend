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
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response

from backend.api.errors import CustomError
from backend.api.models import Notification
from backend.api.serializers import NotificationSerializer
from backend.static.error_codes import ERROR__API__ID_NOT_PROVIDED, ERROR__API__NOTIFICATION__UPDATE_INVALID, \
    ERROR__API__USER__NO_OWNERSHIP, ERROR__API__ID_NOT_FOUND


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self) -> QuerySet:
        if not self.request.user.is_superuser:
            queryset = Notification.objects.filter(user=self.request.user)
        else:
            queryset = Notification.objects.all()
        request: Request = self.request
        if 'sort' in request.query_params:
            if 'sortdirection' in request.query_params and request.query_params['sortdirection'] == 'desc':
                queryset = queryset.order_by('-' + request.query_params['sort'])
            else:
                queryset = queryset.order_by(request.query_params['sort'])
        else:
            queryset = queryset.order_by("-created")
        return queryset

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        if 'pk' not in kwargs:
            raise CustomError(ERROR__API__ID_NOT_PROVIDED)
        try:
            notification: Notification = Notification.objects.get(pk=kwargs['pk'])
        except Exception as e:
            raise CustomError(ERROR__API__ID_NOT_FOUND)

        if request.user != notification.user:
            raise CustomError(ERROR__API__USER__NO_OWNERSHIP)

        if 'read' not in request.data or request.data.__len__() > 1:
            raise CustomError(ERROR__API__NOTIFICATION__UPDATE_INVALID)
        notification.read = request.data['read']
        notification.save()

        return Response({'success': True})
