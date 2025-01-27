from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins, permissions
from teachers.models import *
from teachers.serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters import rest_framework as dj_filters
from rest_framework import status
from rest_framework.renderers import JSONRenderer


class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000


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
    pagination_class = CustomPagination
    filter_backends = [filters.OrderingFilter,filters.SearchFilter,dj_filters.DjangoFilterBackend]
    ordering_fields = ['time']
    search_fields = ['headline','comment']
    filterset_fields = ['is_published','subject','author']
    def update(self, request, *args, **kwargs): 
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True) 
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

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
    filter_backends = [dj_filters.DjangoFilterBackend]
    filterset_fields = ['records_FK']

    def update(self, request, *args, **kwargs): 
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True) 
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
            serializer.save()
    
    def perform_create(self, serializer):
        serializer.save(moderator=self.request.user)


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
    pagination_class = CustomPagination
    filter_backends = [dj_filters.DjangoFilterBackend] # добавляем фильтрацию
    filterset_fields = ['records_FK'] # добавляем фильтрацию по полю records_FK
    

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


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
    pagination_class = CustomPagination
    filter_backends = [filters.OrderingFilter,filters.SearchFilter]
    ordering_fields=['time']
    search_fields = ['headline','description']
    


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
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class UserViewSet(GenericViewSet):
    queryset = CustmoUser.objects.all()
    permission_classes = [
        permissions.AllowAny 
    ]
    serializer_class = CustmoUserSerializer

    @action(url_path="info", methods=["GET"], detail=False)
    def get_info(self, request, *args, **kwargs):
        data = {
            "is_authenticated": request.user.is_authenticated
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
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

    @action(url_path="register", methods=["POST"], detail=False)
    def register(self, request, *args, **kwargs):
        serializer = CustmoUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)