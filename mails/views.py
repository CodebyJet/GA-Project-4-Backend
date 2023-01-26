from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from .serializers.common import MailSerializer
from .serializers.populated import PopulatedMailSerializer
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .models import Mail


class MailListView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        mailsFromMe = Mail.objects.filter(
            Q(receiver=request.user.id) | Q(owner=request.user.id)).order_by("created_at")
        serialized_mails = MailSerializer(mailsFromMe, many=True)
        return Response(serialized_mails.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data['owner'] = request.user.id
        print(request.data)
        mail_to_create = MailSerializer(data=request.data)
        try:
            mail_to_create.is_valid()
            mail_to_create.save()
            return Response(mail_to_create.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response({
                "detail": str(e),
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except AssertionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            return Response("Unprocessable Entity", status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class MailDetailView(APIView):
    permission_classes = (IsAuthenticated, )

    def get_mail(self, pk):
        try:
            return Mail.objects.get(pk=pk)
        except Mail.DoesNotExist:
            raise NotFound(detail="Can't find that mail!")

    def get(self, _request, pk):
        mail = self.get_mail(pk=pk)
        serialized_mail = PopulatedMailSerializer(mail)
        return Response(serialized_mail.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        mail_to_edit = self.get_mail(pk=pk)
        if mail_to_edit.owner != request.user:
            raise PermissionDenied()

        updated_mail = MailSerializer(mail_to_edit, data=request.data)
        try:
            updated_mail.is_valid()
            updated_mail.save()
            return Response(updated_mail.data, status=status.HTTP_202_ACCEPTED)

        except AssertionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        except:
            return Response({"detail": "Unprocessable Entity"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request, pk):
        try:
            mail_to_delete = self.get_mail(pk=pk)
            if mail_to_delete.owner != request.user:
                raise PermissionDenied()

            mail_to_delete.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Mail.DoesNotExist:
            raise NotFound(detail="Message not found")
