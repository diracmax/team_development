from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.shortcuts import redirect
from .forms import ProfileForm
from django.contrib.messages.views import SuccessMessageMixin
from timeline.models import Post

QUERY_DICT = {
    "like": {
        "display": "いいね",
        "custom": {
            "table": "like",
            "column": "created_at"
        }
    },
    "entry": {
        "display": "応募",
        "custom": {
            "table": "apply",
            "column": "created_at"
        }
    },
    "join": {
        "display": "参加",
        "custom": {
            "table": "apply",
            "column": "updated_at"
        }
    },
    "recruit": {
        "display": "募集",
        "custom": False
    }
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
        context["title"] = owner + "の" + QUERY_DICT[query]["display"] + "一覧"
        context["name"] = owner
        context["QUERY_DICT"] = QUERY_DICT
        return context
        
        
    def get_queryset(self):
        id = self.kwargs.get('pk', 0)
        query = self.kwargs.get('query', 0)
        if query in QUERY_DICT:
            if not QUERY_DICT[query]["custom"]:
                keyword = "author_id"
                order = "-created_at"
            else:
                keyword = QUERY_DICT[query]["custom"]["table"] + "__user_id"
                order = "-" + QUERY_DICT[query]["custom"]["table"] + "__" + QUERY_DICT[query]["custom"]["column"]
            posts = Post.objects.filter(**{keyword: id})
            return posts.order_by(order)
        raise ValueError("This URL is forbidden. allowed is following:\n" + ",\n".join(["    \"/accounts/[user_id]/"+key+"\"" for key in QUERY_DICT]))
            

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