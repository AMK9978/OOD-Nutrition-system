import base64

import jwt
from rest_framework import authentication, exceptions

from nutrition.models import User

PUBLIC_KEY = base64.b64decode(
    "LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlHYk1CQUdCeXFHU000OUFnRUdCU3VCQkFBakE0R0dBQVFBdmRrYTFzcTBRd2h0QStieDFBVHVTSUEzT2oxOQpYMk0rVExzZDF3SlBGbTI0U05OUXFUWFBidFFLamhFemhsK2ZDNWExZ2ttRzNpaTJBcWt6MnRaTWUzVUFDb3JSCm1QZXh5blR0cFFSQWFKalhDOGpkRXNDU3UvMlMrblpBMmdBc25uNDBRQWxzaEpBZHMybmRYd1FBSjk5T2tXeTUKcEduRkQ2M042Vy84ODlZQW9acz0KLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0t")


class Authentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        user_token = str(request.headers.get('Authorization')).split(" ")[1]
        decoded_token = jwt.decode(user_token, PUBLIC_KEY, algorithms='ES512', options={"verify_signature": False})
        print(decoded_token)
        print(decoded_token['username'])
        if not decoded_token["username"]:
            return None
        try:
            user = User.objects.get(username=decoded_token["username"])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return user, None
