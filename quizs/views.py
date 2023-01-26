from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.db import IntegrityError

from .models import Quiz
from .serializers.common import QuizSerializer
from .serializers.populated import PopulatedQuizSerializer


class QuizListView(APIView):
    def get(self, request):
        quizs = Quiz.objects.all()
        serialized_quizs = QuizSerializer(
            quizs, many=True)
        return Response(serialized_quizs.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data['owner'] = request.user.id
        quiz_to_add = QuizSerializer(data=request.data)
        try:
            quiz_to_add.is_valid()
            quiz_to_add.save()
            return Response(quiz_to_add.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            res = {
                "detail": str(e)
            }
            return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except AssertionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({"detail": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class QuizDetailView(APIView):

    def get_quiz(self, pk):
        try:
            return Quiz.objects.get(pk=pk)
        except Quiz.DoesNotExist:
            raise NotFound(detail="Can't find it babes, soz")

    def get(self, _request, pk):
        quiz = self.get_quiz(pk=pk)
        serialized_quiz = PopulatedQuizSerializer(quiz)
        return Response(serialized_quiz.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        quiz_to_edit = self.get_quiz(pk=pk)
        updated_quiz = QuizSerializer(
            quiz_to_edit, data=request.data)
        try:
            updated_quiz.is_valid()
            updated_quiz.save()
            return Response(updated_quiz.data, status=status.HTTP_202_ACCEPTED)
        except AssertionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({"detail": "Unprocessable Entity"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, _request, pk):
        quiz_to_delete = self.get_quiz(pk=pk)
        quiz_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
