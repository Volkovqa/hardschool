from rest_framework import serializers

from courses.models import (Course, Payment, Lesson, Subscription)
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
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'lessons_count', 'lessons', 'is_subscribed']

    def get_lessons_count(self, obj):
        return obj.lesson_set.all().count()

    def get_is_subscribed(self, instance):
        """Проверка подписки"""
        request = self.context.get('request')
        subscription = Subscription.objects.filter(course=instance.pk, user=request.user).exists()
        if subscription:
            return True
        return False


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["user", "date", "course", "lesson", "amount", "payment_type"]


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Subscription"""
    class Meta:
        model = Subscription
        fields = ["user", "course"]
