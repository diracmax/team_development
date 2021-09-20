from django.db import models
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit

class Post(models.Model):
	author = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
	text = models.TextField(verbose_name='本文')
	photo = models.ImageField(verbose_name='写真', blank=True, null=True, upload_to='images/')
	post_photo = ImageSpecField(source='photo',processors=[ResizeToFit(1080, 1080)],format='JPEG',options={'quality':60})
	created_at = models.DateTimeField(auto_now_add=True, blank=True)


	def get_like(self):
		likes = Like.objects.filter(post=self)
		return [like.user for like in likes]


class Like(models.Model):
	user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
	post = models.ForeignKey('Post', on_delete=models.CASCADE)

	class Meta:
		unique_together = ('user', 'post')
