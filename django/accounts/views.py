from .models import CustomUser, Follow
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.shortcuts import redirect
from .forms import ProfileForm
from django.contrib.messages.views import SuccessMessageMixin
from timeline.models import Post, Apply
from django.http.response import JsonResponse
from django.db import connection

QUERY_DICT = {
    "like": "いいね",
    "entry": "応募",
    "join": "参加",
    "recruit": "募集",
    "follow": "フォロー",
    "follower": "フォロワー",
}

SORT_DICT = {
    "post": {
        "allowed": ["like", "entry", "join", "recruit"],
        "display": "投稿日時",
        "method": "created_at"
    },
    "edit": {
        "allowed": ["like", "entry", "join", "recruit"],
        "display": "更新日時",
        "method": "updated_at"
    },
    "like": {
        "allowed": ["like"],
        "display": "いいね日時",
        "method": "like__created_at"
    },
    "entry": {
        "allowed": ["entry", "join"],
        "display": "応募日時",
        "method": "apply__created_at"
    },
    "join": {
        "allowed": ["join"],
        "display": "参加日時",
        "method": "apply__updated_at"
    },
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


class FollowView(LoginRequiredMixin, generic.View):
    model = Follow

    def post(self, request):
        following_id = request.POST.get('id')
        following = CustomUser.objects.get(id=following_id)

        try:
            # if it already exists, it violates unique constraints
            follow = Follow(follower=self.request.user, following=following)
            follow.save()
            follow_count = Follow.objects.filter(following=following).count()
            data = {'message': 'フォローしました',
                    'follow_count': follow_count}
            return JsonResponse(data)

        except:
            follow = Follow.objects.get(follower=self.request.user, following=following)
            follow.delete()
            follow_count = Follow.objects.filter(following=following).count()
            data = {'message': 'フォロー解除しました',
                    'follow_count': follow_count}
            return JsonResponse(data)


class PostList(LoginRequiredMixin, generic.ListView):
    template_name = 'account/related_posts.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.kwargs.get('query', "")
        owner = CustomUser.objects.get(id=self.kwargs.get('pk', 0))
        context["title"] = owner.username + "の" + QUERY_DICT[query] + "一覧"
        context["account"] = owner
        context["QUERY_DICT"] = QUERY_DICT
        context["SORT_DICT"] = SORT_DICT
        return context

    def get_queryset(self):
        id = self.kwargs.get('pk', 0)
        query = self.kwargs.get('query', 0)
        if query == "recruit":
            posts = Post.objects.filter(author_id=id)
            if self.request.GET.get("order"):
                return posts.order_by(self.request.GET.get("order"))
            return posts.order_by('-created_at')
        if query == "like":
            posts = Post.objects.filter(like__user_id=id)
            if self.request.GET.get("order"):
                return posts.order_by(self.request.GET.get("order"))
            return posts.order_by('-like__created_at')
        if query == "entry":
            posts = Post.objects.filter(apply__user_id=id, apply__is_member=False)
            if self.request.GET.get("order"):
                return posts.order_by(self.request.GET.get("order"))
            return posts.order_by('-apply__created_at')
        if query == "join":
            posts = Post.objects.filter(apply__user_id=id, apply__is_member=True)
            if self.request.GET.get("order"):
                return posts.order_by(self.request.GET.get("order"))
            return posts.order_by('-apply__updated_at')
        if query == "follower":
            accounts = CustomUser.objects.raw('SELECT * FROM accounts_customuser JOIN accounts_follow ON accounts_customuser.id = accounts_follow.follower_id WHERE following_id = %s', str(id))
            return accounts
        if query == "follow":
            accounts = CustomUser.objects.raw('SELECT * FROM accounts_customuser JOIN accounts_follow ON accounts_customuser.id = accounts_follow.following_id WHERE follower_id = %s', str(id))
            return accounts
        raise ValueError("invarid url")


class QuitView(LoginRequiredMixin, generic.View):
    model = CustomUser

    def post(self, request):
        record = CustomUser.objects.get(id=request.user.id)
        record.is_active = False
        record.save()
        return redirect('timeline:index')



edit = ProfileEdit.as_view()
detail = ProfileDetail.as_view()
quit = QuitView.as_view()
postlist = PostList.as_view()
follow = FollowView.as_view()
