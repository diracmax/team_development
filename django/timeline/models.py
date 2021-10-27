from django.db import models
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit
from accounts.models import CustomUser
from django.utils import timezone
from dm.models import ThreadModel
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django_resized import ResizedImageField
from django.core.exceptions import ValidationError

def create_default_category(sender, **kwargs):
    CATEGORIES = [
        "その他", "ハッカソン", "チーム開発", "ミートアップ", "インターン", "作業・雑談"
        ]
    for category in CATEGORIES:
        Category.objects.update_or_create(
            display=category, 
            parent=None, 
            defaults={
                "default_img": "setup/category/"+category+".jpg", "depth": 0
                }
            )


MAX_RATIO = 2.0
MIN_RATIO = 0.5
def validate_image(image):
    ratio = image.height / image.width
    if ratio > MAX_RATIO:
        raise ValidationError("画像が縦に長すぎます。")
    if ratio < MIN_RATIO:
        raise ValidationError("画像が横に長すぎます。")

class Category(models.Model):
    display = models.CharField(max_length=10, verbose_name='カテゴリー')
    parent = models.ForeignKey("self", verbose_name='親カテゴリー', related_name='children', on_delete=models.CASCADE, blank=True, null=True, limit_choices_to={"depth__lt": 3})
    depth = models.IntegerField(default=0, verbose_name='世代', help_text=('先祖の数を手動で入力してください'),)
    # ディレクトリを images -> images/default に変更しました
    default_img = ResizedImageField(verbose_name='デフォルト画像', size=[1080, 1080], blank=True, null=True, upload_to='images/default', default="images/default/default.jpeg", validators=[validate_image])
    post_photo = ImageSpecField(source='default_img', processors=[ResizeToFit(
        1080, 1080)], format='JPEG', options={'quality': 60})

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            ratio = image._height / image._width
            if ratio > MAX_RATIO:
                raise ValidationError("画像が縦に長すぎます。")
            if ratio < MIN_RATIO:
                raise ValidationError("画像が横に長すぎます。")
            return image
        else:
            raise ValidationError("No image found")

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

def get_default_category():
    # 親カテゴリーを返し、無かったらその他を返すようにしたい
    record = Category.objects.get_or_create(display="その他", depth=0)[0]
    return record.pk

class Post(models.Model):
    author = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.SET_DEFAULT, default=get_default_category)

    title = models.CharField(verbose_name='タイトル', max_length=50)
    text = models.TextField(verbose_name='本文' ,max_length=3000)

    # ディレクトリを images -> images/post に変更しました
    photo = ResizedImageField(verbose_name='写真', size=[1080, 1080], blank=True, null=True, upload_to='images/post/', validators=[validate_image])
    post_photo = ImageSpecField(source='photo', processors=[ResizeToFit(
        1080, 1080)], format='JPEG', options={'quality': 60})
    restriction = models.TextField(
        verbose_name='応募条件', blank=True, null=True ,max_length=3000)
    # deadline = models.DateField(
    #     verbose_name='応募期限', blank=True, null=True)

    # ディレクトリを images -> images/post に変更しました
    capacity = models.PositiveIntegerField(
        verbose_name='定員', blank=True, null=True, validators=[MaxValueValidator(100)])
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    # state_control_type = models.CharField(max_length=10, verbose_name='募集ステータス', default="auto", choices=[("auto","自動的に更新"),("open","強制的にオープン"),("close","強制的にクローズ")])
    is_recruited = models.BooleanField(verbose_name='募集中', default=True)

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            ratio = image._height / image._width
            if ratio > MAX_RATIO:
                raise ValidationError("画像が縦に長すぎます。")
            if ratio < MIN_RATIO:
                raise ValidationError("画像が横に長すぎます。")
            return image
        else:
            raise ValidationError("画像が見つかりません。")

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
    text = models.TextField(verbose_name='コメント', max_length=100)
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
    text = models.TextField(verbose_name='コメント', max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
