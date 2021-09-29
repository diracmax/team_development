from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import Post, Like, Apply
from accounts.models import CustomUser
from django.http.response import JsonResponse


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'index.html'
    paginate_by = 10

    def get_queryset(self):
        posts = Post.objects.order_by('-created_at')
        return posts


class CreateView(LoginRequiredMixin, generic.CreateView):
    form_class = PostForm
    success_url = reverse_lazy('timeline:index')

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        messages.success(self.request, '投稿が完了しました。')
        return super(CreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, '投稿が失敗しました。')
        return redirect('timeline:index')


class DeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy('timeline:index')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author == request.user:
            messages.success(self.request, '削除しました。')
            return super().delete(request, *args, **kwargs)


class LikeView(LoginRequiredMixin, generic.View):
    model = Like

    def post(self, request):
        post_id = request.POST.get('id')
        post = Post.objects.get(id=post_id)
        like = Like(user=self.request.user, post=post)
        like.save()
        like_count = Like.objects.filter(post=post).count()
        data = {'message': 'いいねしました',
                'like_count': like_count}
        return JsonResponse(data)


class ApplyView(LoginRequiredMixin, generic.View):
    model = Apply

    def post(self, request):
        post_id = request.POST.get('id')
        post = Post.objects.get(id=post_id)

        try:
            # if it already exists, it violates unique constraints
            apply = Apply(user=self.request.user, post=post)
            apply.save()
            apply_count = Apply.objects.filter(post=post).count()
            data = {'message': '応募しました',
                    'apply_count': apply_count}
            return JsonResponse(data)
        except:
            apply = Apply.objects.get(user=self.request.user, post=post)
            apply.delete()
            apply_count = Apply.objects.filter(post=post).count()
            data = {'message': '応募を取り下げました',
                    'apply_count': apply_count}
            return JsonResponse(data)


class AcceptApplicationView(LoginRequiredMixin, generic.View):
    model = Apply

    def post(self, request, post_id, user_id):
        post = Post.objects.get(id=post_id)
        user = CustomUser.objects.get(id=user_id)

        if self.request.user == post.author:
            application = Apply.objects.get(post=post, user=user)
            application.is_member = True
            application.save()

        return redirect(request.META['HTTP_REFERER'])


class PostDetail(LoginRequiredMixin, generic.DetailView):
    model = Post
    template_name = 'detail.html'


index = IndexView.as_view()
create = CreateView.as_view()
delete = DeleteView.as_view()
like = LikeView.as_view()
apply = ApplyView.as_view()
detail = PostDetail.as_view()
accept = AcceptApplicationView.as_view()
