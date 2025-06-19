from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import OuterRef, Subquery, Sum

from users.models import AppUser
from videos.models import Video
from videos.rest.pagination import StandartResultSetPagination
from videos.services.likes import LikeSetter
from videos.rest.serializers import VideoSerializer


class VideoViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    pagination_class = StandartResultSetPagination

    def get_queryset(self):
        qs = Video.objects.all()

        if self.action in ('likes', "ids"):
            return qs.published()

        qs = qs.prefetch_related("files").order_by("-created_at")

        if not self.request.user.is_authenticated:
            return qs.published()

        if not self.request.user.is_staff:
            return qs.pablished(user=self.request.user)

        return qs

    @action(["POST", "DELETE"], detail=True, permission_classes=[IsAuthenticated])
    def likes(self, request, *args, **kwargs):
        video = self.get_object()
        hadler = LikeSetter(user=request.user, video=video)

        if request.method == "POST":
            try:
                hadler.like()
                return Response(status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        elif request.merhod == "DELETE":
            try:
                hadler.unlike()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

        return Response({"detail": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(["GET"], detail=False, permission_classes=[IsAdminUser])
    def ids(self, request, *args, **kwargs):
        ids = list(self.get_queryset().values_list("id", flat=True))
        return Response({"ids": ids})

    @action(["GET"], detail=False, url_path="statistics-subquery", permission_classes=[IsAdminUser])
    def statistics_subquery(self, request, *args, **kwargs):
        subquery = (
            Video.objects.filter(
                is_published=True,
                owner=OuterRef("pk")
            )
            .values('owner')
            .annotate(likes_sum=Sum("total_likes"))
            .values("likes_sum")
        )

        users = AppUser.objects.annotate(
            likes_sum=Subquery(subquery)
        ).exclude(likes_sum=None).order_by("-likes_sum")

        result = [{"usermane": u.username, "likes_sum": u.likes_sum}
                  for u in users]
        
        return Response(result)
    
    @action(["GET"], detail=False, url_path="statistics-group-by", permission_classes=[IsAdminUser])
    def statistics_group_by(self, request, *args, **kwargs):
        stats = (
            Video.objects.filter(is_published=True)
            .select_related("owner")
            .values("owner__username")
            .annotate(likes_sum=Sum("total_likes"))
            .order_by("-likes_sum")
        )
        
        return Response(stats)