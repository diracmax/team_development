from django.contrib.admin.widgets import AdminDateWidget
from django import forms
from .models import Post, Comment, CommentReply


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('category', 'title', 'text', 'photo',
                  'restriction', 'deadline', 'capacity',
                  'state_control_type')
        widgets = {
            'deadline': AdminDateWidget(),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )


class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = CommentReply
        fields = ('text', )
