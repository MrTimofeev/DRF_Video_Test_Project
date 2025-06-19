from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from videos.rest.views import VideoViewSet

router = DefaultRouter()
router.register(r'videos', VideoViewSet, basename="video")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include(router.urls)),
]
