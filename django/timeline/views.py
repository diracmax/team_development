from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm, CommentForm, CommentReplyForm
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from .models import Post, Like, Apply, Comment, CommentReply, Notification, Category
from accounts.models import CustomUser
from django.http.response import JsonResponse
from django.http import HttpResponse, Http404


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'timeline/index.html'
    template_name = 'index2.html'
    paginate_by = 24

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categorys"] = Category.objects.filter(depth=0).order_by("-pk")
        return context

    def get_queryset(self):
        posts = Post.objects.order_by('-created_at')
        return posts


class CreateView(LoginRequiredMixin, generic.CreateView):
    form_class = PostForm
    template_name = 'timeline/create_post.html'
    template_name = 'create_post2.html'
    success_url = reverse_lazy('timeline:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categorys"] = Category.objects.all()
        return context

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

        try:
            like = Like(user=self.request.user, post=post)
            like.save()

            # Like notification is too anoying
            # notification = Notification.objects.create(
            #     notification_type=1, from_user=request.user, to_user=post.author, post=post)
            # notification.save()

            like_count = Like.objects.filter(post=post).count()
            data = {'like_count': like_count}
            return JsonResponse(data)
        except:
            like = Like.objects.get(user=self.request.user, post=post)
            like.delete()
            like_count = Like.objects.filter(post=post).count()
            data = {'like_count': like_count}
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

            notification = Notification.objects.create(
                notification_type=4, from_user=request.user, to_user=post.author, post=post)
            notification.save()

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
            application.is_member = not application.is_member
            application.save()

        return redirect(request.META['HTTP_REFERER'])


class PostDetail(LoginRequiredMixin, generic.DetailView):
    model = Post
    template_name = 'timeline/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ↓2回呼び出してるので処理がもったいない
        post = Post.objects.get(pk=self.kwargs.get('pk'))
        #
        category = post.category
        categorys = list()
        while category:
            categorys.append(category.display)
            category = category.parent
        categorys.reverse()
        context["categorys"] = categorys
        return context


class UpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    fields = ('title', 'text', 'photo', 'restriction',
              'capacity', 'is_recruited',
              #   'deadline', 'state_control_type'
              )
    template_name = 'timeline/update.html'
    template_name = 'post_update2.html'
    success_url = reverse_lazy('timeline:index')


class CommentView(LoginRequiredMixin, generic.CreateView):
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        pk = self.kwargs.get('pk')
        form.instance.post = Post.objects.get(pk=pk)

        notification = Notification.objects.create(
            notification_type=2, from_user=self.request.user, to_user=form.instance.post.author, post=form.instance.post)
        notification.save()

        messages.success(self.request, 'コメントが完了しました。')
        return super(CommentView, self).form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'コメントが失敗しました。')
        return redirect('timeline:detail', pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse('timeline:detail', kwargs={'pk': self.kwargs['pk']})


class DeleteCommentView(LoginRequiredMixin, generic.DeleteView):
    model = Comment

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author == request.user:
            messages.success(self.request, '削除しました。')
            return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        pk = self.kwargs['pk']
        comment = Comment.objects.get(pk=pk)
        return reverse('timeline:detail', kwargs={'pk': comment.post.id})


class DeleteCommentReplyView(LoginRequiredMixin, generic.DeleteView):
    model = CommentReply

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author == request.user:
            messages.success(self.request, '削除しました。')
            return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        pk = self.kwargs['pk']
        comment_reply = CommentReply.objects.get(pk=pk)
        return reverse('timeline:comment_reply_list', kwargs={'pk': comment_reply.parent.id})


class CommentReplyList(LoginRequiredMixin, generic.ListView):
    template_name = 'timeline/comment_list.html'
    paginate_by = 10

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        parent = Comment.objects.get(pk=pk)
        comment_replys = CommentReply.objects.filter(
            parent=parent).order_by('created_at')
        return comment_replys

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk')
        parent = Comment.objects.get(pk=pk)
        context = super().get_context_data(**kwargs)
        context['parent'] = parent
        return context


class CommentReplyView(LoginRequiredMixin, generic.CreateView):
    form_class = CommentReplyForm

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        pk = self.kwargs.get('pk')
        form.instance.parent = Comment.objects.get(pk=pk)
        messages.success(self.request, 'コメントが完了しました。')
        return super(CommentReplyView, self).form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'コメントが失敗しました。')
        return redirect('timeline:comment_reply_list', pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse('timeline:comment_reply_list', kwargs={'pk': self.kwargs['pk']})


class UpdateCommentView(LoginRequiredMixin, generic.UpdateView):
    model = Comment
    fields = ('text',)
    template_name = 'timeline/update_comment.html'

    def get_object(self):
        pk = self.kwargs['pk']
        comment = Comment.objects.get(pk=pk)
        return comment

    def get_success_url(self):
        pk = self.kwargs['pk']
        comment = Comment.objects.get(pk=pk)
        post = Post.objects.get(pk=comment.post.id)
        return reverse('timeline:detail', kwargs={'pk': post.id})


class UpdateCommentReplyView(LoginRequiredMixin, generic.UpdateView):
    model = CommentReply
    fields = ('text',)
    template_name = 'timeline/update_comment.html'

    def get_object(self):
        pk = self.kwargs['pk']
        comment_reply = CommentReply.objects.get(pk=pk)
        return comment_reply

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        comment_reply = CommentReply.objects.get(pk=pk)
        context["comment_reply"] = comment_reply
        return context

    def get_success_url(self):
        return reverse('timeline:comment_reply_list', kwargs={'pk': self.kwargs['pk']})


class PostNotification(generic.View):
    def get(self, request, notification_pk, object_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        notification.user_has_seen = True
        notification.save()
        return redirect('timeline:detail', pk=object_pk)


class MessageNotification(generic.View):
    def get(self, request, notification_pk, object_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        notification.user_has_seen = True
        notification.save()
        return redirect('dm:thread', pk=object_pk)


class FollowNotification(generic.View):
    def get(self, request, notification_pk, object_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        notification.user_has_seen = True
        notification.save()
        return redirect('accounts:detail', pk=object_pk)


class RemoveNotification(generic.View):
    def delete(self, request, notification_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        notification.user_has_seen = True
        notification.save()
        return HttpResponse('Success', content_type='text/plain')


class NotificationView(LoginRequiredMixin, generic.ListView):
    template_name = 'timeline/notification_list.html'
    paginate_by = 24

    def get_queryset(self):
        request_user = self.request.user
        notifications = Notification.objects.filter(
            to_user=request_user).order_by('-date')
        # to_user=request_user).exclude(user_has_seen=True).order_by('-date')
        return notifications


class PostRelatedAccountList(LoginRequiredMixin, generic.ListView):
    template_name = 'timeline/related_accounts.html'
    paginate_by = 10
    FILTER_DICT = {
        "like": {"display": "いいね", "id": "like__post_id", "option": None, "sort": "-like__created_at"},
        "entry": {"display": "応募者", "id": "apply__post_id", "option": {"apply__is_member": False}, "sort": "-apply__created_at"},
        "join": {"display": "メンバー", "id": "apply__post_id", "option": {"apply__is_member": True}, "sort": "-apply__updated_at"},
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        FILTER = {key: value["display"]
                  for key, value in self.FILTER_DICT.items()}
        context["FILTER_DICT"] = FILTER
        context["filter"] = self.kwargs.get('filter')
        context["post"] = Post.objects.get(pk=self.kwargs.get('pk'))
        return context

    def get_queryset(self):
        post_id = self.kwargs.get('pk')
        filter = self.kwargs.get('filter')
        if filter in self.FILTER_DICT:
            dict_ = self.FILTER_DICT[filter]
            kwargs = dict_["option"] if dict_["option"] else dict()
            kwargs[dict_["id"]] = post_id
            return CustomUser.objects.filter(**kwargs).order_by(dict_["sort"])
        raise Http404("Question does not exist")


index = IndexView.as_view()
create = CreateView.as_view()
delete = DeleteView.as_view()
like = LikeView.as_view()
apply = ApplyView.as_view()
detail = PostDetail.as_view()
accept = AcceptApplicationView.as_view()
update = UpdateView.as_view()
comment = CommentView.as_view()
delete_comment = DeleteCommentView.as_view()
delete_comment_reply = DeleteCommentReplyView.as_view()
comment_reply = CommentReplyView.as_view()
comment_reply_list = CommentReplyList.as_view()
update_comment = UpdateCommentView.as_view()
update_comment_reply = UpdateCommentReplyView.as_view()
