from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    """
    Вью сет, отвечающий за обработку CRUD-запросов для модели курса - Course
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
