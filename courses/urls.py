from django.urls import path
from rest_framework.routers import DefaultRouter
from courses.apps import CoursesConfig
from courses.views import CourseViewSet, LessonListView, LessonDetailView, LessonCreateView, LessonUpdateView, \
    LessonDeleteView

app_name = CoursesConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lessons/list/', LessonListView.as_view(), name='lessons_list'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lessons_detail'),
    path('lessons/create/', LessonCreateView.as_view(), name='lessons_create'),
    path('lessons/<int:pk>/update/', LessonUpdateView.as_view(), name='lessons_update'),
    path('lessons/<int:pk>/delete/', LessonDeleteView.as_view(), name='lessons_delete'),
] + router.urls
