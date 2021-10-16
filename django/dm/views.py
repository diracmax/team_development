from django.views import generic
from django.shortcuts import render
from django.shortcuts import redirect
from .forms import ThreadForm, MessageForm
from .models import ThreadModel, MessageModel
from accounts.models import CustomUser
from django.db.models import Q
from django.contrib import messages
from timeline.utils import Util
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from timeline.models import Notification


class CreateThread(generic.View):
    def post(self, request, pk, *args, **kwargs):
        try:
            receiver = CustomUser.objects.get(pk=pk)

            if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
                thread = ThreadModel.objects.filter(
                    user=request.user, receiver=receiver)[0]
                return redirect('dm:thread', pk=thread.pk)

            if ThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
                thread = ThreadModel.objects.filter(
                    user=receiver, receiver=request.user)[0]
                return redirect('dm:thread', pk=thread.pk)

            sender_thread = ThreadModel(
                user=request.user,
                receiver=receiver
            )
            sender_thread.save()
            thread_pk = sender_thread.pk
            return redirect('dm:thread', pk=thread_pk)
        except:
            messages.error(self.request, 'ユーザーが見つかりませんでした。')
            return redirect('dm:create-thread')


class ListThreads(generic.View):
    def get(self, request, *args, **kwargs):
        threads = ThreadModel.objects.filter(
            Q(user=request.user) | Q(receiver=request.user))
        context = {
            'threads': threads,
        }
        return render(request, 'dm/inbox.html', context)


class CreateMessage(generic.View):
    def post(self, request, pk, *args, **kwargs):
        thread = ThreadModel.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver
        message = MessageModel(
            thread=thread,
            sender_user=request.user,
            receiver_user=receiver,
            body=request.POST.get('message'),
        )
        if len(message.body) <= 60:
            thread.last_message = message.body
        else:
            thread.last_message = message.body[:59]+"..."
        message.save()
        thread.save()

        if receiver.is_active == True:

            notification = Notification.objects.create(
                notification_type=5, from_user=request.user, to_user=receiver, thread=thread)
            notification.save()

            current_site = "localhost:8000"
            relativeLink = "/inbox/" + str(pk) + "/"
            absurl = 'http://'+current_site+relativeLink
            email_body = "こんにちは "+receiver.username + "さん\n" + \
                request.user.username+'さんから新規メッセージが届いています。\n' + absurl
            data = {'email_body': email_body, 'to_email': receiver.email,
                    'email_subject': request.user.username+'さんから新規メッセージがあります'}
            Util.send_email(data)

        return redirect('dm:thread', pk=pk)


class ThreadView(generic.View):
    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        thread = ThreadModel.objects.get(pk=pk)
        message_list = MessageModel.objects.filter(thread__pk__contains=pk)
        context = {
            'thread': thread,
            'form': form,
            'message_list': message_list
        }
        return render(request, 'dm/thread.html', context)
