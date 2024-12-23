from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, permissions
from teachers.models import *
from teachers.serializers import *

from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout

from rest_framework import status


class SubjectViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        mixins.ListModelMixin,
        GenericViewSet
    ):
    queryset=Subject.objects.all()
    serializer_class=SubjectSerializer


class RecordViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        mixins.ListModelMixin,
        GenericViewSet
    ):
    queryset=Record.objects.all()
    serializer_class=RecordSerializer


class FileViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        mixins.ListModelMixin,
        GenericViewSet
    ):
    queryset=File.objects.all()
    serializer_class=FileSerializer


class FeedbackViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        mixins.ListModelMixin,
        GenericViewSet
    ):
    queryset=Feedback.objects.all()
    serializer_class=FeedbackSerializer


class ReviewViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        mixins.ListModelMixin,
        GenericViewSet
    ):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer


class DocumentViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        mixins.ListModelMixin,
        GenericViewSet
    ):
    queryset=Document.objects.all()
    serializer_class=DocumentSerializer


class SchoolViewSet(
        mixins.CreateModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        mixins.ListModelMixin,
        GenericViewSet
    ):
    queryset=School.objects.all()
    serializer_class=SchoolSerializer

class UserViewSet(GenericViewSet):
    queryset = CustmoUser.objects.all()

    @action(url_path="info", methods=["GET"], detail=False)
    def get_info(self, request, *args, **kwargs):
        data = {
            "is_authenticated": request.user.is_authenticated,
            "user_type": "anonymous" if not request.user.is_authenticated else "authenticated",
        }

        if request.user.is_authenticated:
            data.update({
                "username": request.user.username,
                "user_id": request.user.id,
                "fio": request.user.fio,
                "schoolID": request.user.school.id if request.user.school else None,
                "is_superuser": request.user.is_superuser,
            })
        return Response(data)

    @action(url_path="login", methods=["POST"], detail=False)
    def login(self, request, *args, **kwargs):
        username = request.data.get("user")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
        return Response({})

    @action(url_path="logout", methods=["POST"], detail=False)
    def logout(self, request, *args, **kwargs):
        logout(request)
        return Response({})

    @action(url_path="register", methods=["POST"], detail=False)
    def register(self, request, *args, **kwargs):
        serializer = CustmoUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
