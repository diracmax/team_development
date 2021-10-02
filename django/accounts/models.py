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

    def get_follower(self):
        followers = Follow.objects.filter(following=self)
        return [follower.follower for follower in followers]


    class Meta:
        verbose_name_plural = 'CustomUser'


class Follow(models.Model):
    follower = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='following')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)


    class Meta:
    	unique_together = ('follower', 'following')
