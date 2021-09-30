from django.db import models
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit

class Post(models.Model):
	author = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
	text = models.TextField(verbose_name='本文')
	photo = models.ImageField(verbose_name='写真', upload_to='images/', default="images/default.jpeg")
	post_photo = ImageSpecField(source='photo',processors=[ResizeToFit(1080, 1080)],format='JPEG',options={'quality':60})
	created_at = models.DateTimeField(auto_now_add=True, blank=True)
	is_recruited = models.BooleanField(verbose_name='募集中', default=True)

	def get_like(self):
		likes = Like.objects.filter(post=self)
		return [like.user for like in likes]

	def get_applicant(self):
		members = Apply.objects.filter(post=self)
		return [member.user for member in members if member.is_member == False]

	def get_member(self):
		members = Apply.objects.filter(post=self)
		return [member.user for member in members if member.is_member == True]

	def get_apply_number(self):
		return len(self.get_applicant()) + len(self.get_member())

class Like(models.Model):
	user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
	post = models.ForeignKey('Post', on_delete=models.CASCADE)

	class Meta:
		unique_together = ('user', 'post')

class Apply(models.Model):
	user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
	post = models.ForeignKey('Post', on_delete=models.CASCADE)
	is_member = models.BooleanField(default=False)

	class Meta:
		unique_together = ('user', 'post')