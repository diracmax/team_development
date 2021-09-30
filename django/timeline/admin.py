from django.contrib import admin
from .models import Post, Apply

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    fields = ['text', 'photo', 'is_recruited']
    list_display = ('id', 'author', 'text', 'photo', 'created_at', 'is_recruited')


class ApplyAdmin(admin.ModelAdmin):
    fields = ['is_member']
    list_display = ('id', 'is_member', 'post', 'user')

admin.site.register(Post, PostAdmin)
admin.site.register(Apply, ApplyAdmin)
