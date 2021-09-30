from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .forms import ProfileForm
from django.contrib.messages.views import SuccessMessageMixin
from timeline.models import Post, Apply

QUERY_DICT = {
    "like": "いいね",
    "entry": "応募",
    "join": "参加",
    "recruit": "募集",
}

class ProfileEdit(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = CustomUser
    form_class = ProfileForm
    template_name = 'account/edit.html'
    success_url = '/accounts/edit/'
    success_message = 'プロフィールを更新しました。'

    def get_object(self):
        return self.request.user

class ProfileDetail(LoginRequiredMixin, generic.DetailView):
    model = CustomUser
    template_name = 'account/detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["QUERY_DICT"] = QUERY_DICT
        return context

class PostList(LoginRequiredMixin, generic.ListView):
    template_name = 'account/related_posts.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.kwargs.get('query', "")
        owner = CustomUser.objects.get(id=self.kwargs.get('pk', 0)).username
        context["title"] = owner + "の" + QUERY_DICT[query] + "一覧"
        context["name"] = owner
        context["QUERY_DICT"] = QUERY_DICT
        return context
        
        
    def get_queryset(self):
        id = self.kwargs.get('pk', 0)
        query = self.kwargs.get('query', 0)
        if query == "recruit":
            posts = Post.objects.filter(author_id=id)
            return posts.order_by('-created_at')
        if query == "like":
            posts = Post.objects.filter(like__user_id=id)
            return posts.order_by('-created_at')
        if query == "entry":
            posts = Post.objects.filter(apply__user_id=id, apply__is_member=False)
            return posts.order_by('-created_at')
        if query == "join":
            posts = Post.objects.filter(apply__user_id=id, apply__is_member=True)
            return posts.order_by('-created_at')
        raise ValueError("invarid url")
            

edit = ProfileEdit.as_view()
detail = ProfileDetail.as_view()
