from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill
from django.core.validators import MaxValueValidator
from django.contrib.auth.validators import UnicodeUsernameValidator
from .validators import GithubIdValidator, check_github_id_prefix
from django_resized import ResizedImageField


class CustomUser(AbstractUser):
    username = models.CharField(
        ('username'),
        max_length=40,
        unique=True,
        help_text=(
            'Required. 40 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[UnicodeUsernameValidator()],

        error_messages={
            'unique': ("このユーザーネームはすでに使用されています。"),
        },
    )
    description = models.TextField(verbose_name='プロフィール', null=True, blank=True, max_length=400)
    # ディレクトリを images -> images/account に変更しました
    photo = ResizedImageField(verbose_name='写真', size=[200, 200], crop=['middle', 'center'], blank=True, null=True, upload_to='images/account')
    photo_middle = ImageSpecField(source='photo',
                                  processors=[ResizeToFill(150, 150)],
                                  format='JPEG',)
    photo_small = ImageSpecField(source='photo',
                                 processors=[ResizeToFill(50, 50)],
                                 format='JPEG',)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    school = models.CharField(verbose_name='学校', blank=True, null=True, max_length=50)
    # ↓自動更新されない。生年月日にして出力で制御したほうがいいのでは
    age = models.PositiveIntegerField(verbose_name='年齢', blank=True, null=True, validators=[MaxValueValidator(200)])
    github_id = models.CharField(blank=True, null=True, max_length=39, validators=[GithubIdValidator(), check_github_id_prefix])


    def get_follower(self):
        followers = Follow.objects.filter(following=self)
        return [follower.follower for follower in followers]

    def get_following(self):
        followings = Follow.objects.filter(follower=self)
        return [following.following for following in followings]

    class Meta:
        verbose_name_plural = 'CustomUser'


class Follow(models.Model):
    follower = models.ForeignKey(
        'accounts.CustomUser', on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(
        'accounts.CustomUser', on_delete=models.CASCADE, related_name='following')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        unique_together = ('follower', 'following')
