from rest_framework import serializers

from courses.models import Course
from courses.models import Lesson


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = ["id", "course_id", "title", "description", "video_url"]


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(source='lesson_set', many=True)
    lessons_count = serializers.SerializerMethodField(read_only=True)

    def get_lessons_count(self, obj):
        return obj.lesson_set.all().count()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'lessons_count', 'lessons']
