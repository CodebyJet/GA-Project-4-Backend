from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.db import IntegrityError

from .models import Description
from .serializers.common import DescriptionSerializer
from .serializers.populated import PopulatedDescriptionSerializer


class DescriptionListView(APIView):
    def get(self, _request):
        descriptions = Description.objects.all()
        serialized_descriptions = DescriptionSerializer(descriptions, many=True)
        return Response(serialized_descriptions.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data['owner'] = request.user.id
        description_to_add = DescriptionSerializer(data=request.data)
        try:
            description_to_add.is_valid()
            description_to_add.save()
            return Response(description_to_add.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            res = {
                "detail": str(e)
            }
            return Response(res, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except AssertionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({"detail": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class DescriptionDetailView(APIView):  

    def get_description(self, pk):
        try:
            return Description.objects.get(pk=pk)
        except Description.DoesNotExist:
            raise NotFound(detail="Can't find it babes, soz")

    def get(self, _request, pk):
        description = self.get_description(pk=pk)
        serialized_description = PopulatedDescriptionSerializer(description)
        return Response(serialized_description.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        description_to_edit = self.get_description(pk=pk)
        updated_description = DescriptionSerializer(description_to_edit, data=request.data)
        try:
            updated_description.is_valid()
            updated_description.save()
            return Response(updated_description.data, status=status.HTTP_202_ACCEPTED)
        except AssertionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response({"detail": "Unprocessable Entity"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, _request, pk):
        description_to_delete = self.get_description(pk=pk)
        description_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
