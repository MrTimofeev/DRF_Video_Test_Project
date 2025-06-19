from django.contrib import admin
from videos.models import Video, VideoFile


class VideoFileInLine(admin.TabularInline):
    model = VideoFile
    extra = 1 
    
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'is_published', 'total_likes', 'created_at')
    list_filter = ('is_published', 'owner')
    search_fields = ('name', 'owner__username')
    inlines = [VideoFileInLine]
    

