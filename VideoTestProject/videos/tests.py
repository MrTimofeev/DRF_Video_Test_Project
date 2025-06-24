from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from videos.models import Video, Like
from users.models import AppUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from django.test import RequestFactory


class VideoApiTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = AppUser.objects.create_user(username="testuser", password="12345")
        self.video = Video.objects.create(
            name="Test Video",
            owner=self.user,
            is_published=True,
            total_likes=0
        )
        
    def test_get_video_list(self):
        client = APIClient()
        url = reverse('video-list')
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
    def test_like_video_requires_authentication(self):
        url = reverse('video-likes', kwargs={'pk': self.video.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_authenticated_user_can_like_video(self):
        self.client.force_authenticate(user=self.user)  
        url = reverse('video-likes', kwargs={'pk': self.video.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.video.refresh_from_db()
        self.assertEqual(self.video.total_likes, 1)
        
    def test_authenticated_user_cannot_like_video_twice(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('video-likes', kwargs={'pk': self.video.pk})

        # Первый лайк
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Обновляем данные видео и проверяем наличие лайка
        self.video.refresh_from_db()
        self.assertEqual(self.video.total_likes, 1)
        self.assertTrue(Like.objects.filter(video=self.video, user=self.user).exists())

        # Вторая попытка лайка
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'Лайк уже поставлен')

        # Проверяем, что количество лайков не изменилось
        self.video.refresh_from_db()
        self.assertEqual(self.video.total_likes, 1)
        
        
    def test_authenticated_user_can_unlike_video(self):
        self.client.force_authenticate(user=self.user)  
        url = reverse('video-likes', kwargs={'pk': self.video.pk})
        
        # Ставим лайк
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем
        self.video.refresh_from_db()
        self.assertEqual(self.video.total_likes, 1)
        self.assertTrue(Like.objects.filter(video=self.video, user=self.user).exists())
        
        # Убираем лайк
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Проверяем, что лайк удален
        self.video.refresh_from_db()
        self.assertEqual(self.video.total_likes, 0)
        self.assertFalse(Like.objects.filter(video=self.video, user=self.user).exists())
        
        