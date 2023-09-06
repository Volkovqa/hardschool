from rest_framework.serializers import ModelSerializer

from courses.serializers import PaymentSerializer
from users.models import User


class UserListSerializer(ModelSerializer):
    """
    Вывод списка пользователей с их основными полями
    """

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "phone_number", "location", "is_active"]


class UserDetailSerializer(ModelSerializer):
    """
    Детальный вывод одного пользователя. Кроме основных, есть вложенное поле истории платежей
    """
    payments = PaymentSerializer(source='payment_set', many=True)

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "phone_number", "location", "is_active", "payments"]

