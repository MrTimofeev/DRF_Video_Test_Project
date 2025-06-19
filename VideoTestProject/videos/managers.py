from django.db import models


class VideoQuerySet(models.QuerySet):
    def published(self, user=None):
        queryset = self.filter(is_published=True)
        if user:
            queryset |= self.filter(owner=user)
        return queryset.distinct()
    
class VideoManager(models.Manager):
    def get_queryset(self):
        return VideoQuerySet(self.model, using=self._db)
    
    def published(self, user=None):
        return self.get_queryset().published(user)
