from django import forms
# from .models import CustomUser


class ThreadForm(forms.Form):
    username = forms.CharField(label='', max_length=100)


class MessageForm(forms.Form):
    message = forms.CharField(label='', max_length=1000)
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['message'].widget = forms.Textarea(attrs={'rows': '3', 'placeholder': 'メッセージを入力'})
        self.fields['message'].widget.attrs['class'] = 'form-control'
