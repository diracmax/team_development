from django.db import models
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit
from accounts.models import CustomUser
from django.utils import timezone
from dm.models import ThreadModel
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

class Category(models.Model):
    display = models.CharField(max_length=10, verbose_name='カテゴリー')
    parent = models.ForeignKey("self", verbose_name='親カテゴリー', on_delete=models.CASCADE, blank=True, null=True, limit_choices_to={"depth__lt": 3})
    depth = models.IntegerField(default=0, verbose_name='世代', help_text=('先祖の数を手動で入力してください'),)
    default_img = models.ImageField(
        verbose_name='デフォルト画像', upload_to='images/default', default="images/default/default.jpeg")
    post_photo = ImageSpecField(source='default_img', processors=[ResizeToFit(
        1080, 1080)], format='JPEG', options={'quality': 60})

    def __str__(self):
        # 親カテゴリ名をさかのぼって表示
        name = self.display
        current = self.parent
        while current:
            name = current.display+" > "+name
            current = current.parent
        return name
    
    class Meta:
        # 同じカテゴリ名は親が違う場合には許す
        unique_together = ("display", "parent")

# def get_deleted_category():
#     # 親カテゴリーを返し、無かったらその他を返すようにしたい
#     return Category.objects.get_or_create(display="その他")[0]
        
class Post(models.Model):
    author = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    # category = models.ForeignKey('Category',default=get_deleted_category() on_delete=models.SET(get_deleted_category()), blank=True, null=True)
    title = models.CharField(verbose_name='タイトル', max_length=128)
    text = models.TextField(verbose_name='本文')
    photo = models.ImageField(
        verbose_name='写真', upload_to='images/', null=True, blank=True)
    post_photo = ImageSpecField(source='photo', processors=[ResizeToFit(
        1080, 1080)], format='JPEG', options={'quality': 60})
    restriction = models.TextField(
        verbose_name='応募条件', blank=True, null=True)
    # deadline = models.DateField(
    #     verbose_name='応募期限', blank=True, null=True)
    capacity = models.PositiveIntegerField(
        verbose_name='定員', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    # state_control_type = models.CharField(max_length=10, verbose_name='募集ステータス', default="auto", choices=[("auto","自動的に更新"),("open","強制的にオープン"),("close","強制的にクローズ")])
    is_recruited = models.BooleanField(verbose_name='募集中', default=True)

    def get_member(self):
        members = Apply.objects.filter(post=self)
        return [member.user for member in members if member.is_member == True]

    def get_apply_number(self):
        return len(self.get_applicant()) + len(self.get_member())

    def get_comment(self):
        comments = Comment.objects.filter(post=self).order_by('-created_at')
        return [comment for comment in comments]

    def get_like(self):
        likes = Like.objects.filter(post=self)
        return [like.user for like in likes]

    def get_applicant(self):
        members = Apply.objects.filter(post=self)
        return [member.user for member in members if member.is_member == False]

    # def is_applyable(self):
    #     """
    #     deadline_flag: 締切り過ぎている場合のみFalse
    #     capacity_flag: 定員満たしている場合のみFalse
    #     """
    #     if self.state_control_type=="open":
    #         return True
    #     if self.state_control_type=="close":
    #         return False
    #     deadliine_flag = not self.deadline or (self.deadline <= datetime.date.today())
    #     capacity_flag = not self.capacity or (int(self.capacity) > len(self.get_member())) 
    #     return deadliine_flag and capacity_flag
        

class Like(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        unique_together = ('user', 'post')


class Apply(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    is_member = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'post')


class Comment(models.Model):
    author = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    text = models.TextField(verbose_name='コメント')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)


class Notification(models.Model):
    # 1 = Like, 2 = Comment, 3 = Follow, 4 = Apply, 5 = Message
    notification_type = models.IntegerField(null=True, blank=True)
    to_user = models.ForeignKey(
        CustomUser, related_name='notification_to', on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(
        CustomUser, related_name='notification_from', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(
        'Post', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    comment = models.ForeignKey(
        'Comment', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    thread = models.ForeignKey(
        ThreadModel, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    user_has_seen = models.BooleanField(default=False)


class CommentReply(models.Model):
    author = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'Comment', verbose_name='親コメント', on_delete=models.CASCADE, related_name='parent_comment')
    text = models.TextField(verbose_name='コメント')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
