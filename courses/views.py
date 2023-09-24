from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import DestroyAPIView, UpdateAPIView, CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter

from courses.models import Course, Lesson, Payment
from courses.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer

from courses.services.permissions import IsOwner, IsStaff

from courses.paginators import CoursePaginator, LessonsPaginator
from courses.tasks import _send_email


class CourseViewSet(ModelViewSet):
    """
    Вью сет, отвечающий за обработку CRUD-запросов для модели курса - Course
    """
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursePaginator

    def get_permissions(self):
        """Права доступа"""
        if self.action == 'retrive':
            permission_classes = [IsOwner | IsStaff]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated | IsStaff]
        elif self.action == 'destroy':
            permission_classes = [IsOwner | IsStaff]
        elif self.action == 'update':
            permission_classes = [IsOwner | IsStaff]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        updated_course = serializer.save()
        _send_email.delay(updated_course.pk)


class LessonListView(ListAPIView):
    """
    Класс-контроллер на основе дженерика для CRUD для модели урока Lesson
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonsPaginator
    permission_classes = [IsOwner | IsStaff]


class LessonDetailView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwner | IsStaff]


class LessonCreateView(CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated | IsStaff]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonUpdateView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwner | IsStaff]


class LessonDeleteView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsOwner]


class PaymentListView(ListAPIView):
    """
    Класс-контроллер на основе дженерика для модели Payment
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)

    # сортировка
    ordering_fields = ('date',)

    # фильтрация по полям
    filterset_fields = ('course', 'lesson', 'payment_type')


class PaymentCreateView(CreateAPIView):
    """Создание платежа"""
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        """Сохраняет пользователя и курс"""
        new_payment = serializer.save()
        new_payment.user = self.request.user
        new_payment.course = Course.objects.get(pk=self.kwargs.get('pk'))
        new_payment.save()


class PaymentRetrieveView(RetrieveAPIView):
    serializer_class = PaymentSerializer

    def get_object(self):
        object = Payment.objects.get(
            user=self.request.user,
            paid_course=Course.objects.get(pk=self.kwargs.get('pk'))
        )
        return object


class SubscriptionListAPIView(ListAPIView):
    serializer_class = SubscriptionSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner, IsStaff]


class SubscriptionCreateAPIView(CreateAPIView):
    """Создание подписки"""
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer):
        new_subscribe = serializer.save()
        new_subscribe.user = self.request.user
        new_subscribe.save()


class SubscriptionDeleteAPIView(DestroyAPIView):
    """Удаление подписки"""
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner, IsStaff]
