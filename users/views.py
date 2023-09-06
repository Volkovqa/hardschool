from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserListSerializer, UserDetailSerializer


class UserViewSet(ModelViewSet):
    """
    Вью сет, отвечающий за обработку CRUD-запросов для модели курса - Course
    """
    serializer_class = UserListSerializer
    queryset = User.objects.all()

    def retrieve(self, request, pk=None):
        """
        Переопределил, чтобы при выводе определенного пользователя,
        кроме основной информации, выводилась история его платежей.
        При list-выводе истории нет.
        """
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)
