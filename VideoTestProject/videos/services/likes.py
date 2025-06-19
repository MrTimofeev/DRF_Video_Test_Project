from django.db import transaction
from django.db.models import F
from videos.models import Like


class LikeSetter:
    def __init__(self, user, video):
        self.user = user
        self.video = video

    @transaction.atomic
    def like(self):
        like, created = self.video.like_set.select_for_update().get_or_create(
            video=self.video,
            user=self.user
        )

        if not created:
            raise Exception("Лайк уже поставлен")

        self.video.total_likes = F('total_likes') + 1
        self.video.save(update_fields=["total_likes"])

    @transaction.atomic
    def unlike(self):
        try:
            like = self.video.like_set.select_for_update().get(
                video=self.video,
                user=self.user
            )
            like.delete()
            self.video.total_likes = F('total_likes') - 1
            self.video.save(update_fields=["total_likes"])
        except Like.DoesNotExist:
            raise Exception("Лайк не найден")
            
