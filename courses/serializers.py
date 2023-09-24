from rest_framework import serializers

from courses.models import (Course, Payment, Lesson, Subscription)
from courses.validators import YouTubeLinkValidator
from courses.services.payment import create_payment


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = ["id", "course_id", "title", "description", "video_url", "owner"]
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

    def create(self, validated_data):
        payment = Payment(
            user=validated_data['user'],
            amount=validated_data['amount'],
            payment_type=validated_data['payment_type'],
            payment_id=create_payment(validated_data['amount']),
        )
        payment.save()
        return payment


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Subscription"""
    class Meta:
        model = Subscription
        fields = ["user", "course"]
