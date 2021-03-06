from rest_framework import exceptions
from rest_framework.authentication import (
    get_authorization_header,
    BaseAuthentication,
)
from api.models import Token, IPBinding
from django.utils.translation import ugettext_lazy as _


class TokenIPAuth(BaseAuthentication):
    keyword = 'Token'

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            key = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)
        ip = request.META.get('REMOTE_ADDR')

        return self.authenticate_credentials(key, ip)

    @staticmethod
    def authenticate_credentials(key, ip):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            msg = _('Invalid token.')
            raise exceptions.AuthenticationFailed(msg)
        if token.ip_restricted and token.ip_set.filter(ip=ip).count() == 0:
            msg = _('token does not match this ip')
            raise exceptions.AuthenticationFailed(msg)
        return None, token

    def authenticate_header(self, request):
        return self.keyword
