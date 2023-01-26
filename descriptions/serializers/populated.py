from .common import DescriptionSerializer
from jwt_auth.serializers.common import UserSerializer

class PopulatedDescriptionSerializer(DescriptionSerializer):
  owner = UserSerializer()