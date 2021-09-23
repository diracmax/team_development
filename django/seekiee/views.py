from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from .forms import PostForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Posts

# Create your views here.
class IndexView(ListView):
    template_name ='seekiee/index.html'
    queryset = Posts.objects.order_by('-posted_at')
    paginate_by = 9


@method_decorator(login_required, name='dispatch')
class CreatePostView(CreateView):
    form_class = PostForm
    template_name = "seekiee/post.html"
    success_url = reverse_lazy('seekiee:index')

    def form_valid(self, form):
        postdata = form.save(commit=False)
        postdata.user = self.request.user
        postdata.save()
        return super().form_valid(form)


class MyPostView(ListView):
    template_name ='seekiee/my_post.html'
    paginate_by = 9

    def get_queryset(self):
        queryset = Posts.objects.filter(user=self.request.user).order_by('-posted_at')
        return queryset


class DetailView(DetailView):
    template_name ='seekiee/post_detail.html'
    model = Posts


class DeleteView(DeleteView):
    model = Posts
    template_name = 'seekiee/post_delete.html'
    success_url = reverse_lazy('seekiee:index')

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)