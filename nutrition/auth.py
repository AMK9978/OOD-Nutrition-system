from rest_framework import authentication, exceptions
from rest_framework_jwt.utils import jwt_decode_handler

from nutrition.models import User


class Authentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        body = jwt_decode_handler(str(request.headers.get('Authorization')).split(" ")[1])
        username = body['username']
        if not username:
            return None
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return user, None
