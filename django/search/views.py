from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from timeline.models import Post, Apply
from accounts.models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.db.models import Q



class PostList(LoginRequiredMixin, generic.ListView):
    template_name = 'search/post.html'
    paginate_by = 10

    def get_queryset(self):
        q_word = self.request.GET.get('word')
        if q_word:
            object_list = Post.objects.filter(
                Q(title__icontains=q_word) | Q(text__icontains=q_word))
        else:
            object_list = []
        return object_list


class AccountList(LoginRequiredMixin, generic.ListView):
    template_name = 'search/account.html'
    paginate_by = 10

    def get_queryset(self):
        q_word = self.request.GET.get('word')
        if q_word:
            object_list = CustomUser.objects.filter(
                Q(username__icontains=q_word) | Q(description__icontains=q_word))
        else:
            object_list = []
        return object_list
