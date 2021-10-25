from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from accounts.models import CustomUser
from timeline.models import Post, Apply, Category
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.db.models import Q



class PostList(LoginRequiredMixin, generic.ListView):
    template_name = 'search/post.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categorys"] = Category.objects.filter(depth=0).order_by("-pk")
        return context

    def get_queryset(self):
        q = dict()
        q["word"] = self.request.GET.get('word')
        q["category"] = self.request.GET.get('category')
        # print("word=" + q["word"])
        # print("category=" + q["category"])
        if q["word"] and q["category"]:
            object_list = Post.objects.filter(
                    Q(title__icontains=q["word"]) | Q(text__icontains=q["word"]),
                    Q(category__display=q["category"])
                    )
            return object_list
        if q["word"]:
            object_list = Post.objects.filter(
                    Q(title__icontains=q["word"]) | Q(text__icontains=q["word"])
                    )
            return object_list
        if q["category"]:
            # 子カテゴリも含めて表示したい
            object_list = Post.objects.filter(
                    Q(category__display=q["category"])
                    )
            return object_list
        return Post.objects.all()

class AccountList(LoginRequiredMixin, generic.ListView):
    template_name = 'search/account.html'
    paginate_by = 10

    def get_queryset(self):
        q = dict()
        q["word"] = self.request.GET.get('word')
        # q_apply = self.request.GET.get('apply')
        # if q_apply:
        #     q_apply = q_apply.split("-", 1)
        #     q["post_id"] = q_apply[0]
        #     q["is_member"] = True if q_apply[1]=="member" else False

        # if q["word"] and q["apply"]:
        #     object_list = CustomUser.objects.filter(
        #         Q(username__icontains=q["word"]),
        #         Q(apply__post_id=q["post_id"]),
        #         Q(apply__is_member=q["is_member"])
        #         )

        # if q["apply"]:
        #     object_list = CustomUser.objects.filter(
        #         Q(apply__post_id=q["post_id"]),
        #         Q(apply__is_member=q["is_member"])
        #         )

        if q["word"]:
            object_list = CustomUser.objects.filter(
                Q(username__icontains=q["word"]))
        else:
            object_list = CustomUser.objects.all()
        return object_list