from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import DestroyAPIView, UpdateAPIView, CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter

from courses.models import Course, Lesson, Payment
from courses.serializers import CourseSerializer, LessonSerializer, PaymentSerializer


class CourseViewSet(ModelViewSet):
    """
    Вью сет, отвечающий за обработку CRUD-запросов для модели курса - Course
    """
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class LessonListView(ListAPIView):
    """
    Класс-контроллер на основе дженерика для CRUD для модели урока Lesson
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDetailView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonCreateView(CreateAPIView):
    serializer_class = LessonSerializer


class LessonUpdateView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDeleteView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class PaymentListView(ListAPIView):
    """
    Класс-контроллер на основе дженерика для модели Payment
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('date',)
    filterset_fields = ('course', 'lesson', 'payment_type')
