from .common import QuizSerializer
from jwt_auth.serializers.common import UserSerializer

class PopulatedQuizSerializer(QuizSerializer):
  owner = UserSerializer()