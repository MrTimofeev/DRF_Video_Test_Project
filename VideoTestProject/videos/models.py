from django.db import models
from videos.managers import VideoManager
from users.models import AppUser


class Video(models.Model):
    owner = models.ForeignKey("users.AppUser", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    is_published = models.BooleanField(default=False)
    total_likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = VideoManager()
    
    def __str__(self):
        return self.name


class VideoFile(models.Model):
    QUANTITY_CHOICES = [
        ("HD", "720p"),
        ("FHD", "1080p"),
        ("UHD", "4k"),
    ]

    video = models.ForeignKey("videos.Video", on_delete=models.CASCADE, related_name="files")
    file = models.FileField(blank=True, null=True, upload_to='videos/')
    quantity = models.CharField(
        max_length=3, 
        choices=QUANTITY_CHOICES, 
        default='HD'
    )

    def __str__(self):
        return f"{self.video.name} - {self.get_quantity_display()}"


class Like(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)

    class Meta: 
        unique_together = ('video', 'user')
        