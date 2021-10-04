from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'photo',
                  'recruitment_conditions', 'capacity')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )
