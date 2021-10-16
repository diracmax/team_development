from django.db import models
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit
from accounts.models import CustomUser
from django.utils import timezone
from dm.models import ThreadModel


class Category(models.Model):
    display = models.CharField(max_length=10, verbose_name='カテゴリー')
    parent = models.ForeignKey("self", verbose_name='親カテゴリー', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        name = self.display
        current = self.parent
        while current:
            name = current.display+" > "+name
            current = current.parent
        return name
    
    class Meta:
        unique_together = ("display", "parent")

def get_deleted_category():
    return Category.objects.get_or_create(display="その他")[0]
        
class Post(models.Model):
    author = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True)
    # category = models.ForeignKey('Category',default=get_deleted_category() on_delete=models.SET(get_deleted_category()), blank=True, null=True)
    title = models.CharField(verbose_name='タイトル', max_length=128)
    text = models.TextField(verbose_name='本文')
    photo = models.ImageField(
        verbose_name='写真', upload_to='images/', default="images/default.jpeg")
    post_photo = ImageSpecField(source='photo', processors=[ResizeToFit(
        1080, 1080)], format='JPEG', options={'quality': 60})
    recruitment_conditions = models.TextField(
        verbose_name='募集条件', blank=True, null=True)
    capacity = models.PositiveIntegerField(
        verbose_name='定員', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
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
