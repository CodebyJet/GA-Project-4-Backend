from .common import MailSerializer
from jwt_auth.serializers.common import UserSerializer


class PopulatedMailSerializer(MailSerializer):
  owner = UserSerializer()
  receiver = UserSerializer()
