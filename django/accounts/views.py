from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .forms import ProfileForm
from django.contrib.messages.views import SuccessMessageMixin

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

edit = ProfileEdit.as_view()
detail = ProfileDetail.as_view()
