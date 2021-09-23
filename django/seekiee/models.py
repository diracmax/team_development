from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Categories(models.Model):
	title = models.CharField(verbose_name='カテゴリ', max_length=20)

	def __str__(self):
		return self.title


class Posts(models.Model):
	user = models.ForeignKey(CustomUser, verbose_name='ユーザー', on_delete=models.CASCADE)
	category = models.ForeignKey(Categories, verbose_name='カテゴリ' ,on_delete=models.PROTECT)
	title = models.CharField(verbose_name='タイトル', max_length=200)
	comment = models.TextField(verbose_name='コメント')
	image = models.ImageField(verbose_name='イメージ', upload_to = 'post_image')
	posted_at = models.DateTimeField(verbose_name='投稿日時', auto_now_add=True)

	def __str__(self):
		return self.title