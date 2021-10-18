from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from timeline.models import Post, Apply
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.db.models import Q



class PostList(LoginRequiredMixin, generic.ListView):
    template_name = 'search/post.html'
    paginate_by = 10

    def get_queryset(self):
        q = dict()
        q["word"] = self.request.GET.get('word')
        q["category"] = self.request.GET.get('category')
        if q["word"] and q["category"]:
            object_list = Post.objects.filter(
                    Q(title__icontains=q["word"]) | Q(text__icontains=q["word"]),
                    Q(category__dispaly=q["category"])
                    )
            return object_list
        if q["word"]:
            object_list = Post.objects.filter(
                    Q(title__icontains=q["word"]) | Q(text__icontains=q["word"])
                    )
            return object_list
        if q["category"]:
            object_list = Post.objects.filter(
                    Q(category__display=q["category"])
                    )
            return object_list
        return Post.objects.all()