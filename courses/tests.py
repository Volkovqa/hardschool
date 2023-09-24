from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Lesson, Course, Subscription, Payment
from users.models import User


class LessonTestCase(APITestCase):
    def create_user(self):
        """Создание пользователя"""
        self.user = User.objects.create(
            email='test@test.com',
            is_staff=False,
            is_active=True,
        )
        self.user.set_password('1234')
        self.user.save()

    def setUp(self) -> None:
        """Подготовка данных"""
        self.create_user()

        self.course = Course.objects.create(
            title='course test',
            description='list test description',
            owner=self.user
        )

        self.lesson = Lesson.objects.create(
            title='list test',
            description='list test description',
            owner=self.user
        )

    def test_list_lesson(self):
        """Тестирование вывода списка уроков"""

        response = self.client.get(
            reverse('courses:lessons_list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'count': 1, 'next': None, 'previous': None, 'results': [
                {'id': 4, 'course_id': None, 'title': 'list test', 'description': 'list test description',
                 'video_url': None, 'owner': 3}]}
        )

    def test_create_lesson(self):
        """Тестирование создания уроков"""
        self.client.force_authenticate(self.user)

        data = {
            'title': 'test',
            'description': 'test description',
            'course': self.course.title
        }

        response = self.client.post(
            reverse('courses:lessons_create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Lesson.objects.count(),
            2
        )

    def test_update_lesson(self):
        """Тестирование обновления"""
        self.client.force_authenticate(self.user)
        data = {
            'title': 'test lesson updated',
        }

        response = self.client.patch(
            reverse("courses:lessons_update", kwargs={'pk': self.lesson.id}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        # Check updated name

        self.assertEqual(
            Lesson.objects.get(pk=self.lesson.id).title,
            'test lesson updated'
        )

    def test_delete_lesson(self):
        """Тестирование удаления урока"""
        self.client.force_authenticate(self.user)
        response = self.client.delete(
            reverse("courses:lessons_delete", kwargs={'pk': self.lesson.id})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        # Check that no lesson exists in Database
        self.assertFalse(
            Lesson.objects.exists()
        )


class SetupTestCase(APITestCase):
    def setUp(self):
        self.user = User(email='test@test.ru', is_superuser=True, is_staff=True, is_active=True)
        self.user.set_password('123QWE456RTY')
        self.user.save()

        response = self.client.post(
            '/api/token/',
            {"email": "test@test.ru", "password": "123QWE456RTY"}
        ).json()

        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')


class SubscribeTestCase(SetupTestCase):
    def setUp(self):
        super().setUp()

        self.course = Course.objects.create(
            name='Test course',
            description='Test description',
            price=100
        )

    def test_subscription_create(self):
        payment = Payment.objects.create(amount=100, user=self.user)
        data = {
            'course': self.course.id,
            'user': self.user.id,
            'payment': payment.id
        }

        response = self.client.post('/courses/subscriptions/create/', data)
        self.assertEqual(response.status_code, 201)

        subscription = Subscription.objects.get(id=response.data['id'])
        self.assertEqual(subscription.course, self.course)
        self.assertEqual(subscription.user, self.user)
        self.assertEqual(subscription.payment, payment)
        self.assertFalse(subscription.status)

    def test_subscription_delete(self):
        subscription = Subscription.objects.create(
            course=self.course,
            user=self.user,
            payment=Payments.objects.create(user=self.user, payment_amount=100)
        )

        url = f'/courses/subscriptions/delete/{subscription.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

        with self.assertRaises(ObjectDoesNotExist):
            Subscription.objects.get(id=subscription.id)
