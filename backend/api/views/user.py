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

from datetime import datetime

import pytz
from django.forms.models import model_to_dict
from django.http import QueryDict
from rest_framework import viewsets, filters, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request

from backend.api.errors import CustomError
from backend.static import permissions
from backend.static.date_utils import parse_date
from backend.static.emails import EmailSender, FrontendLinks
from backend.static.encryption import RSAEncryption
from backend.static.error_codes import *
from backend.api.models import (
    UserProfile,
    Permission,
    Rlc,
    UserEncryptionKeys,
    Notification,
    NotificationGroup,
)
from backend.api.serializers import (
    UserProfileSerializer,
    UserProfileCreatorSerializer,
    UserProfileNameSerializer,
    RlcSerializer,
    UserProfileForeignSerializer,
)
from backend.static.permissions import PERMISSION_ACCEPT_NEW_USERS_RLC
from backend.static.middleware import get_private_key_from_request


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handles reading and updating profiles"""

    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = (
        "name",
        "email",
    )

    def list(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = UserProfile.objects.all()
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            queryset = UserProfile.objects.filter(rlc=request.user.rlc, is_active=True)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = UserProfileNameSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = UserProfileNameSerializer(queryset, many=True)
            return Response(serializer.data)

    def retrieve(self, request, pk=None, **kwargs):
        if pk is None:
            raise CustomError(ERROR__API__USER__ID_NOT_PROVIDED)
        try:
            user = UserProfile.objects.get(pk=pk)
        except Exception as e:
            raise CustomError(ERROR__API__USER__NOT_FOUND)

        if request.user.rlc != user.rlc:
            if request.user.is_superuser or request.user.has_permission(
                permissions.PERMISSION_VIEW_FULL_USER_DETAIL_OVERALL
            ):
                serializer = UserProfileSerializer(user)
            else:
                raise CustomError(ERROR__API__USER__NOT_SAME_RLC)
        else:
            if request.user.has_permission(
                permissions.PERMISSION_VIEW_FULL_USER_DETAIL_RLC
            ):
                serializer = UserProfileSerializer(user)
            else:
                serializer = UserProfileForeignSerializer(user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        try:
            user_id = kwargs["pk"]
            user = UserProfile.objects.get(pk=user_id)
        except:
            raise CustomError(ERROR__API__ID_NOT_FOUND)
        if request.user != user and not request.user.is_superuser:
            raise CustomError(ERROR__API__PERMISSION__INSUFFICIENT)
        data = request.data
        if "birthday" in data:
            user.birthday = parse_date(data["birthday"])
        if "postal_code" in data:
            user.postal_code = data["postal_code"]
        if "street" in data:
            user.street = data["street"]
        if "city" in data:
            user.city = data["city"]
        if "phone_number" in data:
            user.phone_number = data["phone_number"]
        if "user_state" in data:
            user.user_state = data["user_state"]
        if "user_record_state" in data:
            user.user_record_state = data["user_record_state"]
        if request.user.is_superuser:
            if "email" in data and data["email"] != "":
                user.email = data["email"]
            if "name" in data and data["name"] != "":
                user.name = data["name"]
            if "is_active" in data:
                user.is_active = data["is_active"]
        user.save()
        return Response(UserProfileSerializer(user).data)


class UserProfileCreatorViewSet(viewsets.ModelViewSet):
    """Handles creating profiles"""

    serializer_class = UserProfileCreatorSerializer
    queryset = UserProfile.objects.none()
    authentication_classes = ()
    permission_classes = ()

    def create(self, request: Request):
        if type(request.data) is QueryDict:
            data = request.data.dict()
        else:
            data = dict(request.data)
        if "rlc" in data:
            del data["rlc"]

        # Check if email already in use
        if not "email" in request.data:
            raise CustomError(ERROR__API__USER__CAN_NOT_CREATE)
        if UserProfile.objects.filter(email=request.data["email"].lower()).count() > 0:
            raise CustomError(ERROR__API__EMAIL__ALREADY_IN_USE)
        data["email"] = data["email"].lower()

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        # check if rlc exists before saving
        if "rlc" not in request.data:
            raise CustomError(ERROR__API__REGISTER__NO_RLC_PROVIDED)
        try:
            rlc = Rlc.objects.get(pk=request.data["rlc"])
        except:
            raise CustomError(ERROR__API__REGISTER__RLC_NOT_FOUND)
        self.perform_create(serializer)

        user = UserProfile.objects.get(email=request.data["email"].lower())
        user.rlc = rlc
        user.save()
        if "birthday" in request.data and request.data["birthday"] != "Invalid date":
            user.birthday = request.data["birthday"]
        user.is_active = False
        user.save()

        user.generate_new_user_encryption_keys()

        # new user request
        from backend.api.models import NewUserRequest

        new_user_request = NewUserRequest(request_from=user)
        new_user_request.save()

        # new user activation link
        from backend.api.models import UserActivationLink

        user_activation_link = UserActivationLink(user=user)
        user_activation_link.save()

        EmailSender.send_user_activation_email(
            user, FrontendLinks.get_user_activation_link(user_activation_link)
        )

        Notification.objects.notify_new_user_request(user, new_user_request)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class LoginViewSet(viewsets.ViewSet):
    """checks email and password and returns auth token"""

    serializer_class = AuthTokenSerializer
    authentication_classes = ()
    permission_classes = ()

    def create(self, request):
        """
        use the obtainauthToken APIView to validate and create a token
        additionally add all important information for app usage
        like static possible states, possible permissions and so on
        Args:
            request: the request with data: 'username' and 'password"

        Returns:
        token, information and permissions of user
        private_key of user
        all possible permissions, country states, countries, clients, record states, consultants
        """
        user_password = request.data["password"]
        data = {"password": user_password, "username": request.data["username"].lower()}
        serializer = self.serializer_class(data=data)
        LoginViewSet.check_if_user_active(data["username"])
        if serializer.is_valid():
            token, created = Token.objects.get_or_create(
                user=serializer.validated_data["user"]
            )
            Token.objects.filter(user=token.user).exclude(
                key=token.key
            ).delete()  # delete old tokens, keep new
            if not created:
                # update the created time of the token to keep it valid
                token.created = datetime.utcnow().replace(tzinfo=pytz.utc)
                token.save()
            # get encryption keys
            encryption_keys = UserEncryptionKeys.objects.get(user=token.user)
            if not encryption_keys:
                private, public = RSAEncryption.generate_keys()
                encryption_keys = UserEncryptionKeys(
                    user=token.user, private_key=private, public_key=public
                )
                encryption_keys.save()
            # decrypt keys with users password (or: if not encrypted atm, encrypt them with users password)
            private_key = encryption_keys.decrypt_private_key(user_password)

            # from backend.recordmanagement.helpers import (
            #     resolve_missing_record_key_entries,
            # )

            # resolve_missing_record_key_entries(token.user, private_key)
            # TODO: superuser?
            if not token.user.is_superuser:
                from backend.api.helpers import resolve_missing_rlc_keys_entries

                resolve_missing_rlc_keys_entries(token.user, private_key)

            return Response(LoginViewSet.get_login_data(token.key, private_key))
        raise CustomError(ERROR__API__LOGIN__INVALID_CREDENTIALS)

    def get(self, request):
        token = request.META["HTTP_AUTHORIZATION"].split(" ")[1]
        try:
            Token.objects.get(key=token)
        except:
            raise CustomError(ERROR__API__NOT_AUTHENTICATED)

        return Response(LoginViewSet.get_login_data(token))

    @staticmethod
    def get_login_data(token, private_key=None):
        user = Token.objects.get(key=token).user
        serialized_user = UserProfileSerializer(user).data
        serialized_rlc = RlcSerializer(user.rlc).data

        notifications = NotificationGroup.objects.filter(user=user, read=False).count()

        statics = LoginViewSet.get_statics(user)
        return_object = {
            "token": token,
            "user": serialized_user,
            "rlc": serialized_rlc,
            "notifications": notifications,
        }
        return_object.update(statics)
        if private_key:
            return_object.update({"users_private_key": private_key})

        return return_object

    @staticmethod
    def get_statics(user):
        user_permissions = [
            model_to_dict(perm) for perm in user.get_all_user_permissions()
        ]
        overall_permissions = [
            model_to_dict(permission) for permission in Permission.objects.all()
        ]
        user_states_possible = UserProfile.user_states_possible
        user_record_states_possible = UserProfile.user_record_states_possible

        return {
            "permissions": user_permissions,
            "all_permissions": overall_permissions,
            "user_states": user_states_possible,
            "user_record_states": user_record_states_possible,
        }

    @staticmethod
    def check_if_user_active(user_email):
        """
        checks if user exists and if user is active
        :param user_email: string, email of user
        :return:
        """
        try:
            user = UserProfile.objects.get(email=user_email)
        except:
            raise CustomError(ERROR__API__USER__NOT_FOUND)
        if not user.is_active:
            raise CustomError(ERROR__API__USER__INACTIVE)


class LogoutViewSet(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        if not request.user.is_authenticated:
            return Response()
        Token.objects.filter(user=request.user).delete()
        return Response()


class InactiveUsersViewSet(APIView):
    def get(self, request):
        if not request.user.has_permission(
            permissions.PERMISSION_ACTIVATE_INACTIVE_USERS_RLC, for_rlc=request.user.rlc
        ):
            raise CustomError(ERROR__API__PERMISSION__INSUFFICIENT)
        inactive_users = UserProfile.objects.filter(
            rlc=request.user.rlc, is_active=False
        )
        return Response(UserProfileSerializer(inactive_users, many=True).data)

    def post(self, request):
        if not request.user.has_permission(
            permissions.PERMISSION_ACTIVATE_INACTIVE_USERS_RLC, for_rlc=request.user.rlc
        ):
            raise CustomError(ERROR__API__PERMISSION__INSUFFICIENT)
        # method and user_id
        if request.data["method"] == "activate":
            try:
                user = UserProfile.objects.get(pk=request.data["user_id"])
            except:
                raise CustomError(ERROR__API__USER__NOT_FOUND)

            granting_users_private_key = get_private_key_from_request(request)
            rlcs_aes_key = request.user.get_rlcs_aes_key(granting_users_private_key)
            user.generate_rlc_keys_for_this_user(rlcs_aes_key)

            user.is_active = True
            user.save()
            return Response(UserProfileSerializer(user).data)
        raise CustomError(ERROR__API__ACTION_NOT_VALID)
