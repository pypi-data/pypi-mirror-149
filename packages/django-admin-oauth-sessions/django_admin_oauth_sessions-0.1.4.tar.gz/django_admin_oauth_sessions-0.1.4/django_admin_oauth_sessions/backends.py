import json
from urllib.request import urlopen

import jwt
import requests
from allauth.socialaccount.models import SocialToken
from datetime import datetime
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.utils import timezone

from django_admin_oauth_sessions.utils import get_keycloak_tokens
from django.contrib.auth import get_user_model
User = get_user_model()

class DjangoAdminAuthKeycloak(BaseBackend):
    def __init__(self):
        self.public_key = self.get_keycloak_public_key()

    def authenticate(self, request, **credentials):
        try:
            return self.validate_sso_tokens(credentials.get("user"))
        except Exception as e:
            pass
        return None

    @classmethod
    def get_keycloak_public_key(cls):
        try:
            url = settings.KEYCLOAK[
                      "BASE_URL"] + '/auth/realms/' + 'dehaat'
            json_url = urlopen(url)
            data = json.loads(json_url.read())
        except Exception as e:
            msg = "Not able to acquire Keycloak Public Key"
            raise Exception(msg)

        return '-----BEGIN PUBLIC KEY-----\n' + data[
            "public_key"] + '\n-----END PUBLIC KEY-----'

    def refresh_toekn(self, user, refresh_toekn):
        data = {
            "client_id": settings.KEYCLOAK.get("CLIENT_ID"),
            "client_secret": settings.KEYCLOAK.get("CLIENT_SECRET"),
            "grant_type": "refresh_token",
            "refresh_token": refresh_toekn
        }
        realm_name = 'dehaat'
        response = requests.post(
            settings.KEYCLOAK["BASE_URL"]
            + settings.KEYCLOAK["ENDPOINTS"][
                "acquire_service_token"].format(
                realm_name
            ),
            data=data,
        )
        if response.status_code not in {
            200,
        }:
            return None

        token_info = response.json()

        decoded_access_token = jwt.decode(
            token_info.get("access_token"), self.public_key,
            audience="account", algorithms=["RS256"])
        local_tz = timezone.get_current_timezone()
        expires_at = datetime.fromtimestamp(decoded_access_token["exp"],
                                   tz=local_tz).strftime(
            '%Y-%m-%d %H:%M:%S.%f%z')
        expires_at = "{0}:{1}".format(expires_at[:-2], expires_at[-2:])

        SocialToken.objects.filter(account__user=user,
                                   account__provider="keycloak").update(
            token=token_info.get("access_token"),
            token_secret=token_info.get("refresh_token"),
            expires_at=expires_at)

        return token_info

    def validate_sso_tokens(self, user):
        try:
            access_token, refresh_token = get_keycloak_tokens(user)

            if not access_token or not refresh_token:
                return None

            public_key = self.public_key
            decoded_access_token = jwt.decode(access_token, public_key,
                                              audience="account",
                                              algorithms=["RS256"])
        except jwt.exceptions.ExpiredSignatureError:
            msg = 'Token is expired.'
            try:
                self.refresh_toekn(user, refresh_token)
            except Exception as e:
                return None

        return User.objects.get(pk=user)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
