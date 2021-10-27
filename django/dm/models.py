from django.db import models
from django.utils import timezone
from accounts.models import CustomUser


class ThreadModel(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='+')
    receiver = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='+')
    has_unread = models.BooleanField(default=False)
    last_message = models.CharField(max_length=1000, default="")
    updated_at = models.DateTimeField(auto_now=True)


class MessageModel(models.Model):
    thread = models.ForeignKey(
        'ThreadModel', related_name='+', on_delete=models.CASCADE, blank=True, null=True)
    sender_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='+')
    receiver_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='+')
    body = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
