from rest_framework import serializers

from courses.models import Course, Payment
from courses.models import Lesson
from courses.validators import YouTubeLinkValidator


class LessonSerializer(serializers.ModelSerializer):
    description = serializers.CharField()
    video_url = serializers.URLField()

    class Meta:
        model = Lesson
        fields = ["id", "course_id", "title", "description", "video_url"]
        validators = [YouTubeLinkValidator(field='video_url')]


class CourseSerializer(serializers.ModelSerializer):
    description = serializers.CharField()

    lessons = LessonSerializer(source='lesson_set', many=True)
    lessons_count = serializers.SerializerMethodField(read_only=True)

    def get_lessons_count(self, obj):
        return obj.lesson_set.all().count()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'lessons_count', 'lessons']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["user", "date", "course", "lesson", "amount", "payment_type"]
