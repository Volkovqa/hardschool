from rest_framework.generics import DestroyAPIView, UpdateAPIView, CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.viewsets import ModelViewSet

from courses.models import Course, Lesson
from courses.serializers import CourseSerializer, LessonSerializer


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
