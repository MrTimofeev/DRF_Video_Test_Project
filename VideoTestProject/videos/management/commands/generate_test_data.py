import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from videos.models import Video, VideoFile
from django.db import transaction

User = get_user_model()

class Command(BaseCommand):
    help = "Генерирует 100 000 видео для 10 000 пользователей (быстро)"

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=10_000)
        parser.add_argument('--videos-per-user', type=int, default=10)

    def handle(self, *args, **options):
        total_users = options['users']
        videos_per_user = options['videos_per_user']

        self.stdout.write(f"Создаю {total_users} пользователей...")

        # Создаем пользователей за один запрос
        users = []
        for i in range(total_users):
            user, created = User.objects.get_or_create(
                username=f"user_{i}",
                defaults={"email": f"user_{i}@example.com"}
            )
            if created:
                user.set_unusable_password()
                users.append(user)

        # Если пользователи уже существуют — просто получаем их
        if len(users) == 0:
            users = list(User.objects.filter(username__startswith="user_")[:total_users])

        self.stdout.write(f"Найдено или создано {len(users)} пользователей")

        # Генерируем видео
        self.stdout.write(f"Создаю {len(users) * videos_per_user} видео...")

        videos_to_create = []
        for user in users:
            for j in range(videos_per_user):
                videos_to_create.append(
                    Video(
                        owner=user,
                        name=f"Видео {j} от {user.username}",
                        is_published=random.choice([True, False]),
                        total_likes=random.randint(0, 100),
                    )
                )

        with transaction.atomic():
            Video.objects.bulk_create(videos_to_create, batch_size=1000)

        self.stdout.write(f"Создано {len(videos_to_create)} видео")

        # Добавляем файлы к первым N видео
        sample_videos = Video.objects.all().order_by('?')[:5000]
        video_files = []

        qualities = ['HD', 'FHD', 'UHD']

        for video in sample_videos:
            for quality in qualities:
                video_files.append(
                    VideoFile(
                        video=video,
                        file=f"videos/{video.id}_{quality}.mp4",
                        quantity=quality
                    )
                )

        with transaction.atomic():
            VideoFile.objects.bulk_create(video_files, batch_size=1000)

        self.stdout.write(f"Добавлено {len(video_files)} видеофайлов")

        self.stdout.write(self.style.SUCCESS("✅ Тестовые данные успешно созданы"))