from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill

class CustomUser(AbstractUser):
    description = models.TextField(verbose_name='プロフィール', null=True, blank=True)
    photo = models.ImageField(verbose_name='写真', blank=True, null=True, upload_to='images/')
    thumbnail = ImageSpecField(source='photo',
                               processors=[ResizeToFill(256, 256)],
                               format='JPEG',
                               options={'quality': 60})
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    school = models.CharField(verbose_name='学校', blank=True, null=True, max_length=128)
    age = models.PositiveIntegerField(verbose_name='年齢', blank=True, null=True)
    github_id = models.CharField(blank=True, null=True, max_length=128)


    class Meta:
        verbose_name_plural = 'CustomUser'
