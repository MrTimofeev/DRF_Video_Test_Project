from django.db import models


class Video(models.Model):
    owner = models.ForeignKey("users.AppUser", on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    total_likes = models.IntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class VideoFile(models.Model):
    QUANTITY_CHOICES = [
        ("HD", "720p"),
        ("FHD", "1080p"),
        ("UHD", "4k"),
    ]

    video = models.ForeignKey("videos.Video", on_delete=models.CASCADE)
    file = models.FileField(blank=True, null=True)
    quantity = models.CharField(
        max_length=3, 
        choices=QUANTITY_CHOICES, 
        default='HD'
    )

    def __str__(self):
        return f"{self.video}_{self.quantity}"


class Like(models.Model):
    video = models.ForeignKey("videos.Video", on_delete=models.CASCADE)
    user = models.ForeignKey("users.AppUser", on_delete=models.CASCADE)
