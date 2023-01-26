from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.conf import settings
import jwt

User = get_user_model()


class JWTAuthentication(BasicAuthentication):

    def authenticate(self, request):
        # Get the authorization header from the incoming request and save it to a variable
        auth_header = request.headers.get("Authorization")

        # Check if auth_header has a value. If it doesn't, return None.
        if not auth_header:
            return None

        if not auth_header.startswith('Bearer'):
            raise PermissionDenied(detail="Invalid Auth Token Format")

        # remove Bearer from beginning of the auth_header and leave just the token.
        token = auth_header.replace('Bearer ', '')

        # Try to get the payload from the token and make sure the user exists
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])

            user = User.objects.get(pk=payload.get('sub'))

        # if jwt.decode errors, we can catch it with this exception:
        except jwt.exceptions.InvalidTokenError:
            raise PermissionDenied(detail='User Not Found')

        # If there is no user with that sub in the db:
        except User.DoesNotExist:
            raise PermissionDenied(detail='User Not Found')

        # If everything is ok
        return (user, token)
