from rest_framework import serializers

from courses.models import Course
from courses.models import Lesson


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField(read_only=True)

    def get_lessons_count(self, obj):
        return obj.lesson_set.all().count()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'lessons_count']
        # fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"
